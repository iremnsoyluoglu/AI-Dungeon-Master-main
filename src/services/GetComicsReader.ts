import axios from "axios";
import * as cheerio from "cheerio";
import { ComicIssue, ComicPanel, StoryElement } from "../types/comic";

export class GetComicsReader {
  private baseUrl = "https://getcomics.info";
  private apiEndpoint = "https://getcomics.info/wp-json/wp/v2";

  constructor() {
    // Set up axios with proper headers to avoid blocking
    axios.defaults.headers.common["User-Agent"] =
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36";
  }

  async fetchComicsByGenre(
    genre: string,
    limit: number = 20
  ): Promise<ComicIssue[]> {
    try {
      console.log(`Fetching ${genre} comics from GetComics...`);

      // Search for comics by genre
      const searchResults = await this.searchComics({
        genre: genre,
        tags: this.getGenreTags(genre),
        limit: limit,
      });

      const processedComics: ComicIssue[] = [];

      for (const comic of searchResults) {
        try {
          console.log(`Processing comic: ${comic.title}`);
          const processed = await this.processComicPages(comic);
          processedComics.push(processed);

          // Add delay to avoid overwhelming the server
          await this.delay(1000);
        } catch (error) {
          console.error(`Error processing comic ${comic.title}:`, error);
          continue;
        }
      }

      return processedComics;
    } catch (error) {
      console.error("Error fetching comics:", error);
      throw new Error(`Failed to fetch ${genre} comics: ${error}`);
    }
  }

  private async searchComics(params: {
    genre: string;
    tags: string[];
    limit: number;
  }): Promise<any[]> {
    try {
      // Search for comics using WordPress API
      const response = await axios.get(`${this.apiEndpoint}/posts`, {
        params: {
          search: params.genre,
          per_page: params.limit,
          _embed: true,
        },
      });

      return response.data.filter(
        (post: any) =>
          post.title.rend.toLowerCase().includes(params.genre.toLowerCase()) ||
          params.tags.some((tag) =>
            post.content.rend.toLowerCase().includes(tag.toLowerCase())
          )
      );
    } catch (error) {
      console.error("Error searching comics:", error);
      // Fallback to mock data for development
      return this.getMockComics(params.genre, params.limit);
    }
  }

  private async processComicPages(comic: any): Promise<ComicIssue> {
    try {
      // Extract comic data from WordPress post
      const comicData = this.extractComicData(comic);

      // Get comic pages (in real implementation, this would download and process images)
      const panels = await this.extractPanels(comicData.pages || []);

      // Extract text from panels
      const textData = await this.extractText(panels);

      // Analyze story structure
      const storyStructure = this.analyzeStoryStructure(textData);

      return {
        title: comicData.title,
        series: comicData.series,
        genre: this.determineGenre(comicData),
        panels: panels,
        storyStructure: storyStructure,
        coverUrl: comicData.coverUrl,
        issueNumber: comicData.issueNumber,
        publisher: comicData.publisher,
        year: comicData.year,
      };
    } catch (error) {
      console.error("Error processing comic pages:", error);
      throw error;
    }
  }

  private extractComicData(post: any): any {
    const $ = cheerio.load(post.content.rend);

    return {
      title: post.title.rend,
      series: this.extractSeries(post.title.rend),
      coverUrl: this.extractCoverUrl($),
      issueNumber: this.extractIssueNumber(post.title.rend),
      publisher: this.extractPublisher($),
      year: this.extractYear(post.title.rend),
      pages: this.extractPageLinks($),
    };
  }

  private async extractPanels(pages: string[]): Promise<ComicPanel[]> {
    const panels: ComicPanel[] = [];

    for (let i = 0; i < pages.length; i++) {
      const pageUrl = pages[i];

      // In a real implementation, this would:
      // 1. Download the image
      // 2. Use computer vision to detect panels
      // 3. Extract text from each panel

      // For now, create mock panels
      const panelCount = Math.floor(Math.random() * 6) + 4; // 4-9 panels per page

      for (let j = 0; j < panelCount; j++) {
        panels.push({
          id: `page_${i}_panel_${j}`,
          imageUrl: pageUrl,
          text: this.generateMockText(),
          characters: this.generateMockCharacters(),
          setting: this.generateMockSetting(),
          mood: this.generateMockMood(),
          actionType: this.generateMockActionType(),
        });
      }
    }

    return panels;
  }

  private async extractText(panels: ComicPanel[]): Promise<string[]> {
    const allText: string[] = [];

    for (const panel of panels) {
      // In real implementation, use OCR (Tesseract.js) to extract text
      allText.push(...panel.text);
    }

    return allText;
  }

