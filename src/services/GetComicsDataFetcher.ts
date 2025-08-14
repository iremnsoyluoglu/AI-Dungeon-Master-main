import { ComicData, ComicPage, DialogueLine } from "../types/llmComic";
import {
  ComicVineAPI,
  ComicVineIssue,
  ComicVineCharacter,
} from "./ComicVineAPI";

export class GetComicsDataFetcher {
  private comicVineAPI: ComicVineAPI;

  constructor() {
    this.comicVineAPI = new ComicVineAPI({
      apiKey: process.env.COMIC_VINE_API_KEY || "",
      baseUrl: "https://comicvine.gamespot.com/api",
      rateLimit: 200, // Comic Vine allows 200 requests per hour
    });
  }

  // Comic Vine'dan comic verisi çek ve LLM formatına dönüştür
  async fetchComicsForLLM(
    genre: string,
    count: number = 1
  ): Promise<ComicData[]> {
    try {
      // Genre'e göre comic ara
      const searchResults = await this.comicVineAPI.searchComics(genre, count);

      const comics: ComicData[] = [];

      for (const issue of searchResults.results.slice(0, count)) {
        // Detaylı issue bilgilerini al
        const detailedIssue = await this.comicVineAPI.getIssueDetails(issue.id);
        const comicData = detailedIssue.results;

        // LLM formatına dönüştür
        const comic: ComicData = {
          title: comicData.name,
          genre: this.extractGenre(comicData),
          series: comicData.volume?.name || "Unknown Series",
          pages: await this.createComicPages(comicData),
        };

        comics.push(comic);
      }

      return comics;
    } catch (error) {
      console.error("Error fetching comics from Comic Vine:", error);
      // Fallback to mock data
      return this.getMockComics(genre, count);
    }
  }

  private async createComicPages(issue: ComicVineIssue): Promise<ComicPage[]> {
    const pages: ComicPage[] = [];

    // Comic Vine'dan gelen veriyi analiz et
    const description = issue.description || issue.deck || "";
    const characters = issue.character_credits || [];
    const locations = issue.location_credits || [];
    const concepts = issue.concept_credits || [];

    // Description'ı sayfalara böl (basit bölme)
    const sentences = description
      .split(/[.!?]+/)
      .filter((s) => s.trim().length > 0);
    const sentencesPerPage = Math.max(1, Math.floor(sentences.length / 3));

    for (
      let i = 0;
      i < Math.min(3, Math.ceil(sentences.length / sentencesPerPage));
      i++
    ) {
      const startIndex = i * sentencesPerPage;
      const endIndex = Math.min(
        startIndex + sentencesPerPage,
        sentences.length
      );
      const pageSentences = sentences.slice(startIndex, endIndex);

      const page: ComicPage = {
        pageNumber: i + 1,
        imageUrl: issue.image?.medium_url || "",
        extractedText: pageSentences.join(". ") + ".",
        panelDescriptions: this.generatePanelDescriptions(
          pageSentences,
          characters,
          locations
        ),
        characterDialogue: this.generateCharacterDialogue(
          characters,
          pageSentences
        ),
      };

      pages.push(page);
    }

    return pages;
  }

  private generatePanelDescriptions(
    sentences: string[],
    characters: ComicVineCharacter[],
    locations: any[]
  ): string[] {
    const descriptions: string[] = [];

    // Her cümle için panel açıklaması oluştur
    sentences.forEach((sentence, index) => {
      let description = sentence;

      // Karakter isimlerini ekle
      if (characters.length > 0 && index < characters.length) {
        const character = characters[index];
        description = `${character.name} is featured in this panel. ${sentence}`;
      }

      // Lokasyon bilgisi ekle
      if (locations.length > 0 && index < locations.length) {
        const location = locations[index];
        description = `Scene takes place in ${location.name}. ${description}`;
      }

      descriptions.push(description);
    });

    return descriptions;
  }

  private generateCharacterDialogue(
    characters: ComicVineCharacter[],
    sentences: string[]
  ): DialogueLine[] {
    const dialogue: DialogueLine[] = [];

    characters.forEach((character, index) => {
      if (index < sentences.length) {
        dialogue.push({
          character: character.name,
          text: sentences[index],
          emotion: this.detectEmotion(sentences[index]),
          context: character.deck || "general",
        });
      }
    });

    return dialogue;
  }

  private detectEmotion(text: string): string {
    const lowerText = text.toLowerCase();

    if (
      lowerText.includes("!") ||
      lowerText.includes("angry") ||
      lowerText.includes("rage")
    ) {
      return "angry";
    } else if (
      lowerText.includes("?") ||
      lowerText.includes("wonder") ||
      lowerText.includes("curious")
    ) {
      return "curious";
    } else if (
      lowerText.includes("happy") ||
      lowerText.includes("joy") ||
      lowerText.includes("laugh")
    ) {
      return "happy";
    } else if (
      lowerText.includes("sad") ||
      lowerText.includes("cry") ||
      lowerText.includes("tear")
    ) {
      return "sad";
    } else if (
      lowerText.includes("fear") ||
      lowerText.includes("scared") ||
      lowerText.includes("terrified")
    ) {
      return "fearful";
    } else {
      return "neutral";
    }
  }

  private extractGenre(issue: ComicVineIssue): string {
    // Volume'dan genre çıkarmaya çalış
    const volumeName = issue.volume?.name?.toLowerCase() || "";
    const description = (issue.description || "").toLowerCase();

    if (volumeName.includes("fantasy") || description.includes("fantasy")) {
      return "fantasy";
    } else if (
      volumeName.includes("sci-fi") ||
      volumeName.includes("science") ||
      description.includes("space")
    ) {
      return "sci-fi";
    } else if (
      volumeName.includes("horror") ||
      description.includes("horror")
    ) {
      return "horror";
    } else if (
      volumeName.includes("superhero") ||
      description.includes("superhero")
    ) {
      return "superhero";
    } else if (
      volumeName.includes("western") ||
      description.includes("western")
    ) {
      return "western";
    } else {
      return "adventure";
    }
  }

  // Mock data fallback
  private getMockComics(genre: string, count: number): ComicData[] {
    return [
      {
        title: `Mock ${genre} Comic`,
        genre: genre,
        series: "Mock Series",
        pages: [
          {
            pageNumber: 1,
            imageUrl: "https://example.com/mock.jpg",
            extractedText: "This is a mock comic for testing purposes.",
            panelDescriptions: ["Mock panel description"],
            characterDialogue: [
              {
                character: "Mock Character",
                text: "Mock dialogue",
                emotion: "neutral",
                context: "mock",
              },
            ],
          },
        ],
      },
    ];
  }

  // Test Comic Vine API connection
  async testConnection(): Promise<boolean> {
    try {
      const result = await this.comicVineAPI.searchComics("test", 1);
      return result.status_code === 1;
    } catch (error) {
      console.error("Comic Vine API test failed:", error);
      return false;
    }
  }
}
