const express = require("express");
const cors = require("cors");
const multer = require("multer");

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Multer configuration
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 5 * 1024 * 1024 },
});

// Load scenarios endpoint
app.get("/api/scenarios", (req, res) => {
  try {
    // Basit senaryolar döndür
    const scenarios = [
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
      {
        id: "scenario_3",
        title: "🛡️ Warhammer 40K Macera", 
        description: "İmparatorluk için savaş zamanı",
        theme: "warhammer",
        difficulty: "hard",
        complexity: "high",
        estimatedPlayTime: 120,
        source: "predefined",
        created_at: new Date().toISOString(),
      }
    ];

    res.json({
      success: true,
      scenarios: scenarios,
    });
  } catch (error) {
    console.error("Error loading scenarios:", error);
    res.status(500).json({
      success: false,
      error: "Failed to load scenarios",
    });
  }
});

// Get AI generated scenarios
app.get("/api/ai/scenarios", (req, res) => {
  try {
    // Basit AI senaryoları döndür
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
    ];

    res.json({
      success: true,
      scenarios: aiScenarios,
    });
  } catch (error) {
    console.error("Error loading AI scenarios:", error);
    res.status(500).json({
      success: false,
      error: "Failed to load AI scenarios",
    });
  }
});

// Dosya okuma endpoint'i
app.post("/api/read-file", upload.single("file"), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "Dosya yüklenmedi!" });
    }

    const fileType = req.file.mimetype;
    let content = "";

    if (fileType === "text/plain" || fileType === "text/markdown") {
      content = req.file.buffer.toString("utf8");
    } else if (fileType === "application/pdf") {
      content = "PDF dosyası okundu - içerik işleniyor...";
    } else if (
      fileType === "application/msword" ||
      fileType ===
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ) {
      content = "Word dosyası okundu - içerik işleniyor...";
    } else {
      content = req.file.buffer.toString("utf8");
    }

    res.json({
      content: content,
      fileName: req.file.originalname,
      fileSize: req.file.size,
    });
  } catch (error) {
    console.error("Dosya okuma hatası:", error);
    res.status(500).json({ error: "Dosya okunamadı: " + error.message });
  }
});

