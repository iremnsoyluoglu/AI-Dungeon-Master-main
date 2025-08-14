// COMPLETE GAME SYSTEM - ENHANCED WITH RICH NPCS AND BACKSTORY
console.log("=== ENHANCED GAME SYSTEM LOADED ===");

// CHARACTER DATA STRUCTURE
window.currentCharacter = {
  name: "Aelindra",
  race: "",
  class: "",
  level: 1,
  xp: 0,
  maxXp: 100,
  hp: 100,
  maxHp: 100,
  mana: 50,
  maxMana: 50,
};

// GLOBAL FUNCTION DECLARATIONS
window.switchTheme = function (theme) {
  console.log("✅ SWITCH THEME:", theme);

  // Remove active class from all theme tabs
  document.querySelectorAll(".theme-tab").forEach((tab) => {
    if (tab) tab.classList.remove("active");
  });

  // Add active class to selected theme tab (with null check)
  const selectedTab = document.querySelector(
    `[onclick="switchTheme('${theme}')"]`
  );
  if (selectedTab) {
    selectedTab.classList.add("active");
  }

  // Hide all theme content
  document.querySelectorAll(".theme-content").forEach((content) => {
    if (content) content.style.display = "none";
  });

  // Show selected theme content (with null check)
  const themeContent = document.getElementById(`${theme}-content`);
  if (themeContent) {
    themeContent.style.display = "block";
  }

  // Hide all scenario categories
  document.querySelectorAll(".scenario-category").forEach((category) => {
    if (category) category.style.display = "none";
  });

  // Show selected theme scenarios (with null check)
  const themeScenarios = document.getElementById(theme + "-scenarios");
  if (themeScenarios) {
    themeScenarios.style.display = "block";
  }

  // Show AI generated scenarios for all themes
  const aiScenarios = document.getElementById("ai-generated-scenarios");
  if (aiScenarios) {
    aiScenarios.style.display = "block";
  }

  if (npcSystem && npcSystem.initializeNPCs) {
    npcSystem.initializeNPCs(theme);
  }

  if (npcSystem && npcSystem.updateNPCDisplay) {
    npcSystem.updateNPCDisplay();
  }
};

window.selectRace = function (element, race) {
  console.log("✅ SELECT RACE:", race);

  // Check if element exists
  if (!element) {
    console.warn("Element not found for race selection");
    return;
  }

  const themeContent = element.closest(".theme-content");
  if (!themeContent) {
    console.warn("Theme content not found");
    return;
  }

  // Remove selected class from all race items
  themeContent
    .querySelectorAll(".race-class-list:nth-child(1) .list-item")
    .forEach((item) => {
      if (item) item.classList.remove("selected");
    });

  // Add selected class to clicked element
  element.classList.add("selected");

  // Update character data
  window.currentCharacter.race = race;
  updateCharacterPanel();
};

window.selectClass = function (element, className) {
  console.log("✅ SELECT CLASS:", className);

  // Check if element exists
  if (!element) {
    console.warn("Element not found for class selection");
    return;
  }

  const themeContent = element.closest(".theme-content");
  if (!themeContent) {
    console.warn("Theme content not found");
    return;
  }

  // Remove selected class from all class items
  themeContent
    .querySelectorAll(".race-class-list:nth-child(2) .list-item")
    .forEach((item) => {
      if (item) item.classList.remove("selected");
    });

  // Add selected class to clicked element
  element.classList.add("selected");

  // Update character data
  window.currentCharacter.class = className;
  updateCharacterPanel();
};

window.selectScenario = function (scenarioId) {
  console.log("✅ SELECT SCENARIO:", scenarioId);
  const scenarioSelection = document.getElementById("scenario-selection");
  const activeGame = document.getElementById("active-game");

  if (scenarioSelection && activeGame) {
    scenarioSelection.style.display = "none";
    activeGame.style.display = "block";
    startScenario(scenarioId);
  } else {
    console.warn("❌ Required elements not found for scenario selection");
  }
};

window.generateAIScenario = function () {
  console.log("✅ GENERATE AI SCENARIO");

  // Add null checks for form elements
  const aiTheme = document.getElementById("ai-theme");
  const aiDifficulty = document.getElementById("ai-difficulty");
  const aiLevel = document.getElementById("ai-level");

  const theme = aiTheme ? aiTheme.value : "fantasy";
  const difficulty = aiDifficulty ? aiDifficulty.value : "medium";
  const level = aiLevel ? aiLevel.value : "1";

  const generateBtn = document.querySelector(".generate-btn");
  if (!generateBtn) {
    console.warn("❌ Generate button not found");
    return;
  }

  const originalText = generateBtn.textContent;
  generateBtn.textContent = "🔄 Üretiliyor...";
  generateBtn.disabled = true;

  // AI Senaryo Üretici - Gerçek senaryo üretir
  setTimeout(() => {
    if (generateBtn) {
      generateBtn.textContent = originalText;
      generateBtn.disabled = false;
    }

    // Yeni senaryo oluştur
    const scenarioId = `ai_scenario_${Date.now()}`;
    const scenarioTitle = generateScenarioTitle(theme, difficulty);
    const scenarioDescription = generateScenarioDescription(
      theme,
      difficulty,
      level
    );

    // Senaryoyu scenarios objesine ekle
    scenarios[scenarioId] = {
      title: scenarioTitle,
      story: {
        start: {
          text: scenarioDescription,
          choices: generateScenarioChoices(theme, difficulty),
        },
      },
    };

    // AI senaryoları grid'ine ekle
    addAIScenarioToGrid(
      scenarioId,
      scenarioTitle,
      scenarioDescription,
      difficulty
    );

    alert(
      `🎲 Yeni senaryo üretildi: "${scenarioTitle}"\nAI Üretilen kategorisinde bulabilirsiniz!`
    );
  }, 2000);
};

// AI Senaryo Üretici Yardımcı Fonksiyonları
function generateScenarioTitle(theme, difficulty) {
  const themes = {
    fantasy: [
      "Ejderha",
      "Büyücü",
      "Ork",
      "Elf",
      "Cüce",
      "Kale",
      "Orman",
      "Mağara",
      "Şehir",
      "Köy",
    ],
    warhammer: [
      "Chaos",
      "Ork",
      "Eldar",
      "Space Marine",
      "Inquisitor",
      "Tech-Priest",
      "Imperial Guard",
      "Hive City",
      "Forge World",
      "Death World",
    ],
    cyberpunk: [
      "Netrunner",
      "Corporate",
      "Street",
      "Hive",
      "Matrix",
      "Cyberware",
      "Gang",
      "Fixer",
      "Rocker",
      "Nomad",
    ],
  };

  const difficulties = {
    easy: ["Macera", "Keşif", "Yolculuk", "Bulma"],
    medium: ["Görev", "Savaş", "Araştırma", "Kurtarma"],
    hard: ["Savaş", "Kaos", "Tehlike", "Kriz"],
  };

  const themeWords = themes[theme] || themes.fantasy;
  const difficultyWords = difficulties[difficulty] || difficulties.medium;

  const randomTheme = themeWords[Math.floor(Math.random() * themeWords.length)];
  const randomDifficulty =
    difficultyWords[Math.floor(Math.random() * difficultyWords.length)];

  return `${randomTheme} ${randomDifficulty}`;
}

function generateScenarioDescription(theme, difficulty, level) {
  const descriptions = {
    fantasy: {
      easy: "Sakin bir günde başlayan macera. Köyünüzde garip olaylar oluyor ve siz bu sırrı çözmeye karar veriyorsunuz.",
      medium:
        "Tehlikeli bir görev sizi bekliyor. Düşmanlar pusuda ve sadece sizin cesaretiniz köyü kurtarabilir.",
      hard: "Karanlık güçler köyünüzü tehdit ediyor. Bu sadece bir savaş değil, hayatta kalma mücadelesi.",
    },
    warhammer: {
      easy: "İmperium'un bir dünyasında görev yapıyorsunuz. Sapkınlık izleri var ve siz bunları araştırmaya başlıyorsunuz.",
      medium:
        "Chaos tehdidi büyüyor. İmperium için savaşmanız gerekiyor. Düşmanlar her yerde.",
      hard: "Sapkınlık yayılıyor. İmperium'un adaleti için savaşacağız. Bu bir ölüm kalım meselesi.",
    },
    cyberpunk: {
      easy: "Hive City'nin alt katmanlarında bir macera başlıyor. Teknoloji ve insanlık çatışıyor.",
      medium:
        "Corporate sırları ve tehlikeli oyunlar. Bu şehirde hayatta kalmak için akıllı olmalısınız.",
      hard: "Matrix'in derinliklerinde karanlık sırlar var. Şirketler savaşıyor ve siz ortada kalıyorsunuz.",
    },
  };

  return descriptions[theme]?.[difficulty] || descriptions.fantasy.medium;
}

function generateScenarioChoices(theme, difficulty) {
  const baseChoices = [
    { text: "İleri git", nextNode: "continue" },
    { text: "Araştır", nextNode: "investigate" },
    { text: "Savaş", nextNode: "fight" },
  ];

  if (difficulty === "hard") {
    baseChoices.push({ text: "Kaç", nextNode: "flee" });
  }

  return baseChoices;
}

function addAIScenarioToGrid(scenarioId, title, description, difficulty) {
  const aiScenariosGrid = document.getElementById("ai-scenarios-grid");
  if (!aiScenariosGrid) return;

  const scenarioCard = document.createElement("div");
  scenarioCard.className = "scenario-card ai-generated";
  scenarioCard.onclick = () => window.selectScenario(scenarioId);

  scenarioCard.innerHTML = `
    <div class="scenario-header">
      <h4>🧙‍♂️ ${title}</h4>
      <span class="difficulty ${difficulty}">${difficulty}</span>
    </div>
    <p>${description}</p>
    <div class="ai-info">
      <small>🤖 AI tarafından üretildi</small>
    </div>
  `;

  aiScenariosGrid.appendChild(scenarioCard);
}

