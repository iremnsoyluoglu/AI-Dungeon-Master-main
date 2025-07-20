// Basit ve hatasız oyun akışı için güncel JS

document.addEventListener("DOMContentLoaded", function () {
  const setupArea = document.getElementById("setup-area");
  const startBtn = document.getElementById("start-game-btn");
  const charArea = document.getElementById("character-area");
  const saveCharBtn = document.getElementById("save-char-btn");
  const gameArea = document.getElementById("game-area");
  const campaignSelect = document.getElementById("campaign-select");
  let playerCount = 1;
  let totalPlayers = 1;
  let selectedCampaign = "";
  let characters = [];
  let charStep = 1;
  let campaignBackgrounds = {
    dragon_lords: "/static/images/background.jpg",
    // Diğer kampanyalar için de ekleyebilirsin
  };
  let lastBg = "";

  // Kampanya seçiminde hover ile background göster
  campaignSelect.addEventListener("mouseover", function (e) {
    if (e.target.tagName === "OPTION") {
      const val = e.target.value;
      if (campaignBackgrounds[val]) {
        document.body.style.backgroundImage = `url('${campaignBackgrounds[val]}')`;
        document.body.style.backgroundSize = "cover";
        document.body.style.backgroundRepeat = "no-repeat";
        document.body.style.backgroundPosition = "center";
        lastBg = campaignBackgrounds[val];
      }
    }
  });
  campaignSelect.addEventListener("mouseout", function (e) {
    document.body.style.backgroundImage = "";
  });
  campaignSelect.addEventListener("change", function (e) {
    const val = e.target.value;
    if (campaignBackgrounds[val]) {
      document.body.style.backgroundImage = `url('${campaignBackgrounds[val]}')`;
      document.body.style.backgroundSize = "cover";
      document.body.style.backgroundRepeat = "no-repeat";
      document.body.style.backgroundPosition = "center";
      lastBg = campaignBackgrounds[val];
    } else {
      document.body.style.backgroundImage = "";
    }
  });

  startBtn.onclick = function () {
    playerCount = parseInt(document.getElementById("player-count").value) || 1;
    totalPlayers = playerCount;
    selectedCampaign = campaignSelect.value;
    setupArea.style.display = "none";
    charArea.style.display = "block";
    charStep = 1;
    characters = [];
    showCharForm();
  };

  function showCharForm() {
    document.getElementById("char-name").value = "";
    document.getElementById("char-class").value = "warrior";
    document.getElementById(
      "char-progress"
    ).innerText = `Oyuncu ${charStep}/${totalPlayers} karakterini oluşturuyor`;
  }

  saveCharBtn.onclick = function () {
    const name = document.getElementById("char-name").value.trim();
    const charClass = document.getElementById("char-class").value;
    if (!name) {
      alert("Karakter adı girin!");
      return;
    }
    characters.push({ name, class: charClass });
    if (charStep < totalPlayers) {
      charStep++;
      showCharForm();
    } else {
      // Tüm karakterler oluşturuldu, backend'e gönder
      fetch("/api/game/session/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          campaign_id: selectedCampaign,
          players: characters,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          // İlk sahneyi getir
          fetch(`/api/campaign/${selectedCampaign}/step/start`)
            .then((res) => res.json())
            .then((data) => {
              charArea.style.display = "none";
              showGameArea(
                data.step.description,
                data.step.choices,
                data.step.background
              );
            });
        });
    }
  };

  // Genel amaçlı buton oluşturucu
  function useButton(label, onClick) {
    const btn = document.createElement("button");
    btn.textContent = label;
    btn.onclick = onClick;
    btn.className = "game-btn";
    return btn;
  }

  // Envanter alanı ekle
  let inventoryDiv = document.createElement("div");
  inventoryDiv.id = "inventory-area";
  inventoryDiv.style.background = "#181818";
  inventoryDiv.style.color = "#fff";
  inventoryDiv.style.padding = "10px";
  inventoryDiv.style.margin = "10px 0";
  inventoryDiv.style.borderRadius = "8px";
  inventoryDiv.innerHTML = '<b>Envanter:</b><div id="inventory-list"></div>';
  document.querySelector(".container").appendChild(inventoryDiv);

  function updateInventory() {
    const invList = document.getElementById("inventory-list");
    invList.innerHTML = "";
    if (
      !characters[0] ||
      !characters[0].inventory ||
      characters[0].inventory.length === 0
    ) {
      invList.innerHTML = "<i>Envanter boş</i>";
      return;
    }
    characters[0].inventory.forEach((item, idx) => {
      const itemDiv = document.createElement("div");
      itemDiv.style.marginBottom = "4px";
      itemDiv.textContent = `${item.name} (${item.type || "eşya"})`;
      if (item.usable || item.type === "potion") {
        itemDiv.appendChild(
          useButton("Kullan", () => {
            fetch("/api/game/use-item", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ item, index: idx }),
            })
              .then((res) => res.json())
              .then((data) => {
                alert(data.message);
                if (data.character) characters[0] = data.character;
                updateInventory();
              });
          })
        );
      }
      invList.appendChild(itemDiv);
    });
  }

  function showGameArea(description, choices, background, extra = {}) {
    gameArea.style.display = "block";
    document.getElementById("scene-description").innerText = description;
    const choiceDiv = document.getElementById("choice-buttons");
    choiceDiv.innerHTML = "";
    if (background) {
      document.body.style.backgroundImage = `url('${background}')`;
      document.body.style.backgroundSize = "cover";
      document.body.style.backgroundRepeat = "no-repeat";
      document.body.style.backgroundPosition = "center";
      lastBg = background;
    } else if (lastBg) {
      document.body.style.backgroundImage = `url('${lastBg}')`;
    } else {
      document.body.style.backgroundImage = "";
    }
    // Normal seçim butonları
    if (choices && choices.length > 0) {
      choices.forEach((choice) => {
        const btn = useButton(choice.text, function () {
          fetch(
            `/api/campaign/${selectedCampaign}/step/${
              choice.nextSceneId || choice.id
            }`
          )
            .then((res) => res.json())
            .then((data) => {
              // Yeni sahnede ekstra alanlar varsa onları da ilet
              showGameArea(
                data.step.description,
                data.step.choices,
                data.step.background,
                data.step
              );
            });
        });
        choiceDiv.appendChild(btn);
      });
    }
    // Savaş butonları (combat: true ise)
    if (extra && extra.combat) {
      choiceDiv.appendChild(
        useButton("🗡 Saldır", () => {
          fetch("/api/game/battle", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              player: characters[0],
              enemy_name: "Ejderha",
            }),
          })
            .then((res) => res.json())
            .then((data) => {
              alert(data.log.join("\n"));
              // Sonuca göre yeni sahneye geçilebilir
            });
        })
      );
      choiceDiv.appendChild(
        useButton("🛡 Savun", () => {
          alert("Savunma yapıldı!");
        })
      );
      choiceDiv.appendChild(
        useButton("✨ Skill Kullan", () => {
          // Skill popup/menu
          const skillDiv = document.createElement("div");
          skillDiv.style.marginTop = "10px";
          skillDiv.style.background = "#222";
          skillDiv.style.padding = "10px";
          skillDiv.style.borderRadius = "8px";
          skillDiv.style.display = "flex";
          skillDiv.style.flexDirection = "column";
          skillDiv.style.alignItems = "flex-start";
          skillDiv.innerHTML = "<b>Skill Seç:</b>";
          // Sadece açılmış skill'ler
          (characters[0].skills || [])
            .filter((s) => s.unlocked)
            .forEach((skill) => {
              skillDiv.appendChild(
                useButton(
                  skill.name +
                    (skill.name.toLowerCase().includes("ultimate")
                      ? " ❗"
                      : ""),
                  () => {
                    fetch("/api/game/battle", {
                      method: "POST",
                      headers: { "Content-Type": "application/json" },
                      body: JSON.stringify({
                        player: characters[0],
                        enemy_name: "Ejderha",
                        skill_name: skill.name,
                      }),
                    })
                      .then((res) => res.json())
                      .then((data) => {
                        alert(data.log.join("\n"));
                        skillDiv.remove();
                        // Sonuca göre yeni sahneye geçilebilir
                      });
                  }
                )
              );
            });
          choiceDiv.appendChild(skillDiv);
        })
      );
      choiceDiv.appendChild(
        useButton("🏃 Kaç", () => {
          alert("Kaçmaya çalışıyorsun!");
        })
      );
    }
    // Good/Evil seçim butonları (alignment_choice varsa)
    if (extra && extra.alignment_choice) {
      choiceDiv.appendChild(
        useButton("İyi Seçim: Yardım Et / Kurtar", () => {
          // Good path için API veya sahne ilerletme
          alert("İyi yol seçildi!");
        })
      );
      choiceDiv.appendChild(
        useButton("Kötü Seçim: Öldür / Yağmala", () => {
          // Evil path için API veya sahne ilerletme
          alert("Kötü yol seçildi!");
        })
      );
    }
    // NPC etkileşim butonları (npc varsa)
    if (extra && extra.npc) {
      choiceDiv.appendChild(
        useButton("Soru sor (NPC)", () => {
          fetch("/api/game/npc-interact", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              player: characters[0],
              npc: extra.npc,
              choice: "ask",
            }),
          })
            .then((res) => res.json())
            .then((data) => {
              alert(data.message);
            });
        })
      );
      choiceDiv.appendChild(
        useButton("Yardım et (NPC)", () => {
          fetch("/api/game/npc-interact", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              player: characters[0],
              npc: extra.npc,
              choice: "help",
            }),
          })
            .then((res) => res.json())
            .then((data) => {
              alert(data.message);
            });
        })
      );
      choiceDiv.appendChild(
        useButton("Tehdit et (NPC)", () => {
          fetch("/api/game/npc-interact", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              player: characters[0],
              npc: extra.npc,
              choice: "threaten",
            }),
          })
            .then((res) => res.json())
            .then((data) => {
              alert(data.message);
            });
        })
      );
    }
    // Final fight'ta evil_ally ve kötü yol seçildiyse Brakk yardımı göster
    if (
      extra &&
      extra.evil_ally &&
      characters[0] &&
      characters[0].good_evil < 0
    ) {
      const brakkDiv = document.createElement("div");
      brakkDiv.style.background = "#330";
      brakkDiv.style.color = "#ffb347";
      brakkDiv.style.padding = "8px";
      brakkDiv.style.margin = "8px 0";
      brakkDiv.style.borderRadius = "6px";
      brakkDiv.innerHTML =
        "<b>Brakk the Cruel yanında! Final savaşta ekstra saldırı ve destek alıyorsun! 🗡️";
      document.getElementById("choice-buttons").prepend(brakkDiv);
    }
  }

  // Check system status
  fetch("/api/health")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById(
        "status"
      ).textContent = `Status: ${data.status} | Version: ${data.version}`;
    })
    .catch((error) => {
      document.getElementById("status").textContent =
        "Status: Error connecting to server";
    });
});
