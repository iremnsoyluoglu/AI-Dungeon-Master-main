import {
  LearnedPatterns,
  RPGScenario,
  RPGGameScene,
  CharacterArchetype,
  StoryPattern,
  DialoguePattern,
  MoodPattern,
  ActionPattern,
  ScenarioKnowledge,
} from "../types/comic";

export class LearnedScenarioGenerator {
  constructor(private knowledgeBase: ScenarioKnowledge) {}

  generateRPGScenario(
    theme: string,
    difficulty: "easy" | "medium" | "hard"
  ): RPGScenario {
    console.log(`Generating ${difficulty} RPG scenario with theme: ${theme}`);

    // Select relevant patterns based on theme
    const relevantPatterns = this.selectRelevantPatterns(theme);

    // Build scenario from patterns
    const scenario = this.buildScenario(relevantPatterns, difficulty);

    return scenario;
  }

  private selectRelevantPatterns(theme: string): {
    storyPatterns: StoryPattern[];
    characters: CharacterArchetype[];
    dialogue: DialoguePattern[];
    moods: MoodPattern[];
    actions: ActionPattern[];
  } {
    // Filter patterns based on theme
    const storyPatterns = this.knowledgeBase.storyPatterns.filter(
      (pattern) =>
        pattern.description.toLowerCase().includes(theme.toLowerCase()) ||
        pattern.rpgEquivalent.toLowerCase().includes(theme.toLowerCase())
    );

    const characters = this.knowledgeBase.characterArchetypes.filter(
      (char) =>
        char.personality.some((trait) =>
          trait.toLowerCase().includes(theme.toLowerCase())
        ) || char.role === "quest_giver" // Always include quest givers
    );

    const dialogue = this.knowledgeBase.dialogueStyles.filter(
      (dialogue) =>
        dialogue.context.toLowerCase().includes(theme.toLowerCase()) ||
        dialogue.type === "information" // Always include information dialogue
    );

    const moods = this.knowledgeBase.plotStructures
      .filter((structure) =>
        structure.description.toLowerCase().includes(theme.toLowerCase())
      )
      .map(() => this.knowledgeBase.dialogueStyles[0]) // Placeholder for mood patterns
      .filter(Boolean);

    const actions = this.knowledgeBase.conflictTypes
      .filter((conflict) =>
        conflict.toLowerCase().includes(theme.toLowerCase())
      )
      .map((type) => ({
        type: type as any,
        setup: `Setup for ${type} encounter`,
        climax: `Climax of ${type} encounter`,
        resolution: `Resolution of ${type} encounter`,
        rpgMechanics: [`${type} mechanics`],
      }));

    return {
      storyPatterns:
        storyPatterns.length > 0
          ? storyPatterns
          : this.knowledgeBase.storyPatterns,
      characters:
        characters.length > 0
          ? characters
          : this.knowledgeBase.characterArchetypes,
      dialogue:
        dialogue.length > 0 ? dialogue : this.knowledgeBase.dialogueStyles,
      moods: moods.length > 0 ? moods : [],
      actions: actions.length > 0 ? actions : [],
    };
  }

  private buildScenario(
    patterns: any,
    difficulty: "easy" | "medium" | "hard"
  ): RPGScenario {
    const title = this.generateTitle(patterns);
    const setting = this.createSetting(patterns);
    const scenes = this.createScenes(patterns, difficulty);
    const npcs = this.createNPCs(patterns);
    const conflicts = this.createConflicts(patterns);
    const boss = this.createBoss(patterns, difficulty);

    return {
      title,
      setting,
      scenes,
      npcs,
      conflicts,
      boss,
      difficulty,
      estimatedDuration: this.estimateDuration(scenes, difficulty),
    };
  }

