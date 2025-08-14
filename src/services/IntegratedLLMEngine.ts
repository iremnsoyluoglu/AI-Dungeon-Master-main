import { ComicData, LearningResponse, RPGScenario } from "../types/llmComic";
import { FRPRPGScenario, FRPMechanics } from "../types/frpMechanics";
import { LLMComicLearningSystem } from "./LLMComicLearningSystem";
import { FRPLLMEngine } from "./FRPLLMEngine";
import { ScenarioDatabase } from "./ScenarioDatabase";
import { StoredScenario } from "../types/scenarioStorage";

export class IntegratedLLMEngine {
  private comicLearningSystem: LLMComicLearningSystem;
  private frpEngine: FRPLLMEngine;
  private scenarioDatabase: ScenarioDatabase;

  constructor() {
    this.comicLearningSystem = new LLMComicLearningSystem();
    this.frpEngine = new FRPLLMEngine();
    this.scenarioDatabase = new ScenarioDatabase();
    this.scenarioDatabase.initialize();
  }

  // Comic'ten hem genel hem FRP mekaniklerini öğren
  async learnFromComic(comicData: ComicData): Promise<{
    generalLearning: LearningResponse;
    frpMechanics: FRPMechanics;
  }> {
    const [generalLearning, frpMechanics] = await Promise.all([
      this.comicLearningSystem.feedComicToLLM(comicData),
      this.frpEngine.learnFRPFromComic(comicData),
    ]);

    return { generalLearning, frpMechanics };
  }

  // Hem genel hem FRP mekaniklerini kullanarak senaryo üret ve otomatik kaydet
  async generateIntegratedScenario(
    theme: string,
    difficulty: string
  ): Promise<StoredScenario> {
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

  private mergeScenarios(
    general: RPGScenario,
    frp: FRPRPGScenario
  ): FRPRPGScenario {
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

  private convertToFRPScenes(generalScenes: any[]): any[] {
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

  private createDecisionPointsFromChoices(choices: string[]): any[] {
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
  getSystemStatus(): {
    generalKnowledge: string;
    frpKnowledge: string;
    learnedComics: number;
    learnedFRPMechanics: number;
  } {
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
  async getAllScenarios(): Promise<StoredScenario[]> {
    return await this.scenarioDatabase.getAllScenarios();
  }

  // Favori senaryoları getir
  async getFavoriteScenarios(): Promise<StoredScenario[]> {
    return await this.scenarioDatabase.getFavorites();
  }

  // Favori durumunu değiştir
  async toggleFavorite(scenarioId: string): Promise<boolean> {
    return await this.scenarioDatabase.toggleFavorite(scenarioId);
  }
}
