const express = require("express");
const cors = require("cors");

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Load scenarios endpoint
app.get("/", (req, res) => {
  try {
    // Load all scenario files
    const enhancedScenarios = require("../data/enhanced_scenarios.json");
    const cyberpunkScenarios = require("../data/enhanced_cyberpunk_scenarios.json");
    const hiveCityScenarios = require("../data/expanded_hive_city.json");
    const warhammerScenarios = require("../data/enhanced_warhammer_scenarios.json");

    // Combine all scenarios
    const allScenarios = [
      ...enhancedScenarios,
      ...cyberpunkScenarios,
      ...hiveCityScenarios,
      ...warhammerScenarios,
    ];

    res.json({
      success: true,
      scenarios: allScenarios,
    });
  } catch (error) {
    console.error("Error loading scenarios:", error);
    res.status(500).json({
      success: false,
      error: "Failed to load scenarios",
    });
  }
});

// Export for Vercel
module.exports = app;
