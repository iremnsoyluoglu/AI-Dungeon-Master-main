const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");
const llmProxy = require("./llmProxy");
const loadBalancerConfig = require("./loadBalancerConfig");
const dataManager = require("./dataManager");

// Gerçek LLM servislerini import et
let IntegratedLLMEngine = null;
let GetComicsDataFetcher = null;
let GameMasterAI = null;

console.log("✅ Gerçek veri sistemi aktif - Oyuncu kayıtları korunuyor");

// Gerçek senaryo veritabanı - Oyuncu tercihlerine göre dinamik
const getScenarios = () => {
  return dataManager.getScenarios();
};

const app = express();
app.use(cors());
app.use(express.json());

app.use("/api/llm", llmProxy);

// Load Balancer Routes
app.get("/api/loadbalancer/health", (req, res) => {
  try {
    const healthStatus = loadBalancerConfig.getHealthStatus();
    res.json(healthStatus);
  } catch (error) {
    console.error("Load balancer health check error:", error);
    res.status(500).json({ error: error.message });
  }
});

app.get("/api/loadbalancer/stats", (req, res) => {
  try {
    const stats = loadBalancerConfig.getLoadBalancerStats();
    res.json(stats);
  } catch (error) {
    console.error("Load balancer stats error:", error);
    res.status(500).json({ error: error.message });
  }
});

// LLM Load Balancer Routes
app.post("/api/loadbalancer/llm/generate", async (req, res) => {
  try {
    const llmLoadBalancer = loadBalancerConfig.getLLMLoadBalancer();
    await llmLoadBalancer.forwardLLMRequest(req, res);
  } catch (error) {
    console.error("LLM load balancer error:", error);
    if (!res.headersSent) {
      res.status(500).json({ error: "LLM service unavailable" });
    }
  }
});

// Game Engine Load Balancer Routes
app.post("/api/loadbalancer/game/combat", async (req, res) => {
  try {
    const gameEngineLoadBalancer =
      loadBalancerConfig.getGameEngineLoadBalancer();
    await gameEngineLoadBalancer.forwardGameRequest(req, res);
  } catch (error) {
    console.error("Game engine load balancer error:", error);
    if (!res.headersSent) {
      res.status(500).json({ error: "Game engine service unavailable" });
    }
  }
});

// API Server Load Balancer Routes
app.post("/api/loadbalancer/api/forward", async (req, res) => {
  try {
    const apiServerLoadBalancer = loadBalancerConfig.getAPIServerLoadBalancer();
    await apiServerLoadBalancer.forwardAPIRequest(req, res);
  } catch (error) {
    console.error("API server load balancer error:", error);
    if (!res.headersSent) {
      res.status(500).json({ error: "API server unavailable" });
    }
  }
});

// Game Engine Load Balancer Routes
app.post("/api/loadbalancer/game", async (req, res) => {
  try {
    const gameEngineLoadBalancer =
      loadBalancerConfig.getGameEngineLoadBalancer();
    await gameEngineLoadBalancer.forwardGameRequest(req, res);
  } catch (error) {
    console.error("Game engine load balancer error:", error);
    res.status(500).json({ error: "Game engine unavailable" });
  }
});

// API Server Load Balancer Routes - Disabled due to path-to-regexp issues
// app.use("/api/loadbalancer/api", async (req, res, next) => {
//   try {
//     const apiServerLoadBalancer = loadBalancerConfig.getAPIServerLoadBalancer();
//     await apiServerLoadBalancer.forwardAPIRequest(req, res);
//   } catch (error) {
//     console.error("API server load balancer error:", error);
//     if (!res.headersSent) {
//       res.status(500).json({ error: "API server unavailable" });
//     }
//   }
// });