  private analyzeStoryStructure(textData: string[]): StoryElement[] {
    const storyElements: StoryElement[] = [];

    // Simple story structure analysis based on text patterns
    const setupKeywords = [
      "beginning",
      "start",
      "introduction",
      "arrive",
      "enter",
    ];
    const conflictKeywords = [
      "fight",
      "battle",
      "conflict",
      "danger",
      "threat",
      "enemy",
    ];
    const choiceKeywords = ["decide", "choose", "option", "either", "or"];
    const climaxKeywords = [
      "final",
      "climax",
      "ultimate",
      "showdown",
      "battle",
    ];
    const resolutionKeywords = [
      "end",
      "conclusion",
      "victory",
      "defeat",
      "resolve",
    ];

    let currentType: StoryElement["type"] = "setup";
    let currentText = "";
    let characterCount = 0;

    for (const text of textData) {
      const lowerText = text.toLowerCase();

      // Determine story element type based on keywords
      if (conflictKeywords.some((keyword) => lowerText.includes(keyword))) {
        if (currentText) {
          storyElements.push({
            type: currentType,
            description: currentText.trim(),
            characters: this.extractCharacters(currentText),
            location: this.extractLocation(currentText),
          });
        }
        currentType = "conflict";
        currentText = text;
      } else if (
        choiceKeywords.some((keyword) => lowerText.includes(keyword))
      ) {
        if (currentText) {
          storyElements.push({
            type: currentType,
            description: currentText.trim(),
            characters: this.extractCharacters(currentText),
            location: this.extractLocation(currentText),
          });
        }
        currentType = "choice";
        currentText = text;
      } else if (
        climaxKeywords.some((keyword) => lowerText.includes(keyword))
      ) {
        if (currentText) {
          storyElements.push({
            type: currentType,
            description: currentText.trim(),
            characters: this.extractCharacters(currentText),
            location: this.extractLocation(currentText),
          });
        }
        currentType = "climax";
        currentText = text;
      } else if (
        resolutionKeywords.some((keyword) => lowerText.includes(keyword))
      ) {
        if (currentText) {
          storyElements.push({
            type: currentType,
            description: currentText.trim(),
            characters: this.extractCharacters(currentText),
            location: this.extractLocation(currentText),
          });
        }
        currentType = "resolution";
        currentText = text;
      } else {
        currentText += " " + text;
      }
    }

    // Add the last element
    if (currentText) {
      storyElements.push({
        type: currentType,
        description: currentText.trim(),
        characters: this.extractCharacters(currentText),
        location: this.extractLocation(currentText),
      });
    }

    return storyElements;
  }

  private extractCharacters(text: string): string[] {
    // Simple character extraction (in real implementation, use NLP)
    const characterPatterns = [
      /([A-Z][a-z]+ [A-Z][a-z]+)/g, // Full names
      /([A-Z][a-z]+)/g, // Single names
      /(the [A-Z][a-z]+)/g, // "The" + name
    ];

    const characters: string[] = [];

    for (const pattern of characterPatterns) {
      const matches = text.match(pattern);
      if (matches) {
        characters.push(...matches);
      }
    }

    return [...new Set(characters)].slice(0, 5); // Limit to 5 characters
  }

  private extractLocation(text: string): string {
    const locationKeywords = [
      "in",
      "at",
      "inside",
      "outside",
      "near",
      "within",
    ];
    const words = text.split(" ");

    for (let i = 0; i < words.length - 1; i++) {
      if (locationKeywords.includes(words[i].toLowerCase())) {
        return words[i + 1] || "Unknown location";
      }
    }

    return "Unknown location";
  }

  private getGenreTags(genre: string): string[] {
    const genreTags: { [key: string]: string[] } = {
      fantasy: [
        "D&D",
        "Dungeons",
        "Dragons",
        "Conan",
        "Lord of the Rings",
        "fantasy",
      ],
      "sci-fi": [
        "Star Wars",
        "Star Trek",
        "40K",
        "Warhammer",
        "Alien",
        "sci-fi",
      ],
      horror: ["Hellboy", "Constantine", "zombie", "vampire", "horror"],
      adventure: ["Indiana Jones", "adventure", "exploration", "treasure"],
      superhero: ["Marvel", "DC", "superhero", "comics"],
    };

    return genreTags[genre] || ["comics"];
  }

  private determineGenre(comicData: any): ComicIssue["genre"] {
    const title = comicData.title.toLowerCase();
    const series = comicData.series.toLowerCase();

    if (
      title.includes("d&d") ||
      title.includes("dungeon") ||
      title.includes("conan")
    ) {
      return "fantasy";
    } else if (
      title.includes("star") ||
      title.includes("warhammer") ||
      title.includes("alien")
    ) {
      return "sci-fi";
    } else if (
      title.includes("hellboy") ||
      title.includes("constantine") ||
      title.includes("zombie")
    ) {
      return "horror";
    } else if (title.includes("indiana") || title.includes("adventure")) {
      return "adventure";
    } else {
      return "superhero";
    }
  }

