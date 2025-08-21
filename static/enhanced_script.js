// Enhanced Script for AI Dungeon Master
// =====================================

console.log("🎮 Enhanced Script Loading...");

// Global game state
window.gameState = {
  currentScenario: null,
  currentNode: "start",
  playerChoices: [],
  gameHistory: [],
  currentTheme: "fantasy",
  currentDifficulty: "medium",
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
    charisma: 10,
  },
};

console.log("✅ Game state initialized");

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

// ENHANCED SCENARIO SYSTEM
window.enhancedScenarioSystem = {
  currentScenario: null,
  currentLevel: null,
  npcRelationships: {},
  questProgress: {},

  // Load enhanced scenario
  loadEnhancedScenario: function (scenarioId) {
    console.log(`🎮 Loading enhanced scenario: ${scenarioId}`);
    fetch(`/api/scenarios/enhanced/${scenarioId}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          this.currentScenario = data.scenario;
          this.displayScenarioInfo();
          this.loadNPCRelationships(scenarioId);
          this.loadQuestProgress(scenarioId);
          console.log(`✅ Enhanced scenario loaded: ${data.scenario.title}`);
        } else {
          console.error("Failed to load enhanced scenario:", data.error);
        }
      })
      .catch((error) => {
        console.error("Error loading enhanced scenario:", error);
      });
  },

  // Display scenario information
  displayScenarioInfo: function () {
    const scenarioInfo = document.getElementById("scenario-info");
    if (!scenarioInfo || !this.currentScenario) return;

    scenarioInfo.innerHTML = `
      <div class="scenario-header">
        <h2>${this.currentScenario.title}</h2>
        <p>${this.currentScenario.description}</p>
        <div class="scenario-stats">
          <span>Zorluk: ${this.currentScenario.difficulty}</span>
          <span>Tahmini Süre: ${
            this.currentScenario.estimatedPlayTime
          } dakika</span>
        </div>
      </div>
      <div class="level-progression">
        <h3>Seviye İlerlemesi</h3>
        <div class="level-list">
          ${Object.keys(this.currentScenario.levels)
            .map((levelId) => {
              const level = this.currentScenario.levels[levelId];
              return `
              <div class="level-item" onclick="window.enhancedScenarioSystem.loadLevel('${levelId}')">
                <h4>${level.title}</h4>
                <p>${level.description}</p>
                <span>Seviye: ${level.min_level}-${level.max_level}</span>
              </div>
            `;
            })
            .join("")}
        </div>
      </div>
    `;
  },

  // Load specific level
  loadLevel: function (levelId) {
    if (!this.currentScenario) return;

    console.log(`📊 Loading level: ${levelId}`);
    fetch(`/api/scenarios/enhanced/${this.currentScenario.id}/level/${levelId}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          this.currentLevel = data.level;
          this.displayLevelInfo();
          this.loadLevelEnemies(levelId);
          console.log(`✅ Level loaded: ${data.level.title}`);
        } else {
          console.error("Failed to load level:", data.error);
        }
      })
      .catch((error) => {
        console.error("Error loading level:", error);
      });
  },

  // Display level information
  displayLevelInfo: function () {
    const levelInfo = document.getElementById("level-info");
    if (!levelInfo || !this.currentLevel) return;

    levelInfo.innerHTML = `
      <div class="level-header">
        <h3>${this.currentLevel.title}</h3>
        <p>${this.currentLevel.description}</p>
      </div>
      <div class="enemies-section">
        <h4>Düşmanlar</h4>
        <div class="enemies-list">
          ${this.currentLevel.enemies
            .map(
              (enemy) => `
            <div class="enemy-item">
              <span class="enemy-name">${enemy.name}</span>
              <span class="enemy-level">Seviye ${enemy.level}</span>
              <span class="enemy-hp">HP: ${enemy.hp}</span>
              <span class="enemy-xp">XP: ${enemy.xp_reward}</span>
            </div>
          `
            )
            .join("")}
        </div>
      </div>
      ${
        this.currentLevel.boss
          ? `
        <div class="boss-section">
          <h4>Boss</h4>
          <div class="boss-item">
            <span class="boss-name">${this.currentLevel.boss.name}</span>
            <span class="boss-level">Seviye ${this.currentLevel.boss.level}</span>
            <span class="boss-hp">HP: ${this.currentLevel.boss.hp}</span>
            <span class="boss-xp">XP: ${this.currentLevel.boss.xp_reward}</span>
          </div>
        </div>
      `
          : ""
      }
      <div class="side-quests-section">
        <h4>Yan Görevler</h4>
        <div class="quests-list">
          ${this.currentLevel.side_quests
            .map(
              (quest) => `
            <div class="quest-item">
              <span class="quest-title">${quest.title}</span>
              <p>${quest.description}</p>
              <span class="quest-reward">XP: ${quest.xp_reward}, Altın: ${quest.gold_reward}</span>
              <button onclick="window.enhancedScenarioSystem.completeQuest('${quest.id}')" class="quest-btn">Görevi Tamamla</button>
            </div>
          `
            )
            .join("")}
        </div>
      </div>
    `;
  },

  // Load NPC relationships
  loadNPCRelationships: function (scenarioId) {
    console.log(`👥 Loading NPC relationships for scenario: ${scenarioId}`);

    // Load relationships for each NPC in the scenario
    if (this.currentScenario && this.currentScenario.npc_relationships) {
      Object.keys(this.currentScenario.npc_relationships).forEach((npcId) => {
        this.getNPCRelationship(scenarioId, npcId);
      });
    }
  },

  // Get NPC relationship
  getNPCRelationship: function (scenarioId, npcId) {
    fetch(
      `/api/scenarios/enhanced/${scenarioId}/npc/${npcId}/relationship?username=${window.playerStats.currentUserId}`
    )
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          this.npcRelationships[npcId] = data.relationship;
          this.displayNPCRelationships();
        }
      })
      .catch((error) => {
        console.error("Error loading NPC relationship:", error);
      });
  },

  // Update NPC relationship
  updateNPCRelationship: function (
    scenarioId,
    npcId,
    trustChange,
    questCompleted = false
  ) {
    fetch(
      `/api/scenarios/enhanced/${scenarioId}/npc/${npcId}/relationship?username=${window.playerStats.currentUserId}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          trust_change: trustChange,
          quest_completed: questCompleted,
        }),
      }
    )
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          this.npcRelationships[npcId] = data.relationship;
          this.displayNPCRelationships();
          console.log(`✅ NPC relationship updated: ${npcId}`);
        }
      })
      .catch((error) => {
        console.error("Error updating NPC relationship:", error);
      });
  },

  // Display NPC relationships
  displayNPCRelationships: function () {
    const npcRelationshipsContainer =
      document.getElementById("npc-relationships");
    if (!npcRelationshipsContainer) return;

    npcRelationshipsContainer.innerHTML = `
      <h3>NPC İlişkileri</h3>
      <div class="relationships-list">
        ${Object.keys(this.npcRelationships)
          .map((npcId) => {
            const relationship = this.npcRelationships[npcId];
            return `
            <div class="relationship-item">
              <span class="npc-name">${npcId}</span>
              <span class="trust-level">Güven: ${relationship.trust_level}/100</span>
              <span class="relationship-status">${relationship.relationship_status}</span>
              <span class="quests-completed">Görevler: ${relationship.quests_completed}</span>
            </div>
          `;
          })
          .join("")}
      </div>
    `;
  },

  // Complete quest
  completeQuest: function (questId) {
    if (!this.currentScenario) return;

    console.log(`📋 Completing quest: ${questId}`);
    fetch(
      `/api/scenarios/enhanced/${this.currentScenario.id}/quest/${questId}/complete`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: window.playerStats.currentUserId,
        }),
      }
    )
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          this.questProgress = data.progress;
          this.displayQuestProgress();
          console.log(`✅ Quest completed! Rewards:`, data.rewards);

          // Show rewards notification
          this.showRewardsNotification(data.rewards);
        }
      })
      .catch((error) => {
        console.error("Error completing quest:", error);
      });
  },

  // Load quest progress
  loadQuestProgress: function (scenarioId) {
    // This would be loaded from the server
    this.questProgress = {
      completed_quests: [],
      total_xp: 0,
      total_gold: 0,
    };
    this.displayQuestProgress();
  },

  // Display quest progress
  displayQuestProgress: function () {
    const questProgressContainer = document.getElementById("quest-progress");
    if (!questProgressContainer) return;

    questProgressContainer.innerHTML = `
      <h3>Görev İlerlemesi</h3>
      <div class="progress-stats">
        <span>Tamamlanan Görevler: ${this.questProgress.completed_quests.length}</span>
        <span>Toplam XP: ${this.questProgress.total_xp}</span>
        <span>Toplam Altın: ${this.questProgress.total_gold}</span>
      </div>
    `;
  },

  // Show rewards notification
  showRewardsNotification: function (rewards) {
    const notification = document.createElement("div");
    notification.className = "rewards-notification";
    notification.innerHTML = `
      <h4>🎉 Görev Tamamlandı!</h4>
      <p>XP: +${rewards.xp}</p>
      <p>Altın: +${rewards.gold}</p>
      ${rewards.items ? `<p>Eşyalar: ${rewards.items.join(", ")}</p>` : ""}
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.remove();
    }, 5000);
  },

  // Get possible endings
  getPossibleEndings: function () {
    if (!this.currentScenario) return;

    console.log(
      `🏁 Getting possible endings for scenario: ${this.currentScenario.id}`
    );
    fetch(
      `/api/scenarios/enhanced/${this.currentScenario.id}/ending?username=${window.playerStats.currentUserId}`
    )
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          this.displayPossibleEndings(data.possible_endings);
          console.log(`✅ Possible endings loaded:`, data.possible_endings);
        }
      })
      .catch((error) => {
        console.error("Error loading possible endings:", error);
      });
  },

  // Display possible endings
  displayPossibleEndings: function (endings) {
    const endingsContainer = document.getElementById("possible-endings");
    if (!endingsContainer) return;

    endingsContainer.innerHTML = `
      <h3>Mümkün Sonlar</h3>
      <div class="endings-list">
        ${endings
          .map(
            (ending) => `
          <div class="ending-item">
            <h4>${ending.name}</h4>
            <p>${ending.description}</p>
          </div>
        `
          )
          .join("")}
      </div>
    `;
  },
};

