import {
  ComicIssue,
  ComicPanel,
  StoryElement,
  LearnedPatterns,
  StoryPattern,
  CharacterArchetype,
  DialoguePattern,
  MoodPattern,
  ActionPattern,
  ScenarioKnowledge,
  RPGStats,
} from "../types/comic";

export class ComicLearningEngine {
  private knowledgeBase: ScenarioKnowledge = {
    storyPatterns: [],
    characterArchetypes: [],
    dialogueStyles: [],
    plotStructures: [],
    conflictTypes: [],
    settingDescriptions: [],
  };

  constructor() {
    this.initializeKnowledgeBase();
  }

  // Main method to process comics and learn patterns
  async processComic(comicData: ComicIssue): Promise<LearnedPatterns> {
    console.log(`Learning from comic: ${comicData.title}`);

    const patterns: LearnedPatterns = {
      storyFlow: this.analyzeStoryFlow(comicData.storyStructure),
      characters: this.analyzeCharacters(comicData.panels),
      dialogue: this.analyzeDialogue(comicData.panels),
      mood: this.analyzeMood(comicData.panels),
      actionSequences: this.analyzeActionSequences(comicData.panels),
    };

    // Update knowledge base with learned patterns
    this.updateKnowledgeBase(patterns);

    return patterns;
  }

  // Get the current knowledge base
  getKnowledgeBase(): ScenarioKnowledge {
    return this.knowledgeBase;
  }

  // Analyze story flow and convert to RPG concepts
  private analyzeStoryFlow(storyElements: StoryElement[]): StoryPattern[] {
    const patterns: StoryPattern[] = [];

    for (const element of storyElements) {
      const rpgEquivalent = this.convertToRPGConcept(element);
      const effectiveness = this.calculateEffectiveness(element);
      const usage = this.determineUsage(element);

      patterns.push({
        type: element.type,
        rpgEquivalent,
        effectiveness,
        usage,
        description: element.description,
      });
    }

    return patterns;
  }

  // Convert story elements to RPG concepts
  private convertToRPGConcept(element: StoryElement): string {
    const rpgMappings: { [key: string]: string } = {
      setup: "Session Opening - Introduce the quest and setting",
      conflict: "Combat Encounter - Players face enemies or challenges",
      choice: "Player Decision Point - Multiple paths forward",
      consequence: "Outcome Resolution - Results of player choices",
      climax: "Boss Battle - Final confrontation",
      resolution: "Session Conclusion - Wrap up and rewards",
    };

    return rpgMappings[element.type] || "General RPG Scene";
  }

  // Calculate effectiveness of story elements
  private calculateEffectiveness(element: StoryElement): number {
    let score = 0.5; // Base score

    // Score based on character involvement
    score += element.characters.length * 0.1;

    // Score based on description length (more detail = better)
    score += Math.min(element.description.length / 100, 0.3);

    // Score based on location specificity
    if (element.location !== "Unknown location") {
      score += 0.2;
    }

    return Math.min(score, 1.0);
  }

  // Determine where in the story this element is used
  private determineUsage(
    element: StoryElement
  ): "opening" | "middle" | "climax" {
    if (element.type === "setup") return "opening";
    if (element.type === "climax" || element.type === "resolution")
      return "climax";
    return "middle";
  }

  // Analyze characters and convert to RPG archetypes
  private analyzeCharacters(panels: ComicPanel[]): CharacterArchetype[] {
    const characterMap = new Map<string, any>();

    // Extract all characters from panels
    for (const panel of panels) {
      for (const charName of panel.characters) {
        if (!characterMap.has(charName)) {
          characterMap.set(charName, {
            name: charName,
            appearances: 0,
            dialogues: [],
            contexts: [],
            moods: [],
          });
        }

        const char = characterMap.get(charName);
        char.appearances++;
        char.contexts.push(panel.setting);
        char.moods.push(panel.mood);
      }
    }

    // Convert to RPG archetypes
    const archetypes: CharacterArchetype[] = [];
    for (const [name, char] of characterMap) {
      archetypes.push({
        name,
        role: this.determineRPGRole(char),
        personality: this.extractPersonality(char),
        typicalDialogue: this.extractDialoguePatterns(char),
        visualDescription: this.generateVisualDescription(char),
        rpgStats: this.suggestRPGStats(char),
      });
    }

    return archetypes;
  }

  // Determine RPG role based on character analysis
  private determineRPGRole(char: any): CharacterArchetype["role"] {
    const appearances = char.appearances;
    const contexts = char.contexts;
    const moods = char.moods;

    // Analyze patterns to determine role
    if (appearances > 10) {
      return "quest_giver";
    } else if (moods.some((m: string) => m === "horror" || m === "tension")) {
      return "enemy";
    } else if (
      contexts.some((c: string) => c.includes("shop") || c.includes("market"))
    ) {
      return "merchant";
    } else if (appearances > 5) {
      return "ally";
    } else {
      return "trickster";
    }
  }