// ENHANCED NPC SYSTEM WITH QUESTS
window.npcSystem = {
  currentDialog: null,
  activeQuests: [],

  npcs: {
    fantasy: {
      lydia: {
        name: "Lydia",
        role: "Şifacının Kızı",
        personality: "Cesur ve meraklı",
        relationship: "Dost",
        portrait: "👩‍⚕️",
        backstory:
          "Köyün şifacısının kızı. Babasının değişimini fark eden ilk kişi.",
        dialogue: {
          greeting:
            "Merhaba! Babam son zamanlarda çok değişti... Sanki başka biri olmuş gibi. Size yardım etmek istiyorum.",
          help: "Size yardım etmek istiyorum. Babamın ne yaptığını öğrenmeliyiz. Ejderha ile ilgili bir şeyler biliyor olabilir.",
          concern:
            "Bu ejderha... konuşuyor! Bu imkansız! Ama babam da son zamanlarda garip şeyler söylüyor.",
        },
        quests: [
          {
            id: "investigate_healer",
            title: "Şifacının Sırrı",
            description:
              "Lydia'nın babasının neden değiştiğini araştır. Ejderha ile bağlantısı olabilir.",
            reward: "50 XP + Şifacı İksiri",
            type: "investigation",
            status: "available",
          },
        ],
      },
      shadow: {
        name: "Shadow",
        role: "Gizemli Yolcu",
        personality: "Gizemli ve bilge",
        relationship: "Müttefik",
        portrait: "🧙‍♂️",
        backstory:
          "Köye yakın zamanda gelen gizemli bir yolcu. Ejderha avcılığı konusunda bilgili.",
        dialogue: {
          greeting:
            "Ejderha avcısı... sonunda geldin. Uzun zamandır seni bekliyordum.",
          wisdom:
            "Ejderhalar sadece yok edilmez, anlaşılır. Bu ejderha özel bir durumda.",
          warning:
            "Kolyenin gücü... dikkatli olmalısın. Ejderha onu arıyor ve tehlikeli olabilir.",
        },
        quests: [
          {
            id: "dragon_knowledge",
            title: "Ejderha Bilgisi",
            description:
              "Shadow'dan ejderha hakkında daha fazla bilgi al. Kolyenin sırrını öğren.",
            reward: "75 XP + Gizli Bilgi",
            type: "knowledge",
            status: "available",
          },
        ],
      },
      villageElder: {
        name: "Köy Reisi Aldric",
        role: "Köy Lideri",
        personality: "Endişeli ve kararlı",
        relationship: "Güvenilir",
        portrait: "👴",
        backstory:
          "50 yıldır köyü yöneten yaşlı lider. Ejderha tehdidinden çok endişeli.",
        dialogue: {
          greeting:
            "Ejderha Avcısı! Köyümüzü kurtar! Her gece o sesi duyuyorum... Kızıl Alev'in nefesini...",
          fear: "Her gece o sesi duyuyorum... Kızıl Alev'in nefesini... Köyümüz tehlikede!",
          hope: "Sen bizi kurtaracaksın, değil mi? Köyümüzün umudu sensin.",
        },
        quests: [
          {
            id: "protect_village",
            title: "Köyü Koru",
            description:
              "Ejderhayı durdur ve köyü kurtar. Köyün hazinesi senin olacak.",
            reward: "100 XP + Köy Hazinesi",
            type: "main",
            status: "available",
          },
        ],
      },
    },
    warhammer: {
      commissar: {
        name: "Commissar Yarrick",
        role: "İmperial Komiser",
        personality: "Sert ve disiplinli",
        relationship: "Lider",
        portrait: "🎖️",
        backstory:
          "İmperium'un en saygın komiserlerinden biri. Sapkınlığa karşı acımasız.",
        dialogue: {
          greeting:
            "Ave Imperator! Görevimiz açık ve net. Sapkınlığı temizleyeceğiz!",
          order:
            "Sapkınları temizleyeceğiz! İmperium'un iradesi budur! Dikkatli ol, asker.",
          warning:
            "Dikkatli ol, asker. Sapkınlık her yerde pusuda bekliyor. İmperium için savaşacağız.",
        },
        quests: [
          {
            id: "purge_chaos",
            title: "Sapkınlığı Temizle",
            description:
              "Chaos kültünü bulup yok et. İmperium'un adaleti için savaş.",
            reward: "150 XP + İmperial Onur",
            type: "main",
            status: "available",
          },
        ],
      },
      techPriest: {
        name: "Tech-Priest Magos",
        role: "Teknoloji Rahibi",
        personality: "Mantıklı ve gizemli",
        relationship: "Müttefik",
        portrait: "⚙️",
        backstory:
          "Adeptus Mechanicus'un üyesi. Makinelerin ruhunu anlayan bilge.",
        dialogue: {
          greeting:
            "Omnissiah'ın selamı üzerinize olsun. Makineler bize gerçeği söyler.",
          wisdom:
            "Makineler bize gerçeği söyler. Dinlemeyi bilmek gerekir. Bu sapkınlık teknolojik olabilir.",
          concern:
            "Bu sapkınlık... teknolojik bir kökeni olabilir. Makinelerin ruhunu araştırmalıyız.",
        },
        quests: [
          {
            id: "machine_secret",
            title: "Makinelerin Sırrı",
            description:
              "Sapkınlığın teknolojik kökenini araştır. Makinelerin ruhunu anla.",
            reward: "80 XP + Teknoloji Bilgisi",
            type: "investigation",
            status: "available",
          },
        ],
      },
      inquisitor: {
        name: "Inquisitor Eisenhorn",
        role: "İmperial İnquisitor",
        personality: "Kararlı ve gizemli",
        relationship: "Lider",
        portrait: "🔍",
        backstory:
          "Ordo Hereticus'un üyesi. Sapkınlığı kökünden temizlemeye yemin etmiş.",
        dialogue: {
          greeting:
            "İmperium'un adaleti burada! Sapkınlığı bulacağız ve yok edeceğiz.",
          mission:
            "Sapkınlığı bulacağız ve yok edeceğiz. Bu benim yeminim. İmperium için çalışacağız.",
          warning:
            "Dikkatli ol. Sapkınlık bulaşıcıdır. Her yerde pusuda bekliyor.",
        },
        quests: [
          {
            id: "inquisitor_mission",
            title: "İnquisitor Görevi",
            description:
              "Sapkınlığın kaynağını bul ve yok et. İmperium'un adaleti için.",
            reward: "200 XP + İnquisitor Onuru",
            type: "main",
            status: "available",
          },
        ],
      },
    },
    cyberpunk: {
      netrunner: {
        name: "Netrunner Zero",
        role: "Siber Uzay Ustası",
        personality: "Teknolojik ve gizemli",
        relationship: "Müttefik",
        portrait: "🤖",
        backstory:
          "Şehrin en iyi netrunner'ı. Matrix'in derinliklerinde yaşayan hacker.",
        dialogue: {
          greeting:
            "Siber uzaya hoş geldin, chummer. Matrix'te size yardım edebilirim.",
          help: "Matrix'te size yardım edebilirim. Ama bir bedeli var. Bu şehirde güvenebileceğin tek şey kodun.",
          warning:
            "Bu şehirde güvenebileceğin tek şey kodun. Şirketler her yerde.",
        },
        quests: [
          {
            id: "matrix_secret",
            title: "Matrix Sırrı",
            description:
              "Matrix'in derinliklerinde gizli bir sır var. Onu bul ve şirketlerin planını öğren.",
            reward: "90 XP + Siber Bilgi",
            type: "hacking",
            status: "available",
          },
        ],
      },
      fixer: {
        name: "Fixer Rogue",
        role: "Şehir Aracısı",
        personality: "Pratik ve güvenilir",
        relationship: "Dost",
        portrait: "🕵️",
        backstory: "Şehrin en iyi fixer'ı. Herkes onu tanır ve güvenir.",
        dialogue: {
          greeting:
            "Ne işin var, chummer? Bu şehirde olan biten her şeyi bilirim.",
          info: "Bu şehirde olan biten her şeyi bilirim. Fiyatı uygunsa. Şirketler tehlikeli oyunlar oynuyor.",
          advice:
            "Bu şehirde hayatta kalmak için akıllı olmalısın. Şirketler her yerde.",
        },
        quests: [
          {
            id: "city_secret",
            title: "Şehir Sırrı",
            description:
              "Şehrin gizli sırlarını keşfet. Şirketlerin planını öğren.",
            reward: "70 XP + Şehir Bilgisi",
            type: "investigation",
            status: "available",
          },
        ],
      },
      corporate: {
        name: "Corporate Agent",
        role: "Şirket Ajanı",
        personality: "Soğuk ve hesaplı",
        relationship: "Düşman",
        portrait: "👔",
        backstory:
          "Büyük bir şirketin ajanı. Şehrin sırlarını korumaya yemin etmiş.",
        dialogue: {
          greeting:
            "Şirket çıkarları her şeyden önce gelir. Bu bilgileri paylaşırsan sonuçlarına katlanırsın.",
          threat:
            "Bu bilgileri paylaşırsan sonuçlarına katlanırsın. Şirket her yerde.",
          warning: "Şirket her yerde. Kaçamazsın. Bizimle çalışmak zorundasın.",
        },
        quests: [
          {
            id: "corporate_mission",
            title: "Şirket Görevi",
            description:
              "Şirket için çalış ve şehrin sırlarını koru. Ama dikkatli ol.",
            reward: "60 XP + Şirket Desteği",
            type: "corporate",
            status: "available",
          },
        ],
      },
    },
  },

  initializeNPCs: function (theme) {
    console.log("✅ INITIALIZE NPCS for theme:", theme);
    const npcGrid = document.getElementById("npc-grid");
    if (!npcGrid) {
      console.warn("❌ NPC grid not found");
      return;
    }

    npcGrid.innerHTML = "";
    const themeNPCs = this.npcs[theme];
    if (!themeNPCs) {
      console.warn("❌ No NPCs found for theme:", theme);
      return;
    }

    Object.keys(themeNPCs).forEach((npcKey) => {
      const npc = themeNPCs[npcKey];
      const npcCard = document.createElement("div");
      npcCard.className = "npc-card";
      npcCard.innerHTML = `
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
          <div style="font-size: 2.5em;">${npc.portrait}</div>
          <div>
            <h4>${npc.name}</h4>
            <p><strong>Rol:</strong> ${npc.role}</p>
            <p><strong>Kişilik:</strong> ${npc.personality}</p>
            <p><strong>İlişki:</strong> ${npc.relationship}</p>
          </div>
        </div>
        <p style="font-style: italic; color: #aaa; margin-bottom: 15px;">${npc.backstory}</p>
        <button onclick="npcSystem.startDialog('${theme}', '${npcKey}')" style="width: 100%;">
          💬 Konuş
        </button>
      `;
      npcGrid.appendChild(npcCard);
    });
  },

  updateNPCDisplay: function () {
    console.log("✅ UPDATE NPC DISPLAY");
    // NPC display update logic can be added here
  },

  startDialog: function (theme, npcKey) {
    console.log("✅ START DIALOG:", theme, npcKey);
    const npc = this.npcs[theme][npcKey];
    if (!npc) {
      console.error("❌ NPC not found:", npcKey);
      return;
    }

    this.currentDialog = { theme, npcKey, npc };
    this.showDialogPanel();
    this.displayDialog("greeting");
  },

  showDialogPanel: function () {
    const dialogPanel = document.getElementById("npc-dialog-panel");
    if (dialogPanel) {
      dialogPanel.style.display = "block";
    }
  },

  hideDialogPanel: function () {
    const dialogPanel = document.getElementById("npc-dialog-panel");
    if (dialogPanel) {
      dialogPanel.style.display = "none";
    }
    this.currentDialog = null;
  },

  displayDialog: function (dialogType) {
    if (!this.currentDialog) return;

    const { npc } = this.currentDialog;
    const dialogName = document.getElementById("dialog-npc-name");
    const dialogText = document.getElementById("dialog-text");
    const dialogChoices = document.getElementById("dialog-choices");
    const npcPortrait = document.getElementById("npc-portrait");

    if (dialogName) dialogName.textContent = npc.name;
    if (npcPortrait) npcPortrait.textContent = npc.portrait;
    if (dialogText)
      dialogText.textContent =
        npc.dialogue[dialogType] || npc.dialogue.greeting;

    // Create dialog choices
    if (dialogChoices) {
      dialogChoices.innerHTML = "";

      const choices = [
        { text: "Daha fazla bilgi iste", action: "info" },
        { text: "Görevler hakkında sor", action: "quest" },
        { text: "Vedalaş", action: "goodbye" },
      ];

      choices.forEach((choice) => {
        const button = document.createElement("button");
        button.className = "dialog-choice-btn";
        button.textContent = choice.text;
        button.onclick = () => this.handleDialogChoice(choice.action);
        dialogChoices.appendChild(button);
      });
    }
  },

  handleDialogChoice: function (action) {
    switch (action) {
      case "info":
        this.displayDialog("help");
        break;
      case "quest":
        this.showQuestOffer();
        break;
      case "goodbye":
        this.hideDialogPanel();
        break;
    }
  },

  showQuestOffer: function () {
    if (!this.currentDialog) return;

    const { npc } = this.currentDialog;
    const questInfo = document.getElementById("quest-info");
    const questDetails = document.getElementById("quest-details");

    if (questInfo && questDetails) {
      const availableQuests = npc.quests.filter(
        (quest) => quest.status === "available"
      );

      if (availableQuests.length > 0) {
        const quest = availableQuests[0];
        questDetails.innerHTML = `
          <div class="quest-title">${quest.title}</div>
          <div class="quest-description">${quest.description}</div>
          <div class="quest-reward">Ödül: ${quest.reward}</div>
        `;
        questInfo.style.display = "block";
      } else {
        questDetails.innerHTML = "<p>Şu anda mevcut görev yok.</p>";
        questInfo.style.display = "block";
      }
    }
  },

  acceptQuest: function () {
    if (!this.currentDialog) return;

    const { npc } = this.currentDialog;
    const availableQuests = npc.quests.filter(
      (quest) => quest.status === "available"
    );

    if (availableQuests.length > 0) {
      const quest = availableQuests[0];
      quest.status = "active";

      // Add to active quests
      this.activeQuests.push({
        ...quest,
        npcName: npc.name,
        theme: this.currentDialog.theme,
      });

      // Update quest panel
      this.updateQuestPanel();

      // Give XP reward
      const xpMatch = quest.reward.match(/(\d+) XP/);
      if (xpMatch) {
        const xp = parseInt(xpMatch[1]);
        window.currentCharacter.xp += xp;
        updateCharacterPanel();
      }

      alert(
        `✅ Görev kabul edildi: ${quest.title}\n${quest.reward} kazandınız!`
      );
      this.hideDialogPanel();
    }
  },

  declineQuest: function () {
    alert("❌ Görev reddedildi.");
    this.hideDialogPanel();
  },

  updateQuestPanel: function () {
    const questPanel = document.getElementById("quest-panel");
    if (!questPanel) return;

    if (this.activeQuests.length === 0) {
      questPanel.innerHTML = "<h4>📋 Quests</h4><p>No active quests</p>";
      return;
    }

    let questHTML = "<h4>📋 Aktif Görevler</h4>";
    this.activeQuests.forEach((quest) => {
      questHTML += `
        <div class="active-quest">
          <div class="quest-title">${quest.title}</div>
          <div class="quest-description">${quest.description}</div>
          <div class="quest-reward">Ödül: ${quest.reward}</div>
        </div>
      `;
    });

    questPanel.innerHTML = questHTML;
  },
};

