// Enhanced Script for AI Dungeon Master
// =====================================

// Global game state
window.gameState = {
  currentScenario: null,
  currentNode: 'start',
  playerChoices: [],
  gameHistory: [],
  currentTheme: 'fantasy',
  currentDifficulty: 'medium',
  currentLevel: 1,
  currentXP: 0,
  skillPoints: 0,
  unlockedSkills: [],
  skillLevels: {},
  currentStats: {
    hp: 100,
    max_hp: 100,
    mana: 50,
    max_mana: 50,
    attack: 10,
    defense: 5,
    strength: 10,
    dexterity: 10,
    intelligence: 10,
    charisma: 10
  }
};

// Player statistics tracking
window.playerStats = {
  karma: 0,
  reputation: 0,
  npc_relationships: {},
  faction_standing: {},
  moral_choices: [],
  quests_completed: 0,
  quests_failed: 0,
  combat_victories: 0,
  combat_defeats: 0,
  exploration_points: 0,
  currentUserId: "guest_001",
};

// NPC SYSTEM
window.npcSystem = {
  currentNPCs: [],
  activeQuests: [],
  npcRelationships: {},
  
  // Load NPCs for current scenario
  loadNPCs: function(scenarioId) {
    console.log(`👥 Loading NPCs for scenario: ${scenarioId}`);
    fetch(`/api/npcs/${scenarioId}`)
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          this.currentNPCs = data.npcs;
          this.displayNPCs();
          console.log(`✅ Loaded ${Object.keys(data.npcs).length} NPCs`);
        } else {
          console.warn("No NPCs found for scenario, using fallback");
          this.loadFallbackNPCs();
        }
      })
      .catch(error => {
        console.error("Error loading NPCs:", error);
        // Fallback NPCs
        this.loadFallbackNPCs();
      });
  },
  
  // Display NPCs in the UI
  displayNPCs: function() {
    const npcContainer = document.getElementById('npc-container');
    if (!npcContainer) {
      console.error("NPC container not found");
      return;
    }
    
    npcContainer.innerHTML = '';
    
    Object.keys(this.currentNPCs).forEach(npcId => {
      const npc = this.currentNPCs[npcId];
      const npcElement = document.createElement('div');
      npcElement.className = 'npc-item';
      npcElement.innerHTML = `
        <div class="npc-header">
          <span class="npc-name">${npc.name}</span>
          <span class="npc-title">${npc.title || ''}</span>
        </div>
        <div class="npc-description">${npc.description || 'Mysterious character...'}</div>
        <div class="npc-actions">
          <button onclick="window.npcSystem.interactWithNPC('${npcId}', 'greeting')" class="npc-btn">Selamla</button>
          <button onclick="window.npcSystem.interactWithNPC('${npcId}', 'quest')" class="npc-btn">Görev İste</button>
          <button onclick="window.npcSystem.interactWithNPC('${npcId}', 'trade')" class="npc-btn">Ticaret</button>
        </div>
      `;
      npcContainer.appendChild(npcElement);
    });
  },
  
  // Interact with NPC
  interactWithNPC: function(npcId, interactionType) {
    console.log(`👥 Interacting with NPC ${npcId}: ${interactionType}`);
    
    const currentScenario = window.currentScenario || 'cyberpunk_city_secrets';
    
    fetch(`/api/npcs/${currentScenario}/${npcId}/interact`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        interaction_type: interactionType
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        this.handleNPCResponse(data);
      }
    })
    .catch(error => {
      console.error("Error interacting with NPC:", error);
      this.handleNPCResponse({
        success: true,
        response: "Merhaba! Nasılsın?",
        npc_name: "NPC",
        npc_title: "Villager"
      });
    });
  },
  
  // Handle NPC response
  handleNPCResponse: function(data) {
    const storyText = document.getElementById('story-text');
    if (storyText) {
      storyText.innerHTML = `
        <div class="npc-dialogue">
          <div class="npc-speaker">${data.npc_name} (${data.npc_title})</div>
          <div class="npc-message">${data.response}</div>
        </div>
      `;
    }
  },
  
  // Load fallback NPCs if API fails
  loadFallbackNPCs: function() {
    console.log("🔄 Loading fallback NPCs...");
    this.currentNPCs = {
      'detective_max': {
        name: 'Detective Max',
        title: 'Şehir Dedektifi',
        description: 'Deneyimli bir dedektif. Şehirdeki gizemleri çözmek için yardım edebilir.'
      },
      'neon': {
        name: 'Neon',
        title: 'Gizli Hacker',
        description: 'Siber uzayın derinliklerinde yaşayan gizemli bir hacker.'
      }
    };
    this.displayNPCs();
  }
};

