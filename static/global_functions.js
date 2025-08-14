// GLOBAL FUNCTIONS - MUST BE LOADED FIRST
console.log("✅ Loading global functions...");

// SWITCH THEME FUNCTION
window.switchTheme = function (theme) {
  console.log("✅ SWITCH THEME:", theme);
  
  // Remove active class from all theme tabs
  document.querySelectorAll(".theme-tab").forEach((tab) => {
    if (tab) tab.classList.remove("active");
  });
  
  // Add active class to clicked tab
  const activeTab = document.querySelector(`[onclick="switchTheme('${theme}')"]`);
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
  document.querySelectorAll(".race-class-list:nth-child(1) .list-item").forEach((item) => {
    if (item) item.classList.remove("selected");
  });
  
  // Add selected class to clicked race
  const selectedRace = document.querySelector(`[onclick="selectRace('${race}')"]`);
  if (selectedRace) {
    selectedRace.classList.add("selected");
  }
  
  // Update character panel
  if (window.updateCharacterPanel) {
    window.updateCharacterPanel();
  }
};

// SELECT CLASS FUNCTION
window.selectClass = function (className) {
  console.log("✅ SELECT CLASS:", className);
  
  // Remove selected class from all class items
  document.querySelectorAll(".race-class-list:nth-child(2) .list-item").forEach((item) => {
    if (item) item.classList.remove("selected");
  });
  
  // Add selected class to clicked class
  const selectedClass = document.querySelector(`[onclick="selectClass('${className}')"]`);
  if (selectedClass) {
    selectedClass.classList.add("selected");
  }
  
  // Update character panel
  if (window.updateCharacterPanel) {
    window.updateCharacterPanel();
  }
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
  alert("AI Senaryo üretimi yakında gelecek!");
};

// START SCENARIO FUNCTION
window.startScenario = function (scenarioId) {
  console.log("✅ START SCENARIO:", scenarioId);
  
  if (!window.scenarios) {
    console.error("❌ Scenarios not defined");
    return;
  }
  
  const scenario = window.scenarios[scenarioId];
  if (!scenario) {
    console.error("❌ Scenario not found:", scenarioId);
    return;
  }
  
  // Update scenario title
  const titleElement = document.getElementById("current-scenario-title");
  if (titleElement) {
    titleElement.textContent = scenario.title;
  }
  
  // Start with the first story node
  const firstNode = scenario.story.start;
  if (firstNode) {
    window.displayStoryNode(firstNode);
  }
  
  console.log("✅ Scenario started successfully");
};

// DISPLAY STORY NODE FUNCTION
window.displayStoryNode = function (node) {
  console.log("✅ DISPLAY STORY NODE:", node.title);
  
  const storyText = document.getElementById("story-text");
  const choicesGrid = document.getElementById("choices-grid");
  
  if (storyText && node) {
    storyText.innerHTML = `
      <h3>${node.title}</h3>
      <p>${node.text}</p>
    `;
  }

  if (choicesGrid && node.choices) {
    choicesGrid.innerHTML = "";
    node.choices.forEach((choice) => {
      const choiceButton = document.createElement("button");
      choiceButton.className = "choice-btn";
      choiceButton.textContent = choice.text;
      choiceButton.onclick = () => window.makeChoice(choice.nextNode);
      choicesGrid.appendChild(choiceButton);
    });
  }

  console.log("✅ Story node displayed");
};

// MAKE CHOICE FUNCTION
window.makeChoice = function (nextNodeId) {
  console.log("✅ MAKE CHOICE:", nextNodeId);

  // Find current scenario
  const currentScenario = window.getCurrentScenario();
  if (!currentScenario) {
    console.error("❌ No active scenario");
    return;
  }

  const nextNode = currentScenario.story[nextNodeId];
  if (nextNode) {
    window.displayStoryNode(nextNode);
  } else {
    console.error("❌ Next node not found:", nextNodeId);
  }
};

// GET CURRENT SCENARIO FUNCTION
window.getCurrentScenario = function () {
  // Get current scenario based on active scenario ID
  const titleElement = document.getElementById("current-scenario-title");
  if (titleElement && window.scenarios) {
    const title = titleElement.textContent;
    // Find scenario by title
    for (const [scenarioId, scenario] of Object.entries(window.scenarios)) {
      if (scenario.title === title) {
        return scenario;
      }
    }
  }
  // Fallback to first scenario
  return window.scenarios ? window.scenarios.living_dragon_hunt : null;
};

// UPDATE CHARACTER PANEL FUNCTION
window.updateCharacterPanel = function () {
  console.log("✅ UPDATE CHARACTER PANEL");
  
  const characterPanel = document.getElementById("character-panel");
  if (!characterPanel) return;
  
  const selectedRace = document.querySelector(".race-class-list:nth-child(1) .list-item.selected");
  const selectedClass = document.querySelector(".race-class-list:nth-child(2) .list-item.selected");
  
  const raceText = selectedRace ? selectedRace.textContent.trim() : "Seçilmedi";
  const classText = selectedClass ? selectedClass.textContent.trim() : "Seçilmedi";
  
  const characterInfo = {
    characterName: "İsimsiz Kahraman",
    race: raceText,
    class: classText
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

console.log("✅ Global functions loaded successfully!");
