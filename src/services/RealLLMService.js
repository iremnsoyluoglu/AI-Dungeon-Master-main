const fetch = require("node-fetch");

class RealLLMService {
  constructor() {
    this.apiKey = process.env.OPENAI_API_KEY;
    this.provider = process.env.LLM_PROVIDER || "openai";
    this.model = process.env.LLM_MODEL || "gpt-4";
    this.temperature = parseFloat(process.env.LLM_TEMPERATURE) || 0.7;
    this.maxTokens = parseInt(process.env.LLM_MAX_TOKENS) || 2000;
  }

  async callLLM(prompt) {
    try {
      switch (this.provider.toLowerCase()) {
        case "openai":
          return await this.callOpenAI(prompt);
        case "anthropic":
          return await this.callAnthropic(prompt);
        case "azure":
          return await this.callAzure(prompt);
        default:
          throw new Error(`Unsupported LLM provider: ${this.provider}`);
      }
    } catch (error) {
      console.error("LLM API call failed:", error);
      // Mock response if API fails
      return this.getMockResponse(prompt);
    }
  }

  async callOpenAI(prompt) {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.apiKey}`,
      },
      body: JSON.stringify({
        model: this.model,
        messages: [
          {
            role: "system",
            content:
              "You are an expert RPG scenario writer and Game Master. Respond in the exact format requested.",
          },
          {
            role: "user",
            content: prompt,
          },
        ],
        temperature: this.temperature,
        max_tokens: this.maxTokens,
      }),
    });

    if (!response.ok) {
      throw new Error(
        `OpenAI API error: ${response.status} ${response.statusText}`
      );
    }

    const data = await response.json();
    return data.choices[0].message.content;
  }

  async callAnthropic(prompt) {
    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": this.apiKey,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: this.model,
        max_tokens: this.maxTokens,
        messages: [
          {
            role: "user",
            content: prompt,
          },
        ],
      }),
    });

    if (!response.ok) {
      throw new Error(
        `Anthropic API error: ${response.status} ${response.statusText}`
      );
    }

    const data = await response.json();
    return data.content[0].text;
  }

  async callAzure(prompt) {
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT;
    const deployment = process.env.AZURE_OPENAI_DEPLOYMENT;

    const response = await fetch(
      `${endpoint}/openai/deployments/${deployment}/chat/completions?api-version=2023-05-15`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "api-key": this.apiKey,
        },
        body: JSON.stringify({
          messages: [
            {
              role: "system",
              content:
                "You are an expert RPG scenario writer and Game Master. Respond in the exact format requested.",
            },
            {
              role: "user",
              content: prompt,
            },
          ],
          temperature: this.temperature,
          max_tokens: this.maxTokens,
        }),
      }
    );

    if (!response.ok) {
      throw new Error(
        `Azure OpenAI API error: ${response.status} ${response.statusText}`
      );
    }

    const data = await response.json();
    return data.choices[0].message.content;
  }

  getMockResponse(prompt) {
    // Basit mock response - gerçek sistemde daha gelişmiş olacak
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
    } else if (prompt.includes("TASK:") && prompt.includes("senaryosu üret")) {
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
    } else if (prompt.includes("NARRATIVE:")) {
      return `
NARRATIVE: You find yourself at the entrance of an ancient temple. The air is thick with mystery and danger. What would you like to do?

AVAILABLE_ACTIONS:
- Explore: Search the area for clues and hidden passages
- Talk: Attempt to communicate with any nearby NPCs
- Investigate: Examine the temple entrance more closely

DICE_ROLLS:
- Explore: d20 Perception DC 15
- Talk: d20 Charisma DC 12
- Investigate: d20 Investigation DC 14

CONSEQUENCES:
- Explore Success: You find a hidden switch
- Explore Failure: You miss important clues
- Talk Success: NPC provides valuable information
- Talk Failure: NPC is suspicious of you
`;
    } else {
      return `
TITLE: Adventure Begins
DESCRIPTION: A new adventure awaits you in this mysterious world.

SCENES:
- Scene 1: Starting Point
  Description: You begin your journey here
  NPCs: Guide
  Decision Points: Choose your path
  Combat: None initially

CHOICES:
- Explore the area
- Talk to the guide
- Rest and prepare

FRP MECHANICS:
- Dice Types: d4, d6, d8, d10, d12, d20, d100
- Skill Checks: Various skills required
- Combat System: Turn-based with initiative
- Status Effects: Multiple effects possible
`;
    }
  }
}

module.exports = { RealLLMService };