// QUEST SYSTEM
window.questSystem = {
  activeQuests: [],
  completedQuests: [],
  
  // Load available quests
  loadQuests: function() {
    console.log("📋 Loading available quests...");
    fetch('/api/quests/active')
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          this.activeQuests = data.quests || [];
          this.displayQuests();
        }
      })
      .catch(error => {
        console.error("Error loading quests:", error);
        this.loadFallbackQuests();
      });
  },
  
  // Display quests in UI
  displayQuests: function() {
    const questContainer = document.getElementById('quest-container');
    if (!questContainer) {
      console.error("Quest container not found");
      return;
    }
    
    questContainer.innerHTML = '';
    
    this.activeQuests.forEach(quest => {
      const questElement = document.createElement('div');
      questElement.className = 'quest-item';
      questElement.innerHTML = `
        <div class="quest-header">
          <span class="quest-title">${quest.title}</span>
          <span class="quest-level">Seviye ${quest.level || 1}</span>
        </div>
        <div class="quest-description">${quest.description}</div>
        <div class="quest-rewards">
          <span class="reward-xp">XP: ${quest.rewards?.xp || 100}</span>
          <span class="reward-gold">Altın: ${quest.rewards?.gold || 50}</span>
        </div>
        <div class="quest-actions">
          <button onclick="window.questSystem.acceptQuest('${quest.id}')" class="quest-btn">Kabul Et</button>
          <button onclick="window.questSystem.viewQuestDetails('${quest.id}')" class="quest-btn">Detaylar</button>
        </div>
      `;
      questContainer.appendChild(questElement);
    });
  },
  
  // Accept a quest
  acceptQuest: function(questId) {
    console.log(`📋 Accepting quest: ${questId}`);
    
    fetch('/api/quests/accept', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        quest_id: questId,
        user_id: window.playerStats.currentUserId
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        console.log("✅ Quest accepted!");
        this.loadQuests(); // Refresh quest list
      }
    })
    .catch(error => {
      console.error("Error accepting quest:", error);
    });
  },
  
  // View quest details
  viewQuestDetails: function(questId) {
    const quest = this.activeQuests.find(q => q.id === questId);
    if (quest) {
      const storyText = document.getElementById('story-text');
      if (storyText) {
        storyText.innerHTML = `
          <div class="quest-details">
            <h3>${quest.title}</h3>
            <p><strong>Seviye:</strong> ${quest.level || 1}</p>
            <p><strong>Açıklama:</strong> ${quest.description}</p>
            <p><strong>Ödüller:</strong></p>
            <ul>
              <li>XP: ${quest.rewards?.xp || 100}</li>
              <li>Altın: ${quest.rewards?.gold || 50}</li>
              ${quest.rewards?.items ? `<li>Eşyalar: ${quest.rewards.items.join(', ')}</li>` : ''}
            </ul>
            <button onclick="window.questSystem.acceptQuest('${quest.id}')" class="quest-btn">Bu Görevi Kabul Et</button>
          </div>
        `;
      }
    }
  },
  
  // Load fallback quests if API fails
  loadFallbackQuests: function() {
    console.log("🔄 Loading fallback quests...");
    this.activeQuests = [
      {
        id: 'investigate_healer',
        title: 'Şifacının Sırrı',
        description: 'Lydia\'nın babasının neden değiştiğini araştır. Ejderha ile bağlantısı olabilir.',
        level: 1,
        rewards: { xp: 50, gold: 25, items: ['Şifacı İksiri'] }
      },
      {
        id: 'dragon_knowledge',
        title: 'Ejderha Bilgisi',
        description: 'Shadow\'dan ejderha hakkında daha fazla bilgi al. Kolyenin sırrını öğren.',
        level: 2,
        rewards: { xp: 75, gold: 50, items: ['Gizli Bilgi'] }
      }
    ];
    this.displayQuests();
  }
};

