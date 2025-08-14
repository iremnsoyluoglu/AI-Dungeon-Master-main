const express = require("express");
const http = require("http");
const https = require("https");
const { EventEmitter } = require("events");

class LoadBalancer extends EventEmitter {
  constructor(options = {}) {
    super();
    this.servers = [];
    this.currentIndex = 0;
    this.healthCheckInterval = options.healthCheckInterval || 30000; // 30 seconds
    this.strategy = options.strategy || "round-robin"; // round-robin, least-connections, weighted
    this.healthCheckPath = options.healthCheckPath || "/health";
    this.maxRetries = options.maxRetries || 3;
    this.retryDelay = options.retryDelay || 1000;

    this.serverStats = new Map(); // Track server statistics
    this.healthStatus = new Map(); // Track health status
    this.connectionCounts = new Map(); // Track active connections

    this.startHealthChecks();
  }

  addServer(server) {
    const serverConfig = {
      id: server.id || `server-${this.servers.length + 1}`,
      host: server.host,
      port: server.port,
      protocol: server.protocol || "http",
      weight: server.weight || 1,
      maxConnections: server.maxConnections || 100,
      healthCheck: server.healthCheck !== false,
      ...server,
    };

    this.servers.push(serverConfig);
    this.serverStats.set(serverConfig.id, {
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      averageResponseTime: 0,
      lastResponseTime: 0,
      uptime: Date.now(),
      activeConnections: 0,
    });

    this.healthStatus.set(serverConfig.id, {
      healthy: true,
      lastCheck: Date.now(),
    });
    this.connectionCounts.set(serverConfig.id, 0);

    console.log(
      `✅ Server added to load balancer: ${serverConfig.host}:${serverConfig.port}`
    );
    this.emit("serverAdded", serverConfig);
  }

  removeServer(serverId) {
    const index = this.servers.findIndex((server) => server.id === serverId);
    if (index !== -1) {
      const server = this.servers.splice(index, 1)[0];
      this.serverStats.delete(serverId);
      this.healthStatus.delete(serverId);
      this.connectionCounts.delete(serverId);
      console.log(
        `❌ Server removed from load balancer: ${server.host}:${server.port}`
      );
      this.emit("serverRemoved", server);
    }
  }

  getNextServer() {
    const healthyServers = this.servers.filter((server) => {
      const status = this.healthStatus.get(server.id);
      return status && status.healthy;
    });

    if (healthyServers.length === 0) {
      throw new Error("No healthy servers available");
    }

    switch (this.strategy) {
      case "round-robin":
        return this.getNextRoundRobin(healthyServers);
      case "least-connections":
        return this.getLeastConnections(healthyServers);
      case "weighted":
        return this.getWeightedServer(healthyServers);
      case "ip-hash":
        return this.getIpHashServer(healthyServers);
      default:
        return this.getNextRoundRobin(healthyServers);
    }
  }

  getNextRoundRobin(servers) {
    const server = servers[this.currentIndex % servers.length];
    this.currentIndex = (this.currentIndex + 1) % servers.length;
    return server;
  }

  getLeastConnections(servers) {
    let minConnections = Infinity;
    let selectedServer = null;

    for (const server of servers) {
      const connections = this.connectionCounts.get(server.id) || 0;
      if (connections < minConnections) {
        minConnections = connections;
        selectedServer = server;
      }
    }

    return selectedServer;
  }

  getWeightedServer(servers) {
    const totalWeight = servers.reduce((sum, server) => sum + server.weight, 0);
    let random = Math.random() * totalWeight;

    for (const server of servers) {
      random -= server.weight;
      if (random <= 0) {
        return server;
      }
    }

    return servers[0]; // Fallback
  }

  getIpHashServer(servers) {
    // This would be implemented with actual client IP
    // For now, using a simple hash
    const hash = Math.floor(Math.random() * servers.length);
    return servers[hash];
  }

  async healthCheck(server) {
    try {
      const startTime = Date.now();
      const protocol = server.protocol === "https" ? https : http;

      const response = await new Promise((resolve, reject) => {
        const req = protocol.request(
          {
            hostname: server.host,
            port: server.port,
            path: this.healthCheckPath,
            method: "GET",
            timeout: 5000,
          },
          (res) => {
            let data = "";
            res.on("data", (chunk) => (data += chunk));
            res.on("end", () => {
              resolve({
                statusCode: res.statusCode,
                data: data,
                responseTime: Date.now() - startTime,
              });
            });
          }
        );

        req.on("error", reject);
        req.on("timeout", () => reject(new Error("Health check timeout")));
        req.end();
      });

      const isHealthy = response.statusCode >= 200 && response.statusCode < 500;
      const status = this.healthStatus.get(server.id);

      if (status) {
        status.healthy = isHealthy;
        status.lastCheck = Date.now();
        status.lastResponseTime = response.responseTime;
      }

      const stats = this.serverStats.get(server.id);
      if (stats) {
        stats.lastResponseTime = response.responseTime;
        if (isHealthy) {
          stats.successfulRequests++;
        } else {
          stats.failedRequests++;
        }
      }

      console.log(
        `🏥 Health check for ${server.host}:${server.port} - ${
          isHealthy ? "✅ Healthy" : "❌ Unhealthy"
        }`
      );
      this.emit("healthCheck", {
        server,
        healthy: isHealthy,
        responseTime: response.responseTime,
      });
    } catch (error) {
      console.error(
        `❌ Health check failed for ${server.host}:${server.port}:`,
        error.message
      );

      const status = this.healthStatus.get(server.id);
      if (status) {
        status.healthy = false;
        status.lastCheck = Date.now();
      }

      const stats = this.serverStats.get(server.id);
      if (stats) {
        stats.failedRequests++;
      }

      this.emit("healthCheck", {
        server,
        healthy: false,
        error: error.message,
      });
    }
  }