// NPC SYSTEM
window.npcSystem = {
  currentNPCs: [],
  activeQuests: [],
  npcRelationships: {},

  // Load NPCs for current scenario
  loadNPCs: function (scenarioId) {
    console.log(`👥 Loading NPCs for scenario: ${scenarioId}`);
    fetch(`/api/npcs/${scenarioId}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          this.currentNPCs = data.npcs;
          this.displayNPCs();
          console.log(`✅ Loaded ${Object.keys(data.npcs).length} NPCs`);
        } else {
          console.warn("No NPCs found for scenario, using fallback");
          this.loadFallbackNPCs();
        }
      })
      .catch((error) => {
        console.error("Error loading NPCs:", error);
        // Fallback NPCs
        this.loadFallbackNPCs();
      });
  },

  // Display NPCs in the UI
  displayNPCs: function () {
    const npcContainer = document.getElementById("npc-container");
    if (!npcContainer) {
      console.error("NPC container not found");
      return;
    }

    npcContainer.innerHTML = "";

    Object.keys(this.currentNPCs).forEach((npcId) => {
      const npc = this.currentNPCs[npcId];
      const npcElement = document.createElement("div");
      npcElement.className = "npc-item";
      npcElement.innerHTML = `
        <div class="npc-header">
          <span class="npc-name">${npc.name}</span>
          <span class="npc-title">${npc.title || ""}</span>
        </div>
        <div class="npc-description">${
          npc.description || "Mysterious character..."
        }</div>
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
  interactWithNPC: function (npcId, interactionType) {
    console.log(`👥 Interacting with NPC ${npcId}: ${interactionType}`);

    const currentScenario = window.currentScenario || "cyberpunk_city_secrets";

    fetch(`/api/npcs/${currentScenario}/${npcId}/interact`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        interaction_type: interactionType,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          this.handleNPCResponse(data);
        }
      })
      .catch((error) => {
        console.error("Error interacting with NPC:", error);
        this.handleNPCResponse({
          success: true,
          response: "Merhaba! Nasılsın?",
          npc_name: "NPC",
          npc_title: "Villager",
        });
      });
  },

  // Handle NPC response
  handleNPCResponse: function (data) {
    const storyText = document.getElementById("story-text");
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
  loadFallbackNPCs: function () {
    console.log("🔄 Loading fallback NPCs...");
    this.currentNPCs = {
      detective_max: {
        name: "Detective Max",
        title: "Şehir Dedektifi",
        description:
          "Deneyimli bir dedektif. Şehirdeki gizemleri çözmek için yardım edebilir.",
      },
      neon: {
        name: "Neon",
        title: "Gizli Hacker",
        description: "Siber uzayın derinliklerinde yaşayan gizemli bir hacker.",
      },
    };
    this.displayNPCs();
  },
};

// QUEST SYSTEM
window.questSystem = {
  activeQuests: [],
  completedQuests: [],

  // Load available quests
  loadQuests: function () {
    console.log("📋 Loading available quests...");
    fetch("/api/quests/active")
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          this.activeQuests = data.quests || [];
          this.displayQuests();
        }
      })
      .catch((error) => {
        console.error("Error loading quests:", error);
        this.loadFallbackQuests();
      });
  },

  // Display quests in UI
  displayQuests: function () {
    const questContainer = document.getElementById("quest-container");
    if (!questContainer) {
      console.error("Quest container not found");
      return;
    }

    questContainer.innerHTML = "";

    this.activeQuests.forEach((quest) => {
      const questElement = document.createElement("div");
      questElement.className = "quest-item";
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
          <button onclick="window.questSystem.acceptQuest('${
            quest.id
          }')" class="quest-btn">Kabul Et</button>
          <button onclick="window.questSystem.viewQuestDetails('${
            quest.id
          }')" class="quest-btn">Detaylar</button>
        </div>
      `;
      questContainer.appendChild(questElement);
    });
  },

  // Accept a quest
  acceptQuest: function (questId) {
    console.log(`📋 Accepting quest: ${questId}`);

    fetch("/api/quests/accept", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        quest_id: questId,
        user_id: window.playerStats.currentUserId,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          console.log("✅ Quest accepted!");
          this.loadQuests(); // Refresh quest list
        }
      })
      .catch((error) => {
        console.error("Error accepting quest:", error);
      });
  },

  // View quest details
  viewQuestDetails: function (questId) {
    const quest = this.activeQuests.find((q) => q.id === questId);
    if (quest) {
      const storyText = document.getElementById("story-text");
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
              ${
                quest.rewards?.items
                  ? `<li>Eşyalar: ${quest.rewards.items.join(", ")}</li>`
                  : ""
              }
            </ul>
            <button onclick="window.questSystem.acceptQuest('${
              quest.id
            }')" class="quest-btn">Bu Görevi Kabul Et</button>
          </div>
        `;
      }
    }
  },

  // Load fallback quests if API fails
  loadFallbackQuests: function () {
    console.log("🔄 Loading fallback quests...");
    this.activeQuests = [
      {
        id: "investigate_healer",
        title: "Şifacının Sırrı",
        description:
          "Lydia'nın babasının neden değiştiğini araştır. Ejderha ile bağlantısı olabilir.",
        level: 1,
        rewards: { xp: 50, gold: 25, items: ["Şifacı İksiri"] },
      },
      {
        id: "dragon_knowledge",
        title: "Ejderha Bilgisi",
        description:
          "Shadow'dan ejderha hakkında daha fazla bilgi al. Kolyenin sırrını öğren.",
        level: 2,
        rewards: { xp: 75, gold: 50, items: ["Gizli Bilgi"] },
      },
    ];
    this.displayQuests();
  },
};

// Player Statistics System
window.loadPlayerStatistics = function () {
  console.log("📊 Loading player statistics...");

  fetch(`/api/player/statistics/${window.playerStats.currentUserId}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        window.playerStats = { ...window.playerStats, ...data.statistics };
        window.updateStatisticsDisplay();
      }
    })
    .catch((error) => {
      console.error("Error loading player statistics:", error);
    });
};

window.updatePlayerStatistics = function (statType, value, context = {}) {
  console.log(`📊 Updating ${statType}: ${value}`);

  fetch("/api/player/statistics/update", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: window.playerStats.currentUserId,
      stat_type: statType,
      value: value,
      context: context,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        window.playerStats = { ...window.playerStats, ...data.statistics };
        window.updateStatisticsDisplay();
      }
    })
    .catch((error) => {
      console.error("Error updating player statistics:", error);
    });
};

window.updateStatisticsDisplay = function () {
  const karmaElement = document.getElementById("player-karma");
  const reputationElement = document.getElementById("player-reputation");

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
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        window.gameState.skillPoints = data.progression.skill_points;
        window.gameState.unlockedSkills = data.progression.unlocked_skills;
        window.updateLevelDisplay();
        window.displayAvailableSkills();
      }
    })
    .catch((error) => {
      console.error("Error loading skill system:", error);
    });
};

window.loadAvailableSkills = function () {
  console.log("⚔️ Loading available skills...");

  fetch(`/api/skills/available/${window.playerStats.currentUserId}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        window.displayAvailableSkills(data.skills);
      }
    })
    .catch((error) => {
      console.error("Error loading available skills:", error);
    });
};

