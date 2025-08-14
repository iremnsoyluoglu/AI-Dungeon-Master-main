// Global variables
let currentUser = null;
let currentCharacter = null;
let currentScenario = null;
let currentGameSession = null;
let currentCombatSession = null;
let currentTheme = "fantasy"; // Add this missing variable
let hiddenMoralState = {
  karma: 0,
  relationships: {},
  reputation: {},
  choices: [],
  moralAlignment: "neutral",
  storyFlags: {},
  npcMemories: {},
  worldState: {},
};

const API_BASE = "http://localhost:5002";

// ===== UTILITY FUNCTIONS =====

function showMessage(message, type = "info") {
  console.log(`[${type.toUpperCase()}] ${message}`);

  // Create a simple message display
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${type}`;
  messageDiv.textContent = message;
  messageDiv.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 10px 20px;
    border-radius: 5px;
    color: white;
    font-weight: bold;
    z-index: 10000;
    animation: slideIn 0.3s ease;
  `;

  // Set background color based on type
  switch (type) {
    case "success":
      messageDiv.style.backgroundColor = "#28a745";
      break;
    case "error":
      messageDiv.style.backgroundColor = "#dc3545";
      break;
    case "warning":
      messageDiv.style.backgroundColor = "#ffc107";
      messageDiv.style.color = "#000";
      break;
    default:
      messageDiv.style.backgroundColor = "#17a2b8";
  }

  document.body.appendChild(messageDiv);

  // Remove message after 3 seconds
  setTimeout(() => {
    if (messageDiv.parentNode) {
      messageDiv.parentNode.removeChild(messageDiv);
    }
  }, 3000);
}

// Initialize when page loads
document.addEventListener("DOMContentLoaded", function () {
  console.log("🎮 AI Dungeon Master başlatılıyor...");

  // Check authentication status
  checkAuthStatus();

  // Setup event listeners
  setupEventListeners();
});

// ===== AUTHENTICATION FUNCTIONS =====

async function checkAuthStatus() {
  const token = localStorage.getItem("auth_token");
  if (token) {
    try {
      const response = await fetch(`${API_BASE}/api/auth/verify`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token }),
      });

      const data = await response.json();
      if (data.success) {
        currentUser = {
          id: data.user_id,
          username: data.username,
          is_guest: data.is_guest,
        };
        showGameScreen();
        updateUserInfo();
      } else {
        localStorage.removeItem("auth_token");
        showAuthScreen();
      }
    } catch (error) {
      console.error("Auth check error:", error);
      showAuthScreen();
    }
  } else {
    showAuthScreen();
  }
}

function showAuthScreen() {
  document.getElementById("auth-screen").style.display = "block";
  document.getElementById("game-screen").style.display = "none";
}

function showGameScreen() {
  console.log("🎮 showGameScreen çağrıldı");

  // Hide auth screen if it exists
  const authScreen = document.getElementById("auth-screen");
  if (authScreen) {
    authScreen.style.display = "none";
  }

  // Show game screen
  const gameScreen = document.getElementById("game-screen");
  if (gameScreen) {
    gameScreen.style.display = "block";
  }

  // Hide all modals to ensure they don't show
  const modals = document.querySelectorAll(".modal");
  modals.forEach((modal) => {
    modal.style.display = "none";
  });

  console.log("✅ showGameScreen tamamlandı - Modals hidden!");
}

function showAuthTab(tabName) {
  // Hide all tabs
  document.querySelectorAll(".auth-tab").forEach((tab) => {
    tab.classList.remove("active");
  });
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.classList.remove("active");
  });

  // Show selected tab
  document.getElementById(`${tabName}-tab`).classList.add("active");
  event.target.classList.add("active");
}

async function registerUser() {
  const username = document.getElementById("register-username").value;
  const email = document.getElementById("register-email").value;
  const password = document.getElementById("register-password").value;
  const passwordConfirm = document.getElementById(
    "register-password-confirm"
  ).value;

  console.log("📝 Register denemesi:", { username, email, password: "***" });

  if (password !== passwordConfirm) {
    showMessage("Şifreler eşleşmiyor!", "error");
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    });

    console.log("📡 Register response status:", response.status);
    const data = await response.json();
    console.log("📄 Register response data:", data);

    if (data.success) {
      showMessage("Kayıt başarılı! Şimdi giriş yapabilirsiniz.", "success");
      showAuthTab("login");
    } else {
      console.error("❌ Register hatası:", data.error);
      showMessage(data.error, "error");
    }
  } catch (error) {
    console.error("❌ Register exception:", error);
    showMessage("Sunucu bağlantı hatası. Lütfen tekrar deneyin.", "error");
  }
}

