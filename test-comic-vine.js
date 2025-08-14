require("dotenv").config();
const { ComicVineAPI } = require("./src/services/ComicVineAPI");

async function testComicVineAPI() {
  console.log("🔍 Testing Comic Vine API...\n");

  const config = {
    apiKey: process.env.COMIC_VINE_API_KEY,
    baseUrl: "https://comicvine.gamespot.com/api",
    rateLimit: 200,
  };

  console.log("Configuration:");
  console.log(`- API Key: ${config.apiKey ? "✅ Set" : "❌ Missing"}`);
  console.log(`- Base URL: ${config.baseUrl}`);
  console.log(`- Rate Limit: ${config.rateLimit} requests/hour\n`);

  if (!config.apiKey) {
    console.error(
      "❌ Comic Vine API Key is missing! Please set COMIC_VINE_API_KEY in your .env file."
    );
    console.log("Get your API key from: https://comicvine.gamespot.com/api/");
    return;
  }

  try {
    const api = new ComicVineAPI(config);

    // Test 1: Search for comics
    console.log("1. Testing comic search...");
    const searchResults = await api.searchComics("fantasy", 3);
    console.log(`✅ Found ${searchResults.results.length} comics`);

    if (searchResults.results.length > 0) {
      const firstComic = searchResults.results[0];
      console.log(
        `   First comic: ${firstComic.name} (${firstComic.volume?.name})`
      );

      // Test 2: Get detailed issue info
      console.log("\n2. Testing detailed issue info...");
      const detailedIssue = await api.getIssueDetails(firstComic.id);
      console.log(`✅ Got details for: ${detailedIssue.results.name}`);
      console.log(
        `   Description: ${detailedIssue.results.description?.substring(
          0,
          100
        )}...`
      );
      console.log(
        `   Characters: ${detailedIssue.results.character_credits?.length || 0}`
      );
      console.log(
        `   Image: ${detailedIssue.results.image?.medium_url || "No image"}`
      );

      // Test 3: Search for characters
      console.log("\n3. Testing character search...");
      const characterResults = await api.searchCharacters("superman", 2);
      console.log(`✅ Found ${characterResults.results.length} characters`);

      if (characterResults.results.length > 0) {
        console.log(`   First character: ${characterResults.results[0].name}`);
      }
    }

    // Test 4: Rate limit status
    console.log("\n4. Rate limit status:");
    const rateLimitStatus = api.getRateLimitStatus();
    console.log(`   Requests made: ${rateLimitStatus.requestsMade}`);
    console.log(`   Remaining: ${rateLimitStatus.remaining}`);

    console.log("\n🎉 Comic Vine API tests completed successfully!");
  } catch (error) {
    console.error("❌ Error testing Comic Vine API:", error.message);
    if (error.response) {
      console.error("Response status:", error.response.status);
      console.error("Response data:", error.response.data);
    }
  }
}

// Run test
testComicVineAPI();
