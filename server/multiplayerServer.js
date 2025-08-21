const { Server } = require("socket.io");
const dataManager = require("./dataManager");

class MultiplayerServer {
  constructor() {
    this.io = null;
    this.gameSessions = new Map();
    this.playerSessions = new Map();
  }

  initialize(server) {
    this.io = new Server(server, {
      cors: {
        origin: ["http://localhost:3001", "http://localhost:3000"],
        methods: ["GET", "POST"]
      }
    });

    this.setupEventHandlers();
    console.log("🎮 Multiplayer server initialized");
  }

  setupEventHandlers() {
    this.io.on("connection", (socket) => {
      console.log(`👤 Player connected: ${socket.id}`);

      // Join game session
      socket.on("join_session", (data) => {
        this.handleJoinSession(socket, data);
      });

      // Leave game session
      socket.on("leave_session", (data) => {
        this.handleLeaveSession(socket, data);
      });

      // Player action
      socket.on("player_action", (data) => {
        this.handlePlayerAction(socket, data);
      });

      // Chat message
      socket.on("chat_message", (data) => {
        this.handleChatMessage(socket, data);
      });

      // Disconnect
      socket.on("disconnect", () => {
        this.handleDisconnect(socket);
      });
    });
  }

  handleJoinSession(socket, data) {
    const { sessionId, playerName, character } = data;
    
    if (!this.gameSessions.has(sessionId)) {
      this.gameSessions.set(sessionId, {
        id: sessionId,
        players: new Map(),
        gameState: "waiting",
        scenario: null,
        currentNarrative: "",
        availableActions: []
      });
    }

    const session = this.gameSessions.get(sessionId);
    session.players.set(socket.id, {
      id: socket.id,
      name: playerName,
      character: character,
      joinedAt: new Date()
    });

    socket.join(sessionId);
    this.playerSessions.set(socket.id, sessionId);

    // Notify all players in session
    this.io.to(sessionId).emit("player_joined", {
      playerId: socket.id,
      playerName: playerName,
      character: character,
      totalPlayers: session.players.size
    });

    console.log(`👥 Player ${playerName} joined session ${sessionId}`);
  }

  handleLeaveSession(socket, data) {
    const sessionId = this.playerSessions.get(socket.id);
    if (!sessionId) return;

    const session = this.gameSessions.get(sessionId);
    if (!session) return;

    session.players.delete(socket.id);
    this.playerSessions.delete(socket.id);
    socket.leave(sessionId);

    // Notify remaining players
    this.io.to(sessionId).emit("player_left", {
      playerId: socket.id,
      totalPlayers: session.players.size
    });

    // Clean up empty sessions
    if (session.players.size === 0) {
      this.gameSessions.delete(sessionId);
      console.log(`🗑️ Session ${sessionId} cleaned up`);
    }

    console.log(`👋 Player left session ${sessionId}`);
  }

  handlePlayerAction(socket, data) {
    const sessionId = this.playerSessions.get(socket.id);
    if (!sessionId) return;

    const session = this.gameSessions.get(sessionId);
    if (!session) return;

    // Broadcast action to all players in session
    this.io.to(sessionId).emit("player_action", {
      playerId: socket.id,
      action: data.action,
      timestamp: new Date()
    });

    console.log(`⚡ Player action in session ${sessionId}: ${data.action.type}`);
  }

  handleChatMessage(socket, data) {
    const sessionId = this.playerSessions.get(socket.id);
    if (!sessionId) return;

    // Broadcast chat message to all players in session
    this.io.to(sessionId).emit("chat_message", {
      playerId: socket.id,
      message: data.message,
      timestamp: new Date()
    });

    console.log(`💬 Chat message in session ${sessionId}`);
  }

  handleDisconnect(socket) {
    const sessionId = this.playerSessions.get(socket.id);
    if (sessionId) {
      this.handleLeaveSession(socket, {});
    }

    console.log(`🔌 Player disconnected: ${socket.id}`);
  }

  // Get available sessions
  getAvailableSessions() {
    const sessions = [];
    for (const [sessionId, session] of this.gameSessions) {
      sessions.push({
        id: sessionId,
        playerCount: session.players.size,
        maxPlayers: 5,
        status: session.gameState,
        scenario: session.scenario?.title || "Unknown"
      });
    }
    return sessions;
  }

  // Create new session
  createSession(sessionId, scenario) {
    if (this.gameSessions.has(sessionId)) {
      return false; // Session already exists
    }

    this.gameSessions.set(sessionId, {
      id: sessionId,
      players: new Map(),
      gameState: "waiting",
      scenario: scenario,
      currentNarrative: "",
      availableActions: []
    });

    console.log(`🎮 New session created: ${sessionId}`);
    return true;
  }
}

module.exports = MultiplayerServer;