  // Extract personality traits from character data
  private extractPersonality(char: any): string[] {
    const traits: string[] = [];
    const moods = char.moods;

    if (moods.some((m: string) => m === "action")) {
      traits.push("brave", "aggressive");
    }
    if (moods.some((m: string) => m === "mystery")) {
      traits.push("mysterious", "secretive");
    }
    if (moods.some((m: string) => m === "calm")) {
      traits.push("wise", "patient");
    }
    if (moods.some((m: string) => m === "horror")) {
      traits.push("fearsome", "intimidating");
    }

    return traits.length > 0 ? traits : ["neutral"];
  }

  // Extract dialogue patterns
  private extractDialoguePatterns(char: any): string[] {
    // In a real implementation, this would analyze actual dialogue
    const patterns = [
      "Greetings and introductions",
      "Quest descriptions",
      "Warnings about dangers",
      "Information sharing",
    ];

    return patterns.slice(0, Math.floor(Math.random() * 3) + 1);
  }

  // Generate visual description
  private generateVisualDescription(char: any): string {
    const descriptions = [
      "Tall and imposing figure",
      "Wizened old character",
      "Young and energetic",
      "Mysterious hooded figure",
      "Armored warrior",
      "Robed mage",
    ];

    return descriptions[Math.floor(Math.random() * descriptions.length)];
  }

  // Suggest RPG stats based on character analysis
  private suggestRPGStats(char: any): RPGStats {
    const role = this.determineRPGRole(char);
    const baseStats = {
      strength: 10,
      dexterity: 10,
      constitution: 10,
      intelligence: 10,
      wisdom: 10,
      charisma: 10,
      level: 1,
      class: "Commoner",
    };

    switch (role) {
      case "quest_giver":
        return {
          ...baseStats,
          charisma: 16,
          wisdom: 14,
          level: 5,
          class: "Noble",
        };
      case "enemy":
        return {
          ...baseStats,
          strength: 16,
          constitution: 14,
          level: 8,
          class: "Warrior",
        };
      case "merchant":
        return {
          ...baseStats,
          charisma: 14,
          intelligence: 12,
          level: 3,
          class: "Merchant",
        };
      case "ally":
        return {
          ...baseStats,
          dexterity: 14,
          wisdom: 12,
          level: 4,
          class: "Ranger",
        };
      default:
        return baseStats;
    }
  }

  // Analyze dialogue patterns
  private analyzeDialogue(panels: ComicPanel[]): DialoguePattern[] {
    const dialoguePanels = panels.filter((p) => p.actionType === "dialogue");
    const patterns: DialoguePattern[] = [];

    // Analyze different types of dialogue
    const dialogueTypes: DialoguePattern["type"][] = [
      "threat",
      "persuasion",
      "information",
      "banter",
      "monologue",
    ];

    for (const type of dialogueTypes) {
      const relevantPanels = dialoguePanels.filter((p) =>
        p.text.some((t) => this.matchesDialogueType(t, type))
      );

      if (relevantPanels.length > 0) {
        patterns.push({
          type,
          examples: this.extractDialogueExamples(relevantPanels),
          effectiveness: this.calculateDialogueEffectiveness(relevantPanels),
          context: this.determineDialogueContext(relevantPanels),
        });
      }
    }

    return patterns;
  }

  // Check if text matches dialogue type
  private matchesDialogueType(
    text: string,
    type: DialoguePattern["type"]
  ): boolean {
    const lowerText = text.toLowerCase();

    switch (type) {
      case "threat":
        return (
          lowerText.includes("kill") ||
          lowerText.includes("destroy") ||
          lowerText.includes("die")
        );
      case "persuasion":
        return (
          lowerText.includes("please") ||
          lowerText.includes("help") ||
          lowerText.includes("need")
        );
      case "information":
        return (
          lowerText.includes("tell") ||
          lowerText.includes("know") ||
          lowerText.includes("find")
        );
      case "banter":
        return (
          lowerText.includes("joke") ||
          lowerText.includes("laugh") ||
          lowerText.includes("funny")
        );
      case "monologue":
        return text.length > 100; // Long text blocks
      default:
        return false;
    }
  }

  // Extract dialogue examples
  private extractDialogueExamples(panels: ComicPanel[]): string[] {
    return panels
      .flatMap((p) => p.text)
      .filter((t) => t.length > 10 && t.length < 200)
      .slice(0, 5);
  }

  // Calculate dialogue effectiveness
  private calculateDialogueEffectiveness(panels: ComicPanel[]): number {
    let score = 0.5;

    // More dialogue panels = higher effectiveness
    score += Math.min(panels.length / 10, 0.3);

    // Variety in text length = better dialogue
    const textLengths = panels.flatMap((p) => p.text).map((t) => t.length);
    const variance = this.calculateVariance(textLengths);
    score += Math.min(variance / 1000, 0.2);

    return Math.min(score, 1.0);
  }