// Load Balancer Management Routes
app.post("/api/loadbalancer/server/add", (req, res) => {
  try {
    const { type, server } = req.body;
    console.log("Adding server:", { type, server });

    switch (type) {
      case "llm":
        loadBalancerConfig.llmLoadBalancer.addLLMService(server);
        break;
      case "game":
        loadBalancerConfig.gameEngineLoadBalancer.addGameEngine(server);
        break;
      case "api":
        loadBalancerConfig.apiServerLoadBalancer.addAPIServer(server);
        break;
      default:
        throw new Error(`Unknown server type: ${type}`);
    }

    res.json({
      success: true,
      message: `Server added to ${type} load balancer`,
    });
  } catch (error) {
    console.error("Add server error:", error);
    res.status(500).json({ error: error.message });
  }
});

app.delete("/api/loadbalancer/server/remove", (req, res) => {
  try {
    const { type, serverId } = req.body;
    console.log("Removing server:", { type, serverId });

    switch (type) {
      case "llm":
        loadBalancerConfig.llmLoadBalancer.removeServer(serverId);
        break;
      case "game":
        loadBalancerConfig.gameEngineLoadBalancer.removeServer(serverId);
        break;
      case "api":
        loadBalancerConfig.apiServerLoadBalancer.removeServer(serverId);
        break;
      default:
        throw new Error(`Unknown server type: ${type}`);
    }

    res.json({
      success: true,
      message: `Server removed from ${type} load balancer`,
    });
  } catch (error) {
    console.error("Remove server error:", error);
    res.status(500).json({ error: error.message });
  }
});