  private generateTitle(patterns: any): string {
    const themes = [
      "Ancient",
      "Dark",
      "Mysterious",
      "Forgotten",
      "Hidden",
      "Lost",
    ];
    const locations = [
      "Temple",
      "Dungeon",
      "Castle",
      "Forest",
      "Cavern",
      "Tower",
    ];
    const threats = ["Curse", "Monster", "Trap", "Secret", "Treasure", "Power"];

    const theme = themes[Math.floor(Math.random() * themes.length)];
    const location = locations[Math.floor(Math.random() * locations.length)];
    const threat = threats[Math.floor(Math.random() * threats.length)];

    return `${theme} ${location} of the ${threat}`;
  }

  private createSetting(patterns: any): string {
    const settings = [
      "A crumbling ancient temple hidden deep in the mountains",
      "A dark dungeon beneath an abandoned castle",
      "A mysterious forest where shadows whisper ancient secrets",
      "A forgotten city buried beneath the sands of time",
      "A haunted mansion on the edge of a cursed village",
      "An underground cavern system filled with strange creatures",
      "A floating island in the sky, home to ancient magic",
      "A cyberpunk city where technology and magic collide",
    ];

    return settings[Math.floor(Math.random() * settings.length)];
  }

  private createScenes(
    patterns: any,
    difficulty: "easy" | "medium" | "hard"
  ): RPGGameScene[] {
    const scenes: RPGGameScene[] = [];

    // Determine number of scenes based on difficulty
    const sceneCount =
      difficulty === "easy" ? 3 : difficulty === "medium" ? 5 : 7;

    // Create opening scene
    scenes.push(this.createOpeningScene(patterns));

    // Create middle scenes
    for (let i = 1; i < sceneCount - 1; i++) {
      scenes.push(this.createMiddleScene(patterns, i));
    }

    // Create climax scene
    scenes.push(this.createClimaxScene(patterns, difficulty));

    return scenes;
  }

  private createOpeningScene(patterns: any): RPGGameScene {
    const openingPatterns = patterns.storyPatterns.filter(
      (p: StoryPattern) => p.usage === "opening"
    );
    const pattern =
      openingPatterns.length > 0
        ? openingPatterns[0]
        : patterns.storyPatterns[0];

    return {
      title: "The Call to Adventure",
      description:
        pattern.description ||
        "The party receives a mysterious quest that leads them to an ancient location.",
      location: "Town Square or Tavern",
      characters: ["Quest Giver", "Local Merchant", "Town Guard"],
      choices: [
        "Accept the quest immediately",
        "Ask for more information about the dangers",
        "Negotiate for better rewards",
        "Refuse and seek other opportunities",
      ],
      consequences: [
        "Begin the adventure with enthusiasm",
        "Gain valuable information about the quest",
        "Receive better equipment or gold",
        "Find an alternative quest with different challenges",
      ],
      rpgMechanics: [
        "Social interaction",
        "Quest acceptance",
        "Information gathering",
      ],
    };
  }

  private createMiddleScene(patterns: any, sceneIndex: number): RPGGameScene {
    const middlePatterns = patterns.storyPatterns.filter(
      (p: StoryPattern) => p.usage === "middle"
    );
    const pattern =
      middlePatterns.length > 0
        ? middlePatterns[sceneIndex % middlePatterns.length]
        : patterns.storyPatterns[0];

    const sceneTypes = [
      {
        title: "The First Challenge",
        description:
          "The party encounters their first obstacle in the adventure.",
        choices: [
          "Fight through the challenge",
          "Find a way around",
          "Use diplomacy",
          "Use stealth",
        ],
      },
      {
        title: "A Mysterious Discovery",
        description:
          "The party finds something unexpected that changes their understanding of the quest.",
        choices: [
          "Investigate further",
          "Continue with the original plan",
          "Share the discovery",
          "Keep it secret",
        ],
      },
      {
        title: "An Ally in Need",
        description: "The party meets someone who needs their help.",
        choices: [
          "Help immediately",
          "Ask for payment",
          "Refuse to help",
          "Offer conditional aid",
        ],
      },
    ];

    const sceneType = sceneTypes[sceneIndex % sceneTypes.length];

    return {
      title: sceneType.title,
      description: pattern.description || sceneType.description,
      location: this.generateLocation(),
      characters: this.generateCharacters(2, 4),
      choices: sceneType.choices,
      consequences: [
        "Gain experience and loot",
        "Find a shortcut or advantage",
        "Make a new ally",
        "Avoid unnecessary conflict",
      ],
      rpgMechanics: [
        "Combat",
        "Skill checks",
        "Social interaction",
        "Exploration",
      ],
    };
  }