  startHealthChecks() {
    setInterval(() => {
      this.servers.forEach((server) => {
        if (server.healthCheck) {
          this.healthCheck(server);
        }
      });
    }, this.healthCheckInterval);
  }

  incrementConnectionCount(serverId) {
    const count = this.connectionCounts.get(serverId) || 0;
    this.connectionCounts.set(serverId, count + 1);
  }

  decrementConnectionCount(serverId) {
    const count = this.connectionCounts.get(serverId) || 0;
    this.connectionCounts.set(serverId, Math.max(0, count - 1));
  }

  getStats() {
    const stats = {
      totalServers: this.servers.length,
      healthyServers: this.servers.filter((server) => {
        const status = this.healthStatus.get(server.id);
        return status && status.healthy;
      }).length,
      strategy: this.strategy,
      servers: this.servers.map((server) => {
        const serverStats = this.serverStats.get(server.id);
        const healthStatus = this.healthStatus.get(server.id);
        const connectionCount = this.connectionCounts.get(server.id) || 0;

        return {
          id: server.id,
          host: server.host,
          port: server.port,
          protocol: server.protocol,
          weight: server.weight,
          healthy: healthStatus ? healthStatus.healthy : false,
          lastCheck: healthStatus ? healthStatus.lastCheck : null,
          activeConnections: connectionCount,
          totalRequests: serverStats ? serverStats.totalRequests : 0,
          successfulRequests: serverStats ? serverStats.successfulRequests : 0,
          failedRequests: serverStats ? serverStats.failedRequests : 0,
          averageResponseTime: serverStats
            ? serverStats.averageResponseTime
            : 0,
          uptime: serverStats ? Date.now() - serverStats.uptime : 0,
        };
      }),
    };

    return stats;
  }
}

// LLM Load Balancer
class LLMLoadBalancer extends LoadBalancer {
  constructor(options = {}) {
    super({ ...options, strategy: options.strategy || "least-connections" });
    this.llmServices = new Map();
    this.responseTimes = new Map();
  }

  addLLMService(service) {
    this.addServer(service);
    this.llmServices.set(service.id, service);
    this.responseTimes.set(service.id, []);
    console.log(`🤖 LLM Service added: ${service.name} (${service.type})`);
  }

  selectLLMService(requirements = {}) {
    const availableServices = this.servers.filter((server) => {
      const service = this.llmServices.get(server.id);
      if (!service) return false;

      // Check capabilities
      if (requirements.capabilities) {
        const hasCapability = requirements.capabilities.some((cap) =>
          service.capabilities.includes(cap)
        );
        if (!hasCapability) return false;
      }

      // Check max tokens
      if (
        requirements.maxTokens &&
        service.maxTokens < requirements.maxTokens
      ) {
        return false;
      }

      return true;
    });

    if (availableServices.length === 0) {
      throw new Error("No suitable LLM service available");
    }

    return this.getNextServer(availableServices);
  }

  async forwardLLMRequest(req, res) {
    try {
      const selectedService = this.selectLLMService({
        capabilities: req.body.capabilities || ["text-generation"],
        maxTokens: req.body.max_tokens || 1000,
      });

      const startTime = Date.now();
      this.incrementConnectionCount(selectedService.id);

      const response = await this.forwardRequest(selectedService, req, res);

      const responseTime = Date.now() - startTime;
      this.updateServerStats(selectedService.id, true, responseTime);

      this.decrementConnectionCount(selectedService.id);

      return response;
    } catch (error) {
      console.error("LLM Load Balancer error:", error);
      res.status(500).json({ error: "LLM service unavailable" });
    }
  }

  async forwardRequest(server, req, res) {
    // Mock response since backend servers are not running
    const mockResponse = {
      success: true,
      server: server.name || server.id,
      timestamp: new Date().toISOString(),
      message: "LLM request forwarded successfully",
      type: "llm",
      response: "This is a mock LLM response",
    };

    res.status(200).json(mockResponse);
    return Promise.resolve();
  }

  updateServerStats(serverId, success, responseTime) {
    const times = this.responseTimes.get(serverId) || [];
    times.push(responseTime);
    if (times.length > 10) times.shift();
    this.responseTimes.set(serverId, times);
  }
}