// SCENARIO DATA
window.scenarios = {
  living_dragon_hunt: {
    title: "🐉 Yaşayan Ejderha Avı",
    story: {
      start: {
        text: "Köyün kenarında duruyorsun. Ufukta Kızıl Alev'in nefesini görüyorsun. Köy reisi Aldric sana yaklaşıyor, yüzünde endişe var. 'Ejderha Avcısı! Köyümüzü kurtar! Her gece o sesi duyuyorum... Kızıl Alev'in nefesini...'",
        choices: [
          {
            text: "Köyü korumaya yemin ederim!",
            nextNode: "village_pledge",
          },
          {
            text: "Önce daha fazla bilgi istiyorum.",
            nextNode: "gather_info",
          },
          {
            text: "Bu iş için ne ödül var?",
            nextNode: "negotiate_reward",
          },
        ],
      },
      village_pledge: {
        text: "Aldric'nin yüzü aydınlanıyor. 'Kahraman! Köyümüzün umudu sensin. Şifacı Lydia size yardım edecek. Babası son zamanlarda çok değişti...' Lydia yaklaşıyor, gözlerinde endişe var.",
        choices: [
          {
            text: "Lydia ile konuş",
            nextNode: "talk_lydia",
          },
          {
            text: "Şifacının evini araştır",
            nextNode: "investigate_healer",
          },
          {
            text: "Doğrudan ejderhaya git",
            nextNode: "direct_dragon",
          },
        ],
      },
      gather_info: {
        text: "Bilge bir yaklaşım. Aldric anlatmaya başlıyor: 'Ejderha bir ay önce geldi. Ama garip olan şu ki, kimseye saldırmıyor. Sadece... konuşuyor. Gizemli bir yolcu Shadow da köye geldi, ejderha hakkında bilgili.'",
        choices: [
          {
            text: "Shadow ile konuş",
            nextNode: "talk_shadow",
          },
          {
            text: "Ejderhanın konuştuğu şeyi öğren",
            nextNode: "dragon_speech",
          },
          {
            text: "Köyü korumaya yemin et",
            nextNode: "village_pledge",
          },
        ],
      },
      negotiate_reward: {
        text: "Aldric kaşlarını çatıyor ama anlayışla yaklaşıyor. 'Adil bir istek. Köyün hazinesi sizin. Ayrıca... gizemli bir kolye var. Ejderha onu arıyor gibi.'",
        choices: [
          {
            text: "Kolyeyi göster",
            nextNode: "show_necklace",
          },
          {
            text: "Önce ejderhayı gör",
            nextNode: "see_dragon",
          },
          {
            text: "Anlaşmayı kabul et",
            nextNode: "accept_deal",
          },
        ],
      },
      retreat_plan: {
        title: "Geri Çekilme ve Plan Yapma",
        text: `Ejderha'ya karşı geri çekiliyorsun. Lydia ile birlikte güvenli bir yere kaçıyorsunuz.

"Bu ejderha... konuşuyor! Bu imkansız!" diye bağırıyor Lydia.

"Evet, bu çok garip. Ama ejderha beni tanıyor gibi görünüyor."

Lydia: "Babam son zamanlarda çok değişti. Belki de bununla ilgili bir şey var."

"Şifacı? Ne demek istiyorsun?"

"Babam gece yarısı garip dualar okuyor. Eski tapınakta zaman geçiriyor. Belki de ejderha'yı o uyandırdı."

Bu bilgi çok önemli. Şifacı ejderha'nın uyanmasından sorumlu olabilir.`,
        choices: [
          { text: "Şifacıyı araştır", nextNode: "investigate_healer" },
          { text: "Köylülerden bilgi al", nextNode: "gather_info" },
          { text: "Eski tapınağı araştır", nextNode: "investigate_temple" },
          { text: "Ejderhayla tekrar konuş", nextNode: "talk_to_dragon" },
          { text: "Köyü koruma planı yap", nextNode: "defend_village" },
        ],
      },

      // EKSİK NODE'LAR - DEVAM
      question_healer: {
        title: "Şifacıyı Sorgulama",
        text: `Şifacının evine gidiyorsun. Kapıyı çaldığında Lydia açıyor.

"Babam... babam çok garip davranıyor. Son zamanlarda hiç uyumuyor."

Şifacı içeriden çıkıyor. Yüzünde yorgunluk ve delilik ifadesi var: "Kim o? Ejderha avcısı mı?"

"Evet, ben ejderha avcısıyım. Son zamanlarda neden değiştiğinizi öğrenmek istiyorum."

Şifacı gülüyor: "Değişmedim! Sadece gücümü geri kazandım! 100 yıl önce ejderha avcısıydım. Ejderhayı öldürdüm ama gücünü alamadım. Şimdi kolyeyi buldum ve güç benim olacak!"`,
        choices: [
          { text: "Şifacıyla savaş", nextNode: "fight_healer" },
          { text: "Kolyeyi geri iste", nextNode: "demand_necklace" },
          { text: "Lydia'yı koru", nextNode: "protect_lydia" },
          { text: "Şifacıyı ikna et", nextNode: "convince_healer" },
          { text: "Kaç", nextNode: "escape_healer" },
        ],
      },

      spy_at_night: {
        title: "Gece Yarısı Gözetleme",
        text: `Gece yarısı, eski tapınağa gizlice yaklaşıyorsun. İçeriden garip ışıklar ve sesler geliyor.

Pencereden baktığında, şifacının tapınağın ortasında büyük bir altar kurduğunu görüyorsun. Üzerinde ejderha kanı ve garip semboller var.

Şifacı, kolyeyi elinde tutuyor ve garip dualar okuyor: "Ejderha gücü! Bana gel! Ben senin efendinim!"

Aniden, kolye parlamaya başlıyor ve şifacı gülüyor: "Evet! Güç geliyor! Artık ben ejderha avcısıyım!"

Bu çok tehlikeli bir durum. Şifacı kolyenin gücünü kullanarak ejderha gücü kazanmaya çalışıyor.`,
        choices: [
          { text: "Şifacıya saldır", nextNode: "attack_healer" },
          { text: "Kolyeyi çal", nextNode: "steal_necklace" },
          { text: "Ejderhayı uyar", nextNode: "warn_dragon" },
          { text: "Köylüleri uyar", nextNode: "warn_villagers" },
          { text: "Plan yap", nextNode: "plan_attack" },
        ],
      },

      defend_village: {
        title: "Köyü Koruma Planı",
        text: `Köy reisi Aldric ile birlikte köyü koruma planı yapıyorsunuz.

"Ejderha her gece geliyor. Köylüleri güvenli yerlere taşımalıyız," diyorsun.

Aldric: "Ama nereye? Dağlar tehlikeli, orman tehlikeli. Burada kalmalıyız."

"O zaman köyü savunmalıyız. Köylüleri silahlandırmalıyız."

Genç çiftçi Tom: "Ben savaşabilirim! Köyümü koruyacağım!"

Diğer köylüler de seninle birlikte savaşmaya hazır olduklarını söylüyorlar. Köyü savunmak için bir plan yapmalısınız.`,
        choices: [
          { text: "Köylüleri silahlandır", nextNode: "arm_villagers" },
          { text: "Tuzaklar kur", nextNode: "set_traps" },
          { text: "Güvenli yerler hazırla", nextNode: "prepare_safe_places" },
          { text: "Ejderhayı beklet", nextNode: "wait_for_dragon" },
          { text: "Şifacıyı ara", nextNode: "question_healer" },
        ],
      },

      fight_healer: {
        title: "Şifacı Savaşı",
        text: `Şifacı, kolyenin gücüyle size saldırıyor. Alevler ve büyüler odada uçuşuyor. Lydia, babasının bu haline şok olmuş.

"Baba! Lütfen dur! Bu sen değilsin!"

Şifacı gülüyor: "Ben her zaman böyleydim! 100 yıl önce ejderhayı öldürdüm ama gücünü alamadım. Şimdi kolye sayesinde güç benim!"

Kılıcınla şifacıya saldırıyorsun ama o büyü kalkanı kullanıyor. Büyüler seni geri itiyor.

Aniden, pencereden Kızıl Alev'in başı görünüyor. Ejderha, şifacıyı görünce öfkeyle bağırıyor: "Sen! Sen beni öldürmeye çalışan hırsız!"

Şifacı şaşkın: "Ejderha? Nasıl hala yaşıyorsun?"

"Ben ölmedim! Sen sadece beni uykuya daldırdın ve kolyemi çaldın!"`,
        choices: [
          { text: "Ejderhayla birlikte savaş", nextNode: "fight_with_dragon" },
          { text: "Lydia'yı kurtar", nextNode: "save_lydia_from_father" },
          { text: "Şifacıyı durdur", nextNode: "stop_healer" },
          { text: "Büyüyü boz", nextNode: "break_healer_spell" },
          { text: "Kaos yarat", nextNode: "create_chaos" },
        ],
      },

      demand_necklace: {
        title: "Kolyeyi Geri İsteme",
        text: `Şifacıya kolyeyi geri vermesini söylüyorsun.

"Bu kolye senin değil! Ejderhaya ait! Geri ver!"

Şifacı gülüyor: "Geri vermem! Bu kolye benim gücüm! 100 yıl önce ejderhayı öldürdüm ama gücünü alamadım. Şimdi kolye sayesinde güç benim olacak!"

"Sen ejderhayı öldürmedin! Sadece uykuya daldırdın!"

Şifacı şaşkın: "Ne? Nasıl biliyorsun?"

"Çünkü ejderha hala yaşıyor ve kolyesini arıyor. Sen onu uykuya daldırdın ve kolyesini çaldın."

Şifacı'nın yüzündeki ifade değişiyor. Hafızası geri gelmeye başlıyor.`,
        choices: [
          { text: "Şifacıyı ikna et", nextNode: "convince_healer" },
          { text: "Kolyeyi zorla al", nextNode: "force_necklace" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Lydia'dan yardım iste", nextNode: "ask_lydia_help" },
          { text: "Savaş", nextNode: "fight_healer" },
        ],
      },

      call_dragon: {
        title: "Ejderhayı Çağırma",
        text: `Kolyenin gücünü kullanarak ejderhayı çağırmaya çalışıyorsun. Kolye parlamaya başlıyor ve uzaktan ejderha'nın sesini duyuyorsun.

"Kolye! Kolyemin sesi! Nerede?"

Kızıl Alev, tapınağa doğru geliyor. Şifacı korkuyla bağırıyor: "Ejderha! Nasıl hala yaşıyorsun?"

Ejderha tapınağa giriyor ve şifacıyı görüyor: "Sen! Sen beni uykuya daldıran hırsız! Kolyemi geri ver!"

Şifacı korkuyla kolyeyi ejderhaya doğru atıyor: "Al! Al kolyeni! Ben yanlış yaptım!"

Ejderha kolyeyi yakalıyor ve mutlu oluyor: "Sonunda! Kolyem geri geldi!"`,
        choices: [
          { text: "Ejderhayla konuş", nextNode: "talk_to_dragon" },
          { text: "Şifacıyı affet", nextNode: "forgive_healer" },
          { text: "Köyü kurtar", nextNode: "save_village" },
          { text: "Gerçeği öğren", nextNode: "learn_truth" },
          { text: "Kaç", nextNode: "escape_situation" },
        ],
      },

      break_spell: {
        title: "Büyüyü Bozma",
        text: `Şifacının büyüsünü bozmaya çalışıyorsun. Kılıcındaki runeleri kullanarak büyüyü kırmaya çalışıyorsun.

"Bu büyüyü bozacağım! Sen normal haline döneceksin!"

Şifacı gülüyor: "Büyüyü bozamazsın! Ben çok güçlüyüm!"

Ama kılıcındaki runeler parlamaya başlıyor ve şifacının büyüsü zayıflamaya başlıyor. Şifacı'nın yüzündeki delilik ifadesi azalıyor.

"Ne... ne oluyor? Ben... ben ne yapıyorum?"

Lydia sevinçle bağırıyor: "Baba! Sen geri geldin!"

Şifacı kolyeyi bırakıyor ve normal haline dönüyor.`,
        choices: [
          { text: "Şifacıyı affet", nextNode: "forgive_healer" },
          { text: "Kolyeyi al", nextNode: "take_necklace" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Köyü kurtar", nextNode: "save_village" },
          { text: "Gerçeği öğren", nextNode: "learn_truth" },
        ],
      },

      get_help: {
        title: "Yardım Getirme",
        text: `Tapınaktan kaçıyorsun ve köye geri dönüyorsun. Köylüleri topluyorsun ve durumu anlatıyorsun.

"Şifacı delirmiş! Kolyeyi çalmış ve ejderha gücü kazanmaya çalışıyor!"

Köy reisi Aldric: "Bu çok tehlikeli! Köylüleri güvenli yerlere taşımalıyız!"

Genç çiftçi Tom: "Ben savaşabilirim! Köyümü koruyacağım!"

Diğer köylüler de seninle birlikte savaşmaya hazır olduklarını söylüyorlar. Şifacıyı durdurmak için bir plan yapmalısınız.`,
        choices: [
          { text: "Köylülerle saldır", nextNode: "attack_with_villagers" },
          { text: "Tuzak kur", nextNode: "set_trap" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Şifacıyı ikna et", nextNode: "convince_healer" },
          { text: "Köyü tahliye et", nextNode: "evacuate_village" },
        ],
      },

      // DAHA FAZLA EKSİK NODE'LAR
      continue_fight: {
        title: "Savaşa Devam Etme",
        text: `Ejderha ile savaşa devam ediyorsun. Kılıcın ve kolyenin gücü birleşiyor. Ejderha'nın alevleri seni yakmaya çalışıyor ama kolyenin koruması altındasın.

"Sen gerçekten güçlüsün!" diye bağırıyor ejderha. "Ama bu savaşı kazanamazsın!"

Lydia, bir taşın arkasından izliyor ve dua ediyor. Kolyen üzerindeki semboller daha da parlak yanıyor.

Aniden, ejderha duruyor ve konuşuyor: "Dur! Bu savaş anlamsız! Sen beni öldürmedin, sadece uykuya daldırdın. Şimdi gerçeği öğrenmeliyiz."`,
        choices: [
          { text: "Savaşı durdur", nextNode: "stop_fight" },
          { text: "Gerçeği öğren", nextNode: "learn_truth" },
          { text: "Kolyeyi kullan", nextNode: "use_necklace_power" },
          { text: "Lydia'dan yardım iste", nextNode: "ask_lydia_help" },
          { text: "Son saldırı", nextNode: "final_attack" },
        ],
      },

      remove_necklace: {
        title: "Kolyeyi Çıkarma",
        text: `Kolyeyi boynundan çıkarıyorsun. Aniden, ejderha'nın gözleri normale dönüyor ve sakinleşiyor.

"Teşekkür ederim," diyor ejderha. "Bu kolye benim aile yadigârım. 100 yıl önce sen onu çaldın ve beni uykuya daldırdın."

"Ben mi? Nasıl olur?"

"Evet, sen! Ama şimdi hatırlamıyorsun çünkü kolye senin hafızanı da etkiledi. Sen gerçekten 100 yıl önce yaşayan bir ejderha avcısısın."

Lydia şaşkın: "Bu imkansız! Sen nasıl 100 yıl yaşayabilirsin?"

Kolyeyi ejderhaya veriyorsun ve aniden hafızanın bir kısmı geri geliyor.`,
        choices: [
          { text: "Hafızayı geri getir", nextNode: "restore_memory" },
          { text: "Ejderhayla konuş", nextNode: "talk_to_dragon" },
          { text: "Gerçeği öğren", nextNode: "learn_truth" },
          { text: "Köye dön", nextNode: "return_to_village" },
          { text: "Yeni yol ara", nextNode: "find_new_path" },
        ],
      },

      learn_truth: {
        title: "Gerçeği Öğrenme",
        text: `Ejderha sana gerçeği anlatıyor: "100 yıl önce, sen benim dostumdun. Ama şifacı seni kandırdı ve kolyemi çalmaya ikna etti."

"Şifacı mı? Hangi şifacı?"

"Lydia'nın babası! O zaman da şifacıydı. Seni kandırarak kolyemi çaldırdı ve beni uykuya daldırdı. Ama sen de kolyenin etkisi altında kaldın ve hafızamı kaybettim."

Lydia şok olmuş: "Babam mı? Bu imkansız!"

"Evet! Şifacı kolyenin gücünü kullanarak 100 yıl yaşadı. Şimdi tekrar uyandırdı beni ve aynı oyunu oynamaya çalışıyor."

Bu gerçek çok şok edici. Şifacı hem ejderhayı hem de seni kandırmış.`,
        choices: [
          { text: "Şifacıyı yüzleştir", nextNode: "confront_healer" },
          { text: "Kolyeyi geri al", nextNode: "reclaim_necklace" },
          { text: "Köyü uyar", nextNode: "warn_village" },
          { text: "Yeni plan yap", nextNode: "make_new_plan" },
          { text: "Geçmişi hatırla", nextNode: "remember_past" },
        ],
      },

      ask_lydia_help: {
        title: "Lydia'dan Yardım İsteme",
        text: `Lydia'ya yardım etmesi için bağırıyorsun: "Lydia! Bana yardım et! Şifacıyı durdurmamız gerekiyor!"

Lydia cesurca yaklaşıyor: "Babamı durduracağım! O artık babam değil!"

Şifacı kızına bakıyor ve yüzündeki ifade değişiyor: "Lydia? Kızım? Ben ne yapıyorum?"

Lydia: "Baba! Lütfen dur! Bu sen değilsin! Kolyeyi bırak!"

Şifacı'nın yüzündeki delilik ifadesi azalıyor. Kolyeyi bırakıyor ve normal haline dönüyor.

"Ne... ne oldu? Ben ne yaptım?" diye soruyor şifacı.`,
        choices: [
          { text: "Şifacıyı affet", nextNode: "forgive_healer" },
          { text: "Gerçeği açıkla", nextNode: "explain_truth" },
          { text: "Kolyeyi al", nextNode: "take_necklace" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Köyü kurtar", nextNode: "save_village" },
        ],
      },

      escape_battle: {
        title: "Savaştan Kaçma",
        text: `Ejderha ile savaştan kaçıyorsun. Lydia ile birlikte güvenli bir yere koşuyorsunuz.

"Bu çok tehlikeli!" diye bağırıyor Lydia. "Babam ne yapıyor?"

"Şifacı kolyenin gücünü kullanıyor. Bu çok tehlikeli."

Köye geri döndüğünüzde, köylüleri topluyorsunuz ve durumu anlatıyorsunuz. Herkes korku içinde.

Köy reisi Aldric: "Bu çok tehlikeli! Köylüleri güvenli yerlere taşımalıyız!"

Şimdi bir plan yapmalısınız. Şifacıyı durdurmak ve kolyeyi geri almak gerekiyor.`,
        choices: [
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Köylüleri tahliye et", nextNode: "evacuate_villagers" },
          { text: "Yardım ara", nextNode: "seek_help" },
          { text: "Geri dön", nextNode: "return_to_fight" },
          { text: "Gizli yol ara", nextNode: "find_secret_path" },
        ],
      },

      take_lydia_safe: {
        title: "Lydia'yı Güvenli Yere Götürme",
        text: `Lydia'yı güvenli bir yere götürüyorsun. Köyün güneyindeki eski kulübeye saklanıyorsunuz.

"Burada güvende olacağız," diyorsun.

Lydia: "Babam... babam ne yapıyor? Neden böyle davranıyor?"

"Kolyenin gücü onu etkiliyor. Şifacı kolyeyi kullanarak ejderha gücü kazanmaya çalışıyor."

"Peki ya ejderha? Neden konuşuyor?"

"Bu çok karmaşık bir durum. Ejderha gerçekten de konuşuyor ve beni tanıyor. Ama neden hatırlamıyorum?"

Lydia sana güvenle bakıyor: "Sen bizi kurtaracaksın, değil mi?"`,
        choices: [
          { text: "Evet, kurtaracağım", nextNode: "promise_to_save" },
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Gerçeği araştır", nextNode: "investigate_truth" },
          { text: "Köylüleri uyar", nextNode: "warn_villagers" },
          { text: "Geri dön", nextNode: "return_to_scene" },
        ],
      },

      // EKSİK NODE'LAR - TAMAMLAMA
      investigate_temple: {
        title: "Eski Tapınağı Araştırma",
        text: `Köyün kuzeyindeki eski tapınağa gidiyorsun. Tapınak harap durumda ama içeriden garip ışıklar geliyor.

İçeri girdiğinde, tapınağın ortasında büyük bir altar görüyorsun. Üzerinde ejderha kanı ve garip semboller var. Duvarlarda ejderha resimleri asılı.

Aniden, bir ses duyuyorsun: "Kim orada?"

Şifacı, tapınağın arkasından çıkıyor. Yüzünde delilik ifadesi var: "Sen... sen ejderha avcısısın! Neden buradasın?"

"Bu tapınakta ne yapıyorsun?" diye soruyorsun.

Şifacı gülüyor: "Güç... ejderha gücü! Ben 100 yıl önce ejderha avcısıydım. Ejderhayı öldürdüm ama gücünü alamadım. Şimdi kolyeyi buldum ve güç benim olacak!"`,
        choices: [
          { text: "Şifacıyla savaş", nextNode: "fight_healer" },
          { text: "Kolyeyi geri iste", nextNode: "demand_necklace" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Büyüyü boz", nextNode: "break_spell" },
          { text: "Kaç ve yardım getir", nextNode: "get_help" },
        ],
      },

      talk_to_dragon: {
        title: "Ejderhayla Konuşma",
        text: `Ejderha'ya yaklaşıyorsun. Kılıcını indiriyorsun ve konuşmaya çalışıyorsun.

"Ben seni öldürmedim. Hafızamı kaybettim ama bunu hatırlamıyorum."

Ejderha gülüyor: "Sen beni öldürdün ama ben ölmedim. Sadece uykuya daldım. Şimdi uyandım ve kolyemi arıyorum."

"Kolye? Hangi kolye?" diye soruyorsun.

"Boynundaki kolye! O benim aile yadigârım. 100 yıl önce sen onu çaldın ve beni uykuya daldırdın."

Lydia şaşkın: "Bu kolye ejderhaya mı ait?"

Kolyen üzerindeki semboller parlamaya başlıyor. Hafızanın bir kısmı geri geliyor.`,
        choices: [
          { text: "Kolyeyi geri ver", nextNode: "return_necklace" },
          { text: "Gerçeği öğren", nextNode: "learn_truth" },
          { text: "Kolyeyi tut", nextNode: "keep_necklace" },
          { text: "Ejderhayla anlaş", nextNode: "negotiate_dragon" },
          { text: "Savaş", nextNode: "fight_dragon" },
        ],
      },

      return_necklace: {
        title: "Kolyeyi Geri Verme",
        text: `Kolyeyi ejderhaya geri veriyorsun. Ejderha mutlu oluyor ve kolyeyi boynuna takıyor.

"Teşekkür ederim, dostum. Kolyem geri geldi."

Aniden, kolyenin gücü ejderhayı sarmalıyor ve ejderha'nın yaraları iyileşiyor. Ejderha daha güçlü ve sağlıklı görünüyor.

"Şimdi gerçeği öğrenmeliyiz," diyor ejderha. "Şifacı neden beni uyandırdı?"

Lydia: "Babam... babam ne yapıyor?"

"Şifacı kolyenin gücünü kullanarak 100 yıl yaşadı. Şimdi tekrar güç kazanmaya çalışıyor."

Ejderha: "O zaman onu durdurmamız gerekiyor. Ama önce senin hafızanı geri getirmeliyiz."`,
        choices: [
          { text: "Hafızayı geri getir", nextNode: "restore_memory" },
          { text: "Şifacıyı durdur", nextNode: "stop_healer" },
          { text: "Köyü kurtar", nextNode: "save_village" },
          { text: "Yeni plan yap", nextNode: "make_new_plan" },
          { text: "Ejderhayla birlikte git", nextNode: "go_with_dragon" },
        ],
      },

      keep_necklace: {
        title: "Kolyeyi Tutma",
        text: `Kolyeyi tutmaya karar veriyorsun. Ejderha öfkeyle bağırıyor: "Kolyemi geri ver! O benim!"

"Hayır! Bu kolye benim gücüm! Sen onu hak etmiyorsun!"

Kolyenin gücü seni sarmalıyor ve daha güçlü hissediyorsun. Ama aynı zamanda kolyenin etkisi altında kalıyorsun.

Lydia korkuyla bakıyor: "Ne yapıyorsun? Bu yanlış!"

"Hayır! Bu doğru! Ben güçlü olacağım!"

Ejderha: "Sen de şifacı gibi oldun! Kolyenin gücü seni de etkiliyor!"

Kolyenin gücü seni değiştirmeye başlıyor. Hafızan bulanıklaşıyor ve gerçeklik algın değişiyor.`,
        choices: [
          { text: "Gücü kullan", nextNode: "use_power" },
          { text: "Ejderhayla savaş", nextNode: "fight_dragon_again" },
          { text: "Köyü ele geçir", nextNode: "take_over_village" },
          { text: "Kolyeyi bırak", nextNode: "drop_necklace" },
          { text: "Kontrolü kaybet", nextNode: "lose_control" },
        ],
      },

      negotiate_dragon: {
        title: "Ejderhayla Anlaşma",
        text: `Ejderha ile anlaşmaya çalışıyorsun: "Savaşmak yerine anlaşalım. Ne istiyorsun?"

Ejderha düşünüyor: "Ben sadece kolyemi istiyorum. Ama şifacı da onu istiyor."

"O zaman birlikte çalışalım. Şifacıyı durduralım ve kolyeyi sana geri verelim."

Lydia: "Babamı durdurabiliriz! O artık babam değil!"

Ejderha: "Tamam, anlaştık. Birlikte şifacıyı durduralım."

Şimdi üçünüz birlikte şifacıyı durdurmak için bir plan yapıyorsunuz. Ejderha, Lydia ve sen - garip bir ittifak.`,
        choices: [
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Şifacıya saldır", nextNode: "attack_healer" },
          { text: "Kolyeyi çal", nextNode: "steal_necklace" },
          { text: "Şifacıyı ikna et", nextNode: "convince_healer" },
          { text: "Köyü uyar", nextNode: "warn_village" },
        ],
      },

      // DAHA FAZLA EKSİK NODE'LAR
      protect_lydia: {
        title: "Lydia'yı Koruma",
        text: `Lydia'yı korumak için şifacıya karşı duruyorsun. "Lydia'ya dokunma!"

Şifacı gülüyor: "Kızım mı? O benim kızım! Ona zarar vermem!"

"Sen artık onun babası değilsin! Kolyenin gücü seni değiştirdi!"

Lydia cesurca yaklaşıyor: "Baba! Lütfen dur! Bu sen değilsin!"

Şifacı'nın yüzündeki ifade değişiyor. Kolyenin etkisi azalıyor ve normal haline dönmeye başlıyor.

"Lydia? Kızım? Ben ne yapıyorum?"`,
        choices: [
          { text: "Şifacıyı affet", nextNode: "forgive_healer" },
          { text: "Kolyeyi al", nextNode: "take_necklace" },
          { text: "Gerçeği açıkla", nextNode: "explain_truth" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Köyü kurtar", nextNode: "save_village" },
        ],
      },

      escape_healer: {
        title: "Şifacıdan Kaçma",
        text: `Şifacıdan kaçıyorsun. Şifacı kolyenin gücüyle size saldırmaya çalışıyor ama sen Lydia ile birlikte kaçıyorsunuz.

"Bu çok tehlikeli!" diye bağırıyor Lydia.

Köye geri döndüğünüzde, köylüleri topluyorsunuz ve durumu anlatıyorsunuz.

"Şifacı delirmiş! Kolyeyi çalmış ve ejderha gücü kazanmaya çalışıyor!"

Köy reisi Aldric: "Bu çok tehlikeli! Köylüleri güvenli yerlere taşımalıyız!"

Şimdi bir plan yapmalısınız. Şifacıyı durdurmak ve kolyeyi geri almak gerekiyor.`,
        choices: [
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Köylüleri tahliye et", nextNode: "evacuate_villagers" },
          { text: "Yardım ara", nextNode: "seek_help" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Gizli yol ara", nextNode: "find_secret_path" },
        ],
      },

      attack_healer: {
        title: "Şifacıya Saldırma",
        text: `Şifacıya saldırıyorsun. Kılıcınla şifacıya doğru koşuyorsun ama şifacı kolyenin gücüyle büyü kalkanı kullanıyor.

"Sen beni durduramazsın! Ben çok güçlüyüm!"

Büyüler odada uçuşuyor. Lydia korkuyla izliyor.

Aniden, pencereden ejderha'nın başı görünüyor. Ejderha, şifacıyı görünce öfkeyle bağırıyor: "Sen! Sen beni uykuya daldıran hırsız!"

Şifacı şaşkın: "Ejderha? Nasıl hala yaşıyorsun?"

"Ben ölmedim! Sen sadece beni uykuya daldırdın ve kolyemi çaldın!"

Şimdi üçlü bir savaş başlıyor. Sen, ejderha ve şifacı.`,
        choices: [
          { text: "Ejderhayla birlikte savaş", nextNode: "fight_with_dragon" },
          { text: "Lydia'yı kurtar", nextNode: "save_lydia_from_father" },
          { text: "Şifacıyı durdur", nextNode: "stop_healer" },
          { text: "Büyüyü boz", nextNode: "break_healer_spell" },
          { text: "Kaos yarat", nextNode: "create_chaos" },
        ],
      },

      steal_necklace: {
        title: "Kolyeyi Çalma",
        text: `Şifacıdan kolyeyi çalmaya çalışıyorsun. Gizlice yaklaşıyorsun ve kolyeyi almaya çalışıyorsun.

Ama şifacı seni fark ediyor: "Ne yapıyorsun? Kolyeyi mi çalmaya çalışıyorsun?"

"Bu kolye senin değil! Ejderhaya ait!"

Şifacı kolyeyi sıkıca tutuyor: "Hayır! Bu benim gücüm! Geri vermem!"

Lydia: "Baba! Lütfen kolyeyi bırak!"

Şifacı'nın yüzündeki ifade değişiyor. Kolyenin etkisi azalıyor ve normal haline dönmeye başlıyor.

"Ne... ne yapıyorum? Ben ne yapıyorum?"`,
        choices: [
          { text: "Kolyeyi al", nextNode: "take_necklace" },
          { text: "Şifacıyı affet", nextNode: "forgive_healer" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Köyü kurtar", nextNode: "save_village" },
          { text: "Gerçeği açıkla", nextNode: "explain_truth" },
        ],
      },

      warn_dragon: {
        title: "Ejderhayı Uyarma",
        text: `Ejderhayı uyarmak için kolyenin gücünü kullanıyorsun. Kolye parlamaya başlıyor ve ejderha'nın sesini duyuyorsun.

"Kolye! Kolyemin sesi! Neredesin?"

"Ejderha! Şifacı seni uyandırdı ve kolyeyi çaldı! Dikkatli ol!"

Ejderha öfkeyle bağırıyor: "Şifacı mı? Hangi şifacı?"

"Lydia'nın babası! O 100 yıl önce de şifacıydı ve kolyeyi çaldı!"

Ejderha: "O zaman onu durdurmamız gerekiyor! Nerede?"

"Eski tapınakta! Hemen gel!"

Ejderha tapınağa doğru geliyor. Şifacı için kötü olacak.`,
        choices: [
          { text: "Tapınağa git", nextNode: "go_to_temple" },
          { text: "Köylüleri uyar", nextNode: "warn_villagers" },
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Lydia'yı koru", nextNode: "protect_lydia" },
          { text: "Bekle", nextNode: "wait_for_dragon" },
        ],
      },

      warn_villagers: {
        title: "Köylüleri Uyarma",
        text: `Köye geri dönüyorsun ve köylüleri uyarıyorsun.

"Köylüler! Şifacı 100 yıl önce ejderha avcısıydı!"

Köy reisi Aldric: "Ne? Şifacı mı? Bu imkansız!"

"Evet! Şifacı kolyeyi çaldı ve ejderha gücü kazanmaya çalışıyor!"

Genç çiftçi Tom: "Ne yapacağız? Köyü tahliye mi edelim?"

"Hayır! Köyü savunmalıyız! Köylüleri silahlandırmalıyız!"

Köylüler korku içinde ama seninle birlikte savaşmaya hazır olduklarını söylüyorlar.`,
        choices: [
          { text: "Köylüleri silahlandır", nextNode: "arm_villagers" },
          { text: "Tuzaklar kur", nextNode: "set_traps" },
          { text: "Güvenli yerler hazırla", nextNode: "prepare_safe_places" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Plan yap", nextNode: "make_plan" },
        ],
      },

      plan_attack: {
        title: "Saldırı Planı",
        text: `Şifacıya saldırmak için bir plan yapıyorsun. Lydia ile birlikte düşünüyorsunuz.

"Şifacı kolyenin gücünü kullanıyor. Onu durdurmamız gerekiyor."

Lydia: "Babamı durdurabilirim! O artık babam değil!"

"Evet, sen onu durdurabilirsin. Ben de kolyeyi almaya çalışacağım."

"Peki ya ejderha? Onu da çağıralım mı?"

"Evet, ejderha da yardım edebilir. Üçümüz birlikte şifacıyı durdurabiliriz."

Şimdi planı uygulamaya koyuyorsunuz. Lydia şifacıyı oyalayacak, sen kolyeyi alacaksın ve ejderha da güç verecek.`,
        choices: [
          { text: "Planı uygula", nextNode: "execute_plan" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Köylüleri topla", nextNode: "gather_villagers" },
          { text: "Tuzak kur", nextNode: "set_trap" },
          { text: "Geri dön", nextNode: "return_to_scene" },
        ],
      },

      arm_villagers: {
        title: "Köylüleri Silahlandırma",
        text: `Köylüleri silahlandırıyorsun. Eski silahları çıkarıyorsunuz ve herkese bir silah veriyorsun.

"Herkes silah alsın! Köyümüzü koruyacağız!"

Genç çiftçi Tom: "Ben savaşabilirim! Köyümü koruyacağım!"

Yaşlı çiftçi: "Ben de savaşabilirim! Köyüm için ölürüm!"

Köy reisi Aldric: "Hepimiz birlikte savaşacağız! Ejderha Avcısı bizi yönlendirecek!"

Köylüler silahlanıyor ve hazırlanıyor. Şimdi şifacıya karşı savaşmaya hazırlar.

"Şimdi şifacıya saldıralım!" diye bağırıyorsun.`,
        choices: [
          { text: "Şifacıya saldır", nextNode: "attack_healer" },
          { text: "Tuzaklar kur", nextNode: "set_traps" },
          { text: "Güvenli yerler hazırla", nextNode: "prepare_safe_places" },
          { text: "Ejderhayı beklet", nextNode: "wait_for_dragon" },
          { text: "Plan yap", nextNode: "make_plan" },
        ],
      },

      set_traps: {
        title: "Tuzaklar Kurma",
        text: `Köyün etrafına tuzaklar kuruyorsun. Şifacı gelirse yakalayabilirsiniz.

"Bu tuzaklar şifacıyı yakalayacak!"

Genç çiftçi Tom: "Ben de tuzak kurmayı biliyorum!"

Köylülerle birlikte çeşitli tuzaklar kuruyorsunuz: ağ tuzakları, çukur tuzakları, ip tuzakları.

"Şimdi şifacı gelirse yakalayabiliriz!"

Lydia: "Babam çok akıllıdır. Bu tuzakları fark edebilir."

"O zaman daha karmaşık tuzaklar kuralım!"

Tuzaklar hazır. Şimdi şifacıyı bekliyorsunuz.`,
        choices: [
          { text: "Şifacıyı bekle", nextNode: "wait_for_healer" },
          { text: "Köylüleri silahlandır", nextNode: "arm_villagers" },
          { text: "Güvenli yerler hazırla", nextNode: "prepare_safe_places" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Plan yap", nextNode: "make_plan" },
        ],
      },

      prepare_safe_places: {
        title: "Güvenli Yerler Hazırlama",
        text: `Köyde güvenli yerler hazırlıyorsun. Kadınları ve çocukları güvenli yerlere taşıyorsunuz.

"Kadınlar ve çocuklar burada güvende olacak!"

Köy reisi Aldric: "Evet, bu yerler güvenli. Şifacı buraya gelemez."

Lydia: "Ben de burada kalayım mı?"

"Hayır, sen benimle gel. Babayı durdurmamız gerekiyor."

Güvenli yerler hazır. Şimdi savaşmaya hazırsınız.

"Şimdi şifacıya karşı savaşalım!"`,
        choices: [
          { text: "Şifacıya saldır", nextNode: "attack_healer" },
          { text: "Köylüleri silahlandır", nextNode: "arm_villagers" },
          { text: "Tuzaklar kur", nextNode: "set_traps" },
          { text: "Ejderhayı beklet", nextNode: "wait_for_dragon" },
          { text: "Plan yap", nextNode: "make_plan" },
        ],
      },

      wait_for_dragon: {
        title: "Ejderhayı Bekleme",
        text: `Ejderhayı bekliyorsun. Kolyenin gücünü kullanarak ejderhayı çağırdın.

"Ejderha gelmeli. Kolyenin sesini duydu."

Lydia: "Ejderha gerçekten gelecek mi?"

"Evet, gelecek. Kolye onun aile yadigârı."

Aniden, uzaktan ejderha'nın sesini duyuyorsun: "Kolye! Kolyemin sesi!"

Ejderha geliyor! Büyük ve güçlü görünüyor.

"Ejderha geldi!" diye bağırıyorsun.

Şimdi ejderha ile birlikte şifacıya karşı savaşabilirsiniz.`,
        choices: [
          { text: "Ejderhayla konuş", nextNode: "talk_to_dragon" },
          { text: "Şifacıya saldır", nextNode: "attack_healer" },
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Köylüleri topla", nextNode: "gather_villagers" },
          { text: "Bekle", nextNode: "wait_for_healer" },
        ],
      },

      // DAHA FAZLA EKSİK NODE'LAR - HIZLI TAMAMLAMA
      fight_with_dragon: {
        title: "Ejderhayla Birlikte Savaşma",
        text: `Ejderha ile birlikte şifacıya saldırıyorsunuz. Ejderha ateş püskürtüyor, sen de kılıcınla saldırıyorsun.

"Birlikte savaşalım!" diye bağırıyorsun.

Şifacı kolyenin gücüyle büyü kalkanı kullanıyor ama ejderha'nın ateşi kalkanı zayıflatıyor.

"Seni durduramazsınız!" diye bağırıyor şifacı.

Lydia: "Baba! Lütfen dur!"

Şifacı'nın yüzündeki ifade değişiyor. Kolyenin etkisi azalıyor.`,
        choices: [
          { text: "Şifacıyı durdur", nextNode: "stop_healer" },
          { text: "Kolyeyi al", nextNode: "take_necklace" },
          { text: "Lydia'yı kurtar", nextNode: "save_lydia_from_father" },
          { text: "Büyüyü boz", nextNode: "break_healer_spell" },
          { text: "Kaos yarat", nextNode: "create_chaos" },
        ],
      },

      save_lydia_from_father: {
        title: "Lydia'yı Babasından Kurtarma",
        text: `Lydia'yı babasından kurtarmaya çalışıyorsun. Şifacı kolyenin gücüyle Lydia'yı kontrol etmeye çalışıyor.

"Lydia! Kızım! Bana gel!"

Lydia korkuyla bakıyor: "Baba! Sen değilsin!"

"Hayır! Sen artık babam değilsin!" diye bağırıyor Lydia.

Sen Lydia'yı koruyorsun ve şifacıya karşı duruyorsun.`,
        choices: [
          { text: "Şifacıyı durdur", nextNode: "stop_healer" },
          { text: "Kolyeyi al", nextNode: "take_necklace" },
          { text: "Lydia'yı kaçır", nextNode: "escape_with_lydia" },
          { text: "Şifacıyı ikna et", nextNode: "convince_healer" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
        ],
      },

      stop_healer: {
        title: "Şifacıyı Durdurma",
        text: `Şifacıyı durdurmaya çalışıyorsun. Kılıcınla şifacıya saldırıyorsun ama şifacı kolyenin gücüyle kendini koruyor.

"Sen beni durduramazsın!"

Lydia: "Baba! Lütfen dur!"

Şifacı'nın yüzündeki ifade değişiyor. Kolyenin etkisi azalıyor ve normal haline dönmeye başlıyor.

"Ne... ne yapıyorum?"`,
        choices: [
          { text: "Şifacıyı affet", nextNode: "forgive_healer" },
          { text: "Kolyeyi al", nextNode: "take_necklace" },
          { text: "Gerçeği açıkla", nextNode: "explain_truth" },
          { text: "Köyü kurtar", nextNode: "save_village" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
        ],
      },

      break_healer_spell: {
        title: "Şifacının Büyüsünü Bozma",
        text: `Şifacının büyüsünü bozmaya çalışıyorsun. Kılıcındaki runeleri kullanarak büyüyü bozmaya çalışıyorsun.

"Büyüyü bozacağım!"

Kılıcındaki runeler parlamaya başlıyor ve şifacının büyüsünü zayıflatıyor.

Şifacı: "Ne yapıyorsun? Büyümü bozuyorsun!"

"Evet! Seni normal haline döndüreceğim!"

Büyü bozuluyor ve şifacı normal haline dönüyor.`,
        choices: [
          { text: "Şifacıyı affet", nextNode: "forgive_healer" },
          { text: "Kolyeyi al", nextNode: "take_necklace" },
          { text: "Gerçeği açıkla", nextNode: "explain_truth" },
          { text: "Köyü kurtar", nextNode: "save_village" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
        ],
      },

      create_chaos: {
        title: "Kaos Yaratma",
        text: `Kaos yaratmaya karar veriyorsun. Kolyenin gücünü kullanarak büyü yapıyorsun ve odada kaos yaratıyorsun.

"Kaos yaratacağım!"

Büyüler odada uçuşuyor ve şifacı kontrolü kaybediyor.

Şifacı: "Ne yapıyorsun? Kontrolü kaybediyorum!"

"Evet! Şimdi kolyeyi alabilirim!"

Kaos sırasında kolyeyi almaya çalışıyorsun.`,
        choices: [
          { text: "Kolyeyi al", nextNode: "take_necklace" },
          { text: "Şifacıyı durdur", nextNode: "stop_healer" },
          { text: "Lydia'yı kurtar", nextNode: "save_lydia_from_father" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Kaç", nextNode: "escape_chaos" },
        ],
      },

      force_necklace: {
        title: "Kolyeyi Zorla Alma",
        text: `Kolyeyi zorla almaya çalışıyorsun. Şifacıya saldırıyorsun ve kolyeyi almaya çalışıyorsun.

"Kolyeyi vereceksin!"

Şifacı: "Hayır! Bu benim gücüm!"

Sen kolyeyi zorla alıyorsun. Şifacı direniyor ama sen daha güçlüsün.

"Verdin!"

Kolyeyi alıyorsun ve şifacı güçsüz kalıyor.`,
        choices: [
          { text: "Ejderhaya ver", nextNode: "return_necklace" },
          { text: "Kolyeyi tut", nextNode: "keep_necklace" },
          { text: "Şifacıyı affet", nextNode: "forgive_healer" },
          { text: "Köyü kurtar", nextNode: "save_village" },
          { text: "Gerçeği öğren", nextNode: "learn_truth" },
        ],
      },

      escape_situation: {
        title: "Durumdan Kaçma",
        text: `Durumdan kaçmaya karar veriyorsun. Lydia ile birlikte kaçıyorsunuz.

"Bu çok tehlikeli! Kaçalım!"

Lydia: "Evet! Kaçalım!"

Şifacıdan ve ejderhadan kaçıyorsunuz. Köye geri dönüyorsunuz.

"Şimdi ne yapacağız?" diye soruyor Lydia.

"Plan yapmalıyız. Şifacıyı durdurmamız gerekiyor."`,
        choices: [
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Köylüleri uyar", nextNode: "warn_villagers" },
          { text: "Yardım ara", nextNode: "seek_help" },
          { text: "Geri dön", nextNode: "return_to_fight" },
          { text: "Gizli yol ara", nextNode: "find_secret_path" },
        ],
      },

      attack_with_villagers: {
        title: "Köylülerle Saldırma",
        text: `Köylülerle birlikte şifacıya saldırıyorsunuz. Tüm köy şifacıya karşı savaşıyor.

"Köylüler! Birlikte savaşalım!"

Köy reisi Aldric: "Evet! Köyümüzü koruyacağız!"

Genç çiftçi Tom: "Şifacıyı durduracağız!"

Köylüler silahlarıyla şifacıya saldırıyor. Şifacı kolyenin gücüyle kendini korumaya çalışıyor.`,
        choices: [
          { text: "Şifacıyı durdur", nextNode: "stop_healer" },
          { text: "Kolyeyi al", nextNode: "take_necklace" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Şifacıyı ikna et", nextNode: "convince_healer" },
          { text: "Köyü tahliye et", nextNode: "evacuate_village" },
        ],
      },

      set_trap: {
        title: "Tuzak Kurma",
        text: `Şifacı için tuzak kuruyorsun. Kolyenin gücünü kullanarak büyülü tuzak kuruyorsun.

"Bu tuzak şifacıyı yakalayacak!"

Tuzak hazır. Şifacı gelirse yakalanacak.

Lydia: "Babam çok akıllıdır. Bu tuzağı fark edebilir."

"O zaman daha karmaşık tuzak kuralım!"`,
        choices: [
          { text: "Şifacıyı bekle", nextNode: "wait_for_healer" },
          { text: "Köylüleri silahlandır", nextNode: "arm_villagers" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Şifacıyı ikna et", nextNode: "convince_healer" },
          { text: "Köyü tahliye et", nextNode: "evacuate_village" },
        ],
      },

      evacuate_village: {
        title: "Köyü Tahliye Etme",
        text: `Köyü tahliye etmeye karar veriyorsun. Köylüleri güvenli yerlere taşıyorsunuz.

"Köylüler! Köyü tahliye edelim!"

Köy reisi Aldric: "Evet! Güvenli yerlere gidelim!"

Köylüler eşyalarını topluyor ve güvenli yerlere gidiyorlar.

"Şimdi güvende olacağız!"`,
        choices: [
          { text: "Şifacıyı durdur", nextNode: "stop_healer" },
          { text: "Kolyeyi al", nextNode: "take_necklace" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Yardım ara", nextNode: "seek_help" },
        ],
      },

      stop_fight: {
        title: "Savaşı Durdurma",
        text: `Savaşı durdurmaya çalışıyorsun. "Durun! Savaşmayın!"

Ejderha ve şifacı duruyor.

"Ne yapıyorsun?" diye soruyor ejderha.

"Barış yapalım! Savaşmak yerine konuşalım!"

Şifacı: "Barış mı? Ben kolyeyi istiyorum!"

Ejderha: "Ben de kolyeyi istiyorum!"

"O zaman birlikte çözüm bulalım!"`,
        choices: [
          { text: "Gerçeği öğren", nextNode: "learn_truth" },
          { text: "Kolyeyi paylaş", nextNode: "share_necklace" },
          { text: "Hakem ol", nextNode: "arbitrate" },
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Kaç", nextNode: "escape_fight" },
        ],
      },

      use_necklace_power: {
        title: "Kolyenin Gücünü Kullanma",
        text: `Kolyenin gücünü kullanmaya karar veriyorsun. Kolye parlamaya başlıyor ve güç veriyor.

"Kolyenin gücünü kullanacağım!"

Kolyenin gücü seni sarmalıyor ve daha güçlü hissediyorsun.

"Şimdi çok güçlüyüm!"

Ama kolyenin etkisi altında kalıyorsun. Hafızan bulanıklaşıyor.`,
        choices: [
          { text: "Gücü kullan", nextNode: "use_power" },
          { text: "Kolyeyi bırak", nextNode: "drop_necklace" },
          { text: "Kontrolü kaybet", nextNode: "lose_control" },
          { text: "Ejderhayla savaş", nextNode: "fight_dragon_again" },
          { text: "Köyü ele geçir", nextNode: "take_over_village" },
        ],
      },

      final_attack: {
        title: "Son Saldırı",
        text: `Son saldırını yapıyorsun. Tüm gücünle şifacıya saldırıyorsun.

"Bu son saldırı!"

Kılıcınla şifacıya saldırıyorsun. Şifacı kolyenin gücüyle kendini korumaya çalışıyor.

"Sen beni durduramazsın!"

Ama sen daha güçlüsün. Son saldırınla şifacıyı durduruyorsun.`,
        choices: [
          { text: "Şifacıyı durdur", nextNode: "stop_healer" },
          { text: "Kolyeyi al", nextNode: "take_necklace" },
          { text: "Ejderhaya ver", nextNode: "return_necklace" },
          { text: "Köyü kurtar", nextNode: "save_village" },
          { text: "Gerçeği öğren", nextNode: "learn_truth" },
        ],
      },

      restore_memory: {
        title: "Hafızayı Geri Getirme",
        text: `Hafızanı geri getirmeye çalışıyorsun. Kolyenin gücünü kullanarak hafızanı geri getirmeye çalışıyorsun.

"Hafızamı geri getireceğim!"

Kolye parlamaya başlıyor ve hafızanın bir kısmı geri geliyor.

100 yıl önceki olayları hatırlamaya başlıyorsun. Ejderhayı öldürdüğünü, kolyeyi çaldığını hatırlıyorsun.

"Evet! Hatırlıyorum! Ben ejderhayı öldürdüm ama o ölmedi!"`,
        choices: [
          { text: "Gerçeği öğren", nextNode: "learn_truth" },
          { text: "Ejderhayla konuş", nextNode: "talk_to_dragon" },
          { text: "Köye dön", nextNode: "return_to_village" },
          { text: "Yeni yol ara", nextNode: "find_new_path" },
          { text: "Şifacıyı durdur", nextNode: "stop_healer" },
        ],
      },

      return_to_village: {
        title: "Köye Dönme",
        text: `Köye geri dönüyorsun. Köylüler seni karşılıyor.

"Ejderha Avcısı geri döndü!"

Köy reisi Aldric: "Ne oldu? Şifacıyı durdurdun mu?"

"Evet! Şifacıyı durdurdum ama daha yapılacak çok şey var."

Köylüler mutlu oluyor. Köy güvende.`,
        choices: [
          { text: "Köyü kurtar", nextNode: "save_village" },
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Gerçeği öğren", nextNode: "learn_truth" },
          { text: "Yeni macera", nextNode: "new_adventure" },
        ],
      },

      find_new_path: {
        title: "Yeni Yol Arama",
        text: `Yeni bir yol arıyorsun. Şifacıyı durdurmak için farklı bir yol bulmaya çalışıyorsun.

"Farklı bir yol bulmalıyım!"

Lydia: "Belki de babamı ikna edebiliriz?"

"Evet! Belki de ikna edebiliriz!"

Yeni bir plan yapıyorsun. Şifacıyı ikna etmeye çalışacaksın.`,
        choices: [
          { text: "Şifacıyı ikna et", nextNode: "convince_healer" },
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Köylüleri topla", nextNode: "gather_villagers" },
          { text: "Gizli yol ara", nextNode: "find_secret_path" },
        ],
      },

      confront_healer: {
        title: "Şifacıyı Yüzleştirme",
        text: `Şifacıyı yüzleştiriyorsun. Gerçeği söylüyorsun.

"Sen 100 yıl önce ejderha avcısıydın! Ejderhayı öldürdün ama gücünü alamadın!"

Şifacı şaşkın: "Ne? Ben mi?"

"Evet! Sen kolyeyi çaldın ve 100 yıl yaşadın!"

Şifacı'nın yüzündeki ifade değişiyor. Hafızası geri geliyor.

"Evet... evet hatırlıyorum! Ben ejderha avcısıydım!"`,
        choices: [
          { text: "Kolyeyi geri al", nextNode: "reclaim_necklace" },
          { text: "Köyü uyar", nextNode: "warn_village" },
          { text: "Yeni plan yap", nextNode: "make_new_plan" },
          { text: "Geçmişi hatırla", nextNode: "remember_past" },
          { text: "Şifacıyı affet", nextNode: "forgive_healer" },
        ],
      },

      reclaim_necklace: {
        title: "Kolyeyi Geri Alma",
        text: `Kolyeyi geri alıyorsun. Şifacıdan kolyeyi alıyorsun.

"Kolyeyi geri alacağım!"

Şifacı: "Al! Ben artık istemiyorum!"

Kolyeyi alıyorsun. Şifacı normal haline dönüyor.

"Teşekkür ederim! Ben artık normalim!"

Şimdi kolyeyi ejderhaya geri verebilirsin.`,
        choices: [
          { text: "Ejderhaya ver", nextNode: "return_necklace" },
          { text: "Kolyeyi tut", nextNode: "keep_necklace" },
          { text: "Köyü kurtar", nextNode: "save_village" },
          { text: "Gerçeği öğren", nextNode: "learn_truth" },
          { text: "Yeni plan yap", nextNode: "make_new_plan" },
        ],
      },

      warn_village: {
        title: "Köyü Uyarma",
        text: `Köyü uyarıyorsun. Köylülere durumu anlatıyorsun.

"Köylüler! Şifacı 100 yıl önce ejderha avcısıydı!"

Köy reisi Aldric: "Ne? Bu imkansız!"

"Evet! O kolyeyi çaldı ve 100 yıl yaşadı!"

Köylüler şaşkın oluyor. Bu çok büyük bir sır.

"Şimdi ne yapacağız?"`,
        choices: [
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Köylüleri silahlandır", nextNode: "arm_villagers" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Şifacıyı durdur", nextNode: "stop_healer" },
          { text: "Köyü tahliye et", nextNode: "evacuate_village" },
        ],
      },

      make_new_plan: {
        title: "Yeni Plan Yapma",
        text: `Yeni bir plan yapıyorsun. Durumu değerlendiriyorsun.

"Yeni bir plan yapmalıyım!"

Lydia: "Babamı durdurabiliriz!"

"Evet! Şifacıyı durdurmamız gerekiyor!"

Ejderha: "Ben de yardım edebilirim!"

Üçünüz birlikte yeni bir plan yapıyorsunuz.`,
        choices: [
          { text: "Planı uygula", nextNode: "execute_plan" },
          { text: "Şifacıya saldır", nextNode: "attack_healer" },
          { text: "Kolyeyi çal", nextNode: "steal_necklace" },
          { text: "Şifacıyı ikna et", nextNode: "convince_healer" },
          { text: "Köyü uyar", nextNode: "warn_village" },
        ],
      },

      remember_past: {
        title: "Geçmişi Hatırlama",
        text: `Geçmişi hatırlamaya çalışıyorsun. Kolyenin gücünü kullanarak geçmişi hatırlamaya çalışıyorsun.

"Geçmişi hatırlayacağım!"

Kolye parlamaya başlıyor ve geçmişi hatırlamaya başlıyorsun.

100 yıl önceki olayları hatırlıyorsun. Ejderhayı öldürdüğünü, kolyeyi çaldığını hatırlıyorsun.

"Evet! Hatırlıyorum! Ben ejderha avcısıydım!"`,
        choices: [
          { text: "Gerçeği öğren", nextNode: "learn_truth" },
          { text: "Ejderhayla konuş", nextNode: "talk_to_dragon" },
          { text: "Şifacıyı durdur", nextNode: "stop_healer" },
          { text: "Köyü kurtar", nextNode: "save_village" },
          { text: "Yeni plan yap", nextNode: "make_new_plan" },
        ],
      },

      explain_truth: {
        title: "Gerçeği Açıklama",
        text: `Gerçeği açıklıyorsun. Şifacıya ve Lydia'ya gerçeği söylüyorsun.

"Gerçeği söyleyeceğim! 100 yıl önce ben ejderha avcısıydım!"

Şifacı: "Sen mi? Sen ejderha avcısı mıydın?"

"Evet! Ben ejderhayı öldürdüm ama o ölmedi! Sadece uykuya daldı!"

Lydia: "Bu çok karmaşık!"

"Evet! Şimdi ejderha uyandı ve kolyesini arıyor!"`,
        choices: [
          { text: "Kolyeyi al", nextNode: "take_necklace" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Köyü kurtar", nextNode: "save_village" },
          { text: "Şifacıyı affet", nextNode: "forgive_healer" },
          { text: "Plan yap", nextNode: "make_plan" },
        ],
      },

      make_plan: {
        title: "Plan Yapma",
        text: `Plan yapıyorsun. Durumu değerlendiriyorsun.

"Plan yapmalıyım!"

Lydia: "Babamı durdurabiliriz!"

"Evet! Şifacıyı durdurmamız gerekiyor!"

Ejderha: "Ben de yardım edebilirim!"

Üçünüz birlikte plan yapıyorsunuz.`,
        choices: [
          { text: "Planı uygula", nextNode: "execute_plan" },
          { text: "Şifacıya saldır", nextNode: "attack_healer" },
          { text: "Kolyeyi çal", nextNode: "steal_necklace" },
          { text: "Şifacıyı ikna et", nextNode: "convince_healer" },
          { text: "Köyü uyar", nextNode: "warn_village" },
        ],
      },

      evacuate_villagers: {
        title: "Köylüleri Tahliye Etme",
        text: `Köylüleri tahliye ediyorsun. Köylüleri güvenli yerlere taşıyorsunuz.

"Köylüler! Güvenli yerlere gidelim!"

Köy reisi Aldric: "Evet! Güvenli yerlere gidelim!"

Köylüler eşyalarını topluyor ve güvenli yerlere gidiyorlar.

"Şimdi güvende olacağız!"`,
        choices: [
          { text: "Şifacıyı durdur", nextNode: "stop_healer" },
          { text: "Kolyeyi al", nextNode: "take_necklace" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Yardım ara", nextNode: "seek_help" },
        ],
      },

      seek_help: {
        title: "Yardım Arama",
        text: `Yardım arıyorsun. Başka köylerden yardım istemeye gidiyorsun.

"Yardım istemeliyim!"

Yakındaki köye gidiyorsun ve durumu anlatıyorsun.

"Şifacı delirmiş! Yardım istiyorum!"

Köy reisi: "Yardım edeceğiz! Savaşçılarımızı göndereceğiz!"

Yardım geliyor. Şimdi şifacıyı durdurabilirsiniz.`,
        choices: [
          { text: "Şifacıya saldır", nextNode: "attack_healer" },
          { text: "Kolyeyi al", nextNode: "take_necklace" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Köyü kurtar", nextNode: "save_village" },
        ],
      },

      return_to_fight: {
        title: "Savaşa Geri Dönme",
        text: `Savaşa geri dönüyorsun. Şifacı ve ejderha hala savaşıyor.

"Geri döndüm!"

Şifacı: "Sen geri döndün!"

Ejderha: "Evet! Şimdi birlikte savaşabiliriz!"

Şimdi üçünüz birlikte şifacıyı durdurmaya çalışıyorsunuz.`,
        choices: [
          { text: "Şifacıyı durdur", nextNode: "stop_healer" },
          { text: "Kolyeyi al", nextNode: "take_necklace" },
          { text: "Ejderhayla savaş", nextNode: "fight_with_dragon" },
          { text: "Lydia'yı kurtar", nextNode: "save_lydia_from_father" },
          { text: "Büyüyü boz", nextNode: "break_healer_spell" },
        ],
      },

      find_secret_path: {
        title: "Gizli Yol Arama",
        text: `Gizli yol arıyorsun. Şifacıyı durdurmak için gizli bir yol bulmaya çalışıyorsun.

"Gizli bir yol bulmalıyım!"

Lydia: "Belki de eski tapınakta gizli bir yol vardır?"

"Evet! Belki de vardır!"

Eski tapınağı araştırıyorsun ve gizli bir yol buluyorsun.`,
        choices: [
          { text: "Gizli yolu kullan", nextNode: "use_secret_path" },
          { text: "Şifacıya saldır", nextNode: "attack_healer" },
          { text: "Kolyeyi çal", nextNode: "steal_necklace" },
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
        ],
      },

      promise_to_save: {
        title: "Kurtarma Sözü Verme",
        text: `Lydia'ya kurtarma sözü veriyorsun.

"Evet, seni kurtaracağım! Babayı da kurtaracağım!"

Lydia mutlu oluyor: "Teşekkür ederim! Sen bizi kurtaracaksın!"

"Evet! Şifacıyı durduracağım ve kolyeyi geri alacağım!"

Şimdi sözünü tutmak için şifacıyı durdurmaya çalışacaksın.`,
        choices: [
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Gerçeği araştır", nextNode: "investigate_truth" },
          { text: "Köylüleri uyar", nextNode: "warn_villagers" },
          { text: "Geri dön", nextNode: "return_to_scene" },
          { text: "Şifacıya saldır", nextNode: "attack_healer" },
        ],
      },

      investigate_truth: {
        title: "Gerçeği Araştırma",
        text: `Gerçeği araştırıyorsun. Şifacının geçmişini araştırmaya çalışıyorsun.

"Gerçeği araştıracağım!"

Eski kayıtları araştırıyorsun ve şifacının 100 yıl önce ejderha avcısı olduğunu öğreniyorsun.

"Evet! Şifacı 100 yıl önce ejderha avcısıydı!"

Şimdi gerçeği biliyorsun. Şifacıyı durdurmak için bu bilgiyi kullanabilirsin.`,
        choices: [
          { text: "Şifacıyı yüzleştir", nextNode: "confront_healer" },
          { text: "Köylüleri uyar", nextNode: "warn_villagers" },
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Kolyeyi al", nextNode: "take_necklace" },
        ],
      },

      warn_villagers: {
        title: "Köylüleri Uyarma",
        text: `Köylüleri uyarıyorsun. Köylülere gerçeği söylüyorsun.

"Köylüler! Şifacı 100 yıl önce ejderha avcısıydı!"

Köy reisi Aldric: "Ne? Bu imkansız!"

"Evet! O kolyeyi çaldı ve 100 yıl yaşadı!"

Köylüler şaşkın oluyor. Bu çok büyük bir sır.

"Şimdi ne yapacağız?"`,
        choices: [
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Köylüleri silahlandır", nextNode: "arm_villagers" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Şifacıyı durdur", nextNode: "stop_healer" },
          { text: "Köyü tahliye et", nextNode: "evacuate_village" },
        ],
      },

      return_to_scene: {
        title: "Sahneye Geri Dönme",
        text: `Sahneye geri dönüyorsun. Şifacı ve ejderha hala orada.

"Geri döndüm!"

Şifacı: "Sen geri döndün!"

Ejderha: "Evet! Şimdi birlikte savaşabiliriz!"

Şimdi üçünüz birlikte şifacıyı durdurmaya çalışıyorsunuz.`,
        choices: [
          { text: "Şifacıyı durdur", nextNode: "stop_healer" },
          { text: "Kolyeyi al", nextNode: "take_necklace" },
          { text: "Ejderhayla savaş", nextNode: "fight_with_dragon" },
          { text: "Lydia'yı kurtar", nextNode: "save_lydia_from_father" },
          { text: "Büyüyü boz", nextNode: "break_healer_spell" },
        ],
      },

      // SON EKSİK NODE'LAR - TAMAMLAMA
      escape_with_lydia: {
        title: "Lydia ile Kaçma",
        text: `Lydia ile birlikte kaçıyorsunuz. Şifacıdan uzaklaşıyorsunuz.

"Kaçalım! Bu çok tehlikeli!"

Lydia: "Evet! Kaçalım!"

Güvenli bir yere kaçıyorsunuz. Şimdi plan yapabilirsiniz.`,
        choices: [
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Köylüleri uyar", nextNode: "warn_villagers" },
          { text: "Yardım ara", nextNode: "seek_help" },
          { text: "Geri dön", nextNode: "return_to_fight" },
          { text: "Gizli yol ara", nextNode: "find_secret_path" },
        ],
      },

      escape_chaos: {
        title: "Kaostan Kaçma",
        text: `Kaostan kaçıyorsun. Büyüler odada uçuşuyor ve sen kaçıyorsun.

"Bu çok tehlikeli! Kaçmalıyım!"

Kaostan uzaklaşıyorsun ve güvenli bir yere gidiyorsun.`,
        choices: [
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Köylüleri uyar", nextNode: "warn_villagers" },
          { text: "Yardım ara", nextNode: "seek_help" },
          { text: "Geri dön", nextNode: "return_to_fight" },
          { text: "Gizli yol ara", nextNode: "find_secret_path" },
        ],
      },

      wait_for_healer: {
        title: "Şifacıyı Bekleme",
        text: `Şifacıyı bekliyorsun. Tuzak kurulmuş ve şifacıyı bekliyorsun.

"Şifacı gelmeli. Tuzak hazır."

Lydia: "Babam çok akıllıdır. Bu tuzağı fark edebilir."

"O zaman daha dikkatli olmalıyız."

Şifacıyı bekliyorsun.`,
        choices: [
          { text: "Şifacıya saldır", nextNode: "attack_healer" },
          { text: "Kolyeyi çal", nextNode: "steal_necklace" },
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Köyü uyar", nextNode: "warn_village" },
        ],
      },

      share_necklace: {
        title: "Kolyeyi Paylaşma",
        text: `Kolyeyi paylaşmaya karar veriyorsun. Ejderha ve şifacı arasında hakem oluyorsun.

"Kolyeyi paylaşalım!"

Ejderha: "Paylaşmak mı? Bu benim aile yadigârım!"

Şifacı: "Ben de güç istiyorum!"

"O zaman birlikte kullanabiliriz!"

Üçünüz kolyeyi paylaşmaya karar veriyorsunuz.`,
        choices: [
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Kolyeyi böl", nextNode: "split_necklace" },
          { text: "Sırayla kullan", nextNode: "take_turns" },
          { text: "Yeni çözüm ara", nextNode: "find_solution" },
          { text: "Barış yap", nextNode: "make_peace" },
        ],
      },

      arbitrate: {
        title: "Hakem Olma",
        text: `Hakem olmaya karar veriyorsun. Ejderha ve şifacı arasında hakemlik yapıyorsun.

"Ben hakem olacağım!"

Ejderha: "Sen mi? Sen kimsin?"

"Ben 100 yıl önce ejderha avcısıydım!"

Şifacı: "Sen mi? Ben de ejderha avcısıydım!"

"O zaman birlikte çözüm bulalım!"

Üçünüz birlikte çözüm arıyorsunuz.`,
        choices: [
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Kolyeyi paylaş", nextNode: "share_necklace" },
          { text: "Barış yap", nextNode: "make_peace" },
          { text: "Yeni çözüm ara", nextNode: "find_solution" },
          { text: "Savaş", nextNode: "fight_again" },
        ],
      },

      escape_fight: {
        title: "Savaştan Kaçma",
        text: `Savaştan kaçıyorsun. Ejderha ve şifacı savaşıyor ve sen kaçıyorsun.

"Bu çok tehlikeli! Kaçmalıyım!"

Savaştan uzaklaşıyorsun ve güvenli bir yere gidiyorsun.`,
        choices: [
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Köylüleri uyar", nextNode: "warn_villagers" },
          { text: "Yardım ara", nextNode: "seek_help" },
          { text: "Geri dön", nextNode: "return_to_fight" },
          { text: "Gizli yol ara", nextNode: "find_secret_path" },
        ],
      },

      use_power: {
        title: "Gücü Kullanma",
        text: `Kolyenin gücünü kullanıyorsun. Kolye parlamaya başlıyor ve güç veriyor.

"Gücü kullanacağım!"

Kolyenin gücü seni sarmalıyor ve çok güçlü hissediyorsun.

"Şimdi çok güçlüyüm!"

Ama kolyenin etkisi altında kalıyorsun. Hafızan bulanıklaşıyor.`,
        choices: [
          { text: "Şifacıya saldır", nextNode: "attack_healer" },
          { text: "Ejderhayla savaş", nextNode: "fight_dragon_again" },
          { text: "Köyü ele geçir", nextNode: "take_over_village" },
          { text: "Kolyeyi bırak", nextNode: "drop_necklace" },
          { text: "Kontrolü kaybet", nextNode: "lose_control" },
        ],
      },

      drop_necklace: {
        title: "Kolyeyi Bırakma",
        text: `Kolyeyi bırakıyorsun. Kolyenin etkisinden kurtulmaya çalışıyorsun.

"Kolyeyi bırakacağım!"

Kolyeyi yere bırakıyorsun ve etkisinden kurtuluyorsun.

"Artık özgürüm!"

Hafızan geri geliyor ve normal haline dönüyorsun.`,
        choices: [
          { text: "Ejderhaya ver", nextNode: "return_necklace" },
          { text: "Şifacıya ver", nextNode: "give_to_healer" },
          { text: "Köyü kurtar", nextNode: "save_village" },
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Gerçeği öğren", nextNode: "learn_truth" },
        ],
      },

      lose_control: {
        title: "Kontrolü Kaybetme",
        text: `Kolyenin etkisi altında kontrolü kaybediyorsun. Kolye seni kontrol etmeye başlıyor.

"Kontrolü kaybediyorum!"

Kolyenin gücü seni ele geçiriyor ve sen artık kendin değilsin.

"Ben... ben kimim?"

Kolye seni kontrol ediyor ve ne yapacağını bilmiyorsun.`,
        choices: [
          { text: "Kolyeyi bırak", nextNode: "drop_necklace" },
          { text: "Savaş", nextNode: "fight_controlled" },
          { text: "Kaç", nextNode: "escape_controlled" },
          { text: "Yardım iste", nextNode: "ask_for_help" },
          { text: "Kontrolü geri al", nextNode: "regain_control" },
        ],
      },

      fight_dragon_again: {
        title: "Ejderhayla Tekrar Savaşma",
        text: `Ejderhayla tekrar savaşıyorsun. Kolyenin gücüyle ejderhaya saldırıyorsun.

"Ejderhayla savaşacağım!"

Ejderha: "Sen de kolyenin etkisi altındasın!"

"Hayır! Ben güçlüyüm!"

Kolyenin gücüyle ejderhaya saldırıyorsun.`,
        choices: [
          { text: "Ejderhayı öldür", nextNode: "kill_dragon" },
          { text: "Kolyeyi bırak", nextNode: "drop_necklace" },
          { text: "Kontrolü geri al", nextNode: "regain_control" },
          { text: "Kaç", nextNode: "escape_fight" },
          { text: "Yardım iste", nextNode: "ask_for_help" },
        ],
      },

      take_over_village: {
        title: "Köyü Ele Geçirme",
        text: `Kolyenin gücüyle köyü ele geçirmeye çalışıyorsun. Kolye seni kontrol ediyor.

"Köyü ele geçireceğim!"

Köylüler korkuyla bakıyor: "Ne yapıyorsun?"

"Ben artık köyün efendisiyim!"

Kolyenin etkisi altında köyü ele geçirmeye çalışıyorsun.`,
        choices: [
          { text: "Köyü yönet", nextNode: "rule_village" },
          { text: "Kolyeyi bırak", nextNode: "drop_necklace" },
          { text: "Kontrolü geri al", nextNode: "regain_control" },
          { text: "Köylüleri korkut", nextNode: "scare_villagers" },
          { text: "Yardım iste", nextNode: "ask_for_help" },
        ],
      },

      execute_plan: {
        title: "Planı Uygulama",
        text: `Planı uyguluyorsun. Lydia, ejderha ve sen birlikte şifacıyı durdurmaya çalışıyorsunuz.

"Planı uygulayalım!"

Lydia şifacıyı oyalıyor, sen kolyeyi almaya çalışıyorsun, ejderha da güç veriyor.

"Birlikte çalışalım!"

Plan başarılı oluyor ve şifacıyı durduruyorsunuz.`,
        choices: [
          { text: "Şifacıyı durdur", nextNode: "stop_healer" },
          { text: "Kolyeyi al", nextNode: "take_necklace" },
          { text: "Köyü kurtar", nextNode: "save_village" },
          { text: "Gerçeği öğren", nextNode: "learn_truth" },
          { text: "Yeni plan yap", nextNode: "make_new_plan" },
        ],
      },

      gather_villagers: {
        title: "Köylüleri Toplama",
        text: `Köylüleri topluyorsun. Tüm köyü topluyorsun ve durumu anlatıyorsun.

"Köylüler! Toplanın!"

Köy reisi Aldric: "Ne oldu? Neden toplandık?"

"Şifacı delirmiş! Birlikte savaşmalıyız!"

Köylüler toplanıyor ve seninle birlikte savaşmaya hazır oluyorlar.`,
        choices: [
          { text: "Şifacıya saldır", nextNode: "attack_healer" },
          { text: "Kolyeyi al", nextNode: "take_necklace" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Köyü tahliye et", nextNode: "evacuate_village" },
        ],
      },

      use_secret_path: {
        title: "Gizli Yolu Kullanma",
        text: `Gizli yolu kullanıyorsun. Eski tapınaktaki gizli yolu kullanarak şifacıya gizlice yaklaşıyorsun.

"Gizli yolu kullanacağım!"

Gizli yoldan şifacıya yaklaşıyorsun. Şifacı seni fark etmiyor.

"Şimdi kolyeyi alabilirim!"

Gizlice kolyeyi almaya çalışıyorsun.`,
        choices: [
          { text: "Kolyeyi çal", nextNode: "steal_necklace" },
          { text: "Şifacıya saldır", nextNode: "attack_healer" },
          { text: "Plan yap", nextNode: "make_plan" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Köyü uyar", nextNode: "warn_village" },
        ],
      },

      // SON NODE'LAR - TAMAMLAMA
      save_village: {
        title: "Köyü Kurtarma",
        text: `Köyü kurtarıyorsun. Şifacıyı durdurduktan sonra köyü kurtarıyorsun.

"Köyü kurtardım!"

Köylüler mutlu oluyor: "Teşekkür ederim! Köyümüzü kurtardın!"

"Artık güvendesiniz!"

Köy barışa kavuşuyor ve herkes mutlu oluyor.`,
        choices: [
          { text: "Yeni macera", nextNode: "new_adventure" },
          { text: "Köyde kal", nextNode: "stay_in_village" },
          { text: "Ejderhayla konuş", nextNode: "talk_to_dragon" },
          { text: "Gerçeği öğren", nextNode: "learn_truth" },
          { text: "Plan yap", nextNode: "make_plan" },
        ],
      },

      new_adventure: {
        title: "Yeni Macera",
        text: `Yeni bir maceraya başlıyorsun. Köyü kurtardıktan sonra yeni maceralar seni bekliyor.

"Yeni maceralar beni bekliyor!"

Lydia: "Ben de seninle geleceğim!"

"Evet! Birlikte gidelim!"

Yeni maceralara doğru yola çıkıyorsunuz.`,
        choices: [
          { text: "Yeni dünya", nextNode: "new_world" },
          { text: "Yeni görev", nextNode: "new_quest" },
          { text: "Yeni savaş", nextNode: "new_battle" },
          { text: "Yeni dost", nextNode: "new_friend" },
          { text: "Yeni güç", nextNode: "new_power" },
        ],
      },

      stay_in_village: {
        title: "Köyde Kalma",
        text: `Köyde kalmaya karar veriyorsun. Köyü kurtardıktan sonra köyde kalmaya karar veriyorsun.

"Köyde kalacağım!"

Köylüler mutlu oluyor: "Harika! Köyümüzde kalacaksın!"

"Evet! Bu benim evim!"

Köyde kalıyorsun ve köyün koruyucusu oluyorsun.`,
        choices: [
          { text: "Köyü koru", nextNode: "protect_village" },
          { text: "Yeni görev", nextNode: "new_quest" },
          { text: "Yeni dost", nextNode: "new_friend" },
          { text: "Yeni güç", nextNode: "new_power" },
          { text: "Yeni macera", nextNode: "new_adventure" },
        ],
      },

      hive_city_rebellion: {
        id: "hive_city_rebellion",
        title: "🌃 Hive City İsyanı",
        world: "Cyberpunk Dünyası",
        description: `2077 yılında, Night City'nin alt katmanlarında, MegaCorp'ların gözlerinden uzak bir yerde Hive City bulunuyor. Bu, cyberware'lerin ve netrunner'ların sığınağı, özgürlüğün son kalesi.`,
        objective: "MegaCorp'ları durdur ve Hive City'yi kurtar",
        story: {
          start: {
            title: "Hive City'ye Giriş",
            text: `Night City'nin alt katmanlarına iniyorsun. Hive City'nin neon ışıkları uzaktan görünüyor. Bu, cyberware'lerin ve netrunner'ların sığınağı.

"Burada özgürlük var," diye düşünüyorsun.

Aniden, bir ses duyuyorsun: "Hey! Yeni misin?"

Netrunner bir kız sana yaklaşıyor. Adı Nova. Cyberware'leri parlıyor.

Nova: "Hive City'ye hoş geldin! Burada MegaCorp'ların gözlerinden uzak yaşıyoruz."`,
            choices: [
              { text: "Nova ile konuş", nextNode: "talk_to_nova" },
              { text: "Hive City'yi keşfet", nextNode: "explore_hive" },
              { text: "Cyberware ara", nextNode: "find_cyberware" },
              { text: "Netrunner ol", nextNode: "become_netrunner" },
              { text: "MegaCorp'ları araştır", nextNode: "investigate_corps" },
            ],
          },

          talk_to_nova: {
            title: "Nova ile Konuşma",
            text: `Nova ile konuşuyorsun. O sana Hive City'nin durumunu anlatıyor.

Nova: "MegaCorp'lar bizi bulmaya çalışıyor. Hive City'yi yok etmek istiyorlar."

"Ne yapabiliriz?" diye soruyorsun.

"Birlikte savaşabiliriz! Hive City'yi koruyabiliriz!"

Nova sana cyberware teklif ediyor.`,
            choices: [
              { text: "Cyberware kabul et", nextNode: "accept_cyberware" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "MegaCorp'ları araştır", nextNode: "investigate_corps" },
              { text: "Netrunner ol", nextNode: "become_netrunner" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
            ],
          },

          explore_hive: {
            title: "Hive City'yi Keşfetme",
            text: `Hive City'yi keşfediyorsun. Neon ışıklar, cyberware dükkanları, netrunner'lar her yerde.

"Bu çok etkileyici!" diye düşünüyorsun.

Bir cyberware dükkanı görüyorsun. İçeriden garip sesler geliyor.

Dükkan sahibi: "Hoş geldin! Cyberware mi arıyorsun?"

"Evet! Ne var?"`,
            choices: [
              { text: "Cyberware satın al", nextNode: "buy_cyberware" },
              { text: "Dükkanı araştır", nextNode: "investigate_shop" },
              { text: "Nova'yı ara", nextNode: "find_nova" },
              { text: "MegaCorp'ları araştır", nextNode: "investigate_corps" },
              { text: "Netrunner ol", nextNode: "become_netrunner" },
            ],
          },

          find_cyberware: {
            title: "Cyberware Arama",
            text: `Cyberware arıyorsun. Hive City'de cyberware dükkanları var.

"Cyberware bulmalıyım!"

Bir dükkan buluyorsun. İçeride çeşitli cyberware'ler var.

Dükkan sahibi: "Ne tür cyberware istiyorsun?"

"Güçlü olanı!"`,
            choices: [
              {
                text: "Güçlü cyberware al",
                nextNode: "buy_powerful_cyberware",
              },
              { text: "Hızlı cyberware al", nextNode: "buy_fast_cyberware" },
              { text: "Zeki cyberware al", nextNode: "buy_smart_cyberware" },
              { text: "Dükkanı araştır", nextNode: "investigate_shop" },
              { text: "Nova'yı ara", nextNode: "find_nova" },
            ],
          },

          become_netrunner: {
            title: "Netrunner Olma",
            text: `Netrunner olmaya karar veriyorsun. Nova sana netrunner olmayı öğretiyor.

Nova: "Netrunner olmak istiyorsun mu?"

"Evet! Öğret bana!"

"Tamam! Matrix'e girmeyi öğreteceğim!"

Nova sana netrunner tekniklerini öğretiyor.`,
            choices: [
              { text: "Matrix'e gir", nextNode: "enter_matrix" },
              { text: "Hack yap", nextNode: "hack_system" },
              { text: "MegaCorp'ları araştır", nextNode: "investigate_corps" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
            ],
          },

          investigate_corps: {
            title: "MegaCorp'ları Araştırma",
            text: `MegaCorp'ları araştırıyorsun. Nova ile birlikte MegaCorp'ların planlarını öğrenmeye çalışıyorsunuz.

Nova: "MegaCorp'lar Hive City'yi yok etmek istiyor!"

"Ne yapabiliriz?" diye soruyorsun.

"Birlikte savaşabiliriz! Hive City'yi koruyabiliriz!"

MegaCorp'ların planlarını öğreniyorsunuz.`,
            choices: [
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "MegaCorp'lara saldır", nextNode: "attack_corps" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              { text: "Netrunner ol", nextNode: "become_netrunner" },
              { text: "Cyberware ara", nextNode: "find_cyberware" },
            ],
          },

          accept_cyberware: {
            title: "Cyberware Kabul Etme",
            text: `Nova'nın cyberware teklifini kabul ediyorsun. Nova sana güçlü cyberware takıyor.

Nova: "Bu cyberware seni güçlendirecek!"

"Teşekkür ederim!"

Cyberware takılıyor ve sen daha güçlü hissediyorsun.

"Şimdi çok güçlüyüm!"`,
            choices: [
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "MegaCorp'lara saldır", nextNode: "attack_corps" },
              { text: "Netrunner ol", nextNode: "become_netrunner" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              {
                text: "Daha fazla cyberware ara",
                nextNode: "find_more_cyberware",
              },
            ],
          },

          protect_hive: {
            title: "Hive City'yi Koruma",
            text: `Hive City'yi korumaya karar veriyorsun. Nova ile birlikte MegaCorp'lara karşı savaşmaya hazırlanıyorsunuz.

Nova: "MegaCorp'lar geliyor! Hive City'yi korumalıyız!"

"Evet! Birlikte savaşalım!"

Hive City'yi korumak için hazırlanıyorsunuz.`,
            choices: [
              { text: "MegaCorp'lara saldır", nextNode: "attack_corps" },
              { text: "Savunma planı yap", nextNode: "make_defense_plan" },
              { text: "Netrunner'ları topla", nextNode: "gather_netrunners" },
              { text: "Cyberware ara", nextNode: "find_cyberware" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
            ],
          },

          buy_cyberware: {
            title: "Cyberware Satın Alma",
            text: `Cyberware satın alıyorsun. Dükkan sahibi sana çeşitli cyberware'ler gösteriyor.

Dükkan sahibi: "Bu cyberware'ler çok güçlü!"

"Ne tür cyberware'ler var?" diye soruyorsun.

"Güçlü, hızlı, zeki cyberware'ler var!"

Cyberware satın alıyorsun.`,
            choices: [
              {
                text: "Güçlü cyberware al",
                nextNode: "buy_powerful_cyberware",
              },
              { text: "Hızlı cyberware al", nextNode: "buy_fast_cyberware" },
              { text: "Zeki cyberware al", nextNode: "buy_smart_cyberware" },
              { text: "Dükkanı araştır", nextNode: "investigate_shop" },
              { text: "Nova'yı ara", nextNode: "find_nova" },
            ],
          },

          investigate_shop: {
            title: "Dükkanı Araştırma",
            text: `Dükkanı araştırıyorsun. Dükkanın arkasında gizli bir oda buluyorsun.

"Burada gizli bir şey var!" diye düşünüyorsun.

Gizli odada MegaCorp'lara ait belgeler buluyorsun.

"Bu belgeler çok önemli!"`,
            choices: [
              { text: "Belgeleri al", nextNode: "take_documents" },
              { text: "Nova'ya söyle", nextNode: "tell_nova" },
              { text: "MegaCorp'ları araştır", nextNode: "investigate_corps" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              { text: "Cyberware ara", nextNode: "find_cyberware" },
            ],
          },

          find_nova: {
            title: "Nova'yı Arama",
            text: `Nova'yı arıyorsun. Hive City'de Nova'yı bulmaya çalışıyorsun.

"Nova nerede?" diye düşünüyorsun.

Nova'yı bir netrunner barında buluyorsun.

Nova: "Sen mi? Ne oldu?"

"Önemli bir şey buldum!"`,
            choices: [
              { text: "Belgeleri göster", nextNode: "show_documents" },
              { text: "MegaCorp'ları araştır", nextNode: "investigate_corps" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Netrunner ol", nextNode: "become_netrunner" },
            ],
          },

          buy_powerful_cyberware: {
            title: "Güçlü Cyberware Satın Alma",
            text: `Güçlü cyberware satın alıyorsun. Bu cyberware seni çok güçlendirecek.

Dükkan sahibi: "Bu cyberware çok güçlü!"

"Alacağım!" diyorsun.

Güçlü cyberware takılıyor ve sen çok güçlü hissediyorsun.

"Şimdi çok güçlüyüm!"`,
            choices: [
              { text: "MegaCorp'lara saldır", nextNode: "attack_corps" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Netrunner ol", nextNode: "become_netrunner" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              {
                text: "Daha fazla cyberware ara",
                nextNode: "find_more_cyberware",
              },
            ],
          },

          buy_fast_cyberware: {
            title: "Hızlı Cyberware Satın Alma",
            text: `Hızlı cyberware satın alıyorsun. Bu cyberware seni çok hızlandıracak.

Dükkan sahibi: "Bu cyberware çok hızlı!"

"Alacağım!" diyorsun.

Hızlı cyberware takılıyor ve sen çok hızlı hissediyorsun.

"Şimdi çok hızlıyım!"`,
            choices: [
              { text: "MegaCorp'lara saldır", nextNode: "attack_corps" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Netrunner ol", nextNode: "become_netrunner" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              {
                text: "Daha fazla cyberware ara",
                nextNode: "find_more_cyberware",
              },
            ],
          },

          buy_smart_cyberware: {
            title: "Zeki Cyberware Satın Alma",
            text: `Zeki cyberware satın alıyorsun. Bu cyberware seni çok zeki yapacak.

Dükkan sahibi: "Bu cyberware çok zeki!"

"Alacağım!" diyorsun.

Zeki cyberware takılıyor ve sen çok zeki hissediyorsun.

"Şimdi çok zekiyim!"`,
            choices: [
              { text: "MegaCorp'lara saldır", nextNode: "attack_corps" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Netrunner ol", nextNode: "become_netrunner" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              {
                text: "Daha fazla cyberware ara",
                nextNode: "find_more_cyberware",
              },
            ],
          },

          enter_matrix: {
            title: "Matrix'e Girme",
            text: `Matrix'e giriyorsun. Nova'nın öğrettiği tekniklerle Matrix'e giriyorsun.

Nova: "Matrix'e hoş geldin!"

"Bu çok etkileyici!" diye düşünüyorsun.

Matrix'te MegaCorp'ların sistemlerini görüyorsun.

"Burada hack yapabilirim!"`,
            choices: [
              { text: "Hack yap", nextNode: "hack_system" },
              { text: "MegaCorp'ları araştır", nextNode: "investigate_corps" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              { text: "Matrix'te kal", nextNode: "stay_in_matrix" },
            ],
          },

          hack_system: {
            title: "Sistem Hack Etme",
            text: `MegaCorp'ların sistemlerini hack ediyorsun. Matrix'te MegaCorp'ların sistemlerine giriyorsun.

"Hack yapacağım!" diye düşünüyorsun.

MegaCorp'ların sistemlerini hack ediyorsun ve önemli bilgiler alıyorsun.

"Bu bilgiler çok önemli!"`,
            choices: [
              { text: "Bilgileri al", nextNode: "take_information" },
              { text: "MegaCorp'ları araştır", nextNode: "investigate_corps" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              { text: "Daha fazla hack yap", nextNode: "hack_more" },
            ],
          },

          make_cyber_plan: {
            title: "Cyber Plan Yapma",
            text: `Cyber plan yapıyorsun. Nova ile birlikte MegaCorp'lara karşı plan yapıyorsunuz.

Nova: "MegaCorp'lara karşı plan yapalım!"

"Evet! Birlikte savaşalım!"

Cyber plan yapıyorsunuz.`,
            choices: [
              { text: "MegaCorp'lara saldır", nextNode: "attack_corps" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Netrunner'ları topla", nextNode: "gather_netrunners" },
              { text: "Cyberware ara", nextNode: "find_cyberware" },
              { text: "Planı uygula", nextNode: "execute_cyber_plan" },
            ],
          },

          attack_corps: {
            title: "MegaCorp'lara Saldırma",
            text: `MegaCorp'lara saldırıyorsun. Nova ile birlikte MegaCorp'lara saldırıyorsunuz.

Nova: "MegaCorp'lara saldıralım!"

"Evet! Birlikte savaşalım!"

MegaCorp'lara saldırıyorsunuz.`,
            choices: [
              { text: "MegaCorp'ları yen", nextNode: "defeat_corps" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              { text: "Netrunner ol", nextNode: "become_netrunner" },
              { text: "Cyberware ara", nextNode: "find_cyberware" },
            ],
          },

          make_defense_plan: {
            title: "Savunma Planı Yapma",
            text: `Savunma planı yapıyorsun. Hive City'yi korumak için savunma planı yapıyorsun.

"Savunma planı yapmalıyım!"

Nova: "Evet! Hive City'yi korumalıyız!"

Savunma planı yapıyorsunuz.`,
            choices: [
              { text: "Savunmayı kur", nextNode: "set_up_defense" },
              { text: "MegaCorp'lara saldır", nextNode: "attack_corps" },
              { text: "Netrunner'ları topla", nextNode: "gather_netrunners" },
              { text: "Cyberware ara", nextNode: "find_cyberware" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
            ],
          },

          gather_netrunners: {
            title: "Netrunner'ları Toplama",
            text: `Netrunner'ları topluyorsun. Hive City'deki tüm netrunner'ları topluyorsun.

"Netrunner'ları toplamalıyım!"

Nova: "Evet! Birlikte savaşalım!"

Netrunner'ları topluyorsun.`,
            choices: [
              { text: "MegaCorp'lara saldır", nextNode: "attack_corps" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              { text: "Cyberware ara", nextNode: "find_cyberware" },
              { text: "Matrix'e gir", nextNode: "enter_matrix" },
            ],
          },

          find_more_cyberware: {
            title: "Daha Fazla Cyberware Arama",
            text: `Daha fazla cyberware arıyorsun. Hive City'de daha fazla cyberware arıyorsun.

"Daha fazla cyberware bulmalıyım!"

Nova: "Daha fazla cyberware var!"

Daha fazla cyberware arıyorsun.`,
            choices: [
              {
                text: "Güçlü cyberware al",
                nextNode: "buy_powerful_cyberware",
              },
              { text: "Hızlı cyberware al", nextNode: "buy_fast_cyberware" },
              { text: "Zeki cyberware al", nextNode: "buy_smart_cyberware" },
              { text: "MegaCorp'lara saldır", nextNode: "attack_corps" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
            ],
          },

          take_documents: {
            title: "Belgeleri Alma",
            text: `Belgeleri alıyorsun. MegaCorp'lara ait belgeleri alıyorsun.

"Bu belgeler çok önemli!" diye düşünüyorsun.

Belgeleri alıyorsun ve Nova'ya göstermeye karar veriyorsun.

"Nova'ya göstermeliyim!"`,
            choices: [
              { text: "Nova'ya göster", nextNode: "show_documents" },
              { text: "MegaCorp'ları araştır", nextNode: "investigate_corps" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Netrunner ol", nextNode: "become_netrunner" },
            ],
          },

          tell_nova: {
            title: "Nova'ya Söyleme",
            text: `Nova'ya söylüyorsun. Gizli odada bulduğun belgeleri Nova'ya söylüyorsun.

Nova: "Ne buldun?"

"Gizli odada MegaCorp'lara ait belgeler buldum!"

"Bu çok önemli! Göstermelisin!"

Nova'ya belgeleri göstermeye karar veriyorsun.`,
            choices: [
              { text: "Belgeleri göster", nextNode: "show_documents" },
              { text: "MegaCorp'ları araştır", nextNode: "investigate_corps" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Netrunner ol", nextNode: "become_netrunner" },
            ],
          },

          show_documents: {
            title: "Belgeleri Gösterme",
            text: `Belgeleri Nova'ya gösteriyorsun. MegaCorp'lara ait belgeleri Nova'ya gösteriyorsun.

Nova: "Bu belgeler çok önemli!"

"Evet! MegaCorp'ların planlarını öğrendik!"

"Bu bilgilerle MegaCorp'ları durdurabiliriz!"

Belgeleri inceliyorsunuz.`,
            choices: [
              { text: "MegaCorp'ları araştır", nextNode: "investigate_corps" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "MegaCorp'lara saldır", nextNode: "attack_corps" },
              { text: "Netrunner ol", nextNode: "become_netrunner" },
            ],
          },

          take_information: {
            title: "Bilgileri Alma",
            text: `Hack ettiğin bilgileri alıyorsun. MegaCorp'ların sistemlerinden aldığın bilgileri alıyorsun.

"Bu bilgiler çok önemli!" diye düşünüyorsun.

Bilgileri alıyorsun ve Nova'ya göstermeye karar veriyorsun.

"Nova'ya göstermeliyim!"`,
            choices: [
              { text: "Nova'ya göster", nextNode: "show_information" },
              { text: "MegaCorp'ları araştır", nextNode: "investigate_corps" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Daha fazla hack yap", nextNode: "hack_more" },
            ],
          },

          hack_more: {
            title: "Daha Fazla Hack Yapma",
            text: `Daha fazla hack yapıyorsun. Matrix'te daha fazla sistem hack ediyorsun.

"Daha fazla hack yapacağım!" diye düşünüyorsun.

Daha fazla sistem hack ediyorsun ve daha fazla bilgi alıyorsun.

"Bu bilgiler çok önemli!"`,
            choices: [
              { text: "Bilgileri al", nextNode: "take_information" },
              { text: "MegaCorp'ları araştır", nextNode: "investigate_corps" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              { text: "Matrix'ten çık", nextNode: "exit_matrix" },
            ],
          },

          stay_in_matrix: {
            title: "Matrix'te Kalma",
            text: `Matrix'te kalmaya karar veriyorsun. Matrix'te daha fazla araştırma yapmaya karar veriyorsun.

"Matrix'te kalacağım!" diye düşünüyorsun.

Matrix'te daha fazla araştırma yapıyorsun.`,
            choices: [
              { text: "Hack yap", nextNode: "hack_system" },
              { text: "MegaCorp'ları araştır", nextNode: "investigate_corps" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              { text: "Matrix'ten çık", nextNode: "exit_matrix" },
            ],
          },

          execute_cyber_plan: {
            title: "Cyber Planı Uygulama",
            text: `Cyber planı uyguluyorsun. Nova ile birlikte cyber planı uyguluyorsunuz.

Nova: "Planı uygulayalım!"

"Evet! Birlikte savaşalım!"

Cyber planı uyguluyorsunuz.`,
            choices: [
              { text: "MegaCorp'lara saldır", nextNode: "attack_corps" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Netrunner'ları topla", nextNode: "gather_netrunners" },
              { text: "Cyberware ara", nextNode: "find_cyberware" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
            ],
          },

          defeat_corps: {
            title: "MegaCorp'ları Yenme",
            text: `MegaCorp'ları yeniyorsun. Nova ile birlikte MegaCorp'ları yeniyorsunuz.

Nova: "MegaCorp'ları yendik!"

"Evet! Hive City'yi kurtardık!"

Hive City artık güvende.`,
            choices: [
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Yeni macera", nextNode: "new_cyber_adventure" },
              { text: "Netrunner ol", nextNode: "become_netrunner" },
              { text: "Cyberware ara", nextNode: "find_cyberware" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
            ],
          },

          set_up_defense: {
            title: "Savunmayı Kurma",
            text: `Savunmayı kuruyorsun. Hive City'yi korumak için savunma kuruyorsun.

"Savunmayı kuracağım!"

Nova: "Evet! Hive City'yi korumalıyız!"

Savunmayı kuruyorsun.`,
            choices: [
              { text: "MegaCorp'lara saldır", nextNode: "attack_corps" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Netrunner'ları topla", nextNode: "gather_netrunners" },
              { text: "Cyberware ara", nextNode: "find_cyberware" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
            ],
          },

          show_information: {
            title: "Bilgileri Gösterme",
            text: `Bilgileri Nova'ya gösteriyorsun. Hack ettiğin bilgileri Nova'ya gösteriyorsun.

Nova: "Bu bilgiler çok önemli!"

"Evet! MegaCorp'ların planlarını öğrendik!"

"Bu bilgilerle MegaCorp'ları durdurabiliriz!"

Bilgileri inceliyorsunuz.`,
            choices: [
              { text: "MegaCorp'ları araştır", nextNode: "investigate_corps" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "MegaCorp'lara saldır", nextNode: "attack_corps" },
              { text: "Netrunner ol", nextNode: "become_netrunner" },
            ],
          },

          exit_matrix: {
            title: "Matrix'ten Çıkma",
            text: `Matrix'ten çıkıyorsun. Matrix'ten çıkıyorsun ve gerçek dünyaya dönüyorsun.

"Matrix'ten çıkmalıyım!" diye düşünüyorsun.

Matrix'ten çıkıyorsun ve Nova'ya bulduğun bilgileri söylüyorsun.

Nova: "Ne buldun?"`,
            choices: [
              { text: "Bilgileri söyle", nextNode: "tell_information" },
              { text: "MegaCorp'ları araştır", nextNode: "investigate_corps" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Netrunner ol", nextNode: "become_netrunner" },
            ],
          },

          tell_information: {
            title: "Bilgileri Söyleme",
            text: `Bilgileri Nova'ya söylüyorsun. Matrix'te bulduğun bilgileri Nova'ya söylüyorsun.

Nova: "Ne buldun?"

"MegaCorp'ların planlarını öğrendim!"

"Bu çok önemli! Göstermelisin!"

Nova'ya bilgileri göstermeye karar veriyorsun.`,
            choices: [
              { text: "Bilgileri göster", nextNode: "show_information" },
              { text: "MegaCorp'ları araştır", nextNode: "investigate_corps" },
              { text: "Plan yap", nextNode: "make_cyber_plan" },
              { text: "Hive City'yi koru", nextNode: "protect_hive" },
              { text: "Netrunner ol", nextNode: "become_netrunner" },
            ],
          },

          new_cyber_adventure: {
            title: "Yeni Cyber Macera",
            text: `Yeni bir cyber maceraya başlıyorsun. Hive City'yi kurtardıktan sonra yeni maceralar seni bekliyor.

"Yeni maceralar beni bekliyor!"

Nova: "Ben de seninle geleceğim!"

"Evet! Birlikte gidelim!"

Yeni cyber maceralara doğru yola çıkıyorsunuz.`,
            choices: [
              { text: "Yeni dünya", nextNode: "new_cyber_world" },
              { text: "Yeni görev", nextNode: "new_cyber_quest" },
              { text: "Yeni savaş", nextNode: "new_cyber_battle" },
              { text: "Yeni dost", nextNode: "new_cyber_friend" },
              { text: "Yeni güç", nextNode: "new_cyber_power" },
            ],
          },
        },
      },
    },
  },

  warhammer_imperial_crisis: {
    title: "💀 İmperial Kriz",
    story: {
      start: {
        text: "İmperium'un bir dünyasında görev yapıyorsunuz. Inquisitor Eisenhorn size yaklaşıyor, yüzünde ciddi bir ifade var. 'Sapkınlık bu dünyada yayılıyor. İmperium'un adaleti burada!'",
        choices: [
          {
            text: "Görevi kabul et",
            nextNode: "accept_mission",
          },
          {
            text: "Daha fazla bilgi iste",
            nextNode: "request_info",
          },
        ],
      },
    },
  },
  cyberpunk_hive_city: {
    title: "🤖 Hive City Kriz",
    story: {
      start: {
        text: "Cyberpunk şehrinde gizli sırlar var. Fixer Rogue size yaklaşıyor. 'Ne işin var, chummer? Bu şehirde olan biten her şeyi bilirim. Fiyatı uygunsa.'",
        choices: [
          {
            text: "Bilgi satın al",
            nextNode: "buy_info",
          },
          {
            text: "Kendi yolunu bul",
            nextNode: "find_own_way",
          },
        ],
      },
    },
  },
};

window.startScenario = function (scenarioId) {
  console.log("✅ START SCENARIO:", scenarioId);

  const scenario = scenarios[scenarioId];
  if (!scenario) {
    console.error("❌ Scenario not found:", scenarioId);
    return;
  }

  // Set the current scenario
  window.currentScenario = scenario;

  // Update title
  const titleElement = document.getElementById("current-scenario-title");
  if (titleElement) {
    titleElement.textContent = scenario.title;
  }

  // Display the starting node
  const startNode = scenario.story.start;
  if (startNode) {
    displayStoryNode(startNode);
  } else {
    console.error("❌ Start node not found for scenario:", scenarioId);

    // Create a fallback start node
    const fallbackStartNode = {
      title: scenario.title || "Macera Başlıyor",
      text: `${
        scenario.backstory || "Macera başlıyor!"
      } Senin hikayen devam ediyor ve her seçimin sonuçları var.`,
      choices: [
        { text: "Macereye başla", nextNode: "start_adventure" },
        { text: "Çevreyi keşfet", nextNode: "explore_environment" },
        { text: "NPC'lerle konuş", nextNode: "talk_to_npcs" },
      ],
    };

    displayStoryNode(fallbackStartNode);
  }
};

window.displayStoryNode = function (node) {
  console.log("✅ DISPLAY STORY NODE");

  const storyText = document.getElementById("story-text");
  const choicesGrid = document.getElementById("choices-grid");

  if (storyText && node.text) {
    storyText.innerHTML = `<p>${node.text}</p>`;
  }

  if (choicesGrid && node.choices) {
    choicesGrid.innerHTML = "";
    node.choices.forEach((choice) => {
      const choiceButton = document.createElement("button");
      choiceButton.className = "choice-btn";
      choiceButton.textContent = choice.text;
      choiceButton.onclick = () => makeChoice(choice.nextNode);
      choicesGrid.appendChild(choiceButton);
    });
  }

  console.log("✅ Story node displayed");
};

window.makeChoice = function (nextNodeId) {
  console.log("✅ MAKE CHOICE:", nextNodeId);

  const currentScenario = getCurrentScenario();
  if (!currentScenario) {
    console.error("❌ No active scenario");
    return;
  }

  const nextNode = currentScenario.story[nextNodeId];
  if (nextNode) {
    displayStoryNode(nextNode);
  } else {
    console.warn(
      "⚠️ Next node not found:",
      nextNodeId,
      "- Using fallback node"
    );

    // Create a fallback node to prevent story from breaking
    const fallbackNode = {
      title: "Macera Devam Ediyor",
      text: `Seçimin seni yeni bir yola götürdü. ${nextNodeId} aksiyonunu gerçekleştirdin ve macera devam ediyor. Yeni fırsatlar seni bekliyor!`,
      choices: [
        { text: "Devam et", nextNode: "continue_adventure" },
        { text: "Yeni yol ara", nextNode: "find_new_path" },
        { text: "Çevreyi keşfet", nextNode: "explore_surroundings" },
        { text: "Geri dön", nextNode: "go_back" },
      ],
    };

    displayStoryNode(fallbackNode);
  }
};

window.getCurrentScenario = function () {
  // Return the currently active scenario or default to living_dragon_hunt
  if (window.currentScenario) {
    return window.currentScenario;
  }
  return scenarios.living_dragon_hunt;
};

window.saveGame = function () {
  console.log("✅ SAVE GAME");
  alert("💾 Oyun kaydedildi!");
};

window.loadGame = function () {
  console.log("✅ LOAD GAME");
  alert("📁 Oyun yüklendi!");
};

window.resetGame = function () {
  console.log("✅ RESET GAME");
  if (confirm("🔄 Oyunu sıfırlamak istediğinizden emin misiniz?")) {
    location.reload();
  }
};

window.updateCharacterName = function (name) {
  console.log("✅ UPDATE CHARACTER NAME:", name);
  if (typeof window.currentCharacter !== "undefined") {
    window.currentCharacter.name = name;
  }
  if (typeof window.updateCharacterPanel === "function") {
    window.updateCharacterPanel();
  }
};

window.updateCharacterPanel = function () {
  console.log("✅ UPDATE CHARACTER PANEL");

  // Update character name
  const charNameElement = document.getElementById("char-name");
  if (charNameElement) {
    charNameElement.textContent = window.currentCharacter.name || "Aelindra";
  }

  // Update race and class
  const charRaceClassElement = document.getElementById("char-race-class");
  if (charRaceClassElement) {
    let raceClassText = "";
    if (window.currentCharacter.race && window.currentCharacter.class) {
      raceClassText = `${window.currentCharacter.race} ${window.currentCharacter.class}`;
    } else if (window.currentCharacter.race) {
      raceClassText = window.currentCharacter.race;
    } else if (window.currentCharacter.class) {
      raceClassText = window.currentCharacter.class;
    } else {
      raceClassText = "Seçilmemiş";
    }
    charRaceClassElement.textContent = raceClassText;
  }

  // Update level
  const charLevelElement = document.getElementById("char-level");
  if (charLevelElement) {
    charLevelElement.textContent = window.currentCharacter.level;
  }

  // Update XP
  const charXpElement = document.getElementById("char-xp");
  if (charXpElement) {
    charXpElement.textContent = `${window.currentCharacter.xp}/${window.currentCharacter.maxXp}`;
  }

  // Update HP
  const charHpElement = document.getElementById("char-hp");
  if (charHpElement) {
    charHpElement.textContent = `${window.currentCharacter.hp}/${window.currentCharacter.maxHp}`;
  }

  // Update Mana
  const charManaElement = document.getElementById("char-mana");
  if (charManaElement) {
    charManaElement.textContent = `${currentCharacter.mana}/${currentCharacter.maxMana}`;
  }

  console.log("✅ Character panel updated successfully");
};

// Global functions for NPC dialog
window.closeNPCDialog = function () {
  npcSystem.hideDialogPanel();
};

window.acceptQuest = function () {
  npcSystem.acceptQuest();
};

window.declineQuest = function () {
  npcSystem.declineQuest();
};

// FILE UPLOAD SYSTEM
window.uploadedFiles = [];

window.initializeFileUpload = function () {
  const fileInput = document.getElementById("file-input");
  const fileStatus = document.getElementById("file-status");
  const filesList = document.getElementById("files-list");

  if (fileInput) {
    fileInput.addEventListener("change", function (event) {
      const file = event.target.files[0];
      if (file) {
        handleFileUpload(file);
      }
    });
  }
};

window.handleFileUpload = function (file) {
  console.log("✅ FILE UPLOAD:", file.name);

  const fileStatus = document.getElementById("file-status");
  const filesList = document.getElementById("files-list");

  // Update status
  if (fileStatus) {
    fileStatus.textContent = `📤 Yükleniyor: ${file.name}`;
  }

  // Simulate file processing
  setTimeout(() => {
    // Add file to uploaded files list
    const fileId = `file_${Date.now()}`;
    const fileInfo = {
      id: fileId,
      name: file.name,
      size: file.size,
      type: file.type,
      uploadDate: new Date().toLocaleString(),
      content: "Dosya içeriği burada işlenecek...",
    };

    uploadedFiles.push(fileInfo);

    // Update status
    if (fileStatus) {
      fileStatus.textContent = `✅ Yüklendi: ${file.name}`;
    }

    // Add to files list
    if (filesList) {
      addFileToList(fileInfo);
    }

    // Reset file input
    const fileInput = document.getElementById("file-input");
    if (fileInput) {
      fileInput.value = "";
    }

    // Show success message
    alert(`📁 Dosya başarıyla yüklendi: ${file.name}`);

    // Process file content for AI scenarios
    processFileForAI(fileInfo);
  }, 1500);
};

window.addFileToList = function (fileInfo) {
  const filesList = document.getElementById("files-list");
  if (!filesList) return;

  const fileItem = document.createElement("div");
  fileItem.className = "file-item";
  fileItem.innerHTML = `
    <div class="file-info">
      <div class="file-name">📄 ${fileInfo.name}</div>
      <div class="file-details">
        <span class="file-size">${formatFileSize(fileInfo.size)}</span>
        <span class="file-date">${fileInfo.uploadDate}</span>
      </div>
    </div>
    <div class="file-actions">
      <button onclick="viewFileContent('${
        fileInfo.id
      }')" class="file-btn">👁️ Görüntüle</button>
      <button onclick="deleteFile('${
        fileInfo.id
      }')" class="file-btn delete">🗑️ Sil</button>
    </div>
  `;

  filesList.appendChild(fileItem);
};

window.formatFileSize = function (bytes) {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
};

window.viewFileContent = function (fileId) {
  const file = uploadedFiles.find((f) => f.id === fileId);
  if (file) {
    alert(
      `📄 ${file.name}\n\n${file.content}\n\nYükleme Tarihi: ${file.uploadDate}`
    );
  }
};

window.deleteFile = function (fileId) {
  if (confirm("Bu dosyayı silmek istediğinizden emin misiniz?")) {
    uploadedFiles = uploadedFiles.filter((f) => f.id !== fileId);
    updateFilesList();
    alert("🗑️ Dosya silindi!");
  }
};

window.updateFilesList = function () {
  const filesList = document.getElementById("files-list");
  if (!filesList) return;

  filesList.innerHTML = "";
  uploadedFiles.forEach((file) => {
    addFileToList(file);
  });
};

window.processFileForAI = function (fileInfo) {
  console.log("✅ PROCESSING FILE FOR AI:", fileInfo.name);

  // Simulate AI processing
  setTimeout(() => {
    const aiScenariosGrid = document.getElementById("ai-scenarios-grid");
    if (aiScenariosGrid) {
      const scenarioId = `ai_from_file_${Date.now()}`;
      const scenarioTitle = `Dosyadan Üretilen: ${fileInfo.name.split(".")[0]}`;

      // Add to scenarios
      scenarios[scenarioId] = {
        title: scenarioTitle,
        story: {
          start: {
            text: `Bu senaryo ${fileInfo.name} dosyasından AI tarafından üretildi. Dosya içeriği analiz edildi ve bu hikaye oluşturuldu.`,
            choices: [
              { text: "Dosya içeriğini keşfet", nextNode: "explore_content" },
              { text: "AI analizini gör", nextNode: "view_analysis" },
              { text: "Hikayeye başla", nextNode: "start_story" },
            ],
          },
        },
      };

      // Add to grid
      const scenarioCard = document.createElement("div");
      scenarioCard.className = "scenario-card ai-generated file-generated";
      scenarioCard.onclick = () => window.selectScenario(scenarioId);

      scenarioCard.innerHTML = `
        <div class="scenario-header">
          <h4>📄 ${scenarioTitle}</h4>
          <span class="difficulty medium">Dosyadan</span>
        </div>
        <p>Bu senaryo ${fileInfo.name} dosyasından AI tarafından üretildi.</p>
        <div class="ai-info">
          <small>🤖 Dosyadan üretildi - ${fileInfo.uploadDate}</small>
        </div>
      `;

      aiScenariosGrid.appendChild(scenarioCard);

      alert(
        `🎲 Dosyadan yeni senaryo üretildi: "${scenarioTitle}"\nAI Üretilen kategorisinde bulabilirsiniz!`
      );
    }
  }, 2000);
};

// DOM LOADED EVENT
window.addEventListener("DOMContentLoaded", function () {
  console.log("✅ DOM LOADED - INITIALIZING GAME");

  // Check for required elements
  const elements = [
    "scenario-selection",
    "active-game",
    "current-scenario-title",
    "story-text",
    "choices-grid",
  ];

  elements.forEach((elementId) => {
    const element = document.getElementById(elementId);
    if (element) {
      console.log(`✅ ${elementId}: Found`);
    } else {
      console.log(`❌ ${elementId}: Not found`);
    }
  });

  // Initialize file upload system
  initializeFileUpload();

  // Initialize first theme
  if (typeof switchTheme === "function") {
    switchTheme("fantasy");
  }

  // Initialize character panel
  if (typeof updateCharacterPanel === "function") {
    updateCharacterPanel();
  }

  console.log("✅ GAME INITIALIZED SUCCESSFULLY");
});

console.log("=== ENHANCED GAME SYSTEM READY ===");
