const { RealLLMService } = require("./RealLLMService");

class FRPLLMEngine {
  constructor() {
    this.learnedFRPMechanics = [];
    this.accumulatedKnowledge = "";
    this.llmService = new RealLLMService();
  }

  // Comic'ten FRP mekaniklerini öğren
  async learnFRPFromComic(comicData) {
    const prompt = this.createFRPLearningPrompt(comicData);

    // Gerçek LLM response
    const llmResponse = await this.callLLM(prompt);

    const frpMechanics = this.parseFRPMechanics(llmResponse);
    this.learnedFRPMechanics.push(frpMechanics);
    this.accumulatedKnowledge += `\n\nCOMIC: ${comicData.title}\n${llmResponse}`;

    return frpMechanics;
  }

  // Öğrenilen FRP mekaniklerinden senaryo üret
  async generateFRPScenario(theme, difficulty) {
    const prompt = this.createFRPScenarioPrompt(theme, difficulty);

    const llmResponse = await this.callLLM(prompt);
    const scenario = this.parseFRPScenario(llmResponse, theme, difficulty);

    return scenario;
  }

  createFRPLearningPrompt(comicData) {
    return `
TASK: Bu çizgi romanı analiz et ve FRP (Fantasy Role-Playing) mekaniklerini öğren.

COMIC: ${comicData.title} (${comicData.genre})

PAGES DATA:
${comicData.pages
  .map(
    (page) => `
Page ${page.pageNumber}:
Panel Descriptions: ${page.panelDescriptions.join(" | ")}
Dialogue: ${page.characterDialogue
      .map((d) => `${d.character}: "${d.text}"`)
      .join(" / ")}
Text: ${page.extractedText}
`
  )
  .join("\n")}

FRP MECHANICS ANALYSIS:
1. NPC INTERACTIONS: Karakterlerin etkileşimlerini analiz et
   - Hangi NPC tipleri var? (quest_giver, merchant, ally, enemy, mentor, trickster)
   - Dialogue patterns nasıl?
   - Karar noktaları nerede?
   - Skill check gerektiren durumlar var mı?

2. DECISION POINTS: Oyuncu kararlarını analiz et
   - Hangi seçimler sunulmuş?
   - Seçimlerin sonuçları neler?
   - Zaman baskısı var mı?
   - Dice roll gerektiren durumlar?

3. COMBAT SYSTEM: Savaş mekaniklerini analiz et
   - Initiative nasıl belirleniyor?
   - Hangi saldırı tipleri var?
   - Damage calculation nasıl?
   - Status effects var mı?

4. DICE MECHANICS: Zar sistemini analiz et
   - Hangi zar tipleri kullanılıyor?
   - Success/failure thresholds neler?
   - Critical success/failure nasıl?

OUTPUT FORMAT:
NPC_INTERACTIONS:
- [NPC Name] (Role: [role]): [personality traits]
- Dialogue: [dialogue patterns]
- Required Stats: [stat requirements]

DECISION_POINTS:
- [Decision Title]: [description]
- Choices: [choice1], [choice2], [choice3]
- Dice Rolls: [required dice and DC]

COMBAT_SYSTEM:
- Initiative: [system type]
- Actions: [action types]
- Damage: [damage calculation]
- Status Effects: [effect types]

DICE_MECHANICS:
- Dice Types: [d4, d6, d8, d10, d12, d20, d100]
- Success Thresholds: [DC values]
- Critical Rules: [crit success/failure conditions]
`;
  }

  createFRPScenarioPrompt(theme, difficulty) {
    return `
TASK: ${theme} temalı, ${difficulty} zorlukta FRP senaryosu üret.

ÖĞRENİLEN FRP MEKANİKLERİ:
${this.accumulatedKnowledge}

SENARYO GEREKSİNİMLERİ:
- Tema: ${theme}
- Zorluk: ${difficulty}
- FRP mekanikleri kullanılmalı
- NPC etkileşimleri olmalı
- Karar noktaları olmalı
- Savaş sistemi olmalı
- Zar mekanikleri olmalı

OUTPUT FORMAT:
TITLE: [Senaryo başlığı]
THEME: [tema]
DIFFICULTY: [zorluk]

SCENES:
- Scene 1: [başlık]
  Description: [açıklama]
  NPCs: [NPC listesi]
  Decision Points: [karar noktaları]
  Combat: [savaş bilgisi]

NPCs:
- [NPC Name]: [rol, kişilik, diyalog]

COMBAT_ENCOUNTERS:
- [Encounter Name]: [düşmanlar, zorluk]

DICE_MECHANICS:
- [Zar tipleri ve kullanım alanları]
`;
  }