window.displayAvailableSkills = function (skills) {
  const skillsContainer = document.getElementById("available-skills");
  if (!skillsContainer) return;

  skillsContainer.innerHTML = "";

  if (skills && skills.length > 0) {
    skills.forEach((skill) => {
      const skillElement = document.createElement("div");
      skillElement.className = "skill-item";
      skillElement.innerHTML = `
        <div class="skill-header">
          <span class="skill-name">${skill.name}</span>
          <span class="skill-type">${skill.type}</span>
        </div>
        <div class="skill-description">${skill.description}</div>
        <div class="skill-requirements">
          <small>Gereksinimler: Seviye ${skill.requirements.level}, ${
        skill.requirements.skill_points
      } SP</small>
        </div>
        <button onclick="window.unlockSkill('${skill.id}')" class="skill-btn" ${
        !skill.can_unlock ? "disabled" : ""
      }>
          ${skill.can_unlock ? "Aç" : skill.unlock_message}
        </button>
      `;
      skillsContainer.appendChild(skillElement);
    });
  } else {
    skillsContainer.innerHTML = "<p>Henüz açılabilir beceri yok.</p>";
  }
};

window.displayUnlockedSkills = function () {
  const skillsContainer = document.getElementById("unlocked-skills");
  if (!skillsContainer) return;

  skillsContainer.innerHTML = "";

  if (window.gameState.unlockedSkills.length > 0) {
    window.gameState.unlockedSkills.forEach((skillId) => {
      const skillElement = document.createElement("div");
      skillElement.className = "skill-item unlocked";
      skillElement.innerHTML = `
        <div class="skill-header">
          <span class="skill-name">${skillId}</span>
          <span class="skill-level">Seviye ${
            window.gameState.skillLevels[skillId] || 1
          }</span>
        </div>
        <button onclick="window.useSkill('${skillId}')" class="skill-btn">Kullan</button>
      `;
      skillsContainer.appendChild(skillElement);
    });
  } else {
    skillsContainer.innerHTML = "<p>Henüz açılmış beceri yok.</p>";
  }
};

window.unlockSkill = function (skillId) {
  console.log(`⚔️ Unlocking skill: ${skillId}`);

  fetch("/api/skills/unlock", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: window.playerStats.currentUserId,
      skill_id: skillId,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
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
    .catch((error) => {
      console.error("Error unlocking skill:", error);
    });
};

window.useSkill = function (skillId) {
  console.log(`⚔️ Using skill: ${skillId}`);

  fetch("/api/skills/use", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: window.playerStats.currentUserId,
      skill_id: skillId,
      target: "enemy",
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        console.log("✅ Skill used successfully!");
        window.applySkillEffects(data.skill_result);
      } else {
        console.error("❌ Failed to use skill:", data.message);
      }
    })
    .catch((error) => {
      console.error("Error using skill:", error);
    });
};

window.applySkillEffects = function (skillResult) {
  const storyText = document.getElementById("story-text");
  if (storyText) {
    storyText.innerHTML = `
      <div class="skill-result">
        <h3>${skillResult.skill_name} Kullanıldı!</h3>
        <p>${skillResult.message}</p>
        <div class="skill-effects">
          ${Object.entries(skillResult.effects)
            .map(
              ([effect, value]) =>
                `<div class="effect">${effect}: ${value}</div>`
            )
            .join("")}
        </div>
      </div>
    `;
  }
};

// Level System
window.updateLevelDisplay = function () {
  const levelElement = document.getElementById("player-level");
  const xpElement = document.getElementById("player-xp");
  const skillPointsElement = document.getElementById("skill-points");

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
    5: { experience_required: 700, skill_points_gained: 2 },
  };

  return (
    levelRequirements[level] || {
      experience_required: 0,
      skill_points_gained: 0,
    }
  );
};

window.gainXP = function (xpAmount) {
  console.log(`⭐ Gaining ${xpAmount} XP`);

  fetch("/api/character/gain_xp", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: window.playerStats.currentUserId,
      xp: xpAmount,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        window.gameState.currentXP = data.total_xp;

        if (data.level_up.leveled_up) {
          window.showLevelUpNotification(
            data.level_up.new_level,
            data.level_up.skill_points_gained
          );
          window.gameState.currentLevel = data.level_up.new_level;
          window.gameState.skillPoints += data.level_up.skill_points_gained;
        }

        window.updateLevelDisplay();
      }
    })
    .catch((error) => {
      console.error("Error gaining XP:", error);
    });
};

window.showLevelUpNotification = function (newLevel, skillPointsGained) {
  const storyText = document.getElementById("story-text");
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
  const tabs = ["available", "unlocked"];
  tabs.forEach((t) => {
    const tabElement = document.getElementById(`skills-${t}-tab`);
    const contentElement = document.getElementById(`skills-${t}-content`);

    if (tabElement && contentElement) {
      if (t === tab) {
        tabElement.classList.add("active");
        contentElement.style.display = "block";
      } else {
        tabElement.classList.remove("active");
        contentElement.style.display = "none";
      }
    }
  });
};

// Theme switching
window.switchTheme = function (theme) {
  console.log(`🎨 Switching to ${theme} theme`);

  window.gameState.currentTheme = theme;

  // Update UI elements - use theme-tab class instead of theme-btn
  const themeTabs = document.querySelectorAll(".theme-tab");
  themeTabs.forEach((tab) => {
    tab.classList.remove("active");
  });

  // Find and activate the clicked tab
  const clickedTab = event.target;
  if (clickedTab && clickedTab.classList.contains("theme-tab")) {
    clickedTab.classList.add("active");
  }

  // Hide all theme content
  const themeContents = document.querySelectorAll(".theme-content");
  themeContents.forEach((content) => {
    content.style.display = "none";
  });

  // Show the selected theme content
  const selectedContent = document.getElementById(`${theme}-content`);
  if (selectedContent) {
    selectedContent.style.display = "block";
  }

  // Update character creation
  const characterCreation = document.getElementById("character-creation");
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

  // Remove selected class from all race list items
  const raceItems = document.querySelectorAll(".list-item");
  raceItems.forEach((item) => item.classList.remove("selected"));

  // Add selected class to selected button
  element.classList.add("selected");

  // Update game state
  window.gameState.characterRace = race;

  // Update stats based on race
  if (window.applyRaceClassToStats) {
    window.applyRaceClassToStats();
  }
};

window.selectClass = function (element, className) {
  console.log(`⚔️ Selected class: ${className}`);

  // Remove selected class from all class list items
  const classItems = document.querySelectorAll(".list-item");
  classItems.forEach((item) => item.classList.remove("selected"));

  // Add selected class to selected button
  element.classList.add("selected");

  // Update game state
  window.gameState.characterClass = className;

  // Update stats based on class
  if (window.applyRaceClassToStats) {
    window.applyRaceClassToStats();
  }
};

// Scenario selection
window.selectScenario = function (scenarioId) {
  console.log(`🎮 Selected scenario: ${scenarioId}`);

  window.gameState.currentScenario = scenarioId;

  // Hide scenario selection, show active game
  const scenarioSelection = document.getElementById("scenario-selection");
  const activeGame = document.getElementById("active-game");

  if (scenarioSelection && activeGame) {
    scenarioSelection.style.display = "none";
    activeGame.style.display = "block";
  }

  // Load scenario data
  window.startScenario(scenarioId);
};