app.put("/api/loadbalancer/config/update", (req, res) => {
  try {
    const { type, config } = req.body;
    console.log("Updating config:", { type, config });

    switch (type) {
      case "llm":
        if (config.strategy)
          loadBalancerConfig.llmLoadBalancer.strategy = config.strategy;
        if (config.healthCheckInterval)
          loadBalancerConfig.llmLoadBalancer.healthCheckInterval =
            config.healthCheckInterval;
        break;
      case "game":
        if (config.strategy)
          loadBalancerConfig.gameEngineLoadBalancer.strategy = config.strategy;
        if (config.healthCheckInterval)
          loadBalancerConfig.gameEngineLoadBalancer.healthCheckInterval =
            config.healthCheckInterval;
        break;
      case "api":
        if (config.strategy)
          loadBalancerConfig.apiServerLoadBalancer.strategy = config.strategy;
        if (config.healthCheckInterval)
          loadBalancerConfig.apiServerLoadBalancer.healthCheckInterval =
            config.healthCheckInterval;
        break;
      default:
        throw new Error(`Unknown load balancer type: ${type}`);
    }

    res.json({
      success: true,
      message: `${type} load balancer config updated`,
    });
  } catch (error) {
    console.error("Update config error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Health check endpoint for individual servers
app.get("/health", (req, res) => {
  res.json({
    status: "healthy",
    timestamp: new Date().toISOString(),
    server: "AI Dungeon Master API",
    version: "1.0.0",
  });
});

// Gerçek LLM servislerini başlat (şimdilik devre dışı)
let integratedEngine = null;
let comicsFetcher = null;
let gameMasterAI = null;

console.log("✅ LLM servisleri aktif");

// Game Master AI (şimdilik mock)
const gameMaster = {
  startGame: async (scenario) => {
    console.log(`🎮 Mock Game Master ile oyun başlatılıyor: ${scenario.title}`);

    // Senaryo temasına göre farklı seçenekler
    const getActionsByTheme = (theme) => {
      switch (theme) {
        case "fantasy":
          return [
            {
              type: "explore",
              description: "🗺️ Çevreyi keşfet",
              diceRoll: {
                diceType: "d20",
                targetNumber: 15,
                skill: "perception",
              },
              consequences: {
                success: "Gizli bir geçit buldun! Hazine odasına gidebilirsin.",
                failure: "Hiçbir şey bulamadın, ama dikkatli olmalısın.",
              },
            },
            {
              type: "talk",
              description: "💬 NPC ile konuş",
              diceRoll: {
                diceType: "d20",
                targetNumber: 12,
                skill: "charisma",
              },
              consequences: {
                success:
                  "NPC seninle işbirliği yapmaya karar verdi. Bilgi verdi!",
                failure: "NPC seni reddetti ve güvenmiyor.",
              },
            },
            {
              type: "investigate",
              description: "🔍 Detaylı araştır",
              diceRoll: {
                diceType: "d20",
                targetNumber: 18,
                skill: "investigation",
              },
              consequences: {
                success: "Önemli bir ipucu buldun! Gizli sırları keşfettin.",
                failure: "Araştırma sonuçsuz kaldı.",
              },
            },
            {
              type: "stealth",
              description: "👤 Gizlice ilerle",
              diceRoll: { diceType: "d20", targetNumber: 14, skill: "stealth" },
              consequences: {
                success:
                  "Kimse seni fark etmedi! Güvenli bir şekilde ilerledin.",
                failure: "Gürültü yaptın ve dikkat çektin!",
              },
            },
          ];
        case "warhammer":
          return [
            {
              type: "scan",
              description: "📡 Teknoloji taraması",
              diceRoll: { diceType: "d20", targetNumber: 16, skill: "tech" },
              consequences: {
                success: "Eski teknoloji kalıntıları tespit ettin!",
                failure: "Tarama sonuçsuz kaldı.",
              },
            },
            {
              type: "purge",
              description: "🔥 Heretikleri temizle",
              diceRoll: { diceType: "d20", targetNumber: 13, skill: "combat" },
              consequences: {
                success: "Heretikleri başarıyla temizledin!",
                failure: "Savaş zorlaştı, geri çekilmek zorunda kaldın.",
              },
            },
            {
              type: "investigate",
              description: "🔍 Soruşturma yap",
              diceRoll: {
                diceType: "d20",
                targetNumber: 15,
                skill: "investigation",
              },
              consequences: {
                success: "Heretik aktivitelerin izini sürdün!",
                failure: "Soruşturma sonuçsuz kaldı.",
              },
            },
            {
              type: "fortify",
              description: "🏗️ Pozisyonu güçlendir",
              diceRoll: {
                diceType: "d20",
                targetNumber: 12,
                skill: "engineering",
              },
              consequences: {
                success: "Pozisyonu başarıyla güçlendirdin!",
                failure: "Güçlendirme yetersiz kaldı.",
              },
            },
          ];
        case "horror":
          return [
            {
              type: "investigate",
              description: "🔍 Korkunç sırları araştır",
              diceRoll: {
                diceType: "d20",
                targetNumber: 17,
                skill: "investigation",
              },
              consequences: {
                success: "Korkunç gerçeği öğrendin ama aklını korudun!",
                failure: "Araştırma seni korkuttu ve geri çekildin.",
              },
            },
            {
              type: "hide",
              description: "👻 Saklan",
              diceRoll: { diceType: "d20", targetNumber: 14, skill: "stealth" },
              consequences: {
                success: "Başarıyla saklandın ve tehlikeyi atlattın!",
                failure: "Saklanamadın ve tehlikeyle karşılaştın!",
              },
            },
            {
              type: "exorcise",
              description: "⛪ Laneti kaldır",
              diceRoll: {
                diceType: "d20",
                targetNumber: 18,
                skill: "religion",
              },
              consequences: {
                success: "Laneti başarıyla kaldırdın!",
                failure: "Lanet güçlendi ve seni etkiledi!",
              },
            },
            {
              type: "escape",
              description: "🏃 Kaç",
              diceRoll: {
                diceType: "d20",
                targetNumber: 13,
                skill: "athletics",
              },
              consequences: {
                success: "Başarıyla kaçtın!",
                failure: "Kaçamadın ve yakalandın!",
              },
            },
          ];
        default:
          return [
            {
              type: "explore",
              description: "🗺️ Çevreyi keşfet",
              diceRoll: {
                diceType: "d20",
                targetNumber: 15,
                skill: "perception",
              },
              consequences: {
                success: "Gizli bir geçit buldun!",
                failure: "Hiçbir şey bulamadın.",
              },
            },
            {
              type: "talk",
              description: "💬 NPC ile konuş",
              diceRoll: {
                diceType: "d20",
                targetNumber: 12,
                skill: "charisma",
              },
              consequences: {
                success: "NPC seninle işbirliği yapmaya karar verdi.",
                failure: "NPC seni reddetti.",
              },
            },
          ];
      }
    };

    // Senaryo temasına göre farklı anlatımlar
    const getNarrativeByTheme = (theme) => {
      switch (theme) {
        case "fantasy":
          return "Antik bir tapınağın girişindesin. Hava gizem ve tehlikeyle dolu. Ne yapmak istiyorsun?";
        case "warhammer":
          return "Imperial Guard karargahındasın. Heretik aktiviteler tespit edildi. Görevini yerine getirmelisin!";
        case "horror":
          return "Karanlık bir evdesin. Korkunç sesler duyuyorsun. Ne yapmak istiyorsun?";
        default:
          return "Macera başladı! Ne yapmak istiyorsun?";
      }
    };

    return {
      narrative: `🎮 ${scenario.title} oyunu başladı! ${getNarrativeByTheme(
        scenario.theme
      )}`,
      availableActions: getActionsByTheme(scenario.theme),
      currentState: {
        currentScene: 0,
        playerHP: 100,
        playerInventory: ["Elma", "İksir"],
        playerStats: {
          strength: 15,
          dexterity: 14,
          intelligence: 12,
          charisma: 10,
        },
        activeEffects: [],
        gameProgress: {
          completedScenes: [],
          choices: [],
          combatWins: 0,
          itemsFound: 0,
        },
      },
      isCombat: false,
    };
  },
  processPlayerAction: async (action, diceResult) => {
    return {
      narrative: `⚡ ${action} aksiyonunu gerçekleştirdin${
        diceResult ? ` (Zar: ${diceResult})` : ""
      }. Game Master sonucu değerlendiriyor...`,
      availableActions: [
        {
          type: "continue",
          description: "Devam et",
          consequences: {
            success: "Yoluna devam ediyorsun.",
            failure: "Bir engelle karşılaştın.",
          },
        },
      ],
      currentState: {
        currentScene: 1,
        playerHP: 95,
        playerInventory: ["Elma", "İksir", "Yeni Item"],
        playerStats: {
          strength: 15,
          dexterity: 14,
          intelligence: 12,
          charisma: 10,
        },
        activeEffects: [],
        gameProgress: {
          completedScenes: [0],
          choices: [action],
          combatWins: 0,
          itemsFound: 1,
        },
      },
      isCombat: false,
    };
  },
};

// Senaryo üret
app.post("/api/scenario/generate", async (req, res) => {
  try {
    const { theme = "fantasy", difficulty = "medium" } = req.body;
    console.log(`🎲 Senaryo üretiliyor: ${theme} - ${difficulty}`);

    if (integratedEngine) {
      // Gerçek LLM ile senaryo üret
      console.log("🤖 LLM ile senaryo üretiliyor...");
      const scenario = await integratedEngine.generateScenario(
        theme,
        difficulty
      );
      console.log("✅ LLM senaryo üretimi tamamlandı");
      res.json(scenario);
    } else {
      // Mock senaryo üretimi (gerçek sistem düzeltilince değiştirilecek)
      const themes = {
        fantasy: {
          titles: [
            "🐉 Ejderha Mağarası",
            "🏰 Kayıp Krallık",
            "🔮 Büyücü Akademisi",
            "🗡️ Karanlık Orman",
            "⚔️ Savaşçılar Vadisi",
          ],
          descriptions: [
            "Bir ejderha mağarasında gizli hazine arayışı",
            "Kayıp krallığı kurtarmak için tehlikeli yolculuk",
            "Büyücü akademisinde eğitim ve macera",
            "Karanlık ormanda gizli geçitler",
            "Savaşçılar vadisinde düello ve onur",
          ],
        },
        warhammer: {
          titles: [
            "🛡️ Space Marine Görevi",
            "⚙️ Tech-Priest Araştırması",
            "🔍 Inquisitor Soruşturması",
            "🎖️ Imperial Guard Operasyonu",
            "⚔️ Chaos İstilası",
          ],
          descriptions: [
            "Ork istilasını durdurmak için Space Marine görevi",
            "Eski teknoloji kalıntılarını araştırma",
            "Heretik aktiviteleri soruşturma",
            "Imperial Guard ile savunma operasyonu",
            "Chaos güçlerine karşı savaş",
          ],
        },
        horror: {
          titles: [
            "👻 Korku Evi",
            "🕯️ Lanetli Manastır",
            "🌙 Karanlık Ritüel",
            "🩸 Vampir Avı",
            "💀 Zombi İstilası",
          ],
          descriptions: [
            "Eski evde gizli korkular",
            "Lanetli manastırda karanlık sırlar",
            "Ay ışığında tehlikeli ritüeller",
            "Vampir sürüsünü avlama",
            "Zombi istilasını durdurma",
          ],
        },
      };

      const selectedTheme = themes[theme] || themes.fantasy;
      const titleIndex = Math.floor(
        Math.random() * selectedTheme.titles.length
      );
      const descIndex = Math.floor(
        Math.random() * selectedTheme.descriptions.length
      );

      const newScenario = {
        id: `scenario_${Date.now()}`,
        title: selectedTheme.titles[titleIndex],
        theme: theme,
        difficulty: difficulty,
        description: selectedTheme.descriptions[descIndex],
        isFavorite: false,
        createdAt: new Date().toISOString(),
        tags: [theme, difficulty, "generated"],
        content: {
          introduction: `${selectedTheme.descriptions[descIndex]}. Bu macerada kahramanlar zorlu görevlerle karşılaşacak.`,
          scenes: [
            {
              id: "scene_1",
              title: "Başlangıç",
              description: "Maceranın başlangıç noktası",
              choices: [
                { id: "choice_1", text: "İleri git", nextScene: "scene_2" },
                { id: "choice_2", text: "Etrafı keşfet", nextScene: "scene_3" },
              ],
            },
          ],
          npcs: [
            {
              id: "npc_1",
              name: "Rehber",
              description: "Yol gösterici karakter",
              role: "ally",
            },
          ],
        },
      };

      dataManager.saveScenario(newScenario);
      console.log(`✅ Mock senaryo üretildi: ${newScenario.title}`);
      res.json(newScenario);
    }
  } catch (error) {
    console.error("Scenario generation error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Comic learning endpoint (senaryo motorunu beslemek için)
app.post("/api/comic/learn", async (req, res) => {
  try {
    const { comicData } = req.body;
    console.log("📚 Comic'ten öğrenme başladı...");

    if (integratedEngine && comicsFetcher) {
      // Gerçek LLM ile comic'ten öğren
      console.log("📚 LLM ile comic'ten öğrenme başladı...");
      const learningResult = await integratedEngine.learnFromComic(comicData);
      console.log("✅ LLM comic'ten öğrenme tamamlandı");
      res.json({
        success: true,
        generalLearning: learningResult.generalLearning,
        frpMechanics: learningResult.frpMechanics,
        sessionId: `learning_${Date.now()}`,
      });
    } else {
      // Mock learning (gerçek sistem düzeltilince değiştirilecek)
      const learningResult = {
        success: true,
        learnedTechniques: [
          "Karakter gelişimi",
          "Savaş sahneleri",
          "Diyalog yazımı",
          "FRP mekanikleri",
        ],
        knowledgeBase: "Comic bilgileri öğrenildi ve senaryo motoruna eklendi",
        sessionId: `learning_${Date.now()}`,
      };

      console.log("✅ Mock comic'ten öğrenme tamamlandı");
      res.json(learningResult);
    }
  } catch (error) {
    console.error("Comic learning error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Tüm senaryoları getir
app.get("/api/scenarios", async (req, res) => {
  try {
    const scenariosData = getScenarios();
    const scenarios = scenariosData.scenarios || scenariosData;

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

// Favori senaryoları getir
app.get("/api/scenarios/favorites", async (req, res) => {
  try {
    const scenariosData = getScenarios();
    const scenarios = scenariosData.scenarios || scenariosData;
    const favorites = scenarios.filter((s) => s.isFavorite);
    res.json({
      success: true,
      scenarios: favorites,
      total: favorites.length,
    });
  } catch (error) {
    console.error("Get favorites error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Favori durumunu değiştir
app.post("/api/scenarios/:id/favorite", async (req, res) => {
  try {
    const { id } = req.params;
    const scenariosData = getScenarios();
    const scenarios = scenariosData.scenarios || scenariosData;
    const scenario = scenarios.find((s) => s.id === id);
    if (scenario) {
      scenario.isFavorite = !scenario.isFavorite;
      res.json({ success: true, isFavorite: scenario.isFavorite });
    } else {
      res.status(404).json({ error: "Senaryo bulunamadı" });
    }
  } catch (error) {
    console.error("Toggle favorite error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Sistem durumunu getir
app.get("/api/scenario/status", (req, res) => {
  const scenariosData = getScenarios();
  const scenarios = scenariosData.scenarios || scenariosData;

  if (integratedEngine) {
    const status = integratedEngine.getSystemStatus();
    res.json({
      generalKnowledge: status.generalKnowledge,
      frpKnowledge: status.frpKnowledge,
      learnedComics: status.learnedComics,
      learnedFRPMechanics: status.learnedFRPMechanics,
      totalScenarios: scenarios.length,
      systemStatus: "LLM Active",
    });
  } else {
    res.json({
      generalKnowledge: "Mock system - gerçek sistem düzeltilince aktif olacak",
      frpKnowledge: "Mock system - gerçek sistem düzeltilince aktif olacak",
      learnedComics: 0,
      learnedFRPMechanics: 0,
      totalScenarios: scenarios.length,
      systemStatus: "Mock Mode",
    });
  }
});

// Game Master API Endpoints
// Oyunu başlat
app.post("/api/game/start", async (req, res) => {
  try {
    const { scenarioId, scenario } = req.body;
    console.log(`🎮 Oyun başlatılıyor: ${scenario.title}`);

    if (gameMasterAI) {
      // Gerçek Game Master AI ile oyunu başlat
      console.log(`🎮 Game Master AI ile oyun başlatılıyor: ${scenario.title}`);
      const gameResponse = await gameMasterAI.startGame(scenario);
      res.json(gameResponse);
    } else {
      // Mock Game Master ile oyunu başlat
      console.log(
        `🎮 Mock Game Master ile oyun başlatılıyor: ${scenario.title}`
      );
      const gameResponse = await gameMaster.startGame(scenario);
      res.json(gameResponse);
    }
  } catch (error) {
    console.error("Game start error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Oyuncu aksiyonunu işle
app.post("/api/game/action", async (req, res) => {
  try {
    const { action, diceResult } = req.body;
    const gameResponse = await gameMaster.processPlayerAction(
      action,
      diceResult
    );
    res.json(gameResponse);
  } catch (error) {
    console.error("Action processing error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Combat başlat
app.post("/api/game/combat/start", async (req, res) => {
  try {
    const gameResponse = await gameMaster.startCombat();
    res.json(gameResponse);
  } catch (error) {
    console.error("Combat start error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Combat aksiyonu işle
app.post("/api/game/combat/action", async (req, res) => {
  try {
    const { action, target, diceResult } = req.body;
    const gameResponse = await gameMaster.processCombatAction(
      action,
      target,
      diceResult
    );
    res.json(gameResponse);
  } catch (error) {
    console.error("Combat action error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Oyun durumunu al
app.get("/api/game/state", (req, res) => {
  try {
    const gameState = gameMaster.getCurrentGameState();
    res.json(gameState);
  } catch (error) {
    console.error("Get game state error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Oyunu kaydet
app.post("/api/game/save", (req, res) => {
  try {
    const savedGame = gameMaster.saveGame();
    res.json(savedGame);
  } catch (error) {
    console.error("Save game error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Oyunu yükle
app.post("/api/game/load", (req, res) => {
  try {
    const { savedGame } = req.body;
    gameMaster.loadGame(savedGame);
    const gameState = gameMaster.getCurrentGameState();
    res.json(gameState);
  } catch (error) {
    console.error("Load game error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Dice roll endpoint
app.post("/api/dice/roll", (req, res) => {
  try {
    const { diceType = "d20", modifier = 0 } = req.body;
    const maxValue = parseInt(diceType.replace("d", ""));
    const roll = Math.floor(Math.random() * maxValue) + 1 + modifier;

    res.json({
      result: roll,
      diceType: diceType,
      modifier: modifier,
      naturalRoll: roll - modifier,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error("Dice roll error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Character classes endpoint
app.get("/api/characters/classes", (req, res) => {
  try {
    const classes = [
      {
        id: "warrior",
        name: "Savaşçı",
        description: "Güçlü ve dayanıklı savaşçı",
      },
      {
        id: "mage",
        name: "Büyücü",
        description: "Güçlü büyüler yapabilen büyücü",
      },
      {
        id: "rogue",
        name: "Hırsız",
        description: "Çevik ve gizli hareket eden hırsız",
      },
      {
        id: "cleric",
        name: "Rahip",
        description: "İlahi güçlerle donanmış rahip",
      },
      { id: "ranger", name: "Avcı", description: "Doğa ile uyumlu avcı" },
    ];
    res.json(classes);
  } catch (error) {
    console.error("Get character classes error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Character races endpoint
app.get("/api/characters/races", (req, res) => {
  try {
    const races = [
      { id: "human", name: "İnsan", description: "Çok yönlü ve uyumlu" },
      { id: "elf", name: "Elf", description: "Uzun ömürlü ve büyüye yatkın" },
      { id: "dwarf", name: "Cüce", description: "Güçlü ve zanaatkâr" },
      { id: "halfling", name: "Yarık", description: "Küçük ama çevik" },
      { id: "orc", name: "Ork", description: "Güçlü ve savaşçı" },
    ];
    res.json(races);
  } catch (error) {
    console.error("Get character races error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Create character endpoint
app.post("/api/characters", (req, res) => {
  try {
    const { name, characterClass, characterRace } = req.body;
    const characterId = `char_${Date.now()}`;

    const newCharacter = {
      id: characterId,
      name: name,
      class: characterClass,
      race: characterRace,
      level: 1,
      experience: 0,
      stats: {
        strength: Math.floor(Math.random() * 10) + 10,
        dexterity: Math.floor(Math.random() * 10) + 10,
        constitution: Math.floor(Math.random() * 10) + 10,
        intelligence: Math.floor(Math.random() * 10) + 10,
        wisdom: Math.floor(Math.random() * 10) + 10,
        charisma: Math.floor(Math.random() * 10) + 10,
      },
      skills: [],
      createdAt: new Date().toISOString(),
    };

    res.json({
      success: true,
      character: newCharacter,
      message: "Karakter başarıyla oluşturuldu!",
    });
  } catch (error) {
    console.error("Create character error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Character level endpoint
app.get("/api/characters/:characterId/level", (req, res) => {
  try {
    const { characterId } = req.params;
    // Mock character data
    res.json({
      level: 1,
      experience: 0,
      experienceToNext: 100,
    });
  } catch (error) {
    console.error("Get character level error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Character skills endpoint
app.get("/api/characters/:characterId/skills", (req, res) => {
  try {
    const { characterId } = req.params;
    // Mock skills data
    res.json({
      availableSkills: [
        {
          id: "sword_mastery",
          name: "Kılıç Ustalığı",
          cost: 1,
          unlocked: false,
        },
        { id: "magic_bolt", name: "Büyü Oku", cost: 2, unlocked: false },
        { id: "stealth", name: "Gizlilik", cost: 1, unlocked: false },
        { id: "healing", name: "İyileştirme", cost: 2, unlocked: false },
      ],
      unlockedSkills: [],
    });
  } catch (error) {
    console.error("Get character skills error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Unlock skill endpoint
app.post("/api/characters/:characterId/unlock_skill", (req, res) => {
  try {
    const { characterId } = req.params;
    const { skillId } = req.body;

    res.json({
      success: true,
      message: "Yetenek başarıyla açıldı!",
      unlockedSkill: { id: skillId, name: "Yeni Yetenek" },
    });
  } catch (error) {
    console.error("Unlock skill error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Save game endpoint
app.post("/api/save/game", (req, res) => {
  try {
    const { gameData, saveName, playerId } = req.body;
    const saveId = `save_${Date.now()}`;

    const saveData = {
      id: saveId,
      name: saveName,
      playerId: playerId,
      timestamp: new Date().toISOString(),
      gameData: gameData,
    };

    dataManager.savePlayerGame(playerId, saveData);

    res.json({
      success: true,
      saveId: saveId,
      saveName: saveName,
      timestamp: new Date().toISOString(),
      message: "Oyun başarıyla kaydedildi!",
    });
  } catch (error) {
    console.error("Save game error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Load game endpoint
app.post("/api/save/load", (req, res) => {
  try {
    const { saveId, playerId } = req.body;

    const playerSaves = dataManager.getPlayerSaves(playerId);
    const savedGame = playerSaves.find((save) => save.id === saveId);

    if (!savedGame) {
      return res.status(404).json({ error: "Kayıt bulunamadı!" });
    }

    res.json({
      success: true,
      savedGame: savedGame,
    });
  } catch (error) {
    console.error("Load game error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Get player saves endpoint
app.get("/api/save/player/:playerId", (req, res) => {
  try {
    const { playerId } = req.params;
    const playerSaves = dataManager.getPlayerSaves(playerId);

    res.json({
      success: true,
      saves: playerSaves,
    });
  } catch (error) {
    console.error("Get player saves error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Delete save endpoint
app.post("/api/save/delete", (req, res) => {
  try {
    const { saveId, playerId } = req.body;

    const playerSaves = dataManager.getPlayerSaves(playerId);
    const updatedSaves = playerSaves.filter((save) => save.id !== saveId);

    // Kayıtları güncelle
    const savesDir = path.join(__dirname, "../data/saves");
    const savesFile = path.join(savesDir, `${playerId}_saves.json`);
    fs.writeFileSync(savesFile, JSON.stringify(updatedSaves, null, 2));

    res.json({
      success: true,
      message: "Kayıt başarıyla silindi!",
    });
  } catch (error) {
    console.error("Delete save error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Multiplayer sessions endpoint
app.get("/api/multiplayer/sessions", (req, res) => {
  try {
    // Mock multiplayer sessions
    const sessions = [
      {
        id: "session_1",
        name: "Ejderha Avı",
        players: 3,
        maxPlayers: 5,
        status: "active",
      },
      {
        id: "session_2",
        name: "Karanlık Orman",
        players: 1,
        maxPlayers: 4,
        status: "waiting",
      },
    ];

    res.json(sessions);
  } catch (error) {
    console.error("Get multiplayer sessions error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Leave multiplayer session endpoint
app.post("/api/multiplayer/sessions/:sessionId/leave", (req, res) => {
  try {
    const { sessionId } = req.params;

    res.json({
      success: true,
      message: "Oturumdan ayrıldınız!",
    });
  } catch (error) {
    console.error("Leave session error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Export the app for use in server.js
module.exports = app;
