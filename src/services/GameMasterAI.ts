import { RealLLMService } from "./RealLLMService";
import { StoredScenario } from "../types/scenarioStorage";

export interface GameState {
  currentScene: number;
  playerHP: number;
  playerInventory: string[];
  playerStats: {
    strength: number;
    dexterity: number;
    intelligence: number;
    charisma: number;
  };
  activeEffects: Array<{
    name: string;
    duration: number;
    effect: string;
  }>;
  gameProgress: {
    completedScenes: number[];
    choices: string[];
    combatWins: number;
    itemsFound: number;
  };
}

export interface GameAction {
  type: "choice" | "combat" | "explore" | "talk" | "use_item";
  description: string;
  diceRoll?: {
    diceType: string;
    targetNumber: number;
    skill?: string;
  };
  consequences: {
    success: string;
    failure: string;
  };
}

export interface GameResponse {
  narrative: string;
  availableActions: GameAction[];
  currentState: GameState;
  isCombat: boolean;
  combatInfo?: {
    enemies: Array<{
      name: string;
      hp: number;
      attack: number;
      defense: number;
    }>;
    initiative: string[];
  };
}

export class GameMasterAI {
  private llmService: RealLLMService;
  private currentScenario: StoredScenario | null = null;
  private gameState: GameState;

  constructor() {
    this.llmService = new RealLLMService({
      provider: (process.env.LLM_PROVIDER as any) || "openai",
      model: process.env.LLM_MODEL || "gpt-4",
      temperature: parseFloat(process.env.LLM_TEMPERATURE || "0.8"),
      maxTokens: parseInt(process.env.LLM_MAX_TOKENS || "2000"),
      apiKey: process.env.OPENAI_API_KEY || "",
    });

    this.gameState = this.initializeGameState();
  }

  private initializeGameState(): GameState {
    return {
      currentScene: 0,
      playerHP: 100,
      playerInventory: [],
      playerStats: {
        strength: 15,
        dexterity: 14,
        intelligence: 12,
        charisma: 10,
      },
      activeEffects: [],
      gameProgress: {
        completedScenes: [],
        choices: [],
        combatWins: 0,
        itemsFound: 0,
      },
    };
  }

  // Oyunu başlat
  async startGame(scenario: StoredScenario): Promise<GameResponse> {
    this.currentScenario = scenario;
    this.gameState = this.initializeGameState();

    const prompt = this.createGameStartPrompt(scenario);
    const response = await this.llmService.callLLM({
      prompt,
      temperature: 0.8,
      maxTokens: 1500,
    });

    return this.parseGameResponse(response.text);
  }

  // Oyuncu aksiyonunu işle
  async processPlayerAction(
    action: string,
    diceResult?: number
  ): Promise<GameResponse> {
    if (!this.currentScenario) {
      throw new Error("No active game session");
    }

    const prompt = this.createActionPrompt(action, diceResult);
    const response = await this.llmService.callLLM({
      prompt,
      temperature: 0.8,
      maxTokens: 1500,
    });

    return this.parseGameResponse(response.text);
  }

  // Combat başlat
  async startCombat(): Promise<GameResponse> {
    if (!this.currentScenario) {
      throw new Error("No active game session");
    }

    const prompt = this.createCombatPrompt();
    const response = await this.llmService.callLLM({
      prompt,
      temperature: 0.8,
      maxTokens: 1500,
    });

    return this.parseGameResponse(response.text);
  }

  // Combat aksiyonu işle
  async processCombatAction(
    action: string,
    target?: string,
    diceResult?: number
  ): Promise<GameResponse> {
    if (!this.currentScenario) {
      throw new Error("No active game session");
    }

    const prompt = this.createCombatActionPrompt(action, target, diceResult);
    const response = await this.llmService.callLLM({
      prompt,
      temperature: 0.8,
      maxTokens: 1500,
    });

    return this.parseGameResponse(response.text);
  }

  private createGameStartPrompt(scenario: StoredScenario): string {
    return `
Sen bir FRP oyununun Game Master'ısın. Oyuncuya senaryoyu anlat ve seçimler sun.

SENARYO: ${scenario.title}
TEMA: ${scenario.theme}
ZORLUK: ${scenario.difficulty}

OYUNCU STATLARI:
- HP: ${this.gameState.playerHP}
- Strength: ${this.gameState.playerStats.strength}
- Dexterity: ${this.gameState.playerStats.dexterity}
- Intelligence: ${this.gameState.playerStats.intelligence}
- Charisma: ${this.gameState.playerStats.charisma}

GÖREVİN:
1. Oyuncuya mevcut durumu anlat
2. 3-4 seçenek sun (keşfet, konuş, savaş, item kullan vb.)
3. Her seçenek için zar atışı gerekip gerekmediğini belirt
4. Oyuncuyu heyecanlandır ve oyuna çek

FORMAT:
NARRATIVE: [Durumu anlat]
ACTIONS: [Seçenekler listesi]
COMBAT: [Savaş var mı? true/false]
`;
  }