// Dosya tabanlı senaryo üretimi endpoint'i
app.post("/api/generate-scenario", async (req, res) => {
  try {
    const { theme, difficulty, fileContent, knowledgeBase } = req.body;

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

      story_nodes: {
        start: {
          id: "start",
          title: "🚀 Dosya Macerasının Başlangıcı",
          description: `Dosya içeriğinden üretilen bu macerada kendini buluyorsun. ${theme} temalı ${difficulty} zorlukta bir yolculuk seni bekliyor.`,
          choices: [
            {
              id: "explore_carefully",
              text: "Dikkatli bir şekilde çevreyi keşfet",
              nextNode: "careful_exploration",
              effect: { stealth: 2, intelligence: 1 },
            },
            {
              id: "rush_forward",
              text: "Hızlıca ileri atıl",
              nextNode: "rushed_encounter",
              effect: { strength: 2, dexterity: 1 },
            },
            {
              id: "seek_help",
              text: "Yardım ara",
              nextNode: "npc_encounter",
              effect: { charisma: 2, wisdom: 1 },
            },
          ],
        },
        careful_exploration: {
          id: "careful_exploration",
          title: "🔍 Dikkatli Keşif",
          description:
            "Çevreyi dikkatli bir şekilde inceliyorsun. Dosya içeriğinden üretilen gizli geçitler ve tuzaklar fark ediyorsun.",
          choices: [
            {
              id: "use_stealth",
              text: "Gizlilik kullanarak ilerle",
              nextNode: "stealth_mission",
              effect: { stealth: 3, experience: 50 },
            },
            {
              id: "disable_traps",
              text: "Tuzakları etkisiz hale getir",
              nextNode: "trap_discovery",
              effect: { intelligence: 2, dexterity: 1 },
            },
          ],
        },
        rushed_encounter: {
          id: "rushed_encounter",
          title: "⚔️ Hızlı Karşılaşma",
          description:
            "Hızlı hareket etmen sonucu dosya içeriğinden üretilen beklenmedik bir düşmanla karşılaştın!",
          choices: [
            {
              id: "fight_bravely",
              text: "Cesurca savaş",
              nextNode: "combat_scene_1",
              effect: { strength: 3, combat_skill: 2 },
            },
            {
              id: "tactical_retreat",
              text: "Taktiksel geri çekil",
              nextNode: "tactical_positioning",
              effect: { wisdom: 2, dexterity: 1 },
            },
          ],
        },
        npc_encounter: {
          id: "npc_encounter",
          title: "👥 NPC Karşılaşması",
          description:
            "Dosya içeriğinden üretilen bir NPC ile karşılaştın. Size yardım etmek istiyor ama güvenilir mi?",
          choices: [
            {
              id: "trust_npc",
              text: "NPC'ye güven",
              nextNode: "npc_alliance",
              effect: { charisma: 2, npc_trust: 30 },
            },
            {
              id: "be_cautious",
              text: "İhtiyatlı ol",
              nextNode: "cautious_interaction",
              effect: { wisdom: 2, intelligence: 1 },
            },
          ],
        },
        combat_scene_1: {
          id: "combat_scene_1",
          title: "⚔️ Savaş Sahnesi - Dosya Düşmanı",
          description:
            "Dosya içeriğinden üretilen düşman ile karşı karşıyasın! Savaş başlıyor!",
          choices: [
            {
              id: "heavy_attack",
              text: "Ağır saldırı",
              nextNode: "combat_victory",
              effect: { strength: 3, damage: 25 },
            },
            {
              id: "defensive_stance",
              text: "Savunma pozisyonu",
              nextNode: "defensive_victory",
              effect: { constitution: 2, defense: 15 },
            },
          ],
        },
        npc_alliance: {
          id: "npc_alliance",
          title: "🤝 NPC İttifakı",
          description:
            "Dosya içeriğinden üretilen NPC ile ittifak kurdun. Birlikte daha güçlüsünüz.",
          choices: [
            {
              id: "plan_together",
              text: "Birlikte plan yap",
              nextNode: "strategic_planning",
              effect: { intelligence: 2, teamwork: 1 },
            },
            {
              id: "split_up",
              text: "Ayrı ayrı hareket et",
              nextNode: "split_mission",
              effect: { dexterity: 2, independence: 1 },
            },
          ],
        },
        strategic_planning: {
          id: "strategic_planning",
          title: "🧠 Stratejik Planlama",
          description:
            "NPC ile birlikte detaylı bir plan hazırladınız. Dosya içeriğinden üretilen düşmanın zayıf noktalarını belirlediniz.",
          choices: [
            {
              id: "execute_plan",
              text: "Planı uygula",
              nextNode: "planned_attack",
              effect: { intelligence: 3, strategy: 2 },
            },
            {
              id: "adapt_plan",
              text: "Planı değiştir",
              nextNode: "adaptive_strategy",
              effect: { wisdom: 2, flexibility: 1 },
            },
          ],
        },
        planned_attack: {
          id: "planned_attack",
          title: "🎯 Planlanmış Saldırı",
          description:
            "Hazırladığınız planı mükemmel bir şekilde uyguladınız. Dosya içeriğinden üretilen düşman şaşkın!",
          choices: [
            {
              id: "finish_them",
              text: "Düşmanı bitir",
              nextNode: "ending_victory",
              effect: { strength: 3, victory: 1 },
            },
            {
              id: "show_mercy",
              text: "Merhamet göster",
              nextNode: "ending_redemption",
              effect: { charisma: 2, wisdom: 2 },
            },
          ],
        },
        ending_victory: {
          id: "ending_victory",
          title: "🏆 Zafer Sonu",
          description:
            "Dosya içeriğinden üretilen macerada mükemmel bir zafer kazandın! Maceran başarıyla tamamlandı.",
          choices: [],
        },
        ending_redemption: {
          id: "ending_redemption",
          title: "🕊️ Kefaret Sonu",
          description:
            "Dosya içeriğinden üretilen macerada merhametin sayesinde düşmanın kalbini kazandın. Barış sağlandı.",
          choices: [],
        },
      },

      npc_relationships: {
        file_npc: {
          name: "Dosya NPC'si",
          trust_level: 0,
          quests_completed: 0,
          relationship_status: "stranger",
          ending_impact: "high",
        },
      },

      ending_variations: {
        victory: {
          requirements: { strength: 15, intelligence: 10 },
          description: "Zafer kazandın!",
        },
        redemption: {
          requirements: { charisma: 15, wisdom: 12 },
          description: "Merhametle kazandın!",
        },
        sacrifice: {
          requirements: { constitution: 18, charisma: 8 },
          description: "Fedakarlıkla kazandın!",
        },
      },
    };

    res.json({
      success: true,
      scenario: scenario,
      message: "Senaryo başarıyla üretildi!",
    });
  } catch (error) {
    console.error("Senaryo üretim hatası:", error);
    res.status(500).json({ error: "Senaryo üretilemedi: " + error.message });
  }
});

// Health check
app.get("/api/health", (req, res) => {
  res.json({ status: "OK", timestamp: new Date().toISOString() });
});

// Root endpoint
app.get("/", (req, res) => {
  res.json({ message: "AI Dungeon Master API is running!" });
});

// Catch all other routes
app.get("*", (req, res) => {
  res.status(404).json({ error: "Route not found" });
});

module.exports = app;