  // Determine dialogue context
  private determineDialogueContext(panels: ComicPanel[]): string {
    const settings = panels.map((p) => p.setting);
    const mostCommon = this.getMostCommon(settings);
    return mostCommon || "General conversation";
  }

  // Analyze mood patterns
  private analyzeMood(panels: ComicPanel[]): MoodPattern[] {
    const moodGroups = new Map<string, ComicPanel[]>();

    // Group panels by mood
    for (const panel of panels) {
      if (!moodGroups.has(panel.mood)) {
        moodGroups.set(panel.mood, []);
      }
      moodGroups.get(panel.mood)!.push(panel);
    }

    const patterns: MoodPattern[] = [];

    for (const [mood, moodPanels] of moodGroups) {
      patterns.push({
        type: mood as MoodPattern["type"],
        visualElements: this.extractVisualElements(moodPanels),
        dialogueCues: this.extractDialogueCues(moodPanels),
        rpgEquivalent: this.convertMoodToRPG(mood),
      });
    }

    return patterns;
  }

  // Extract visual elements for mood
  private extractVisualElements(panels: ComicPanel[]): string[] {
    const elements: string[] = [];

    for (const panel of panels) {
      if (panel.setting.includes("dark") || panel.setting.includes("shadow")) {
        elements.push("dark lighting", "shadows");
      }
      if (
        panel.setting.includes("ancient") ||
        panel.setting.includes("temple")
      ) {
        elements.push("ancient architecture", "mystical symbols");
      }
      if (
        panel.setting.includes("forest") ||
        panel.setting.includes("nature")
      ) {
        elements.push("natural environment", "organic shapes");
      }
    }

    return [...new Set(elements)];
  }

  // Extract dialogue cues for mood
  private extractDialogueCues(panels: ComicPanel[]): string[] {
    const cues: string[] = [];

    for (const panel of panels) {
      for (const text of panel.text) {
        if (text.includes("!")) cues.push("exclamation");
        if (text.includes("?")) cues.push("question");
        if (text.includes("...")) cues.push("hesitation");
        if (text.length > 50) cues.push("detailed explanation");
      }
    }

    return [...new Set(cues)];
  }

  // Convert mood to RPG equivalent
  private convertMoodToRPG(mood: string): string {
    const moodMappings: { [key: string]: string } = {
      tension: "Combat preparation or stealth sequence",
      mystery: "Investigation or puzzle solving",
      action: "Combat encounter or chase sequence",
      calm: "Social interaction or rest period",
      horror: "Horror encounter or survival challenge",
    };

    return moodMappings[mood] || "General scene";
  }

  // Analyze action sequences
  private analyzeActionSequences(panels: ComicPanel[]): ActionPattern[] {
    const actionPanels = panels.filter((p) => p.actionType === "action");
    const patterns: ActionPattern[] = [];

    // Group consecutive action panels
    const sequences = this.groupConsecutivePanels(actionPanels);

    for (const sequence of sequences) {
      if (sequence.length >= 3) {
        // Minimum sequence length
        patterns.push({
          type: this.determineActionType(sequence),
          setup: this.createActionSetup(sequence),
          climax: this.createActionClimax(sequence),
          resolution: this.createActionResolution(sequence),
          rpgMechanics: this.suggestRPGMechanics(sequence),
        });
      }
    }

    return patterns;
  }

  // Group consecutive action panels
  private groupConsecutivePanels(panels: ComicPanel[]): ComicPanel[][] {
    const sequences: ComicPanel[][] = [];
    let currentSequence: ComicPanel[] = [];

    for (const panel of panels) {
      if (
        currentSequence.length === 0 ||
        this.isConsecutive(currentSequence[currentSequence.length - 1], panel)
      ) {
        currentSequence.push(panel);
      } else {
        if (currentSequence.length > 0) {
          sequences.push([...currentSequence]);
        }
        currentSequence = [panel];
      }
    }

    if (currentSequence.length > 0) {
      sequences.push(currentSequence);
    }

    return sequences;
  }

  // Check if panels are consecutive
  private isConsecutive(panel1: ComicPanel, panel2: ComicPanel): boolean {
    // Simple heuristic: same setting or similar mood
    return panel1.setting === panel2.setting || panel1.mood === panel2.mood;
  }

