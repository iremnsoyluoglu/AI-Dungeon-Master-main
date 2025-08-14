import { FRPRPGScenario } from "./frpMechanics";

export interface StoredScenario {
  id: string;
  title: string;
  theme: string;
  difficulty: string;
  createdAt: Date;
  lastModified: Date;
  scenario: FRPRPGScenario;
  metadata: ScenarioMetadata;
  tags: string[];
  isFavorite: boolean;
  playCount: number;
  averageRating: number;
}

export interface ScenarioMetadata {
  sourceComics: string[];
  learningSessionId: string;
  generationTime: number; // milliseconds
  llmModel: string;
  llmProvider: string;
  tokenUsage?: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
  version: string;
}

export interface ScenarioFilter {
  theme?: string;
  difficulty?: string;
  tags?: string[];
  dateRange?: {
    start: Date;
    end: Date;
  };
  isFavorite?: boolean;
  minRating?: number;
}

export interface ScenarioSearchResult {
  scenarios: StoredScenario[];
  totalCount: number;
  page: number;
  pageSize: number;
}

export interface ScenarioStats {
  totalScenarios: number;
  scenariosByTheme: Record<string, number>;
  scenariosByDifficulty: Record<string, number>;
  averageGenerationTime: number;
  mostUsedTags: Array<{ tag: string; count: number }>;
  recentScenarios: StoredScenario[];
}
