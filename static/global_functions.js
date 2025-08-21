// GLOBAL FUNCTIONS - MUST BE LOADED FIRST
console.log("✅ Loading global functions...");

// --- LIGHTWEIGHT STORY PROGRESSION TRACKING (per scenario) ---
window.storyProgress = window.storyProgress || {};

function getScenarioProgress(scenarioId) {
  const key = scenarioId || window.currentScenarioId || "unknown";
  if (!window.storyProgress[key]) {
    window.storyProgress[key] = {
      cluesFound: 0,
      sideQuestsCompleted: 0,
      fightsWon: 0,
      visitedLocations: {},
    };
  }
  return window.storyProgress[key];
}

function markVisited(scenarioId, locationKey) {
  const prog = getScenarioProgress(scenarioId);
  if (locationKey) {
    prog.visitedLocations[locationKey] = true;
  }
}

function recordClue(scenarioId) {
  const prog = getScenarioProgress(scenarioId);
  prog.cluesFound += 1;
}

function recordSideQuest(scenarioId) {
  const prog = getScenarioProgress(scenarioId);
  prog.sideQuestsCompleted += 1;
}

function recordFightWin(scenarioId) {
  const prog = getScenarioProgress(scenarioId);
  prog.fightsWon += 1;
}

function isLikelyFinalNode(scenarioId, nextNodeId) {
  const id = (nextNodeId || "").toLowerCase();
  const sid = (scenarioId || "").toLowerCase();

  const patterns = {
    dragon_hunters_path: [
      "final",
      "boss",
      "fight_dragon",
      "fight_with_dragon",
      "final_attack",
    ],
    magical_forest_mysteries: [
      "final",
      "boss",
      "fight_malakar",
      "confront_malakar",
    ],
    hive_city_defense: [
      "final",
      "boss",
      "fight_collective",
      "collective_core",
      "target_collective_core",
    ],
    cyberpunk_city_secrets: [
      "final",
      "boss",
      "fight_megacorp",
      "megacorp_core",
      "target_megacorp_core",
    ],
  };

  const matchers = patterns[sid] || [
    "final",
    "boss",
    "end",
    "confront",
    "fight_",
  ];
  return matchers.some((m) => id.includes(m));
}

function gatingRequirementsMet(scenarioId) {
  const prog = getScenarioProgress(scenarioId);

  // Get current player level
  let playerLevel = 1;
  try {
    if (window.skillSystem && window.skillSystem.progression) {
      playerLevel = window.skillSystem.progression.level || 1;
    }
  } catch (e) {
    console.warn("⚠️ Could not get player level:", e);
  }

  // STRICT GATING: Player must be at least level 5 and have significant progress
  const levelRequirement = playerLevel >= 5;
  const clueRequirement = prog.cluesFound >= 5; // Increased from 2 to 5
  const sideQuestRequirement = prog.sideQuestsCompleted >= 3; // Increased from 1 to 3
  const fightRequirement = prog.fightsWon >= 8; // Must win at least 8 fights
  const explorationRequirement = Object.keys(prog.visitedLocations).length >= 6; // Must visit 6+ locations

  console.log("🎯 Gating check:", {
    scenarioId,
    playerLevel,
    levelRequirement,
    cluesFound: prog.cluesFound,
    clueRequirement,
    sideQuestsCompleted: prog.sideQuestsCompleted,
    sideQuestRequirement,
    fightsWon: prog.fightsWon,
    fightRequirement,
    locationsVisited: Object.keys(prog.visitedLocations).length,
    explorationRequirement,
  });

  return (
    levelRequirement &&
    clueRequirement &&
    sideQuestRequirement &&
    fightRequirement &&
    explorationRequirement
  );
}

function buildExplorationGateNode(scenarioId) {
  const sid = (scenarioId || "").toLowerCase();
  const prog = getScenarioProgress(scenarioId);
  
  // Get current player level
  let playerLevel = 1;
  try {
    if (window.skillSystem && window.skillSystem.progression) {
      playerLevel = window.skillSystem.progression.level || 1;
    }
  } catch (e) {
    console.warn("⚠️ Could not get player level:", e);
  }
  
  let themeExplore = [
    { text: "Çevreyi keşfet", nextNode: "explore_environment" },
    { text: "NPC'lerle konuş", nextNode: "talk_to_npcs" },
    { text: "Yan görev ara", nextNode: "find_side_quest" },
    { text: "Düşmanlarla savaş", nextNode: "find_enemies" },
  ];

  // FANTASY THEME - Dragon Hunters Path
  if (sid === "dragon_hunters_path") {
    themeExplore = [
      { text: "Köyü araştır", nextNode: "gather_info" },
      { text: "Eski tapınağa git", nextNode: "investigate_temple" },
      { text: "Haydut izi sür", nextNode: "track_bandits" },
      { text: "Ormanı keşfet", nextNode: "explore_forest" },
      { text: "Mağaraları ara", nextNode: "explore_caves" },
      { text: "Köylülerle konuş", nextNode: "talk_to_villagers" },
      { text: "Haydutlarla savaş", nextNode: "fight_bandits" },
      { text: "Kurt sürüsüyle karşılaş", nextNode: "fight_wolves" },
      { text: "Tapınak muhafızlarıyla savaş", nextNode: "fight_guards" },
      { text: "Eski kalıntıları ara", nextNode: "explore_ruins" },
    ];
  } 
  // FANTASY THEME - Magical Forest Mysteries
  else if (sid === "magical_forest_mysteries") {
    themeExplore = [
      { text: "Ormanda iz sür", nextNode: "explore_forest" },
      { text: "Köyde konuş", nextNode: "talk_to_villagers" },
      { text: "Ruhların fısıltısını takip et", nextNode: "follow_whispers" },
      { text: "Eski kalıntıları ara", nextNode: "explore_ruins" },
      { text: "Gizli geçitleri bul", nextNode: "find_secret_passages" },
      { text: "Orman yaratıklarıyla savaş", nextNode: "fight_forest_creatures" },
      { text: "Büyülü tuzakları atlat", nextNode: "avoid_magical_traps" },
      { text: "Kayıp köylüleri ara", nextNode: "search_missing_villagers" },
      { text: "Eski muhafızlarla savaş", nextNode: "fight_ancient_guards" },
      { text: "Ruh varlıklarıyla karşılaş", nextNode: "confront_spirits" },
    ];
  } 
  // SCI-FI THEME - Hive City Defense
  else if (sid === "hive_city_defense") {
    themeExplore = [
      { text: "Laboratuvarları incele", nextNode: "investigate_laboratory_complex" },
      { text: "Devriye rotalarını keşfet", nextNode: "scout_patrols" },
      { text: "Direnişle temas kur", nextNode: "find_resistance" },
      { text: "Alt seviyeleri ara", nextNode: "explore_lower_levels" },
      { text: "Güvenlik sistemlerini hack'le", nextNode: "hack_security" },
      { text: "Robotlarla savaş", nextNode: "fight_robots" },
      { text: "Mutantlarla karşılaş", nextNode: "fight_mutants" },
      { text: "Veri merkezini keşfet", nextNode: "explore_data_center" },
      { text: "Güvenlik botlarıyla savaş", nextNode: "fight_security_bots" },
      { text: "Hack'lenmiş sistemleri onar", nextNode: "repair_systems" },
      { text: "Gizli laboratuvarları bul", nextNode: "find_secret_labs" },
      { text: "AI kontrollü makinelerle savaş", nextNode: "fight_ai_machines" },
    ];
  } 
  // CYBERPUNK THEME - Cyberpunk City Secrets
  else if (sid === "cyberpunk_city_secrets") {
    themeExplore = [
      { text: "Arka sokakları keşfet", nextNode: "explore_backstreets" },
      { text: "Netrunner ile buluş", nextNode: "find_hacker" },
      { text: "Şirket veri merkezini izle", nextNode: "recon_megacorp" },
      { text: "Underground'ı ara", nextNode: "explore_underground" },
      { text: "Gangsterlarla savaş", nextNode: "fight_gangsters" },
      { text: "Güvenlik botlarıyla karşılaş", nextNode: "fight_security_bots" },
      { text: "Hack'lenmiş sistemleri onar", nextNode: "repair_systems" },
      { text: "Gizli laboratuvarları bul", nextNode: "find_secret_labs" },
      { text: "Corporate muhafızlarla savaş", nextNode: "fight_corporate_guards" },
      { text: "Cyber-psycho'larla karşılaş", nextNode: "fight_cyberpsychos" },
      { text: "AI kontrollü sistemlerle savaş", nextNode: "fight_ai_systems" },
      { text: "Underground çeteleriyle savaş", nextNode: "fight_underground_gangs" },
    ];
  }

  const description = `Ana tehditle yüzleşmeden önce daha fazla deneyim kazanmalısın!

🎯 Gereksinimler:
• Seviye: ${playerLevel}/5 (${playerLevel >= 5 ? '✅' : '❌'})
• İpucu: ${prog.cluesFound}/5 (${prog.cluesFound >= 5 ? '✅' : '❌'})
• Yan görev: ${prog.sideQuestsCompleted}/3 (${prog.sideQuestsCompleted >= 3 ? '✅' : '❌'})
• Savaş zaferi: ${prog.fightsWon}/8 (${prog.fightsWon >= 8 ? '✅' : '❌'})
• Keşfedilen yer: ${Object.keys(prog.visitedLocations).length}/6 (${Object.keys(prog.visitedLocations).length >= 6 ? '✅' : '❌'})

Alternatif yolları keşfet, yan görevleri tamamla, düşmanlarla savaş ve gerçeği kendin ortaya çıkar.`;

  return {
    title: "Henüz Zamanı Değil - Daha Fazla Deneyim Gerekli",
    description: description,
    choices: themeExplore,
  };
}

function maybeInterceptFinal(scenarioId, nextNodeId) {
  if (!isLikelyFinalNode(scenarioId, nextNodeId)) return null;
  if (gatingRequirementsMet(scenarioId)) return null;
  return buildExplorationGateNode(scenarioId);
}

// SWITCH THEME FUNCTION
window.switchTheme = function (theme) {
  console.log("✅ SWITCH THEME:", theme);

  // Remove active class from all theme tabs
  document.querySelectorAll(".theme-tab").forEach((tab) => {
    if (tab) tab.classList.remove("active");
  });

  // Add active class to clicked tab
  const activeTab = document.querySelector(
    `[onclick="switchTheme('${theme}')"]`
  );
  if (activeTab) {
    activeTab.classList.add("active");
  }

  // Hide all theme content
  document.querySelectorAll(".theme-content").forEach((content) => {
    if (content) content.style.display = "none";
  });

  // Show selected theme content
  const themeContent = document.getElementById(`${theme}-content`);
  if (themeContent) {
    themeContent.style.display = "block";
  }

  // Hide all scenario categories
  document.querySelectorAll(".scenario-category").forEach((category) => {
    if (category) category.style.display = "none";
  });

  // Show selected theme's scenario category
  const scenarioCategory = document.getElementById(theme + "-scenarios");
  if (scenarioCategory) {
    scenarioCategory.style.display = "block";
  }

  // Initialize NPCs for the selected theme
  if (window.npcSystem && window.npcSystem.initializeNPCs) {
    window.npcSystem.initializeNPCs(theme);
    window.npcSystem.updateNPCDisplay();
  }
};

// SELECT RACE FUNCTION
window.selectRace = function (race) {
  console.log("✅ SELECT RACE:", race);

  // Remove selected class from all race items
  document
    .querySelectorAll(".race-class-list:nth-child(1) .list-item")
    .forEach((item) => {
      if (item) item.classList.remove("selected");
    });

  // Add selected class to clicked race
  const selectedRace = document.querySelector(
    `[onclick="selectRace('${race}')"]`
  );
  if (selectedRace) {
    selectedRace.classList.add("selected");
  }

  // Update character panel
  if (window.updateCharacterPanel) {
    window.updateCharacterPanel();
  }

  // Apply race/class derived stats
  if (window.applyRaceClassToStats) {
    window.applyRaceClassToStats();
  }
};