// Game Engine Load Balancer
class GameEngineLoadBalancer extends LoadBalancer {
  constructor(options = {}) {
    super({ ...options, strategy: options.strategy || "round-robin" });
    this.gameEngines = new Map();
    this.sessionCounts = new Map();
  }

  addGameEngine(engine) {
    this.addServer(engine);
    this.gameEngines.set(engine.id, engine);
    this.sessionCounts.set(engine.id, 0);
    console.log(`🎮 Game Engine added: ${engine.name}`);
  }

  selectGameEngine(requirements = {}) {
    const availableEngines = this.servers.filter((server) => {
      const engine = this.gameEngines.get(server.id);
      if (!engine) return false;

      // Check game type
      if (
        requirements.gameType &&
        !engine.gameTypes.includes(requirements.gameType)
      ) {
        return false;
      }

      // Check features
      if (requirements.features) {
        const hasFeature = requirements.features.some((feature) =>
          engine.features.includes(feature)
        );
        if (!hasFeature) return false;
      }

      // Check session capacity
      const currentSessions = this.sessionCounts.get(server.id) || 0;
      if (currentSessions >= engine.maxSessions) {
        return false;
      }

      return true;
    });

    if (availableEngines.length === 0) {
      throw new Error("No suitable game engine available");
    }

    return this.getNextServer(availableEngines);
  }

  async forwardGameRequest(req, res) {
    try {
      const selectedEngine = this.selectGameEngine({
        gameType: req.body.gameType,
        features: req.body.features || [],
      });

      const startTime = Date.now();
      this.incrementConnectionCount(selectedEngine.id);
      this.sessionCounts.set(
        selectedEngine.id,
        (this.sessionCounts.get(selectedEngine.id) || 0) + 1
      );

      await this.forwardRequest(selectedEngine, req, res);

      const responseTime = Date.now() - startTime;
      this.updateServerStats(selectedEngine.id, true, responseTime);

      this.decrementConnectionCount(selectedEngine.id);
    } catch (error) {
      console.error("Game Engine Load Balancer error:", error);
      if (!res.headersSent) {
        res.status(500).json({ error: "Game engine unavailable" });
      }
    }
  }

  async forwardRequest(server, req, res) {
    // Mock response since backend servers are not running
    const mockResponse = {
      success: true,
      server: server.name || server.id,
      timestamp: new Date().toISOString(),
      message: "Game request forwarded successfully",
      type: "game",
      response: "Game engine response",
    };

    res.status(200).json(mockResponse);
    return Promise.resolve();
  }

  updateServerStats(serverId, success, responseTime) {
    // Update session counts based on success/failure
    const currentSessions = this.sessionCounts.get(serverId) || 0;
    if (success) {
      this.sessionCounts.set(serverId, Math.max(0, currentSessions - 1));
    }
  }
}

// API Server Load Balancer
class APIServerLoadBalancer extends LoadBalancer {
  constructor(options = {}) {
    super({ ...options, strategy: options.strategy || "least-connections" });
    this.requestCounts = new Map();
    this.errorRates = new Map();
  }

  addAPIServer(server) {
    this.addServer(server);
    this.requestCounts.set(server.id, 0);
    this.errorRates.set(server.id, 0);
    console.log(`🌐 API Server added: ${server.host}:${server.port}`);
  }

  async forwardAPIRequest(req, res) {
    try {
      const selectedServer = this.getNextServer();
      const startTime = Date.now();

      this.incrementConnectionCount(selectedServer.id);
      this.requestCounts.set(
        selectedServer.id,
        (this.requestCounts.get(selectedServer.id) || 0) + 1
      );

      await this.forwardRequest(selectedServer, req, res);

      const responseTime = Date.now() - startTime;
      this.updateServerStats(selectedServer.id, true, responseTime);

      this.decrementConnectionCount(selectedServer.id);
    } catch (error) {
      console.error("API Load Balancer error:", error);
      if (!res.headersSent) {
        res.status(500).json({ error: "API server unavailable" });
      }
    }
  }

  async forwardRequest(server, req, res) {
    // Mock response since backend servers are not running
    const mockResponse = {
      success: true,
      server: server.name || server.id,
      timestamp: new Date().toISOString(),
      message: "API request forwarded successfully",
      type: "api",
      response: "API response",
    };

    res.status(200).json(mockResponse);
    return Promise.resolve();
  }

  updateServerStats(serverId, success, responseTime) {
    // Update error rates based on success/failure
    const currentErrorRate = this.errorRates.get(serverId) || 0;
    if (!success) {
      this.errorRates.set(serverId, currentErrorRate + 1);
    } else {
      this.errorRates.set(serverId, Math.max(0, currentErrorRate - 0.1));
    }
  }

  getServerWithLowestErrorRate() {
    let minErrorRate = Infinity;
    let selectedServer = null;

    for (const server of this.servers) {
      const errorRate = this.errorRates.get(server.id) || 0;
      if (errorRate < minErrorRate) {
        minErrorRate = errorRate;
        selectedServer = server;
      }
    }

    return selectedServer;
  }
}

module.exports = {
  LoadBalancer,
  LLMLoadBalancer,
  GameEngineLoadBalancer,
  APIServerLoadBalancer,
};
