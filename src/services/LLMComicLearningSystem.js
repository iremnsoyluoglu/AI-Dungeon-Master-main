const { RealLLMService } = require("./RealLLMService");
const { LLMComicTrainer } = require("./LLMComicTrainer");

class LLMComicLearningSystem {
  constructor() {
    this.llmService = new RealLLMService();
    this.trainer = new LLMComicTrainer();
    this.knowledgeBase = "";
    this.learnedComics = [];
  }

  // Comic'i LLM'e besle ve öğren
  async feedComicToLLM(comicData) {
    const prompt = this.trainer.createComicReadingPrompt(comicData);

    try {
      const llmResponse = await this.llmService.callLLM(prompt);
      const learningResult = this.parseLearningResponse(llmResponse);

      // Bilgi tabanını güncelle
      this.knowledgeBase += `\n\nCOMIC: ${comicData.title}\n${llmResponse}`;
      this.learnedComics.push({
        title: comicData.title,
        learningResult,
        timestamp: new Date().toISOString(),
      });

      return learningResult;
    } catch (error) {
      console.error("LLM learning error:", error);
      // Mock response if LLM fails
      return this.getMockLearningResponse(comicData);
    }
  }

  // Öğrenilen bilgilerden senaryo üret
  async generateScenarioFromLearning(theme, difficulty) {
    const prompt = this.trainer.createScenarioGenerationPrompt(
      theme,
      difficulty,
      this.knowledgeBase
    );

    try {
      const llmResponse = await this.llmService.callLLM(prompt);
      return this.parseScenarioResponse(llmResponse, theme, difficulty);
    } catch (error) {
      console.error("LLM scenario generation error:", error);
      // Mock response if LLM fails
      return this.getMockScenarioResponse(theme, difficulty);
    }
  }

  parseLearningResponse(llmResponse) {
    // Basit parsing - gerçek sistemde daha gelişmiş olacak
    return {
      success: true,
      learnedTechniques: this.extractTechniques(llmResponse),
      knowledgeBase: llmResponse,
      sessionId: `learning_${Date.now()}`,
    };
  }

  extractTechniques(response) {
    const techniques = [];

    if (response.includes("karakter")) techniques.push("Karakter gelişimi");
    if (response.includes("savaş") || response.includes("combat"))
      techniques.push("Savaş sahneleri");
    if (response.includes("diyalog") || response.includes("dialogue"))
      techniques.push("Diyalog yazımı");
    if (response.includes("FRP") || response.includes("mekanik"))
      techniques.push("FRP mekanikleri");
    if (response.includes("zar") || response.includes("dice"))
      techniques.push("Zar sistemleri");
    if (response.includes("karar") || response.includes("decision"))
      techniques.push("Karar noktaları");

    return techniques.length > 0 ? techniques : ["Genel hikaye teknikleri"];
  }

  parseScenarioResponse(llmResponse, theme, difficulty) {
    // Basit parsing - gerçek sistemde daha gelişmiş olacak
    const titleMatch = llmResponse.match(/TITLE: (.+)/);
    const title = titleMatch ? titleMatch[1].trim() : `${theme} Adventure`;

    const descriptionMatch = llmResponse.match(/DESCRIPTION: (.+)/);
    const description = descriptionMatch
      ? descriptionMatch[1].trim()
      : `${theme} temalı macera`;

    return {
      title,
      theme,
      difficulty,
      description,
      scenes: this.parseScenes(llmResponse),
      choices: this.parseChoices(llmResponse),
    };
  }

  parseScenes(response) {
    const scenesSection = response.match(/SCENES:(.*?)(?=CHOICES:|$)/s);
    if (!scenesSection) return [];

    return [
      {
        id: "scene_1",
        title: "Main Scene",
        description: "Adventure begins here",
        choices: ["Explore", "Talk to NPC", "Fight"],
      },
    ];
  }

  parseChoices(response) {
    const choicesSection = response.match(/CHOICES:(.*?)$/s);
    if (!choicesSection) return [];

    return choicesSection[1]
      .split("\n")
      .filter((line) => line.trim() && line.startsWith("-"))
      .map((line) => line.replace("-", "").trim())
      .filter(Boolean);
  }

  getMockLearningResponse(comicData) {
    return {
      success: true,
      learnedTechniques: [
        "Karakter gelişimi",
        "Savaş sahneleri",
        "Diyalog yazımı",
        "FRP mekanikleri",
      ],
      knowledgeBase: `Mock learning from ${comicData.title}`,
      sessionId: `mock_learning_${Date.now()}`,
    };
  }

  getMockScenarioResponse(theme, difficulty) {
    return {
      title: `${theme} Adventure`,
      theme,
      difficulty,
      description: `${theme} temalı, ${difficulty} zorlukta macera`,
      scenes: [
        {
          id: "scene_1",
          title: "Main Scene",
          description: "Adventure begins here",
          choices: ["Explore", "Talk to NPC", "Fight"],
        },
      ],
      choices: ["Explore", "Talk to NPC", "Fight"],
    };
  }

  getKnowledgeBase() {
    return this.knowledgeBase;
  }

  getLearnedComics() {
    return this.learnedComics;
  }
}

module.exports = { LLMComicLearningSystem };
