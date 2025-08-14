require('dotenv').config();
const { ScenarioDatabase } = require('./src/services/ScenarioDatabase');
const { FRPRPGScenario } = require('./src/types/frpMechanics');

async function testScenarioStorage() {
  console.log('🗄️ Testing Scenario Storage...\n');

  const db = new ScenarioDatabase();
  await db.initialize();

  // Test 1: Senaryo kaydetme
  console.log('1. Testing scenario saving...');
  const testScenario = {
    title: 'Test Fantasy Adventure',
    theme: 'fantasy',
    difficulty: 'medium',
    scenes: [
      {
        id: 'scene_1',
        title: 'Forest Entrance',
        description: 'A mysterious forest awaits...',
        npcs: [],
        decisionPoints: [],
        combatEncounter: null,
        rewards: [],
        nextScenes: []
      }
    ],
    npcs: [
      {
        id: 'npc_1',
        name: 'Old Wizard',
        dialogue: 'Welcome, young adventurer!',
        personality: 'wise',
        role: 'mentor'
      }
    ],
    combatEncounters: [
      {
        id: 'combat_1',
        title: 'Goblin Ambush',
        enemies: [
          {
            name: 'Goblin',
            hp: 10,
            attack: 5,
            defense: 2
          }
        ],
        environment: 'forest',
        victoryConditions: ['defeat_all_enemies'],
        defeatConditions: ['party_defeated']
      }
    ],
    diceMechanics: {
      diceTypes: ['d6', 'd20'],
      customRules: ['advantage_on_natural_20']
    }
  };

  const metadata = {
    sourceComics: ['Test Comic #1'],
    learningSessionId: 'test_session_123',
    generationTime: 2500,
    llmModel: 'gpt-4',
    llmProvider: 'openai'
  };

  const tags = ['fantasy', 'adventure', 'test'];

  try {
    const savedScenario = await db.saveScenario(testScenario, metadata, tags);
    console.log('✅ Scenario saved successfully!');
    console.log(`   ID: ${savedScenario.id}`);
    console.log(`   Title: ${savedScenario.title}`);
    console.log(`   Created: ${savedScenario.createdAt}`);
    console.log(`   Tags: ${savedScenario.tags.join(', ')}\n`);

    // Test 2: Tüm senaryoları getirme
    console.log('2. Testing get all scenarios...');
    const allScenarios = await db.getAllScenarios();
    console.log(`✅ Found ${allScenarios.length} scenarios\n`);

    // Test 3: Favori işlemleri
    console.log('3. Testing favorite operations...');
    const isFavorite = await db.toggleFavorite(savedScenario.id);
    console.log(`✅ Toggled favorite: ${isFavorite}`);

    const favorites = await db.getFavorites();
    console.log(`✅ Found ${favorites.length} favorite scenarios\n`);

    // Test 4: Favori durumunu tekrar değiştir
    const isFavoriteAgain = await db.toggleFavorite(savedScenario.id);
    console.log(`✅ Toggled favorite again: ${isFavoriteAgain}`);

    const favoritesAfter = await db.getFavorites();
    console.log(`✅ Found ${favoritesAfter.length} favorite scenarios after toggle\n`);

    console.log('🎉 All scenario storage tests passed!');

  } catch (error) {
    console.error('❌ Error testing scenario storage:', error);
  }
}

// Run test
testScenarioStorage(); 