// Start scenario function
window.startScenario = function (scenarioId) {
  console.log(`🚀 Starting scenario: ${scenarioId}`);

  // Load enhanced scenario data
  if (window.enhancedScenarioSystem) {
    window.enhancedScenarioSystem.loadEnhancedScenario(scenarioId);
  }

  // Load NPCs for this scenario
  if (window.npcSystem) {
    window.npcSystem.loadNPCs(scenarioId);
  }

  // Load quests for this scenario
  if (window.questSystem) {
    window.questSystem.loadQuests();
  }

  // Update UI
  const currentScenarioTitle = document.getElementById(
    "current-scenario-title"
  );
  if (currentScenarioTitle) {
    currentScenarioTitle.textContent = `Senaryo: ${scenarioId}`;
  }

  // Load initial story content
  window.loadStoryContent(scenarioId);
};

// Load story content
window.loadStoryContent = function (scenarioId) {
  console.log(`📖 Loading story content for: ${scenarioId}`);

  // For now, directly display the default story instead of trying to fetch from API
  // This ensures the story content is always displayed
  window.displayDefaultStory(scenarioId);

  // In the future, this could be enhanced to load from API:
  /*
  fetch(`/api/stories/${scenarioId}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        window.displayStoryNode(data.story);
      } else {
        // Fallback to default story
        window.displayDefaultStory(scenarioId);
      }
    })
    .catch((error) => {
      console.error("Error loading story:", error);
      // Fallback to default story
      window.displayDefaultStory(scenarioId);
    });
  */
};

// Display story node
window.displayStoryNode = function (storyNode) {
  const storyText = document.getElementById("story-text");
  const choicesGrid = document.getElementById("choices-grid");

  if (storyText) {
    storyText.innerHTML = storyNode.text || "Hikaye yükleniyor...";
  }

  if (choicesGrid && storyNode.choices) {
    choicesGrid.innerHTML = storyNode.choices
      .map(
        (choice) =>
          `<button class="choice-btn" onclick="window.makeChoice('${choice.id}')">${choice.text}</button>`
      )
      .join("");
  }
};

// Display default story
window.displayDefaultStory = function (scenarioId) {
  console.log(`📖 Displaying default story for: ${scenarioId}`);

  const storyText = document.getElementById("story-text");
  const choicesGrid = document.getElementById("choices-grid");

  if (!storyText || !choicesGrid) {
    console.error("Story display elements not found!");
    return;
  }

  // Default story content based on scenario
  let storyContent = "";
  let choices = [];

  if (
    scenarioId === "living_dragon_hunt" ||
    scenarioId === "dragon_hunters_path"
  ) {
    storyContent = `
      <div class="story-content">
        <h3>🐉 Ejderha Avcısının Yolu</h3>
        <p>Güneş batarken köyün üzerinde kızıl bir gölge beliriyor. Kızıl Alev adıyla bilinen ejderha gökyüzünde uçuyor ve alevler saçarak köyü yakıyor. Sen ejderha avcısısın ve bu tehlikeli görevde her şeyi riske atacaksın. Köy meydanında yaşlı bir adam seni bekliyor - köy reisi Aldric.</p>
        
        <div class="story-atmosphere">
          <div class="atmosphere-item">
            <span class="atmosphere-icon">🌅</span>
            <span>Güneş batımının kızıl ışıkları</span>
          </div>
          <div class="atmosphere-item">
            <span class="atmosphere-icon">🔥</span>
            <span>Yanan köy evleri</span>
          </div>
          <div class="atmosphere-item">
            <span class="atmosphere-icon">🐉</span>
            <span>Uzak ejderha uğultusu</span>
          </div>
        </div>
      </div>
    `;

    choices = [
      { id: "talk_to_aldric", text: "Aldric ile konuş", icon: "👴" },
      { id: "track_dragon", text: "Hemen ejderhayı takip et", icon: "🐉" },
      { id: "gather_info", text: "Köylülerden bilgi topla", icon: "👥" },
      { id: "find_healer", text: "Şifacıyı ara", icon: "🏥" },
    ];
  } else if (scenarioId === "magical_forest_mysteries") {
    storyContent = `
      <div class="story-content">
        <h3>🌳 Büyülü Ormanın Gizemleri</h3>
        <p>Büyülü ormanın derinliklerinde gizli sırlar ve antik ruhlar var. Ormanın derinliklerinde kaybolmuş bir büyücü köyü ve unutulmuş bir tapınak keşfedeceksin. Her adımda yeni bir gizem ve tehlikeli kararlar seni bekliyor.</p>
      </div>
    `;

    choices = [
      { id: "explore_forest", text: "Ormanı keşfet", icon: "🌲" },
      { id: "find_village", text: "Büyücü köyünü ara", icon: "🏘️" },
      { id: "search_temple", text: "Tapınağı ara", icon: "⛪" },
      { id: "talk_spirits", text: "Ruhlarla konuş", icon: "👻" },
    ];
  } else if (scenarioId === "warhammer_imperial_crisis") {
    storyContent = `
      <div class="story-content">
        <h3>🚀 Warhammer 40K: İmparatorluk Krizi</h3>
        <p>Hive şehrinde AI ve büyük şirketler arasında gizli savaş var. Şehrin savunması için tehlikeli görevler üstleneceksin. Her seçim seni değiştirecek, her karar dünyayı değiştirecek.</p>
      </div>
    `;

    choices = [
      { id: "defend_hive", text: "Hive'ı savun", icon: "🛡️" },
      { id: "investigate_ai", text: "AI'ı araştır", icon: "🤖" },
      { id: "negotiate", text: "Müzakere et", icon: "🤝" },
      { id: "infiltrate", text: "Sızma yap", icon: "🕵️" },
    ];
  } else if (scenarioId === "cyberpunk_hive_city") {
    storyContent = `
      <div class="story-content">
        <h3>🌃 Cyberpunk: Şehir Gizemleri</h3>
        <p>Cyberpunk şehrinde gizli sırlar ve tehlikeli komplolar var. Şehrin derinliklerinde kaybolmuş teknolojiler ve unutulmuş sırlar keşfedeceksin. Her seçim seni değiştirecek, her karar dünyayı değiştirecek.</p>
      </div>
    `;

    choices = [
      { id: "hack_system", text: "Sistemi hackle", icon: "💻" },
      { id: "find_tech", text: "Teknoloji ara", icon: "🔧" },
      { id: "meet_contacts", text: "Bağlantıları bul", icon: "👥" },
      { id: "escape_city", text: "Şehirden kaç", icon: "🏃" },
    ];
  } else {
    // Default story for any other scenario
    storyContent = `
      <div class="story-content">
        <h3>🎮 Macera Başlıyor</h3>
        <p>Senaryo başlıyor! Seçimlerin hikayeyi şekillendirecek. Dikkatli ol ve doğru kararları ver.</p>
      </div>
    `;

    choices = [
      { id: "continue", text: "Devam et", icon: "➡️" },
      { id: "explore", text: "Keşfet", icon: "🔍" },
      { id: "rest", text: "Dinlen", icon: "😴" },
      { id: "inventory", text: "Envanter", icon: "🎒" },
    ];
  }

  // Display story content
  storyText.innerHTML = storyContent;

  // Display choice buttons
  choicesGrid.innerHTML = choices
    .map(
      (choice) => `
    <button class="choice-btn" onclick="window.makeChoice('${choice.id}')">
      <span class="choice-icon">${choice.icon}</span>
      <span class="choice-text">${choice.text}</span>
    </button>
  `
    )
    .join("");

  console.log(`✅ Story displayed with ${choices.length} choices`);
};

// Make choice function
window.makeChoice = function (choiceId) {
  console.log(`🎯 Player made choice: ${choiceId}`);

  // Add choice to game history
  window.gameState.playerChoices.push({
    choiceId: choiceId,
    timestamp: new Date().toISOString(),
    scenario: window.gameState.currentScenario,
  });

  // Process choice and show next story node
  window.processChoice(choiceId);
};

// Process choice and show next story
window.processChoice = function (choiceId) {
  console.log(`🔄 Processing choice: ${choiceId}`);

  // Show loading state
  const storyText = document.getElementById("story-text");
  const choicesGrid = document.getElementById("choices-grid");

  if (storyText) {
    storyText.innerHTML =
      '<div class="loading-story">Hikaye yükleniyor...</div>';
  }

  if (choicesGrid) {
    choicesGrid.innerHTML =
      '<div class="loading-choices">Seçenekler yükleniyor...</div>';
  }

  // Simulate story progression (in real implementation, this would load from API)
  setTimeout(() => {
    window.showNextStoryNode(choiceId);
  }, 1000);
};

