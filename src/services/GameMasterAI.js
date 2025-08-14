const { RealLLMService } = require("./RealLLMService");

class GameMasterAI {
  constructor() {
    this.llmService = new RealLLMService();
    this.currentGameState = null;
    this.currentScenario = null;
    this.playerCharacter = null;
  }

  // Oyunu başlat
  async startGame(scenario) {
    this.currentScenario = scenario;
    this.currentGameState = {
      currentScene: 0,
      playerHP: 100,
      playerInventory: ["Elma", "İksir"],
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

    try {
      const prompt = this.createGameStartPrompt(scenario);
      const llmResponse = await this.llmService.callLLM(prompt);
      return this.parseGameResponse(llmResponse);
    } catch (error) {
      console.error("Game Master AI error:", error);
      return this.getMockGameStartResponse(scenario);
    }
  }

  // Oyuncu aksiyonunu işle
  async processPlayerAction(action, diceResult) {
    try {
      const prompt = this.createActionPrompt(action, diceResult);
      const llmResponse = await this.llmService.callLLM(prompt);
      return this.parseGameResponse(llmResponse);
    } catch (error) {
      console.error("Action processing error:", error);
      return this.getMockActionResponse(action, diceResult);
    }
  }

  // Combat başlat
  async startCombat() {
    try {
      const prompt = this.createCombatStartPrompt();
      const llmResponse = await this.llmService.callLLM(prompt);
      return this.parseCombatResponse(llmResponse);
    } catch (error) {
      console.error("Combat start error:", error);
      return this.getMockCombatResponse();
    }
  }

  // Combat aksiyonu işle
  async processCombatAction(action, target, diceResult) {
    try {
      const prompt = this.createCombatActionPrompt(action, target, diceResult);
      const llmResponse = await this.llmService.callLLM(prompt);
      return this.parseCombatResponse(llmResponse);
    } catch (error) {
      console.error("Combat action error:", error);
      return this.getMockCombatActionResponse(action, target, diceResult);
    }
  }

  createGameStartPrompt(scenario) {
    return `
TASK: ${scenario.title} senaryosunu başlat ve oyuncuya ilk sahneyi anlat.

SENARYO: ${scenario.title}
TEMA: ${scenario.theme}
ZORLUK: ${scenario.difficulty}
AÇIKLAMA: ${scenario.description}

OYUNCU DURUMU:
- HP: ${this.currentGameState.playerHP}
- Envanter: ${this.currentGameState.playerInventory.join(", ")}
- İstatistikler: ${JSON.stringify(this.currentGameState.playerStats)}

OUTPUT FORMAT:
NARRATIVE: [Senaryo açılış anlatımı]
AVAILABLE_ACTIONS:
- [Aksiyon 1]: [açıklama]
- [Aksiyon 2]: [açıklama]
- [Aksiyon 3]: [açıklama]

DICE_ROLLS:
- [Aksiyon]: [zar tipi] [hedef sayı] [beceri]

CONSEQUENCES:
- [Aksiyon] Success: [başarı sonucu]
- [Aksiyon] Failure: [başarısızlık sonucu]
`;
  }

  createActionPrompt(action, diceResult) {
    return `
TASK: Oyuncu aksiyonunu işle ve sonucu anlat.

AKSİYON: ${action}
ZAR SONUCU: ${diceResult || "Yok"}
SENARYO: ${this.currentScenario.title}
OYUNCU DURUMU: ${JSON.stringify(this.currentGameState)}

OUTPUT FORMAT:
NARRATIVE: [Aksiyon sonucu anlatımı]
AVAILABLE_ACTIONS:
- [Sonraki aksiyon 1]: [açıklama]
- [Sonraki aksiyon 2]: [açıklama]

GAME_STATE_UPDATE:
- HP: [yeni HP]
- Inventory: [yeni envanter]
- Effects: [aktif etkiler]
`;
  }

  createCombatStartPrompt() {
    return `
TASK: Combat sahnesini başlat.

SENARYO: ${this.currentScenario.title}
OYUNCU: HP ${this.currentGameState.playerHP}

OUTPUT FORMAT:
COMBAT_START: [Combat başlangıç anlatımı]
ENEMIES:
- [Düşman 1]: HP [sayı], Attack [sayı], Defense [sayı]
- [Düşman 2]: HP [sayı], Attack [sayı], Defense [sayı]

INITIATIVE_ORDER:
1. [İlk sıra]
2. [İkinci sıra]
3. [Üçüncü sıra]

AVAILABLE_ACTIONS:
- Attack: [açıklama]
- Defend: [açıklama]
- Use Item: [açıklama]
- Cast Spell: [açıklama]
`;
  }

  createCombatActionPrompt(action, target, diceResult) {
    return `
TASK: Combat aksiyonunu işle.

AKSİYON: ${action}
HEDEF: ${target}
ZAR SONUCU: ${diceResult}
OYUNCU HP: ${this.currentGameState.playerHP}

OUTPUT FORMAT:
COMBAT_RESULT: [Aksiyon sonucu anlatımı]
DAMAGE_DEALT: [verilen hasar]
DAMAGE_TAKEN: [alınan hasar]
ENEMY_STATUS: [düşman durumu]
PLAYER_STATUS: [oyuncu durumu]

NEXT_ACTIONS:
- [Sonraki aksiyon 1]
- [Sonraki aksiyon 2]
`;
  }

  parseGameResponse(llmResponse) {
    // Basit parsing - gerçek sistemde daha gelişmiş olacak
    const narrativeMatch = llmResponse.match(
      /NARRATIVE: (.+?)(?=AVAILABLE_ACTIONS|$)/s
    );
    const narrative = narrativeMatch
      ? narrativeMatch[1].trim()
      : "Game Master hazırlanıyor...";

    const actionsMatch = llmResponse.match(
      /AVAILABLE_ACTIONS:(.*?)(?=DICE_ROLLS|CONSEQUENCES|$)/s
    );
    const availableActions = this.parseActions(
      actionsMatch ? actionsMatch[1] : ""
    );

    return {
      narrative,
      availableActions,
      currentState: this.currentGameState,
      isCombat: false,
    };
  }

  parseCombatResponse(llmResponse) {
    const combatMatch = llmResponse.match(/COMBAT_START: (.+?)(?=ENEMIES|$)/s);
    const narrative = combatMatch ? combatMatch[1].trim() : "Combat başlıyor!";

    const enemiesMatch = llmResponse.match(
      /ENEMIES:(.*?)(?=INITIATIVE_ORDER|AVAILABLE_ACTIONS|$)/s
    );
    const enemies = this.parseEnemies(enemiesMatch ? enemiesMatch[1] : "");

    return {
      narrative,
      enemies,
      isCombat: true,
      currentState: this.currentGameState,
    };
  }

  parseActions(actionsText) {
    if (!actionsText) return [];

    return actionsText
      .split("\n")
      .filter((line) => line.trim() && line.includes(":"))
      .map((line) => {
        const match = line.match(/- (.+?): (.+)/);
        if (match) {
          return {
            type: match[1].trim().toLowerCase().replace(/\s+/g, "_"),
            description: match[2].trim(),
          };
        }
        return null;
      })
      .filter(Boolean);
  }

  parseEnemies(enemiesText) {
    if (!enemiesText) return [];

    return enemiesText
      .split("\n")
      .filter((line) => line.trim() && line.includes("HP"))
      .map((line) => {
        const match = line.match(
          /- (.+?): HP (.+?), Attack (.+?), Defense (.+)/
        );
        if (match) {
          return {
            name: match[1].trim(),
            hp: parseInt(match[2]) || 20,
            attack: parseInt(match[3]) || 5,
            defense: parseInt(match[4]) || 3,
          };
        }
        return null;
      })
      .filter(Boolean);
  }

  getMockGameStartResponse(scenario) {
    return {
      narrative: `🎮 ${scenario.title} oyunu başladı! Game Master hazırlanıyor...`,
      availableActions: [
        {
          type: "explore",
          description: "Çevreyi keşfet",
        },
        {
          type: "talk",
          description: "NPC ile konuş",
        },
        {
          type: "investigate",
          description: "Detayları araştır",
        },
      ],
      currentState: this.currentGameState,
      isCombat: false,
    };
  }

  getMockActionResponse(action, diceResult) {
    return {
      narrative: `⚡ ${action} aksiyonunu gerçekleştirdin${
        diceResult ? ` (Zar: ${diceResult})` : ""
      }. Game Master sonucu değerlendiriyor...`,
      availableActions: [
        {
          type: "continue",
          description: "Devam et",
        },
      ],
      currentState: this.currentGameState,
      isCombat: false,
    };
  }

  getMockCombatResponse() {
    return {
      narrative: "⚔️ Combat başlıyor! Düşmanlar karşında!",
      enemies: [
        { name: "Goblin", hp: 15, attack: 4, defense: 2 },
        { name: "Orc", hp: 25, attack: 6, defense: 4 },
      ],
      isCombat: true,
      currentState: this.currentGameState,
    };
  }

  getMockCombatActionResponse(action, target, diceResult) {
    return {
      narrative: `⚔️ ${action} aksiyonu ${target} hedefine karşı gerçekleştirildi${
        diceResult ? ` (Zar: ${diceResult})` : ""
      }!`,
      damageDealt: Math.floor(Math.random() * 10) + 5,
      damageTaken: Math.floor(Math.random() * 5) + 1,
      enemyStatus: "Enemy is wounded",
      playerStatus: "Player is ready",
      nextActions: ["Attack", "Defend", "Use Item"],
    };
  }

  getCurrentGameState() {
    return this.currentGameState;
  }

  saveGame() {
    return {
      scenario: this.currentScenario,
      gameState: this.currentGameState,
      playerCharacter: this.playerCharacter,
      timestamp: new Date().toISOString(),
    };
  }

  loadGame(savedGame) {
    this.currentScenario = savedGame.scenario;
    this.currentGameState = savedGame.gameState;
    this.playerCharacter = savedGame.playerCharacter;
  }
}

module.exports = { GameMasterAI };