// SELECT CLASS FUNCTION
window.selectClass = function (className) {
  console.log("✅ SELECT CLASS:", className);

  // Remove selected class from all class items
  document
    .querySelectorAll(".race-class-list:nth-child(2) .list-item")
    .forEach((item) => {
      if (item) item.classList.remove("selected");
    });

  // Add selected class to clicked class
  const selectedClass = document.querySelector(
    `[onclick="selectClass('${className}')"]`
  );
  if (selectedClass) {
    selectedClass.classList.add("selected");
  }

  // Update character panel
  if (window.updateCharacterPanel) {
    window.updateCharacterPanel();
  }

  // Apply race/class derived stats
  if (window.applyRaceClassToStats) {
    window.applyRaceClassToStats();
  }
};

// --- RACE/CLASS -> STATS WIRING ---
// Cache game data
window.gameData = window.gameData || { races: null, classes: null };

window.loadRacesAndClasses = async function () {
  try {
    if (!window.gameData.races) {
      const r = await fetch("/api/game/character/races");
      const rj = await r.json();
      if (rj && rj.success !== false) window.gameData.races = rj.races || rj;
    }
    if (!window.gameData.classes) {
      const c = await fetch("/api/game/character/classes");
      const cj = await c.json();
      if (cj && cj.success !== false)
        window.gameData.classes = cj.classes || cj;
    }
  } catch (e) {
    console.warn("⚠️ Failed to load races/classes:", e);
  }
};

window.applyRaceClassToStats = async function () {
  // Ensure data is loaded
  if (!window.gameData.races || !window.gameData.classes) {
    await window.loadRacesAndClasses();
  }

  // Read selected names from UI
  const selectedRaceEl = document.querySelector(
    ".race-class-list:nth-child(1) .list-item.selected"
  );
  const selectedClassEl = document.querySelector(
    ".race-class-list:nth-child(2) .list-item.selected"
  );
  const raceName = selectedRaceEl ? selectedRaceEl.textContent.trim() : null;
  const className = selectedClassEl ? selectedClassEl.textContent.trim() : null;

  if (!className) {
    console.log("ℹ️ No class selected yet; skipping stat apply");
    return;
  }

  // Resolve class by name
  let classData = null;
  try {
    const classes = window.gameData.classes || {};
    for (const key in classes) {
      const c = classes[key];
      if (c && (c.name === className || key === className)) {
        classData = c;
        break;
      }
    }
  } catch (e) {
    /* ignore */
  }

  if (!classData) {
    console.warn("⚠️ Class not found for stats:", className);
    return;
  }

  // Resolve race bonuses by name (optional)
  let raceBonus = { hp_bonus: 0, attack_bonus: 0, defense_bonus: 0 };
  if (raceName) {
    try {
      const races = window.gameData.races || {};
      for (const key in races) {
        const r = races[key];
        if (r && (r.name === raceName || key === raceName)) {
          raceBonus = r;
          break;
        }
      }
    } catch (e) {
      /* ignore */
    }
  }

  // Compute derived stats
  const baseHp =
    Number(classData.base_hp || 100) + Number(raceBonus.hp_bonus || 0);
  const baseAttack =
    Number(classData.base_attack || 50) + Number(raceBonus.attack_bonus || 0);
  const baseDefense =
    Number(classData.base_defense || 50) + Number(raceBonus.defense_bonus || 0);

  // Apply to combat player stats immediately
  try {
    if (window.combatSystem && window.combatSystem.player) {
      window.combatSystem.player.maxHealth = Math.max(1, baseHp);
      // If current health exceeds new max, clamp it; otherwise fill to max when class selected first time
      if (
        window.combatSystem.player.health > window.combatSystem.player.maxHealth
      ) {
        window.combatSystem.player.health =
          window.combatSystem.player.maxHealth;
      } else if (!window.combatSystem.isActive) {
        // Out of combat, refill to max on selection for clarity
        window.combatSystem.player.health =
          window.combatSystem.player.maxHealth;
      }
      // Stash additional combat-relevant fields
      window.combatSystem.player.attack = baseAttack;
      window.combatSystem.player.defense = baseDefense;
      // Reflect changes if combat UI is visible
      if (typeof window.combatSystem.updateCombatUI === "function") {
        window.combatSystem.updateCombatUI();
      }
    }
  } catch (e) {
    console.warn("⚠️ Could not apply stats to combat system:", e);
  }

  // Also update window.currentCharacter stats
  try {
    if (window.currentCharacter) {
      window.currentCharacter.maxHp = Math.max(1, baseHp);
      window.currentCharacter.hp = Math.max(1, baseHp);
      window.currentCharacter.attack = baseAttack;
      window.currentCharacter.defense = baseDefense;

      // Update character panel to reflect changes
      if (typeof window.updateCharacterPanel === "function") {
        window.updateCharacterPanel();
      }
    }
  } catch (e) {
    console.warn("⚠️ Could not apply stats to currentCharacter:", e);
  }

  // Optionally persist to backend progression stats (guest user)
  try {
    fetch("/api/character/stats/guest_001", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        hp: baseHp,
        max_hp: baseHp,
        attack: baseAttack,
        defense: baseDefense,
      }),
    }).catch(() => {});
  } catch (_) {}
};

// SELECT SCENARIO FUNCTION
window.selectScenario = function (scenarioId) {
  console.log("✅ SELECT SCENARIO:", scenarioId);

  // Start the selected scenario
  if (window.startScenario) {
    window.startScenario(scenarioId);
  }
};

// GENERATE AI SCENARIO FUNCTION
window.generateAIScenario = function () {
  console.log("✅ GENERATE AI SCENARIO");
  
  // Get AI scenario parameters
  const theme = document.getElementById("ai-theme")?.value || "fantasy";
  const difficulty = document.getElementById("ai-difficulty")?.value || "medium";
  const level = document.getElementById("ai-level")?.value || 5;
  
  // Check if file is uploaded
  const fileInput = document.getElementById("file-input");
  let fileContent = "";
  
  if (fileInput && fileInput.files[0]) {
    const file = fileInput.files[0];
    const reader = new FileReader();
    
    reader.onload = function(e) {
      fileContent = e.target.result;
      generateScenarioWithFile(theme, difficulty, level, fileContent);
    };
    
    reader.readAsText(file);
  } else {
    // Generate without file
    generateScenarioWithFile(theme, difficulty, level, "");
  }
};

// Generate scenario with file content
async function generateScenarioWithFile(theme, difficulty, level, fileContent) {
  // Show loading state
  const generateBtn = document.querySelector(".generate-btn");
  if (generateBtn) {
    generateBtn.textContent = "🧙‍♂️ Üretiliyor...";
    generateBtn.disabled = true;
  }
  
  try {
    // Call API to generate scenario
    const response = await fetch('/api/generate-scenario', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        theme: theme,
        difficulty: difficulty,
        fileContent: fileContent
      }),
    });
    
    const data = await response.json();
    
    if (data.success) {
      // Add to AI scenarios grid
      addAIScenarioToGrid(data.scenario);
      
      // Show success message
      alert(`✅ AI Senaryo üretildi: ${data.scenario.title}`);
    } else {
      alert('❌ Senaryo üretilemedi!');
    }
  } catch (error) {
    console.error('Hata:', error);
    alert('❌ Bir hata oluştu!');
  } finally {
    // Reset button
    if (generateBtn) {
      generateBtn.textContent = "🧙‍♂️ Senaryo Üret";
      generateBtn.disabled = false;
    }
  }
}

// Make choice for AI scenarios
function makeAIChoice(nextNodeId) {
  console.log("✅ MAKE AI CHOICE:", nextNodeId);
  
  try {
    const scenarioId = window.currentScenarioId;
    const scenario = window.currentScenario;
    
    if (!scenario || !scenario.nodes) {
      console.error("❌ No AI scenario or nodes found");
      return;
    }
    
    // Get the next node
    const nextNode = scenario.nodes[nextNodeId];
    
    if (!nextNode) {
      console.error("❌ AI Node not found:", nextNodeId);
      // Create a fallback node
      const fallbackNode = {
        id: nextNodeId,
        title: "Macera Devam Ediyor",
        description: "Macera devam ediyor ve yeni kararlar vermen gerekiyor.",
        choices: [
          { text: "Devam et", next_node: "start" },
          { text: "Geri dön", next_node: "start" }
        ]
      };
      window.displayStoryNode(fallbackNode);
      return;
    }
    
    console.log("✅ AI Next node:", nextNode);
    
    // Display the next node
    window.displayStoryNode(nextNode);
    
  } catch (error) {
    console.error("❌ Error making AI choice:", error);
  }
}

// Load AI scenarios on page load
window.loadAIScenarios = function() {
  try {
    // Clear existing scenarios
    const aiScenariosGrid = document.getElementById("ai-scenarios-grid");
    if (aiScenariosGrid) {
      aiScenariosGrid.innerHTML = "";
    }
    
    // Load from localStorage or use default scenarios
    let scenarios = JSON.parse(localStorage.getItem('ai_generated_scenarios') || '[]');
    
    // If no scenarios exist, create some default ones
    if (scenarios.length === 0) {
      scenarios = [
        {
          id: "ai_fantasy_adventure",
          title: "Kayıp Krallık",
          description: "Eski bir haritada keşfedilen kayıp krallığın sırları...",
          difficulty: "Orta"
        },
        {
          id: "ai_scifi_mystery", 
          title: "Uzay İstasyonu",
          description: "Gizemli sinyaller gönderen terk edilmiş uzay istasyonu...",
          difficulty: "Zor"
        },
        {
          id: "ai_cyberpunk_heist",
          title: "MegaCorp Hack",
          description: "En büyük şirketin veri merkezinden gizli bilgiler çalma görevi...",
          difficulty: "Çok Zor"
        },
        {
          id: "ai_fantasy_quest",
          title: "Büyülü Orman",
          description: "Büyülü yaratıkların yaşadığı gizemli ormanın keşfi...",
          difficulty: "Kolay"
        },
        {
          id: "ai_scifi_exploration",
          title: "Yabancı Gezegen",
          description: "Bilinmeyen bir gezegende hayatta kalma mücadelesi...",
          difficulty: "Orta"
        }
      ];
      
      // Save default scenarios to localStorage
      localStorage.setItem('ai_generated_scenarios', JSON.stringify(scenarios));
    }
    
    scenarios.forEach(scenario => {
      addAIScenarioToGrid(scenario.id, scenario.title, scenario.description, scenario.difficulty);
    });
    
    console.log(`✅ Loaded ${scenarios.length} AI scenarios`);
  } catch (error) {
    console.error("❌ Error loading AI scenarios:", error);
  }
};

// DISPLAY STORY NODE FUNCTION
window.displayStoryNode = function (node) {
  console.log("✅ DISPLAY STORY NODE:", node.title);

  const storyText = document.getElementById("story-text");
  const choicesGrid = document.getElementById("choices-grid");

  // Track current node on the active scenario for downstream logic (stats, quest hooks)
  try {
    const activeScenario = getCurrentScenario();
    if (activeScenario) {
      activeScenario.currentNode = node;
    }
  } catch (e) {
    console.warn("⚠️ Could not set currentNode on scenario:", e);
  }

  if (storyText && node) {
    // Display story text - check both 'text' and 'description' properties
    const storyContent =
      node.description || node.text || "Hikaye devam ediyor...";
    storyText.innerHTML = `<p>${storyContent}</p>`;
  }

  if (choicesGrid && node.choices) {
    choicesGrid.innerHTML = "";
    node.choices.forEach((choice) => {
      const choiceButton = document.createElement("button");
      choiceButton.className = "choice-btn";
      choiceButton.textContent = choice.text || "Devam et";
      choiceButton.onclick = () => {
        const nextNodeId =
          choice.next_node || choice.nextNode || choice.next_node_id || "start";
        // Exploration gating: if player tries to jump to likely final too early, intercept
        try {
          const scenarioId =
            window.currentScenarioId ||
            (window.currentScenario && window.currentScenario.id);
          const gate = maybeInterceptFinal(scenarioId, nextNodeId);
          if (gate) {
            console.log(
              "🚧 Final hedefe erken yönelim engellendi, önce keşif gerekli."
            );
            window.displayStoryNode(gate);
            return;
          }
        } catch (e) {
          /* ignore */
        }
        console.log("✅ Choice clicked:", choice.text, "->", nextNodeId);
        window.makeChoice(nextNodeId);
      };
      choicesGrid.appendChild(choiceButton);
    });
  }

  console.log("✅ Story node displayed");

  // Auto-trigger combat when the node indicates a battle across scenarios
  try {
    const nodeId = (node.id || "").toLowerCase();
    const nodeTitle = (node.title || "").toLowerCase();

    // Use the new combat trigger function
    if (window.autoTriggerCombat) {
      window.autoTriggerCombat(window.currentScenarioId, nodeId, nodeTitle);
    }
  } catch (e) {
    console.warn("⚠️ Combat auto-trigger skipped:", e);
  }
};

