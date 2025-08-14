require("dotenv").config();
const { RealLLMService } = require("./src/services/RealLLMService");

async function testLLMConnection() {
  console.log("🔍 Testing LLM Connection...\n");

  // Test configuration
  const config = {
    provider: process.env.LLM_PROVIDER || "openai",
    model: process.env.LLM_MODEL || "gpt-4",
    temperature: parseFloat(process.env.LLM_TEMPERATURE || "0.7"),
    maxTokens: parseInt(process.env.LLM_MAX_TOKENS || "4000"),
    apiKey: process.env.OPENAI_API_KEY || process.env.ANTHROPIC_API_KEY,
  };

  console.log("Configuration:");
  console.log(`- Provider: ${config.provider}`);
  console.log(`- Model: ${config.model}`);
  console.log(`- Temperature: ${config.temperature}`);
  console.log(`- Max Tokens: ${config.maxTokens}`);
  console.log(`- API Key: ${config.apiKey ? "✅ Set" : "❌ Missing"}\n`);

  if (!config.apiKey) {
    console.error(
      "❌ API Key is missing! Please set OPENAI_API_KEY or ANTHROPIC_API_KEY in your .env file."
    );
    return;
  }

  try {
    const llmService = new RealLLMService(config);

    // Test connection
    console.log("Testing connection...");
    const isConnected = await llmService.testConnection();

    if (isConnected) {
      console.log("✅ LLM connection successful!\n");

      // Test comic analysis prompt
      console.log("Testing comic analysis...");
      const comicPrompt = `
TASK: Bu çizgi romanı analiz et ve RPG senaryo yazmak için öğren.

COMIC: Dungeons & Dragons: The Lost Relic (fantasy)

PAGES DATA:
Page 1:
Panel Descriptions: A group of adventurers stands before a crumbling stone archway | A close-up of a nervous rogue checking for traps | A wizard raises a glowing staff, illuminating the darkness
Dialogue: Rogue: "Are you sure this is the right place?" / Wizard: "The map leads here. Stay alert."
Text: The party enters the ancient ruins. Shadows move in the torchlight.

ANALYSIS INSTRUCTIONS:
1. STORY STRUCTURE: Bu comic'teki hikaye akışını analiz et
2. CHARACTER ANALYSIS: Karakterleri RPG NPC'leri olarak değerlendir
3. WORLD BUILDING: Setting ve atmosphere
4. ACTION SEQUENCES: Savaş ve aksiyon sahneleri
5. RPG CONVERSION: Bu comic'ten RPG senaryosu yazarken

OUTPUT: Öğrendiğin her kategori için bullet points ver.
`;

      const response = await llmService.callLLM({
        prompt: comicPrompt,
        temperature: 0.7,
        maxTokens: 500,
      });

      console.log("✅ Comic analysis successful!");
      console.log("Response:");
      console.log(response.text);
      console.log("\nUsage:", response.usage);
    } else {
      console.log("❌ LLM connection failed!");
    }
  } catch (error) {
    console.error("❌ Error testing LLM:", error.message);
  }
}

// Run test
testLLMConnection();
