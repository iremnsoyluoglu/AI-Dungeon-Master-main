export interface ComicData {
  title: string;
  pages: ComicPage[];
  genre: string;
  series: string;
}

export interface ComicPage {
  pageNumber: number;
  imageUrl: string;
  extractedText: string;
  panelDescriptions: string[];
  characterDialogue: DialogueLine[];
}

export interface DialogueLine {
  character: string;
  text: string;
  emotion: string;
  context: string;
}

export interface LearningResponse {
  llmResponse: string;
  learnedKnowledge: LearnedKnowledge;
}

export interface LearnedKnowledge {
  storyPatterns: string[];
  characterArchetypes: string[];
  worldBuilding: string[];
  actionSequences: string[];
  rpgConversion: string[];
}

export interface RPGScenario {
  title: string;
  scenes: any[];
  boss: any;
  theme: string;
  difficulty: string;
} 