  // Determine action type
  private determineActionType(sequence: ComicPanel[]): ActionPattern["type"] {
    const texts = sequence
      .flatMap((p) => p.text)
      .join(" ")
      .toLowerCase();

    if (
      texts.includes("fight") ||
      texts.includes("battle") ||
      texts.includes("attack")
    ) {
      return "combat";
    } else if (
      texts.includes("run") ||
      texts.includes("chase") ||
      texts.includes("escape")
    ) {
      return "chase";
    } else if (
      texts.includes("hide") ||
      texts.includes("sneak") ||
      texts.includes("stealth")
    ) {
      return "stealth";
    } else if (
      texts.includes("talk") ||
      texts.includes("negotiate") ||
      texts.includes("persuade")
    ) {
      return "social";
    } else {
      return "exploration";
    }
  }

  // Create action setup
  private createActionSetup(sequence: ComicPanel[]): string {
    const firstPanel = sequence[0];
    return `The scene begins in ${firstPanel.setting} with a ${
      firstPanel.mood
    } atmosphere. ${
      firstPanel.text[0] || "Tension builds as the action is about to begin."
    }`;
  }

  // Create action climax
  private createActionClimax(sequence: ComicPanel[]): string {
    const middlePanel = sequence[Math.floor(sequence.length / 2)];
    return `The action reaches its peak as ${
      middlePanel.text[0] || "the conflict intensifies."
    }`;
  }

  // Create action resolution
  private createActionResolution(sequence: ComicPanel[]): string {
    const lastPanel = sequence[sequence.length - 1];
    return `The sequence concludes with ${
      lastPanel.text[0] || "the resolution of the conflict."
    }`;
  }

  // Suggest RPG mechanics
  private suggestRPGMechanics(sequence: ComicPanel[]): string[] {
    const actionType = this.determineActionType(sequence);

    const mechanics: { [key: string]: string[] } = {
      combat: [
        "Initiative rolls",
        "Attack rolls",
        "Damage calculation",
        "Combat positioning",
      ],
      chase: [
        "Athletics checks",
        "Acrobatics checks",
        "Stealth vs Perception",
        "Chase mechanics",
      ],
      stealth: [
        "Stealth checks",
        "Perception checks",
        "Sneak attack mechanics",
        "Cover system",
      ],
      social: [
        "Persuasion checks",
        "Intimidation checks",
        "Insight checks",
        "Social encounter rules",
      ],
      exploration: [
        "Investigation checks",
        "Survival checks",
        "Perception checks",
        "Exploration mechanics",
      ],
    };

    return mechanics[actionType] || ["General skill checks"];
  }

  // Update knowledge base with new patterns
  private updateKnowledgeBase(patterns: LearnedPatterns): void {
    // Add story patterns
    this.knowledgeBase.storyPatterns.push(...patterns.storyFlow);

    // Add character archetypes
    this.knowledgeBase.characterArchetypes.push(...patterns.characters);

    // Add dialogue styles
    this.knowledgeBase.dialogueStyles.push(...patterns.dialogue);

    // Add plot structures
    this.knowledgeBase.plotStructures.push(
      ...patterns.storyFlow.map((p) => ({
        type: p.type as any,
        description: p.description,
        characters: [],
        location: "",
      }))
    );

    // Add conflict types
    const newConflicts = patterns.actionSequences.map((a) => a.type);
    this.knowledgeBase.conflictTypes.push(...newConflicts);

    // Add setting descriptions
    const newSettings = patterns.storyFlow.map((s) => s.description);
    this.knowledgeBase.settingDescriptions.push(...newSettings);
  }

  // Initialize knowledge base with default patterns
  private initializeKnowledgeBase(): void {
    // Add some default RPG knowledge
    this.knowledgeBase.storyPatterns = [
      {
        type: "setup",
        rpgEquivalent: "Session Opening",
        effectiveness: 0.8,
        usage: "opening",
        description: "Introduce the quest and setting",
      },
    ];

    this.knowledgeBase.characterArchetypes = [
      {
        name: "Default Quest Giver",
        role: "quest_giver",
        personality: ["wise", "knowledgeable"],
        typicalDialogue: ["Greetings, adventurer", "I have a quest for you"],
        visualDescription: "A wise old figure",
        rpgStats: {
          charisma: 16,
          wisdom: 14,
          level: 5,
          class: "Noble",
        },
      },
    ];
  }

  // Utility methods
  private calculateVariance(numbers: number[]): number {
    const mean = numbers.reduce((a, b) => a + b, 0) / numbers.length;
    const squaredDiffs = numbers.map((n) => Math.pow(n - mean, 2));
    return squaredDiffs.reduce((a, b) => a + b, 0) / numbers.length;
  }

  private getMostCommon<T>(array: T[]): T | null {
    const counts = new Map<T, number>();
    let maxCount = 0;
    let mostCommon: T | null = null;

    for (const item of array) {
      const count = (counts.get(item) || 0) + 1;
      counts.set(item, count);

      if (count > maxCount) {
        maxCount = count;
        mostCommon = item;
      }
    }

    return mostCommon;
  }
}
