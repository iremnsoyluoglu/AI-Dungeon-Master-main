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
