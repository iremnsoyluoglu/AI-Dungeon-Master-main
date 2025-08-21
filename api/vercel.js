const express = require("express");
const cors = require("cors");
const { createServer } = require("http");
const { Server } = require("socket.io");

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Import routers
const scenariosRouter = require("./scenarios");
const aiScenariosRouter = require("./ai/scenarios");

// API Routes
app.use("/api/scenarios", scenariosRouter);
app.use("/api/ai/scenarios", aiScenariosRouter);

// Multiplayer session endpoints
app.get("/api/multiplayer/sessions", (req, res) => {
  // Mock multiplayer sessions
  res.json([
    { id: "session1", name: "Dragon Hunters", players: 2, maxPlayers: 4 },
    { id: "session2", name: "Neon City Runners", players: 1, maxPlayers: 3 },
    { id: "session3", name: "Haunted Mansion", players: 3, maxPlayers: 5 },
  ]);
});

app.post("/api/multiplayer/sessions/:sessionId/leave", (req, res) => {
  res.json({ success: true });
});

// Health check
app.get("/api/health", (req, res) => {
  res.json({ status: "OK", timestamp: new Date().toISOString() });
});

// Serve static files
app.use(express.static("dist"));

// Serve React app for all other routes
app.get("*", (req, res) => {
  res.sendFile("index.html", { root: "dist" });
});

module.exports = app;