  private createClimaxScene(
    patterns: any,
    difficulty: "easy" | "medium" | "hard"
  ): RPGGameScene {
    const climaxPatterns = patterns.storyPatterns.filter(
      (p: StoryPattern) => p.usage === "climax"
    );
    const pattern =
      climaxPatterns.length > 0 ? climaxPatterns[0] : patterns.storyPatterns[0];

    const difficultyModifiers = {
      easy: {
        title: "The Final Challenge",
        description:
          "A manageable final obstacle stands between the party and their goal.",
        choices: [
          "Direct confrontation",
          "Clever strategy",
          "Negotiation",
          "Quick escape",
        ],
      },
      medium: {
        title: "The Ultimate Test",
        description:
          "A formidable challenge that will test all the party's skills and teamwork.",
        choices: [
          "Coordinated attack",
          "Divide and conquer",
          "Strategic retreat",
          "Call for reinforcements",
        ],
      },
      hard: {
        title: "The Impossible Choice",
        description:
          "An overwhelming challenge that requires sacrifice and clever thinking to overcome.",
        choices: [
          "Sacrifice for victory",
          "Find the hidden weakness",
          "Use forbidden magic",
          "Make a deal with the enemy",
        ],
      },
    };

    const modifier = difficultyModifiers[difficulty];

    return {
      title: modifier.title,
      description: pattern.description || modifier.description,
      location: "The Heart of the Dungeon",
      characters: ["Final Boss", "Minions", "Prisoners"],
      choices: modifier.choices,
      consequences: [
        "Victory with great rewards",
        "Victory with consequences",
        "Partial success",
        "Defeat with escape opportunity",
      ],
      rpgMechanics: [
        "Boss combat",
        "Environmental hazards",
        "Multiple objectives",
        "Time pressure",
      ],
    };
  }

  private createNPCs(patterns: any): CharacterArchetype[] {
    const npcs: CharacterArchetype[] = [];

    // Always include a quest giver
    const questGivers = patterns.characters.filter(
      (c: CharacterArchetype) => c.role === "quest_giver"
    );
    if (questGivers.length > 0) {
      npcs.push(questGivers[0]);
    }

    // Add 2-4 additional NPCs
    const otherNPCs = patterns.characters.filter(
      (c: CharacterArchetype) => c.role !== "quest_giver"
    );
    const selectedNPCs = otherNPCs.slice(0, Math.min(4, otherNPCs.length));
    npcs.push(...selectedNPCs);

    return npcs;
  }

  private createConflicts(patterns: any): string[] {
    const conflicts: string[] = [];

    // Add conflicts based on action patterns
    patterns.actions.forEach((action: ActionPattern) => {
      conflicts.push(`${action.type} encounter`);
    });

    // Add generic conflicts if needed
    if (conflicts.length < 3) {
      const genericConflicts = [
        "Environmental hazards",
        "Puzzle challenges",
        "Social conflicts",
        "Resource management",
        "Time pressure",
      ];

      conflicts.push(...genericConflicts.slice(0, 3 - conflicts.length));
    }

    return conflicts;
  }