// Show next story node
window.showNextStoryNode = function (previousChoiceId) {
  console.log(`📖 Showing next story node after choice: ${previousChoiceId}`);

  const storyText = document.getElementById("story-text");
  const choicesGrid = document.getElementById("choices-grid");

  // Generate next story based on previous choice
  let nextStory = "";
  let nextChoices = [];

  if (previousChoiceId === "talk_to_aldric") {
    nextStory = `
      <div class="story-content">
        <h3>👴 Aldric ile Konuşma</h3>
        <p>Aldric'in yüzünde hem umut hem de derin bir keder var. "Ejderha Avcısı! Sonunda geldin. Köyümüzün umudu sensin. Her gece o sesi duyuyorum... Kızıl Alev'in nefesini... Ama bir şeyler ters gitti. Ejderha artık sadece yıkım getirmiyor, bir mesaj veriyor gibi."</p>
      </div>
    `;

    nextChoices = [
      { id: "ask_about_message", text: "Mesaj hakkında sor", icon: "💬" },
      { id: "ask_about_history", text: "Geçmişi öğren", icon: "📚" },
      { id: "ask_for_help", text: "Yardım iste", icon: "🤝" },
      { id: "leave_aldric", text: "Aldric'i bırak", icon: "👋" },
    ];
  } else if (previousChoiceId === "track_dragon") {
    nextStory = `
      <div class="story-content">
        <h3>🐉 Ejderha Takibi</h3>
        <p>Ejderhanın izini sürmeye başlıyorsun. Gökyüzünde kızıl bir gölge görüyorsun ve uzaktan ejderha uğultusu geliyor. Ejderha köyün etrafında dönüyor ve belirli binaları hedef alıyor.</p>
      </div>
    `;

    nextChoices = [
      { id: "follow_dragon", text: "Ejderhayı takip et", icon: "🐉" },
      { id: "observe_pattern", text: "Deseni gözlemle", icon: "👁️" },
      { id: "prepare_attack", text: "Saldırıya hazırlan", icon: "⚔️" },
      { id: "return_village", text: "Köye dön", icon: "🏘️" },
    ];
  } else {
    // Default next story
    nextStory = `
      <div class="story-content">
        <h3>🎮 Hikaye Devam Ediyor</h3>
        <p>Seçimin hikayeyi şekillendirdi. Şimdi ne yapmak istiyorsun?</p>
      </div>
    `;

    nextChoices = [
      { id: "continue_story", text: "Hikayeye devam et", icon: "➡️" },
      { id: "explore_area", text: "Bölgeyi keşfet", icon: "🔍" },
      { id: "check_inventory", text: "Envanteri kontrol et", icon: "🎒" },
      { id: "save_game", text: "Oyunu kaydet", icon: "💾" },
    ];
  }

  // Display next story
  if (storyText) {
    storyText.innerHTML = nextStory;
  }

  // Display next choices
  if (choicesGrid) {
    choicesGrid.innerHTML = nextChoices
      .map(
        (choice) => `
      <button class="choice-btn" onclick="window.makeChoice('${choice.id}')">
        <span class="choice-icon">${choice.icon}</span>
        <span class="choice-text">${choice.text}</span>
      </button>
    `
      )
      .join("");
  }

  console.log(`✅ Next story displayed with ${nextChoices.length} choices`);
};

// AI Scenario Generation
window.generateAIScenario = function () {
  console.log("🤖 Generating AI scenario...");

  const theme = window.gameState.currentTheme;
  const difficulty = window.gameState.currentDifficulty;

  fetch("/api/ai/generate_scenario", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      theme: theme,
      difficulty: difficulty,
      scenario_type: "adventure",
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        console.log("✅ AI scenario generated!");
        window.addAIScenarioToGrid(
          data.scenario.id,
          data.scenario.title,
          data.scenario.description,
          data.scenario.difficulty
        );
      }
    })
    .catch((error) => {
      console.error("Error generating AI scenario:", error);
    });
};

// Helper functions for AI scenarios
function generateScenarioTitle(theme, difficulty) {
  const titles = {
    fantasy: {
      easy: ["Küçük Macera", "Orman Yolculuğu", "Köy Görevi"],
      medium: ["Ejderha Avı", "Büyücü Kulesi", "Antik Tapınak"],
      hard: ["Kaos Savaşı", "Karanlık Lord", "Efsanevi Macera"],
    },
    scifi: {
      easy: ["Uzay İstasyonu", "Robot Tamiri", "Koloni Görevi"],
      medium: ["AI Kontrolü", "Uzay Savaşı", "Teknoloji Araştırması"],
      hard: ["Galaktik Savaş", "Kara Delik", "Siber Savaş"],
    },
    cyberpunk: {
      easy: ["Şehir Görevi", "Hack İşi", "Underground"],
      medium: ["MegaCorp Infiltration", "AI Rebellion", "Neon Savaşı"],
      hard: ["Matrix Savaşı", "Siber Apocalypse", "Digital Hell"],
    },
    warhammer: {
      easy: ["İmperial Görev", "Chaos Temizliği", "Hive Patrol"],
      medium: ["Space Marine Mission", "Ork Invasion", "Eldar Encounter"],
      hard: ["Chaos Lord Battle", "Tyranid Swarm", "Necron Awakening"],
    },
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
    warhammer: `Seviye ${level} Warhammer 40K savaşı. Chaos ve İmperium arasında seçim yap.`,
  };

  return descriptions[theme] || descriptions.fantasy;
}

function generateScenarioChoices(theme, difficulty) {
  const baseChoices = [
    { text: "İleri git", effect: "exploration + 5" },
    { text: "Dikkatli ol", effect: "defense + 3" },
    { text: "Saldır", effect: "attack + 5" },
  ];

  return baseChoices;
}

