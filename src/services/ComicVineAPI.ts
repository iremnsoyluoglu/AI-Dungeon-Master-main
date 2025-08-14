import axios from "axios";

export interface ComicVineConfig {
  apiKey: string;
  baseUrl: string;
  rateLimit: number; // requests per hour
}

export interface ComicVineIssue {
  id: number;
  name: string;
  issue_number: string;
  volume: {
    name: string;
    publisher: {
      name: string;
    };
  };
  description: string;
  deck: string;
  image: {
    medium_url: string;
    screen_url: string;
  };
  character_credits: ComicVineCharacter[];
  team_credits: ComicVineTeam[];
  location_credits: ComicVineLocation[];
  concept_credits: ComicVineConcept[];
  story_arc_credits: ComicVineStoryArc[];
  person_credits: ComicVinePerson[];
  api_detail_url: string;
  site_detail_url: string;
}

export interface ComicVineCharacter {
  id: number;
  name: string;
  deck: string;
  description: string;
  image: {
    medium_url: string;
  };
  real_name: string;
  aliases: string;
  birth: string;
  powers: string;
  origin: {
    name: string;
  };
  publisher: {
    name: string;
  };
}

export interface ComicVineTeam {
  id: number;
  name: string;
  deck: string;
  description: string;
  image: {
    medium_url: string;
  };
}

export interface ComicVineLocation {
  id: number;
  name: string;
  deck: string;
  description: string;
}

export interface ComicVineConcept {
  id: number;
  name: string;
  deck: string;
  description: string;
}

export interface ComicVineStoryArc {
  id: number;
  name: string;
  deck: string;
  description: string;
}

export interface ComicVinePerson {
  id: number;
  name: string;
  role: string;
}

export interface ComicVineSearchResult {
  results: ComicVineIssue[];
  number_of_total_results: number;
  status_code: number;
}

export class ComicVineAPI {
  private config: ComicVineConfig;
  private requestCount: number = 0;
  private lastRequestTime: number = 0;

  constructor(config: ComicVineConfig) {
    this.config = config;
  }

  private async makeRequest(
    endpoint: string,
    params: Record<string, any> = {}
  ) {
    // Rate limiting check
    const now = Date.now();
    if (now - this.lastRequestTime < 1000) {
      // 1 second between requests
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }

    if (this.requestCount >= this.config.rateLimit) {
      throw new Error(
        "Rate limit exceeded. Please wait before making more requests."
      );
    }

    const url = `${this.config.baseUrl}${endpoint}`;
    const queryParams = new URLSearchParams({
      api_key: this.config.apiKey,
      format: "json",
      ...params,
    });

    try {
      const response = await axios.get(`${url}?${queryParams}`);
      this.requestCount++;
      this.lastRequestTime = now;
      return response.data;
    } catch (error) {
      console.error("Comic Vine API error:", error);
      throw error;
    }
  }

  // Search for comics by title
  async searchComics(
    query: string,
    limit: number = 10
  ): Promise<ComicVineSearchResult> {
    return await this.makeRequest("/search", {
      resources: "issue",
      query: query,
      limit: limit,
    });
  }

  // Get comic issues by volume
  async getIssuesByVolume(
    volumeId: number,
    limit: number = 20
  ): Promise<ComicVineSearchResult> {
    return await this.makeRequest("/volume/4050-" + volumeId + "/issues", {
      limit: limit,
    });
  }

  // Get specific issue details
  async getIssueDetails(issueId: number): Promise<{ results: ComicVineIssue }> {
    return await this.makeRequest("/issue/4000-" + issueId);
  }

  // Get character details
  async getCharacterDetails(
    characterId: number
  ): Promise<{ results: ComicVineCharacter }> {
    return await this.makeRequest("/character/4005-" + characterId);
  }

  // Get popular comics (trending)
  async getPopularComics(limit: number = 10): Promise<ComicVineSearchResult> {
    return await this.makeRequest("/issues", {
      sort: "date_last_updated:desc",
      limit: limit,
    });
  }

  // Get comics by publisher
  async getComicsByPublisher(
    publisherId: number,
    limit: number = 20
  ): Promise<ComicVineSearchResult> {
    return await this.makeRequest(
      "/publisher/4010-" + publisherId + "/issues",
      {
        limit: limit,
      }
    );
  }

  // Get comics by genre/theme
  async getComicsByTheme(
    theme: string,
    limit: number = 10
  ): Promise<ComicVineSearchResult> {
    return await this.makeRequest("/search", {
      resources: "issue",
      query: theme,
      limit: limit,
    });
  }

  // Get story arc details
  async getStoryArcDetails(arcId: number): Promise<any> {
    return await this.makeRequest("/story_arc/4045-" + arcId);
  }

  // Get issues in a story arc
  async getIssuesInStoryArc(
    arcId: number,
    limit: number = 20
  ): Promise<ComicVineSearchResult> {
    return await this.makeRequest("/story_arc/4045-" + arcId + "/issues", {
      limit: limit,
    });
  }

  // Search for characters
  async searchCharacters(query: string, limit: number = 10): Promise<any> {
    return await this.makeRequest("/search", {
      resources: "character",
      query: query,
      limit: limit,
    });
  }

  // Get team details
  async getTeamDetails(teamId: number): Promise<any> {
    return await this.makeRequest("/team/4060-" + teamId);
  }

  // Reset rate limit counter (for testing)
  resetRateLimit() {
    this.requestCount = 0;
    this.lastRequestTime = 0;
  }

  // Get current rate limit status
  getRateLimitStatus() {
    return {
      requestsMade: this.requestCount,
      limit: this.config.rateLimit,
      remaining: this.config.rateLimit - this.requestCount,
    };
  }
}