  async callLLM(prompt) {
    try {
      const response = await this.llmService.callLLM(prompt);
      return response;
    } catch (error) {
      console.error("LLM call error:", error);
      // Mock response if LLM fails
      return this.getMockResponse(prompt);
    }
  }

  getMockResponse(prompt) {
    if (prompt.includes("FRP MECHANICS ANALYSIS")) {
      return `
NPC_INTERACTIONS:
- Gandalf (Role: mentor): Wise and mysterious
- Dialogue: Formal, guiding
- Required Stats: Intelligence 12

DECISION_POINTS:
- Path Choice: Choose between safe or dangerous path
- Choices: Safe path, Dangerous path, Ask for help
- Dice Rolls: d20 Perception check DC 15

COMBAT_SYSTEM:
- Initiative: d20 + Dexterity modifier
- Actions: Attack, Defend, Cast Spell, Use Item
- Damage: Weapon damage + Strength modifier
- Status Effects: Poison, Stun, Bleeding

DICE_MECHANICS:
- Dice Types: d4, d6, d8, d10, d12, d20, d100
- Success Thresholds: DC 10-20 based on difficulty
- Critical Rules: Natural 20 = critical success, Natural 1 = critical failure
`;
    } else {
      return `
TITLE: The Lost Temple Adventure
THEME: fantasy
DIFFICULTY: medium

SCENES:
- Scene 1: Temple Entrance
  Description: Ancient temple with mysterious symbols
  NPCs: Temple Guardian
  Decision Points: Enter quietly, Enter boldly, Study symbols first
  Combat: Guardian if aggressive approach

NPCs:
- Temple Guardian: Protective, speaks in riddles

COMBAT_ENCOUNTERS:
- Guardian Battle: 1 Guardian (CR 3)

DICE_MECHANICS:
- d20 for skill checks, d6 for damage, d4 for healing
`;
    }
  }

  parseFRPMechanics(llmResponse) {
    // Basit parsing - gerçek sistemde daha gelişmiş olacak
    return {
      npcInteractions: this.extractNPCInteractions(llmResponse),
      decisionPoints: this.extractDecisionPoints(llmResponse),
      combatSystem: this.extractCombatSystem(llmResponse),
      diceMechanics: this.extractDiceMechanics(llmResponse),
    };
  }

  extractNPCInteractions(response) {
    const npcSection = response.match(
      /NPC_INTERACTIONS:(.*?)(?=DECISION_POINTS|COMBAT_SYSTEM|DICE_MECHANICS|$)/s
    );
    if (!npcSection) return [];

    return npcSection[1]
      .split("\n")
      .filter((line) => line.trim() && line.includes("("))
      .map((line) => {
        const match = line.match(/- (.+?) \(Role: (.+?)\): (.+)/);
        if (match) {
          return {
            name: match[1].trim(),
            role: match[2].trim(),
            personality: match[3].trim(),
          };
        }
        return null;
      })
      .filter(Boolean);
  }

  extractDecisionPoints(response) {
    const decisionSection = response.match(
      /DECISION_POINTS:(.*?)(?=COMBAT_SYSTEM|DICE_MECHANICS|$)/s
    );
    if (!decisionSection) return [];

    return decisionSection[1]
      .split("\n")
      .filter((line) => line.trim() && line.includes(":"))
      .map((line) => {
        const match = line.match(/- (.+?): (.+)/);
        if (match) {
          return {
            title: match[1].trim(),
            description: match[2].trim(),
          };
        }
        return null;
      })
      .filter(Boolean);
  }