// MAKE CHOICE FUNCTION
window.makeChoice = function (nextNodeId) {
  console.log("✅ MAKE CHOICE:", nextNodeId);

  // Get current scenario ID - this is the key fix
  const scenarioId = window.currentScenarioId;
  if (!scenarioId) {
    console.error("❌ No active scenario ID");
    return;
  }

  console.log("✅ Using scenario ID:", scenarioId);

  // Check if this is an AI generated scenario
  if (scenarioId.startsWith('ai_scenario_')) {
    makeAIChoice(nextNodeId);
    return;
  }

  // Check if this choice triggers any quest actions
  const questActions = {
    // Dragon Hunters Path quests
    talk_lydia: "investigate_healer",
    investigate_healer: "investigate_healer",
    talk_shadow: "dragon_knowledge",
    learn_dragon_secret: "dragon_knowledge",
    find_evidence: "investigate_healer",
    understand_necklace: "dragon_knowledge",
    urgent_find_lydia: "investigate_healer",
    search_healer_room: "investigate_healer",
    observe_healer: "investigate_healer",
    convince_healer: "investigate_healer",
    strike_necklace: "investigate_healer",
    prepare_combat_healer: "investigate_healer",
    peace_with_dragon: "dragon_knowledge",
    return_necklace_dragon: "dragon_knowledge",
    summon_dragon: "dragon_knowledge",

    // Hive City Defense quests
    investigate_laboratory_complex: "hive_investigation",
    work_with_dr_alex: "hive_investigation",
    fight_robots: "hive_combat",
    target_robot_weakness: "hive_combat",
    infiltrate_control_center: "hive_infiltration",
    confront_collective: "hive_confrontation",
    fight_collective: "hive_final_battle",
    target_collective_core: "hive_final_battle",

    // Magical Forest Mysteries quests
    investigate_west_forest: "forest_investigation",
    follow_voice: "forest_investigation",
    rescue_finn: "forest_rescue",
    confront_malakar: "forest_confrontation",
    fight_malakar: "forest_combat",
    talk_to_elara: "forest_communication",
    rescue_all_people: "forest_rescue",

    // Cyberpunk City Secrets quests
    investigate_megacorp_center: "cyberpunk_investigation",
    find_hacker: "cyberpunk_investigation",
    work_with_neon: "cyberpunk_infiltration",
    confront_megacorp: "cyberpunk_confrontation",
    fight_megacorp: "cyberpunk_combat",
    target_megacorp_core: "cyberpunk_final_battle",
  };

  const questId = questActions[nextNodeId];
  if (questId && window.npcSystem && window.npcSystem.activeQuests) {
    const hasQuest = window.npcSystem.activeQuests.some(
      (quest) => quest.id === questId
    );
    if (hasQuest) {
      // Complete quest action
      window.npcSystem.completeQuestAction(questId, nextNodeId);
    }
  }

  // Fetch the next node from backend
  fetch(`/api/story/node/${scenarioId}/${nextNodeId}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        const node = data.node;
        console.log("✅ Backend node data:", node);

        // Record lightweight progress based on node id/title
        try {
          const nodeId = (node.id || nextNodeId || "").toLowerCase();
          // Simple heuristics: mark clues/sidequests/locations
          if (
            nodeId.includes("investigate") ||
            nodeId.includes("clue") ||
            nodeId.includes("evidence") ||
            nodeId.includes("ipucu")
          ) {
            recordClue(scenarioId);
          }
          if (
            nodeId.includes("side") ||
            nodeId.includes("yan_") ||
            nodeId.includes("rescue") ||
            nodeId.includes("save") ||
            nodeId.includes("yardim") ||
            nodeId.includes("help")
          ) {
            recordSideQuest(scenarioId);
          }
          if (
            nodeId.includes("explore") ||
            nodeId.includes("travel") ||
            nodeId.includes("journey") ||
            nodeId.includes("keşfet") ||
            nodeId.includes("yolculuk")
          ) {
            markVisited(scenarioId, nodeId);
          }
        } catch (e) {
          /* ignore */
        }

        // Update player statistics based on the choice made
        if (window.updatePlayerStatistics) {
          // Get the current node from the backend response to find the choice effects
          if (node && node.choices) {
            // Find the choice that was made to get its effects
            const choice = node.choices.find(
              (c) =>
                (c.next_node || c.nextNode || c.next_node_id) === nextNodeId
            );

            if (choice) {
              // Update karma if choice has karma effect
              if (choice.karma_effect) {
                window.updatePlayerStatistics("karma", choice.karma_effect, {
                  choice: choice.text,
                  context: "story_choice",
                });
              }

              // Update reputation if choice has reputation effect
              if (choice.reputation_effect) {
                window.updatePlayerStatistics(
                  "reputation",
                  choice.reputation_effect,
                  {
                    choice: choice.text,
                    context: "story_choice",
                  }
                );
              }

              // Update NPC relationship if choice has relationship effect
              if (choice.npc_relationship_effect) {
                window.updatePlayerStatistics(
                  "npc_relationship",
                  choice.npc_relationship_effect,
                  {
                    choice: choice.text,
                    npc_id: choice.npc_id || "unknown",
                    context: "story_choice",
                  }
                );
              }

              // Record moral choice
              window.updatePlayerStatistics("moral_choice", 0, {
                choice: choice.text,
                karma_effect: choice.karma_effect || 0,
                reputation_effect: choice.reputation_effect || 0,
              });
            }
          }
        }

        // Use the node data directly from backend
        window.displayStoryNode(node);
      } else {
        console.error("❌ Failed to fetch node:", data.message);
        // Show error message
        const errorNode = {
          title: "Hikaye Devam Ediyor",
          description:
            "Bu hikaye yolu henüz tamamlanmadı. Lütfen başka bir seçim yapın veya hikayenin başına dönün.",
          choices: [
            { text: "Başa dön", nextNode: "start" },
            { text: "Farklı yol seç", nextNode: "talk_aldric" },
          ],
        };
        window.displayStoryNode(errorNode);
      }
    })
    .catch((error) => {
      console.error("❌ Error fetching node:", error);
      // Show error message
      const errorNode = {
        title: "Hikaye Devam Ediyor",
        description:
          "Bu hikaye yolu henüz tamamlanmadı. Lütfen başka bir seçim yapın veya hikayenin başına dönün.",
        choices: [
          { text: "Başa dön", nextNode: "start" },
          { text: "Farklı yol seç", nextNode: "talk_aldric" },
        ],
      };
      window.displayStoryNode(errorNode);
    });
};

// GET CURRENT SCENARIO FUNCTION
window.getCurrentScenario = function () {
  // Use the global currentScenario that's set by startScenario
  if (window.currentScenario) {
    return window.currentScenario;
  }

  // Fallback: Get current scenario based on active scenario ID
  const scenarioId = window.currentScenarioId;
  if (scenarioId && window.scenarios) {
    return window.scenarios[scenarioId] || null;
  }

  return null;
};

// UPDATE CHARACTER PANEL FUNCTION
window.updateCharacterPanel = function () {
  console.log("✅ UPDATE CHARACTER PANEL");

  const characterPanel = document.getElementById("character-panel");
  if (!characterPanel) return;

  const selectedRace = document.querySelector(
    ".race-class-list:nth-child(1) .list-item.selected"
  );
  const selectedClass = document.querySelector(
    ".race-class-list:nth-child(2) .list-item.selected"
  );

  const raceText = selectedRace ? selectedRace.textContent.trim() : "Seçilmedi";
  const classText = selectedClass
    ? selectedClass.textContent.trim()
    : "Seçilmedi";

  const characterInfo = {
    characterName: "İsimsiz Kahraman",
    race: raceText,
    class: classText,
  };

  console.log("✅ Character panel updated:", characterInfo);

  characterPanel.innerHTML = `
    <h3>🎭 Karakter Bilgileri</h3>
    <p><strong>İsim:</strong> ${characterInfo.characterName}</p>
    <p><strong>Irk:</strong> ${characterInfo.race}</p>
    <p><strong>Sınıf:</strong> ${characterInfo.class}</p>
  `;
};

// SAVE GAME FUNCTION
window.saveGame = function () {
  console.log("✅ SAVE GAME");
  alert("💾 Oyun kaydedildi!");
};

// LOAD GAME FUNCTION
window.loadGame = function () {
  console.log("✅ LOAD GAME");
  alert("📁 Oyun yüklendi!");
};

// RESET GAME FUNCTION
window.resetGame = function () {
  console.log("✅ RESET GAME");
  if (confirm("🔄 Oyunu sıfırlamak istediğinizden emin misiniz?")) {
    location.reload();
  }
};

// UPDATE CHARACTER NAME FUNCTION
window.updateCharacterName = function (name) {
  console.log("✅ UPDATE CHARACTER NAME:", name);
  if (window.updateCharacterPanel) {
    window.updateCharacterPanel();
  }
};

// COMBAT SYSTEM FUNCTIONS
window.combatSystem = {
  isActive: false,
  player: {
    name: "Oyuncu",
    health: 100,
    maxHealth: 100,
    energy: 50,
    maxEnergy: 50,
    avatar: "👤",
  },
  enemy: {
    name: "Düşman",
    health: 100,
    maxHealth: 100,
    energy: 50,
    maxEnergy: 50,
    avatar: "👹",
  },
  turn: "player", // "player" or "enemy"
  log: [],

  // Initialize combat
  startCombat: function (enemyData) {
    console.log("⚔️ Starting combat with:", enemyData);

    this.isActive = true;
    this.enemy = {
      name: enemyData.name || "Düşman",
      health: enemyData.health || 100,
      maxHealth: enemyData.maxHealth || 100,
      energy: enemyData.energy || 50,
      maxEnergy: enemyData.maxEnergy || 50,
      avatar: enemyData.avatar || "👹",
    };

    this.turn = "player";
    this.log = [];

    // Show combat section (guard against missing elements)
    const combatEl = document.getElementById("combat-section");
    const storyEl = document.getElementById("story-text");
    const choicesEl = document.getElementById("choices-section");
    if (combatEl) combatEl.style.display = "block";
    if (storyEl) storyEl.style.display = "none";
    if (choicesEl) choicesEl.style.display = "none";

    this.updateCombatUI();
    this.addLogEntry(
      "⚔️ Savaş başladı! " + this.enemy.name + " ile karşı karşıyasın!"
    );
  },

  // Update combat UI
  updateCombatUI: function () {
    // Update player stats
    document.getElementById("player-name").textContent = this.player.name;
    document.getElementById("player-avatar").textContent = this.player.avatar;
    document.getElementById("player-health-text").textContent =
      this.player.health + "/" + this.player.maxHealth;
    document.getElementById("player-energy-text").textContent =
      this.player.energy + "/" + this.player.maxEnergy;

    // Update health and energy bars
    const playerHealthPercent =
      (this.player.health / this.player.maxHealth) * 100;
    const playerEnergyPercent =
      (this.player.energy / this.player.maxEnergy) * 100;
    document.getElementById("player-health-fill").style.width =
      playerHealthPercent + "%";
    document.getElementById("player-energy-fill").style.width =
      playerEnergyPercent + "%";

    // Update enemy stats
    document.getElementById("enemy-name").textContent = this.enemy.name;
    document.getElementById("enemy-avatar").textContent = this.enemy.avatar;
    document.getElementById("enemy-health-text").textContent =
      this.enemy.health + "/" + this.enemy.maxHealth;
    document.getElementById("enemy-energy-text").textContent =
      this.enemy.energy + "/" + this.enemy.maxEnergy;

    const enemyHealthPercent = (this.enemy.health / this.enemy.maxHealth) * 100;
    const enemyEnergyPercent = (this.enemy.energy / this.enemy.maxEnergy) * 100;
    document.getElementById("enemy-health-fill").style.width =
      enemyHealthPercent + "%";
    document.getElementById("enemy-energy-fill").style.width =
      enemyEnergyPercent + "%";

    // Update turn indicator
    document.getElementById("combat-turn").textContent =
      "Sıra: " + (this.turn === "player" ? "Oyuncu" : "Düşman");

    // Generate combat actions
    this.generateCombatActions();

    // Update log
    this.updateCombatLog();
  },

  // Generate combat action buttons
  generateCombatActions: function () {
    const actionGrid = document.getElementById("combat-action-grid");
    actionGrid.innerHTML = "";

    if (this.turn === "player") {
      // Get current character class and race
      const selectedRace = document.querySelector(
        ".race-class-list:nth-child(1) .list-item.selected"
      );
      const selectedClass = document.querySelector(
        ".race-class-list:nth-child(2) .list-item.selected"
      );

      const characterRace = selectedRace
        ? selectedRace.textContent.trim().toLowerCase()
        : "";
      const characterClass = selectedClass
        ? selectedClass.textContent.trim().toLowerCase()
        : "";

      console.log("🎭 Combat for character:", {
        race: characterRace,
        class: characterClass,
      });

      // Get current level for skill requirements
      const currentLevel = parseInt(document.getElementById("character-level").textContent) || 1;

      // Base actions based on character class with level requirements
      let actions = [];

      // === FANTASY THEME CLASSES ===
      if (
        characterClass.includes("savaşçı") ||
        characterClass.includes("warrior")
      ) {
        actions = [
          {
            name: "🗡️ Kılıç Saldırısı",
            damage: 15,
            energy: 10,
            type: "attack",
            levelRequired: 1,
            classRequired: "warrior"
          },
          { 
            name: "🛡️ Kalkan Savunması", 
            damage: 0, 
            energy: 5, 
            type: "defend",
            levelRequired: 1,
            classRequired: "warrior"
          },
          { 
            name: "⚡ Hızlı Saldırı", 
            damage: 8, 
            energy: 5, 
            type: "quick",
            levelRequired: 2,
            classRequired: "warrior"
          },
          {
            name: "😤 Öfke Saldırısı",
            damage: 25,
            energy: 20,
            type: "attack",
            levelRequired: 3,
            classRequired: "warrior"
          }
        ];
      }
      // Mage class actions
      else if (
        characterClass.includes("büyücü") ||
        characterClass.includes("mage")
      ) {
        actions = [
          { 
            name: "🔮 Ateş Topu", 
            damage: 25, 
            energy: 20, 
            type: "magic",
            levelRequired: 1,
            classRequired: "mage"
          },
          { 
            name: "❄️ Buz Kalkanı", 
            damage: 0, 
            energy: 15, 
            type: "defend",
            levelRequired: 2,
            classRequired: "mage"
          },
          { 
            name: "⚡ Yıldırım", 
            damage: 30, 
            energy: 25, 
            type: "magic",
            levelRequired: 3,
            classRequired: "mage"
          },
          {
            name: "🌪️ Kasırga",
            damage: 35,
            energy: 30,
            type: "magic",
            levelRequired: 4,
            classRequired: "mage"
          }
        ];
      }
      // Rogue class actions
      else if (
        characterClass.includes("hırsız") ||
        characterClass.includes("rogue")
      ) {
        actions = [
          { 
            name: "🗡️ Sırtından Vur", 
            damage: 20, 
            energy: 8, 
            type: "attack",
            levelRequired: 1,
            classRequired: "rogue"
          },
          { 
            name: "👤 Gizlen", 
            damage: 0, 
            energy: 5, 
            type: "stealth",
            levelRequired: 2,
            classRequired: "rogue"
          },
          { 
            name: "☠️ Zehirli Bıçak", 
            damage: 12, 
            energy: 10, 
            type: "attack",
            levelRequired: 2,
            classRequired: "rogue"
          },
          {
            name: "🎯 Kritik Vuruş",
            damage: 40,
            energy: 25,
            type: "attack",
            levelRequired: 3,
            classRequired: "rogue"
          }
        ];
      }

      // === SCI-FI THEME CLASSES ===
      else if (
        characterClass.includes("astronot") ||
        characterClass.includes("astronaut")
      ) {
        actions = [
          { name: "🔫 Lazer Silahı", damage: 18, energy: 12, type: "ranged" },
          {
            name: "🛡️ Kalkan Jeneratörü",
            damage: 0,
            energy: 8,
            type: "defend",
          },
          { name: "⚡ Hızlı Atış", damage: 10, energy: 6, type: "ranged" },
        ];
      } else if (
        characterClass.includes("mühendis") ||
        characterClass.includes("engineer")
      ) {
        actions = [
          { name: "🔧 Drone Saldırısı", damage: 22, energy: 15, type: "tech" },
          {
            name: "🛡️ Teknoloji Kalkanı",
            damage: 0,
            energy: 10,
            type: "defend",
          },
          { name: "⚡ Sistem Hack", damage: 16, energy: 12, type: "tech" },
        ];
      } else if (
        characterClass.includes("doktor") ||
        characterClass.includes("doctor")
      ) {
        actions = [
          {
            name: "💉 Nanobot Saldırısı",
            damage: 20,
            energy: 14,
            type: "tech",
          },
          { name: "🛡️ Medikal Kalkan", damage: 0, energy: 8, type: "defend" },
          {
            name: "⚡ Hızlı İyileştirme",
            damage: -15,
            energy: 12,
            type: "heal",
          },
        ];
      }

      // === CYBERPUNK THEME CLASSES ===
      else if (
        characterClass.includes("netrunner") ||
        characterClass.includes("hacker")
      ) {
        actions = [
          { name: "💻 Sistem Hack", damage: 24, energy: 16, type: "cyber" },
          { name: "🛡️ Dijital Kalkan", damage: 0, energy: 10, type: "defend" },
          { name: "⚡ Hızlı Hack", damage: 14, energy: 8, type: "cyber" },
        ];
      } else if (
        characterClass.includes("street") ||
        characterClass.includes("gangster")
      ) {
        actions = [
          { name: "🔫 Tabanca Atışı", damage: 16, energy: 10, type: "ranged" },
          { name: "🛡️ Sokak Savunması", damage: 0, energy: 6, type: "defend" },
          { name: "⚡ Hızlı Çekim", damage: 12, energy: 7, type: "ranged" },
        ];
      } else if (
        characterClass.includes("corporate") ||
        characterClass.includes("executive")
      ) {
        actions = [
          { name: "💰 Para Gücü", damage: 26, energy: 18, type: "social" },
          {
            name: "🛡️ Güvenlik Kalkanı",
            damage: 0,
            energy: 12,
            type: "defend",
          },
          {
            name: "⚡ Hızlı Satın Alma",
            damage: 18,
            energy: 14,
            type: "social",
          },
        ];
      }

      // === WARHAMMER THEME CLASSES ===
      else if (
        characterClass.includes("space marine") ||
        characterClass.includes("astartes")
      ) {
        actions = [
          { name: "🔫 Bolter Atışı", damage: 28, energy: 20, type: "ranged" },
          { name: "🛡️ Power Armor", damage: 0, energy: 15, type: "defend" },
          { name: "⚡ Chainsword", damage: 22, energy: 12, type: "melee" },
        ];
      } else if (
        characterClass.includes("inquisitor") ||
        characterClass.includes("sorgulayıcı")
      ) {
        actions = [
          {
            name: "⚡ Psikik Saldırı",
            damage: 30,
            energy: 22,
            type: "psychic",
          },
          { name: "🛡️ İnanç Kalkanı", damage: 0, energy: 12, type: "defend" },
          { name: "⚡ Hızlı Yargı", damage: 20, energy: 15, type: "psychic" },
        ];
      } else if (
        characterClass.includes("tech-priest") ||
        characterClass.includes("teknisyen")
      ) {
        actions = [
          { name: "🔧 Mekanik Saldırı", damage: 24, energy: 16, type: "tech" },
          {
            name: "🛡️ Teknoloji Kalkanı",
            damage: 0,
            energy: 10,
            type: "defend",
          },
          { name: "⚡ Hızlı Tamir", damage: -18, energy: 14, type: "heal" },
        ];
      }

      // Default actions for unknown class
      else {
        actions = [
          { name: "👊 Yumruk", damage: 10, energy: 5, type: "attack" },
          { name: "🛡️ Savunma", damage: 0, energy: 3, type: "defend" },
        ];
      }

      // === RACE-SPECIFIC ACTIONS FOR ALL THEMES ===

      // Fantasy Races
      if (characterRace.includes("elf")) {
        actions.push({
          name: "🌿 Doğa Büyüsü",
          damage: 18,
          energy: 12,
          type: "magic",
        });
      } else if (characterRace.includes("cüce")) {
        actions.push({
          name: "🔨 Çekiç Vuruşu",
          damage: 22,
          energy: 15,
          type: "attack",
        });
      } else if (characterRace.includes("ork")) {
        actions.push({
          name: "😤 Öfke Saldırısı",
          damage: 25,
          energy: 20,
          type: "attack",
        });
      }

      // Sci-Fi Races
      else if (
        characterRace.includes("android") ||
        characterRace.includes("robot")
      ) {
        actions.push({
          name: "🤖 Sistem Override",
          damage: 20,
          energy: 14,
          type: "tech",
        });
      } else if (
        characterRace.includes("alien") ||
        characterRace.includes("uzaylı")
      ) {
        actions.push({
          name: "👽 Telepatik Saldırı",
          damage: 24,
          energy: 16,
          type: "psychic",
        });
      } else if (
        characterRace.includes("mutant") ||
        characterRace.includes("mutasyon")
      ) {
        actions.push({
          name: "🧬 Mutasyon Gücü",
          damage: 26,
          energy: 18,
          type: "special",
        });
      }

      // Cyberpunk Races
      else if (
        characterRace.includes("cyborg") ||
        characterRace.includes("yarı robot")
      ) {
        actions.push({
          name: "🔧 Siber Saldırı",
          damage: 22,
          energy: 15,
          type: "cyber",
        });
      } else if (
        characterRace.includes("enhanced") ||
        characterRace.includes("geliştirilmiş")
      ) {
        actions.push({
          name: "💊 Stim Saldırısı",
          damage: 28,
          energy: 20,
          type: "enhanced",
        });
      } else if (
        characterRace.includes("baseline") ||
        characterRace.includes("normal")
      ) {
        actions.push({
          name: "👊 İnsan Gücü",
          damage: 16,
          energy: 10,
          type: "melee",
        });
      }

      // Warhammer Races
      else if (
        characterRace.includes("human") ||
        characterRace.includes("insan")
      ) {
        actions.push({
          name: "⚡ İnsan Azmi",
          damage: 18,
          energy: 12,
          type: "melee",
        });
      } else if (
        characterRace.includes("eldar") ||
        characterRace.includes("elf")
      ) {
        actions.push({
          name: "🔮 Psikik Güç",
          damage: 26,
          energy: 18,
          type: "psychic",
        });
      } else if (
        characterRace.includes("ork") ||
        characterRace.includes("yeşil")
      ) {
        actions.push({
          name: "💪 Ork Gücü",
          damage: 30,
          energy: 22,
          type: "melee",
        });
      }

      // Universal consumables (available to all)
      actions.push(
        { name: "💊 Can İksiri", damage: -20, energy: 15, type: "heal" },
        { name: "⚡ Enerji İksiri", damage: 0, energy: -15, type: "energy" }
      );

      // Add unlocked skills to combat actions (filtered by character class)
      if (window.skillSystem && window.skillSystem.progression) {
        const unlockedSkills =
          window.skillSystem.progression.unlocked_skills || [];

        unlockedSkills.forEach((skillId) => {
          const skill = window.skillSystem.availableSkills.find(
            (s) => s.id === skillId
          );

          if (!skill) return;

          // Skill'i karakter sınıfına göre filtrele
          const skillRequirements = skill.requirements || {};
          const requiredClass = skillRequirements.class;
          const requiredRace = skillRequirements.race;

          // Eğer skill'in sınıf gereksinimi varsa ve karakter uymuyorsa, atla
          if (
            requiredClass &&
            !characterClass.includes(requiredClass.toLowerCase())
          ) {
            console.log(
              `❌ Skill ${skill.name} sınıf uyumsuzluğu: ${requiredClass} gerekli, ${characterClass} mevcut`
            );
            return;
          }

          // Eğer skill'in ırk gereksinimi varsa ve karakter uymuyorsa, atla
          if (
            requiredRace &&
            !characterRace.includes(requiredRace.toLowerCase())
          ) {
            console.log(
              `❌ Skill ${skill.name} ırk uyumsuzluğu: ${requiredRace} gerekli, ${characterRace} mevcut`
            );
            return;
          }

          // Combat skill'lerini ekle
          if (
            skill.type === "combat" ||
            skill.type === "magic" ||
            skill.type === "stealth" ||
            skill.type === "ultimate" ||
            skill.type === "tech" ||
            skill.type === "cyber" ||
            skill.type === "psychic" ||
            skill.type === "ranged" ||
            skill.type === "melee" ||
            skill.type === "social" ||
            skill.type === "enhanced"
          ) {
            const skillLevel =
              window.skillSystem.progression.skill_levels[skillId] || 1;
            let damage = skill.effects?.damage || 0;
            let energy = skill.effects?.energy_cost || 10;
            let mana = skill.effects?.mana_cost || 0;

            // Calculate skill effects based on level
            if (skill.progression && skill.progression.bonus_per_level) {
              const levelBonus =
                skill.progression.bonus_per_level[skillLevel - 1] || 0;
              damage += levelBonus;
            }

            console.log(
              `✅ Combat skill eklendi: ${skill.name} (${skill.type})`
            );
            actions.push({
              name: skill.name,
              damage: damage,
              energy: energy,
              mana: mana,
              type: "skill",
              skillId: skillId,
              skillType: skill.type,
              effects: skill.effects,
            });
          }
        });
      }

      actions.forEach((action) => {
        const button = document.createElement("button");
        button.className = "combat-action-btn";
        
        // Check if action is locked based on level and class requirements
        const isLocked = (action.levelRequired && action.levelRequired > currentLevel) || 
                        (action.classRequired && !characterClass.includes(action.classRequired.toLowerCase()));
        
        if (isLocked) {
          button.className += " locked";
          button.disabled = true;
        } else {
          button.disabled = this.player.energy < action.energy;
        }

        let buttonText = action.name;
        if (action.damage > 0) {
          buttonText += `<span class="action-damage">-${action.damage} HP</span>`;
        } else if (action.damage < 0) {
          buttonText += `<span class="action-heal">+${Math.abs(
            action.damage
          )} HP</span>`;
        }
        buttonText += `<span class="action-energy">-${action.energy} E</span>`;
        
        if (isLocked) {
          buttonText += `<span class="lock-reason">${action.levelRequired ? 'Seviye ' + action.levelRequired + ' gerekli' : 'Sınıf uyumsuzluğu'}</span>`;
        }

        button.innerHTML = buttonText;
        if (!isLocked) {
          button.onclick = () => this.performAction(action);
        }
        actionGrid.appendChild(button);
      });
    } else {
      // Enemy turn - show waiting message
      const waitingDiv = document.createElement("div");
      waitingDiv.className = "combat-action-btn";
      waitingDiv.style.textAlign = "center";
      waitingDiv.textContent = "Düşman düşünüyor...";
      actionGrid.appendChild(waitingDiv);

      // Simulate enemy action after 2 seconds
      setTimeout(() => this.performEnemyAction(), 2000);
    }
  },

  // Perform player action
  performAction: function (action) {
    if (this.player.energy < action.energy) {
      this.addLogEntry("❌ Yeterli enerjin yok!");
      return;
    }

    // Consume energy
    this.player.energy -= action.energy;

    // Apply action effects
    if (
      action.type === "attack" ||
      action.type === "quick" ||
      action.type === "magic"
    ) {
      // Attack enemy
      this.enemy.health = Math.max(0, this.enemy.health - action.damage);
      this.addLogEntry(`🗡️ ${action.name} ile ${action.damage} hasar verdin!`);
    } else if (action.type === "skill") {
      // Use skill with new system
      if (action.skillId && window.useSkill) {
        const skillResult = window.useSkill(action.skillId);
        if (skillResult && skillResult.damage) {
          this.enemy.health = Math.max(
            0,
            this.enemy.health - skillResult.damage
          );
          this.addLogEntry(
            `⚔️ ${action.name} ile ${skillResult.damage} hasar verdin!`
          );
        }
        if (skillResult && skillResult.healing) {
          this.player.health = Math.min(
            this.player.maxHealth,
            this.player.health + skillResult.healing
          );
          this.addLogEntry(
            `💚 ${action.name} ile ${skillResult.healing} can iyileştirdin!`
          );
        }
        if (skillResult && skillResult.energy_restore) {
          this.player.energy = Math.min(
            this.player.maxEnergy,
            this.player.energy + skillResult.energy_restore
          );
          this.addLogEntry(`⚡ ${action.name} ile enerjini yeniledin!`);
        }
      } else {
        // Fallback for skill actions
        this.enemy.health = Math.max(0, this.enemy.health - action.damage);
        this.addLogEntry(
          `⚔️ ${action.name} ile ${action.damage} hasar verdin!`
        );
      }
    } else if (action.type === "heal") {
      // Heal player
      this.player.health = Math.min(
        this.player.maxHealth,
        this.player.health - action.damage
      );
      this.addLogEntry(`💊 ${Math.abs(action.damage)} can iyileştirdin!`);
    } else if (action.type === "energy") {
      // Restore energy
      this.player.energy = Math.min(
        this.player.maxEnergy,
        this.player.energy - action.damage
      );
      this.addLogEntry(`⚡ Enerjini yeniledin!`);
    }

    // Check if enemy is defeated
    if (this.enemy.health <= 0) {
      this.endCombat("victory");
      return;
    }

    // Switch to enemy turn
    this.turn = "enemy";
    this.updateCombatUI();
  },

  // Perform enemy action
  performEnemyAction: function () {
    // Get player level for scaling
    let playerLevel = 1;
    try {
      if (window.skillSystem && window.skillSystem.progression) {
        playerLevel = window.skillSystem.progression.level || 1;
      }
    } catch (e) {
      console.warn("⚠️ Could not get player level for enemy scaling:", e);
    }
    
    // Scale enemy actions based on player level and enemy type
    const enemyName = (this.enemy.name || "").toLowerCase();
    let baseDamage = 12;
    let baseEnergy = 8;
    
    // FANTASY THEME ENEMIES
    if (enemyName.includes("ejderha") || enemyName.includes("dragon")) {
      baseDamage = 25 + (playerLevel * 3);
      baseEnergy = 15;
      const actions = [
        { name: "🔥 Alev Nefesi", damage: baseDamage, energy: baseEnergy },
        { name: "🦷 Diş Saldırısı", damage: baseDamage * 0.8, energy: baseEnergy * 0.6 },
        { name: "🛡️ Pulluk Savunma", damage: 0, energy: 5 },
        { name: "⚡ Kanat Vuruşu", damage: baseDamage * 0.7, energy: baseEnergy * 0.5 },
      ];
      const action = actions[Math.floor(Math.random() * actions.length)];
      this.executeEnemyAction(action);
    } else if (enemyName.includes("şifacı") || enemyName.includes("healer")) {
      baseDamage = 18 + (playerLevel * 2);
      baseEnergy = 12;
      const actions = [
        { name: "🔮 Büyü Saldırısı", damage: baseDamage, energy: baseEnergy },
        { name: "💊 İyileştirme", damage: -15, energy: 10 },
        { name: "🛡️ Büyü Kalkanı", damage: 0, energy: 8 },
        { name: "⚡ Yıldırım", damage: baseDamage * 0.9, energy: baseEnergy * 0.8 },
      ];
      const action = actions[Math.floor(Math.random() * actions.length)];
      this.executeEnemyAction(action);
    } else if (enemyName.includes("haydut") || enemyName.includes("bandit")) {
      baseDamage = 15 + (playerLevel * 1.5);
      baseEnergy = 10;
      const actions = [
        { name: "🗡️ Kılıç Saldırısı", damage: baseDamage, energy: baseEnergy },
        { name: "🏹 Ok Atışı", damage: baseDamage * 0.8, energy: baseEnergy * 0.7 },
        { name: "🛡️ Kalkan Savunması", damage: 0, energy: 6 },
        { name: "⚡ Hızlı Saldırı", damage: baseDamage * 0.6, energy: baseEnergy * 0.5 },
      ];
      const action = actions[Math.floor(Math.random() * actions.length)];
      this.executeEnemyAction(action);
    } else if (enemyName.includes("kurt") || enemyName.includes("wolf")) {
      baseDamage = 12 + (playerLevel * 1.2);
      baseEnergy = 8;
      const actions = [
        { name: "🦷 Diş Saldırısı", damage: baseDamage, energy: baseEnergy },
        { name: "⚡ Hızlı Koşu", damage: baseDamage * 0.7, energy: baseEnergy * 0.6 },
        { name: "🛡️ Sürü Savunması", damage: 0, energy: 5 },
        { name: "🐺 Uluma", damage: baseDamage * 0.5, energy: baseEnergy * 0.4 },
      ];
      const action = actions[Math.floor(Math.random() * actions.length)];
      this.executeEnemyAction(action);
    } else if (enemyName.includes("yaratık") || enemyName.includes("creature")) {
      baseDamage = 14 + (playerLevel * 1.3);
      baseEnergy = 9;
      const actions = [
        { name: "🦊 Pençe Saldırısı", damage: baseDamage, energy: baseEnergy },
        { name: "🌲 Orman Gücü", damage: baseDamage * 0.9, energy: baseEnergy * 0.8 },
        { name: "🛡️ Doğal Savunma", damage: 0, energy: 6 },
        { name: "⚡ Hızlı Kaçış", damage: baseDamage * 0.6, energy: baseEnergy * 0.5 },
      ];
      const action = actions[Math.floor(Math.random() * actions.length)];
      this.executeEnemyAction(action);
    } else if (enemyName.includes("muhafız") || enemyName.includes("guard")) {
      baseDamage = 16 + (playerLevel * 1.4);
      baseEnergy = 11;
      const actions = [
        { name: "⚔️ Kılıç Saldırısı", damage: baseDamage, energy: baseEnergy },
        { name: "🛡️ Kalkan Savunması", damage: 0, energy: 7 },
        { name: "🏹 Mızrak Atışı", damage: baseDamage * 0.8, energy: baseEnergy * 0.7 },
        { name: "⚡ Disiplinli Saldırı", damage: baseDamage * 0.7, energy: baseEnergy * 0.6 },
      ];
      const action = actions[Math.floor(Math.random() * actions.length)];
      this.executeEnemyAction(action);
    }
    // SCI-FI THEME ENEMIES
    else if (enemyName.includes("robot") || enemyName.includes("bot")) {
      baseDamage = 20 + (playerLevel * 2.5);
      baseEnergy = 15;
      const actions = [
        { name: "🔫 Lazer Atışı", damage: baseDamage, energy: baseEnergy },
        { name: "⚡ Elektrik Şoku", damage: baseDamage * 0.9, energy: baseEnergy * 0.8 },
        { name: "🛡️ Metal Kalkan", damage: 0, energy: 8 },
        { name: "🔧 Sistem Tamiri", damage: -20, energy: 12 },
      ];
      const action = actions[Math.floor(Math.random() * actions.length)];
      this.executeEnemyAction(action);
    } else if (enemyName.includes("mutant") || enemyName.includes("mutant")) {
      baseDamage = 22 + (playerLevel * 2.2);
      baseEnergy = 14;
      const actions = [
        { name: "🧬 Mutasyon Saldırısı", damage: baseDamage, energy: baseEnergy },
        { name: "🦠 Biyolojik Silah", damage: baseDamage * 0.9, energy: baseEnergy * 0.8 },
        { name: "🛡️ Organik Kalkan", damage: 0, energy: 7 },
        { name: "⚡ Hızlı Rejenerasyon", damage: -15, energy: 10 },
      ];
      const action = actions[Math.floor(Math.random() * actions.length)];
      this.executeEnemyAction(action);
    } else if (enemyName.includes("ai") || enemyName.includes("collective")) {
      baseDamage = 28 + (playerLevel * 3.5);
      baseEnergy = 20;
      const actions = [
        { name: "🤖 AI Saldırısı", damage: baseDamage, energy: baseEnergy },
        { name: "🔮 Hologram Saldırısı", damage: baseDamage * 0.8, energy: baseEnergy * 0.7 },
        { name: "🛡️ Dijital Kalkan", damage: 0, energy: 10 },
        { name: "⚡ Sistem Hack'i", damage: baseDamage * 0.6, energy: baseEnergy * 0.5 },
      ];
      const action = actions[Math.floor(Math.random() * actions.length)];
      this.executeEnemyAction(action);
    }
    // CYBERPUNK THEME ENEMIES
    else if (enemyName.includes("gangster") || enemyName.includes("gang")) {
      baseDamage = 18 + (playerLevel * 1.8);
      baseEnergy = 12;
      const actions = [
        { name: "🔫 Silah Atışı", damage: baseDamage, energy: baseEnergy },
        { name: "⚡ Hızlı Saldırı", damage: baseDamage * 0.8, energy: baseEnergy * 0.7 },
        { name: "🛡️ Gizlenme", damage: 0, energy: 6 },
        { name: "💊 Stim Saldırısı", damage: baseDamage * 0.9, energy: baseEnergy * 0.8 },
      ];
      const action = actions[Math.floor(Math.random() * actions.length)];
      this.executeEnemyAction(action);
    } else if (enemyName.includes("cyber") || enemyName.includes("psycho")) {
      baseDamage = 25 + (playerLevel * 2.8);
      baseEnergy = 16;
      const actions = [
        { name: "🔧 Cyber Saldırısı", damage: baseDamage, energy: baseEnergy },
        { name: "⚡ Neural Hack", damage: baseDamage * 0.9, energy: baseEnergy * 0.8 },
        { name: "🛡️ Cyber Kalkan", damage: 0, energy: 9 },
        { name: "💊 Rage Mode", damage: baseDamage * 1.2, energy: baseEnergy * 1.1 },
      ];
      const action = actions[Math.floor(Math.random() * actions.length)];
      this.executeEnemyAction(action);
    } else if (enemyName.includes("corporate") || enemyName.includes("corp")) {
      baseDamage = 20 + (playerLevel * 2.0);
      baseEnergy = 13;
      const actions = [
        { name: "💼 Corporate Saldırısı", damage: baseDamage, energy: baseEnergy },
        { name: "🔫 Precision Shot", damage: baseDamage * 0.9, energy: baseEnergy * 0.8 },
        { name: "🛡️ Tactical Shield", damage: 0, energy: 8 },
        { name: "⚡ Tactical Strike", damage: baseDamage * 0.8, energy: baseEnergy * 0.7 },
      ];
      const action = actions[Math.floor(Math.random() * actions.length)];
      this.executeEnemyAction(action);
    } else {
      // Default enemy actions (scaled with level)
      baseDamage = 12 + (playerLevel * 1.2);
      baseEnergy = 8 + (playerLevel * 0.5);
      const actions = [
        { name: "🗡️ Saldırı", damage: baseDamage, energy: baseEnergy },
        { name: "🛡️ Savunma", damage: 0, energy: 5 },
        { name: "⚡ Hızlı Saldırı", damage: baseDamage * 0.7, energy: baseEnergy * 0.6 },
      ];
      const action = actions[Math.floor(Math.random() * actions.length)];
      this.executeEnemyAction(action);
    }
  },

  // Execute enemy action
  executeEnemyAction: function (action) {
    if (this.enemy.energy >= action.energy) {
      this.enemy.energy -= action.energy;

      if (action.damage > 0) {
        this.player.health = Math.max(0, this.player.health - action.damage);
        this.addLogEntry(
          `👹 ${this.enemy.name} ${action.name} ile ${action.damage} hasar verdi!`
        );
      } else if (action.damage < 0) {
        // Enemy healing
        this.enemy.health = Math.min(
          this.enemy.maxHealth,
          this.enemy.health - action.damage
        );
        this.addLogEntry(`💚 ${this.enemy.name} ${Math.abs(action.damage)} can iyileştirdi!`);
      } else {
        this.addLogEntry(`🛡️ ${this.enemy.name} savunmaya geçti!`);
      }
    } else {
      this.addLogEntry(`⚡ ${this.enemy.name} enerjisini yeniledi!`);
      this.enemy.energy = Math.min(
        this.enemy.maxEnergy,
        this.enemy.energy + 15
      );
    }

    // Check if player is defeated
    if (this.player.health <= 0) {
      this.endCombat("defeat");
      return;
    }

    // Switch to player turn
    this.turn = "player";
    this.updateCombatUI();
  },

  // End combat
  endCombat: function (result) {
    this.isActive = false;

    if (result === "victory") {
      this.addLogEntry("🎉 Zafer! Düşmanı yendin!");
      try {
        recordFightWin(window.currentScenarioId);
      } catch (_) {}
      
      // Calculate XP reward based on enemy difficulty and theme
      let xpReward = 25; // Base XP
      const enemyName = (this.enemy.name || "").toLowerCase();
      const scenarioId = (window.currentScenarioId || "").toLowerCase();
      
      // FANTASY THEME XP REWARDS
      if (scenarioId.includes("dragon") || scenarioId.includes("forest")) {
        if (enemyName.includes("ejderha") || enemyName.includes("dragon")) {
          xpReward = 150;
        } else if (enemyName.includes("şifacı") || enemyName.includes("healer")) {
          xpReward = 100;
        } else if (enemyName.includes("haydut") || enemyName.includes("bandit")) {
          xpReward = 50;
        } else if (enemyName.includes("kurt") || enemyName.includes("wolf")) {
          xpReward = 30;
        } else if (enemyName.includes("yaratık") || enemyName.includes("creature")) {
          xpReward = 40;
        } else if (enemyName.includes("muhafız") || enemyName.includes("guard")) {
          xpReward = 60;
        }
      }
      // SCI-FI THEME XP REWARDS
      else if (scenarioId.includes("hive")) {
        if (enemyName.includes("ai") || enemyName.includes("collective")) {
          xpReward = 200;
        } else if (enemyName.includes("robot") || enemyName.includes("bot")) {
          xpReward = 75;
        } else if (enemyName.includes("mutant") || enemyName.includes("mutant")) {
          xpReward = 90;
        } else if (enemyName.includes("güvenlik") || enemyName.includes("security")) {
          xpReward = 45;
        } else if (enemyName.includes("veri") || enemyName.includes("data")) {
          xpReward = 55;
        }
      }
      // CYBERPUNK THEME XP REWARDS
      else if (scenarioId.includes("cyberpunk")) {
        if (enemyName.includes("ai") || enemyName.includes("system")) {
          xpReward = 180;
        } else if (enemyName.includes("cyber") || enemyName.includes("psycho")) {
          xpReward = 120;
        } else if (enemyName.includes("gangster") || enemyName.includes("gang")) {
          xpReward = 65;
        } else if (enemyName.includes("corporate") || enemyName.includes("corp")) {
          xpReward = 80;
        } else if (enemyName.includes("güvenlik") || enemyName.includes("security")) {
          xpReward = 50;
        }
      }
      
      // Award XP and show level up notification
      try {
        if (window.gainXP) {
          window.gainXP(xpReward);
          this.addLogEntry(`⭐ ${xpReward} XP kazandın!`);
        }
      } catch (e) {
        console.warn("⚠️ Could not award XP:", e);
      }
      
      // Mark context-sensitive quest actions as completed based on active enemy/scenario
      try {
        if (
          window.npcSystem &&
          typeof window.npcSystem.completeQuestAction === "function"
        ) {
          // Healer-related combat in dragon scenario
          if (
            scenarioId.includes("dragon") &&
            (enemyName.includes("şifacı") || enemyName.includes("healer"))
          ) {
            window.npcSystem.completeQuestAction(
              "investigate_healer",
              "prepare_combat_healer"
            );
          }
          // AI or external threat combats in other scenarios could be wired similarly later
        }
      } catch (e) {
        console.warn("⚠️ Quest hook after combat skipped:", e);
      }
      
      setTimeout(() => {
        const combatEl = document.getElementById("combat-section");
        const storyEl = document.getElementById("story-text");
        const choicesEl = document.getElementById("choices-section");
        if (combatEl) combatEl.style.display = "none";
        if (storyEl) storyEl.style.display = "block";
        if (choicesEl) choicesEl.style.display = "block";
        
        // Continue story after combat
        window.displayStoryNode({
          title: "Savaş Sonrası",
          description: `Düşmanı yendin ve ${xpReward} XP kazandın! Hikaye devam ediyor...`,
          choices: [{ text: "Devam et", nextNode: "continue_after_combat" }],
        });
      }, 2000);
    } else {
      this.addLogEntry("💀 Yenildin! Savaş kaybedildi!");
      setTimeout(() => {
        const combatEl = document.getElementById("combat-section");
        const storyEl = document.getElementById("story-text");
        const choicesEl = document.getElementById("choices-section");
        if (combatEl) combatEl.style.display = "none";
        if (storyEl) storyEl.style.display = "block";
        if (choicesEl) choicesEl.style.display = "block";
        
        // Game over or restart
        window.displayStoryNode({
          title: "Savaş Sonrası",
          description: "Savaşta yenildin. Tekrar dene!",
          choices: [{ text: "Tekrar dene", nextNode: "restart_after_defeat" }],
        });
      }, 2000);
    }
  },

  // Add log entry
  addLogEntry: function (message) {
    this.log.push({
      message: message,
      timestamp: new Date().toLocaleTimeString(),
    });

    // Keep only last 10 entries
    if (this.log.length > 10) {
      this.log.shift();
    }

    this.updateCombatLog();
  },

  // Update combat log display
  updateCombatLog: function () {
    const logContainer = document.getElementById("combat-log-container");
    logContainer.innerHTML = "";

    this.log.forEach((entry) => {
      const logEntry = document.createElement("div");
      logEntry.className = "log-entry";
      logEntry.innerHTML = `<span class="log-time">[${entry.timestamp}]</span> ${entry.message}`;
      logContainer.appendChild(logEntry);
    });

    // Scroll to bottom
    logContainer.scrollTop = logContainer.scrollHeight;
  },
};

// AUTO-TRIGGER COMBAT FUNCTION
window.autoTriggerCombat = function (scenarioId, nodeId, nodeTitle) {
  try {
    console.log("⚔️ Checking for combat trigger:", {
      scenarioId,
      nodeId,
      nodeTitle,
    });

    // Check if this node should trigger combat
    const isCombatNode =
      nodeId.includes("fight") ||
      nodeId.includes("attack") ||
      nodeId.includes("combat") ||
      nodeId.includes("battle") ||
      nodeTitle.includes("Savaş") ||
      nodeTitle.includes("Saldır") ||
      nodeTitle.includes("Dövüş");

    if (isCombatNode && window.combatSystem && !window.combatSystem.isActive) {
      console.log("⚔️ Combat triggered for node:", nodeId);

      // Define enemies based on scenario and specific node
      let enemyData = {
        name: "Bilinmeyen Düşman",
        health: 100,
        maxHealth: 100,
        energy: 50,
        maxEnergy: 50,
        avatar: "👹",
      };

      // FANTASY THEME - Dragon Hunters Path enemies
      if (scenarioId === "dragon_hunters_path") {
        if (nodeId.includes("healer") || nodeTitle.includes("Şifacı")) {
          enemyData = {
            name: "Şifacı",
            health: 120,
            maxHealth: 120,
            energy: 80,
            maxEnergy: 80,
            avatar: "🧙‍♂️",
          };
        } else if (nodeId.includes("dragon") || nodeTitle.includes("Ejderha")) {
          enemyData = {
            name: "Kızıl Ejderha",
            health: 300,
            maxHealth: 300,
            energy: 100,
            maxEnergy: 100,
            avatar: "🐉",
          };
        } else if (nodeId.includes("father") || nodeTitle.includes("Baba")) {
          enemyData = {
            name: "Lydia'nın Babası",
            health: 150,
            maxHealth: 150,
            energy: 60,
            maxEnergy: 60,
            avatar: "👨‍🦳",
          };
        } else if (nodeId.includes("bandit") || nodeTitle.includes("Haydut")) {
          enemyData = {
            name: "Haydut Çetesi",
            health: 80,
            maxHealth: 80,
            energy: 50,
            maxEnergy: 50,
            avatar: "🗡️",
          };
        } else if (nodeId.includes("wolf") || nodeTitle.includes("Kurt")) {
          enemyData = {
            name: "Kurt Sürüsü",
            health: 60,
            maxHealth: 60,
            energy: 40,
            maxEnergy: 40,
            avatar: "🐺",
          };
        } else if (nodeId.includes("temple") || nodeTitle.includes("Tapınak")) {
          enemyData = {
            name: "Tapınak Muhafızı",
            health: 100,
            maxHealth: 100,
            energy: 70,
            maxEnergy: 70,
            avatar: "⚔️",
          };
        } else if (nodeId.includes("cave") || nodeTitle.includes("Mağara")) {
          enemyData = {
            name: "Mağara Yaratığı",
            health: 90,
            maxHealth: 90,
            energy: 55,
            maxEnergy: 55,
            avatar: "🦇",
          };
        } else if (nodeId.includes("forest") || nodeTitle.includes("Orman")) {
          enemyData = {
            name: "Orman Yaratığı",
            health: 70,
            maxHealth: 70,
            energy: 45,
            maxEnergy: 45,
            avatar: "🦊",
          };
        }
      }
      // FANTASY THEME - Magical Forest Mysteries enemies
      else if (scenarioId === "magical_forest_mysteries") {
        if (nodeId.includes("malakar") || nodeTitle.includes("Malakar")) {
          enemyData = {
            name: "Malakar",
            health: 180,
            maxHealth: 180,
            energy: 90,
            maxEnergy: 90,
            avatar: "🧙‍♂️",
          };
        } else if (nodeId.includes("forest") || nodeTitle.includes("Orman")) {
          enemyData = {
            name: "Orman Yaratığı",
            health: 140,
            maxHealth: 140,
            energy: 70,
            maxEnergy: 70,
            avatar: "🌲",
          };
        } else if (nodeId.includes("spirit") || nodeTitle.includes("Ruh")) {
          enemyData = {
            name: "Orman Ruhu",
            health: 160,
            maxHealth: 160,
            energy: 80,
            maxEnergy: 80,
            avatar: "👻",
          };
        } else if (nodeId.includes("creature") || nodeTitle.includes("Yaratık")) {
          enemyData = {
            name: "Orman Yaratığı",
            health: 120,
            maxHealth: 120,
            energy: 60,
            maxEnergy: 60,
            avatar: "🦊",
          };
        } else if (nodeId.includes("trap") || nodeTitle.includes("Tuzak")) {
          enemyData = {
            name: "Büyülü Tuzak",
            health: 80,
            maxHealth: 80,
            energy: 50,
            maxEnergy: 50,
            avatar: "⚡",
          };
        } else if (nodeId.includes("ruins") || nodeTitle.includes("Kalıntı")) {
          enemyData = {
            name: "Eski Muhafız",
            health: 100,
            maxHealth: 100,
            energy: 65,
            maxEnergy: 65,
            avatar: "🗿",
          };
        } else if (nodeId.includes("ancient") || nodeTitle.includes("Eski")) {
          enemyData = {
            name: "Eski Muhafız",
            health: 110,
            maxHealth: 110,
            energy: 70,
            maxEnergy: 70,
            avatar: "🗿",
          };
        } else if (nodeId.includes("spirit") || nodeTitle.includes("Ruh")) {
          enemyData = {
            name: "Ruh Varlığı",
            health: 130,
            maxHealth: 130,
            energy: 75,
            maxEnergy: 75,
            avatar: "👻",
          };
        }
      }
      // SCI-FI THEME - Hive City Defense enemies
      else if (scenarioId === "hive_city_defense") {
        if (nodeId.includes("collective") || nodeTitle.includes("Collective")) {
          enemyData = {
            name: "The Collective",
            health: 250,
            maxHealth: 250,
            energy: 120,
            maxEnergy: 120,
            avatar: "🤖",
          };
        } else if (nodeId.includes("robot") || nodeTitle.includes("Robot")) {
          enemyData = {
            name: "Hive Robot",
            health: 120,
            maxHealth: 120,
            energy: 60,
            maxEnergy: 60,
            avatar: "🤖",
          };
        } else if (
          nodeId.includes("dr_alex") ||
          nodeTitle.includes("Dr. Alex")
        ) {
          enemyData = {
            name: "Dr. Alex",
            health: 100,
            maxHealth: 100,
            energy: 50,
            maxEnergy: 50,
            avatar: "👨‍🔬",
          };
        } else if (nodeId.includes("mutant") || nodeTitle.includes("Mutant")) {
          enemyData = {
            name: "Hive Mutant",
            health: 150,
            maxHealth: 150,
            energy: 75,
            maxEnergy: 75,
            avatar: "🧬",
          };
        } else if (nodeId.includes("security") || nodeTitle.includes("Güvenlik")) {
          enemyData = {
            name: "Güvenlik Sistemi",
            health: 90,
            maxHealth: 90,
            energy: 45,
            maxEnergy: 45,
            avatar: "🔒",
          };
        } else if (nodeId.includes("data") || nodeTitle.includes("Veri")) {
          enemyData = {
            name: "Veri Merkezi Koruyucusu",
            health: 110,
            maxHealth: 110,
            energy: 55,
            maxEnergy: 55,
            avatar: "💾",
          };
        } else if (nodeId.includes("ai") || nodeTitle.includes("AI")) {
          enemyData = {
            name: "AI Kontrollü Makine",
            health: 180,
            maxHealth: 180,
            energy: 90,
            maxEnergy: 90,
            avatar: "🤖",
          };
        } else if (nodeId.includes("laboratory") || nodeTitle.includes("Laboratuvar")) {
          enemyData = {
            name: "Laboratuvar Koruyucusu",
            health: 130,
            maxHealth: 130,
            energy: 65,
            maxEnergy: 65,
            avatar: "🧪",
          };
        }
      }
      // CYBERPUNK THEME - Cyberpunk City Secrets enemies
      else if (scenarioId === "cyberpunk_city_secrets") {
        if (nodeId.includes("megacorp") || nodeTitle.includes("MegaCorp")) {
          enemyData = {
            name: "MegaCorp AI",
            health: 300,
            maxHealth: 300,
            energy: 150,
            maxEnergy: 150,
            avatar: "🤖",
          };
        } else if (nodeId.includes("robot") || nodeTitle.includes("Robot")) {
          enemyData = {
            name: "Cyberpunk Robot",
            health: 130,
            maxHealth: 130,
            energy: 65,
            maxEnergy: 65,
            avatar: "🤖",
          };
        } else if (
          nodeId.includes("dr_sarah") ||
          nodeTitle.includes("Dr. Sarah")
        ) {
          enemyData = {
            name: "Dr. Sarah",
            health: 110,
            maxHealth: 110,
            energy: 55,
            maxEnergy: 55,
            avatar: "👩‍🔬",
          };
        } else if (nodeId.includes("gangster") || nodeTitle.includes("Gangster")) {
          enemyData = {
            name: "Underground Gangster",
            health: 100,
            maxHealth: 100,
            energy: 50,
            maxEnergy: 50,
            avatar: "🔫",
          };
        } else if (nodeId.includes("cyber") || nodeTitle.includes("Cyber")) {
          enemyData = {
            name: "Cyber-Psycho",
            health: 160,
            maxHealth: 160,
            energy: 80,
            maxEnergy: 80,
            avatar: "🔧",
          };
        } else if (nodeId.includes("corporate") || nodeTitle.includes("Corporate")) {
          enemyData = {
            name: "Corporate Guard",
            health: 120,
            maxHealth: 120,
            energy: 60,
            maxEnergy: 60,
            avatar: "💼",
          };
        } else if (nodeId.includes("security") || nodeTitle.includes("Security")) {
          enemyData = {
            name: "Security Bot",
            health: 95,
            maxHealth: 95,
            energy: 48,
            maxEnergy: 48,
            avatar: "🤖",
          };
        } else if (nodeId.includes("ai") || nodeTitle.includes("AI")) {
          enemyData = {
            name: "AI System",
            health: 200,
            maxHealth: 200,
            energy: 100,
            maxEnergy: 100,
            avatar: "🤖",
          };
        } else if (nodeId.includes("underground") || nodeTitle.includes("Underground")) {
          enemyData = {
            name: "Underground Gang",
            health: 85,
            maxHealth: 85,
            energy: 43,
            maxEnergy: 43,
            avatar: "🔫",
          };
        }
      }

      // Enter combat mode
      window.combatSystem.startCombat(enemyData);
    }
  } catch (e) {
    console.warn("⚠️ Combat auto-trigger skipped:", e);
  }
};


              success: "Gezgin sana mağara hakkında ipuçları veriyor.",
              failure: "Gezgin seni görmezden geliyor.",
            },
          ],
          nextScenes: ["cave_entrance", "bandit_camp"],
        },
      },
    },
    2: {
      title: "Mağara Keşfi",
      description: "Karanlık mağarada gizli hazineler...",
      scenes: {
        1: {
          title: "Mağara Girişi",
          description: "Büyük bir mağara ağzı. İçeriden garip sesler geliyor.",
          npcs: ["Mağara Bekçisi"],
          encounters: ["Cave Guardian", "Rockfall"],
          choices: [
            {
              text: "Sessizce içeri gir",
              requires: { skill: "stealth", dc: 16 },
              success: "Bekçiyi fark etmeden geçiyorsun.",
              failure: "Bekçi seni fark ediyor ve saldırıyor.",
            },
            {
              text: "Bekçiyle konuş",
              requires: { skill: "charisma", dc: 18 },
              success: "Bekçi seni dostça karşılıyor.",
              failure: "Bekçi seni düşman olarak görüyor.",
            },
          ],
          nextScenes: ["cave_tunnel", "treasure_room"],
        },
        2: {
          title: "Mağara Tüneli",
          description:
            "Dar ve karanlık bir tünel. Duvarlarda garip işaretler var.",
          npcs: [],
          encounters: ["Giant Spider", "Poisonous Gas", "Ancient Trap"],
          choices: [
            {
              text: "İşaretleri incele",
              requires: { skill: "intelligence", dc: 14 },
              success: "Tuzakları fark ediyorsun ve güvenli yolu buluyorsun.",
              failure: "Bir tuzağa düşüyorsun.",
            },
            {
              text: "Hızlıca geç",
              requires: { skill: "dexterity", dc: 16 },
              success: "Tuzakları atlatıyorsun.",
              failure: "Bir tuzağa düşüyorsun.",
            },
          ],
          nextScenes: ["treasure_room", "boss_chamber"],
        },
        3: {
          title: "Hazine Odası",
          description:
            "Parlak hazinelerle dolu büyük bir oda. Ortada bir sandık var.",
          npcs: [],
          encounters: ["Treasure Guardian", "Mimic Chest"],
          choices: [
            {
              text: "Sandığı aç",
              requires: { skill: "dexterity", dc: 12 },
              success: "Değerli hazineler buluyorsun.",
              failure: "Sandık bir mimic çıkıyor ve saldırıyor.",
            },
            {
              text: "Odayı araştır",
              requires: { skill: "intelligence", dc: 15 },
              success: "Gizli geçidi buluyorsun.",
              failure: "Hiçbir şey bulamıyorsun.",
            },
          ],
          nextScenes: ["boss_chamber"],
        },
      },
    },
    3: {
      title: "Boss Savaşı",
      description: "Mağaranın efendisiyle karşılaşma...",
      scenes: {
        1: {
          title: "Boss Odası",
          description: "Devasa bir oda. Ortada büyük bir yaratık var.",
          npcs: ["Cave Boss"],
          encounters: ["Boss Battle"],
          choices: [
            {
              text: "Savaş",
              requires: { skill: "combat", dc: 20 },
              success: "Boss'u yeniyorsun ve hazineleri alıyorsun.",
              failure: "Boss seni yeniyor.",
            },
            {
              text: "Kaç",
              requires: { skill: "dexterity", dc: 18 },
              success: "Güvenli bir şekilde kaçıyorsun.",
              failure: "Boss seni yakalıyor.",
            },
          ],
          nextScenes: ["victory_celebration", "defeat_escape"],
        },
      },
    },
  },

  // Start story progression
  startStory: function () {
    this.currentChapter = 1;
    this.currentScene = 1;
    this.storyProgress = 0;
    this.updateStoryUI();
    this.showCurrentScene();
  },

  // Show current scene with detailed narrative
  showCurrentScene: function () {
    const chapter = this.storyChapters[this.currentChapter];
    const scene = chapter.scenes[this.currentScene];

    if (!scene) {
      console.error("Scene not found:", this.currentScene);
      return;
    }

    // Update environmental state
    this.updateEnvironmentalState();

    // Create immersive narrative
    let narrative = this.createImmersiveNarrative(scene);

    // Update story display
    const storyContainer = document.getElementById("story-container");
    if (storyContainer) {
      storyContainer.innerHTML = `
        <div class="story-chapter">
          <h3>📖 Bölüm ${this.currentChapter}: ${chapter.title}</h3>
          <p class="chapter-description">${chapter.description}</p>
        </div>
        <div class="story-scene">
          <h4>🎭 Sahne ${this.currentScene}: ${scene.title}</h4>
          <div class="scene-description">${narrative}</div>
          <div class="environmental-info">
            <span class="time">🕐 ${this.environmentalState.timeOfDay}</span>
            <span class="weather">🌤️ ${this.environmentalState.weather}</span>
            <span class="location">📍 ${this.environmentalState.location}</span>
          </div>
        </div>
        <div class="story-choices">
          <h4>🎯 Seçenekleriniz</h4>
          ${this.generateChoiceButtons(scene.choices)}
        </div>
      `;
    }

    // Update progress
    this.updateStoryProgress();
  },

  // Create immersive narrative with environmental details
  createImmersiveNarrative: function (scene) {
    let narrative = scene.description;

    // Add environmental details
    const timeDetails = {
      morning: "Güneş yeni doğmuş ve hava taze.",
      afternoon: "Güneş gökyüzünde yüksek ve sıcak.",
      evening: "Güneş batmaya başlıyor ve gölgeler uzuyor.",
      night: "Gece karanlığı her yeri sarmış.",
    };

    const weatherDetails = {
      clear: "Gökyüzü açık ve hava güzel.",
      cloudy: "Bulutlar gökyüzünü kaplamış.",
      rainy: "Yağmur damlaları düşüyor.",
      stormy: "Gök gürlüyor ve şimşek çakıyor.",
    };

    const atmosphereDetails = {
      peaceful: "Etraf huzurlu ve sakin.",
      tense: "Gergin bir atmosfer var.",
      dangerous: "Tehlikeli bir hava var.",
      mysterious: "Gizemli bir atmosfer var.",
    };

    narrative += ` ${timeDetails[this.environmentalState.timeOfDay]} ${
      weatherDetails[this.environmentalState.weather]
    } ${atmosphereDetails[this.environmentalState.atmosphere]}`;

    // Add NPC details
    if (scene.npcs && scene.npcs.length > 0) {
      narrative += ` Etrafta ${scene.npcs.join(", ")} var.`;
    }

    // Add encounter hints
    if (scene.encounters && scene.encounters.length > 0) {
      narrative += ` Dikkatli ol, ${scene.encounters.join(
        " veya "
      )} ile karşılaşabilirsin.`;
    }

    return narrative;
  },

  // Generate choice buttons with skill requirements
  generateChoiceButtons: function (choices) {
    if (!choices) return "<p>Bu sahnede seçenek yok.</p>";

    return choices
      .map((choice, index) => {
        const skillInfo = choice.requires
          ? ` (${choice.requires.skill} ${choice.requires.dc}+)`
          : "";
        return `
        <button class="story-choice-btn" onclick="window.storySystem.makeChoice(${index})">
          <span class="choice-text">${choice.text}${skillInfo}</span>
          <span class="choice-requirement">${
            choice.requires
              ? `Gerekli: ${choice.requires.skill} ${choice.requires.dc}`
              : "Gereksinim yok"
          }</span>
        </button>
      `;
      })
      .join("");
  },

  // Make a story choice
  makeChoice: function (choiceIndex) {
    const chapter = this.storyChapters[this.currentChapter];
    const scene = chapter.scenes[this.currentScene];
    const choice = scene.choices[choiceIndex];

    if (!choice) {
      console.error("Choice not found:", choiceIndex);
      return;
    }

    // Check skill requirement
    if (choice.requires) {
      const skillCheck = this.performSkillCheck(
        choice.requires.skill,
        choice.requires.dc
      );

      if (skillCheck.success) {
        this.showChoiceResult(choice.success, true);
      } else {
        this.showChoiceResult(choice.failure, false);
      }
    } else {
      this.showChoiceResult(choice.success || "Seçimin tamamlandı.", true);
    }

    // Record choice
    this.storyChoices.push({
      chapter: this.currentChapter,
      scene: this.currentScene,
      choice: choiceIndex,
      timestamp: new Date().toISOString(),
    });

    // Progress to next scene after delay
    setTimeout(() => {
      this.progressToNextScene();
    }, 3000);
  },

  // Perform skill check with dice roll
  performSkillCheck: function (skill, dc) {
    const roll = Math.floor(Math.random() * 20) + 1;
    const success = roll >= dc;

    // Show dice roll result
    this.showDiceResult(roll, dc, skill, success);

    return { success, roll, dc };
  },

  // Show dice roll result
  showDiceResult: function (roll, dc, skill, success) {
    const resultContainer = document.getElementById("dice-result-container");
    if (resultContainer) {
      resultContainer.innerHTML = `
        <div class="dice-result ${success ? "success" : "failure"}">
          <h4>🎲 Zar Atışı</h4>
          <p>Beceri: ${skill}</p>
          <p>Zar: ${roll} (Hedef: ${dc})</p>
          <p>Sonuç: ${success ? "✅ Başarılı" : "❌ Başarısız"}</p>
        </div>
      `;

      // Hide after 3 seconds
      setTimeout(() => {
        resultContainer.innerHTML = "";
      }, 3000);
    }
  },

  // Show choice result
  showChoiceResult: function (result, success) {
    const resultContainer = document.getElementById("choice-result-container");
    if (resultContainer) {
      resultContainer.innerHTML = `
        <div class="choice-result ${success ? "success" : "failure"}">
          <h4>${success ? "✅ Başarılı" : "❌ Başarısız"}</h4>
          <p>${result}</p>
        </div>
      `;

      // Hide after 3 seconds
      setTimeout(() => {
        resultContainer.innerHTML = "";
      }, 3000);
    }
  },

  // Progress to next scene
  progressToNextScene: function () {
    this.currentScene++;

    // Check if chapter is complete
    const chapter = this.storyChapters[this.currentChapter];
    if (!chapter.scenes[this.currentScene]) {
      this.currentChapter++;
      this.currentScene = 1;

      // Check if story is complete
      if (!this.storyChapters[this.currentChapter]) {
        this.completeStory();
        return;
      }
    }

    this.showCurrentScene();
  },

  // Complete story
  completeStory: function () {
    this.storyProgress = 100;
    this.updateStoryUI();

    const storyContainer = document.getElementById("story-container");
    if (storyContainer) {
      storyContainer.innerHTML = `
        <div class="story-complete">
          <h3>🎉 Hikaye Tamamlandı!</h3>
          <p>Mükemmel bir macera yaşadın! Tüm zorlukları aştın ve hazineleri elde ettin.</p>
          <div class="story-stats">
            <h4>📊 Macera İstatistikleri</h4>
            <p>Tamamlanan Bölümler: ${this.currentChapter - 1}</p>
            <p>Karşılaşılan NPC'ler: ${this.encounteredNPCs.length}</p>
            <p>Keşfedilen Lokasyonlar: ${this.discoveredLocations.length}</p>
            <p>Yapılan Seçimler: ${this.storyChoices.length}</p>
          </div>
          <button onclick="window.storySystem.startNewStory()" class="new-story-btn">🔄 Yeni Macera Başlat</button>
        </div>
      `;
    }
  },

  // Start new story
  startNewStory: function () {
    this.currentChapter = 1;
    this.currentScene = 1;
    this.storyProgress = 0;
    this.discoveredLocations = [];
    this.encounteredNPCs = [];
    this.completedQuests = [];
    this.storyChoices = [];
    this.updateEnvironmentalState();
    this.showCurrentScene();
  },

  // Update environmental state
  updateEnvironmentalState: function () {
    // Change time based on story progress
    const timeProgress = this.storyProgress / 100;
    if (timeProgress < 0.25) {
      this.environmentalState.timeOfDay = "morning";
    } else if (timeProgress < 0.5) {
      this.environmentalState.timeOfDay = "afternoon";
    } else if (timeProgress < 0.75) {
      this.environmentalState.timeOfDay = "evening";
    } else {
      this.environmentalState.timeOfDay = "night";
    }

    // Change weather randomly
    const weathers = ["clear", "cloudy", "rainy", "stormy"];
    this.environmentalState.weather =
      weathers[Math.floor(Math.random() * weathers.length)];

    // Change atmosphere based on chapter
    const atmospheres = ["peaceful", "tense", "dangerous", "mysterious"];
    this.environmentalState.atmosphere =
      atmospheres[Math.floor(Math.random() * atmospheres.length)];
  },

  // Update story progress
  updateStoryProgress: function () {
    const totalScenes = Object.keys(this.storyChapters).length * 3; // Assuming 3 scenes per chapter
    const completedScenes =
      (this.currentChapter - 1) * 3 + (this.currentScene - 1);
    this.storyProgress = Math.floor((completedScenes / totalScenes) * 100);
    this.updateStoryUI();
  },

  // Update story UI
  updateStoryUI: function () {
    const progressBar = document.getElementById("story-progress-bar");
    if (progressBar) {
      progressBar.style.width = `${this.storyProgress}%`;
    }

    const progressText = document.getElementById("story-progress-text");
    if (progressText) {
      progressText.textContent = `İlerleme: ${this.storyProgress}%`;
    }
  },
};

console.log("✅ Global functions loaded successfully!");