// Player Statistics System
window.loadPlayerStatistics = function () {
  console.log("📊 Loading player statistics...");
  
  fetch(`/api/player/statistics/${window.playerStats.currentUserId}`)
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        window.playerStats = { ...window.playerStats, ...data.statistics };
        window.updateStatisticsDisplay();
      }
    })
    .catch(error => {
      console.error("Error loading player statistics:", error);
    });
};

window.updatePlayerStatistics = function (statType, value, context = {}) {
  console.log(`📊 Updating ${statType}: ${value}`);
  
  fetch('/api/player/statistics/update', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: window.playerStats.currentUserId,
      stat_type: statType,
      value: value,
      context: context
    })
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        window.playerStats = { ...window.playerStats, ...data.statistics };
        window.updateStatisticsDisplay();
      }
    })
    .catch(error => {
      console.error("Error updating player statistics:", error);
    });
};

window.updateStatisticsDisplay = function () {
  const karmaElement = document.getElementById('player-karma');
  const reputationElement = document.getElementById('player-reputation');
  
  if (karmaElement) {
    karmaElement.textContent = window.playerStats.karma || 0;
  }
  
  if (reputationElement) {
    reputationElement.textContent = window.playerStats.reputation || 0;
  }
};

// Skill System
window.loadSkillSystem = function () {
  console.log("⚔️ Loading skill system...");
  
  fetch(`/api/skills/available/${window.playerStats.currentUserId}`)
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        window.gameState.skillPoints = data.progression.skill_points;
        window.gameState.unlockedSkills = data.progression.unlocked_skills;
        window.updateLevelDisplay();
        window.displayAvailableSkills();
      }
    })
    .catch(error => {
      console.error("Error loading skill system:", error);
    });
};

window.loadAvailableSkills = function () {
  console.log("⚔️ Loading available skills...");
  
  fetch(`/api/skills/available/${window.playerStats.currentUserId}`)
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        window.displayAvailableSkills(data.skills);
      }
    })
    .catch(error => {
      console.error("Error loading available skills:", error);
    });
};

window.displayAvailableSkills = function (skills) {
  const skillsContainer = document.getElementById('available-skills');
  if (!skillsContainer) return;
  
  skillsContainer.innerHTML = '';
  
  if (skills && skills.length > 0) {
    skills.forEach(skill => {
      const skillElement = document.createElement('div');
      skillElement.className = 'skill-item';
      skillElement.innerHTML = `
        <div class="skill-header">
          <span class="skill-name">${skill.name}</span>
          <span class="skill-type">${skill.type}</span>
        </div>
        <div class="skill-description">${skill.description}</div>
        <div class="skill-requirements">
          <small>Gereksinimler: Seviye ${skill.requirements.level}, ${skill.requirements.skill_points} SP</small>
        </div>
        <button onclick="window.unlockSkill('${skill.id}')" class="skill-btn" ${!skill.can_unlock ? 'disabled' : ''}>
          ${skill.can_unlock ? 'Aç' : skill.unlock_message}
        </button>
      `;
      skillsContainer.appendChild(skillElement);
    });
  } else {
    skillsContainer.innerHTML = '<p>Henüz açılabilir beceri yok.</p>';
  }
};