  private createActionPrompt(action: string, diceResult?: number): string {
    return `
Sen bir FRP oyununun Game Master'ısın. Oyuncunun aksiyonunu işle.

OYUNCU AKSİYONU: ${action}
ZAR SONUCU: ${diceResult || "Yok"}

MEVCUT DURUM:
- HP: ${this.gameState.playerHP}
- Scene: ${this.gameState.currentScene}
- Inventory: ${this.gameState.playerInventory.join(", ")}

GÖREVİN:
1. Aksiyonun sonucunu anlat
2. HP, inventory veya stat değişikliklerini belirt
3. Yeni seçenekler sun
4. Hikayeyi ilerlet

FORMAT:
NARRATIVE: [Sonucu anlat]
HP_CHANGE: [HP değişikliği]
INVENTORY_CHANGE: [Envanter değişikliği]
ACTIONS: [Yeni seçenekler]
COMBAT: [Savaş var mı? true/false]
`;
  }

  private createCombatPrompt(): string {
    return `
Sen bir FRP oyununun Game Master'ısın. Combat başlat.

MEVCUT DURUM:
- HP: ${this.gameState.playerHP}
- Scene: ${this.gameState.currentScene}

GÖREVİN:
1. Düşmanları tanıt
2. Initiative sırasını belirt
3. Combat seçeneklerini sun (saldır, savun, kaç, item kullan)

FORMAT:
NARRATIVE: [Combat başlangıcı]
ENEMIES: [Düşman listesi]
INITIATIVE: [Sıra]
COMBAT_ACTIONS: [Savaş seçenekleri]
COMBAT: true
`;
  }

  private createCombatActionPrompt(
    action: string,
    target?: string,
    diceResult?: number
  ): string {
    return `
Sen bir FRP oyununun Game Master'ısın. Combat aksiyonunu işle.

AKSİYON: ${action}
HEDEF: ${target || "Yok"}
ZAR SONUCU: ${diceResult || "Yok"}

MEVCUT DURUM:
- HP: ${this.gameState.playerHP}

GÖREVİN:
1. Aksiyonun sonucunu anlat
2. Hasar hesapla
3. Düşman tepkisini belirt
4. Combat devam ediyor mu kontrol et

FORMAT:
NARRATIVE: [Aksiyon sonucu]
DAMAGE_DEALT: [Verilen hasar]
DAMAGE_TAKEN: [Alınan hasar]
ENEMY_RESPONSE: [Düşman tepkisi]
COMBAT_CONTINUES: [true/false]
COMBAT_ACTIONS: [Devam eden seçenekler]
`;
  }

  private parseGameResponse(llmResponse: string): GameResponse {
    // Basit parsing - gerçek uygulamada daha gelişmiş parsing gerekir
    const lines = llmResponse.split("\n");

    let narrative = "";
    let actions: GameAction[] = [];
    let isCombat = false;
    let combatInfo = undefined;

    for (const line of lines) {
      if (line.startsWith("NARRATIVE:")) {
        narrative = line.replace("NARRATIVE:", "").trim();
      } else if (
        line.startsWith("ACTIONS:") ||
        line.startsWith("COMBAT_ACTIONS:")
      ) {
        // Actions parsing
        actions = this.parseActions(line);
      } else if (line.startsWith("COMBAT:")) {
        isCombat = line.includes("true");
      }
    }

    return {
      narrative: narrative || "Game Master is thinking...",
      availableActions: actions,
      currentState: this.gameState,
      isCombat,
      combatInfo,
    };
  }

  private parseActions(actionLine: string): GameAction[] {
    // Basit action parsing
    const actions: GameAction[] = [];
    const actionText = actionLine.replace(/ACTIONS?:\s*/, "");

    // Örnek actions
    actions.push({
      type: "explore",
      description: "Çevreyi keşfet",
      diceRoll: { diceType: "d20", targetNumber: 15, skill: "perception" },
      consequences: {
        success: "Gizli bir geçit buldun!",
        failure: "Hiçbir şey bulamadın.",
      },
    });

    actions.push({
      type: "talk",
      description: "NPC ile konuş",
      diceRoll: { diceType: "d20", targetNumber: 12, skill: "charisma" },
      consequences: {
        success: "NPC seninle işbirliği yapmaya karar verdi.",
        failure: "NPC seni reddetti.",
      },
    });

    return actions;
  }

  // Oyun durumunu güncelle
  updateGameState(updates: Partial<GameState>) {
    this.gameState = { ...this.gameState, ...updates };
  }

  // Mevcut oyun durumunu al
  getCurrentGameState(): GameState {
    return this.gameState;
  }

  // Oyunu kaydet
  saveGame(): any {
    return {
      scenario: this.currentScenario,
      gameState: this.gameState,
      timestamp: new Date(),
    };
  }

  // Oyunu yükle
  loadGame(savedGame: any) {
    this.currentScenario = savedGame.scenario;
    this.gameState = savedGame.gameState;
  }
}
