const { ComicVineAPI } = require("./ComicVineAPI");

class GetComicsDataFetcher {
  constructor() {
    this.comicVineAPI = new ComicVineAPI();
  }

  // Comic Vine API'den comic verisi çek
  async fetchComicData(searchTerm) {
    try {
      console.log(`🔍 Comic Vine'da aranıyor: ${searchTerm}`);

      // Comic arama
      const searchResults = await this.comicVineAPI.searchComics(searchTerm);

      if (!searchResults || searchResults.length === 0) {
        throw new Error("Comic bulunamadı");
      }

      // İlk sonucu al
      const firstResult = searchResults[0];
      console.log(`📚 Comic bulundu: ${firstResult.name}`);

      // Detaylı bilgileri al
      const comicDetails = await this.comicVineAPI.getIssueDetails(
        firstResult.id
      );

      // Comic verisi oluştur
      const comicData = this.createComicData(firstResult, comicDetails);

      console.log(`✅ Comic verisi hazırlandı: ${comicData.title}`);
      return comicData;
    } catch (error) {
      console.error("Comic fetching error:", error);
      // Mock data if API fails
      return this.getMockComicData(searchTerm);
    }
  }

  createComicData(searchResult, details) {
    return {
      title: searchResult.name || "Unknown Comic",
      genre: searchResult.genre || "adventure",
      publisher: searchResult.publisher || "Unknown Publisher",
      pages: this.createMockPages(searchResult, details),
      extractedText:
        details?.description ||
        searchResult.description ||
        "No description available",
      source: "comicvine",
      apiId: searchResult.id,
    };
  }

  createMockPages(searchResult, details) {
    // Mock sayfa verisi oluştur (gerçek sistemde OCR ile çekilecek)
    const pageCount = Math.floor(Math.random() * 20) + 10; // 10-30 sayfa
    const pages = [];

    for (let i = 1; i <= pageCount; i++) {
      pages.push({
        pageNumber: i,
        panelDescriptions: [
          `Panel ${i * 3 - 2}: ${this.getRandomPanelDescription()}`,
          `Panel ${i * 3 - 1}: ${this.getRandomPanelDescription()}`,
          `Panel ${i * 3}: ${this.getRandomPanelDescription()}`,
        ],
        characterDialogue: [
          {
            character: this.getRandomCharacter(),
            text: this.getRandomDialogue(),
          },
          {
            character: this.getRandomCharacter(),
            text: this.getRandomDialogue(),
          },
        ],
        extractedText: `Page ${i} text content with some dialogue and action descriptions.`,
      });
    }

    return pages;
  }

  getRandomPanelDescription() {
    const descriptions = [
      "Hero standing in dramatic pose",
      "Villain plotting in shadows",
      "Action scene with explosions",
      "Character dialogue moment",
      "Landscape establishing shot",
      "Close-up emotional moment",
      "Battle scene with weapons",
      "Mysterious artifact revealed",
    ];
    return descriptions[Math.floor(Math.random() * descriptions.length)];
  }

  getRandomCharacter() {
    const characters = [
      "Hero",
      "Villain",
      "Sidekick",
      "Mentor",
      "Guardian",
      "Merchant",
      "Wizard",
      "Warrior",
    ];
    return characters[Math.floor(Math.random() * characters.length)];
  }

  getRandomDialogue() {
    const dialogues = [
      "We must find the ancient artifact!",
      "The prophecy speaks of this moment.",
      "I will not let you destroy everything!",
      "The power is within you.",
      "This is our only chance.",
      "The darkness is spreading.",
      "We need to work together.",
      "The time has come.",
    ];
    return dialogues[Math.floor(Math.random() * dialogues.length)];
  }

  getMockComicData(searchTerm) {
    return {
      title: `${searchTerm} Adventure`,
      genre: "adventure",
      publisher: "Mock Publisher",
      pages: this.createMockPages({ name: searchTerm }, {}),
      extractedText: `Mock comic data for ${searchTerm}. This is a placeholder for when the API is not available.`,
      source: "mock",
      apiId: "mock_id",
    };
  }

  // Karakter arama
  async searchCharacters(characterName) {
    try {
      return await this.comicVineAPI.searchCharacters(characterName);
    } catch (error) {
      console.error("Character search error:", error);
      return [];
    }
  }

  // Comic detaylarını al
  async getComicDetails(comicId) {
    try {
      return await this.comicVineAPI.getIssueDetails(comicId);
    } catch (error) {
      console.error("Comic details error:", error);
      return null;
    }
  }
}

module.exports = { GetComicsDataFetcher };