window.displayUnlockedSkills = function () {
  const skillsContainer = document.getElementById('unlocked-skills');
  if (!skillsContainer) return;
  
  skillsContainer.innerHTML = '';
  
  if (window.gameState.unlockedSkills.length > 0) {
    window.gameState.unlockedSkills.forEach(skillId => {
      const skillElement = document.createElement('div');
      skillElement.className = 'skill-item unlocked';
      skillElement.innerHTML = `
        <div class="skill-header">
          <span class="skill-name">${skillId}</span>
          <span class="skill-level">Seviye ${window.gameState.skillLevels[skillId] || 1}</span>
        </div>
        <button onclick="window.useSkill('${skillId}')" class="skill-btn">Kullan</button>
      `;
      skillsContainer.appendChild(skillElement);
    });
  } else {
    skillsContainer.innerHTML = '<p>Henüz açılmış beceri yok.</p>';
  }
};

window.unlockSkill = function (skillId) {
  console.log(`⚔️ Unlocking skill: ${skillId}`);
  
  fetch('/api/skills/unlock', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: window.playerStats.currentUserId,
      skill_id: skillId
    })
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        console.log("✅ Skill unlocked!");
        window.gameState.skillPoints = data.progression.skill_points;
        window.gameState.unlockedSkills = data.progression.unlocked_skills;
        window.updateLevelDisplay();
        window.loadAvailableSkills();
        window.displayUnlockedSkills();
      } else {
        console.error("❌ Failed to unlock skill:", data.message);
      }
    })
    .catch(error => {
      console.error("Error unlocking skill:", error);
    });
};

window.useSkill = function (skillId) {
  console.log(`⚔️ Using skill: ${skillId}`);
  
  fetch('/api/skills/use', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: window.playerStats.currentUserId,
      skill_id: skillId,
      target: 'enemy'
    })
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        console.log("✅ Skill used successfully!");
        window.applySkillEffects(data.skill_result);
      } else {
        console.error("❌ Failed to use skill:", data.message);
      }
    })
    .catch(error => {
      console.error("Error using skill:", error);
    });
};

window.applySkillEffects = function (skillResult) {
  const storyText = document.getElementById('story-text');
  if (storyText) {
    storyText.innerHTML = `
      <div class="skill-result">
        <h3>${skillResult.skill_name} Kullanıldı!</h3>
        <p>${skillResult.message}</p>
        <div class="skill-effects">
          ${Object.entries(skillResult.effects).map(([effect, value]) => 
            `<div class="effect">${effect}: ${value}</div>`
          ).join('')}
        </div>
      </div>
    `;
  }
};

// Level System
window.updateLevelDisplay = function () {
  const levelElement = document.getElementById('player-level');
  const xpElement = document.getElementById('player-xp');
  const skillPointsElement = document.getElementById('skill-points');
  
  if (levelElement) {
    levelElement.textContent = window.gameState.currentLevel;
  }
  
  if (xpElement) {
    xpElement.textContent = window.gameState.currentXP;
  }
  
  if (skillPointsElement) {
    skillPointsElement.textContent = window.gameState.skillPoints;
  }
};

window.getLevelData = function (level) {
  const levelRequirements = {
    1: { experience_required: 0, skill_points_gained: 0 },
    2: { experience_required: 100, skill_points_gained: 1 },
    3: { experience_required: 250, skill_points_gained: 1 },
    4: { experience_required: 450, skill_points_gained: 2 },
    5: { experience_required: 700, skill_points_gained: 2 }
  };
  
  return levelRequirements[level] || { experience_required: 0, skill_points_gained: 0 };
};

window.gainXP = function (xpAmount) {
  console.log(`⭐ Gaining ${xpAmount} XP`);
  
  fetch('/api/character/gain_xp', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: window.playerStats.currentUserId,
      xp: xpAmount
    })
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        window.gameState.currentXP = data.total_xp;
        
        if (data.level_up.leveled_up) {
          window.showLevelUpNotification(data.level_up.new_level, data.level_up.skill_points_gained);
          window.gameState.currentLevel = data.level_up.new_level;
          window.gameState.skillPoints += data.level_up.skill_points_gained;
        }
        
        window.updateLevelDisplay();
      }
    })
    .catch(error => {
      console.error("Error gaining XP:", error);
    });
};

