import React, { useState, useRef, useEffect } from "react";
import {
  Box,
  Typography,
  Button,
  TextField,
  Paper,
  Grid,
  Chip,
  Divider,
  Alert,
  LinearProgress,
} from "@mui/material";
import { GameStateManager } from "./GameStateManager";

const StoryPanel = ({ gameState, onAction, onGameStateUpdate }) => {
  const [userInput, setUserInput] = useState("");
  const [gameManager] = useState(() => new GameStateManager());
  const [currentScene, setCurrentScene] = useState(
    gameManager.getCurrentScene()
  );
  const [showLevelUp, setShowLevelUp] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [currentScene]);

  // Seçim sonuçlarını belirle
  const getChoiceResult = (choice) => {
    const results = {
      // Fantasy seçimleri
      explore_forest:
        "Ormanı keşfetmeye başladın. Garip işaretler ve izler var...",
      search_for_sounds: "Yakındaki sesleri aramaya başladın...",
      find_safe_place: "Güvenli bir yer aramaya başladın...",
      immediate_escape: "Hemen kaçmaya başladın...",
      dragon_encounter: "Ejderha sesini takip etmeye başladın...",
      examine_markers: "İşaretleri incelemeye başladın...",
      search_secret_passage: "Gizli geçit aramaya başladın...",
      return_to_start: "Geri dönmeye başladın...",
      help_dragon: "Ejderhaya yardım etmeye karar verdin...",
      attack_dragon: "Ejderhaya saldırmaya hazırlanıyorsun...",
      escape_from_dragon: "Ejderhadan kaçmaya başladın...",
      examine_dragon: "Ejderhayı dikkatlice inceliyorsun...",
      follow_map: "Haritayı takip etmeye başladın...",
      ignore_map: "Haritayı görmezden gelmeye karar verdin...",
      study_markers_deeper: "İşaretleri daha detaylı incelemeye başladın...",
      enter_cave: "Mağaraya girmeye karar verdin...",
      avoid_cave: "Mağaradan uzak durmaya karar verdin...",
      examine_cave_entrance: "Mağara girişini incelemeye başladın...",
      cross_river: "Nehri geçmeye çalışıyorsun...",
      follow_river: "Nehri takip etmeye başladın...",
      hide_near_river: "Nehir kenarında saklanmaya başladın...",
      enter_temple: "Tapınağa girmeye karar verdin...",
      avoid_temple: "Tapınaktan uzak durmaya karar verdin...",
      examine_temple_outside: "Tapınağı dışarıdan incelemeye başladın...",
      fight_wolves: "Kurtlarla savaşa girdin!",
      run_from_wolves: "Kurtlardan kaçmaya başladın...",
      try_to_calm_wolves: "Kurtları sakinleştirmeye çalışıyorsun...",
      wait_in_tree: "Ağaçta beklemeye karar verdin...",
      climb_higher: "Daha yükseğe tırmanmaya başladın...",
      jump_to_another_tree: "Başka ağaca atlamaya hazırlanıyorsun...",
      offer_food: "Kurtlara yiyecek sunmaya karar verdin...",
      speak_to_wolves: "Kurtlarla konuşmaya karar verdin...",
      leave_peacefully: "Barışçıl bir şekilde ayrılmaya karar verdin...",
      explore_temple_deeper: "Tapınağı daha derin keşfetmeye karar verdin...",
      search_for_treasure: "Hazine aramaya karar verdin...",
      leave_temple: "Tapınaktan çıkmaya karar verdin...",
      climb_mountain: "Dağa tırmanmaya başladın...",
      go_around_mountain: "Dağın etrafından dolaşmaya karar verdin...",
      rest_near_mountain: "Dağ yakınında dinlenmeye karar verdin...",
      read_inscriptions: "Yazıları okumaya başladın...",
      enter_temple_after_study:
        "İncelemeden sonra tapınağa girmeye karar verdin...",
      leave_temple_area: "Tapınak bölgesinden ayrılmaya karar verdin...",
      swim_across: "Yüzerek geçmeye çalışıyorsun...",
      find_bridge: "Köprü aramaya başladın...",
      build_raft: "Sal yapmaya başladın...",
      enter_village: "Köye girmeye karar verdin...",
      avoid_village: "Köyden uzak durmaya karar verdin...",
      observe_village: "Köyü uzaktan gözlemlemeye başladın...",
      continue_hiding: "Saklanmaya devam etmeye karar verdin...",
      leave_hiding_spot: "Saklanma yerinden çıkmaya karar verdin...",
      explore_river_area: "Nehir bölgesini keşfetmeye başladın...",
      accept_dragon_quest: "Ejderhanın görevini kabul ettin...",
      ask_dragon_questions: "Ejderhaya sorular sormaya başladın...",
      refuse_dragon_quest: "Ejderhanın görevini reddettin...",
      charge_dragon: "Ejderhaya doğru koşmaya başladın...",
      use_ranged_attack: "Uzaktan saldırmaya hazırlanıyorsun...",
      retreat_from_dragon: "Saldırıdan vazgeçip kaçmaya karar verdin...",
      run_faster: "Daha hızlı koşmaya başladın...",
      hide_from_dragon: "Ejderhadan saklanmaya çalışıyorsun...",
      find_help: "Yardım aramaya başladın...",
      approach_dragon_carefully: "Dikkatlice yaklaşmaya başladın...",
      communicate_with_dragon: "Ejderhayla iletişim kurmaya çalışıyorsun...",
      leave_dragon_alone: "Ejderhayı rahat bırakmaya karar verdin...",
      enter_treasure_room: "Hazine odasına girmeye karar verdin...",
      examine_room_from_outside: "Odayı dışarıdan incelemeye başladın...",
      avoid_treasure_room: "Hazine odasından uzak durmaya karar verdin...",
      explore_new_area: "Yeni bölgeyi keşfetmeye başladın...",
      rest_in_new_area: "Yeni bölgede dinlenmeye karar verdin...",
      follow_hidden_message: "Gizli mesajı takip etmeye başladın...",
      ignore_hidden_message: "Gizli mesajı görmezden gelmeye karar verdin...",
      share_hidden_message:
        "Gizli mesajı başkalarıyla paylaşmaya karar verdin...",
      explore_cave_deeper: "Mağarayı daha derin keşfetmeye karar verdin...",
      search_cave_for_items: "Mağarada eşya aramaya başladın...",
      leave_cave: "Mağaradan çıkmaya karar verdin...",
      enter_cave_after_study:
        "İncelemeden sonra mağaraya girmeye karar verdin...",
      mark_cave_location: "Mağara konumunu işaretlemeye karar verdin...",
      avoid_cave_after_study:
        "İncelemeden sonra mağaradan uzak durmaya karar verdin...",

      // Warhammer 40K seçimleri
      upper_levels: "Yukarı seviyelere çıkmaya başladın...",
      lower_tunnels: "Aşağı tünellere inmeye başladın...",
      escape_with_civilians: "Sivillerle birlikte kaçmaya başladın...",
      officer_meeting: "Subayla konuşmaya başladın...",
      escape_with_crowd: "Kalabalığa karışıp kaçmaya başladın...",
      weapon_depot: "Silah deposuna gitmeye karar verdin...",
      hospital_help: "Hastaneye gitmeye karar verdin...",
      command_center: "Komuta merkezine gitmeye karar verdin...",
      assess_situation: "Durumu değerlendirmeye başladın...",
      get_weapon_from_officer: "Subaydan silah almaya çalışıyorsun...",
      get_info_from_officer: "Subaydan bilgi almaya çalışıyorsun...",

      // Cyberpunk seçimleri
      listen_to_ai: "AI asistanı dinlemeye başladın...",
      explore_environment: "Çevreyi keşfetmeye başladın...",
      find_hackers: "Hackers'ları aramaya başladın...",
      go_to_corporate: "Şirket binasına gitmeye karar verdin...",
      trust_ai: "AI'ya güvenmeye karar verdin...",
      suspect_ai: "AI'yı şüpheli bulmaya başladın...",
      ask_for_more_info: "Daha fazla bilgi istemeye başladın...",
      disable_ai: "AI'yı devre dışı bırakmaya çalışıyorsun...",

      // Savaş sonuçları
      attack_wolves: "Kurtlara saldırmaya başladın...",
      defend_against_wolves: "Savunma pozisyonu almaya başladın...",
      fight_bravely: "Bravurla savaşmaya başladın...",
      retreat_from_enemies: "Savaştan vazgeçip kaçmaya karar verdin...",

      // Kurt etkileşimleri
      offer_food_to_wolves: "Kurtlara yiyecek sunmaya başladın...",
      give_more_food: "Daha fazla yiyecek vermeye karar verdin...",
      speak_to_wolves: "Kurtlarla konuşmaya çalışıyorsun...",

      // Tapınak keşifleri
      explore_temple_deeper: "Tapınağı daha derin keşfetmeye karar verdin...",
      search_for_treasure: "Hazine aramaya karar verdin...",
      enter_treasure_room: "Hazine odasına girmeye karar verdin...",
      search_treasure_deeper: "Daha derine hazine aramaya karar verdin...",
      examine_room_from_outside: "Odayı dışarıdan incelemeye başladın...",
      avoid_treasure_room: "Hazine odasından uzak durmaya karar verdin...",

      // Köy etkileşimleri
      explore_village: "Köyü keşfetmeye başladın...",
      find_soldiers: "Askerleri aramaya başladın...",
      help_soldiers: "Askerlere yardım etmeye karar verdin...",
      avoid_soldiers: "Askerlerden uzak durmaya karar verdin...",
      fight_enemies: "Düşmanlarla savaşmaya karar verdin...",

      // Hastane etkileşimleri
      help_injured: "Yaralılara yardım etmeye karar verdin...",
      avoid_hospital: "Hastanadan uzak durmaya karar verdin...",
      treat_wounds: "Yaraları tedavi etmeye başladın...",

      // Komuta merkezi etkileşimleri
      assess_situation: "Durumu değerlendirmeye başladın...",
      get_weapon_from_officer: "Subaydan silah almaya çalışıyorsun...",
      get_info_from_officer: "Subaydan bilgi almaya çalışıyorsun...",
      accept_corruption: "Koruma kabul etmeye karar verdin...",
      investigate_clues: "İnceleme yapmaya başladın...",

      // AI etkileşimleri
      trust_ai: "AI'ya güvenmeye karar verdin...",
      suspect_ai: "AI'yı şüpheli bulmaya başladın...",
      ask_for_more_info: "Daha fazla bilgi istemeye başladın...",
      disable_ai: "AI'yı devre dışı bırakmaya çalışıyorsun...",

      // Son sahneler
      accept_reward: "Ödülü kabul etmeye karar verdin...",
      start_new_adventure: "Yeni maceraya çıkmaya karar verdin...",
      return_home: "Eve dönmeye karar verdin...",
      mourn_losses: "Yas tutmaya başladın...",
      seek_revenge: "İntikam almaya karar verdin...",
      new_beginning: "Yeni başlangıç yapmaya karar verdin...",
      revenge_quest: "İntikam peşinde olmaya karar verdin...",
      forgive_betrayer: "Affetmeye karar verdin...",
      start_fresh: "Temiz sayfa açmaya karar verdin...",
      restart_game: "Yeni oyun başlatmaya karar verdin...",

      // Genel seçimler
      continue_journey: "Yolculuğuna devam etmeye karar verdin...",
      return_to_start: "Başlangıç noktasına dönmeye karar verdin...",
      rest_after_fight: "Savaştan sonra dinlenmeye karar verdin...",
      rest_after_defense: "Savunmadan sonra dinlenmeye karar verdin...",
      continue_journey_after_fight:
        "Savaştan sonra devam etmeye karar verdin...",
      continue_journey_after_defense:
        "Savunmadan sonra devam etmeye karar verdin...",
      continue_journey_after_rest:
        "Dinlendikten sonra devam etmeye karar verdin...",
      continue_hiding: "Saklanmaya devam etmeye karar verdin...",
      leave_hiding_spot: "Saklanma yerinden çıkmaya karar verdin...",
      explore_river_area: "Nehir bölgesini keşfetmeye başladın...",
      enter_cave: "Mağaraya girmeye karar verdin...",
      avoid_cave: "Mağaradan uzak durmaya karar verdin...",
      leave_cave: "Mağaradan çıkmaya karar verdin...",
      mark_cave_location: "Mağara konumunu işaretlemeye karar verdin...",
      avoid_cave_after_study:
        "İncelemeden sonra mağaradan uzak durmaya karar verdin...",
      enter_cave_after_study:
        "İncelemeden sonra mağaraya girmeye karar verdin...",
      search_for_items: "Eşya aramaya başladın...",
      explore_cave_deeper: "Mağarayı daha derin keşfetmeye karar verdin...",
      search_cave_for_items: "Mağarada eşya aramaya başladın...",
      enter_temple_after_study:
        "İncelemeden sonra tapınağa girmeye karar verdin...",
      leave_temple_area: "Tapınak bölgesinden ayrılmaya karar verdin...",
      read_inscriptions: "Yazıları okumaya başladın...",
      climb_mountain: "Dağa tırmanmaya başladın...",
      go_around_mountain: "Dağın etrafından dolaşmaya karar verdin...",
      rest_near_mountain: "Dağ yakınında dinlenmeye karar verdin...",
      swim_across: "Yüzerek geçmeye çalışıyorsun...",
      find_bridge: "Köprü aramaya başladın...",
      build_raft: "Sal yapmaya başladın...",
      enter_village: "Köye girmeye karar verdin...",
      avoid_village: "Köyden uzak durmaya karar verdin...",
      observe_village: "Köyü uzaktan gözlemlemeye başladın...",
      explore_village: "Köyü keşfetmeye başladın...",
      find_soldiers: "Askerleri aramaya başladın...",
      help_soldiers: "Askerlere yardım etmeye karar verdin...",
      avoid_soldiers: "Askerlerden uzak durmaya karar verdin...",
      fight_enemies: "Düşmanlarla savaşmaya karar verdin...",
      retreat_from_enemies: "Savaştan vazgeçip kaçmaya karar verdin...",
      help_injured: "Yaralılara yardım etmeye karar verdin...",
      avoid_hospital: "Hastanadan uzak durmaya karar verdin...",
      treat_wounds: "Yaraları tedavi etmeye başladın...",
      command_center: "Komuta merkezine gitmeye karar verdin...",
      assess_situation: "Durumu değerlendirmeye başladın...",
      get_weapon_from_officer: "Subaydan silah almaya çalışıyorsun...",
      get_info_from_officer: "Subaydan bilgi almaya çalışıyorsun...",
      accept_corruption: "Koruma kabul etmeye karar verdin...",
      investigate_clues: "İnceleme yapmaya başladın...",
      trust_ai: "AI'ya güvenmeye karar verdin...",
      suspect_ai: "AI'yı şüpheli bulmaya başladın...",
      ask_for_more_info: "Daha fazla bilgi istemeye başladın...",
      disable_ai: "AI'yı devre dışı bırakmaya çalışıyorsun...",
      accept_reward: "Ödülü kabul etmeye karar verdin...",
      start_new_adventure: "Yeni maceraya çıkmaya karar verdin...",
      return_home: "Eve dönmeye karar verdin...",
      mourn_losses: "Yas tutmaya başladın...",
      seek_revenge: "İntikam almaya karar verdin...",
      new_beginning: "Yeni başlangıç yapmaya karar verdin...",
      revenge_quest: "İntikam peşinde olmaya karar verdin...",
      forgive_betrayer: "Affetmeye karar verdin...",
      start_fresh: "Temiz sayfa açmaya karar verdin...",
      restart_game: "Yeni oyun başlatmaya karar verdin...",
    };
    return results[choice.id] || "Seçimini yaptın...";
  };

  // Zar atma fonksiyonu
  const rollDice = (diceType, target, skill) => {
    const max = parseInt(diceType.replace("d", ""));
    const roll = Math.floor(Math.random() * max) + 1;
    const success = roll >= target;

    return {
      roll: roll,
      target: target,
      success: success,
      skill: skill,
    };
  };

  // Savaş sistemi
  const handleCombat = (enemy, skillUsage) => {
    const playerClass = character.class?.toLowerCase();
    const availableSkills = skillUsage[playerClass] || ["Basic Attack"];

    return {
      enemy: enemy,
      availableSkills: availableSkills,
      playerHealth: character.health,
      enemyHealth: enemy.hp,
    };
  };

  // Oyuncu seçimi yapıldığında
  const handleChoice = (choiceId) => {
    const result = gameManager.makeChoice(choiceId);

    if (result) {
      // Zar atma kontrolü
      if (result.choice.diceRoll) {
        const diceResult = rollDice(
          result.choice.diceRoll.type,
          result.choice.diceRoll.target,
          result.choice.diceRoll.skill
        );

        console.log(
          `Zar atma: ${diceResult.roll}/${diceResult.target} (${
            diceResult.skill
          }) - ${diceResult.success ? "Başarılı" : "Başarısız"}`
        );
      }

      // Savaş kontrolü
      if (result.choice.combat && result.scene.enemies) {
        const combatData = handleCombat(
          result.scene.enemies[0],
          result.choice.skill_usage
        );
        console.log("Savaş başladı:", combatData);
      }

      // Seviye atlama kontrolü
      const levelUp = gameManager.checkLevelUp();
      if (levelUp) {
        setShowLevelUp(true);
        setTimeout(() => setShowLevelUp(false), 5000);
      }

      // Yeni sahneyi göster
      setCurrentScene(result.scene);

      // Oyun durumunu güncelle
      if (onGameStateUpdate) {
        onGameStateUpdate(result.gameState);
      }

      // Seçim sonucunu göster
      const choiceResult = getChoiceResult(result.choice);
      if (choiceResult) {
        // Sonucu mesaj olarak ekle
        const newMessage = {
          type: "result",
          content: choiceResult,
          timestamp: Date.now(),
        };

        if (onAction) {
          onAction("choice_result", newMessage);
        }
      }
    }
  };

  // Özel aksiyon
  const handleCustomAction = () => {
    if (userInput.trim()) {
      // Özel aksiyonları işle
      const customResult = processCustomAction(userInput);

      if (onAction) {
        onAction("custom", { content: customResult, input: userInput });
      }

      setUserInput("");
    }
  };

  // Özel aksiyonları işle
  const processCustomAction = (action) => {
    const actionLower = action.toLowerCase();

    if (actionLower.includes("savaş") || actionLower.includes("fight")) {
      return "Savaş pozisyonu aldın!";
    } else if (actionLower.includes("kaç") || actionLower.includes("escape")) {
      return "Kaçmaya çalışıyorsun...";
    } else if (
      actionLower.includes("incele") ||
      actionLower.includes("investigate")
    ) {
      return "Çevreyi dikkatlice inceliyorsun...";
    } else if (actionLower.includes("konuş") || actionLower.includes("talk")) {
      return "Konuşmaya çalışıyorsun...";
    } else {
      return `"${action}" aksiyonunu gerçekleştiriyorsun...`;
    }
  };

  return (
    <Box sx={{ display: "flex", flexDirection: "column", height: "100%" }}>
      {/* Story Display Area */}
      <Box
        sx={{
          flexGrow: 1,
          overflow: "auto",
          p: 2,
          background: "linear-gradient(135deg, #263238 0%, #37474f 100%)",
        }}
      >
        <Typography
          variant="h5"
          sx={{ color: "#ffc107", mb: 2, textAlign: "center" }}
        >
          📜 {currentScene?.title || "Hikaye"}
        </Typography>

        {/* Seviye Atlama Bildirimi */}
        {showLevelUp && (
          <Alert
            severity="success"
            sx={{ mb: 2, backgroundColor: "rgba(76, 175, 80, 0.2)" }}
          >
            🎉 Seviye Atladın! Yeni yetenekler kazandın!
          </Alert>
        )}

        {/* Mevcut Sahne */}
        {currentScene && (
          <Paper
            elevation={3}
            sx={{
              p: 3,
              mb: 3,
              backgroundColor: "rgba(255,193,7,0.1)",
              border: "1px solid #ffc107",
              borderRadius: 2,
            }}
          >
            <Typography
              variant="body1"
              sx={{
                color: "white",
                lineHeight: 1.8,
                fontFamily: '"Times New Roman", serif',
                fontSize: "1.1rem",
              }}
            >
              {currentScene.description}
            </Typography>
          </Paper>
        )}

        {/* Seçenekler */}
        {currentScene?.choices && currentScene.choices.length > 0 && (
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" sx={{ color: "#4caf50", mb: 2 }}>
              ⚡ Seçeneklerin:
            </Typography>
            <Grid container spacing={2}>
              {currentScene.choices.map((choice, index) => (
                <Grid item xs={12} sm={6} key={choice.id}>
                  <Button
                    fullWidth
                    variant="outlined"
                    onClick={() => handleChoice(choice.id)}
                    sx={{
                      borderColor: "#4caf50",
                      color: "#4caf50",
                      py: 2,
                      fontSize: "1rem",
                      fontWeight: "medium",
                      borderRadius: 2,
                      textTransform: "none",
                      "&:hover": {
                        backgroundColor: "#4caf50",
                        color: "white",
                        transform: "scale(1.02)",
                      },
                      transition: "all 0.3s ease",
                    }}
                  >
                    {choice.text}
                  </Button>
                </Grid>
              ))}
            </Grid>
          </Box>
        )}

        {/* Oyun Durumu Bilgisi */}
        <Paper
          elevation={2}
          sx={{
            p: 2,
            backgroundColor: "rgba(76,175,80,0.1)",
            border: "1px solid #4caf50",
          }}
        >
          <Typography variant="h6" sx={{ color: "#4caf50", mb: 1 }}>
            📊 Oyun Durumu
          </Typography>
          <Box sx={{ display: "flex", gap: 2, mb: 1 }}>
            <Typography variant="body2" sx={{ color: "white" }}>
              Seviye: {gameManager.getGameState().player.level}
            </Typography>
            <Typography variant="body2" sx={{ color: "white" }}>
              XP: {gameManager.getGameState().player.experience}
            </Typography>
            <Typography variant="body2" sx={{ color: "white" }}>
              Karma: {gameManager.getGameState().player.karma}
            </Typography>
          </Box>
          <LinearProgress
            variant="determinate"
            value={
              (gameManager.getGameState().player.experience /
                (gameManager.getGameState().player.level * 100)) *
              100
            }
            sx={{
              height: 6,
              borderRadius: 3,
              backgroundColor: "rgba(255,255,255,0.1)",
              "& .MuiLinearProgress-bar": {
                backgroundColor: "#4caf50",
              },
            }}
          />
        </Paper>

        <div ref={messagesEndRef} />
      </Box>

      <Divider sx={{ borderColor: "#ffc107" }} />

      {/* Action Buttons */}
      <Box sx={{ p: 2, backgroundColor: "rgba(0,0,0,0.3)" }}>
        <Typography variant="h6" sx={{ color: "#ffc107", mb: 1 }}>
          ⚡ Hızlı Aksiyonlar
        </Typography>
        <Grid container spacing={1} sx={{ mb: 2 }}>
          {[
            { label: "⚔️ Savaş", action: "combat", color: "#f44336" },
            { label: "💬 Konuş", action: "talk", color: "#2196f3" },
            { label: "🔍 İncele", action: "investigate", color: "#ff9800" },
            { label: "🏃 Kaç", action: "flee", color: "#9c27b0" },
            { label: "🎒 Envanter", action: "inventory", color: "#4caf50" },
            { label: "🧙 Büyü", action: "cast_spell", color: "#673ab7" },
          ].map((btn, index) => (
            <Grid item xs={6} sm={4} key={index}>
              <Button
                fullWidth
                variant="outlined"
                onClick={() => onAction && onAction(btn.action)}
                sx={{
                  borderColor: btn.color,
                  color: btn.color,
                  "&:hover": {
                    backgroundColor: btn.color,
                    color: "white",
                  },
                }}
              >
                {btn.label}
              </Button>
            </Grid>
          ))}
        </Grid>

        {/* Custom Action Input */}
        <Box sx={{ display: "flex", gap: 1 }}>
          <TextField
            fullWidth
            placeholder="Özel aksiyon yazın... (örn: 'mağaraya giriyorum')"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleCustomAction()}
            sx={{
              "& .MuiOutlinedInput-root": {
                color: "white",
                "& fieldset": { borderColor: "#666" },
                "&:hover fieldset": { borderColor: "#ffc107" },
                "&.Mui-focused fieldset": { borderColor: "#ffc107" },
              },
            }}
          />
          <Button
            variant="contained"
            onClick={handleCustomAction}
            sx={{ backgroundColor: "#ffc107", color: "black" }}
          >
            Gönder
          </Button>
        </Box>
      </Box>
    </Box>
  );
};

export default StoryPanel;
