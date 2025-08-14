import { ComicData, LearningResponse } from "../types/llmComic";
import {
  FRPRPGScenario,
  FRPMechanics,
  NPCInteraction,
  DecisionPoint,
  CombatSystem,
  DiceMechanics,
} from "../types/frpMechanics";

export class FRPLLMEngine {
  private learnedFRPMechanics: FRPMechanics[] = [];
  private accumulatedKnowledge: string = "";

  // Comic'ten FRP mekaniklerini öğren
  async learnFRPFromComic(comicData: ComicData): Promise<FRPMechanics> {
    const prompt = this.createFRPLearningPrompt(comicData);

    // Mock LLM response - gerçek sistemde LLM API'ye gönderilecek
    const llmResponse = await this.callLLM(prompt);

    const frpMechanics = this.parseFRPMechanics(llmResponse);
    this.learnedFRPMechanics.push(frpMechanics);
    this.accumulatedKnowledge += `\n\nCOMIC: ${comicData.title}\n${llmResponse}`;

    return frpMechanics;
  }

  // Öğrenilen FRP mekaniklerinden senaryo üret
  async generateFRPScenario(
    theme: string,
    difficulty: string
  ): Promise<FRPRPGScenario> {
    const prompt = this.createFRPScenarioPrompt(theme, difficulty);

    const llmResponse = await this.callLLM(prompt);
    const scenario = this.parseFRPScenario(llmResponse, theme, difficulty);

    return scenario;
  }

  private createFRPLearningPrompt(comicData: ComicData): string {
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

DICE_MECHANICS:
- Standard Dice: [dice types used]
- Success DC: [difficulty classes]
- Critical: [critical rules]
`;
  }

  private createFRPScenarioPrompt(theme: string, difficulty: string): string {
    return `
Sen GetComics'ten onlarca çizgi roman okumuş ve FRP mekaniklerini öğrenmişsin:

LEARNED FRP KNOWLEDGE:
${this.accumulatedKnowledge}

TASK: Bu öğrendiğin FRP mekaniklerini kullanarak tam bir RPG senaryosu yaz.

REQUIREMENTS:
Theme: ${theme}
Difficulty: ${difficulty}

FRP MECHANICS TO INCLUDE:
- NPC Interactions with dialogue options and skill checks
- Decision Points with multiple choices and consequences
- Combat System with initiative, actions, and dice rolls
- Dice Mechanics with proper probability and DCs

OUTPUT FORMAT:
### FRP CAMPAIGN: [Title]
Theme: [theme]
Difficulty: [difficulty]

NPCs:
- [NPC Name] (Role: [role])
  Personality: [traits]
  Dialogue Options:
    - "[dialogue]" (Requires: [skill/stat], DC: [number])
    - "[dialogue]" (Requires: [skill/stat], DC: [number])

Scenes:
Scene 1: [Title]
Description: [description]
NPCs Present: [npc names]
Decision Points:
  - [Decision Title]: [description]
    Choices:
      A) "[choice]" (Requires: [skill/stat], DC: [number])
      B) "[choice]" (Requires: [skill/stat], DC: [number])
      C) "[choice]" (Requires: [skill/stat], DC: [number])

Combat Encounters:
- [Encounter Name]
  Enemies: [enemy list]
  Initiative: [system]
  Actions: [action types]
  Victory: [conditions]
  Defeat: [conditions]

Dice Mechanics:
- Standard: [dice types]
- DCs: [difficulty classes]
- Critical: [rules]

Generate now using your FRP knowledge!
`;
  }

  private async callLLM(prompt: string): Promise<string> {
    // Mock LLM response - gerçek sistemde fetch ile API'ye gönderilecek
    return `
NPC_INTERACTIONS:
- Gandalf (Role: mentor): wise, mysterious, powerful
- Dialogue: formal, cryptic, encouraging
- Required Stats: INT 12, WIS 14

DECISION_POINTS:
- Path Choice: Choose between safe or dangerous route
- Choices: Safe (no risk), Dangerous (high reward, high risk)
- Dice Rolls: Perception DC 15 for safe path, Survival DC 18 for dangerous

COMBAT_SYSTEM:
- Initiative: d20 + DEX modifier
- Actions: Attack (1d20 + STR), Cast Spell (1d20 + INT), Defend (+2 AC)
- Damage: 1d8 + STR modifier

DICE_MECHANICS:
- Standard Dice: d4, d6, d8, d10, d12, d20, d100
- Success DC: 10-20 range
- Critical: Natural 20 = critical success, Natural 1 = critical failure
`;
  }

  private parseFRPMechanics(llmResponse: string): FRPMechanics {
    // Parse LLM response into structured FRP mechanics
    const lines = llmResponse
      .split("\n")
      .map((l) => l.trim())
      .filter(Boolean);

    // Parse NPC Interactions
    const npcInteractions: NPCInteraction[] = [];
    const npcSection = lines.filter(
      (l) => l.startsWith("-") && l.includes("Role:")
    );
    for (const npcLine of npcSection) {
      const match = npcLine.match(/- (.+) \(Role: (.+)\): (.+)/);
      if (match) {
        npcInteractions.push({
          npcName: match[1],
          npcRole: match[2] as any,
          personality: match[3].split(", "),
          dialogueOptions: [],
          consequences: [],
        });
      }
    }

    // Parse Decision Points
    const decisionPoints: DecisionPoint[] = [];
    const decisionSection = lines.filter(
      (l) => l.startsWith("-") && l.includes("Choice")
    );
    for (const decisionLine of decisionSection) {
      const match = decisionLine.match(/- (.+): (.+)/);
      if (match) {
        decisionPoints.push({
          id: `decision_${decisionPoints.length}`,
          title: match[1],
          description: match[2],
          choices: [],
        });
      }
    }

    // Parse Combat System
    const combatSystem: CombatSystem = {
      initiative: { type: "d20", modifiers: {}, order: "descending" },
      actions: [],
      statusEffects: [],
      victoryConditions: [],
      defeatConditions: [],
    };

    // Parse Dice Mechanics
    const diceMechanics: DiceMechanics = {
      standardDice: ["d4", "d6", "d8", "d10", "d12", "d20", "d100"],
      customDice: [],
      probabilityTables: [],
    };

    return {
      npcInteractions,
      decisionPoints,
      combatSystem,
      diceMechanics,
    };
  }

  private parseFRPScenario(
    llmResponse: string,
    theme: string,
    difficulty: string
  ): FRPRPGScenario {
    // Parse LLM response into structured FRP scenario
    return {
      title: `FRP Campaign: ${theme}`,
      theme,
      difficulty,
      scenes: [],
      npcs: [],
      combatEncounters: [],
      diceMechanics: {
        standardDice: ["d4", "d6", "d8", "d10", "d12", "d20", "d100"],
        customDice: [],
        probabilityTables: [],
      },
    };
  }

  // Get accumulated FRP knowledge
  getAccumulatedKnowledge(): string {
    return this.accumulatedKnowledge;
  }

  // Get learned FRP mechanics
  getLearnedFRPMechanics(): FRPMechanics[] {
    return this.learnedFRPMechanics;
  }
}
