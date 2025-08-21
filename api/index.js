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
  try {
    // Load all scenario files
    const enhancedScenarios = require("../data/enhanced_scenarios.json");
    const cyberpunkScenarios = require("../data/enhanced_cyberpunk_scenarios.json");
    const hiveCityScenarios = require("../data/expanded_hive_city.json");
    const warhammerScenarios = require("../data/enhanced_warhammer_scenarios.json");

    // Combine all scenarios
    const allScenarios = [
      ...enhancedScenarios.enhanced_scenarios,
      ...cyberpunkScenarios.enhanced_scenarios,
      ...hiveCityScenarios.enhanced_scenarios,
      ...warhammerScenarios.enhanced_scenarios,
    ];

    res.json({
      success: true,
      scenarios: allScenarios,
    });
  } catch (error) {
    console.error("Error loading scenarios:", error);
    // Fallback to static scenarios
    const fallbackScenarios = [
      {
        id: "dragon_hunters_path",
        title: "🐉 Dragon Hunter's Path",
        description:
          "Köyü tehdit eden ejderhayı durdurmak için kahramanlar toplanıyor. Bu sadece bir görev değil, bu SENİN HİKAYEN. 🔥 PLOT TWIST'LER, 💬 NPC ETKİLEŞİMLERİ, ⚔️ UZUN SAVAŞ SAHNELERİ, 🎯 ACTION-BASED GÖREVLER, 🏁 5+ FARKLI SON!",
        theme: "fantasy",
        difficulty: "hard",
        complexity: "high",
        estimatedPlayTime: 480,
        source: "predefined",
        created_at: new Date().toISOString(),
      },
      {
        id: "cyberpunk_city_secrets",
        title: "🌃 Neon City Runners (Cyberpunk)",
        description:
          "Cyberpunk şehrinin gizli sırlarını keşfet. Teknoloji ve insanlık arasındaki sınır bulanıklaşıyor. Dijital bilinç keşfi - Sen ölmüş birinin bilincin!",
        theme: "cyberpunk",
        difficulty: "hard",
        complexity: "high",
        estimatedPlayTime: 240,
        source: "predefined",
        created_at: new Date().toISOString(),
      },
      {
        id: "hive_city_defense",
        title: "🏙️ Hive City Underworld",
        description:
          "Hive City'de insanlar kayboluyor ve garip teknolojik anormallikler var. Gang savaşları - Underhive'da hayatta kalma!",
        theme: "sci-fi",
        difficulty: "hard",
        complexity: "high",
        estimatedPlayTime: 180,
        source: "predefined",
        created_at: new Date().toISOString(),
      },
      {
        id: "cadia_falls",
        title: "⚔️ Cadia Falls (Warhammer 40K)",
        description:
          "Chaos yozlaşması - Her yerde tehlike. Epik pozisyon savunması - Çoklu wave sistemi!",
        theme: "warhammer",
        difficulty: "hard",
        complexity: "high",
        estimatedPlayTime: 300,
        source: "predefined",
        created_at: new Date().toISOString(),
      },
    ];

    res.json({
      success: true,
      scenarios: fallbackScenarios,
    });
  }
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
