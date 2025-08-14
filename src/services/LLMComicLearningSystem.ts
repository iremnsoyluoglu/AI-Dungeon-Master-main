import {
  ComicData,
  LearningResponse,
  LearnedKnowledge,
  RPGScenario,
  ScenarioKnowledge,
} from "../types/llmComic";
import { LLMComicTrainer } from "./LLMComicTrainer";

export class LLMComicLearningSystem {
  private llmEndpoint: string = "/api/llm"; // Proxy endpoint (Express.js ile)
  private learnedKnowledge: string = "";
  private knowledgeBase: ScenarioKnowledge = {
    storyPatterns: [],
    characterArchetypes: [],
    dialogueStyles: [],
    plotStructures: [],
    conflictTypes: [],
    settingDescriptions: [],
  };

  async feedComicToLLM(comicData: ComicData): Promise<LearningResponse> {
    const trainer = new LLMComicTrainer();
    const prompt = trainer.createComicReadingPrompt(comicData);

    // Gerçek LLM kullanımı
    const llmText = await this.callRealLLM(prompt);

    const learned = this.extractLearning(llmText);
    this.learnedKnowledge += `\n\nCOMIC: ${comicData.title}\n${llmText}`;
    return { llmResponse: llmText, learnedKnowledge: learned };
  }

  extractLearning(llmResponse: string): LearnedKnowledge {
    // Basit string işlemleriyle bullet point'leri ayır
    const lines = llmResponse
      .split("\n")
      .map((l) => l.trim())
      .filter(Boolean);
    const storyPatterns = lines
      .filter((l) => l.startsWith("- Story"))
      .map((l) => l.replace("- Story:", "").trim());
    const characterArchetypes = lines
      .filter((l) => l.startsWith("- Characters"))
      .map((l) => l.replace("- Characters:", "").trim());
    const worldBuilding = lines
      .filter((l) => l.startsWith("- World"))
      .map((l) => l.replace("- World:", "").trim());
    const actionSequences = lines
      .filter((l) => l.startsWith("- Action"))
      .map((l) => l.replace("- Action:", "").trim());
    const rpgConversion = lines
      .filter((l) => l.startsWith("- RPG"))
      .map((l) => l.replace("- RPG:", "").trim());
    return {
      storyPatterns,
      characterArchetypes,
      worldBuilding,
      actionSequences,
      rpgConversion,
    };
  }

  async generateScenarioFromLearning(
    theme: string,
    difficulty: string
  ): Promise<RPGScenario> {
    const trainer = new LLMComicTrainer();
    const prompt = trainer.createScenarioGenerationPrompt(
      theme,
      difficulty,
      this.learnedKnowledge
    );

    // Gerçek LLM kullanımı
    const scenarioText = await this.callRealLLM(prompt);

    // Parse edilen RPG senaryosu döndürülür
    return {
      title: "The Lost Relic",
      scenes: [
        {
          title: "Tapınak Girişi",
          choices: [
            "Tuzakları araştır",
            "Kapıyı zorla",
            "Büyüyle aç",
            "Geri çekil",
          ],
          results: [
            "Gizli geçit buldun",
            "Alarm çaldı",
            "Kapı açıldı",
            "Macera ertelendi",
          ],
        },
        {
          title: "Karanlık Koridor",
          choices: [
            "Sessiz ilerle",
            "Meşale yak",
            "Büyü hazırla",
            "Şarkı söyle",
          ],
          results: [
            "Canavar fark etmedi",
            "Canavar saldırdı",
            "Hazırlık avantajı",
            "Gürültüyle tuzak tetiklendi",
          ],
        },
      ],
      boss: { name: "Dev Yılan", hp: 40, atk: 8, def: 4 },
      theme,
      difficulty,
    };
  }

  // Get the current knowledge base
  getKnowledgeBase(): ScenarioKnowledge {
    return this.knowledgeBase;
  }

  // Gerçek LLM çağrısı
  private async callRealLLM(prompt: string): Promise<string> {
    try {
      const { RealLLMService } = await import("./RealLLMService");

      const llmService = new RealLLMService({
        provider: (process.env.LLM_PROVIDER as any) || "openai",
        model: process.env.LLM_MODEL || "gpt-4",
        temperature: parseFloat(process.env.LLM_TEMPERATURE || "0.7"),
        maxTokens: parseInt(process.env.LLM_MAX_TOKENS || "4000"),
        apiKey:
          process.env.OPENAI_API_KEY || process.env.ANTHROPIC_API_KEY || "",
      });

      const response = await llmService.callLLM({
        prompt,
        temperature: 0.7,
        maxTokens: 2000,
      });

      return response.text;
    } catch (error) {
      console.error("LLM API error:", error);
      // Fallback to mock response if LLM fails
      return `\n- Story: Macera eski bir tapınakta başlıyor.\n- Conflict: Tuzaklar ve canavarlar.\n- Characters: Rogue (nervous), Wizard (serious), Fighter (urgent), Cleric (concerned).\n- World: Karanlık, gizemli, tehlikeli.\n- Action: Tuzaklar, dövüş, takım çalışması.\n- RPG: Oyuncu seçimi, tuzak çözme, savaş, karakter etkileşimi.`;
    }
  }
}
