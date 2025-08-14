const express = require("express");
const cors = require("cors");

console.log("🚀 All backend services starting...");
console.log("📊 Services:");
console.log("  🤖 LLM Servers: 8010, 8011");
console.log("  🎮 Game Engines: 5020, 5021, 5022, 5023, 5024");
console.log("  🌐 API Servers: 5030, 5031");

// Backend Server 1 - LLM Service (Port 8010)
const llmServer1 = express();
llmServer1.use(cors());
llmServer1.use(express.json());

llmServer1.get("/health", (req, res) => {
  res.json({ status: "healthy", service: "LLM Server 1", port: 8010 });
});

llmServer1.post("/generate", (req, res) => {
  res.json({
    success: true,
    response: "This is a mock LLM response from server 1",
    server: "localhost:8010",
    timestamp: new Date().toISOString(),
  });
});

llmServer1.listen(8010, () => {
  console.log("🤖 LLM Server 1 running on port 8010");
});

// Backend Server 2 - LLM Service (Port 8011)
const llmServer2 = express();
llmServer2.use(cors());
llmServer2.use(express.json());

llmServer2.get("/health", (req, res) => {
  res.json({ status: "healthy", service: "LLM Server 2", port: 8011 });
});

llmServer2.post("/generate", (req, res) => {
  res.json({
    success: true,
    response: "This is a mock LLM response from server 2",
    server: "localhost:8011",
    timestamp: new Date().toISOString(),
  });
});

llmServer2.listen(8011, () => {
  console.log("🤖 LLM Server 2 running on port 8011");
});

// Game Engine 1 - Fantasy (Port 5020)
const gameEngine1 = express();
gameEngine1.use(cors());
gameEngine1.use(express.json());

gameEngine1.get("/health", (req, res) => {
  res.json({ status: "healthy", service: "Fantasy Game Engine 1", port: 5020 });
});

gameEngine1.post("/combat", (req, res) => {
  res.json({
    success: true,
    combat_result: "Fantasy combat processed",
    server: "localhost:5020",
    timestamp: new Date().toISOString(),
  });
});

gameEngine1.listen(5020, () => {
  console.log("🎮 Game Engine 1 running on port 5020");
});

// Game Engine 2 - Fantasy (Port 5021)
const gameEngine2 = express();
gameEngine2.use(cors());
gameEngine2.use(express.json());

gameEngine2.get("/health", (req, res) => {
  res.json({ status: "healthy", service: "Fantasy Game Engine 2", port: 5021 });
});

gameEngine2.post("/combat", (req, res) => {
  res.json({
    success: true,
    combat_result: "Fantasy combat processed",
    server: "localhost:5021",
    timestamp: new Date().toISOString(),
  });
});

gameEngine2.listen(5021, () => {
  console.log("🎮 Game Engine 2 running on port 5021");
});

// Game Engine 3 - Sci-Fi (Port 5022)
const gameEngine3 = express();
gameEngine3.use(cors());
gameEngine3.use(express.json());

gameEngine3.get("/health", (req, res) => {
  res.json({ status: "healthy", service: "Sci-Fi Game Engine 1", port: 5022 });
});

gameEngine3.post("/combat", (req, res) => {
  res.json({
    success: true,
    combat_result: "Sci-Fi combat processed",
    server: "localhost:5022",
    timestamp: new Date().toISOString(),
  });
});

gameEngine3.listen(5022, () => {
  console.log("🎮 Game Engine 3 running on port 5022");
});

// Game Engine 4 - Horror (Port 5023)
const gameEngine4 = express();
gameEngine4.use(cors());
gameEngine4.use(express.json());

gameEngine4.get("/health", (req, res) => {
  res.json({ status: "healthy", service: "Horror Game Engine 1", port: 5023 });
});

gameEngine4.post("/combat", (req, res) => {
  res.json({
    success: true,
    combat_result: "Horror combat processed",
    server: "localhost:5023",
    timestamp: new Date().toISOString(),
  });
});

gameEngine4.listen(5023, () => {
  console.log("🎮 Game Engine 4 running on port 5023");
});

// Game Engine 5 - Universal (Port 5024)
const gameEngine5 = express();
gameEngine5.use(cors());
gameEngine5.use(express.json());

gameEngine5.get("/health", (req, res) => {
  res.json({
    status: "healthy",
    service: "Universal Game Engine 1",
    port: 5024,
  });
});

gameEngine5.post("/combat", (req, res) => {
  res.json({
    success: true,
    combat_result: "Universal combat processed",
    server: "localhost:5024",
    timestamp: new Date().toISOString(),
  });
});

gameEngine5.listen(5024, () => {
  console.log("🎮 Game Engine 5 running on port 5024");
});

// API Server 1 (Port 5030)
const apiServer1 = express();
apiServer1.use(cors());
apiServer1.use(express.json());

apiServer1.get("/health", (req, res) => {
  res.json({ status: "healthy", service: "API Server 1", port: 5030 });
});

apiServer1.post("/api/*", (req, res) => {
  res.json({
    success: true,
    api_response: "API request processed",
    server: "localhost:5030",
    timestamp: new Date().toISOString(),
  });
});

apiServer1.listen(5030, () => {
  console.log("🌐 API Server 1 running on port 5030");
});

// API Server 2 (Port 5031)
const apiServer2 = express();
apiServer2.use(cors());
apiServer2.use(express.json());

apiServer2.get("/health", (req, res) => {
  res.json({ status: "healthy", service: "API Server 2", port: 5031 });
});

apiServer2.post("/api/*", (req, res) => {
  res.json({
    success: true,
    api_response: "API request processed",
    server: "localhost:5031",
    timestamp: new Date().toISOString(),
  });
});

apiServer2.listen(5031, () => {
  console.log("🌐 API Server 2 running on port 5031");
});

console.log("✅ All backend services started successfully!");
