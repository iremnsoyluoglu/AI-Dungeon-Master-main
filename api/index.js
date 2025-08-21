const express = require("express");
const cors = require("cors");

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Health check
app.get("/api/health", (req, res) => {
  res.json({ status: "OK", timestamp: new Date().toISOString() });
});

// Load scenarios endpoint
app.get("/api/scenarios", (req, res) => {
  const allScenarios = [
    {
      id: "scenario_1",
      title: "🐉 Fantastik Macera",
      description: "Ejderhalar ve büyücüler dünyasında epik bir yolculuk",
      theme: "fantasy",
      difficulty: "medium",
      complexity: "medium",
      estimatedPlayTime: 60,
      source: "predefined",
      created_at: new Date().toISOString(),
    },
    {
      id: "scenario_2",
      title: "🌃 Cyberpunk Macera",
      description: "Neon ışıklar altında dijital savaş",
      theme: "cyberpunk",
      difficulty: "hard",
      complexity: "high",
      estimatedPlayTime: 90,
      source: "predefined",
      created_at: new Date().toISOString(),
    },
  ];

  res.json({
    success: true,
    scenarios: allScenarios,
  });
});

// Get AI generated scenarios
app.get("/api/ai/scenarios", (req, res) => {
  const aiScenarios = [
    {
      id: "ai_1",
      title: "🤖 AI Üretilen Macera",
      description: "Yapay zeka tarafından üretilen özel macera",
      theme: "fantasy",
      difficulty: "medium",
      source: "ai_generated",
      created_at: new Date().toISOString(),
    },
    {
      id: "ai_2",
      title: "🌃 AI Cyberpunk Macera",
      description: "AI tarafından üretilen cyberpunk dünyası",
      theme: "cyberpunk",
      difficulty: "hard",
      source: "ai_generated",
      created_at: new Date().toISOString(),
    },
  ];

  res.json({
    success: true,
    scenarios: aiScenarios,
  });
});

// Simple scenario generation
app.post("/api/generate-scenario", (req, res) => {
  const { theme, difficulty, fileContent } = req.body;

  const scenario = {
    id: `scenario_${Date.now()}`,
    title: `${theme} Macerası - ${difficulty}`,
    description: `Dosya içeriğinden üretilen ${theme} temalı ${difficulty} zorlukta senaryo`,
    theme: theme,
    difficulty: difficulty,
    complexity: difficulty,
    estimatedPlayTime:
      difficulty === "easy" ? 30 : difficulty === "medium" ? 60 : 90,
    fileContent: fileContent ? fileContent.substring(0, 200) + "..." : null,
    generatedAt: new Date().toISOString(),
    source: "file_generated",
    created_at: new Date().toISOString(),
  };

  res.json({
    success: true,
    scenario: scenario,
    message: "Senaryo başarıyla üretildi!",
  });
});

// Serve static files
app.use(express.static("public"));

// Serve React app for all other routes
app.get("*", (req, res) => {
  res.sendFile("index.html", { root: "public" });
});

module.exports = app;
