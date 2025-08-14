export interface ComicPanel {
  id: string;
  imageUrl: string;
  text: string[];
  characters: string[];
  setting: string;
  mood: string;
  actionType: "dialogue" | "action" | "exposition" | "transition";
}

export interface ComicIssue {
  title: string;
  series: string;
  genre: "fantasy" | "sci-fi" | "horror" | "adventure" | "superhero";
  panels: ComicPanel[];
  storyStructure: StoryElement[];
  coverUrl?: string;
  issueNumber?: string;
  publisher?: string;
  year?: number;
}

export interface StoryElement {
  type:
    | "setup"
    | "conflict"
    | "choice"
    | "consequence"
    | "climax"
    | "resolution";
  description: string;
  characters: string[];
  location: string;
  pageNumber?: number;
}

export interface StoryPattern {
  type: string;
  rpgEquivalent: string;
  effectiveness: number;
  usage: "opening" | "middle" | "climax";
  description: string;
}

export interface CharacterArchetype {
  name: string;
  role: "quest_giver" | "ally" | "enemy" | "merchant" | "mentor" | "trickster";
  personality: string[];
  typicalDialogue: string[];
  visualDescription: string;
  rpgStats: RPGStats;
}

export interface RPGStats {
  strength?: number;
  dexterity?: number;
  constitution?: number;
  intelligence?: number;
  wisdom?: number;
  charisma?: number;
  level?: number;
  class?: string;
}

export interface LearnedPatterns {
  storyFlow: StoryPattern[];
  characters: CharacterArchetype[];
  dialogue: DialoguePattern[];
  mood: MoodPattern[];
  actionSequences: ActionPattern[];
}

export interface DialoguePattern {
  type: "threat" | "persuasion" | "information" | "banter" | "monologue";
  examples: string[];
  effectiveness: number;
  context: string;
}

export interface MoodPattern {
  type: "tension" | "mystery" | "action" | "calm" | "horror";
  visualElements: string[];
  dialogueCues: string[];
  rpgEquivalent: string;
}

export interface ActionPattern {
  type: "combat" | "chase" | "stealth" | "social" | "exploration";
  setup: string;
  climax: string;
  resolution: string;
  rpgMechanics: string[];
}

export interface ScenarioKnowledge {
  storyPatterns: StoryPattern[];
  characterArchetypes: CharacterArchetype[];
  dialogueStyles: DialoguePattern[];
  plotStructures: StoryElement[];
  conflictTypes: string[];
  settingDescriptions: string[];
}

export interface RPGScenario {
  title: string;
  setting: string;
  scenes: RPGGameScene[];
  npcs: CharacterArchetype[];
  conflicts: string[];
  boss?: CharacterArchetype;
  difficulty: "easy" | "medium" | "hard";
  estimatedDuration: string;
}

export interface RPGGameScene {
  title: string;
  description: string;
  location: string;
  characters: string[];
  choices: string[];
  consequences: string[];
  rpgMechanics: string[];
}