window.showLevelUpNotification = function (newLevel, skillPointsGained) {
  const storyText = document.getElementById('story-text');
  if (storyText) {
    storyText.innerHTML = `
      <div class="level-up-notification">
        <h2>🎉 Seviye Atladın!</h2>
        <p>Yeni seviye: ${newLevel}</p>
        <p>Kazanılan beceri puanı: ${skillPointsGained}</p>
        <button onclick="window.loadAvailableSkills()" class="btn">Becerileri Görüntüle</button>
      </div>
    `;
  }
};

// UI Functions
window.switchSkillTab = function (tab) {
  const tabs = ['available', 'unlocked'];
  tabs.forEach(t => {
    const tabElement = document.getElementById(`skills-${t}-tab`);
    const contentElement = document.getElementById(`skills-${t}-content`);
    
    if (tabElement && contentElement) {
      if (t === tab) {
        tabElement.classList.add('active');
        contentElement.style.display = 'block';
      } else {
        tabElement.classList.remove('active');
        contentElement.style.display = 'none';
      }
    }
  });
};

// Theme switching
window.switchTheme = function (theme) {
  console.log(`🎨 Switching to ${theme} theme`);
  
  window.gameState.currentTheme = theme;
  
  // Update UI elements
  const themeButtons = document.querySelectorAll('.theme-btn');
  themeButtons.forEach(btn => {
    btn.classList.remove('active');
    if (btn.dataset.theme === theme) {
      btn.classList.add('active');
    }
  });
  
  // Update character creation
  const characterCreation = document.getElementById('character-creation');
  if (characterCreation) {
    characterCreation.className = `character-creation ${theme}-theme`;
  }
  
  // Load theme-specific content
  if (window.loadThemeContent) {
    window.loadThemeContent(theme);
  }
};

// Character creation functions
window.selectRace = function (element, race) {
  console.log(`👤 Selected race: ${race}`);
  
  // Remove active class from all race buttons
  const raceButtons = document.querySelectorAll('.race-btn');
  raceButtons.forEach(btn => btn.classList.remove('active'));
  
  // Add active class to selected button
  element.classList.add('active');
  
  // Update game state
  window.gameState.characterRace = race;
  
  // Update stats based on race
  window.applyRaceClassToStats();
};

window.selectClass = function (element, className) {
  console.log(`⚔️ Selected class: ${className}`);
  
  // Remove active class from all class buttons
  const classButtons = document.querySelectorAll('.class-btn');
  classButtons.forEach(btn => btn.classList.remove('active'));
  
  // Add active class to selected button
  element.classList.add('active');
  
  // Update game state
  window.gameState.characterClass = className;
  
  // Update stats based on class
  window.applyRaceClassToStats();
};

// Scenario selection
window.selectScenario = function (scenarioId) {
  console.log(`🎮 Selected scenario: ${scenarioId}`);
  
  window.gameState.currentScenario = scenarioId;
  
  // Hide scenario selection, show active game
  const scenarioSelection = document.getElementById('scenario-selection');
  const activeGame = document.getElementById('active-game');
  
  if (scenarioSelection && activeGame) {
    scenarioSelection.style.display = 'none';
    activeGame.style.display = 'block';
  }
  
  // Load scenario data
  window.startScenario(scenarioId);
};

// AI Scenario Generation
window.generateAIScenario = function () {
  console.log("🤖 Generating AI scenario...");
  
  const theme = window.gameState.currentTheme;
  const difficulty = window.gameState.currentDifficulty;
  
  fetch('/api/ai/generate_scenario', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      theme: theme,
      difficulty: difficulty,
      scenario_type: 'adventure'
    })
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        console.log("✅ AI scenario generated!");
        window.addAIScenarioToGrid(data.scenario.id, data.scenario.title, data.scenario.description, data.scenario.difficulty);
      }
    })
    .catch(error => {
      console.error("Error generating AI scenario:", error);
    });
};