function addAIScenarioToGrid(scenarioId, title, description, difficulty) {
  const aiScenariosGrid = document.getElementById("ai-scenarios-grid");
  if (!aiScenariosGrid) return;

  const scenarioCard = document.createElement("div");
  scenarioCard.className = "scenario-card ai-generated";
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
  if (typeof window.switchTheme === "function") {
    window.switchTheme("fantasy");
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

// Initialize enhanced scenario system
window.initializeEnhancedScenarioSystem = function () {
  console.log("🎮 Initializing enhanced scenario system...");

  // Load default scenario
  window.enhancedScenarioSystem.loadEnhancedScenario("dragon_hunters_path");

  // Initialize NPC and Quest systems
  if (window.npcSystem) {
    window.npcSystem.loadNPCs("dragon_hunters_path");
  }

  if (window.questSystem) {
    window.questSystem.loadQuests();
  }

  console.log("✅ Enhanced scenario system initialized!");
};

// Initialize when page loads
window.addEventListener("load", function () {
  console.log("🔄 Page loaded, initializing enhanced systems...");
  setTimeout(window.initializeEnhancedScenarioSystem, 1000);
});

// AI Scenario Generation Functions
window.generateAIScenario = function () {
  console.log("🤖 Generating AI scenario...");

  const theme = document.getElementById("ai-theme").value;
  const difficulty = document.getElementById("ai-difficulty").value;
  const title = document.getElementById("ai-title").value;
  const character = document.getElementById("ai-character").value;
  const description = document.getElementById("ai-description").value;

  if (!theme || !difficulty || !title || !character || !description) {
    alert("❌ Lütfen tüm alanları doldurun!");
    return;
  }

  const resultContainer = document.getElementById("ai-result");
  const generatedContent = document.getElementById(
    "generated-scenario-content"
  );

  // Show loading
  resultContainer.style.display = "block";
  generatedContent.innerHTML =
    '<div style="text-align: center; color: #9c27b0; font-style: italic;">🤖 AI senaryo üretiyor...</div>';

  // Simulate AI generation
  setTimeout(() => {
    const scenario = createAIScenario(
      theme,
      difficulty,
      title,
      character,
      description
    );
    generatedContent.innerHTML = scenario;
  }, 2000);
};

window.clearAIScenario = function () {
  document.getElementById("ai-theme").value = "";
  document.getElementById("ai-difficulty").value = "";
  document.getElementById("ai-title").value = "";
  document.getElementById("ai-character").value = "";
  document.getElementById("ai-description").value = "";
  document.getElementById("ai-result").style.display = "none";
};

window.saveAIScenario = function () {
  alert("✅ AI senaryo başarıyla kaydedildi!");
  // Burada senaryo kaydetme API'si çağrılabilir
};

// Play AI Scenario function
window.playAIScenario = function () {
  const details = document.getElementById("ai-scenario-details");
  const scenarioId = details.dataset.scenarioId;

  console.log("🎮 AI Senaryo oynatılıyor:", scenarioId);

  // Hide AI scenario details
  details.style.display = "none";

  // Hide scenario selection, show active game
  const scenarioSelection = document.getElementById("scenario-selection");
  const activeGame = document.getElementById("active-game");

  if (scenarioSelection && activeGame) {
    scenarioSelection.style.display = "none";
    activeGame.style.display = "block";
  }

  // Set current scenario
  window.gameState.currentScenario = scenarioId;
  window.gameState.scenarioType = "ai_generated";

  // Update scenario title
  const currentScenarioTitle = document.getElementById(
    "current-scenario-title"
  );
  if (currentScenarioTitle) {
    currentScenarioTitle.textContent = `AI Senaryo: ${scenarioId}`;
  }

  // Load story content
  window.loadStoryContent(scenarioId);

  showNotification("🎮 AI Senaryo başlatıldı!", "success");
};

function createAIScenario(theme, difficulty, title, character, description) {
  const themes = {
    fantasy: "🏰",
    warhammer: "⚔️",
    cyberpunk: "🌃",
    scifi: "🚀",
    horror: "👻",
  };

  const difficulties = {
    easy: "🟢 Kolay",
    medium: "🟡 Orta",
    hard: "🔴 Zor",
    extreme: "⚫ Aşırı Zor",
  };

  const playTime = Math.floor(Math.random() * 180) + 60;

  return `
    <div style="margin-bottom: 20px;">
      <h4 style="color: #9c27b0; margin-bottom: 10px;">${themes[theme]} ${title}</h4>
      <p><strong>Ana Karakter:</strong> ${character}</p>
      <p><strong>Açıklama:</strong> ${description}</p>
      <p><strong>Zorluk:</strong> ${difficulties[difficulty]}</p>
      <p><strong>Tahmini Süre:</strong> ${playTime} dakika</p>
    </div>
    
    <div style="background: rgba(156, 39, 176, 0.1); padding: 15px; border-radius: 6px; margin-bottom: 15px;">
      <h5 style="color: #9c27b0; margin-bottom: 10px;">🎯 Ana Görevler:</h5>
      <ul style="color: #ccc; margin: 0; padding-left: 20px;">
        <li>${character} olarak dünyayı keşfet</li>
        <li>Gizemli tehdidi araştır</li>
        <li>Güçlü müttefikler bul</li>
        <li>Final savaşında zafer kazan</li>
      </ul>
    </div>
    
    <div style="background: rgba(156, 39, 176, 0.1); padding: 15px; border-radius: 6px;">
      <h5 style="color: #9c27b0; margin-bottom: 10px;">🎭 Hikaye Elementleri:</h5>
      <ul style="color: #ccc; margin: 0; padding-left: 20px;">
        <li>Detaylı karakter gelişimi</li>
        <li>Çoklu son seçenekleri</li>
        <li>NPC ilişki sistemi</li>
        <li>Dinamik dünya olayları</li>
        <li>Seviye atlama sistemi</li>
      </ul>
    </div>
  `;
}

// Test function for debugging
window.testButtonFunctionality = function () {
  console.log("🧪 Testing button functionality...");

  // Test theme switching
  const themeTabs = document.querySelectorAll(".theme-tab");
  console.log(`Found ${themeTabs.length} theme tabs`);

  // Test race selection
  const raceItems = document.querySelectorAll(".list-item");
  console.log(`Found ${raceItems.length} list items`);

  // Test if functions are defined
  console.log("switchTheme function:", typeof window.switchTheme);
  console.log("selectRace function:", typeof window.selectRace);
  console.log("selectClass function:", typeof window.selectClass);

  return {
    themeTabs: themeTabs.length,
    listItems: raceItems.length,
    functionsDefined: {
      switchTheme: typeof window.switchTheme,
      selectRace: typeof window.selectRace,
      selectClass: typeof window.selectClass,
    },
  };
};

// Auto-test on load
window.addEventListener("load", function () {
  setTimeout(() => {
    console.log("🧪 Running auto-test...");
    window.testButtonFunctionality();
  }, 2000);
});

// AI Senaryo Üretim Fonksiyonları - Sadece Çizgi Roman Kampanyası
window.generateAIScenario = async function () {
  console.log("🧙‍♂️ Çizgi Roman Kampanyası yükleniyor...");

  // Durum göstergesini güncelle
  updateAIStatus("generating", "Çizgi Roman Kampanyası hazırlanıyor...");
  showAIProgress();

  try {
    // Çizgi Roman Kampanyası verilerini yükle
    const response = await fetch("/api/ai-scenarios");
    if (response.ok) {
      const scenarios = await response.json();
      const comicCampaign = scenarios.find(
        (s) => s.id === "comic_universe_frp_campaign"
      );

      if (comicCampaign) {
        console.log("✅ Çizgi Roman Kampanyası yüklendi:", comicCampaign);

        // Mevcut senaryoları temizle ve sadece bu kampanyayı göster
        const grid = document.getElementById("ai-scenarios-grid");
        const placeholder = document.getElementById("ai-scenario-placeholder");

        if (placeholder) {
          placeholder.style.display = "none";
        }

        // Grid'i temizle
        grid.innerHTML = "";

        // Çizgi Roman Kampanyasını ekle
        addComicCampaignToList(comicCampaign);

        // Durum göstergesini güncelle
        updateAIStatus("ready", "Çizgi Roman Kampanyası Hazır");
        hideAIProgress();

        // Başarı mesajı göster
        showNotification("🎭 Çizgi Roman Kampanyası yüklendi!", "success");
      } else {
        throw new Error("Çizgi Roman Kampanyası bulunamadı");
      }
    } else {
      throw new Error("Kampanya yükleme başarısız");
    }
  } catch (error) {
    console.error("❌ Çizgi Roman Kampanyası yükleme hatası:", error);
    updateAIStatus("error", "Hata oluştu");
    hideAIProgress();
    showNotification("❌ Kampanya yükleme başarısız!", "error");
  }
};

// Çizgi Roman Kampanyasını listeye ekle
window.addComicCampaignToList = function (campaign) {
  const grid = document.getElementById("ai-scenarios-grid");

  const campaignCard = document.createElement("div");
  campaignCard.className = "ai-scenario-card comic-campaign";
  campaignCard.onclick = () => showComicCampaignDetails(campaign);

  campaignCard.innerHTML = `
    <div class="ai-scenario-header">
      <h4>${campaign.title}</h4>
      <span class="difficulty ${campaign.difficulty}">${getDifficultyText(
    campaign.difficulty
  )}</span>
    </div>
    <div class="ai-scenario-meta">
      <span>🎭 ${getThemeText(campaign.theme)}</span>
      <span>⭐ ${campaign.min_level}-${campaign.max_level}</span>
      <span>⏱️ ${campaign.duration} dk (${
    campaign.campaign_details.total_duration
  })</span>
    </div>
    <div class="ai-scenario-description">
      ${campaign.description.substring(0, 200)}${
    campaign.description.length > 200 ? "..." : ""
  }
    </div>
    <div class="campaign-features">
      <span>📖 ${campaign.campaign_details.total_scenes} Sahne</span>
      <span>🎯 ${campaign.campaign_details.total_choices} Seçim</span>
      <span>🏁 Çoklu Son</span>
    </div>
    <div class="ai-scenario-footer">
      <span>🎭 Çizgi Roman Evrenlerinden İlham</span>
      <span>📅 ${new Date().toLocaleDateString()}</span>
    </div>
  `;

  grid.appendChild(campaignCard);
};

// Çizgi Roman Kampanyası detaylarını göster
window.showComicCampaignDetails = function (campaign) {
  const details = document.getElementById("ai-scenario-details");
  const title = document.getElementById("ai-scenario-title");
  const theme = document.getElementById("ai-detail-theme");
  const difficulty = document.getElementById("ai-detail-difficulty");
  const level = document.getElementById("ai-detail-level");
  const duration = document.getElementById("ai-detail-duration");
  const description = document.getElementById("ai-detail-description");
  const nodes = document.getElementById("ai-detail-nodes");

  // Detayları doldur
  title.textContent = campaign.title;
  theme.textContent = getThemeText(campaign.theme);
  difficulty.textContent = getDifficultyText(campaign.difficulty);
  level.textContent = `${campaign.min_level}-${campaign.max_level}`;
  duration.textContent = `${campaign.duration} dakika (${campaign.campaign_details.total_duration})`;
  description.textContent = campaign.description;

  // Kampanya özelliklerini listele
  nodes.innerHTML = `
    <div class="campaign-features-list">
      <h5>🎭 Kampanya Özellikleri:</h5>
      <ul>
        <li>📖 Toplam ${campaign.campaign_details.total_scenes} sahne</li>
        <li>🎯 ${campaign.campaign_details.total_choices} farklı seçim</li>
        <li>🏁 Çoklu son seçenekleri</li>
        <li>👤 Karakter gelişimi sistemi</li>
        <li>👥 NPC etkileşimleri</li>
        <li>⚔️ Savaş sistemi</li>
        <li>📈 Beceri ilerlemesi</li>
      </ul>
    </div>
    <div class="universe-list">
      <h5>🌍 Evrenler:</h5>
      <ul>
        <li>🦸‍♂️ Marvel Evreni - Süper Kahramanların Dünyası</li>
        <li>🦇 DC Evreni - Karanlık Kahramanların Gecesi</li>
        <li>🧬 X-Men Evreni - Mutantların Savaşı</li>
        <li>🕷️ Spider-Man Evreni - Örümcek Ağının Gizemleri</li>
        <li>⚡ Avengers Evreni - Dünyayı Kurtaran Kahramanlar</li>
      </ul>
    </div>
  `;

  // Detayları göster
  details.style.display = "block";

  // Kampanya ID'sini sakla
  details.dataset.scenarioId = campaign.id;
};

// Form temizleme fonksiyonunu güncelle
window.clearAIForm = function () {
  // Form alanlarını temizle
  const form = document.querySelector(".ai-scenario-form");
  if (form) {
    const inputs = form.querySelectorAll("input, select, textarea");
    inputs.forEach((input) => {
      if (input.type === "select-one") {
        input.value = input.options[0].value;
      } else {
        input.value = "";
      }
    });
  }

  showNotification("🗑️ Form temizlendi!", "info");
};

// AI senaryolarını yükle - sadece çizgi roman kampanyası
window.loadAIScenarios = async function () {
  try {
    const response = await fetch("/api/ai-scenarios");
    if (response.ok) {
      const scenarios = await response.json();
      console.log("📚 AI Senaryolar yüklendi:", scenarios);

      // Mevcut senaryoları temizle
      const grid = document.getElementById("ai-scenarios-grid");
      const placeholder = document.getElementById("ai-scenario-placeholder");

      // Sadece çizgi roman kampanyasını bul
      const comicCampaign = scenarios.find(
        (s) => s.id === "comic_universe_frp_campaign"
      );

      if (comicCampaign) {
        if (placeholder) {
          placeholder.style.display = "none";
        }

        // Grid'i temizle
        grid.innerHTML = "";

        // Sadece çizgi roman kampanyasını ekle
        addComicCampaignToList(comicCampaign);
      } else {
        if (placeholder) {
          placeholder.style.display = "block";
          placeholder.innerHTML = `
            <div class="placeholder-content">
              <div class="placeholder-icon">🎭</div>
              <h5>Çizgi Roman Kampanyası Yükleniyor</h5>
              <p>Çizgi Roman Evrenlerinden İlham alan kampanya hazırlanıyor...</p>
            </div>
          `;
        }
      }
    }
  } catch (error) {
    console.error("❌ AI Senaryolar yüklenirken hata:", error);
  }
};

// Eksik fonksiyonları ekle
window.updateAIStatus = function (status, text) {
  const statusDot = document.getElementById("status-dot");
  const statusText = document.getElementById("status-text");

  if (statusText) {
    statusText.textContent = text;
  }

  if (statusDot) {
    switch (status) {
      case "ready":
        statusDot.textContent = "🟢";
        statusDot.style.animation = "none";
        break;
      case "generating":
        statusDot.textContent = "🟡";
        statusDot.style.animation = "pulse 1s infinite";
        break;
      case "error":
        statusDot.textContent = "🔴";
        statusDot.style.animation = "none";
        break;
    }
  }
};

window.showAIProgress = function () {
  const progress = document.getElementById("ai-progress");
  const progressFill = document.getElementById("progress-fill");
  const progressText = document.getElementById("progress-text");

  if (progress) {
    progress.style.display = "block";
  }

  if (progressFill && progressText) {
    // Simüle edilmiş ilerleme
    let currentProgress = 0;
    const interval = setInterval(() => {
      currentProgress += Math.random() * 15;
      if (currentProgress > 100) currentProgress = 100;

      progressFill.style.width = currentProgress + "%";
      progressText.textContent = `Kampanya hazırlanıyor... ${Math.round(
        currentProgress
      )}%`;

      if (currentProgress >= 100) {
        clearInterval(interval);
      }
    }, 500);
  }
};

window.hideAIProgress = function () {
  const progress = document.getElementById("ai-progress");
  if (progress) {
    progress.style.display = "none";
  }
};

window.closeAIScenarioDetails = function () {
  const details = document.getElementById("ai-scenario-details");
  if (details) {
    details.style.display = "none";
  }
};

window.editAIScenario = function () {
  const details = document.getElementById("ai-scenario-details");
  const scenarioId = details.dataset.scenarioId;

  console.log("✏️ Çizgi Roman Kampanyası düzenleniyor:", scenarioId);

  // Düzenleme formunu göster (gelecekte implement edilecek)
  showNotification("✏️ Düzenleme özelliği yakında gelecek!", "info");
};

window.deleteAIScenario = function () {
  const details = document.getElementById("ai-scenario-details");
  const scenarioId = details.dataset.scenarioId;

  if (
    confirm("Bu Çizgi Roman Kampanyasını silmek istediğinizden emin misiniz?")
  ) {
    console.log("🗑️ Çizgi Roman Kampanyası siliniyor:", scenarioId);

    // Kampanya kartını bul ve sil
    const campaignCard = document.querySelector(
      `[data-scenario-id="${scenarioId}"]`
    );
    if (campaignCard) {
      campaignCard.remove();
    }

    // Detayları kapat
    closeAIScenarioDetails();

    // Eğer hiç kampanya kalmadıysa placeholder'ı göster
    const grid = document.getElementById("ai-scenarios-grid");
    if (grid && grid.children.length === 0) {
      const placeholder = document.getElementById("ai-scenario-placeholder");
      if (placeholder) {
        placeholder.style.display = "block";
      }
    }

    showNotification("🗑️ Çizgi Roman Kampanyası silindi!", "success");
  }
};

// Yardımcı fonksiyonlar
function getThemeText(theme) {
  const themes = {
    fantasy: "Fantasy",
    cyberpunk: "Cyberpunk",
    warhammer: "Warhammer 40K",
    "post-apocalyptic": "Post-Apocalyptic",
    steampunk: "Steampunk",
    horror: "Horror",
    comic_universe: "Çizgi Roman Evreni",
  };
  return themes[theme] || theme;
}

function getDifficultyText(difficulty) {
  const difficulties = {
    easy: "Kolay",
    medium: "Orta",
    hard: "Zor",
    epic: "Epik",
  };
  return difficulties[difficulty] || difficulty;
}

window.showNotification = function (message, type = "info") {
  // Basit bildirim sistemi
  const notification = document.createElement("div");
  notification.className = `notification notification-${type}`;
  notification.textContent = message;
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 12px 20px;
    border-radius: 8px;
    color: white;
    font-weight: bold;
    z-index: 1000;
    animation: slideInRight 0.3s ease;
  `;

  // Tip bazlı renkler
  switch (type) {
    case "success":
      notification.style.background =
        "linear-gradient(45deg, #4CAF50, #45a049)";
      break;
    case "error":
      notification.style.background =
        "linear-gradient(45deg, #f44336, #d32f2f)";
      break;
    case "warning":
      notification.style.background =
        "linear-gradient(45deg, #ff9800, #f57c00)";
      break;
    default:
      notification.style.background =
        "linear-gradient(45deg, #2196F3, #1976D2)";
  }

  document.body.appendChild(notification);

  // 3 saniye sonra kaldır
  setTimeout(() => {
    notification.style.animation = "slideOutRight 0.3s ease";
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
    }, 300);
  }, 3000);
};

// CSS Animasyonları için stil ekle
const style = document.createElement("style");
style.textContent = `
  @keyframes slideInRight {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }
  
  @keyframes slideOutRight {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
  }
`;
document.head.appendChild(style);

// Sayfa yüklendiğinde AI senaryolarını yükle
document.addEventListener("DOMContentLoaded", function () {
  // Initialize file upload system
  window.initializeFileUpload();
  loadAIScenarios();
});

// Dosya Yükleme ve AI Senaryo Üretim Sistemi
window.initializeFileUpload = function () {
  const fileInput = document.getElementById("file-input");
  const uploadArea = document.getElementById("upload-area");
  const fileStatus = document.getElementById("file-status");

  if (fileInput) {
    fileInput.addEventListener("change", handleFileSelect);
  }

  if (uploadArea) {
    uploadArea.addEventListener("dragover", handleDragOver);
    uploadArea.addEventListener("drop", handleFileDrop);
  }
};

window.handleFileSelect = function (event) {
  const file = event.target.files[0];
  if (file) {
    uploadFile(file);
  }
};

window.handleDragOver = function (event) {
  event.preventDefault();
  event.currentTarget.style.borderColor = "#4CAF50";
};

window.handleFileDrop = function (event) {
  event.preventDefault();
  const file = event.dataTransfer.files[0];
  if (file) {
    uploadFile(file);
  }
  event.currentTarget.style.borderColor = "#666";
};

window.uploadFile = async function (file) {
  console.log("📁 Dosya yükleniyor:", file.name);

  const fileStatus = document.getElementById("file-status");
  if (fileStatus) {
    fileStatus.textContent = `Yükleniyor: ${file.name}...`;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("/api/upload-file", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const result = await response.json();
      console.log("✅ Dosya yüklendi ve senaryo oluşturuldu:", result);

      if (fileStatus) {
        fileStatus.textContent = `✅ ${file.name} - Senaryo oluşturuldu!`;
      }

      // Yeni senaryoyu listeye ekle
      if (result.scenario) {
        addAIScenarioToList(result.scenario);
        showNotification(
          `🎭 ${file.name} dosyasından senaryo oluşturuldu!`,
          "success"
        );
      }

      // Dosya listesini güncelle
      updateFilesList(file.name);
    } else {
      const error = await response.json();
      console.error("❌ Dosya yükleme hatası:", error);

      if (fileStatus) {
        fileStatus.textContent = `❌ Hata: ${error.error}`;
      }

      showNotification(`❌ Dosya yükleme hatası: ${error.error}`, "error");
    }
  } catch (error) {
    console.error("❌ Dosya yükleme hatası:", error);

    if (fileStatus) {
      fileStatus.textContent = `❌ Bağlantı hatası`;
    }

    showNotification("❌ Dosya yükleme başarısız", "error");
  }
};

window.updateFilesList = function (fileName) {
  const filesList = document.getElementById("files-list");
  if (filesList) {
    const fileItem = document.createElement("div");
    fileItem.className = "file-item";
    fileItem.innerHTML = `
      <span class="file-name">📄 ${fileName}</span>
      <span class="file-status">✅ Senaryo oluşturuldu</span>
    `;
    filesList.appendChild(fileItem);
  }
};

// AI Senaryo Üretim Fonksiyonları - Dinamik Dosya Tabanlı
window.generateAIScenario = async function () {
  console.log("🧙‍♂️ Dinamik senaryo üretimi başlatılıyor...");

  // Durum göstergesini güncelle
  updateAIStatus(
    "generating",
    "Dosya analiz ediliyor ve senaryo oluşturuluyor..."
  );
  showAIProgress();

  try {
    // Mevcut AI senaryolarını yükle
    const response = await fetch("/api/ai-scenarios");
    if (response.ok) {
      const scenarios = await response.json();

      console.log("✅ Mevcut senaryolar yüklendi:", scenarios.length);

      // Mevcut senaryoları temizle ve yenilerini göster
      clearAIScenariosList();

      if (scenarios.length > 0) {
        scenarios.forEach((scenario) => {
          addAIScenarioToList(scenario);
        });

        updateAIStatus("ready", `${scenarios.length} senaryo yüklendi`);
        showNotification(
          `🎭 ${scenarios.length} senaryo başarıyla yüklendi!`,
          "success"
        );
      } else {
        showAIScenarioPlaceholder();
        updateAIStatus("ready", "Henüz senaryo yok - Dosya yükleyin!");
      }
    } else {
      throw new Error("Senaryolar yüklenemedi");
    }
  } catch (error) {
    console.error("❌ Senaryo yükleme hatası:", error);
    updateAIStatus("error", "Senaryo yükleme hatası");
    showNotification("❌ Senaryo yükleme başarısız", "error");
  } finally {
    hideAIProgress();
  }
};

window.clearAIScenariosList = function () {
  const scenariosGrid = document.getElementById("ai-scenarios-grid");
  if (scenariosGrid) {
    scenariosGrid.innerHTML = "";
  }
};

window.showAIScenarioPlaceholder = function () {
  const scenariosGrid = document.getElementById("ai-scenarios-grid");
  if (scenariosGrid) {
    scenariosGrid.innerHTML = `
      <div class="ai-scenario-placeholder">
        <div class="placeholder-content">
          <div class="placeholder-icon">📁</div>
          <h5>Dosya Yükleyin</h5>
          <p>Senaryo oluşturmak için PDF veya TXT dosyası yükleyin. Her dosya otomatik olarak analiz edilip senaryoya dönüştürülecek.</p>
          <button class="upload-file-btn" onclick="document.getElementById('file-input').click()">
            📁 Dosya Seç
          </button>
        </div>
      </div>
    `;
  }
};

window.addAIScenarioToList = function (scenario) {
  console.log("📝 Senaryo listeye ekleniyor:", scenario.title);

  const scenariosGrid = document.getElementById("ai-scenarios-grid");
  if (!scenariosGrid) return;

  // Placeholder'ı temizle
  const placeholder = scenariosGrid.querySelector(".ai-scenario-placeholder");
  if (placeholder) {
    placeholder.remove();
  }

  const scenarioCard = document.createElement("div");
  scenarioCard.className = "scenario-card ai-scenario-card";
  scenarioCard.onclick = () => showAIScenarioDetails(scenario);

  // Tema bazlı renk sınıfı
  const themeClass = getThemeClass(scenario.theme);
  scenarioCard.classList.add(themeClass);

  scenarioCard.innerHTML = `
    <div class="scenario-header">
      <h4>${scenario.title}</h4>
      <span class="difficulty ${scenario.difficulty}">${getDifficultyText(
    scenario.difficulty
  )}</span>
    </div>
    <div class="scenario-info">
      <div class="info-item">
        <span class="info-label">🎨 Tema:</span>
        <span class="info-value">${getThemeText(scenario.theme)}</span>
      </div>
      <div class="info-item">
        <span class="info-label">⭐ Seviye:</span>
        <span class="info-value">${scenario.min_level}-${
    scenario.max_level
  }</span>
      </div>
      <div class="info-item">
        <span class="info-label">⏱️ Süre:</span>
        <span class="info-value">${scenario.duration} dk</span>
      </div>
      ${
        scenario.word_count
          ? `
      <div class="info-item">
        <span class="info-label">📊 Kelime:</span>
        <span class="info-value">${scenario.word_count}</span>
      </div>
      `
          : ""
      }
    </div>
    <p class="scenario-description">${scenario.description}</p>
    <div class="scenario-source">
      <span class="source-icon">📁</span>
      <span class="source-text">${scenario.file_source || "AI Üretilen"}</span>
    </div>
  `;

  scenariosGrid.appendChild(scenarioCard);
};

window.getThemeClass = function (theme) {
  const themeClasses = {
    fantasy: "fantasy-theme",
    cyberpunk: "cyberpunk-theme",
    horror: "horror-theme",
    adventure: "adventure-theme",
    comic_universe: "comic-theme",
  };
  return themeClasses[theme] || "default-theme";
};

window.getThemeText = function (theme) {
  const themeTexts = {
    fantasy: "Fantasy",
    cyberpunk: "Cyberpunk",
    horror: "Korku",
    adventure: "Macera",
    comic_universe: "Çizgi Roman",
  };
  return themeTexts[theme] || theme;
};

window.getDifficultyText = function (difficulty) {
  const difficultyTexts = {
    easy: "Kolay",
    medium: "Orta",
    hard: "Zor",
    epic: "Epik",
  };
  return difficultyTexts[difficulty] || difficulty;
};
