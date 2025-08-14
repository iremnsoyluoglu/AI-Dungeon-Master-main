const { LLMComicLearningSystem } = require("./LLMComicLearningSystem");
const { FRPLLMEngine } = require("./FRPLLMEngine");
const { ScenarioDatabase } = require("./ScenarioDatabase");

class IntegratedLLMEngine {
  constructor() {
    this.comicLearningSystem = new LLMComicLearningSystem();
    this.frpEngine = new FRPLLMEngine();
    this.scenarioDatabase = new ScenarioDatabase();
    this.scenarioDatabase.initialize();
  }

  // Comic'ten hem genel hem FRP mekaniklerini öğren
  async learnFromComic(comicData) {
    const [generalLearning, frpMechanics] = await Promise.all([
      this.comicLearningSystem.feedComicToLLM(comicData),
      this.frpEngine.learnFRPFromComic(comicData),
    ]);

    return { generalLearning, frpMechanics };
  }

  // Hem genel hem FRP mekaniklerini kullanarak senaryo üret ve otomatik kaydet
  async generateIntegratedScenario(theme, difficulty) {
    const startTime = Date.now();

    // Önce genel senaryo üret
    const generalScenario =
      await this.comicLearningSystem.generateScenarioFromLearning(
        theme,
        difficulty
      );

    // Sonra FRP mekaniklerini ekle
    const frpScenario = await this.frpEngine.generateFRPScenario(
      theme,
      difficulty
    );

    // İkisini birleştir
    const integratedScenario = this.mergeScenarios(
      generalScenario,
      frpScenario
    );

    // Otomatik kaydet
    const generationTime = Date.now() - startTime;
    const storedScenario = await this.scenarioDatabase.saveScenario(
      integratedScenario,
      {
        sourceComics: ["Dungeons & Dragons: The Lost Relic"], // Mock data
        learningSessionId: `session_${Date.now()}`,
        generationTime,
        llmModel: process.env.LLM_MODEL || "gpt-4",
        llmProvider: process.env.LLM_PROVIDER || "openai",
      },
      [theme, difficulty, "auto-generated"]
    );

    console.log(`🎯 Scenario generated and saved: ${storedScenario.title}`);
    return storedScenario;
  }

  mergeScenarios(general, frp) {
    return {
      title: general.title,
      theme: general.theme || frp.theme,
      difficulty: general.difficulty || frp.difficulty,
      scenes: this.convertToFRPScenes(general.scenes),
      npcs: frp.npcs,
      combatEncounters: frp.combatEncounters,
      diceMechanics: frp.diceMechanics,
    };
  }

  convertToFRPScenes(generalScenes) {
    return generalScenes.map((scene) => ({
      id: `scene_${Math.random().toString(36).substr(2, 9)}`,
      title: scene.title,
      description: scene.description,
      npcs: [],
      decisionPoints: this.createDecisionPointsFromChoices(scene.choices || []),
      combatEncounter: undefined,
      rewards: [],
      nextScenes: [],
    }));
  }

  createDecisionPointsFromChoices(choices) {
    if (!choices || choices.length === 0) return [];

    return [
      {
        id: `decision_${Math.random().toString(36).substr(2, 9)}`,
        title: "Player Choice",
        description: "Choose your next action",
        choices: choices.map((choice, index) => ({
          text: choice,
          requiredSkill: undefined,
          requiredStat: undefined,
          diceRoll: undefined,
          consequences: {
            immediate: `You chose: ${choice}`,
            longTerm: "Your choice will affect the story",
          },
          nextScene: undefined,
        })),
      },
    ];
  }

  // Sistem durumunu al
  getSystemStatus() {
    return {
      generalKnowledge: this.comicLearningSystem.getKnowledgeBase()
        ? "Available"
        : "Not available",
      frpKnowledge: this.frpEngine.getAccumulatedKnowledge()
        ? "Available"
        : "Not available",
      learnedComics: 1, // Mock value
      learnedFRPMechanics: this.frpEngine.getLearnedFRPMechanics().length,
    };
  }

  // Kaydedilen senaryoları getir
  async getAllScenarios() {
    return await this.scenarioDatabase.getAllScenarios();
  }

  // Favori senaryoları getir
  async getFavoriteScenarios() {
    return await this.scenarioDatabase.getFavorites();
  }

  // Favori durumunu değiştir
  async toggleFavorite(scenarioId) {
    return await this.scenarioDatabase.toggleFavorite(scenarioId);
  }
}

module.exports = { IntegratedLLMEngine }; 