  private createBoss(
    patterns: any,
    difficulty: "easy" | "medium" | "hard"
  ): CharacterArchetype | undefined {
    const enemies = patterns.characters.filter(
      (c: CharacterArchetype) => c.role === "enemy"
    );

    if (enemies.length > 0) {
      const boss = { ...enemies[0] };

      // Scale boss stats based on difficulty
      const difficultyMultiplier =
        difficulty === "easy" ? 1.2 : difficulty === "medium" ? 1.5 : 2.0;

      if (boss.rpgStats) {
        Object.keys(boss.rpgStats).forEach((stat) => {
          if (typeof boss.rpgStats[stat] === "number") {
            boss.rpgStats[stat] = Math.floor(
              boss.rpgStats[stat] * difficultyMultiplier
            );
          }
        });
        boss.rpgStats.level = Math.floor(
          (boss.rpgStats.level || 1) * difficultyMultiplier
        );
      }

      return boss;
    }

    return undefined;
  }

  private estimateDuration(
    scenes: RPGGameScene[],
    difficulty: "easy" | "medium" | "hard"
  ): string {
    const baseTime = scenes.length * 30; // 30 minutes per scene
    const difficultyMultiplier =
      difficulty === "easy" ? 0.8 : difficulty === "medium" ? 1.0 : 1.3;
    const totalMinutes = Math.floor(baseTime * difficultyMultiplier);

    const hours = Math.floor(totalMinutes / 60);
    const minutes = totalMinutes % 60;

    if (hours > 0) {
      return `${hours} hour${hours > 1 ? "s" : ""} ${
        minutes > 0 ? `and ${minutes} minutes` : ""
      }`;
    } else {
      return `${minutes} minutes`;
    }
  }

  private generateLocation(): string {
    const locations = [
      "Ancient Temple Chamber",
      "Dark Dungeon Corridor",
      "Mysterious Forest Clearing",
      "Abandoned Castle Room",
      "Underground Cavern",
      "Haunted Mansion Hall",
      "Floating Island Platform",
      "Cyberpunk City Street",
    ];

    return locations[Math.floor(Math.random() * locations.length)];
  }

  private generateCharacters(min: number, max: number): string[] {
    const characterTypes = [
      "Guard",
      "Merchant",
      "Wizard",
      "Warrior",
      "Rogue",
      "Priest",
      "Noble",
      "Peasant",
      "Monster",
      "Spirit",
      "Construct",
      "Beast",
    ];

    const count = Math.floor(Math.random() * (max - min + 1)) + min;
    const characters: string[] = [];

    for (let i = 0; i < count; i++) {
      const type =
        characterTypes[Math.floor(Math.random() * characterTypes.length)];
      characters.push(`${type} ${i + 1}`);
    }

    return characters;
  }

  // Generate multiple scenarios for variety
  generateMultipleScenarios(theme: string, count: number = 3): RPGScenario[] {
    const scenarios: RPGScenario[] = [];
    const difficulties: ("easy" | "medium" | "hard")[] = [
      "easy",
      "medium",
      "hard",
    ];

    for (let i = 0; i < count; i++) {
      const difficulty = difficulties[i % difficulties.length];
      scenarios.push(this.generateRPGScenario(theme, difficulty));
    }

    return scenarios;
  }

  // Generate scenario based on specific comic patterns
  generateScenarioFromComic(
    learnedPatterns: LearnedPatterns,
    theme: string
  ): RPGScenario {
    // Temporarily update knowledge base with comic-specific patterns
    const originalKnowledge = { ...this.knowledgeBase };

    // Add comic patterns to knowledge base
    this.knowledgeBase.storyPatterns.push(...learnedPatterns.storyFlow);
    this.knowledgeBase.characterArchetypes.push(...learnedPatterns.characters);
    this.knowledgeBase.dialogueStyles.push(...learnedPatterns.dialogue);

    // Generate scenario
    const scenario = this.generateRPGScenario(theme, "medium");

    // Restore original knowledge base
    this.knowledgeBase = originalKnowledge;

    return scenario;
  }
}
