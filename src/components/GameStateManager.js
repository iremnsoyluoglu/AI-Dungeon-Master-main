// GameStateManager.js - FRP Hikaye Sistemi

export class GameStateManager {
  constructor() {
    this.gameState = {
      // Oyuncu durumu
      player: {
        health: 100,
        mana: 50,
        experience: 0,
        level: 1,
        inventory: [],
        karma: 0,
        relationships: {},
        location: "start",
        quests: [],
        flags: {}, // Hikaye bayrakları
      },

      // Hikaye durumu
      story: {
        currentScene: "start",
        visitedScenes: [],
        choices: [],
        storyFlags: {},
        npcStates: {},
        worldState: {},
      },

      // Kampanya durumu
      campaign: {
        id: null,
        progress: 0,
        completedQuests: [],
        activeQuests: [],
      },
    };

    this.sceneDatabase = this.initializeSceneDatabase();
  }

  // FRP Hikaye Veritabanı - Her seçim gerçek bir sonuca götürür
  initializeSceneDatabase() {
    return {
      // === EJDERHA AVCISININ YOLU (FANTASY) ===
      start: {
        id: "start",
        title: "Büyülü Ormanın Sırları",
        description: "Büyülü bir ormanda gözlerini açtın. Ağaçlar konuşuyor, yaratıklar her yerde. Sen kimsin ve neden buradasın?",
        backgroundImage: "fantasy_forest.jpg",
        choices: [
          {
            id: "explore_forest",
            text: "Çevreyi keşfet",
            action: "explore",
            target: "explore_forest",
            effects: {
              karma: 5,
              experience: 10,
              storyFlags: { explore_thoroughly: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Perception" },
          },
          {
            id: "search_for_sounds",
            text: "Yakındaki sesleri ara",
            action: "investigate",
            target: "search_for_sounds",
            effects: {
              karma: 0,
              experience: 8,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 10, skill: "Investigation" },
          },
          {
            id: "find_safe_place",
            text: "Güvenli yer ara",
            action: "survive",
            target: "find_safe_place",
            effects: {
              karma: 3,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
            diceRoll: { type: "d20", target: 8, skill: "Survival" },
          },
          {
            id: "immediate_escape",
            text: "Hemen kaç",
            action: "flee",
            target: "immediate_escape",
            effects: {
              karma: -5,
              experience: 3,
              storyFlags: { run_away: true },
            },
            diceRoll: { type: "d20", target: 15, skill: "Athletics" },
          },
        ],
      },

      explore_forest: {
        id: "explore_forest",
        title: "Orman Keşfi",
        description: "Ormanı keşfetmeye başladın. Garip işaretler ve izler var. Bir ejderha sesi duyuyorsun...",
        backgroundImage: "fantasy_forest_exploration.jpg",
        choices: [
          {
            id: "dragon_encounter",
            text: "Ejderha sesini takip et",
            action: "track",
            target: "dragon_encounter",
            effects: {
              karma: 0,
              experience: 15,
              storyFlags: { explore_thoroughly: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Stealth" },
          },
          {
            id: "examine_markers",
            text: "İşaretleri incele",
            action: "investigate",
            target: "examine_markers",
            effects: {
              karma: 5,
              experience: 12,
              storyFlags: { solve_puzzle: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Arcana" },
          },
          {
            id: "search_secret_passage",
            text: "Gizli geçit ara",
            action: "explore",
            target: "search_secret_passage",
            effects: {
              karma: 3,
              experience: 10,
              storyFlags: { explore_ruins: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Investigation" },
          },
          {
            id: "return_to_start",
            text: "Geri dön",
            action: "move",
            target: "start",
            effects: {
              karma: -5,
              experience: 5,
              storyFlags: { avoid_conflict: true },
            },
          },
        ],
      },

      search_for_sounds: {
        id: "search_for_sounds",
        title: "Sesleri Araştırma",
        description: "Sesleri takip ettin. Bir grup kurt seni çevreliyor. Ne yapacaksın?",
        backgroundImage: "fantasy_wolf_pack.jpg",
        choices: [
          {
            id: "fight_wolves",
            text: "Kurtlarla savaş",
            action: "combat",
            target: "wolf_combat",
            effects: {
              karma: -5,
              experience: 20,
              storyFlags: { fight_bravely: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Combat" },
            combat: true,
            skill_usage: {
              warrior: ["Shield Wall", "Sword Strike"],
              mage: ["Fireball", "Ice Bolt"],
              rogue: ["Stealth", "Backstab"],
              priest: ["Heal", "Bless"],
              paladin: ["Kutsal Kalkan", "İyileştirme Dokunuşu"],
              druid: ["Doğa Büyüleri", "Şekil Değiştirme"],
              hunter: ["Çoklu Ok", "Keskin Nişan"],
              warlock: ["Karanlık Büyü", "Demon Çağırma"],
            },
          },
          {
            id: "run_from_wolves",
            text: "Kurtlardan kaç",
            action: "flee",
            target: "escape_wolves",
            effects: {
              karma: -3,
              experience: 8,
              storyFlags: { run_away: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Athletics" },
          },
          {
            id: "try_to_calm_wolves",
            text: "Kurtları sakinleştirmeye çalış",
            action: "persuade",
            target: "calm_wolves",
            effects: {
              karma: 10,
              experience: 15,
              storyFlags: { show_mercy: true },
            },
            diceRoll: { type: "d20", target: 18, skill: "Animal Handling" },
          },
        ],
      },

      find_safe_place: {
        id: "find_safe_place",
        title: "Güvenli Yer Arama",
        description: "Güvenli bir yer aramaya başladın. Eski bir tapınak kalıntısı buldun. İçeri girmek ister misin?",
        backgroundImage: "fantasy_temple_ruins.jpg",
        choices: [
          {
            id: "enter_temple",
            text: "Tapınağa gir",
            action: "explore",
            target: "temple_interior",
            effects: {
              karma: 0,
              experience: 12,
              storyFlags: { explore_ruins: true },
            },
            diceRoll: { type: "d20", target: 10, skill: "Perception" },
          },
          {
            id: "avoid_temple",
            text: "Tapınaktan uzak dur",
            action: "move",
            target: "continue_journey",
            effects: {
              karma: 3,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "examine_temple_outside",
            text: "Tapınağı dışarıdan incele",
            action: "investigate",
            target: "examine_temple_outside",
            effects: {
              karma: 5,
              experience: 8,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Investigation" },
          },
        ],
      },

      immediate_escape: {
        id: "immediate_escape",
        title: "Hızlı Kaçış",
        description: "Hemen kaçmaya başladın. Bir nehir kenarına ulaştın. Ne yapacaksın?",
        backgroundImage: "fantasy_river.jpg",
        choices: [
          {
            id: "cross_river",
            text: "Nehri geç",
            action: "swim",
            target: "river_crossing",
            effects: {
              karma: 0,
              experience: 10,
              storyFlags: { take_risk: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Athletics" },
          },
          {
            id: "follow_river",
            text: "Nehri takip et",
            action: "move",
            target: "river_path",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { explore_thoroughly: true },
            },
          },
          {
            id: "hide_near_river",
            text: "Nehir kenarında saklan",
            action: "hide",
            target: "river_hiding",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Stealth" },
          },
        ],
      },

      dragon_encounter: {
        id: "dragon_encounter",
        title: "Ejderha Karşılaşması",
        description: "Büyük bir ejderha ile karşılaştın! Ama beklenmedik bir şey oluyor - ejderha konuşuyor ve yardım istiyor...",
        backgroundImage: "fantasy_dragon.jpg",
        choices: [
          {
            id: "help_dragon",
            text: "Ejderhaya yardım et",
            action: "help",
            target: "help_dragon",
            effects: {
              karma: 10,
              experience: 20,
              relationship: "friendly",
              storyFlags: { help_enemy: true },
            },
            diceRoll: { type: "d20", target: 15, skill: "Persuasion" },
          },
          {
            id: "attack_dragon",
            text: "Ejderhaya saldır",
            action: "combat",
            target: "attack_dragon",
            effects: {
              karma: -10,
              experience: 25,
              storyFlags: { fight_bravely: true },
            },
            diceRoll: { type: "d20", target: 18, skill: "Combat" },
            combat: true,
            skill_usage: {
              warrior: ["Shield Wall", "Sword Strike"],
              mage: ["Fireball", "Ice Bolt"],
              rogue: ["Stealth", "Backstab"],
              priest: ["Heal", "Bless"],
              paladin: ["Kutsal Kalkan", "İyileştirme Dokunuşu"],
              druid: ["Doğa Büyüleri", "Şekil Değiştirme"],
              hunter: ["Çoklu Ok", "Keskin Nişan"],
              warlock: ["Karanlık Büyü", "Demon Çağırma"],
            },
          },
          {
            id: "escape_from_dragon",
            text: "Kaç",
            action: "flee",
            target: "escape_from_dragon",
            effects: {
              karma: -5,
              experience: 8,
              storyFlags: { run_away: true },
            },
            diceRoll: { type: "d20", target: 13, skill: "Athletics" },
          },
          {
            id: "examine_dragon",
            text: "Ejderhayı incele",
            action: "investigate",
            target: "examine_dragon",
            effects: {
              karma: 0,
              experience: 12,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Insight" },
          },
        ],
        npcs: [
          {
            name: "Koruyucu Ejderha",
            type: "Guardian",
            personality: "Wise",
            motivation: "Protect the forest",
            relationship: "neutral",
            betrayal: false,
            plotTwist: true,
          },
        ],
        plotTwist: true,
      },

      examine_markers: {
        id: "examine_markers",
        title: "İşaretleri İnceleme",
        description: "İşaretleri inceledin. Bunlar eski bir büyücü tarafından bırakılmış. Bir harita buldun. Ne yapacaksın?",
        backgroundImage: "fantasy_ancient_markers.jpg",
        choices: [
          {
            id: "follow_map",
            text: "Haritayı takip et",
            action: "move",
            target: "map_destination",
            effects: {
              karma: 5,
              experience: 15,
              storyFlags: { explore_thoroughly: true },
            },
          },
          {
            id: "ignore_map",
            text: "Haritayı görmezden gel",
            action: "move",
            target: "continue_exploration",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "study_markers_deeper",
            text: "İşaretleri daha detaylı incele",
            action: "investigate",
            target: "deep_marker_study",
            effects: {
              karma: 3,
              experience: 12,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Arcana" },
          },
        ],
      },

      search_secret_passage: {
        id: "search_secret_passage",
        title: "Gizli Geçit Arama",
        description: "Gizli geçit aramaya başladın. Bir mağara girişi buldun. İçeri girmek ister misin?",
        backgroundImage: "fantasy_cave_entrance.jpg",
        choices: [
          {
            id: "enter_cave",
            text: "Mağaraya gir",
            action: "explore",
            target: "cave_interior",
            effects: {
              karma: 0,
              experience: 15,
              storyFlags: { explore_ruins: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Perception" },
          },
          {
            id: "avoid_cave",
            text: "Mağaradan uzak dur",
            action: "move",
            target: "continue_journey",
            effects: {
              karma: 3,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "examine_cave_entrance",
            text: "Mağara girişini incele",
            action: "investigate",
            target: "examine_cave_entrance",
            effects: {
              karma: 5,
              experience: 8,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Investigation" },
          },
        ],
      },

      // === HIVE ŞEHRİNİN SAVUNMASI (WARHAMMER 40K) ===
      hive_start: {
        id: "hive_start",
        title: "Hive Şehrinde Uyanış",
        description: "Hive şehrinin 47. seviyesinde, karanlık bir odada gözlerini açtın. Yukarıdan gelen patlamalar ve çığlıklar... Şehir saldırı altında.",
        backgroundImage: "hive_city.jpg",
        choices: [
          {
            id: "upper_levels",
            text: "Yukarı seviyelere çık ve durumu öğren",
            action: "move",
            target: "upper_levels",
            effects: {
              karma: 5,
              experience: 10,
              storyFlags: { explore_thoroughly: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Athletics" },
          },
          {
            id: "lower_tunnels",
            text: "Aşağı tünellere in ve gizli yollar ara",
            action: "explore",
            target: "lower_tunnels",
            effects: {
              karma: 0,
              experience: 8,
              storyFlags: { explore_ruins: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Stealth" },
          },
          {
            id: "find_soldiers",
            text: "Yakındaki askerleri bul",
            action: "search",
            target: "find_soldiers",
            effects: {
              karma: 3,
              experience: 5,
              storyFlags: { help_others: true },
            },
            diceRoll: { type: "d20", target: 10, skill: "Perception" },
          },
          {
            id: "escape_with_civilians",
            text: "Sivillerle birlikte kaç",
            action: "help",
            target: "escape_with_civilians",
            effects: {
              karma: 10,
              experience: 12,
              storyFlags: { save_others: true },
            },
            diceRoll: { type: "d20", target: 8, skill: "Survival" },
          },
        ],
        items: ["Laser Rifle", "Combat Armor", "Med Kit"],
      },

      upper_levels: {
        id: "upper_levels",
        title: "Üst Seviyeler",
        description: "Üst seviyelere çıktın. Hive'ın 23. seviyesi kaos içinde. İnsanlar panik halinde kaçışıyor. Bir subay seni görüyor ve koşarak geliyor.",
        backgroundImage: "hive_upper_levels.jpg",
        choices: [
          {
            id: "officer_meeting",
            text: "Subayla konuş",
            action: "talk",
            target: "officer_meeting",
            effects: {
              karma: 5,
              experience: 10,
              relationship: "friendly",
              storyFlags: { trust_everyone: true },
            },
          },
          {
            id: "escape_with_crowd",
            text: "Kalabalığa karış ve kaç",
            action: "flee",
            target: "escape_with_crowd",
            effects: {
              karma: -5,
              experience: 5,
              storyFlags: { run_away: true },
            },
            diceRoll: { type: "d20", target: 10, skill: "Stealth" },
          },
          {
            id: "weapon_depot",
            text: "Yakındaki silah deposuna git",
            action: "explore",
            target: "weapon_depot",
            effects: {
              karma: 0,
              experience: 8,
              storyFlags: { explore_thoroughly: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Athletics" },
          },
          {
            id: "hospital_help",
            text: "Hastaneye git ve yaralılara yardım et",
            action: "help",
            target: "hospital_help",
            effects: {
              karma: 10,
              experience: 15,
              storyFlags: { help_others: true },
            },
          },
        ],
        npcs: [
          {
            name: "Teğmen Voss",
            type: "Officer",
            personality: "Suspicious",
            motivation: "Unknown",
            relationship: "neutral",
            betrayal: true,
          },
        ],
        plotTwist: true,
        betrayal: false,
      },

      officer_meeting: {
        id: "officer_meeting",
        title: "Subay Toplantısı",
        description:
          "Subay: 'Teğmen! Sonunda bir subay buldum. Orklar kuzey kapısını yarıyor. Komutan Krell seni arıyor. Hemen komuta merkezine gitmelisin.'",
        backgroundImage: "hive_command_center.jpg",
        choices: [
          {
            id: "command_center",
            text: "Komuta merkezine git",
            action: "move",
            target: "command_center",
            effects: {
              karma: 5,
              experience: 10,
              storyFlags: { trust_everyone: true },
            },
          },
          {
            id: "assess_situation",
            text: "Önce durumu değerlendir",
            action: "investigate",
            target: "assess_situation",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Investigation" },
          },
          {
            id: "get_weapon_from_officer",
            text: "Subaydan silah al",
            action: "negotiate",
            target: "get_weapon_from_officer",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { accept_corruption: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Persuasion" },
          },
          {
            id: "get_info_from_officer",
            text: "Subaydan bilgi al",
            action: "investigate",
            target: "get_info_from_officer",
            effects: {
              karma: 5,
              experience: 8,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Insight" },
          },
        ],
        npcs: [
          {
            name: "Teğmen Voss",
            type: "Officer",
            personality: "Suspicious",
            motivation: "Unknown",
            relationship: "neutral",
            betrayal: true,
          },
        ],
        plotTwist: true,
        betrayal: true,
      },

      // === CYBERPUNK ŞEHRİNİN GİZLİ SIRLARI ===
      cyberpunk_start: {
        id: "cyberpunk_start",
        title: "Neon Şehrinde Uyanış",
        description: "Neon ışıkları altında, mega şirketlerin kontrol ettiği bir şehirde gözlerini açtın. Sibernetik implantların var ve AI asistanın seni uyarıyor: 'Tehlikeli bir durum var.'",
        backgroundImage: "cyberpunk_city.jpg",
        choices: [
          {
            id: "listen_to_ai",
            text: "AI asistanı dinle",
            action: "listen",
            target: "listen_to_ai",
            effects: {
              karma: 5,
              experience: 10,
              storyFlags: { trust_everyone: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Technology" },
          },
          {
            id: "explore_environment",
            text: "Çevreyi keşfet",
            action: "explore",
            target: "explore_environment",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { explore_thoroughly: true },
            },
            diceRoll: { type: "d20", target: 10, skill: "Perception" },
          },
          {
            id: "find_hackers",
            text: "Hackers'ları ara",
            action: "search",
            target: "find_hackers",
            effects: {
              karma: 0,
              experience: 12,
              storyFlags: { help_others: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Hacking" },
          },
          {
            id: "go_to_corporate",
            text: "Şirket binasına git",
            action: "move",
            target: "go_to_corporate",
            effects: {
              karma: -5,
              experience: 5,
              storyFlags: { blind_faith: true },
            },
            diceRoll: { type: "d20", target: 8, skill: "Stealth" },
          },
        ],
        npcs: [
          {
            name: "AI Asistan",
            type: "AI",
            personality: "Helpful",
            motivation: "Help user",
            relationship: "neutral",
            betrayal: true,
          },
        ],
        items: ["Cyber Deck", "Neural Implant", "Energy Pistol"],
      },

      listen_to_ai: {
        id: "listen_to_ai",
        title: "AI Uyarısı",
        description:
          "AI asistan: 'Mega şirketler şehri ele geçirmeye çalışıyor. Sibernetik implantlarınızı kontrol ediyorlar. Hemen harekete geçmelisiniz.'",
        backgroundImage: "cyberpunk_ai_warning.jpg",
        choices: [
          {
            id: "trust_ai",
            text: "AI'ya güven",
            action: "trust",
            target: "trust_ai",
            effects: {
              karma: 5,
              experience: 10,
              relationship: "trust",
              storyFlags: { trust_everyone: true },
            },
          },
          {
            id: "suspect_ai",
            text: "AI'yı şüpheli bul",
            action: "investigate",
            target: "suspect_ai",
            effects: {
              karma: 10,
              experience: 15,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Insight" },
          },
          {
            id: "ask_for_more_info",
            text: "Daha fazla bilgi iste",
            action: "investigate",
            target: "ask_for_more_info",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { explore_thoroughly: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Investigation" },
          },
          {
            id: "disable_ai",
            text: "AI'yı devre dışı bırak",
            action: "hack",
            target: "disable_ai",
            effects: {
              karma: -5,
              experience: 12,
              storyFlags: { blind_faith: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Technology" },
          },
        ],
        npcs: [
          {
            name: "AI Asistan",
            type: "AI",
            personality: "Helpful",
            motivation: "Help user",
            relationship: "neutral",
            betrayal: true,
          },
        ],
        plotTwist: true,
        betrayal: true,
      },

      // === SON SAHNELER ===
      victory_ending: {
        id: "victory_ending",
        title: "Zafer",
        description: "Mücadeleyi kazandın! Sen bir kahraman oldun. Halk seni alkışlıyor ve gelecek parlak görünüyor.",
        backgroundImage: "victory.jpg",
        choices: [
          {
            id: "accept_reward",
            text: "Ödülü kabul et",
            action: "accept",
            target: "accept_reward",
            effects: {
              karma: 15,
              experience: 50,
              item: "Legendary Weapon",
            },
          },
          {
            id: "start_new_adventure",
            text: "Yeni maceraya çık",
            action: "continue",
            target: "start",
            effects: {
              karma: 10,
              experience: 25,
            },
          },
          {
            id: "return_home",
            text: "Eve dön",
            action: "end",
            target: "game_end",
            effects: {
              karma: 5,
              experience: 15,
            },
          },
        ],
        ending: true,
      },

      tragic_ending: {
        id: "tragic_ending",
        title: "Trajik Zafer",
        description: "Zafer kazandın ama büyük bir bedel ödedin. Kayıpların anısı seni takip ediyor.",
        backgroundImage: "tragic.jpg",
        choices: [
          {
            id: "mourn_losses",
            text: "Yas tut",
            action: "mourn",
            target: "mourn_losses",
            effects: {
              karma: 5,
              experience: 20,
            },
          },
          {
            id: "seek_revenge",
            text: "İntikam al",
            action: "revenge",
            target: "seek_revenge",
            effects: {
              karma: -5,
              experience: 15,
            },
          },
          {
            id: "new_beginning",
            text: "Yeni başlangıç yap",
            action: "continue",
            target: "start",
            effects: {
              karma: 0,
              experience: 10,
            },
          },
        ],
        ending: true,
      },

      betrayal_ending: {
        id: "betrayal_ending",
        title: "İhanet",
        description: "Güvendiğin kişinin gerçek yüzünü gördün. İhanet acısı kalbini yakıyor.",
        backgroundImage: "betrayal.jpg",
        choices: [
          {
            id: "revenge_quest",
            text: "İntikam peşinde",
            action: "revenge",
            target: "revenge_quest",
            effects: {
              karma: -10,
              experience: 30,
            },
          },
          {
            id: "forgive_betrayer",
            text: "Affet",
            action: "forgive",
            target: "forgive_betrayer",
            effects: {
              karma: 20,
              experience: 25,
            },
          },
          {
            id: "start_fresh",
            text: "Temiz sayfa aç",
            action: "continue",
            target: "start",
            effects: {
              karma: 5,
              experience: 15,
            },
          },
        ],
        ending: true,
      },

      game_end: {
        id: "game_end",
        title: "Oyun Sonu",
        description: "Yolculuğunu tamamladın! Karakterin gelişti ve yeni deneyimler kazandın.",
        backgroundImage: "game_end.jpg",
        choices: [
          {
            id: "restart_game",
            text: "Yeni oyun başlat",
            action: "restart",
            target: "start",
            effects: {
              storyFlags: { game_restarted: true },
            },
          },
        ],
        ending: true,
      },

      // === EKSİK SAHNELER ===
      wolf_combat: {
        id: "wolf_combat",
        title: "Kurt Savaşı",
        description: "Kurtlarla savaşa girdin! Silahını çektin ve hazırlanıyorsun.",
        backgroundImage: "fantasy_wolf_combat.jpg",
        choices: [
          {
            id: "attack_wolves",
            text: "Kurtlara saldır",
            action: "combat",
            target: "wolf_combat_result",
            effects: {
              karma: -5,
              experience: 25,
              storyFlags: { fight_bravely: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Combat" },
            combat: true,
          },
          {
            id: "defend_against_wolves",
            text: "Savunma pozisyonu al",
            action: "defend",
            target: "wolf_defense_result",
            effects: {
              karma: 0,
              experience: 15,
              storyFlags: { self_preservation: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Defense" },
          },
        ],
        enemies: [
          {
            name: "Kurt Sürüsü",
            type: "Pack",
            hp: 60,
            attack: 14,
            defense: 12,
            specialAbilities: ["Pack Tactics", "Howl"],
            statusEffects: ["Enraged"],
          },
        ],
        combat: true,
      },

      escape_wolves: {
        id: "escape_wolves",
        title: "Kurtlardan Kaçış",
        description: "Kurtlardan kaçmaya başladın. Bir ağaca tırmanmayı başardın. Ne yapacaksın?",
        backgroundImage: "fantasy_tree_climb.jpg",
        choices: [
          {
            id: "wait_in_tree",
            text: "Ağaçta bekle",
            action: "wait",
            target: "wait_in_tree",
            effects: {
              karma: 0,
              experience: 8,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "climb_higher",
            text: "Daha yükseğe tırman",
            action: "climb",
            target: "climb_higher",
            effects: {
              karma: 3,
              experience: 10,
              storyFlags: { explore_thoroughly: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Athletics" },
          },
          {
            id: "jump_to_another_tree",
            text: "Başka ağaca atla",
            action: "jump",
            target: "jump_to_another_tree",
            effects: {
              karma: 0,
              experience: 12,
              storyFlags: { take_risk: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Athletics" },
          },
        ],
      },

      calm_wolves: {
        id: "calm_wolves",
        title: "Kurtları Sakinleştirme",
        description: "Kurtları sakinleştirmeye çalıştın. Kurtlar seni dinliyor gibi görünüyor. Ne yapacaksın?",
        backgroundImage: "fantasy_calm_wolves.jpg",
        choices: [
          {
            id: "offer_food",
            text: "Kurtlara yiyecek ver",
            action: "give",
            target: "offer_food_to_wolves",
            effects: {
              karma: 10,
              experience: 15,
              storyFlags: { show_mercy: true },
            },
          },
          {
            id: "speak_to_wolves",
            text: "Kurtlarla konuş",
            action: "talk",
            target: "speak_to_wolves",
            effects: {
              karma: 5,
              experience: 12,
              storyFlags: { help_others: true },
            },
            diceRoll: { type: "d20", target: 18, skill: "Animal Handling" },
          },
          {
            id: "leave_peacefully",
            text: "Barışçıl bir şekilde ayrıl",
            action: "leave",
            target: "leave_peacefully",
            effects: {
              karma: 8,
              experience: 10,
              storyFlags: { show_mercy: true },
            },
          },
        ],
      },

      temple_interior: {
        id: "temple_interior",
        title: "Tapınak İçi",
        description: "Tapınağın içine girdin. Eski büyülü enerji hissediyorsun. Ne yapacaksın?",
        backgroundImage: "fantasy_temple_interior.jpg",
        choices: [
          {
            id: "explore_temple_deeper",
            text: "Tapınağı daha derin keşfet",
            action: "explore",
            target: "temple_deeper",
            effects: {
              karma: 0,
              experience: 15,
              storyFlags: { explore_ruins: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Perception" },
          },
          {
            id: "search_for_treasure",
            text: "Hazine ara",
            action: "search",
            target: "search_for_treasure",
            effects: {
              karma: -3,
              experience: 12,
              storyFlags: { accept_corruption: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Investigation" },
          },
          {
            id: "leave_temple",
            text: "Tapınaktan çık",
            action: "leave",
            target: "continue_journey",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      continue_journey: {
        id: "continue_journey",
        title: "Yolculuğa Devam",
        description: "Yolculuğuna devam ediyorsun. Önünde bir dağ görünüyor. Ne yapacaksın?",
        backgroundImage: "fantasy_mountain.jpg",
        choices: [
          {
            id: "climb_mountain",
            text: "Dağa tırman",
            action: "climb",
            target: "mountain_climb",
            effects: {
              karma: 5,
              experience: 20,
              storyFlags: { explore_thoroughly: true },
            },
            diceRoll: { type: "d20", target: 15, skill: "Athletics" },
          },
          {
            id: "go_around_mountain",
            text: "Dağın etrafından dolaş",
            action: "move",
            target: "around_mountain",
            effects: {
              karma: 0,
              experience: 10,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "rest_near_mountain",
            text: "Dağ yakınında dinlen",
            action: "rest",
            target: "rest_near_mountain",
            effects: {
              karma: 3,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      examine_temple_outside: {
        id: "examine_temple_outside",
        title: "Tapınağı Dışarıdan İnceleme",
        description: "Tapınağı dışarıdan inceledin. Eski yazılar ve semboller var. Ne yapacaksın?",
        backgroundImage: "fantasy_temple_exterior.jpg",
        choices: [
          {
            id: "read_inscriptions",
            text: "Yazıları oku",
            action: "read",
            target: "read_inscriptions",
            effects: {
              karma: 5,
              experience: 12,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Arcana" },
          },
          {
            id: "enter_temple_after_study",
            text: "İncelemeden sonra tapınağa gir",
            action: "enter",
            target: "temple_interior",
            effects: {
              karma: 3,
              experience: 10,
              storyFlags: { explore_ruins: true },
            },
          },
          {
            id: "leave_temple_area",
            text: "Tapınak bölgesinden ayrıl",
            action: "leave",
            target: "continue_journey",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      river_crossing: {
        id: "river_crossing",
        title: "Nehir Geçişi",
        description: "Nehri geçmeye çalışıyorsun. Su çok hızlı akıyor. Ne yapacaksın?",
        backgroundImage: "fantasy_river_crossing.jpg",
        choices: [
          {
            id: "swim_across",
            text: "Yüzerek geç",
            action: "swim",
            target: "swim_across_river",
            effects: {
              karma: 0,
              experience: 15,
              storyFlags: { take_risk: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Athletics" },
          },
          {
            id: "find_bridge",
            text: "Köprü ara",
            action: "search",
            target: "find_bridge",
            effects: {
              karma: 3,
              experience: 10,
              storyFlags: { explore_thoroughly: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Perception" },
          },
          {
            id: "build_raft",
            text: "Sal yap",
            action: "craft",
            target: "build_raft",
            effects: {
              karma: 5,
              experience: 20,
              storyFlags: { help_others: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Survival" },
          },
        ],
      },

      river_path: {
        id: "river_path",
        title: "Nehir Yolu",
        description: "Nehri takip etmeye başladın. Bir köy görünüyor. Ne yapacaksın?",
        backgroundImage: "fantasy_river_village.jpg",
        choices: [
          {
            id: "enter_village",
            text: "Köye gir",
            action: "enter",
            target: "enter_village",
            effects: {
              karma: 5,
              experience: 10,
              storyFlags: { help_others: true },
            },
          },
          {
            id: "avoid_village",
            text: "Köyden uzak dur",
            action: "avoid",
            target: "avoid_village",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "observe_village",
            text: "Köyü uzaktan gözlemle",
            action: "observe",
            target: "observe_village",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Perception" },
          },
        ],
      },

      river_hiding: {
        id: "river_hiding",
        title: "Nehir Kenarında Saklanma",
        description: "Nehir kenarında saklandın. Tehlike geçti gibi görünüyor. Ne yapacaksın?",
        backgroundImage: "fantasy_river_hiding.jpg",
        choices: [
          {
            id: "continue_hiding",
            text: "Saklanmaya devam et",
            action: "hide",
            target: "continue_hiding",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "leave_hiding_spot",
            text: "Saklanma yerinden çık",
            action: "leave",
            target: "continue_journey",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { explore_thoroughly: true },
            },
          },
          {
            id: "explore_river_area",
            text: "Nehir bölgesini keşfet",
            action: "explore",
            target: "explore_river_area",
            effects: {
              karma: 5,
              experience: 12,
              storyFlags: { explore_thoroughly: true },
            },
            diceRoll: { type: "d20", target: 10, skill: "Perception" },
          },
        ],
      },

      help_dragon: {
        id: "help_dragon",
        title: "Ejderhaya Yardım",
        description: "Ejderhaya yardım etmeye karar verdin. Ejderha sana bir görev veriyor. Ne yapacaksın?",
        backgroundImage: "fantasy_dragon_help.jpg",
        choices: [
          {
            id: "accept_dragon_quest",
            text: "Görevi kabul et",
            action: "accept",
            target: "accept_dragon_quest",
            effects: {
              karma: 15,
              experience: 25,
              storyFlags: { help_others: true },
            },
          },
          {
            id: "ask_dragon_questions",
            text: "Ejderhaya sorular sor",
            action: "ask",
            target: "ask_dragon_questions",
            effects: {
              karma: 5,
              experience: 10,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Insight" },
          },
          {
            id: "refuse_dragon_quest",
            text: "Görevi reddet",
            action: "refuse",
            target: "refuse_dragon_quest",
            effects: {
              karma: -5,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
        npcs: [
          {
            name: "Koruyucu Ejderha",
            type: "Guardian",
            personality: "Wise",
            motivation: "Protect the forest",
            relationship: "ally",
          },
        ],
      },

      attack_dragon: {
        id: "attack_dragon",
        title: "Ejderhaya Saldırı",
        description: "Ejderhaya saldırmaya hazırlanıyorsun. Bu çok tehlikeli bir karar. Ne yapacaksın?",
        backgroundImage: "fantasy_dragon_attack.jpg",
        choices: [
          {
            id: "charge_dragon",
            text: "Ejderhaya doğru koş",
            action: "charge",
            target: "charge_dragon",
            effects: {
              karma: -10,
              experience: 30,
              storyFlags: { fight_bravely: true },
            },
            diceRoll: { type: "d20", target: 20, skill: "Combat" },
            combat: true,
          },
          {
            id: "use_ranged_attack",
            text: "Uzaktan saldır",
            action: "ranged",
            target: "ranged_attack_dragon",
            effects: {
              karma: -5,
              experience: 20,
              storyFlags: { fight_bravely: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Ranged Combat" },
            combat: true,
          },
          {
            id: "retreat_from_dragon",
            text: "Saldırıdan vazgeç ve kaç",
            action: "retreat",
            target: "retreat_from_dragon",
            effects: {
              karma: -3,
              experience: 8,
              storyFlags: { run_away: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Athletics" },
          },
        ],
        enemies: [
          {
            name: "Koruyucu Ejderha",
            type: "Dragon",
            hp: 150,
            attack: 25,
            defense: 20,
            specialAbilities: ["Fire Breath", "Wing Buffet", "Tail Swipe"],
            statusEffects: ["Enraged", "Protective"],
          },
        ],
        combat: true,
      },

      escape_from_dragon: {
        id: "escape_from_dragon",
        title: "Ejderhadan Kaçış",
        description: "Ejderhadan kaçmaya çalışıyorsun. Ejderha seni takip ediyor. Ne yapacaksın?",
        backgroundImage: "fantasy_dragon_escape.jpg",
        choices: [
          {
            id: "run_faster",
            text: "Daha hızlı koş",
            action: "run",
            target: "run_faster_from_dragon",
            effects: {
              karma: -5,
              experience: 10,
              storyFlags: { run_away: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Athletics" },
          },
          {
            id: "hide_from_dragon",
            text: "Ejderhadan saklan",
            action: "hide",
            target: "hide_from_dragon",
            effects: {
              karma: 0,
              experience: 8,
              storyFlags: { self_preservation: true },
            },
            diceRoll: { type: "d20", target: 18, skill: "Stealth" },
          },
          {
            id: "find_help",
            text: "Yardım ara",
            action: "search",
            target: "find_help_against_dragon",
            effects: {
              karma: 5,
              experience: 12,
              storyFlags: { help_others: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Perception" },
          },
        ],
      },

      examine_dragon: {
        id: "examine_dragon",
        title: "Ejderhayı İnceleme",
        description: "Ejderhayı dikkatlice inceliyorsun. Ejderha seni fark etti ama saldırmıyor. Ne yapacaksın?",
        backgroundImage: "fantasy_dragon_examination.jpg",
        choices: [
          {
            id: "approach_dragon_carefully",
            text: "Dikkatlice yaklaş",
            action: "approach",
            target: "approach_dragon_carefully",
            effects: {
              karma: 5,
              experience: 15,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Stealth" },
          },
          {
            id: "communicate_with_dragon",
            text: "Ejderhayla iletişim kur",
            action: "communicate",
            target: "communicate_with_dragon",
            effects: {
              karma: 10,
              experience: 20,
              storyFlags: { help_others: true },
            },
            diceRoll: { type: "d20", target: 18, skill: "Persuasion" },
          },
          {
            id: "leave_dragon_alone",
            text: "Ejderhayı rahat bırak",
            action: "leave",
            target: "leave_dragon_alone",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { show_mercy: true },
            },
          },
        ],
        npcs: [
          {
            name: "Koruyucu Ejderha",
            type: "Guardian",
            personality: "Wise",
            motivation: "Protect the forest",
            relationship: "neutral",
            betrayal: false,
            plotTwist: true,
          },
        ],
      },

      map_destination: {
        id: "map_destination",
        title: "Harita Hedefi",
        description: "Haritayı takip ettin. Bir hazine odasına ulaştın. Ne yapacaksın?",
        backgroundImage: "fantasy_treasure_room.jpg",
        choices: [
          {
            id: "enter_treasure_room",
            text: "Hazine odasına gir",
            action: "enter",
            target: "enter_treasure_room",
            effects: {
              karma: 0,
              experience: 20,
              storyFlags: { explore_ruins: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Perception" },
          },
          {
            id: "examine_room_from_outside",
            text: "Odayı dışarıdan incele",
            action: "examine",
            target: "examine_room_from_outside",
            effects: {
              karma: 5,
              experience: 12,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Investigation" },
          },
          {
            id: "avoid_treasure_room",
            text: "Hazine odasından uzak dur",
            action: "avoid",
            target: "avoid_treasure_room",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      continue_exploration: {
        id: "continue_exploration",
        title: "Keşfe Devam",
        description: "Keşfine devam ediyorsun. Yeni bir bölgeye ulaştın. Ne yapacaksın?",
        backgroundImage: "fantasy_new_area.jpg",
        choices: [
          {
            id: "explore_new_area",
            text: "Yeni bölgeyi keşfet",
            action: "explore",
            target: "explore_new_area",
            effects: {
              karma: 5,
              experience: 15,
              storyFlags: { explore_thoroughly: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Perception" },
          },
          {
            id: "rest_in_new_area",
            text: "Yeni bölgede dinlen",
            action: "rest",
            target: "rest_in_new_area",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      deep_marker_study: {
        id: "deep_marker_study",
        title: "İşaretleri Derinlemesine İnceleme",
        description: "İşaretleri daha detaylı inceledin. Gizli bir mesaj buldun. Ne yapacaksın?",
        backgroundImage: "fantasy_deep_marker_study.jpg",
        choices: [
          {
            id: "follow_hidden_message",
            text: "Gizli mesajı takip et",
            action: "follow",
            target: "follow_hidden_message",
            effects: {
              karma: 5,
              experience: 20,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Investigation" },
          },
          {
            id: "ignore_hidden_message",
            text: "Gizli mesajı görmezden gel",
            action: "ignore",
            target: "ignore_hidden_message",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "share_hidden_message",
            text: "Gizli mesajı başkalarıyla paylaş",
            action: "share",
            target: "share_hidden_message",
            effects: {
              karma: 8,
              experience: 15,
              storyFlags: { help_others: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Persuasion" },
          },
        ],
      },

      cave_interior: {
        id: "cave_interior",
        title: "Mağara İçi",
        description: "Mağaranın içine girdin. Karanlık ve nemli bir yer. Ne yapacaksın?",
        backgroundImage: "fantasy_cave_interior.jpg",
        choices: [
          {
            id: "explore_cave_deeper",
            text: "Mağarayı daha derin keşfet",
            action: "explore",
            target: "explore_cave_deeper",
            effects: {
              karma: 0,
              experience: 18,
              storyFlags: { explore_ruins: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Perception" },
          },
          {
            id: "search_cave_for_items",
            text: "Mağarada eşya ara",
            action: "search",
            target: "search_cave_for_items",
            effects: {
              karma: 3,
              experience: 12,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Investigation" },
          },
          {
            id: "leave_cave",
            text: "Mağaradan çık",
            action: "leave",
            target: "leave_cave",
            effects: {
              karma: 0,
              experience: 8,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      examine_cave_entrance: {
        id: "examine_cave_entrance",
        title: "Mağara Girişini İnceleme",
        description: "Mağara girişini inceledin. Eski işaretler ve izler var. Ne yapacaksın?",
        backgroundImage: "fantasy_cave_entrance_examination.jpg",
        choices: [
          {
            id: "enter_cave_after_study",
            text: "İncelemeden sonra mağaraya gir",
            action: "enter",
            target: "cave_interior",
            effects: {
              karma: 3,
              experience: 12,
              storyFlags: { explore_ruins: true },
            },
          },
          {
            id: "mark_cave_location",
            text: "Mağara konumunu işaretle",
            action: "mark",
            target: "mark_cave_location",
            effects: {
              karma: 5,
              experience: 8,
              storyFlags: { help_others: true },
            },
          },
          {
            id: "avoid_cave_after_study",
            text: "İncelemeden sonra mağaradan uzak dur",
            action: "avoid",
            target: "avoid_cave_after_study",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      wolf_combat_result: {
        id: "wolf_combat_result",
        title: "Kurt Savaşı Sonucu",
        description: "Kurtlarla savaşınızın sonucu belli oldu. Ne yapacaksın?",
        backgroundImage: "fantasy_wolf_combat_result.jpg",
        choices: [
          {
            id: "continue_journey_after_fight",
            text: "Savaştan sonra devam et",
            action: "move",
            target: "continue_journey",
            effects: {
              karma: 0,
              experience: 10,
              storyFlags: { explore_thoroughly: true },
            },
          },
          {
            id: "rest_after_fight",
            text: "Savaştan sonra dinlen",
            action: "rest",
            target: "rest_after_fight",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      wolf_defense_result: {
        id: "wolf_defense_result",
        title: "Kurt Savunması Sonucu",
        description: "Kurtların savunmasına karar verdin. Ne yapacaksın?",
        backgroundImage: "fantasy_wolf_defense_result.jpg",
        choices: [
          {
            id: "continue_journey_after_defense",
            text: "Savunmadan sonra devam et",
            action: "move",
            target: "continue_journey",
            effects: {
              karma: 0,
              experience: 10,
              storyFlags: { explore_thoroughly: true },
            },
          },
          {
            id: "rest_after_defense",
            text: "Savunmadan sonra dinlen",
            action: "rest",
            target: "rest_after_defense",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      rest_after_fight: {
        id: "rest_after_fight",
        title: "Savaştan Sonra Dinlenme",
        description: "Savaştan sonra dinlenmeye başladın. Sağlığınız biraz daha iyileşti.",
        backgroundImage: "fantasy_rest_after_fight.jpg",
        choices: [
          {
            id: "continue_journey_after_rest",
            text: "Dinlendikten sonra devam et",
            action: "move",
            target: "continue_journey",
            effects: {
              karma: 0,
              experience: 10,
              storyFlags: { explore_thoroughly: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      rest_after_defense: {
        id: "rest_after_defense",
        title: "Savunmadan Sonra Dinlenme",
        description: "Savunmadan sonra dinlenmeye başladın. Sağlığınız biraz daha iyileşti.",
        backgroundImage: "fantasy_rest_after_defense.jpg",
        choices: [
          {
            id: "continue_journey_after_rest",
            text: "Dinlendikten sonra devam et",
            action: "move",
            target: "continue_journey",
            effects: {
              karma: 0,
              experience: 10,
              storyFlags: { explore_thoroughly: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      offer_food_to_wolves: {
        id: "offer_food_to_wolves",
        title: "Yiyecek Sunma",
        description: "Kurtlara yiyecek sunmaya karar verdin. Kurtlar seni dinliyor gibi görünüyor.",
        backgroundImage: "fantasy_offer_food_to_wolves.jpg",
        choices: [
          {
            id: "give_more_food",
            text: "Daha fazla yiyecek ver",
            action: "give",
            target: "give_more_food_to_wolves",
            effects: {
              karma: 10,
              experience: 15,
              storyFlags: { show_mercy: true },
            },
          },
          {
            id: "leave_peacefully",
            text: "Barışçıl bir şekilde ayrıl",
            action: "leave",
            target: "leave_peacefully",
            effects: {
              karma: 8,
              experience: 10,
              storyFlags: { show_mercy: true },
            },
          },
          {
            id: "run_from_wolves",
            text: "Kurtlardan kaç",
            action: "flee",
            target: "escape_wolves",
            effects: {
              karma: -3,
              experience: 8,
              storyFlags: { run_away: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Athletics" },
          },
        ],
      },

      give_more_food_to_wolves: {
        id: "give_more_food_to_wolves",
        title: "Daha Fazla Yiyecek Sunma",
        description: "Kurtlara daha fazla yiyecek sunmaya karar verdin. Kurtlar seni dinliyor gibi görünüyor.",
        backgroundImage: "fantasy_give_more_food_to_wolves.jpg",
        choices: [
          {
            id: "give_more_food",
            text: "Daha fazla yiyecek ver",
            action: "give",
            target: "give_more_food_to_wolves",
            effects: {
              karma: 10,
              experience: 15,
              storyFlags: { show_mercy: true },
            },
          },
          {
            id: "leave_peacefully",
            text: "Barışçıl bir şekilde ayrıl",
            action: "leave",
            target: "leave_peacefully",
            effects: {
              karma: 8,
              experience: 10,
              storyFlags: { show_mercy: true },
            },
          },
          {
            id: "run_from_wolves",
            text: "Kurtlardan kaç",
            action: "flee",
            target: "escape_wolves",
            effects: {
              karma: -3,
              experience: 8,
              storyFlags: { run_away: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Athletics" },
          },
        ],
      },

      speak_to_wolves: {
        id: "speak_to_wolves",
        title: "Kurtlarla İletişim",
        description: "Kurtlarla konuşmaya karar verdin. Kurtlar seni dinliyor gibi görünüyor.",
        backgroundImage: "fantasy_speak_to_wolves.jpg",
        choices: [
          {
            id: "offer_food",
            text: "Yiyecek ver",
            action: "give",
            target: "offer_food_to_wolves",
            effects: {
              karma: 10,
              experience: 15,
              storyFlags: { show_mercy: true },
            },
          },
          {
            id: "leave_peacefully",
            text: "Barışçıl bir şekilde ayrıl",
            action: "leave",
            target: "leave_peacefully",
            effects: {
              karma: 8,
              experience: 10,
              storyFlags: { show_mercy: true },
            },
          },
          {
            id: "run_from_wolves",
            text: "Kurtlardan kaç",
            action: "flee",
            target: "escape_wolves",
            effects: {
              karma: -3,
              experience: 8,
              storyFlags: { run_away: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Athletics" },
          },
        ],
      },

      leave_peacefully: {
        id: "leave_peacefully",
        title: "Barışçıl Ayrılış",
        description: "Kurtlardan barışçıl bir şekilde ayrıldın. Kurtlar seni dinliyor gibi görünüyor.",
        backgroundImage: "fantasy_leave_peacefully.jpg",
        choices: [
          {
            id: "continue_journey",
            text: "Devam et",
            action: "move",
            target: "continue_journey",
            effects: {
              karma: 0,
              experience: 10,
              storyFlags: { explore_thoroughly: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      temple_deeper: {
        id: "temple_deeper",
        title: "Tapınağı Daha Derine Keşfi",
        description: "Tapınağı daha derin keşfetmeye karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_temple_deeper.jpg",
        choices: [
          {
            id: "search_for_treasure",
            text: "Hazine ara",
            action: "search",
            target: "search_for_treasure",
            effects: {
              karma: -3,
              experience: 12,
              storyFlags: { accept_corruption: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Investigation" },
          },
          {
            id: "leave_temple",
            text: "Tapınaktan çık",
            action: "leave",
            target: "continue_journey",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "explore_temple_deeper",
            text: "Daha derine keşfet",
            action: "explore",
            target: "temple_deeper",
            effects: {
              karma: 0,
              experience: 15,
              storyFlags: { explore_ruins: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Perception" },
          },
        ],
      },

      search_for_treasure: {
        id: "search_for_treasure",
        title: "Hazine Arama",
        description: "Hazine aramaya karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_treasure_hunt.jpg",
        choices: [
          {
            id: "enter_treasure_room",
            text: "Hazine odasına gir",
            action: "enter",
            target: "enter_treasure_room",
            effects: {
              karma: 0,
              experience: 20,
              storyFlags: { explore_ruins: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Perception" },
          },
          {
            id: "avoid_treasure_room",
            text: "Hazine odasından uzak dur",
            action: "avoid",
            target: "avoid_treasure_room",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "leave_temple",
            text: "Tapınaktan çık",
            action: "leave",
            target: "continue_journey",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      enter_treasure_room: {
        id: "enter_treasure_room",
        title: "Hazine Odasına Giriş",
        description: "Hazine odasına girdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_treasure_room_entrance.jpg",
        choices: [
          {
            id: "search_treasure_deeper",
            text: "Daha derine keşfet",
            action: "explore",
            target: "search_treasure_deeper",
            effects: {
              karma: 0,
              experience: 15,
              storyFlags: { explore_ruins: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Perception" },
          },
          {
            id: "leave_treasure_room",
            text: "Hazine odasından çık",
            action: "leave",
            target: "continue_journey",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "search_for_items",
            text: "Eşya ara",
            action: "search",
            target: "search_for_items",
            effects: {
              karma: 3,
              experience: 12,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Investigation" },
          },
        ],
      },

      search_treasure_deeper: {
        id: "search_treasure_deeper",
        title: "Daha Derine Hazine Arama",
        description: "Hazine aramaya daha derine karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_treasure_hunt_deeper.jpg",
        choices: [
          {
            id: "enter_treasure_room",
            text: "Hazine odasına gir",
            action: "enter",
            target: "enter_treasure_room",
            effects: {
              karma: 0,
              experience: 20,
              storyFlags: { explore_ruins: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Perception" },
          },
          {
            id: "avoid_treasure_room",
            text: "Hazine odasından uzak dur",
            action: "avoid",
            target: "avoid_treasure_room",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "leave_temple",
            text: "Tapınaktan çık",
            action: "leave",
            target: "continue_journey",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      examine_room_from_outside: {
        id: "examine_room_from_outside",
        title: "Odayı Dışarıdan İnceleme",
        description: "Odayı dışarıdan inceledin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_treasure_room_exterior_examination.jpg",
        choices: [
          {
            id: "enter_treasure_room",
            text: "İncelemeden sonra hazine odasına gir",
            action: "enter",
            target: "enter_treasure_room",
            effects: {
              karma: 3,
              experience: 10,
              storyFlags: { explore_ruins: true },
            },
          },
          {
            id: "avoid_treasure_room",
            text: "İncelemeden sonra hazine odasından uzak dur",
            action: "avoid",
            target: "avoid_treasure_room",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      avoid_treasure_room: {
        id: "avoid_treasure_room",
        title: "Hazine Odasından Uzak Durma",
        description: "Hazine odasından uzak durmaya karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_avoid_treasure_room.jpg",
        choices: [
          {
            id: "continue_journey",
            text: "Devam et",
            action: "move",
            target: "continue_journey",
            effects: {
              karma: 0,
              experience: 10,
              storyFlags: { explore_thoroughly: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      enter_village: {
        id: "enter_village",
        title: "Köye Giriş",
        description: "Köye girdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_village_entrance.jpg",
        choices: [
          {
            id: "explore_village",
            text: "Köyi keşfet",
            action: "explore",
            target: "explore_village",
            effects: {
              karma: 5,
              experience: 10,
              storyFlags: { help_others: true },
            },
          },
          {
            id: "avoid_village",
            text: "Köyden uzak dur",
            action: "avoid",
            target: "avoid_village",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "observe_village",
            text: "Köyü uzaktan gözlemle",
            action: "observe",
            target: "observe_village",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Perception" },
          },
        ],
      },

      explore_village: {
        id: "explore_village",
        title: "Köyi Keşfi",
        description: "Köyi keşfetmeye karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_village_exploration.jpg",
        choices: [
          {
            id: "find_soldiers",
            text: "Yakındaki askerleri bul",
            action: "search",
            target: "find_soldiers",
            effects: {
              karma: 3,
              experience: 5,
              storyFlags: { help_others: true },
            },
            diceRoll: { type: "d20", target: 10, skill: "Perception" },
          },
          {
            id: "avoid_village",
            text: "Köyden uzak dur",
            action: "avoid",
            target: "avoid_village",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "observe_village",
            text: "Köyü uzaktan gözlemle",
            action: "observe",
            target: "observe_village",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Perception" },
          },
        ],
      },

      avoid_village: {
        id: "avoid_village",
        title: "Köyden Uzak Durma",
        description: "Köyden uzak durmaya karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_avoid_village.jpg",
        choices: [
          {
            id: "continue_journey",
            text: "Devam et",
            action: "move",
            target: "continue_journey",
            effects: {
              karma: 0,
              experience: 10,
              storyFlags: { explore_thoroughly: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      observe_village: {
        id: "observe_village",
        title: "Köyü Uzaktan Gözlemleme",
        description: "Köyü uzaktan gözlemlemeye karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_observe_village.jpg",
        choices: [
          {
            id: "find_soldiers",
            text: "Yakındaki askerleri bul",
            action: "search",
            target: "find_soldiers",
            effects: {
              karma: 3,
              experience: 5,
              storyFlags: { help_others: true },
            },
            diceRoll: { type: "d20", target: 10, skill: "Perception" },
          },
          {
            id: "avoid_village",
            text: "Köyden uzak dur",
            action: "avoid",
            target: "avoid_village",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      find_soldiers: {
        id: "find_soldiers",
        title: "Askerleri Bulma",
        description: "Yakındaki askerleri bulmaya karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_find_soldiers.jpg",
        choices: [
          {
            id: "help_soldiers",
            text: "Askerlere yardım et",
            action: "help",
            target: "help_soldiers",
            effects: {
              karma: 10,
              experience: 15,
              storyFlags: { help_others: true },
            },
          },
          {
            id: "avoid_soldiers",
            text: "Askerlerden uzak dur",
            action: "avoid",
            target: "avoid_soldiers",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      help_soldiers: {
        id: "help_soldiers",
        title: "Askerlere Yardım",
        description: "Askerlere yardım etmeye karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_help_soldiers.jpg",
        choices: [
          {
            id: "fight_enemies",
            text: "Dışarıdaki tehlikelerle savaş",
            action: "combat",
            target: "fight_enemies",
            effects: {
              karma: -5,
              experience: 20,
              storyFlags: { fight_bravely: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Combat" },
            combat: true,
          },
          {
            id: "avoid_soldiers",
            text: "Askerlerden uzak dur",
            action: "avoid",
            target: "avoid_soldiers",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      avoid_soldiers: {
        id: "avoid_soldiers",
        title: "Askerlerden Uzak Durma",
        description: "Askerlerden uzak durmaya karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_avoid_soldiers.jpg",
        choices: [
          {
            id: "continue_journey",
            text: "Devam et",
            action: "move",
            target: "continue_journey",
            effects: {
              karma: 0,
              experience: 10,
              storyFlags: { explore_thoroughly: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      fight_enemies: {
        id: "fight_enemies",
        title: "Dışarıdaki Tehlikelerle Savaş",
        description: "Dışarıdaki tehlikelerle savaşmaya karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_fight_enemies.jpg",
        choices: [
          {
            id: "fight_bravely",
            text: "Bravurla savaş",
            action: "combat",
            target: "fight_bravely",
            effects: {
              karma: -10,
              experience: 25,
              storyFlags: { fight_bravely: true },
            },
            diceRoll: { type: "d20", target: 18, skill: "Combat" },
            combat: true,
          },
          {
            id: "retreat_from_enemies",
            text: "Savaştan vazgeç ve kaç",
            action: "retreat",
            target: "retreat_from_enemies",
            effects: {
              karma: -3,
              experience: 8,
              storyFlags: { run_away: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Athletics" },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      retreat_from_enemies: {
        id: "retreat_from_enemies",
        title: "Savaştan Vazgeçme",
        description: "Savaştan vazgeçmeye karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_retreat_from_enemies.jpg",
        choices: [
          {
            id: "continue_journey",
            text: "Devam et",
            action: "move",
            target: "continue_journey",
            effects: {
              karma: 0,
              experience: 10,
              storyFlags: { explore_thoroughly: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      hospital_help: {
        id: "hospital_help",
        title: "Hastaneye Gitme",
        description: "Hastaneye gitmeye karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_hospital_help.jpg",
        choices: [
          {
            id: "help_injured",
            text: "Yaralılara yardım et",
            action: "help",
            target: "help_injured",
            effects: {
              karma: 10,
              experience: 15,
              storyFlags: { help_others: true },
            },
          },
          {
            id: "avoid_hospital",
            text: "Hastanadan uzak dur",
            action: "avoid",
            target: "avoid_hospital",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      help_injured: {
        id: "help_injured",
        title: "Yaralılara Yardım",
        description: "Yaralılara yardım etmeye karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_help_injured.jpg",
        choices: [
          {
            id: "treat_wounds",
            text: "Yaraları tedavi et",
            action: "treat",
            target: "treat_wounds",
            effects: {
              karma: 5,
              experience: 10,
              storyFlags: { help_others: true },
            },
          },
          {
            id: "avoid_hospital",
            text: "Hastanadan uzak dur",
            action: "avoid",
            target: "avoid_hospital",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      avoid_hospital: {
        id: "avoid_hospital",
        title: "Hastanadan Uzak Durma",
        description: "Hastanadan uzak durmaya karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_avoid_hospital.jpg",
        choices: [
          {
            id: "continue_journey",
            text: "Devam et",
            action: "move",
            target: "continue_journey",
            effects: {
              karma: 0,
              experience: 10,
              storyFlags: { explore_thoroughly: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      treat_wounds: {
        id: "treat_wounds",
        title: "Yaraları Tedavi Etme",
        description: "Yaraları tedavi etmeye karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_treat_wounds.jpg",
        choices: [
          {
            id: "continue_journey",
            text: "Tedavi sonrası devam et",
            action: "move",
            target: "continue_journey",
            effects: {
              karma: 0,
              experience: 10,
              storyFlags: { explore_thoroughly: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      command_center: {
        id: "command_center",
        title: "Komuta Merkezine Gitme",
        description: "Komuta merkezine gitmeye karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_command_center.jpg",
        choices: [
          {
            id: "assess_situation",
            text: "Durumu değerlendir",
            action: "investigate",
            target: "assess_situation",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { investigate_clues: true },
            },
          },
          {
            id: "get_weapon_from_officer",
            text: "Subaydan silah al",
            action: "negotiate",
            target: "get_weapon_from_officer",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { accept_corruption: true },
            },
          },
          {
            id: "get_info_from_officer",
            text: "Subaydan bilgi al",
            action: "investigate",
            target: "get_info_from_officer",
            effects: {
              karma: 5,
              experience: 8,
              storyFlags: { investigate_clues: true },
            },
          },
        ],
        npcs: [
          {
            name: "Teğmen Voss",
            type: "Officer",
            personality: "Suspicious",
            motivation: "Unknown",
            relationship: "neutral",
            betrayal: true,
          },
        ],
        plotTwist: true,
        betrayal: true,
      },

      assess_situation: {
        id: "assess_situation",
        title: "Durumu Değerlendirme",
        description: "Durumu değerlendirmeye karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_assess_situation.jpg",
        choices: [
          {
            id: "get_weapon_from_officer",
            text: "Subaydan silah al",
            action: "negotiate",
            target: "get_weapon_from_officer",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { accept_corruption: true },
            },
          },
          {
            id: "get_info_from_officer",
            text: "Subaydan bilgi al",
            action: "investigate",
            target: "get_info_from_officer",
            effects: {
              karma: 5,
              experience: 8,
              storyFlags: { investigate_clues: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      get_weapon_from_officer: {
        id: "get_weapon_from_officer",
        title: "Silah Alınma",
        description: "Subaydan silah almaya karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_get_weapon_from_officer.jpg",
        choices: [
          {
            id: "accept_corruption",
            text: "Koruma kabul et",
            action: "accept",
            target: "accept_corruption",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { accept_corruption: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      get_info_from_officer: {
        id: "get_info_from_officer",
        title: "Bilgi Alınma",
        description: "Subaydan bilgi almaya karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_get_info_from_officer.jpg",
        choices: [
          {
            id: "investigate_clues",
            text: "İnceleme yap",
            action: "investigate",
            target: "investigate_clues",
            effects: {
              karma: 5,
              experience: 8,
              storyFlags: { investigate_clues: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      investigate_clues: {
        id: "investigate_clues",
        title: "İnceleme Yapma",
        description: "İnceleme yapmaya karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_investigate_clues.jpg",
        choices: [
          {
            id: "follow_map",
            text: "Haritayı takip et",
            action: "move",
            target: "map_destination",
            effects: {
              karma: 5,
              experience: 15,
              storyFlags: { explore_thoroughly: true },
            },
          },
          {
            id: "ignore_map",
            text: "Haritayı görmezden gel",
            action: "move",
            target: "continue_exploration",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "study_markers_deeper",
            text: "İşaretleri daha detaylı incele",
            action: "investigate",
            target: "deep_marker_study",
            effects: {
              karma: 3,
              experience: 12,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Arcana" },
          },
        ],
      },

      deep_marker_study: {
        id: "deep_marker_study",
        title: "İşaretleri Derinlemesine İnceleme",
        description: "İşaretleri daha detaylı inceledin. Gizli bir mesaj buldun. Ne yapacaksın?",
        backgroundImage: "fantasy_deep_marker_study.jpg",
        choices: [
          {
            id: "follow_hidden_message",
            text: "Gizli mesajı takip et",
            action: "follow",
            target: "follow_hidden_message",
            effects: {
              karma: 5,
              experience: 20,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Investigation" },
          },
          {
            id: "ignore_hidden_message",
            text: "Gizli mesajı görmezden gel",
            action: "ignore",
            target: "ignore_hidden_message",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "share_hidden_message",
            text: "Gizli mesajı başkalarıyla paylaş",
            action: "share",
            target: "share_hidden_message",
            effects: {
              karma: 8,
              experience: 15,
              storyFlags: { help_others: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Persuasion" },
          },
        ],
      },

      cave_interior: {
        id: "cave_interior",
        title: "Mağara İçi",
        description: "Mağaranın içine girdin. Karanlık ve nemli bir yer. Ne yapacaksın?",
        backgroundImage: "fantasy_cave_interior.jpg",
        choices: [
          {
            id: "explore_cave_deeper",
            text: "Mağarayı daha derin keşfet",
            action: "explore",
            target: "explore_cave_deeper",
            effects: {
              karma: 0,
              experience: 18,
              storyFlags: { explore_ruins: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Perception" },
          },
          {
            id: "search_cave_for_items",
            text: "Mağarada eşya ara",
            action: "search",
            target: "search_cave_for_items",
            effects: {
              karma: 3,
              experience: 12,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Investigation" },
          },
          {
            id: "leave_cave",
            text: "Mağaradan çık",
            action: "leave",
            target: "leave_cave",
            effects: {
              karma: 0,
              experience: 8,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      explore_cave_deeper: {
        id: "explore_cave_deeper",
        title: "Daha Derine Mağara Keşfi",
        description: "Mağarayı daha derin keşfetmeye karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_cave_deeper_exploration.jpg",
        choices: [
          {
            id: "enter_cave",
            text: "İncelemeden sonra mağaraya gir",
            action: "enter",
            target: "cave_interior",
            effects: {
              karma: 3,
              experience: 12,
              storyFlags: { explore_ruins: true },
            },
          },
          {
            id: "mark_cave_location",
            text: "Mağara konumunu işaretle",
            action: "mark",
            target: "mark_cave_location",
            effects: {
              karma: 5,
              experience: 8,
              storyFlags: { help_others: true },
            },
          },
          {
            id: "avoid_cave_after_study",
            text: "İncelemeden sonra mağaradan uzak dur",
            action: "avoid",
            target: "avoid_cave_after_study",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      search_cave_for_items: {
        id: "search_cave_for_items",
        title: "Mağarada Eşya Arama",
        description: "Mağarada eşya aramaya karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_cave_item_hunt.jpg",
        choices: [
          {
            id: "enter_cave",
            text: "İncelemeden sonra mağaraya gir",
            action: "enter",
            target: "cave_interior",
            effects: {
              karma: 3,
              experience: 12,
              storyFlags: { explore_ruins: true },
            },
          },
          {
            id: "avoid_cave",
            text: "Mağaradan uzak dur",
            action: "avoid",
            target: "avoid_cave",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
          {
            id: "leave_cave",
            text: "Mağaradan çık",
            action: "leave",
            target: "leave_cave",
            effects: {
              karma: 0,
              experience: 8,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      leave_cave: {
        id: "leave_cave",
        title: "Mağaradan Çıkış",
        description: "Mağaradan çıkış yapmaya karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_leave_cave.jpg",
        choices: [
          {
            id: "continue_journey",
            text: "Devam et",
            action: "move",
            target: "continue_journey",
            effects: {
              karma: 0,
              experience: 10,
              storyFlags: { explore_thoroughly: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      avoid_cave_after_study: {
        id: "avoid_cave_after_study",
        title: "İncelemeden Sonra Mağaradan Uzak Durma",
        description: "İncelemeden sonra mağaradan uzak durmaya karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_avoid_cave_after_study.jpg",
        choices: [
          {
            id: "continue_journey",
            text: "Devam et",
            action: "move",
            target: "continue_journey",
            effects: {
              karma: 0,
              experience: 10,
              storyFlags: { explore_thoroughly: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      mark_cave_location: {
        id: "mark_cave_location",
        title: "Mağara Konumunu İşaretleme",
        description: "Mağara konumunu işaretlemeye karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_mark_cave_location.jpg",
        choices: [
          {
            id: "continue_journey",
            text: "Devam et",
            action: "move",
            target: "continue_journey",
            effects: {
              karma: 0,
              experience: 10,
              storyFlags: { explore_thoroughly: true },
            },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      // === CYBERPUNK ŞEHRİNİN GİZLİ SIRLARI ===
      cyberpunk_start: {
        id: "cyberpunk_start",
        title: "Neon Şehrinde Uyanış",
        description: "Neon ışıkları altında, mega şirketlerin kontrol ettiği bir şehirde gözlerini açtın. Sibernetik implantların var ve AI asistanın seni uyarıyor: 'Tehlikeli bir durum var.'",
        backgroundImage: "cyberpunk_city.jpg",
        choices: [
          {
            id: "listen_to_ai",
            text: "AI asistanı dinle",
            action: "listen",
            target: "listen_to_ai",
            effects: {
              karma: 5,
              experience: 10,
              storyFlags: { trust_everyone: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Technology" },
          },
          {
            id: "explore_environment",
            text: "Çevreyi keşfet",
            action: "explore",
            target: "explore_environment",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { explore_thoroughly: true },
            },
            diceRoll: { type: "d20", target: 10, skill: "Perception" },
          },
          {
            id: "find_hackers",
            text: "Hackers'ları ara",
            action: "search",
            target: "find_hackers",
            effects: {
              karma: 0,
              experience: 12,
              storyFlags: { help_others: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Hacking" },
          },
          {
            id: "go_to_corporate",
            text: "Şirket binasına git",
            action: "move",
            target: "go_to_corporate",
            effects: {
              karma: -5,
              experience: 5,
              storyFlags: { blind_faith: true },
            },
            diceRoll: { type: "d20", target: 8, skill: "Stealth" },
          },
        ],
        npcs: [
          {
            name: "AI Asistan",
            type: "AI",
            personality: "Helpful",
            motivation: "Help user",
            relationship: "neutral",
            betrayal: true,
          },
        ],
        items: ["Cyber Deck", "Neural Implant", "Energy Pistol"],
      },

      listen_to_ai: {
        id: "listen_to_ai",
        title: "AI Uyarısı",
        description:
          "AI asistan: 'Mega şirketler şehri ele geçirmeye çalışıyor. Sibernetik implantlarınızı kontrol ediyorlar. Hemen harekete geçmelisiniz.'",
        backgroundImage: "cyberpunk_ai_warning.jpg",
        choices: [
          {
            id: "trust_ai",
            text: "AI'ya güven",
            action: "trust",
            target: "trust_ai",
            effects: {
              karma: 5,
              experience: 10,
              relationship: "trust",
              storyFlags: { trust_everyone: true },
            },
          },
          {
            id: "suspect_ai",
            text: "AI'yı şüpheli bul",
            action: "investigate",
            target: "suspect_ai",
            effects: {
              karma: 10,
              experience: 15,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Insight" },
          },
          {
            id: "ask_for_more_info",
            text: "Daha fazla bilgi iste",
            action: "investigate",
            target: "ask_for_more_info",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { explore_thoroughly: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Investigation" },
          },
          {
            id: "disable_ai",
            text: "AI'yı devre dışı bırak",
            action: "hack",
            target: "disable_ai",
            effects: {
              karma: -5,
              experience: 12,
              storyFlags: { blind_faith: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Technology" },
          },
        ],
        npcs: [
          {
            name: "AI Asistan",
            type: "AI",
            personality: "Helpful",
            motivation: "Help user",
            relationship: "neutral",
            betrayal: true,
          },
        ],
        plotTwist: true,
        betrayal: true,
      },

      suspect_ai: {
        id: "suspect_ai",
        title: "AI'yı Şüpheli Bulma",
        description: "AI'yı şüpheli bulmaya karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_suspect_ai.jpg",
        choices: [
          {
            id: "investigate_clues",
            text: "İnceleme yap",
            action: "investigate",
            target: "investigate_clues",
            effects: {
              karma: 10,
              experience: 15,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Insight" },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      ask_for_more_info: {
        id: "ask_for_more_info",
        title: "Daha Fazla Bilgi İste",
        description: "Daha fazla bilgi isteye karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_ask_for_more_info.jpg",
        choices: [
          {
            id: "investigate_clues",
            text: "İnceleme yap",
            action: "investigate",
            target: "investigate_clues",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { explore_thoroughly: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Investigation" },
          },
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      disable_ai: {
        id: "disable_ai",
        title: "AI'yı Devre Dışı Bırakma",
        description: "AI'yı devre dışı bırakmaya karar verdin. İçerideki tehlikeleri biliyorsun.",
        backgroundImage: "fantasy_disable_ai.jpg",
        choices: [
          {
            id: "return_to_start",
            text: "Başlangıç noktasına dön",
            action: "return",
            target: "start",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { self_preservation: true },
            },
          },
        ],
      },

      // === HIVE ŞEHRİNİN SAVUNMASI (WARHAMMER 40K) ===
      hive_start: {
        id: "hive_start",
        title: "Hive Şehrinde Uyanış",
        description: "Hive şehrinin 47. seviyesinde, karanlık bir odada gözlerini açtın. Yukarıdan gelen patlamalar ve çığlıklar... Şehir saldırı altında.",
        backgroundImage: "hive_city.jpg",
        choices: [
          {
            id: "upper_levels",
            text: "Yukarı seviyelere çık ve durumu öğren",
            action: "move",
            target: "upper_levels",
            effects: {
              karma: 5,
              experience: 10,
              storyFlags: { explore_thoroughly: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Athletics" },
          },
          {
            id: "lower_tunnels",
            text: "Aşağı tünellere in ve gizli yollar ara",
            action: "explore",
            target: "lower_tunnels",
            effects: {
              karma: 0,
              experience: 8,
              storyFlags: { explore_ruins: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Stealth" },
          },
          {
            id: "find_soldiers",
            text: "Yakındaki askerleri bul",
            action: "search",
            target: "find_soldiers",
            effects: {
              karma: 3,
              experience: 5,
              storyFlags: { help_others: true },
            },
            diceRoll: { type: "d20", target: 10, skill: "Perception" },
          },
          {
            id: "escape_with_civilians",
            text: "Sivillerle birlikte kaç",
            action: "help",
            target: "escape_with_civilians",
            effects: {
              karma: 10,
              experience: 12,
              storyFlags: { save_others: true },
            },
            diceRoll: { type: "d20", target: 8, skill: "Survival" },
          },
        ],
        items: ["Laser Rifle", "Combat Armor", "Med Kit"],
      },

      upper_levels: {
        id: "upper_levels",
        title: "Üst Seviyeler",
        description: "Üst seviyelere çıktın. Hive'ın 23. seviyesi kaos içinde. İnsanlar panik halinde kaçışıyor. Bir subay seni görüyor ve koşarak geliyor.",
        backgroundImage: "hive_upper_levels.jpg",
        choices: [
          {
            id: "officer_meeting",
            text: "Subayla konuş",
            action: "talk",
            target: "officer_meeting",
            effects: {
              karma: 5,
              experience: 10,
              relationship: "friendly",
              storyFlags: { trust_everyone: true },
            },
          },
          {
            id: "escape_with_crowd",
            text: "Kalabalığa karış ve kaç",
            action: "flee",
            target: "escape_with_crowd",
            effects: {
              karma: -5,
              experience: 5,
              storyFlags: { run_away: true },
            },
            diceRoll: { type: "d20", target: 10, skill: "Stealth" },
          },
          {
            id: "weapon_depot",
            text: "Yakındaki silah deposuna git",
            action: "explore",
            target: "weapon_depot",
            effects: {
              karma: 0,
              experience: 8,
              storyFlags: { explore_thoroughly: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Athletics" },
          },
          {
            id: "hospital_help",
            text: "Hastaneye git ve yaralılara yardım et",
            action: "help",
            target: "hospital_help",
            effects: {
              karma: 10,
              experience: 15,
              storyFlags: { help_others: true },
            },
          },
        ],
        npcs: [
          {
            name: "Teğmen Voss",
            type: "Officer",
            personality: "Suspicious",
            motivation: "Unknown",
            relationship: "neutral",
            betrayal: true,
          },
        ],
        plotTwist: true,
        betrayal: false,
      },

      officer_meeting: {
        id: "officer_meeting",
        title: "Subay Toplantısı",
        description:
          "Subay: 'Teğmen! Sonunda bir subay buldum. Orklar kuzey kapısını yarıyor. Komutan Krell seni arıyor. Hemen komuta merkezine gitmelisin.'",
        backgroundImage: "hive_command_center.jpg",
        choices: [
          {
            id: "command_center",
            text: "Komuta merkezine git",
            action: "move",
            target: "command_center",
            effects: {
              karma: 5,
              experience: 10,
              storyFlags: { trust_everyone: true },
            },
          },
          {
            id: "assess_situation",
            text: "Önce durumu değerlendir",
            action: "investigate",
            target: "assess_situation",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Investigation" },
          },
          {
            id: "get_weapon_from_officer",
            text: "Subaydan silah al",
            action: "negotiate",
            target: "get_weapon_from_officer",
            effects: {
              karma: 0,
              experience: 5,
              storyFlags: { accept_corruption: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Persuasion" },
          },
          {
            id: "get_info_from_officer",
            text: "Subaydan bilgi al",
            action: "investigate",
            target: "get_info_from_officer",
            effects: {
              karma: 5,
              experience: 8,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Insight" },
          },
        ],
        npcs: [
          {
            name: "Teğmen Voss",
            type: "Officer",
            personality: "Suspicious",
            motivation: "Unknown",
            relationship: "neutral",
            betrayal: true,
          },
        ],
        plotTwist: true,
        betrayal: true,
      },

      // === CYBERPUNK ŞEHRİNİN GİZLİ SIRLARI ===
      cyberpunk_start: {
        id: "cyberpunk_start",
        title: "Neon Şehrinde Uyanış",
        description: "Neon ışıkları altında, mega şirketlerin kontrol ettiği bir şehirde gözlerini açtın. Sibernetik implantların var ve AI asistanın seni uyarıyor: 'Tehlikeli bir durum var.'",
        backgroundImage: "cyberpunk_city.jpg",
        choices: [
          {
            id: "listen_to_ai",
            text: "AI asistanı dinle",
            action: "listen",
            target: "listen_to_ai",
            effects: {
              karma: 5,
              experience: 10,
              storyFlags: { trust_everyone: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Technology" },
          },
          {
            id: "explore_environment",
            text: "Çevreyi keşfet",
            action: "explore",
            target: "explore_environment",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { explore_thoroughly: true },
            },
            diceRoll: { type: "d20", target: 10, skill: "Perception" },
          },
          {
            id: "find_hackers",
            text: "Hackers'ları ara",
            action: "search",
            target: "find_hackers",
            effects: {
              karma: 0,
              experience: 12,
              storyFlags: { help_others: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Hacking" },
          },
          {
            id: "go_to_corporate",
            text: "Şirket binasına git",
            action: "move",
            target: "go_to_corporate",
            effects: {
              karma: -5,
              experience: 5,
              storyFlags: { blind_faith: true },
            },
            diceRoll: { type: "d20", target: 8, skill: "Stealth" },
          },
        ],
        npcs: [
          {
            name: "AI Asistan",
            type: "AI",
            personality: "Helpful",
            motivation: "Help user",
            relationship: "neutral",
            betrayal: true,
          },
        ],
        items: ["Cyber Deck", "Neural Implant", "Energy Pistol"],
      },

      listen_to_ai: {
        id: "listen_to_ai",
        title: "AI Uyarısı",
        description:
          "AI asistan: 'Mega şirketler şehri ele geçirmeye çalışıyor. Sibernetik implantlarınızı kontrol ediyorlar. Hemen harekete geçmelisiniz.'",
        backgroundImage: "cyberpunk_ai_warning.jpg",
        choices: [
          {
            id: "trust_ai",
            text: "AI'ya güven",
            action: "trust",
            target: "trust_ai",
            effects: {
              karma: 5,
              experience: 10,
              relationship: "trust",
              storyFlags: { trust_everyone: true },
            },
          },
          {
            id: "suspect_ai",
            text: "AI'yı şüpheli bul",
            action: "investigate",
            target: "suspect_ai",
            effects: {
              karma: 10,
              experience: 15,
              storyFlags: { investigate_clues: true },
            },
            diceRoll: { type: "d20", target: 16, skill: "Insight" },
          },
          {
            id: "ask_for_more_info",
            text: "Daha fazla bilgi iste",
            action: "investigate",
            target: "ask_for_more_info",
            effects: {
              karma: 3,
              experience: 8,
              storyFlags: { explore_thoroughly: true },
            },
            diceRoll: { type: "d20", target: 14, skill: "Investigation" },
          },
          {
            id: "disable_ai",
            text: "AI'yı devre dışı bırak",
            action: "hack",
            target: "disable_ai",
            effects: {
              karma: -5,
              experience: 12,
              storyFlags: { blind_faith: true },
            },
            diceRoll: { type: "d20", target: 12, skill: "Technology" },
          },
        ],
        npcs: [
          {
            name: "AI Asistan",
            type: "AI",
            personality: "Helpful",
            motivation: "Help user",
            relationship: "neutral",
            betrayal: true,
          },
        ],
        plotTwist: true,
        betrayal: true,
      },

      // === SON SAHNELER ===
      victory_ending: {
        id: "victory_ending",
        title: "Zafer",
        description: "Mücadeleyi kazandın! Sen bir kahraman oldun. Halk seni alkışlıyor ve gelecek parlak görünüyor.",
        backgroundImage: "victory.jpg",
        choices: [
          {
            id: "accept_reward",
            text: "Ödülü kabul et",
            action: "accept",
            target: "accept_reward",
            effects: {
              karma: 15,
              experience: 50,
              item: "Legendary Weapon",
            },
          },
          {
            id: "start_new_adventure",
            text: "Yeni maceraya çık",
            action: "continue",
            target: "start",
            effects: {
              karma: 10,
              experience: 25,
            },
          },
          {
            id: "return_home",
            text: "Eve dön",
            action: "end",
            target: "game_end",
            effects: {
              karma: 5,
              experience: 15,
            },
          },
        ],
        ending: true,
      },

      tragic_ending: {
        id: "tragic_ending",
        title: "Trajik Zafer",
        description: "Zafer kazandın ama büyük bir bedel ödedin. Kayıpların anısı seni takip ediyor.",
        backgroundImage: "tragic.jpg",
        choices: [
          {
            id: "mourn_losses",
            text: "Yas tut",
            action: "mourn",
            target: "mourn_losses",
            effects: {
              karma: 5,
              experience: 20,
            },
          },
          {
            id: "seek_revenge",
            text: "İntikam al",
            action: "revenge",
            target: "seek_revenge",
            effects: {
              karma: -5,
              experience: 15,
            },
          },
          {
            id: "new_beginning",
            text: "Yeni başlangıç yap",
            action: "continue",
            target: "start",
            effects: {
              karma: 0,
              experience: 10,
            },
          },
        ],
        ending: true,
      },

      betrayal_ending: {
        id: "betrayal_ending",
        title: "İhanet",
        description: "Güvendiğin kişinin gerçek yüzünü gördün. İhanet acısı kalbini yakıyor.",
        backgroundImage: "betrayal.jpg",
        choices: [
          {
            id: "revenge_quest",
            text: "İntikam peşinde",
            action: "revenge",
            target: "revenge_quest",
            effects: {
              karma: -10,
              experience: 30,
            },
          },
          {
            id: "forgive_betrayer",
            text: "Affet",
            action: "forgive",
            target: "forgive_betrayer",
            effects: {
              karma: 20,
              experience: 25,
            },
          },
          {
            id: "start_fresh",
            text: "Temiz sayfa aç",
            action: "continue",
            target: "start",
            effects: {
              karma: 5,
              experience: 15,
            },
          },
        ],
        ending: true,
      },

      game_end: {
        id: "game_end",
        title: "Oyun Sonu",
        description: "Yolculuğunu tamamladın! Karakterin gelişti ve yeni deneyimler kazandın.",
        backgroundImage: "game_end.jpg",
        choices: [
          {
            id: "restart_game",
            text: "Yeni oyun başlat",
            action: "restart",
            target: "start",
            effects: {
              storyFlags: { game_restarted: true },
            },
          },
        ],
        ending: true,
      },
    };
  }

  // Oyuncu seçimi yapıldığında çağrılır
  makeChoice(choiceId) {
    const currentScene = this.sceneDatabase[this.gameState.story.currentScene];
    const choice = currentScene.choices.find((c) => c.id === choiceId);

    if (!choice) {
      console.error("Seçim bulunamadı:", choiceId);
      return null;
    }

    // Seçim sonuçlarını uygula
    this.applyChoiceEffects(choice.effects);

    // Hikaye bayraklarını güncelle
    this.updateStoryFlags(choice.effects.storyFlags || {});

    // Yeni sahneyi yükle
    const nextScene = this.sceneDatabase[choice.target];

    if (!nextScene) {
      console.error("Hedef sahne bulunamadı:", choice.target);
      return null;
    }

    // Sahne geçişini kaydet
    this.gameState.story.visitedScenes.push(this.gameState.story.currentScene);
    this.gameState.story.currentScene = choice.target;
    this.gameState.story.choices.push({
      sceneId: currentScene.id,
      choiceId: choiceId,
      timestamp: Date.now(),
    });

    return {
      scene: nextScene,
      choice: choice,
      gameState: this.gameState,
    };
  }

  // Seçim efektlerini uygula
  applyChoiceEffects(effects) {
    if (effects.health) {
      this.gameState.player.health = Math.max(
        0,
        Math.min(100, this.gameState.player.health + effects.health)
      );
    }
    if (effects.mana) {
      this.gameState.player.mana = Math.max(
        0,
        Math.min(100, this.gameState.player.mana + effects.mana)
      );
    }
    if (effects.experience) {
      this.gameState.player.experience += effects.experience;
      this.checkLevelUp();
    }
    if (effects.karma) {
      this.gameState.player.karma += effects.karma;
    }
    if (effects.location) {
      this.gameState.player.location = effects.location;
    }
    if (effects.inventory) {
      this.gameState.player.inventory.push(...effects.inventory);
    }
    if (effects.relationship) {
      this.gameState.player.relationships[effects.relationship] = true;
    }
  }

  // Hikaye bayraklarını güncelle
  updateStoryFlags(newFlags) {
    this.gameState.story.storyFlags = {
      ...this.gameState.story.storyFlags,
      ...newFlags,
    };
  }

  // Seviye atlama kontrolü
  checkLevelUp() {
    const expNeeded = this.gameState.player.level * 100;
    if (this.gameState.player.experience >= expNeeded) {
      this.gameState.player.level++;
      this.gameState.player.experience -= expNeeded;
      this.gameState.player.health = Math.min(
        100,
        this.gameState.player.health + 10
      );
      this.gameState.player.mana = Math.min(
        100,
        this.gameState.player.mana + 5
      );
      return true;
    }
    return false;
  }

  // Mevcut sahneyi getir
  getCurrentScene() {
    return this.sceneDatabase[this.gameState.story.currentScene];
  }

  // Oyun durumunu getir
  getGameState() {
    return this.gameState;
  }

  // Oyun durumunu sıfırla
  resetGame() {
    this.gameState = {
      player: {
        health: 100,
        mana: 50,
        experience: 0,
        level: 1,
        inventory: [],
        karma: 0,
        relationships: {},
        location: "start",
        quests: [],
        flags: {},
      },
      story: {
        currentScene: "start",
        visitedScenes: [],
        choices: [],
        storyFlags: {},
        npcStates: {},
        worldState: {},
      },
      campaign: {
        id: null,
        progress: 0,
        completedQuests: [],
        activeQuests: [],
      },
    };
  }

  // Hikaye sürekliliği kontrolü - önceki seçimlere göre sahne varyasyonları
  getDynamicScene(sceneId) {
    const baseScene = this.sceneDatabase[sceneId];
    if (!baseScene) return null;

    // Önceki seçimlere göre sahneyi özelleştir
    const storyFlags = this.gameState.story.storyFlags;

    // Örnek: Eğer oyuncu daha önce kurtla savaştıysa, farklı bir sahne göster
    if (sceneId === "dragon_encounter" && storyFlags.fight_bravely) {
      return {
        ...baseScene,
        description:
          "Ejderha ile daha önce savaştığın için, bu sefer daha dikkatli yaklaşıyorsun.",
        choices: baseScene.choices.map((choice) => ({
          ...choice,
          effects: {
            ...choice.effects,
            experience: (choice.effects.experience || 0) + 5, // Bonus XP
          },
        })),
      };
    }

    // Örnek: Eğer oyuncu tapınağı keşfettiyse, farklı seçenekler
    if (sceneId === "accept_quest" && storyFlags.explore_ruins) {
      return {
        ...baseScene,
        description:
          "Tapınağı daha önce keşfettiğin için, içerideki tehlikeleri biliyorsun.",
        choices: [
          ...baseScene.choices,
          {
            id: "use_previous_knowledge",
            text: "Önceki bilgilerini kullan",
            action: "strategy",
            target: "use_previous_knowledge",
            effects: {
              storyFlags: { use_previous_knowledge: true },
              experience: 20,
              karma: 5,
            },
          },
        ],
      };
    }

    return baseScene;
  }
}
