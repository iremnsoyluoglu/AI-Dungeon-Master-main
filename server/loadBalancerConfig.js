const {
  LoadBalancer,
  LLMLoadBalancer,
  GameEngineLoadBalancer,
  APIServerLoadBalancer,
} = require("./loadBalancer");

// LLM Services Configuration
const llmServices = [
  {
    id: "openai-gpt4",
    name: "OpenAI GPT-4",
    type: "openai",
    host: "api.openai.com",
    port: 443,
    protocol: "https",
    capabilities: ["text-generation", "chat"],
    maxTokens: 4096,
    costPerToken: 0.00003,
    weight: 3,
  },
  {
    id: "openai-gpt35",
    name: "OpenAI GPT-3.5",
    type: "openai",
    host: "api.openai.com",
    port: 443,
    protocol: "https",
    capabilities: ["text-generation", "chat"],
    maxTokens: 4096,
    costPerToken: 0.000002,
    weight: 2,
  },
  {
    id: "anthropic-claude",
    name: "Anthropic Claude",
    type: "anthropic",
    host: "api.anthropic.com",
    port: 443,
    protocol: "https",
    capabilities: ["text-generation", "chat"],
    maxTokens: 100000,
    costPerToken: 0.000015,
    weight: 3,
  },
  {
    id: "local-llama",
    name: "Local Llama",
    type: "local",
    host: "localhost",
    port: 8010,
    protocol: "http",
    capabilities: ["text-generation"],
    maxTokens: 2048,
    costPerToken: 0.000001,
    weight: 1,
  },
  {
    id: "local-mistral",
    name: "Local Mistral",
    type: "local",
    host: "localhost",
    port: 8011,
    protocol: "http",
    capabilities: ["text-generation"],
    maxTokens: 2048,
    costPerToken: 0.000001,
    weight: 1,
  },
];

// Game Engine Services Configuration
const gameEngines = [
  {
    id: "fantasy-engine-1",
    name: "Fantasy Game Engine 1",
    type: "fantasy",
    host: "localhost",
    port: 5020,
    protocol: "http",
    capabilities: ["combat", "quest", "npc"],
    weight: 2,
  },
  {
    id: "fantasy-engine-2",
    name: "Fantasy Game Engine 2",
    type: "fantasy",
    host: "localhost",
    port: 5021,
    protocol: "http",
    capabilities: ["combat", "quest", "npc"],
    weight: 2,
  },
  {
    id: "scifi-engine-1",
    name: "Sci-Fi Game Engine 1",
    type: "scifi",
    host: "localhost",
    port: 5022,
    protocol: "http",
    capabilities: ["combat", "quest", "npc"],
    weight: 2,
  },
  {
    id: "horror-engine-1",
    name: "Horror Game Engine 1",
    type: "horror",
    host: "localhost",
    port: 5023,
    protocol: "http",
    capabilities: ["combat", "quest", "npc"],
    weight: 2,
  },
  {
    id: "universal-engine-1",
    name: "Universal Game Engine 1",
    type: "universal",
    host: "localhost",
    port: 5024,
    protocol: "http",
    capabilities: ["combat", "quest", "npc"],
    weight: 3,
  },
];

// API Server Services Configuration
const apiServers = [
  {
    id: "api-server-1",
    name: "API Server 1",
    host: "localhost",
    port: 5030,
    protocol: "http",
    capabilities: ["scenarios", "characters", "combat"],
    weight: 2,
  },
  {
    id: "api-server-2",
    name: "API Server 2",
    host: "localhost",
    port: 5031,
    protocol: "http",
    capabilities: ["scenarios", "characters", "combat"],
    weight: 2,
  },
];

// Initialize Load Balancers
const llmLoadBalancer = new LLMLoadBalancer({
  strategy: "weighted",
  healthCheckInterval: 30000,
});

const gameEngineLoadBalancer = new GameEngineLoadBalancer({
  strategy: "round-robin",
  healthCheckInterval: 30000,
});

const apiServerLoadBalancer = new APIServerLoadBalancer({
  strategy: "least-connections",
  healthCheckInterval: 30000,
});

// Add servers to load balancers (şimdilik devre dışı)
console.log("⚠️ Load balancer servisleri devre dışı, mock mod kullanılıyor");

// gameEngines.forEach((engine) => {
//   gameEngineLoadBalancer.addGameEngine(engine);
// });

// apiServers.forEach((server) => {
//   apiServerLoadBalancer.addAPIServer(server);
// });

// Start health checks
// llmLoadBalancer.startHealthChecks();
// gameEngineLoadBalancer.startHealthChecks();
// apiServerLoadBalancer.startHealthChecks();

// Export load balancer instances
module.exports = {
  llmLoadBalancer,
  gameEngineLoadBalancer,
  apiServerLoadBalancer,

  // Getter methods
  getLLMLoadBalancer: () => llmLoadBalancer,
  getGameEngineLoadBalancer: () => gameEngineLoadBalancer,
  getAPIServerLoadBalancer: () => apiServerLoadBalancer,

  // Health status
  getHealthStatus: () => ({
    llm: llmLoadBalancer.getStats(),
    gameEngine: gameEngineLoadBalancer.getStats(),
    apiServer: apiServerLoadBalancer.getStats(),
  }),

  // Load balancer stats
  getLoadBalancerStats: () => ({
    llm: {
      totalServers: llmLoadBalancer.servers.length,
      activeServers: llmLoadBalancer.servers.filter((s) => s.isHealthy).length,
      strategy: llmLoadBalancer.strategy,
      stats: llmLoadBalancer.getStats(),
    },
    gameEngine: {
      totalServers: gameEngineLoadBalancer.servers.length,
      activeServers: gameEngineLoadBalancer.servers.filter((s) => s.isHealthy)
        .length,
      strategy: gameEngineLoadBalancer.strategy,
      stats: gameEngineLoadBalancer.getStats(),
    },
    apiServer: {
      totalServers: apiServerLoadBalancer.servers.length,
      activeServers: apiServerLoadBalancer.servers.filter((s) => s.isHealthy)
        .length,
      strategy: apiServerLoadBalancer.strategy,
      stats: apiServerLoadBalancer.getStats(),
    },
  }),
};
