const fetch = require("node-fetch");

class ComicVineAPI {
  constructor() {
    this.apiKey = process.env.COMIC_VINE_API_KEY;
    this.baseUrl = "https://comicvine.gamespot.com/api";
    this.rateLimitDelay = 1000; // 1 saniye bekleme
    this.lastRequestTime = 0;
  }

  async makeRequest(endpoint, params = {}) {
    // Rate limiting
    const now = Date.now();
    const timeSinceLastRequest = now - this.lastRequestTime;
    if (timeSinceLastRequest < this.rateLimitDelay) {
      await new Promise((resolve) =>
        setTimeout(resolve, this.rateLimitDelay - timeSinceLastRequest)
      );
    }
    this.lastRequestTime = Date.now();

    const url = new URL(`${this.baseUrl}${endpoint}`);
    url.searchParams.append("api_key", this.apiKey);
    url.searchParams.append("format", "json");

    // Diğer parametreleri ekle
    Object.entries(params).forEach(([key, value]) => {
      url.searchParams.append(key, value);
    });

    try {
      const response = await fetch(url.toString());
      if (!response.ok) {
        throw new Error(
          `Comic Vine API error: ${response.status} ${response.statusText}`
        );
      }
      return await response.json();
    } catch (error) {
      console.error("Comic Vine API request failed:", error);
      throw error;
    }
  }

  async searchComics(query, limit = 10) {
    try {
      const data = await this.makeRequest("/search/", {
        resources: "issue",
        query: query,
        limit: limit.toString(),
        field_list:
          "id,name,description,image,volume,issue_number,cover_date,person_credits,character_credits",
      });

      return data.results || [];
    } catch (error) {
      console.error("Comic search failed:", error);
      // Mock data if API fails
      return this.getMockSearchResults(query, limit);
    }
  }

  async getIssueDetails(issueId) {
    try {
      const data = await this.makeRequest(`/issue/4000-${issueId}/`, {
        field_list:
          "id,name,description,image,volume,issue_number,cover_date,person_credits,character_credits,story_arc_credits,team_credits,location_credits,concept_credits,object_credits,character_died_in,disbanded_teams,first_appearance_characters,first_appearance_concepts,first_appearance_locations,first_appearance_objects,first_appearance_story_arcs,first_appearance_teams",
      });

      return data.results || null;
    } catch (error) {
      console.error("Issue details fetch failed:", error);
      return this.getMockIssueDetails(issueId);
    }
  }

  async searchCharacters(characterName, limit = 10) {
    try {
      const data = await this.makeRequest("/search/", {
        resources: "character",
        query: characterName,
        limit: limit.toString(),
        field_list:
          "id,name,description,image,real_name,aliases,powers,origin,first_appeared_in_issue",
      });

      return data.results || [];
    } catch (error) {
      console.error("Character search failed:", error);
      return this.getMockCharacterResults(characterName, limit);
    }
  }

  async getVolumeDetails(volumeId) {
    try {
      const data = await this.makeRequest(`/volume/4050-${volumeId}/`, {
        field_list:
          "id,name,description,image,start_year,publisher,count_of_issues,deck",
      });

      return data.results || null;
    } catch (error) {
      console.error("Volume details fetch failed:", error);
      return this.getMockVolumeDetails(volumeId);
    }
  }

  // Mock data methods
  getMockSearchResults(query, limit) {
    return Array.from({ length: Math.min(limit, 5) }, (_, i) => ({
      id: `mock_issue_${i + 1}`,
      name: `${query} #${i + 1}`,
      description: `Mock comic issue for ${query}`,
      image: null,
      volume: {
        name: `${query} Series`,
        id: `mock_volume_${i + 1}`,
      },
      issue_number: i + 1,
      cover_date: "2023-01-01",
      person_credits: [],
      character_credits: [],
    }));
  }

  getMockIssueDetails(issueId) {
    return {
      id: issueId,
      name: `Mock Issue ${issueId}`,
      description:
        "This is a mock comic issue with detailed information for testing purposes.",
      image: null,
      volume: {
        name: "Mock Series",
        id: "mock_volume_1",
      },
      issue_number: 1,
      cover_date: "2023-01-01",
      person_credits: [
        { name: "Mock Writer", role: "writer" },
        { name: "Mock Artist", role: "artist" },
      ],
      character_credits: [
        { name: "Mock Hero", role: "hero" },
        { name: "Mock Villain", role: "villain" },
      ],
      story_arc_credits: [],
      team_credits: [],
      location_credits: [],
      concept_credits: [],
      object_credits: [],
    };
  }

  getMockCharacterResults(characterName, limit) {
    return Array.from({ length: Math.min(limit, 3) }, (_, i) => ({
      id: `mock_character_${i + 1}`,
      name: `${characterName} ${i + 1}`,
      description: `Mock character ${i + 1} for ${characterName}`,
      image: null,
      real_name: `Real Name ${i + 1}`,
      aliases: [`Alias ${i + 1}`, `Nickname ${i + 1}`],
      powers: ["Super Strength", "Flight", "Laser Vision"],
      origin: "Mock Origin Story",
      first_appeared_in_issue: {
        name: "Mock Issue #1",
        id: "mock_issue_1",
      },
    }));
  }

  getMockVolumeDetails(volumeId) {
    return {
      id: volumeId,
      name: "Mock Volume",
      description: "This is a mock comic volume for testing purposes.",
      image: null,
      start_year: 2023,
      publisher: {
        name: "Mock Publisher",
        id: "mock_publisher_1",
      },
      count_of_issues: 12,
      deck: "A mock comic series",
    };
  }
}

module.exports = { ComicVineAPI };