  // Helper methods for data extraction
  private extractSeries(title: string): string {
    const seriesPatterns = [
      /(.+?)\s+#\d+/i,
      /(.+?)\s+vol\.\d+/i,
      /(.+?)\s+issue\s+\d+/i,
    ];

    for (const pattern of seriesPatterns) {
      const match = title.match(pattern);
      if (match) {
        return match[1].trim();
      }
    }

    return "Unknown Series";
  }

  private extractCoverUrl($: cheerio.CheerioAPI): string {
    const img = $("img").first();
    return img.attr("src") || "";
  }

  private extractIssueNumber(title: string): string {
    const match = title.match(/#(\d+)/i);
    return match ? match[1] : "";
  }

  private extractPublisher($: cheerio.CheerioAPI): string {
    const text = $.text();
    const publishers = ["Marvel", "DC", "Dark Horse", "Image", "IDW"];

    for (const publisher of publishers) {
      if (text.includes(publisher)) {
        return publisher;
      }
    }

    return "Unknown Publisher";
  }

  private extractYear(title: string): number {
    const match = title.match(/(19|20)\d{2}/);
    return match ? parseInt(match[0]) : new Date().getFullYear();
  }

  private extractPageLinks($: cheerio.CheerioAPI): string[] {
    const links: string[] = [];
    $('a[href*=".jpg"], a[href*=".png"], a[href*=".jpeg"]').each(
      (_, element) => {
        const href = $(element).attr("href");
        if (href) {
          links.push(href);
        }
      }
    );
    return links;
  }

  // Mock data generation for development
  private getMockComics(genre: string, limit: number): any[] {
    const mockComics = [
      {
        title: "Dungeons & Dragons: Honor Among Thieves #1",
        series: "Dungeons & Dragons",
        genre: "fantasy",
      },
      {
        title: "Conan the Barbarian: The Cimmerian #1",
        series: "Conan",
        genre: "fantasy",
      },
      {
        title: "Star Wars: Dark Empire #1",
        series: "Star Wars",
        genre: "sci-fi",
      },
      {
        title: "Hellboy: Seed of Destruction #1",
        series: "Hellboy",
        genre: "horror",
      },
      {
        title: "Indiana Jones: The Lost World #1",
        series: "Indiana Jones",
        genre: "adventure",
      },
    ];

    return mockComics.filter((comic) => comic.genre === genre).slice(0, limit);
  }

  private generateMockText(): string[] {
    const mockTexts = [
      "The ancient temple loomed before them.",
      "We must find the sacred artifact!",
      "The dragon's roar echoed through the cavern.",
      "Choose your path wisely, adventurer.",
      "The battle raged on as spells flew through the air.",
      "In the depths of the dungeon, something stirred.",
      "The treasure was within reach, but at what cost?",
      "Dark forces gathered in the shadows.",
      "The prophecy spoke of a chosen one.",
      "Magic crackled in the air around them.",
    ];

    const count = Math.floor(Math.random() * 3) + 1;
    const selected = [];

    for (let i = 0; i < count; i++) {
      selected.push(mockTexts[Math.floor(Math.random() * mockTexts.length)]);
    }

    return selected;
  }

  private generateMockCharacters(): string[] {
    const characters = [
      "Gandalf",
      "Aragorn",
      "Legolas",
      "Gimli",
      "Frodo",
      "Conan",
      "Red Sonja",
      "Thoth-Amon",
      "Belit",
      "Luke Skywalker",
      "Han Solo",
      "Darth Vader",
      "Leia",
      "Hellboy",
      "Abe Sapien",
      "Liz Sherman",
      "Johann Kraus",
      "Indiana Jones",
      "Marion",
      "Sallah",
      "Marcus",
    ];

    const count = Math.floor(Math.random() * 3) + 1;
    const selected = [];

    for (let i = 0; i < count; i++) {
      selected.push(characters[Math.floor(Math.random() * characters.length)]);
    }

    return [...new Set(selected)];
  }

  private generateMockSetting(): string {
    const settings = [
      "Ancient Temple",
      "Dark Forest",
      "Mountain Pass",
      "Desert Oasis",
      "Underground Cavern",
      "Castle Ruins",
      "Space Station",
      "Alien Planet",
      "Cyberpunk City",
      "Haunted Mansion",
      "Cursed Village",
      "Abandoned Mine",
    ];

    return settings[Math.floor(Math.random() * settings.length)];
  }

  private generateMockMood(): string {
    const moods = ["tension", "mystery", "action", "calm", "horror"];
    return moods[Math.floor(Math.random() * moods.length)];
  }

  private generateMockActionType(): ComicPanel["actionType"] {
    const types: ComicPanel["actionType"][] = [
      "dialogue",
      "action",
      "exposition",
      "transition",
    ];
    return types[Math.floor(Math.random() * types.length)];
  }

  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}