async function loginUser() {
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;

  console.log("🔑 Login denemesi:", { username, password: "***" });

  try {
    const response = await fetch(`${API_BASE}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    console.log("📡 Login response status:", response.status);
    const data = await response.json();
    console.log("📄 Login response data:", data);

    if (data.success) {
      console.log("✅ Login başarılı:", data);

      // Store user data
      currentUser = {
        id: data.user_id,
        username: data.username,
        is_guest: false,
        token: data.token,
      };

      // Store token in localStorage
      localStorage.setItem("auth_token", data.token);
      localStorage.setItem("user_data", JSON.stringify(currentUser));

      // Show success message
      showMessage("Giriş başarılı! Oyun başlıyor...", "success");

      // Switch to game screen
      setTimeout(() => {
        showGameScreen();
        showMainMenu();
      }, 1000);
    } else {
      console.error("❌ Login hatası:", data.error);
      showMessage(data.error, "error");
    }
  } catch (error) {
    console.error("❌ Login exception:", error);
    showMessage("Sunucu bağlantı hatası. Lütfen tekrar deneyin.", "error");
  }
}

// Global function for guest user creation
window.createGuestUser = async function () {
  try {
    console.log("👤 Misafir kullanıcı oluşturuluyor...");

    const response = await fetch(`${API_BASE}/api/auth/guest`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const result = await response.json();
    console.log("📄 Misafir response:", result);

    if (result.success) {
      console.log("✅ Misafir kullanıcı başarıyla oluşturuldu:", result);

      // Store user data
      currentUser = {
        id: result.user_id,
        username: result.username,
        is_guest: true,
        token: result.token,
      };

      // Store token in localStorage
      localStorage.setItem("auth_token", result.token);
      localStorage.setItem("user_data", JSON.stringify(currentUser));

      // Show success message
      showMessage(
        "Misafir kullanıcı başarıyla oluşturuldu! Oyun başlıyor...",
        "success"
      );

      console.log("🔄 Game screen'e geçiliyor...");

      // Switch to game screen and load data
      setTimeout(async () => {
        console.log("🎮 showGameScreen çağrılıyor...");
        try {
          showGameScreen();
          console.log("📋 showMainMenu çağrılıyor...");
          showMainMenu();

          // Load character classes and races
          await loadCharacterClasses();
          await loadCharacterRaces();
          await loadScenarioGenres();
          await loadExistingScenarios();

          console.log("✅ Misafir giriş tamamlandı!");
        } catch (error) {
          console.error("❌ Game screen geçiş hatası:", error);
          showMessage("Oyun ekranına geçiş hatası!", "error");
        }
      }, 1000);
    } else {
      console.error("❌ Misafir kullanıcı oluşturma hatası:", result.error);
      showMessage(
        `Misafir kullanıcı oluşturma hatası: ${result.error}`,
        "error"
      );
    }
  } catch (error) {
    console.error("❌ Misafir kullanıcı oluşturma hatası:", error);
    showMessage("Sunucu bağlantı hatası. Lütfen tekrar deneyin.", "error");
  }
};

async function createGuestUser() {
  try {
    console.log("👤 Misafir kullanıcı oluşturuluyor...");

    const response = await fetch(`${API_BASE}/api/auth/guest`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });

    const data = await response.json();

    if (data.success) {
      console.log("✅ Misafir kullanıcı oluşturuldu:", data.username);

      // Store token
      localStorage.setItem("auth_token", data.token);

      // Set current user
      currentUser = {
        id: data.user_id,
        username: data.username,
        is_guest: true,
        token: data.token,
      };

      // Show game screen
      showGameScreen();
      updateUserInfo();

      showMessage("Misafir olarak giriş yapıldı!", "success");
    } else {
      console.error("❌ Misafir kullanıcı oluşturulamadı:", data.error);
      showMessage("Misafir girişi başarısız: " + data.error, "error");
    }
  } catch (error) {
    console.error("❌ Misafir girişi hatası:", error);
    showMessage("Bağlantı hatası! Lütfen tekrar deneyin.", "error");
  }
}

function logout() {
  localStorage.removeItem("auth_token");
  currentUser = null;
  currentCharacter = null;
  currentScenario = null;
  currentGameSession = null;
  currentCombatSession = null;
  hiddenMoralState = {
    karma: 0,
    relationships: {},
    reputation: {},
    choices: [],
    moralAlignment: "neutral",
    storyFlags: {},
    npcMemories: {},
    worldState: {},
  };
  showAuthScreen();
}

function updateUserInfo() {
  if (currentUser) {
    document.getElementById("current-user").textContent = currentUser.username;
  }
}

// ===== CHARACTER SYSTEM =====

async function loadCharacterClasses() {
  try {
    const response = await fetch(`${API_BASE}/api/game/character/classes`);
    const data = await response.json();

    // Handle both formats: with and without success field
    const classes = data.classes || (data.success && data.classes);

    if (classes) {
      const select = document.getElementById("char-class");
      if (select) {
        select.innerHTML = '<option value="">Sınıf seçin...</option>';

        classes.forEach((charClass) => {
          const option = document.createElement("option");
          option.value = charClass.id;
          option.textContent = `${charClass.name} - ${charClass.description}`;
          select.appendChild(option);
        });

        console.log("Karakter sınıfları başarıyla yüklendi:", classes.length);
      } else {
        console.error("char-class select elementi bulunamadı");
      }
    } else {
      console.error("API'den karakter sınıfları alınamadı:", data);
    }
  } catch (error) {
    console.error("Karakter sınıfları yüklenemedi:", error);
  }
}

async function loadCharacterRaces() {
  try {
    const response = await fetch(`${API_BASE}/api/game/character/races`);
    const data = await response.json();

    if (data.success) {
      const select = document.getElementById("char-race");
      select.innerHTML = '<option value="">Irk seçin...</option>';

      data.races.forEach((race) => {
        const option = document.createElement("option");
        option.value = race.id;
        option.textContent = `${race.name} - ${race.description}`;
        select.appendChild(option);
      });
    }
  } catch (error) {
    console.error("Karakter ırkları yüklenemedi:", error);
  }
}

async function createCharacter() {
  const name = document.getElementById("char-name").value;
  const charClass = document.getElementById("char-class").value;
  const race = document.getElementById("char-race").value;
  const background = document.getElementById("char-background").value;
  const personality = document.getElementById("char-personality").value;
  const ideals = document.getElementById("char-ideals").value;
  const bonds = document.getElementById("char-bonds").value;
  const flaws = document.getElementById("char-flaws").value;

  if (!name || !charClass || !race) {
    showMessage("Lütfen gerekli alanları doldurun!", "error");
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/api/game/character/save`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${
          currentUser?.token || localStorage.getItem("auth_token")
        }`,
      },
      body: JSON.stringify({
        name,
        class: charClass,
        race,
        background,
        personality,
        ideals,
        bonds,
        flaws,
      }),
    });

    const data = await response.json();

    if (data.success) {
      currentCharacter = {
        id: data.character_id,
        name,
        class: charClass,
        race,
        background,
        personality,
        ideals,
        bonds,
        flaws,
      };

      showMessage("Karakter başarıyla oluşturuldu!", "success");

      // Otomatik olarak senaryo seçimine geç
      setTimeout(() => {
        showSection("scenario-selection");
        showMessage("Şimdi bir senaryo seçin!", "info");
      }, 1000);
    } else {
      showMessage(data.error, "error");
    }
  } catch (error) {
    console.error("Karakter oluşturma hatası:", error);
    showMessage("Karakter oluşturulamadı!", "error");
  }
}

// ===== SCENARIO SYSTEM =====

async function loadScenarioGenres() {
  try {
    const response = await fetch(`${API_BASE}/api/scenarios/genres`);
    const data = await response.json();

    if (data.success) {
      const select = document.getElementById("genre-filter");
      select.innerHTML = '<option value="">Tüm Türler</option>';

      data.genres.forEach((genre) => {
        const option = document.createElement("option");
        option.value = genre.id;
        option.textContent = `${genre.icon} ${genre.name}`;
        select.appendChild(option);
      });
    }
  } catch (error) {
    console.error("Senaryo türleri yüklenemedi:", error);
  }
}

async function loadExistingScenarios() {
  try {
    const response = await fetch(`${API_BASE}/api/scenarios`);
    const data = await response.json();

    if (data.success) {
      const scenariosContainer = document.getElementById("scenarios-list");
      scenariosContainer.innerHTML = "";

      data.scenarios.forEach((scenario) => {
        const scenarioCard = document.createElement("div");
        scenarioCard.className = "scenario-card";
        scenarioCard.innerHTML = `
          <h3>${scenario.title}</h3>
          <p>${scenario.description}</p>
          <div class="scenario-meta">
            <span class="difficulty ${scenario.difficulty}">${scenario.difficulty}</span>
            <span class="genre">${scenario.genre}</span>
          </div>
          <button onclick="selectScenario('${scenario.id}')" class="btn-primary">
            Bu Senaryoyu Seç
          </button>
        `;
        scenariosContainer.appendChild(scenarioCard);
      });
    }
  } catch (error) {
    console.error("Mevcut senaryolar yüklenemedi:", error);
  }
}

function selectScenario(scenarioId) {
  console.log("🎯 Senaryo seçildi:", scenarioId);

  // Senaryo bilgilerini al
  fetch(`${API_BASE}/api/scenarios`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        const scenario = data.scenarios.find((s) => s.id === scenarioId);
        if (scenario) {
          currentScenario = scenario;
          showMessage(`"${scenario.title}" senaryosu seçildi!`, "success");

          // Otomatik olarak oyunu başlat
          setTimeout(() => {
            startGameSession();
          }, 1000);
        }
      }
    })
    .catch((error) => {
      console.error("Senaryo seçme hatası:", error);
      showMessage("Senaryo seçilemedi!", "error");
    });
}

async function startGameSession() {
  if (!currentCharacter) {
    showMessage("Önce bir karakter oluşturun!", "error");
    return;
  }

  if (!currentScenario) {
    showMessage("Önce bir senaryo seçin!", "error");
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/api/game/session/start`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${
          currentUser?.token || localStorage.getItem("auth_token")
        }`,
      },
      body: JSON.stringify({
        character_id: currentCharacter.id,
        scenario_id: currentScenario.id,
        scenario: currentScenario,
      }),
    });

    const data = await response.json();

    if (data.success) {
      currentGameSession = {
        id: data.session_id,
        character: currentCharacter,
        scenario: currentScenario,
        game_state: data.game_state,
      };

      showMessage("Oyun başlatıldı! Macera başlıyor...", "success");

      // Oyun ekranına geç
      setTimeout(() => {
        showSection("game-session");
        startAdventure();
      }, 1000);
    } else {
      showMessage(data.error, "error");
    }
  } catch (error) {
    console.error("Oyun başlatma hatası:", error);
    showMessage("Oyun başlatılamadı!", "error");
  }
}

// ===== GAME FUNCTIONS =====

function startAdventure() {
  console.log("🎮 Macera başlıyor...");

  // Senaryo başlığını güncelle
  document.getElementById("scenario-title").textContent = currentScenario.title;
  document.getElementById("character-name").textContent = currentCharacter.name;
  document.getElementById("character-class").textContent =
    currentCharacter.class;
  document.getElementById("character-race").textContent = currentCharacter.race;

  // İlk hikaye metnini göster
  const storyText = document.getElementById("story-text");
  storyText.innerHTML = `
    <h3>${currentScenario.title}</h3>
    <p>${currentScenario.description}</p>
    <p>Karakteriniz <strong>${currentCharacter.name}</strong> olarak, ${currentCharacter.class} sınıfında bir ${currentCharacter.race} olarak bu maceraya başlıyor.</p>
    <p>Hazır mısınız? Seçenekleriniz aşağıda...</p>
  `;

  // İlk seçenekleri göster
  showInitialChoices();
}

function showInitialChoices() {
  const choicesContainer = document.getElementById("choices-container");
  choicesContainer.innerHTML = `
    <button onclick="makeChoice('explore')" class="choice-btn">
      🔍 Etrafı Keşfet
    </button>
    <button onclick="makeChoice('talk')" class="choice-btn">
      💬 NPC'lerle Konuş
    </button>
    <button onclick="makeChoice('combat')" class="choice-btn">
      ⚔️ Savaşa Hazırlan
    </button>
    <button onclick="makeChoice('stealth')" class="choice-btn">
      🥷 Gizlice İlerle
    </button>
  `;
}

function makeChoice(choice) {
  console.log("🎯 Seçim yapıldı:", choice);

  // Seçime göre hikaye devam et
  const storyText = document.getElementById("story-text");

  switch (choice) {
    case "explore":
      storyText.innerHTML += `
        <p>Etrafı keşfetmeye başladınız. Gizli geçitler ve hazineler bulabilirsiniz...</p>
      `;
      break;
    case "talk":
      storyText.innerHTML += `
        <p>NPC'lerle konuşmaya başladınız. Yeni bilgiler ve görevler alabilirsiniz...</p>
      `;
      break;
    case "combat":
      storyText.innerHTML += `
        <p>Savaşa hazırlandınız. Düşmanlar yaklaşıyor...</p>
      `;
      break;
    case "stealth":
      storyText.innerHTML += `
        <p>Gizlice ilerlemeye başladınız. Kimse sizi fark etmiyor...</p>
      `;
      break;
  }

  // Yeni seçenekler göster
  showNewChoices(choice);
}

function showNewChoices(previousChoice) {
  const choicesContainer = document.getElementById("choices-container");

  // Önceki seçime göre yeni seçenekler
  const newChoices = {
    explore: [
      { id: "search", text: "🔍 Detaylı Arama Yap", action: "search" },
      { id: "move", text: "🚶 İlerle", action: "move" },
      { id: "return", text: "↩️ Geri Dön", action: "return" },
    ],
    talk: [
      { id: "ask", text: "❓ Soru Sor", action: "ask" },
      { id: "trade", text: "💰 Ticaret Yap", action: "trade" },
      { id: "quest", text: "📜 Görev Al", action: "quest" },
    ],
    combat: [
      { id: "attack", text: "⚔️ Saldır", action: "attack" },
      { id: "defend", text: "🛡️ Savun", action: "defend" },
      { id: "flee", text: "🏃 Kaç", action: "flee" },
    ],
    stealth: [
      { id: "sneak", text: "🥷 Sız", action: "sneak" },
      { id: "observe", text: "👁️ Gözlemle", action: "observe" },
      { id: "hide", text: "🌿 Saklan", action: "hide" },
    ],
  };

  const choices = newChoices[previousChoice] || [
    { id: "continue", text: "➡️ Devam Et", action: "continue" },
  ];

  choicesContainer.innerHTML = choices
    .map(
      (choice) =>
        `<button onclick="makeChoice('${choice.action}')" class="choice-btn">${choice.text}</button>`
    )
    .join("");
}

// ===== UI FUNCTIONS =====

function showSection(sectionName) {
  // Hide all sections
  document.querySelectorAll(".game-section").forEach((section) => {
    section.style.display = "none";
  });

  // Show selected section
  document.getElementById(sectionName).style.display = "block";

  // Update game status
  document.getElementById("game-status").textContent = sectionName
    .replace("-", " ")
    .toUpperCase();
}

function showMainMenu() {
  showSection("main-menu");
}

function showMessage(message, type = "info") {
  console.log(`📢 ${type.toUpperCase()}: ${message}`);

  // Create message element
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${type}`;
  messageDiv.textContent = message;

  // Add to page
  document.body.appendChild(messageDiv);

  // Remove after 3 seconds
  setTimeout(() => {
    messageDiv.remove();
  }, 3000);
}

function setupEventListeners() {
  // Auth form submissions
  document.getElementById("login-form")?.addEventListener("submit", (e) => {
    e.preventDefault();
    loginUser();
  });

  document.getElementById("register-form")?.addEventListener("submit", (e) => {
    e.preventDefault();
    registerUser();
  });

  document.getElementById("character-form")?.addEventListener("submit", (e) => {
    e.preventDefault();
    createCharacter();
  });
}

// ===== GAME ACTION FUNCTIONS =====

function startCombat() {
  console.log("⚔️ Savaş başlatılıyor...");
  showMessage("Savaş başlatıldı!", "info");
  showSection("combat-panel");
}

function rollDice() {
  const result = Math.floor(Math.random() * 20) + 1;
  console.log("🎲 Zar atıldı:", result);
  showMessage(`Zar sonucu: ${result}`, "info");
}

function explore() {
  console.log("🗺️ Keşif başlatılıyor...");
  showMessage("Keşif başlatıldı!", "info");
}

function rest() {
  console.log("🏕️ Dinlenme başlatılıyor...");
  showMessage("Dinlenme başlatıldı!", "info");
}

function loadClasses() {
  console.log("👥 Sınıflar yükleniyor...");
  loadCharacterClasses();
}

function loadSkills() {
  console.log("⚔️ Skilller yükleniyor...");
  showMessage("Skilller yüklendi!", "info");
}

function loadRaces() {
  console.log("🧙 Irklar yükleniyor...");
  loadCharacterRaces();
}

function loadScenarios() {
  console.log("📚 Senaryolar yükleniyor...");
  loadExistingScenarios();
}

function startStory() {
  console.log("🎬 Hikaye başlatılıyor...");
  showMessage("Hikaye başlatıldı!", "info");
}

function showProgress() {
  console.log("📊 İlerleme durumu gösteriliyor...");
  showMessage("İlerleme durumu gösteriliyor!", "info");
}

function talkToNPC() {
  console.log("👥 NPC ile konuşma başlatılıyor...");
  showMessage("NPC ile konuşma başlatıldı!", "info");
}

function createBranch() {
  console.log("🌿 Yeni dal oluşturuluyor...");
  showMessage("Yeni dal oluşturuldu!", "info");
}

function listBranches() {
  console.log("📋 Dallar listeleniyor...");
  showMessage("Dallar listeleniyor!", "info");
}

function showStorytelling() {
  console.log("📖 Hikaye anlatımı gösteriliyor...");
  showMessage("Hikaye anlatımı gösteriliyor!", "info");
}

// ===== ADDITIONAL GAME FUNCTIONS =====

function loadStoryProgress() {
  console.log("📊 Hikaye ilerleme durumu yükleniyor...");
  showMessage("Hikaye ilerleme durumu yüklendi!", "info");
}

function interactWithNPC() {
  console.log("👥 NPC ile etkileşim başlatılıyor...");
  showMessage("NPC ile etkileşim başlatıldı!", "info");
}

function createStoryBranch() {
  console.log("🌿 Yeni hikaye dalı oluşturuluyor...");
  showMessage("Yeni hikaye dalı oluşturuldu!", "info");
}

function loadStoryBranches() {
  console.log("📋 Hikaye dalları listeleniyor...");
  showMessage("Hikaye dalları listeleniyor!", "info");
}

function showStoryBranches() {
  console.log("📖 Hikaye dalları gösteriliyor...");
  showMessage("Hikaye dalları gösteriliyor!", "info");
}

function saveGame() {
  console.log("💾 Oyun kaydediliyor...");
  showMessage("Oyun kaydedildi!", "success");
}

function loadSaves() {
  console.log("📂 Kayıtlar yükleniyor...");
  showMessage("Kayıtlar yüklendi!", "info");
}

function startGame() {
  console.log("🎮 Oyun başlatılıyor...");
  showMessage("Oyun başlatıldı!", "success");
}

function checkHealth() {
  console.log("🏥 Sistem sağlığı kontrol ediliyor...");
  showMessage("Sistem sağlığı kontrol edildi!", "info");
}

// Force close the AI modal immediately
window.forceCloseModal = function () {
  const ragModal = document.getElementById("rag-question-modal");
  if (ragModal) {
    ragModal.style.display = "none";
  }
  const modals = document.querySelectorAll(".modal");
  modals.forEach((modal) => {
    modal.style.display = "none";
  });
  console.log("🔒 All modals force closed!");
};

// ===== AI FEATURES =====

function openAIAgentPanel() {
  console.log("🤖 AI Agent Panel - Bu özellik geliştiriliyor!");
  showMessage("AI Agent Panel - Bu özellik geliştiriliyor!", "info");
  // DO NOT show modal - just show a message
}

function openAIStoryCreator() {
  console.log("✨ AI Hikaye Oluşturucu açılıyor...");
  const modal = document.getElementById("ai-story-modal");
  if (modal) {
    modal.style.display = "flex";
  }
}

function openRAGQuestion() {
  console.log("❓ RAG Soru Sistemi açılıyor...");
  showMessage("RAG Soru Sistemi - Bu özellik geliştiriliyor!", "info");
}

function generateAIStory() {
  console.log("✨ AI Hikaye üretiliyor...");
  const theme = document.getElementById("story-theme").value;
  const difficulty = document.getElementById("story-difficulty").value;
  const level = document.getElementById("story-level").value;
  const length = document.getElementById("story-length").value;
  const requests = document.getElementById("story-requests").value;

  showMessage("AI Hikaye üretiliyor...", "info");

  // Simulate AI story generation
  setTimeout(() => {
    const storyContent = document.getElementById("ai-story-content");
    storyContent.innerHTML = `
      <h4>${theme.toUpperCase()} Hikayesi</h4>
      <p>Seviye ${level} için ${difficulty} zorlukta ${length} bir hikaye oluşturuldu.</p>
      <p>Özel istekleriniz: ${requests || "Belirtilmedi"}</p>
      <p>Bu hikaye AI tarafından özel olarak sizin için oluşturuldu!</p>
    `;
    document.getElementById("generated-story").style.display = "block";
  }, 2000);
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = "none";
  }
}

// Load scenarios function
function loadScenarios() {
  console.log("📚 Scenarios loading...");
  // This will load the scenarios when the page loads
}

// Call it immediately when script loads
if (typeof window !== "undefined") {
  setTimeout(() => {
    window.forceCloseModal();
  }, 50);
}

// ===== GAME BUTTON FUNCTIONS =====

function selectTheme(theme) {
  console.log(`🎨 Tema seçildi: ${theme}`);
  currentTheme = theme;

  // Update UI to show selected theme
  document.querySelectorAll(".theme-btn").forEach((btn) => {
    btn.classList.remove("active");
  });
  event.target.classList.add("active");

  // Load races and classes for selected theme
  loadRacesAndClasses(theme);

  showMessage(`${theme.toUpperCase()} teması seçildi!`, "success");
}

function showScenarioSelection() {
  console.log("📚 Senaryo seçimi açılıyor...");
  const modal = document.getElementById("scenario-modal");
  if (modal) {
    modal.style.display = "flex";
    loadScenarios();
  }
}

function showCharacterCreation() {
  console.log("👤 Karakter oluşturma açılıyor...");
  const modal = document.getElementById("character-modal");
  if (modal) {
    modal.style.display = "flex";
    loadRacesAndClasses(currentTheme || "fantasy");
  }
}

function createCharacter() {
  console.log("👤 Karakter oluşturuluyor...");
  const selectedRace = document.getElementById("selected-race").textContent;
  const selectedClass = document.getElementById("selected-class").textContent;

  if (selectedRace === "Seçilmedi" || selectedClass === "Seçilmedi") {
    showMessage("Lütfen önce ırk ve sınıf seçin!", "error");
    return;
  }

  currentCharacter = {
    race: selectedRace,
    class: selectedClass,
    level: 1,
    xp: 0,
    karma: 0,
    attributes: {
      str: 10,
      dex: 10,
      int: 10,
      con: 10,
      wis: 10,
      cha: 10,
    },
  };

  updateCharacterDisplay();
  showMessage("Karakter oluşturuldu!", "success");
}

function startScenario() {
  console.log("🎮 Senaryo başlatılıyor...");
  if (!currentCharacter) {
    showMessage("Önce karakter oluşturun!", "error");
    return;
  }
  if (!currentScenario) {
    showMessage("Önce senaryo seçin!", "error");
    return;
  }

  showMessage("Senaryo başlatıldı!", "success");
  // Load scenario content
  loadScenarioContent(currentScenario);
}

function rollDice() {
  console.log("🎲 Zar atılıyor...");
  const result = Math.floor(Math.random() * 20) + 1;
  showMessage(`Zar sonucu: ${result}`, "info");

  // Show dice roll alert
  const alert = document.getElementById("dice-roll-alert");
  if (alert) {
    alert.style.display = "flex";
    setTimeout(() => {
      alert.style.display = "none";
    }, 2000);
  }
}

function checkInventory() {
  console.log("🎒 Envanter kontrol ediliyor...");
  showMessage("Envanter açıldı!", "info");
}

function loadRacesAndClasses(theme) {
  console.log(`🏃 Irk ve sınıflar yükleniyor: ${theme}`);

  const races = {
    fantasy: ["İnsan", "Elf", "Cüce", "Ork", "Yarı Elf"],
    warhammer: ["İnsan", "Space Marine", "Eldar", "Ork", "Tau"],
    cyberpunk: ["İnsan", "Android", "Cyborg", "Mutant", "AI"],
  };

  const classes = {
    fantasy: ["Savaşçı", "Büyücü", "Rahip", "Hırsız", "Paladin"],
    warhammer: [
      "Space Marine",
      "Imperial Guard",
      "Tech Priest",
      "Inquisitor",
      "Commissar",
    ],
    cyberpunk: ["Netrunner", "Solo", "Fixer", "Techie", "Nomad"],
  };

  // Update race options
  const raceOptions = document.getElementById("dynamic-races");
  if (raceOptions) {
    raceOptions.innerHTML = races[theme]
      .map(
        (race) =>
          `<button class="option-btn" onclick="selectRace('${race}')">${race}</button>`
      )
      .join("");
  }

  // Update class options
  const classOptions = document.getElementById("dynamic-classes");
  if (classOptions) {
    classOptions.innerHTML = classes[theme]
      .map(
        (cls) =>
          `<button class="option-btn" onclick="selectClass('${cls}')">${cls}</button>`
      )
      .join("");
  }
}

function selectRace(race) {
  console.log(`🏃 Irk seçildi: ${race}`);
  document.getElementById("selected-race").textContent = race;
  showMessage(`${race} ırkı seçildi!`, "success");
}

function selectClass(cls) {
  console.log(`⚔️ Sınıf seçildi: ${cls}`);
  document.getElementById("selected-class").textContent = cls;
  showMessage(`${cls} sınıfı seçildi!`, "success");
}

function updateCharacterDisplay() {
  if (currentCharacter) {
    document.getElementById("selected-race").textContent =
      currentCharacter.race;
    document.getElementById("selected-class").textContent =
      currentCharacter.class;
    document.getElementById("character-level").textContent =
      currentCharacter.level;
    document.getElementById(
      "character-xp"
    ).textContent = `${currentCharacter.xp}/100`;
    document.getElementById("character-karma").textContent =
      currentCharacter.karma;
  }
}

function loadScenarioContent(scenarioId) {
  console.log(`📖 Senaryo içeriği yükleniyor: ${scenarioId}`);

  fetch(`${API_BASE}/api/scenario/${scenarioId}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        const storyText = document.getElementById("story-text");
        storyText.innerHTML = `
          <h3>${data.scenario.title}</h3>
          <p>${data.scenario.description}</p>
          <div class="scenario-actions">
            <button class="action-btn primary" onclick="startScenario()">
              <i class="fas fa-play"></i> MACERAYA BAŞLA
            </button>
          </div>
        `;
      }
    })
    .catch((error) => {
      console.error("Senaryo yükleme hatası:", error);
      showMessage("Senaryo yüklenirken hata oluştu!", "error");
    });
}

function loadExistingScenarios() {
  console.log("📚 Mevcut senaryolar yükleniyor...");

  fetch(`${API_BASE}/api/scenarios`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        const scenarioList = document.getElementById("scenario-list");
        if (scenarioList) {
          scenarioList.innerHTML = data.scenarios
            .map(
              (scenario) => `
            <div class="scenario-item" onclick="selectScenario('${scenario.id}')">
              <h4>${scenario.title}</h4>
              <p>${scenario.description}</p>
              <span class="scenario-difficulty">${scenario.difficulty}</span>
            </div>
          `
            )
            .join("");
        }
      }
    })
    .catch((error) => {
      console.error("Senaryo listesi yükleme hatası:", error);
      showMessage("Senaryolar yüklenirken hata oluştu!", "error");
    });
}

function selectScenario(scenarioId) {
  console.log(`📖 Senaryo seçildi: ${scenarioId}`);
  currentScenario = scenarioId;

  // Close modal
  closeModal("scenario-modal");

  // Show start button
  const startBtn = document.getElementById("start-scenario-btn");
  if (startBtn) {
    startBtn.style.display = "inline-block";
  }

  showMessage(
    "Senaryo seçildi! Maceraya başlamak için butona tıklayın.",
    "success"
  );
}

// ===== FORCE HIDE RAG MODALS =====
function forceHideRAGModals() {
  const ragModal = document.getElementById("rag-upload-modal");
  if (ragModal) {
    ragModal.style.display = "none";
    ragModal.style.visibility = "hidden";
    ragModal.style.opacity = "0";
    ragModal.style.pointerEvents = "none";
  }

  const ragQuestionModal = document.getElementById("rag-question-modal");
  if (ragQuestionModal) {
    ragQuestionModal.style.display = "none";
    ragQuestionModal.style.visibility = "hidden";
    ragQuestionModal.style.opacity = "0";
    ragQuestionModal.style.pointerEvents = "none";
  }

  // Hide all modals
  const modals = document.querySelectorAll(".modal");
  modals.forEach((modal) => {
    modal.style.display = "none";
    modal.style.visibility = "hidden";
    modal.style.opacity = "0";
    modal.style.pointerEvents = "none";
  });

  console.log("🔒 ALL RAG MODALS FORCE HIDDEN!");
}

// Force hide immediately
forceHideRAGModals();

// Also hide on DOM ready
document.addEventListener("DOMContentLoaded", forceHideRAGModals);

// And hide on window load
window.addEventListener("load", forceHideRAGModals);