// Helper functions for AI scenarios
function generateScenarioTitle(theme, difficulty) {
  const titles = {
    fantasy: {
      easy: ['Küçük Macera', 'Orman Yolculuğu', 'Köy Görevi'],
      medium: ['Ejderha Avı', 'Büyücü Kulesi', 'Antik Tapınak'],
      hard: ['Kaos Savaşı', 'Karanlık Lord', 'Efsanevi Macera']
    },
    scifi: {
      easy: ['Uzay İstasyonu', 'Robot Tamiri', 'Koloni Görevi'],
      medium: ['AI Kontrolü', 'Uzay Savaşı', 'Teknoloji Araştırması'],
      hard: ['Galaktik Savaş', 'Kara Delik', 'Siber Savaş']
    },
    cyberpunk: {
      easy: ['Şehir Görevi', 'Hack İşi', 'Underground'],
      medium: ['MegaCorp Infiltration', 'AI Rebellion', 'Neon Savaşı'],
      hard: ['Matrix Savaşı', 'Siber Apocalypse', 'Digital Hell']
    },
    warhammer: {
      easy: ['İmperial Görev', 'Chaos Temizliği', 'Hive Patrol'],
      medium: ['Space Marine Mission', 'Ork Invasion', 'Eldar Encounter'],
      hard: ['Chaos Lord Battle', 'Tyranid Swarm', 'Necron Awakening']
    }
  };
  
  const themeTitles = titles[theme] || titles.fantasy;
  const difficultyTitles = themeTitles[difficulty] || themeTitles.medium;
  return difficultyTitles[Math.floor(Math.random() * difficultyTitles.length)];
}

function generateScenarioDescription(theme, difficulty, level) {
  const descriptions = {
    fantasy: `Seviye ${level} fantastik macera. Büyülü yaratıklar ve gizemli ormanlar seni bekliyor.`,
    scifi: `Seviye ${level} bilim kurgu görevi. Uzay gemileri ve yapay zeka seni bekliyor.`,
    cyberpunk: `Seviye ${level} cyberpunk gerilim. Neon ışıkları altında tehlikeli bir dünya.`,
    warhammer: `Seviye ${level} Warhammer 40K savaşı. Chaos ve İmperium arasında seçim yap.`
  };
  
  return descriptions[theme] || descriptions.fantasy;
}

function generateScenarioChoices(theme, difficulty) {
  const baseChoices = [
    { text: 'İleri git', effect: 'exploration + 5' },
    { text: 'Dikkatli ol', effect: 'defense + 3' },
    { text: 'Saldır', effect: 'attack + 5' }
  ];
  
  return baseChoices;
}

function addAIScenarioToGrid(scenarioId, title, description, difficulty) {
  const aiScenariosGrid = document.getElementById('ai-scenarios-grid');
  if (!aiScenariosGrid) return;
  
  const scenarioCard = document.createElement('div');
  scenarioCard.className = 'scenario-card ai-generated';
  scenarioCard.innerHTML = `
    <h3>${title}</h3>
    <p>${description}</p>
    <div class="ai-info">
      <small>🤖 AI tarafından üretildi</small>
    </div>
  `;

  aiScenariosGrid.appendChild(scenarioCard);
}

// Initialize everything when DOM is loaded
window.addEventListener("DOMContentLoaded", function () {
  console.log("🎮 AI Dungeon Master Enhanced Script Loaded!");
  
  // Initialize systems
  if (typeof switchTheme === "function") {
    switchTheme('fantasy');
  }
  
  if (typeof updateCharacterPanel === "function") {
    updateCharacterPanel();
  }
  
  if (typeof window.loadSkillSystem === "function") {
    window.loadSkillSystem();
  }
  
  if (typeof window.loadPlayerStatistics === "function") {
    window.loadPlayerStatistics();
  }
  
  if (typeof window.loadAIScenarios === "function") {
    window.loadAIScenarios();
  }
});
