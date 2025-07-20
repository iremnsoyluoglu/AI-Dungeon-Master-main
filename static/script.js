// Basit ve hatasız oyun akışı için temel JS

document.addEventListener("DOMContentLoaded", function () {
  const setupArea = document.getElementById("setup-area");
  const startBtn = document.getElementById("start-game-btn");
  const charArea = document.getElementById("character-area");
  const saveCharBtn = document.getElementById("save-char-btn");
  const gameArea = document.getElementById("game-area");
  let playerCount = 1;
  let totalPlayers = 1;
  let selectedCampaign = "";
  let characters = [];
  let charStep = 1;

  startBtn.onclick = function () {
    playerCount = parseInt(document.getElementById("player-count").value) || 1;
    totalPlayers = playerCount;
    selectedCampaign = document.getElementById("campaign-select").value;
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
          if (!data.success) {
            alert("Oyun başlatılamadı: " + data.error);
            return;
          }
          // İlk sahneyi getir
          fetch(`/api/campaign/${selectedCampaign}/step/start`)
            .then((res) => res.json())
            .then((step) => {
              charArea.style.display = "none";
              showGameArea(step.step.description, step.step.choices);
            });
        });
    }
  };

  function showGameArea(description, choices) {
    gameArea.style.display = "block";
    document.getElementById("scene-description").innerText = description;
    const choiceDiv = document.getElementById("choice-buttons");
    choiceDiv.innerHTML = "";
    if (choices && choices.length > 0) {
      choices.forEach((choice) => {
        const btn = document.createElement("button");
        btn.textContent = choice.text;
        btn.onclick = function () {
          fetch(`/api/campaign/${selectedCampaign}/choice/${choice.id}`)
            .then((res) => res.json())
            .then((result) => {
              if (result.success && result.result && result.result.next_scene) {
                fetch(
                  `/api/campaign/${selectedCampaign}/step/${result.result.next_scene}`
                )
                  .then((res) => res.json())
                  .then((step) => {
                    showGameArea(step.step.description, step.step.choices);
                  });
              } else if (
                result.success &&
                result.result &&
                result.result.result
              ) {
                alert(result.result.result);
              } else {
                alert("Bir hata oluştu veya son sahneye ulaşıldı.");
              }
            });
        };
        choiceDiv.appendChild(btn);
      });
    }
  }
});
