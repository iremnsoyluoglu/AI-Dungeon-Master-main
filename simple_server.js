const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");

const app = express();

// CORS middleware
app.use(cors());
app.use(express.json());

// Serve static files
app.use(express.static(__dirname));

// Simple scenarios data
const getScenarios = () => {
  const scenariosFile = path.join(__dirname, 'data', 'scenarios.json');
  if (fs.existsSync(scenariosFile)) {
    return JSON.parse(fs.readFileSync(scenariosFile, 'utf8'));
  }
  return [];
};

// Scenarios API endpoint
app.get("/api/scenarios", async (req, res) => {
  try {
    const scenarios = getScenarios();
    res.json({
      success: true,
      scenarios: scenarios,
      total: scenarios.length,
    });
  } catch (error) {
    console.error("Get scenarios error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Health check endpoint
app.get("/health", (req, res) => {
  res.json({
    status: "healthy",
    timestamp: new Date().toISOString(),
    server: "Simple AI Dungeon Master API",
    version: "1.0.0",
  });
});

const PORT = process.env.PORT || 5005;

app.listen(PORT, () => {
  console.log(`🚀 Simple AI Dungeon Master Server running on port ${PORT}`);
  console.log(`🔧 API endpoints available at http://localhost:${PORT}/api`);
  console.log(`📊 Scenarios endpoint: http://localhost:${PORT}/api/scenarios`);
  console.log(`🧪 Test page: http://localhost:${PORT}/test_scenario_selection.html`);
});