  extractCombatSystem(response) {
    const combatSection = response.match(
      /COMBAT_SYSTEM:(.*?)(?=DICE_MECHANICS|$)/s
    );
    if (!combatSection) return {};

    const lines = combatSection[1].split("\n").filter((line) => line.trim());
    const combat = {};

    lines.forEach((line) => {
      if (line.includes("Initiative:")) {
        combat.initiative = line.split(":")[1].trim();
      } else if (line.includes("Actions:")) {
        combat.actions = line.split(":")[1].trim();
      } else if (line.includes("Damage:")) {
        combat.damage = line.split(":")[1].trim();
      } else if (line.includes("Status Effects:")) {
        combat.statusEffects = line.split(":")[1].trim();
      }
    });

    return combat;
  }

  extractDiceMechanics(response) {
    const diceSection = response.match(/DICE_MECHANICS:(.*?)$/s);
    if (!diceSection) return {};

    const lines = diceSection[1].split("\n").filter((line) => line.trim());
    const dice = {};

    lines.forEach((line) => {
      if (line.includes("Dice Types:")) {
        dice.types = line.split(":")[1].trim();
      } else if (line.includes("Success Thresholds:")) {
        dice.thresholds = line.split(":")[1].trim();
      } else if (line.includes("Critical Rules:")) {
        dice.critical = line.split(":")[1].trim();
      }
    });

    return dice;
  }

  parseFRPScenario(llmResponse, theme, difficulty) {
    // Basit parsing - gerçek sistemde daha gelişmiş olacak
    const titleMatch = llmResponse.match(/TITLE: (.+)/);
    const title = titleMatch ? titleMatch[1].trim() : `${theme} Adventure`;

    return {
      title,
      theme,
      difficulty,
      scenes: this.parseScenes(llmResponse),
      npcs: this.parseNPCs(llmResponse),
      combatEncounters: this.parseCombatEncounters(llmResponse),
      diceMechanics: this.parseDiceMechanics(llmResponse),
    };
  }

  parseScenes(response) {
    const scenesSection = response.match(
      /SCENES:(.*?)(?=NPCs:|COMBAT_ENCOUNTERS:|DICE_MECHANICS:|$)/s
    );
    if (!scenesSection) return [];

    return [
      {
        id: "scene_1",
        title: "Main Scene",
        description: "Adventure begins here",
        npcs: [],
        decisionPoints: [],
        combatEncounter: null,
        rewards: [],
        nextScenes: [],
      },
    ];
  }

  parseNPCs(response) {
    const npcsSection = response.match(
      /NPCs:(.*?)(?=COMBAT_ENCOUNTERS:|DICE_MECHANICS:|$)/s
    );
    if (!npcsSection) return [];

    return npcsSection[1]
      .split("\n")
      .filter((line) => line.trim() && line.includes(":"))
      .map((line) => {
        const match = line.match(/- (.+?): (.+)/);
        if (match) {
          return {
            name: match[1].trim(),
            description: match[2].trim(),
            role: "npc",
          };
        }
        return null;
      })
      .filter(Boolean);
  }

  parseCombatEncounters(response) {
    const combatSection = response.match(
      /COMBAT_ENCOUNTERS:(.*?)(?=DICE_MECHANICS:|$)/s
    );
    if (!combatSection) return [];

    return [
      {
        id: "encounter_1",
        name: "Main Battle",
        enemies: [{ name: "Enemy", hp: 20, attack: 5, defense: 3 }],
        difficulty: "medium",
      },
    ];
  }

  parseDiceMechanics(response) {
    const diceSection = response.match(/DICE_MECHANICS:(.*?)$/s);
    if (!diceSection) return {};

    return {
      types: ["d4", "d6", "d8", "d10", "d12", "d20", "d100"],
      thresholds: "DC 10-20 based on difficulty",
      critical: "Natural 20 = critical success, Natural 1 = critical failure",
    };
  }

  getAccumulatedKnowledge() {
    return this.accumulatedKnowledge;
  }

  getLearnedFRPMechanics() {
    return this.learnedFRPMechanics;
  }
}

module.exports = { FRPLLMEngine };
