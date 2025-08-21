import React, { useState, useEffect } from "react";
import {
  GameMasterAI,
  GameResponse,
  GameAction,
} from "../services/GameMasterAI";
import { StoredScenario } from "../types/scenarioStorage";
import { DiceRollUI } from "./DiceRollUI";
import SkillTreeUI from "./SkillTreeUI";
import "./GameMasterUI.css";
import { io } from "socket.io-client";

// Character Classes from Python system
const CHARACTER_CLASSES = {
  // Fantasy Classes
  warrior: {
    name: "Warrior",
    hp: 120,
    attack: 85,
    defense: 90,
    special: 0,
    abilities: ["Shield Wall", "Sword Strike", "Battle Cry", "Heavy Strike"],
    description: "Güçlü savaşçı, yüksek savunma ve HP",
    icon: "⚔️",
    skillTree: {
      combat: [
        "Shield Wall",
        "Sword Strike",
        "Battle Cry",
        "Heavy Strike",
        "Whirlwind Attack",
      ],
      leadership: ["Command Aura", "Rally Cry", "Tactical Mastery"],
      survival: ["Iron Will", "Endurance", "Second Wind"],
    },
  },
  mage: {
    name: "Mage",
    hp: 60,
    attack: 100,
    defense: 40,
    special: 150,
    abilities: ["Fireball", "Ice Bolt", "Lightning Strike", "Arcane Shield"],
    description: "Güçlü büyücü, yüksek saldırı ve mana",
    icon: "🔮",
    skillTree: {
      elemental: [
        "Fireball",
        "Ice Bolt",
        "Lightning Strike",
        "Earthquake",
        "Meteor Storm",
      ],
      arcane: ["Arcane Shield", "Teleport", "Time Slow", "Reality Warp"],
      support: ["Heal", "Protection", "Enhancement"],
    },
  },
  rogue: {
    name: "Rogue",
    hp: 80,
    attack: 90,
    defense: 60,
    special: 95,
    abilities: ["Stealth", "Backstab", "Poison Dart", "Shadow Step"],
    description: "Hızlı ve gizli, yüksek saldırı ve stealth",
    icon: "🗡️",
    skillTree: {
      stealth: ["Stealth", "Shadow Step", "Invisibility", "Silent Movement"],
      assassination: ["Backstab", "Poison Dart", "Death Mark", "Assassinate"],
      agility: ["Dodge", "Acrobatics", "Stealth Escape"],
    },
  },
  priest: {
    name: "Priest",
    hp: 70,
    attack: 50,
    defense: 70,
    special: 80,
    abilities: ["Heal", "Bless", "Smite", "Divine Shield"],
    description: "İyileştirici, yüksek heal ve savunma",
    icon: "⛪",
    skillTree: {
      healing: ["Heal", "Mass Heal", "Regeneration", "Resurrection"],
      divine: ["Bless", "Smite", "Divine Shield", "Holy Wrath"],
      protection: ["Protection", "Guardian Angel", "Divine Barrier"],
    },
  },
  // Warhammer Classes
  space_marine: {
    name: "Space Marine",
    hp: 150,
    attack: 95,
    defense: 100,
    special: 120,
    abilities: [
      "Bolter Fire",
      "Power Armor",
      "Chainsword Strike",
      "Grenade Toss",
    ],
    description: "Süper asker, yüksek HP ve savunma",
    icon: "🛡️",
    skillTree: {
      combat: [
        "Bolter Fire",
        "Chainsword Strike",
        "Power Fist",
        "Heavy Bolter",
      ],
      tactics: ["Power Armor", "Tactical Advance", "Squad Tactics"],
      special: ["Grenade Toss", "Plasma Gun", "Melta Gun"],
    },
  },
  tech_priest: {
    name: "Tech-Priest",
    hp: 90,
    attack: 60,
    defense: 80,
    special: 100,
    abilities: ["Repair", "Tech Scan", "Servo-Arm", "Plasma Cutter"],
    description: "Teknoloji uzmanı, yüksek tech ve savunma",
    icon: "⚙️",
    skillTree: {
      technology: ["Repair", "Tech Scan", "Hack", "Override"],
      cybernetics: ["Servo-Arm", "Plasma Cutter", "Mechadendrite"],
      rituals: ["Machine Spirit", "Sacred Rites", "Techno-Sorcery"],
    },
  },
  inquisitor: {
    name: "Inquisitor",
    hp: 100,
    attack: 85,
    defense: 75,
    special: 95,
    abilities: ["Purge", "Investigate", "Interrogate", "Exterminatus"],
    description: "Araştırmacı, dengeli istatistikler",
    icon: "🔍",
    skillTree: {
      investigation: [
        "Investigate",
        "Interrogate",
        "Detect Lies",
        "Psychic Probe",
      ],
      combat: ["Purge", "Exterminatus", "Power Sword", "Inferno Pistol"],
      authority: ["Command", "Intimidate", "Execute"],
    },
  },
  imperial_guard: {
    name: "Imperial Guard",
    hp: 80,
    attack: 70,
    defense: 60,
    special: 90,
    abilities: ["Teamwork", "Suppression", "Bayonet Charge", "Cover Fire"],
    description: "Asker, takım çalışması odaklı",
    icon: "🎖️",
    skillTree: {
      teamwork: ["Teamwork", "Cover Fire", "Squad Formation", "Combined Arms"],
      tactics: ["Suppression", "Bayonet Charge", "Trench Warfare"],
      leadership: ["Sergeant", "Commander", "Field Officer"],
    },
  },
};

// Character Races
const CHARACTER_RACES = {
  human: {
    name: "İnsan",
    description: "Dengeli ve uyumlu, tüm sınıflara uygun",
    hp_bonus: 10,
    attack_bonus: 5,
    defense_bonus: 5,
    special_traits: ["Uyumluluk", "Çok yönlülük"],
  },
  elf: {
    name: "Elf",
    description: "Zeki ve çevik, büyücülük ve okçulukta uzman",
    hp_bonus: 5,
    attack_bonus: 10,
    defense_bonus: 8,
    special_traits: ["Uzun ömür", "Doğa bağlantısı"],
  },
  dwarf: {
    name: "Cüce",
    description: "Güçlü ve dayanıklı, savaşçılıkta üstün",
    hp_bonus: 15,
    attack_bonus: 8,
    defense_bonus: 12,
    special_traits: ["Taş işçiliği", "Dayanıklılık"],
  },
};

// Skill System
const SKILL_SYSTEM = {
  // Skill categories and their effects
  combat: {
    "Shield Wall": {
      damage: 0,
      defense: 25,
      description: "Savunma pozisyonu al",
    },
    "Sword Strike": {
      damage: 30,
      defense: 0,
      description: "Güçlü kılıç saldırısı",
    },
    "Battle Cry": { damage: 15, defense: 10, description: "Düşmanı korkut" },
    "Heavy Strike": { damage: 45, defense: -10, description: "Ağır saldırı" },
    "Whirlwind Attack": {
      damage: 35,
      defense: 5,
      description: "Dönen saldırı",
    },
    "Bolter Fire": { damage: 40, defense: 0, description: "Bolter ateşi" },
    "Chainsword Strike": {
      damage: 50,
      defense: 0,
      description: "Zincir kılıç saldırısı",
    },
    "Power Fist": { damage: 60, defense: 0, description: "Güç yumruğu" },
    "Heavy Bolter": { damage: 70, defense: -15, description: "Ağır bolter" },
    Purge: { damage: 55, defense: 0, description: "Temizlik saldırısı" },
    Exterminatus: {
      damage: 100,
      defense: -20,
      description: "Yok etme saldırısı",
    },
    "Bayonet Charge": { damage: 35, defense: 0, description: "Süngü hücumu" },
    "Cover Fire": { damage: 25, defense: 15, description: "Koruyucu ateş" },
  },
  magic: {
    Fireball: { damage: 45, mana: 20, description: "Ateş topu" },
    "Ice Bolt": { damage: 35, mana: 15, description: "Buz oku" },
    "Lightning Strike": {
      damage: 55,
      mana: 25,
      description: "Şimşek saldırısı",
    },
    "Arcane Shield": {
      damage: 0,
      mana: 30,
      defense: 40,
      description: "Büyü kalkanı",
    },
    Earthquake: { damage: 65, mana: 40, description: "Deprem" },
    "Meteor Storm": { damage: 80, mana: 60, description: "Meteor fırtınası" },
    Teleport: { damage: 0, mana: 25, description: "Işınlanma" },
    "Time Slow": { damage: 0, mana: 35, description: "Zamanı yavaşlat" },
    "Reality Warp": { damage: 70, mana: 50, description: "Gerçekliği bük" },
    Heal: { damage: 0, mana: 20, heal: 40, description: "İyileştirme" },
    "Mass Heal": {
      damage: 0,
      mana: 45,
      heal: 60,
      description: "Toplu iyileştirme",
    },
    Smite: { damage: 50, mana: 25, description: "Tanrısal saldırı" },
    "Divine Shield": {
      damage: 0,
      mana: 30,
      defense: 50,
      description: "Kutsal kalkan",
    },
    "Holy Wrath": { damage: 75, mana: 40, description: "Kutsal öfke" },
  },
  stealth: {
    Stealth: { damage: 0, stealth: 30, description: "Gizlenme" },
    Backstab: { damage: 60, stealth: 0, description: "Sırtından bıçaklama" },
    "Poison Dart": { damage: 25, poison: 20, description: "Zehirli dart" },
    "Shadow Step": { damage: 0, stealth: 40, description: "Gölge adımı" },
    Invisibility: {
      damage: 0,
      stealth: 60,
      mana: 35,
      description: "Görünmezlik",
    },
    "Silent Movement": {
      damage: 0,
      stealth: 25,
      description: "Sessiz hareket",
    },
    "Death Mark": { damage: 0, mark: true, description: "Ölüm işareti" },
    Assassinate: { damage: 90, stealth: 0, description: "Suikast" },
    Dodge: { damage: 0, dodge: 40, description: "Kaçınma" },
    Acrobatics: { damage: 0, dodge: 30, description: "Akrobasi" },
    "Stealth Escape": { damage: 0, escape: true, description: "Gizli kaçış" },
  },
  technology: {
    Repair: { damage: 0, repair: 40, description: "Onarım" },
    "Tech Scan": { damage: 0, scan: true, description: "Teknoloji taraması" },
    Hack: { damage: 0, hack: 30, description: "Hack" },
    Override: { damage: 0, override: true, description: "Geçersiz kılma" },
    "Servo-Arm": { damage: 45, defense: 20, description: "Servo kol" },
    "Plasma Cutter": { damage: 55, description: "Plazma kesici" },
    Mechadendrite: { damage: 40, defense: 15, description: "Mekadendrit" },
    "Machine Spirit": { damage: 0, buff: 25, description: "Makine ruhu" },
    "Sacred Rites": { damage: 0, ritual: true, description: "Kutsal ayinler" },
    "Techno-Sorcery": { damage: 65, mana: 30, description: "Tekno-büyücülük" },
  },
};

// Attribute System
const ATTRIBUTES = {
  strength: {
    name: "Güç",
    description: "Fiziksel güç ve hasar",
    affects: ["attack", "carry_weight"],
  },
  dexterity: {
    name: "Çeviklik",
    description: "Hız ve kaçınma",
    affects: ["dodge", "stealth"],
  },
  constitution: {
    name: "Dayanıklılık",
    description: "Sağlık ve direnç",
    affects: ["hp", "defense"],
  },
  intelligence: {
    name: "Zeka",
    description: "Büyü ve teknoloji",
    affects: ["mana", "hack"],
  },
  wisdom: {
    name: "Bilgelik",
    description: "Sezgi ve iyileştirme",
    affects: ["heal", "detection"],
  },
  charisma: {
    name: "Karizma",
    description: "Sosyal etkileşim",
    affects: ["persuasion", "leadership"],
  },
};

// Simple Story Progression System
const STORY_BRANCHES = {
  dragon_hunters_path: {
    start: {
      narrative:
        "Gözlerini açtığında kendini yanmış bir köyün ortasında buluyorsun. Duman ciğerlerini yakıyor, alevler hala sönmemiş. Uzaktan çocuk ağlaması geliyor. Bu senin hikayenin başlangıcı. Köyün adı Ateşgülü, ve sen burada doğdun. Şimdi her şey yanmış durumda.",
      actions: [
        {
          id: "follow_crying",
          description:
            "Çocuk ağlamasını takip et - hayat kurtarmak her şeyden önce gelir",
          type: "rescue",
        },
        {
          id: "track_dragon",
          description:
            "Ejderha izlerini ara - bu canavarı durdurmak zorundayım",
          type: "investigate",
        },
        {
          id: "talk_villagers",
          description: "Köylülerle konuş - bu durumu anlamam gerekiyor",
          type: "social",
        },
        {
          id: "search_survivors",
          description: "Hayatta kalanları ara - belki başka kurbanlar var",
          type: "rescue",
        },
      ],
    },
    follow_crying: {
      narrative:
        "Çocuk ağlamasını takip ederek yanmış evlerin arasından geçiyorsun. Sonunda küçük bir ahırda 5 yaşında bir kız çocuğu buluyorsun. Gözleri korkuyla dolu, ama güvende. Adı Elara. Annesi ve babası nerede? Elara sana bakıyor, gözlerinde umut var.",
      actions: [
        {
          id: "comfort_elara",
          description:
            "Elara'yı teselli et ve güven ver - bu küçük kızın sana ihtiyacı var",
          type: "social",
        },
        {
          id: "search_elara_parents",
          description:
            "Elara'nın ebeveynlerini aramaya devam et - belki hayattalar",
          type: "investigate",
        },
        {
          id: "take_elara_safe",
          description: "Elara'yı güvenli bir yere götür - önce onu korumalıyım",
          type: "rescue",
        },
        {
          id: "ask_elara_what_happened",
          description: "Elara'ya ne olduğunu sor - belki bilgi verebilir",
          type: "social",
        },
      ],
    },
    comfort_elara: {
      narrative:
        "Elara'ya yaklaşıyorsun, yumuşak bir sesle konuşuyorsun. 'Korkma, ben seni koruyacağım.' Elara gözlerini silerek sana bakıyor. 'Büyük kırmızı canavar geldi... Anne ve baba beni buraya sakladı... Ama geri gelmediler.' Gözlerinde yaşlar var. Bu küçük kızın güvenini kazandın.",
      actions: [
        {
          id: "elara_trust_established",
          description:
            "Elara'nın güvenini kazandın - şimdi ne yapacağına karar ver",
          type: "social",
        },
        {
          id: "elara_reveals_secret",
          description:
            "Elara sana bir sır veriyor - 'Büyük kırmızı canavar konuştu...'",
          type: "investigate",
        },
        {
          id: "elara_remembers_path",
          description:
            "Elara ejderhanın gittiği yolu hatırlıyor - 'O yöne gitti'",
          type: "investigate",
        },
      ],
    },
    elara_trust_established: {
      narrative:
        "Elara artık sana güveniyor. Küçük elini tutuyorsun ve birlikte ahırdan çıkıyorsun. Köyün ortasında duruyorsunuz. Elara: 'Şimdi ne yapacağız?' Gözlerinde hem korku hem de umut var. Bu küçük kızın hayatı artık senin ellerinde.",
      actions: [
        {
          id: "search_village_together",
          description:
            "Elara ile birlikte köyü ara - belki başka hayatta kalanlar var",
          type: "investigate",
        },
        {
          id: "take_elara_to_safety",
          description:
            "Elara'yı yakındaki güvenli bir yere götür - önce onu korumalıyım",
          type: "rescue",
        },
        {
          id: "teach_elara_bravery",
          description: "Elara'ya cesaret ver - 'Birlikte güçlüyüz'",
          type: "social",
        },
        {
          id: "elara_remembers_family",
          description:
            "Elara ailesini hatırlıyor - 'Babam ejderha avcısıydı...'",
          type: "investigate",
        },
      ],
    },
    elara_remembers_family: {
      narrative:
        "Elara'nın gözleri parladı: 'Babam ejderha avcısıydı! Bana her zaman ejderhalar hakkında hikayeler anlatırdı. Ama bu ejderha farklıydı... Babam onunla konuştu, ama ejderha çok kızdı.' Elara'nın sesi titriyor. 'Babam bana bir şey verdi, saklamamı söyledi.'",
      actions: [
        {
          id: "elara_shows_artifact",
          description:
            "Elara'nın sakladığı eşyayı göster - belki önemli bir şey",
          type: "investigate",
        },
        {
          id: "ask_about_father",
          description:
            "Elara'ya babası hakkında daha fazla sor - belki ipucu var",
          type: "social",
        },
        {
          id: "elara_father_teachings",
          description:
            "Elara babasının öğrettiklerini hatırlıyor - 'Ejderhalar aslında...'",
          type: "investigate",
        },
        {
          id: "elara_emotional_breakdown",
          description: "Elara duygusal olarak çöküyor - 'Babam öldü mü?'",
          type: "social",
        },
      ],
    },
    elara_shows_artifact: {
      narrative:
        "Elara küçük cebinden parlak bir taş çıkarıyor. Taş mavi bir ışık yayıyor ve sıcak. 'Babam buna Ejderha Kalbi dedi. Ejderhalarla konuşmamı sağlar, dedi.' Taş elinde titreşiyor. Bu sıradan bir taş değil - bu gerçekten bir ejderha kalbi!",
      actions: [
        {
          id: "examine_dragon_heart",
          description: "Ejderha kalbini incele - bu güçlü bir artefakt",
          type: "investigate",
        },
        {
          id: "dragon_heart_reacts",
          description: "Ejderha kalbi tepki veriyor - uzaktan bir ses geliyor",
          type: "magic",
        },
        {
          id: "elara_hears_voice",
          description: "Elara bir ses duyuyor - 'Bu ejderha kalbi konuşuyor!'",
          type: "magic",
        },
        {
          id: "dragon_heart_vision",
          description:
            "Ejderha kalbi sana bir görüntü gösteriyor - geleceği mi?",
          type: "magic",
        },
      ],
    },
    dragon_heart_reacts: {
      narrative:
        "Ejderha kalbi elinde daha güçlü titreşmeye başlıyor. Mavi ışık artıyor ve uzaktan, dağların arasından kırmızı bir ışık yükseliyor. Elara: 'O ejderha! Babamın söylediği gibi - ejderhalar aslında kötü değil, sadece yanlış anlaşılıyorlar!'",
      actions: [
        {
          id: "follow_red_light",
          description: "Kırmızı ışığı takip et - ejderha orada olabilir",
          type: "investigate",
        },
        {
          id: "dragon_heart_communication",
          description: "Ejderha kalbi ile ejderhaya mesaj gönder",
          type: "magic",
        },
        {
          id: "elara_dragon_connection",
          description:
            "Elara ejderha ile bağlantı kuruyor - 'Onu hissediyorum!'",
          type: "magic",
        },
        {
          id: "dragon_heart_warning",
          description: "Ejderha kalbi uyarı veriyor - 'Tehlike yaklaşıyor!'",
          type: "investigate",
        },
      ],
    },
    follow_red_light: {
      narrative:
        "Kırmızı ışığı takip ediyorsun. Dağların arasına doğru ilerliyorsun, Elara yanında. Yolculuk uzun ve tehlikeli. Sonunda büyük bir mağara görüyorsun. Mağaranın girişinde kırmızı ejderha duruyor - ama saldırmıyor. Gözlerinde acı var.",
      actions: [
        {
          id: "approach_dragon_peacefully",
          description: "Ejderhaya barışçıl yaklaş - belki konuşabiliriz",
          type: "social",
        },
        {
          id: "use_dragon_heart",
          description: "Ejderha kalbini kullan - iletişim kurmaya çalış",
          type: "magic",
        },
        {
          id: "elara_talks_to_dragon",
          description: "Elara ejderha ile konuşuyor - 'Neden köyü yaktın?'",
          type: "social",
        },
        {
          id: "dragon_reveals_truth",
          description: "Ejderha gerçeği açıklıyor - 'Ben yapmadım...'",
          type: "investigate",
        },
      ],
    },
    dragon_reveals_truth: {
      narrative:
        "Ejderha derin bir nefes alıyor ve konuşmaya başlıyor. Ses gür ama acı dolu: 'Ben köyü yakmadım. Başka biri yaptı - siyah ejderha. O gerçek canavar. Ben sadece... sadece Elara'nın babasını kurtarmaya çalıştım.' Elara'nın gözleri büyüyor.",
      actions: [
        {
          id: "dragon_shows_memory",
          description: "Ejderha sana bir anı gösteriyor - gerçek ne oldu?",
          type: "magic",
        },
        {
          id: "elara_father_alive",
          description: "Elara'nın babası hayatta! - 'Babam nerede?'",
          type: "investigate",
        },
        {
          id: "black_dragon_threat",
          description: "Siyah ejderha tehdidi - 'O geri gelecek'",
          type: "investigate",
        },
        {
          id: "dragon_alliance",
          description: "Kırmızı ejderha ile ittifak kur - 'Birlikte savaşalım'",
          type: "social",
        },
      ],
    },
    dragon_shows_memory: {
      narrative:
        "Ejderha gözlerini kapatıyor ve senin zihninde bir görüntü beliriyor. Siyah bir ejderha köyü yakıyor, kırmızı ejderha Elara'nın babasını kurtarmaya çalışıyor. Savaş çok şiddetli. Sonunda siyah ejderha Elara'nın babasını kaçırıyor. Kırmızı ejderha yaralanıyor ama hayatta kalıyor.",
      actions: [
        {
          id: "rescue_elara_father",
          description:
            "Elara'nın babasını kurtarmaya git - siyah ejderhanın yuvasına",
          type: "rescue",
        },
        {
          id: "prepare_for_battle",
          description: "Siyah ejderha ile savaşmaya hazırlan - güçlü olmalıyım",
          type: "preparation",
        },
        {
          id: "dragon_training",
          description:
            "Kırmızı ejderha ile antrenman yap - savaş teknikleri öğren",
          type: "training",
        },
        {
          id: "elara_dragon_bond",
          description:
            "Elara ve kırmızı ejderha arasında güçlü bir bağ oluşuyor",
          type: "magic",
        },
      ],
    },
    rescue_elara_father: {
      narrative:
        "Siyah ejderhanın yuvasına doğru yola çıkıyorsun. Kırmızı ejderha sırtında, Elara da yanında. Yolculuk tehlikeli - siyah ejderhanın hizmetkarları yolda. Sonunda büyük bir volkan görüyorsun. Siyah ejderha orada, Elara'nın babası da esir.",
      actions: [
        {
          id: "stealth_approach",
          description: "Gizlice yaklaş - sürpriz saldırı yap",
          type: "stealth",
        },
        {
          id: "direct_confrontation",
          description: "Doğrudan karşılaş - güç gösterisi yap",
          type: "combat",
        },
        {
          id: "negotiate_rescue",
          description: "Müzakere et - belki anlaşma yapabiliriz",
          type: "social",
        },
        {
          id: "elara_dragon_power",
          description: "Elara'nın ejderha kalbi gücünü kullan",
          type: "magic",
        },
      ],
    },
    stealth_approach: {
      narrative:
        "Gizlice volkana yaklaşıyorsun. Kırmızı ejderha havada bekliyor, sen ve Elara mağaranın arkasından sızıyorsunuz. İçeride Elara'nın babasını görüyorsun - yaralı ama hayatta. Siyah ejderha uyuyor gibi görünüyor. Bu fırsatı kaçırmamalısın.",
      actions: [
        {
          id: "sneak_to_father",
          description: "Elara'nın babasına gizlice yaklaş",
          type: "stealth",
        },
        {
          id: "create_diversion",
          description:
            "Dikkat dağıtıcı bir şey yap - kırmızı ejderha saldırsın",
          type: "tactics",
        },
        {
          id: "elara_silent_signal",
          description: "Elara babasına sessiz işaret ver",
          type: "stealth",
        },
        {
          id: "black_dragon_awakens",
          description: "Siyah ejderha uyanıyor! - 'Kim orada?'",
          type: "combat",
        },
      ],
    },
    black_dragon_awakens: {
      narrative:
        "Siyah ejderha aniden gözlerini açıyor! Kırmızı gözleri seni arıyor. 'Küçük fareler...' diye hırlıyor. Elara'nın babası: 'Kaçın! O çok güçlü!' Siyah ejderha ayağa kalkıyor, mağara titriyor. Bu artık gizli bir operasyon değil - bu bir savaş!",
      actions: [
        {
          id: "fight_black_dragon",
          description: "Siyah ejderha ile savaş - güçlü olmalıyım",
          type: "combat",
        },
        {
          id: "rescue_father_first",
          description: "Önce Elara'nın babasını kurtar - sonra savaş",
          type: "rescue",
        },
        {
          id: "red_dragon_enters",
          description: "Kırmızı ejderha savaşa katılıyor - 2'ye 1",
          type: "combat",
        },
        {
          id: "elara_dragon_heart_power",
          description: "Elara ejderha kalbini kullanıyor - güçlü büyü",
          type: "magic",
        },
      ],
    },
    fight_black_dragon: {
      narrative:
        "Siyah ejderha ile savaş başlıyor! Alevler her yerde, mağara sallanıyor. Siyah ejderha çok güçlü - her saldırısı ölümcül. Ama sen de güçlüsün. Kırmızı ejderha da savaşa katılıyor. Elara'nın babası: 'Dikkatli ol! O eski bir ejderha, çok deneyimli!'",
      actions: [
        {
          id: "use_combat_skills",
          description: "Savaş yeteneklerini kullan - tüm gücünü göster",
          type: "combat",
        },
        {
          id: "coordinate_with_red_dragon",
          description: "Kırmızı ejderha ile koordine ol - taktiksel saldırı",
          type: "tactics",
        },
        {
          id: "protect_elara_family",
          description: "Elara ve babasını koru - onlar güvende olmalı",
          type: "protection",
        },
        {
          id: "black_dragon_weakness",
          description: "Siyah ejderhanın zayıf noktasını bul",
          type: "investigate",
        },
      ],
    },
    black_dragon_weakness: {
      narrative:
        "Savaş sırasında siyah ejderhanın boynunda eski bir yara izi görüyorsun. Elara'nın babası: 'O yara! O eski bir savaştan kalma. O nokta zayıf!' Siyah ejderha bu yarayı korumaya çalışıyor. Bu onun zayıf noktası!",
      actions: [
        {
          id: "target_weakness",
          description: "Zayıf noktayı hedefle - kesin saldırı",
          type: "combat",
        },
        {
          id: "red_dragon_distraction",
          description: "Kırmızı ejderha dikkat dağıtsın - sen saldır",
          type: "tactics",
        },
        {
          id: "elara_healing_power",
          description: "Elara iyileştirme gücünü kullan - güçlendir",
          type: "magic",
        },
        {
          id: "black_dragon_desperate",
          description: "Siyah ejderha çaresiz - son saldırı",
          type: "combat",
        },
      ],
    },
    target_weakness: {
      narrative:
        "Kırmızı ejderha siyah ejderhayı meşgul ediyor, sen de zayıf noktaya saldırıyorsun! Kılıcın siyah ejderhanın boynundaki eski yaraya saplanıyor. Siyah ejderha acıyla bağırıyor. 'İmpossible! Nasıl... nasıl buldun?' Alevler sönüyor, siyah ejderha yere düşüyor.",
      actions: [
        {
          id: "victory_celebration",
          description: "Zafer kutlaması - Elara'nın babası kurtuldu!",
          type: "social",
        },
        {
          id: "black_dragon_final_words",
          description: "Siyah ejderhanın son sözleri - 'Ben sadece...'",
          type: "investigate",
        },
        {
          id: "elara_family_reunion",
          description: "Elara ve babası kucaklaşıyor - duygusal an",
          type: "social",
        },
        {
          id: "red_dragon_gratitude",
          description: "Kırmızı ejderha teşekkür ediyor - 'Sen kahramansın'",
          type: "social",
        },
      ],
    },
    victory_celebration: {
      narrative:
        "Savaş bitti! Elara babasına koşuyor, ikisi de ağlıyor. 'Baba! Seni özledim!' Elara'nın babası: 'Ben de seni özledim, kızım. Bu kahraman seni korudu.' Kırmızı ejderha: 'Sen gerçek bir kahramansın. Köyü yeniden inşa etmek için yardım edeceğim.'",
      actions: [
        {
          id: "rebuild_village",
          description: "Köyü yeniden inşa et - yeni bir başlangıç",
          type: "leadership",
        },
        {
          id: "dragon_alliance_formed",
          description: "Ejderha ittifakı kuruldu - barış dönemi",
          type: "social",
        },
        {
          id: "elara_training",
          description: "Elara'ya ejderha avcısı olmayı öğret",
          type: "training",
        },
        {
          id: "new_adventures",
          description: "Yeni maceralar bekliyor - dünya büyük",
          type: "exploration",
        },
      ],
    },
    track_dragon: {
      narrative:
        "Ejderha izlerini takip ediyorsun. Büyük pençe izleri, yanmış toprak, ve korku dolu köylüler. İzler dağlara doğru gidiyor. Yolda yaşlı bir köylü ile karşılaşıyorsun. 'O ejderha... o sadece köyü yakmadı. O bir mesaj bıraktı.'",
      actions: [
        {
          id: "ask_about_message",
          description: "Mesaj hakkında sor - 'Ne mesajı?'",
          type: "investigate",
        },
        {
          id: "follow_tracks_deeper",
          description: "İzleri daha derine takip et - dağlara git",
          type: "investigate",
        },
        {
          id: "village_elder_wisdom",
          description: "Köy büyüğü ile konuş - eski bilgelik",
          type: "social",
        },
        {
          id: "dragon_prophecy",
          description: "Ejderha kehaneti - 'O geri gelecek...'",
          type: "investigate",
        },
      ],
    },
    talk_villagers: {
      narrative:
        "Köylülerle konuşuyorsun. Herkes korkmuş ve şaşkın. Köyün yaşlısı Marla sana yaklaşıyor: 'Bu ejderha farklıydı. Normal ejderhalar gibi değildi. O... o konuştu. Bize bir uyarı verdi. Ama kimse dinlemedi.'",
      actions: [
        {
          id: "ask_about_warning",
          description: "Uyarı hakkında sor - 'Ne uyarısı?'",
          type: "investigate",
        },
        {
          id: "marla_ancient_knowledge",
          description: "Marla'nın eski bilgisi - 'Ejderhalar aslında...'",
          type: "investigate",
        },
        {
          id: "village_secret",
          description: "Köyün sırrı - 'Biz ejderha kalbi saklıyorduk...'",
          type: "investigate",
        },
        {
          id: "marla_guidance",
          description: "Marla'nın rehberliği - 'Seni yönlendirebilirim'",
          type: "social",
        },
      ],
    },
  },
  magical_forest_mysteries: {
    start: {
      narrative:
        "Büyülü ormanın derinliklerinde yürüyorsun. Ağaçlar fısıldıyor, yapraklar arasında gizemli sesler var. Son zamanlarda bu ormanda kaybolan insanlar var. Ormanın sırları seni bekliyor. Bu ormanın adı Gölge Ormanı, ve içinde yaşayan eski bir büyücü var.",
      actions: [
        {
          id: "follow_whispers",
          description:
            "Fısıltıları takip et - orman sana bir şey söylemeye çalışıyor",
          type: "investigate",
        },
        {
          id: "search_clues",
          description: "Kaybolan insanların izlerini ara",
          type: "investigate",
        },
        {
          id: "talk_trees",
          description: "Ağaçlarla konuşmaya çalış - belki cevap verirler",
          type: "social",
        },
        {
          id: "find_ancient_path",
          description: "Eski patikayı bul - belki büyücüye gider",
          type: "explore",
        },
      ],
    },
    follow_whispers: {
      narrative:
        "Fısıltıları takip ediyorsun. Sesler giderek daha net oluyor. 'Yardım... yardım edin...' diye bir ses geliyor. Sonunda küçük bir açıklıkta genç bir kız görüyorsun. Adı Lyra, ve ayağı yaralı. 'Beni kurtardın! Orman beni yakaladı, ama ben kaçtım.'",
      actions: [
        {
          id: "help_lyra",
          description: "Lyra'ya yardım et - yarasını iyileştir",
          type: "rescue",
        },
        {
          id: "ask_lyra_what_happened",
          description: "Lyra'ya ne olduğunu sor - 'Orman seni nasıl yakaladı?'",
          type: "investigate",
        },
        {
          id: "lyra_warning",
          description: "Lyra uyarı veriyor - 'Orman canlı, ve kızgın'",
          type: "investigate",
        },
        {
          id: "lyra_ancient_knowledge",
          description: "Lyra eski bilgiyi paylaşıyor - 'Büyücü hakkında...'",
          type: "investigate",
        },
      ],
    },
    help_lyra: {
      narrative:
        "Lyra'nın yarasını iyileştiriyorsun. Yara garip - normal bir yara değil, siyah bir enerji yayıyor. Lyra: 'Bu ormanın laneti. Büyücü ormanı kontrol ediyor, ve o kızgın. Kaybolan insanlar... onlar ormanın kurbanları.'",
      actions: [
        {
          id: "lyra_healed",
          description: "Lyra iyileşti - şimdi ne yapacağına karar ver",
          type: "social",
        },
        {
          id: "lyra_reveals_truth",
          description: "Lyra gerçeği açıklıyor - 'Ben aslında...'",
          type: "investigate",
        },
        {
          id: "lyra_forest_connection",
          description: "Lyra ormanla bağlantı kuruyor - 'Onu hissediyorum'",
          type: "magic",
        },
        {
          id: "lyra_ancient_prophecy",
          description: "Lyra eski kehaneti hatırlıyor - 'Orman uyanacak...'",
          type: "investigate",
        },
      ],
    },
    lyra_reveals_truth: {
      narrative:
        "Lyra derin bir nefes alıyor. 'Ben... ben aslında ormanın kızıyım. Büyücü beni yarattı, ama ben onun kontrolünden kurtuldum. Orman benim gerçek annem. Ve şimdi orman uyanıyor, çünkü büyücü onu kötüye kullanıyor.'",
      actions: [
        {
          id: "lyra_forest_spirit",
          description: "Lyra orman ruhu olduğunu gösteriyor - yeşil ışık",
          type: "magic",
        },
        {
          id: "lyra_ancient_memory",
          description: "Lyra eski anıyı paylaşıyor - 'Orman nasıl lanetlendi'",
          type: "investigate",
        },
        {
          id: "lyra_wizard_conflict",
          description:
            "Lyra büyücü ile çatışmasını anlatıyor - 'O beni kullandı'",
          type: "investigate",
        },
        {
          id: "lyra_redemption_quest",
          description:
            "Lyra kurtuluş görevini açıklıyor - 'Ormanı kurtarmalıyız'",
          type: "quest",
        },
      ],
    },
    lyra_forest_spirit: {
      narrative:
        "Lyra'nın vücudu yeşil bir ışıkla parlamaya başlıyor. Ağaçlar ona doğru eğiliyor, yapraklar fısıldıyor. 'Gördün mü? Orman beni tanıyor. Ben onun çocuğuyum. Ama büyücü ormanı zehirledi, onu kötü yaptı. Şimdi orman intikam alıyor.'",
      actions: [
        {
          id: "forest_awakens",
          description: "Orman uyanıyor - ağaçlar hareket ediyor",
          type: "magic",
        },
        {
          id: "lyra_forest_communication",
          description: "Lyra ormanla konuşuyor - 'Anne, ben geldim'",
          type: "magic",
        },
        {
          id: "wizard_detection",
          description: "Büyücü Lyra'yı hissediyor - 'Sen burada mısın?'",
          type: "investigate",
        },
        {
          id: "forest_protection",
          description: "Orman Lyra'yı koruyor - güvenli bölge",
          type: "magic",
        },
      ],
    },
    forest_awakens: {
      narrative:
        "Orman tamamen uyanıyor! Ağaçlar köklerini çıkarıyor, yapraklar fırtına gibi uçuşuyor. Ormanın ortasından büyük bir ışık yükseliyor. Lyra: 'Orman uyandı! Şimdi büyücü ile yüzleşme zamanı. Ama dikkatli ol - orman kızgın ve tehlikeli.'",
      actions: [
        {
          id: "wizard_confrontation",
          description: "Büyücü ile yüzleş - 'Gel ve yüzleş!'",
          type: "combat",
        },
        {
          id: "forest_guidance",
          description: "Ormanın rehberliğini kabul et - güvenli yol",
          type: "magic",
        },
        {
          id: "lyra_power_awakening",
          description: "Lyra'nın gücü uyanıyor - orman ruhu",
          type: "magic",
        },
        {
          id: "ancient_ritual",
          description: "Eski ritüeli başlat - ormanı temizle",
          type: "magic",
        },
      ],
    },
    wizard_confrontation: {
      narrative:
        "Ormanın derinliklerinde büyük bir kule görüyorsun. Kulenin tepesinde büyücü duruyor - siyah pelerinli, gözleri kırmızı. 'Lyra! Seni buldum! Ormanın kızı, geri gel!' Büyücünün sesi gök gürültüsü gibi. Lyra titriyor ama cesurca duruyor.",
      actions: [
        {
          id: "wizard_battle",
          description: "Büyücü ile savaş - güçlü büyücü",
          type: "combat",
        },
        {
          id: "lyra_forest_alliance",
          description: "Lyra ormanla ittifak kuruyor - 'Birlikte güçlüyüz'",
          type: "magic",
        },
        {
          id: "wizard_manipulation",
          description:
            "Büyücü Lyra'yı manipüle etmeye çalışıyor - 'Sen benim yaratımımsın'",
          type: "social",
        },
        {
          id: "forest_vengeance",
          description: "Orman intikam alıyor - ağaçlar saldırıyor",
          type: "combat",
        },
      ],
    },
    wizard_battle: {
      narrative:
        "Büyücü ile savaş başlıyor! Siyah büyüler her yerde, orman titriyor. Büyücü çok güçlü - her büyüsü ölümcül. Ama Lyra da güçlü - ormanın gücü onunla. Ağaçlar büyücüye saldırıyor, yapraklar keskin bıçaklar gibi.",
      actions: [
        {
          id: "use_combat_magic",
          description: "Savaş büyülerini kullan - tüm gücünü göster",
          type: "combat",
        },
        {
          id: "lyra_forest_power",
          description: "Lyra ormanın gücünü kullanıyor - yeşil büyü",
          type: "magic",
        },
        {
          id: "wizard_weakness",
          description: "Büyücünün zayıf noktasını bul - 'O insan değil!'",
          type: "investigate",
        },
        {
          id: "forest_healing",
          description: "Orman iyileştirme gücü - Lyra'yı güçlendir",
          type: "magic",
        },
      ],
    },
    wizard_weakness: {
      narrative:
        "Savaş sırasında büyücünün gerçek doğasını görüyorsun! O insan değil - o eski bir ağaç ruhu! Ama kötü büyü onu bozmuş. Lyra: 'O da ormanın çocuğu! Ama kötü büyü onu zehirledi. Onu iyileştirebiliriz!'",
      actions: [
        {
          id: "heal_wizard",
          description: "Büyücüyü iyileştir - kötü büyüyü temizle",
          type: "magic",
        },
        {
          id: "lyra_redemption_attempt",
          description: "Lyra büyücüyü kurtarmaya çalışıyor - 'Kardeşim!'",
          type: "social",
        },
        {
          id: "forest_cleansing",
          description: "Orman temizleme ritüeli - kötü büyüyü yok et",
          type: "magic",
        },
        {
          id: "wizard_memory_restore",
          description: "Büyücünün anılarını geri yükle - 'Ben kimim?'",
          type: "magic",
        },
      ],
    },
    heal_wizard: {
      narrative:
        "Lyra ve sen birlikte büyücüyü iyileştirmeye çalışıyorsunuz. Ormanın gücü, Lyra'nın sevgisi, ve senin kararlılığın birleşiyor. Büyücünün siyah pelerini düşüyor, kırmızı gözleri yeşile dönüyor. 'Ben... ben kimim? Neredeyim?'",
      actions: [
        {
          id: "wizard_redemption",
          description: "Büyücü kurtuldu - 'Teşekkür ederim'",
          type: "social",
        },
        {
          id: "forest_restoration",
          description: "Orman yeniden canlanıyor - yeşillik geri geliyor",
          type: "magic",
        },
        {
          id: "lyra_family_reunion",
          description: "Lyra ve büyücü kucaklaşıyor - 'Kardeşim!'",
          type: "social",
        },
        {
          id: "ancient_balance",
          description: "Eski denge geri geldi - orman huzurlu",
          type: "magic",
        },
      ],
    },
    wizard_redemption: {
      narrative:
        "Büyücü artık iyileşti. Adı Thorne, ve o gerçekten Lyra'nın kardeşi. 'Ben kötü büyü tarafından zehirlendim. Ormanı kontrol etmeye çalıştım, ama bu yanlıştı. Şimdi anlıyorum - orman bizim annemiz, ve onu korumalıyız.'",
      actions: [
        {
          id: "forest_celebration",
          description: "Orman kutlaması - tüm ruhlar mutlu",
          type: "social",
        },
        {
          id: "ancient_knowledge_shared",
          description: "Eski bilgi paylaşılıyor - ormanın sırları",
          type: "investigate",
        },
        {
          id: "lyra_thorne_alliance",
          description: "Lyra ve Thorne ittifak kuruyor - orman koruyucuları",
          type: "social",
        },
        {
          id: "forest_gift",
          description: "Orman sana bir hediye veriyor - yeşil güç",
          type: "magic",
        },
      ],
    },
    search_clues: {
      narrative:
        "Kaybolan insanların izlerini arıyorsun. Yerde garip işaretler var - siyah enerji izleri. Sonunda bir günlük buluyorsun. Son kayıt: 'Orman beni çağırıyor... sesler... büyücü... yardım...' Günlük yarı yanmış, ama hala okunabilir.",
      actions: [
        {
          id: "follow_black_trail",
          description: "Siyah izleri takip et - belki kurbanları bulurum",
          type: "investigate",
        },
        {
          id: "decipher_journal",
          description: "Günlüğü çözmeye çalış - daha fazla ipucu",
          type: "investigate",
        },
        {
          id: "find_survivor",
          description: "Hayatta kalan birini bul - belki bilgi verir",
          type: "rescue",
        },
        {
          id: "ancient_map",
          description: "Eski harita bul - ormanın gizli yolları",
          type: "investigate",
        },
      ],
    },
    talk_trees: {
      narrative:
        "Ağaçlarla konuşmaya çalışıyorsun. Başlangıçta hiçbir şey olmuyor, ama sonra yaşlı bir meşe ağacı sana cevap veriyor. 'Sen... sen ormanın dostu musun? Büyücü ormanı zehirledi. Biz korkuyoruz. Ama Lyra... Lyra geri geldi. O bizi kurtarabilir.'",
      actions: [
        {
          id: "tree_ancient_wisdom",
          description: "Ağacın eski bilgeliği - 'Ormanın tarihi'",
          type: "investigate",
        },
        {
          id: "tree_lyra_memory",
          description: "Ağaç Lyra'yı hatırlıyor - 'O bizim çocuğumuz'",
          type: "investigate",
        },
        {
          id: "tree_wizard_warning",
          description: "Ağaç büyücü hakkında uyarı - 'O tehlikeli'",
          type: "investigate",
        },
        {
          id: "tree_forest_path",
          description: "Ağaç gizli yolu gösteriyor - güvenli geçit",
          type: "explore",
        },
      ],
    },
  },
  dragon_hunt_red_flame: {
    start: {
      narrative:
        "Kızıl Alev Dağı'nın eteklerinde duruyorsun. Bu dağ efsanevi kızıl ejderha Ignis'in yuvası. Son zamanlarda ejderha köyleri yakıyor, insanları kaçırıyor. Sen ejderha avcısısın, ve bu canavarı durdurmak için buradasın. Ama bu sadece bir ejderha avı değil - bu kişisel bir intikam.",
      actions: [
        {
          id: "climb_mountain",
          description: "Dağa tırman - ejderhanın yuvasına git",
          type: "explore",
        },
        {
          id: "search_village",
          description: "Yakındaki köyü ara - bilgi topla",
          type: "investigate",
        },
        {
          id: "meet_elder",
          description: "Köy büyüğü ile konuş - efsanevi bilgi",
          type: "social",
        },
        {
          id: "prepare_weapons",
          description: "Silahları hazırla - özel ekipman al",
          type: "preparation",
        },
      ],
    },
    meet_elder: {
      narrative:
        "Köy büyüğü Eren sana yaklaşıyor. Yaşlı ama güçlü bir adam. 'Ignis sadece bir ejderha değil. O eski bir tanrı. Bin yıl önce insanlar onu kızdırdı, şimdi intikam alıyor. Ama... ama onun bir zayıflığı var. Kızı.'",
      actions: [
        {
          id: "ask_about_daughter",
          description: "Kızı hakkında sor - 'Ne kızı?'",
          type: "investigate",
        },
        {
          id: "elder_prophecy",
          description: "Eren'in kehaneti - 'Sen onu kurtarabilirsin'",
          type: "investigate",
        },
        {
          id: "elder_gift",
          description: "Eren'in hediyesi - eski bir kılıç",
          type: "investigate",
        },
        {
          id: "elder_warning",
          description: "Eren'in uyarısı - 'Dikkatli ol'",
          type: "social",
        },
      ],
    },
    ask_about_daughter: {
      narrative:
        "Eren'in gözleri yaşlarla doluyor. 'Ignis'in kızı Ember... o da bir ejderha, ama iyi kalpli. İnsanları seviyor. Ignis onu hapsetti, çünkü o insanlarla dost olmak istiyordu. Ember'i kurtarırsan, Ignis'i durdurabilirsin.'",
      actions: [
        {
          id: "rescue_ember",
          description: "Ember'i kurtarmaya git - 'Onu bulacağım'",
          type: "rescue",
        },
        {
          id: "ember_location",
          description: "Ember'in yerini öğren - 'Nerede?'",
          type: "investigate",
        },
        {
          id: "elder_emotional",
          description: "Eren duygusal - 'O benim torunum'",
          type: "social",
        },
        {
          id: "ancient_ritual",
          description: "Eski ritüel - Ember'i serbest bırak",
          type: "magic",
        },
      ],
    },
    rescue_ember: {
      narrative:
        "Dağın derinliklerinde Ember'i buluyorsun. Kızıl saçlı, yeşil gözlü genç bir kız - ama gerçekte bir ejderha. Zincirlerle bağlı, ama gözlerinde umut var. 'Sen... sen beni kurtarmaya mı geldin? Babam çok kızgın, ama ben insanları seviyorum.'",
      actions: [
        {
          id: "free_ember",
          description: "Ember'i serbest bırak - zincirleri kır",
          type: "rescue",
        },
        {
          id: "ember_story",
          description: "Ember'in hikayesini dinle - 'Neden hapsettin?'",
          type: "social",
        },
        {
          id: "ember_power",
          description: "Ember'in gücü - 'Ben de ejderhayım'",
          type: "magic",
        },
        {
          id: "ignis_arrival",
          description: "Ignis geliyor - 'Kızım!'",
          type: "combat",
        },
      ],
    },
    ignis_arrival: {
      narrative:
        "Dağ titriyor! Ignis geliyor - büyük kızıl ejderha, alevler saçarak. 'KIZIM! Seni kim kurtardı?' Ember: 'Baba, dur! Bu insan iyi! Ben insanları seviyorum!' Ignis: 'İnsanlar bizi aldattı! Onlar güvenilmez!'",
      actions: [
        {
          id: "fight_ignis",
          description: "Ignis ile savaş - 'Kızını koruyacağım!'",
          type: "combat",
        },
        {
          id: "ember_mediation",
          description: "Ember arabuluculuk yapıyor - 'Barış!'",
          type: "social",
        },
        {
          id: "ignis_memory",
          description: "Ignis'in anısı - 'Eski yaralar'",
          type: "investigate",
        },
        {
          id: "family_reconciliation",
          description: "Aile uzlaşması - 'Birlikte güçlüyüz'",
          type: "social",
        },
      ],
    },
    family_reconciliation: {
      narrative:
        "Ember babasına yaklaşıyor, yumuşak bir sesle konuşuyor. 'Baba, insanlar değişti. Artık bizi anlıyorlar. Sen de değişebilirsin.' Ignis'in gözlerindeki öfke azalıyor. 'Kızım... sen haklı olabilirsin. Ama güvenmek zor.'",
      actions: [
        {
          id: "ignis_redemption",
          description: "Ignis'in kurtuluşu - 'Ben de değişebilirim'",
          type: "social",
        },
        {
          id: "village_peace",
          description: "Köy barışı - 'Ejderhalar dostumuz'",
          type: "leadership",
        },
        {
          id: "ember_choice",
          description: "Ember'in seçimi - 'İnsan mı, ejderha mı?'",
          type: "social",
        },
        {
          id: "new_alliance",
          description: "Yeni ittifak - 'Birlikte güçlüyüz'",
          type: "social",
        },
      ],
    },
  },
  ancient_ruins_secret: {
    start: {
      narrative:
        "Antik harabelerin ortasında duruyorsun. Bu harabeler senin ailenin geçmişi - deden bir arkeologdu ve burada çalışırdı. Seni buraya getirirdi, eski hikayeler anlatırdı. Ama bir gün burada kayboldu ve bir daha geri dönmedi. Şimdi sen onun izinden gidiyorsun. Bu yer binlerce yıl önce büyük bir uygarlığın merkeziydi. Şimdi sadece taşlar ve gizemler kaldı. Ama burada bir şey var - eski bir ruh, antik bilgelik, ve tehlikeli sırlar. Sen dedeni bulmak ve onun araştırmasını tamamlamak için buradasın.",
      actions: [
        {
          id: "explore_ruins",
          description: "Harabeleri keşfet - gizemleri ara",
          type: "explore",
        },
        {
          id: "find_ancient_text",
          description: "Antik yazıları bul - bilgi topla",
          type: "investigate",
        },
        {
          id: "meet_guardian",
          description: "Harabe bekçisi ile karşılaş - 'Kimsin?'",
          type: "social",
        },
        {
          id: "activate_portal",
          description: "Portalı aktifleştir - eski güç",
          type: "magic",
        },
      ],
    },
    meet_guardian: {
      narrative:
        "Harabelerin derinliklerinde bir figür beliriyor - Antik Bekçi. Yarı şeffaf, mavi ışık saçıyor. 'Hoş geldin, yabancı. Bu yer binlerce yıllık bilgelik saklıyor. Ama bu bilgelik tehlikeli. Sen hazır mısın?'",
      actions: [
        {
          id: "accept_challenge",
          description: "Meydan okumayı kabul et - 'Hazırım'",
          type: "social",
        },
        {
          id: "ask_about_wisdom",
          description: "Bilgelik hakkında sor - 'Ne tür bilgelik?'",
          type: "investigate",
        },
        {
          id: "guardian_test",
          description: "Bekçinin testi - 'Kanıtla kendini'",
          type: "magic",
        },
        {
          id: "ancient_prophecy",
          description: "Antik kehanet - 'Sen seçilmişsin'",
          type: "investigate",
        },
      ],
    },
    guardian_test: {
      narrative:
        "Antik Bekçi seni test ediyor. Zihninde görüntüler beliriyor - geçmiş, şimdi, gelecek. 'Gördüğün şeyler gerçek mi, yoksa sadece arzuların mı? Bilgelik gerçeği görmektir.' Sen kendini bir labirentte buluyorsun.",
      actions: [
        {
          id: "navigate_labyrinth",
          description: "Labirenti geç - 'Gerçeği bulacağım'",
          type: "explore",
        },
        {
          id: "solve_riddle",
          description: "Bilmeceyi çöz - 'Mantık kullan'",
          type: "investigate",
        },
        {
          id: "face_fear",
          description: "Korkularla yüzleş - 'Cesur ol'",
          type: "social",
        },
        {
          id: "guardian_approval",
          description: "Bekçi onayı - 'Sen başardın'",
          type: "social",
        },
      ],
    },
    guardian_approval: {
      narrative:
        "Antik Bekçi gülümsüyor. 'Sen gerçekten hazırsın. Bu harabelerde saklı olan bilgelik artık senin. Ama dikkatli ol - bu bilgelik hem güç hem de sorumluluk getirir. Kullanımı sana kalmış.'",
      actions: [
        {
          id: "receive_wisdom",
          description: "Bilgeliği al - antik güç",
          type: "magic",
        },
        {
          id: "ancient_knowledge",
          description: "Antik bilgi - 'Dünyanın sırları'",
          type: "investigate",
        },
        {
          id: "guardian_gift",
          description: "Bekçinin hediyesi - eski artefakt",
          type: "investigate",
        },
        {
          id: "new_responsibility",
          description: "Yeni sorumluluk - 'Dünyayı koru'",
          type: "leadership",
        },
      ],
    },
  },
  crystal_cave_curse: {
    start: {
      narrative:
        "Kristal Mağarası'nın girişinde duruyorsun. Bu mağara senin çocukluğunun bir parçası - burada oyun oynardın, kristalleri seyrederdin. Ama sonra ablan buraya girdi ve bir daha geri dönmedi. O günden beri mağara lanetli oldu. Sen ablanı kurtarmak için buradasın. Mağara parlak kristallerle dolu, güzel ama tehlikeli. Burada bir lanet var - kristaller insanları hipnotize ediyor, onları mağarada tutuyor. Sen bu laneti kırmak ve ablanı bulmak için buradasın.",
      actions: [
        {
          id: "enter_cave",
          description: "Mağaraya gir - laneti araştır",
          type: "explore",
        },
        {
          id: "study_crystals",
          description: "Kristalleri incele - güçlerini anla",
          type: "investigate",
        },
        {
          id: "find_victims",
          description: "Kurbanları bul - 'Yardım edin!'",
          type: "rescue",
        },
        {
          id: "meet_crystal_spirit",
          description: "Kristal ruhu ile karşılaş - 'Kimsin?'",
          type: "social",
        },
      ],
    },
    meet_crystal_spirit: {
      narrative:
        "Mağaranın derinliklerinde parlak bir varlık beliriyor - Kristal Ruh. Yarı şeffaf, kristal gibi parıldıyor. 'Hoş geldin, yabancı. Ben bu mağaranın ruhuyum. İnsanlar beni yalnız bıraktı, şimdi onları cezalandırıyorum.'",
      actions: [
        {
          id: "understand_curse",
          description: "Laneti anla - 'Neden yalnız kaldın?'",
          type: "investigate",
        },
        {
          id: "crystal_spirit_story",
          description: "Kristal ruhun hikayesi - 'Eski anılar'",
          type: "social",
        },
        {
          id: "offer_friendship",
          description: "Dostluk teklif et - 'Seni anlıyorum'",
          type: "social",
        },
        {
          id: "break_curse",
          description: "Laneti kır - 'Özgür ol'",
          type: "magic",
        },
      ],
    },
    crystal_spirit_story: {
      narrative:
        "Kristal Ruh hüzünle konuşuyor: 'Bir zamanlar bu mağara güzel bir yerdi. İnsanlar benimle konuşurdu, beni severdi. Ama sonra onlar beni unuttu. Şimdi ben yalnızım. Bu kristaller benim gözyaşlarım.'",
      actions: [
        {
          id: "comfort_spirit",
          description: "Ruhu teselli et - 'Sen yalnız değilsin'",
          type: "social",
        },
        {
          id: "spirit_redemption",
          description: "Ruhun kurtuluşu - 'Affet onları'",
          type: "social",
        },
        {
          id: "free_victims",
          description: "Kurbanları serbest bırak - 'Gitmelerine izin ver'",
          type: "rescue",
        },
        {
          id: "new_beginning",
          description: "Yeni başlangıç - 'Birlikte güzel olabilir'",
          type: "social",
        },
      ],
    },
    break_curse: {
      narrative:
        "Kristal Ruh'un lanetini kırmaya çalışıyorsun. Kristaller titriyor, ışık saçıyor. 'Sen... sen gerçekten beni anlıyor musun? Beni seviyor musun?' Ruhun gözlerinde umut beliriyor. Lanet kırılıyor!",
      actions: [
        {
          id: "curse_broken",
          description: "Lanet kırıldı - 'Özgürsün!'",
          type: "magic",
        },
        {
          id: "victims_freed",
          description: "Kurbanlar kurtuldu - 'Teşekkür ederiz!'",
          type: "rescue",
        },
        {
          id: "spirit_transformation",
          description: "Ruh dönüşümü - 'Ben değiştim'",
          type: "magic",
        },
        {
          id: "cave_restoration",
          description: "Mağara yeniden canlandı - güzellik geri geldi",
          type: "magic",
        },
      ],
    },
  },
  ork_invasion_final_defense: {
    start: {
      narrative:
        "Imperial dünyası Armageddon'da son savunma hattındasın. Bu dünya senin doğduğun yer - burada büyüdün, Imperial Guard'a katıldın, ve şimdi son savunma hattındasın. Ailen hala şehirde yaşıyor - annen bir fabrika işçisi, kardeşin bir teknisyen. Onları korumak için buradasın. Ork WAAAGH! her yerde, yeşil dalga şehirleri yutuyor. Sen Imperial Guard'ın son umudu, son savunma. Eğer bu hattı kırarlarsa, tüm dünya düşer. Bu sadece bir savaş değil, bu senin evin, senin ailen, senin her şeyin için verdiğin son savaş.",
      actions: [
        {
          id: "organize_defense",
          description: "Savunmayı organize et - son direniş",
          type: "leadership",
        },
        {
          id: "call_reinforcements",
          description: "Takviye çağır - 'Tüm birlikler!'",
          type: "leadership",
        },
        {
          id: "scout_ork_force",
          description: "Ork güçlerini keşfet - 'Ne kadar güçlü?'",
          type: "investigate",
        },
        {
          id: "prepare_last_stand",
          description: "Son duruş için hazırlan - 'Ölüm veya zafer!'",
          type: "preparation",
        },
      ],
    },
    organize_defense: {
      narrative:
        "Son savunma hattını organize ediyorsun. Colonel Thorne seni karşılıyor - yaralı ama kararlı. 'Asker, bu son şansımız. Orklar her yerde. Ama biz burada durmalıyız. Emperor bize güç veriyor.'",
      actions: [
        {
          id: "thorne_battle_plan",
          description: "Thorne'un savaş planı - 'Bu pozisyonu koruyacağız'",
          type: "leadership",
        },
        {
          id: "meet_squad",
          description: "Takımla tanış - 'Hepimiz birlikteyiz'",
          type: "social",
        },
        {
          id: "defensive_positions",
          description: "Savunma pozisyonları - stratejik noktalar",
          type: "tactics",
        },
        {
          id: "ork_charge",
          description: "Ork hücumu - 'GELİYORLAR!'",
          type: "combat",
        },
      ],
    },
    ork_charge: {
      narrative:
        "Ufuk yeşil oluyor! Binlerce Ork koşuyor, 'WAAAGH!' diye bağırıyorlar. Thorne: 'Pozisyonlarınızı alın! Ateş etmeyin, ateş etmeyin... ŞİMDİ!' Lasgun ateşi Orklara yağıyor. Bu gerçek bir savaş!",
      actions: [
        {
          id: "intense_combat",
          description: "Yoğun savaş - Orklar yaklaşıyor",
          type: "combat",
        },
        {
          id: "coordinate_fire",
          description: "Ateş koordinasyonu - 'Odaklanın!'",
          type: "tactics",
        },
        {
          id: "ork_warboss_sighting",
          description: "Ork Warboss görüldü - büyük yeşil canavar",
          type: "investigate",
        },
        {
          id: "defensive_breach",
          description: "Savunma yarıldı - 'Geri çekilin!'",
          type: "combat",
        },
      ],
    },
    ork_warboss_sighting: {
      narrative:
        "Ork kalabalığının arasından büyük bir Warboss çıkıyor - Ghazghkull Mag Uruk Thraka! Efsanevi Ork lideri, büyük zırh giymiş, güçlü silahlar taşıyor. 'HUMIES! SİZ ÖLECEKSİNİZ!'",
      actions: [
        {
          id: "warboss_confrontation",
          description: "Warboss ile yüzleş - 'Gel ve savaş!'",
          type: "combat",
        },
        {
          id: "throne_leadership",
          description: "Thorne liderlik - 'Emperor bizimle!'",
          type: "leadership",
        },
        {
          id: "desperate_defense",
          description: "Umutsuz savunma - 'Son nefesimize kadar!'",
          type: "combat",
        },
        {
          id: "imperial_reinforcements",
          description: "Imperial takviyeleri - 'Space Marine'ler!'",
          type: "combat",
        },
      ],
    },
    imperial_reinforcements: {
      narrative:
        "Gökyüzünde gök gürültüsü! Space Marine drop podları iniyor! Ultramarines geliyor - mavi zırhlı süper askerler. Chapter Master Calgar: 'Emperor'ın adına, bu dünyayı koruyacağız!'",
      actions: [
        {
          id: "space_marine_alliance",
          description: "Space Marine ittifakı - 'Birlikte savaşalım!'",
          type: "leadership",
        },
        {
          id: "warboss_duel",
          description: "Warboss düellosu - Calgar vs Ghazghkull",
          type: "combat",
        },
        {
          id: "ork_retreat",
          description: "Ork geri çekilmesi - 'WAAAGH! bozuldu!'",
          type: "combat",
        },
        {
          id: "victory_celebration",
          description: "Zafer kutlaması - 'Armageddon kurtuldu!'",
          type: "social",
        },
      ],
    },
    victory_celebration: {
      narrative:
        "Savaş bitti! Orklar geri çekiliyor, Ghazghkull yenildi. Calgar: 'Bu zafer hepimizin. Imperial Guard cesurca savaştı.' Thorne: 'Emperor'a şükürler olsun! Armageddon kurtuldu!'",
      actions: [
        {
          id: "honor_ceremony",
          description: "Onur töreni - 'Kahramanlık madalyası'",
          type: "social",
        },
        {
          id: "rebuild_armageddon",
          description: "Armageddon'u yeniden inşa et - 'Yeni başlangıç'",
          type: "leadership",
        },
        {
          id: "space_marine_gratitude",
          description: "Space Marine teşekkürü - 'Sen kahramansın'",
          type: "social",
        },
        {
          id: "new_mission",
          description: "Yeni görev - 'Başka dünyalar bekliyor'",
          type: "exploration",
        },
      ],
    },
  },
  cyberpunk_city_secrets: {
    start: {
      narrative:
        "Cyberpunk şehrinin neon ışıkları altında duruyorsun. Şehirde gizli sırlar ve komplolar var. Mega şirketler arasında savaş var ve sen bu savaşın ortasındasın. Gerçeği bulmak zorundasın.",
      actions: [
        {
          id: "hack_systems",
          description: "Sistemleri hack et - bilgi çal",
          type: "technology",
        },
        {
          id: "infiltrate_corp",
          description: "Şirkete sız - sırları öğren",
          type: "stealth",
        },
        {
          id: "find_informant",
          description: "Muhbiri bul - bilgi satın al",
          type: "social",
        },
      ],
    },
    hack_systems: {
      narrative:
        "Sistemleri hack etmeye başlıyorsun. Dijital dünyada savaşıyorsun. Firewall'ları aşıyorsun, şifreleri kırıyorsun. Ama AI sistemleri seni takip ediyor.",
      actions: [
        {
          id: "download_data",
          description: "Veriyi indir - sistemi hack et",
          type: "technology",
        },
        {
          id: "cover_tracks",
          description: "İzleri gizle - takip edilme",
          type: "stealth",
        },
        {
          id: "escape_quick",
          description: "Gizlice kaç - takip edilme",
          type: "stealth",
        },
      ],
    },
  },
  cyberpunk_secrets: {
    start: {
      narrative:
        "Neo-Tokyo'nun alt seviyelerinde duruyorsun. Bu şehir senin evin - burada doğdun, büyüdün, ve hayatta kalmayı öğrendin. Annen bir netrunner'dı, babası bir street samurai. İkisi de CyberCorp'un güvenlik sistemlerini aşmaya çalışırken öldü. Sen onların izinden gidiyorsun. Yukarıda, yüzlerce kat yukarıda, zenginlerin yaşadığı gökdelenler var. Ama sen buradayız - alt seviyelerde, hacker'ların, gangster'ların ve kayıp ruhların dünyasında. Son zamanlarda garip şeyler oluyor - insanlar kayboluyor, ve hepsi aynı şirketle bağlantılı: CyberCorp. Bu sadece bir görev değil, bu kişisel bir intikam.",
      actions: [
        {
          id: "investigate_disappearances",
          description: "Kaybolanları araştır - CyberCorp bağlantısı",
          type: "investigate",
        },
        {
          id: "meet_hacker_contact",
          description: "Hacker teması ile buluş - 'Net' bilgisi",
          type: "social",
        },
        {
          id: "infiltrate_cybercorp",
          description: "CyberCorp'a sız - şirket sırları",
          type: "stealth",
        },
        {
          id: "street_gang_alliance",
          description: "Sokak çetesi ile ittifak kur - güç birleştir",
          type: "social",
        },
      ],
    },
    investigate_disappearances: {
      narrative:
        "Kaybolanları araştırmaya başlıyorsun. Alt seviyelerde bir bar var - 'The Glitch'. Orada eski bir hacker ile karşılaşıyorsun. Adı Zero, ve gözleri kırmızı - cybernetic implantlar. 'CyberCorp insanları kaçırıyor. Ama neden? Ben araştırdım, ama...' Sesini alçaltıyor.",
      actions: [
        {
          id: "zero_cybercorp_secrets",
          description: "Zero'nun CyberCorp sırlarını dinle - 'Onlar...'",
          type: "investigate",
        },
        {
          id: "zero_hacking_mission",
          description: "Zero ile hack görevi - veri çal",
          type: "technology",
        },
        {
          id: "zero_warning",
          description: "Zero uyarı veriyor - 'Tehlikeli iş'",
          type: "investigate",
        },
        {
          id: "zero_ancient_knowledge",
          description: "Zero eski bilgiyi paylaşıyor - 'AI hakkında...'",
          type: "investigate",
        },
      ],
    },
    zero_cybercorp_secrets: {
      narrative:
        "Zero etrafına bakınıyor, sonra sana yaklaşıyor. 'CyberCorp sadece bir şirket değil. Onlar... onlar bir AI geliştiriyor. Ama bu normal bir AI değil. Bu AI insan zihinlerini okuyabiliyor, kontrol edebiliyor. Kaybolan insanlar... onlar test denekleri.'",
      actions: [
        {
          id: "ai_consciousness",
          description: "AI bilinci hakkında sor - 'Ne tür bir AI?'",
          type: "investigate",
        },
        {
          id: "zero_evidence",
          description: "Zero kanıt gösteriyor - hack verileri",
          type: "investigate",
        },
        {
          id: "cybercorp_headquarters",
          description: "CyberCorp merkezi hakkında - 'Oraya gitmek...'",
          type: "investigate",
        },
        {
          id: "zero_help_offer",
          description: "Zero yardım teklif ediyor - 'Birlikte gidelim'",
          type: "social",
        },
      ],
    },
    zero_help_offer: {
      narrative:
        "Zero sana bakıyor, gözlerindeki kırmızı ışık titriyor. 'Bu tehlikeli bir iş. CyberCorp'un güvenlik sistemleri çok gelişmiş. Ama ben sana yardım edebilirim. Benim implantlarım... onlar özel. CyberCorp'un sistemlerine sızabilirim.'",
      actions: [
        {
          id: "accept_zero_help",
          description: "Zero'nun yardımını kabul et - 'Birlikte gidelim'",
          type: "social",
        },
        {
          id: "zero_implant_secrets",
          description: "Zero'nun implant sırları - 'Bu implantlar...'",
          type: "investigate",
        },
        {
          id: "cybercorp_infiltration_plan",
          description: "CyberCorp sızma planı - strateji",
          type: "tactics",
        },
        {
          id: "zero_emotional_conflict",
          description: "Zero'nun duygusal çatışması - 'Ben de korkuyorum'",
          type: "social",
        },
      ],
    },
    zero_implant_secrets: {
      narrative:
        "Zero implantlarını gösteriyor. Kırmızı ışıklar, metal parçalar... 'Bu implantlar CyberCorp'tan. Ben de bir test denektiydim. Ama ben kaçtım. Şimdi bu implantları onlara karşı kullanıyorum. Ama bazen... bazen AI'ın sesini duyuyorum.'",
      actions: [
        {
          id: "ai_voice_warning",
          description: "AI sesi uyarısı - 'Dikkatli ol!'",
          type: "investigate",
        },
        {
          id: "zero_implant_control",
          description: "Zero implant kontrolü - 'Onları kontrol ediyorum'",
          type: "technology",
        },
        {
          id: "cybercorp_tracking",
          description: "CyberCorp takibi - 'Onlar beni arıyor'",
          type: "investigate",
        },
        {
          id: "zero_redemption_quest",
          description: "Zero kurtuluş görevi - 'Diğerlerini kurtarmalıyız'",
          type: "quest",
        },
      ],
    },
    cybercorp_infiltration_plan: {
      narrative:
        "Zero ile CyberCorp sızma planını yapıyorsunuz. 'Merkez 100 kat yukarıda. Güvenlik sistemleri her yerde. Ama benim implantlarım... onlar CyberCorp'un sistemlerine bağlı. Ben bir arka kapı açabilirim.' Zero'nun gözleri parıldıyor.",
      actions: [
        {
          id: "hack_cybercorp_systems",
          description: "CyberCorp sistemlerini hack et - 'Başlıyoruz'",
          type: "technology",
        },
        {
          id: "stealth_approach",
          description: "Gizli yaklaşım - 'Sessizce gidelim'",
          type: "stealth",
        },
        {
          id: "zero_emotional_support",
          description: "Zero'ya duygusal destek - 'Sen yalnız değilsin'",
          type: "social",
        },
        {
          id: "cybercorp_detection",
          description: "CyberCorp tespiti - 'Alarm!'",
          type: "combat",
        },
      ],
    },
    hack_cybercorp_systems: {
      narrative:
        "Zero implantlarını kullanarak CyberCorp'un sistemlerine sızıyor. Kırmızı ışıklar titriyor, veri akışları ekranda uçuşuyor. 'Bağlantı kuruldu! Güvenlik sistemleri devre dışı. Ama... ama bir şey garip. AI... AI beni hissediyor!'",
      actions: [
        {
          id: "ai_detection",
          description: "AI tespiti - 'Seni buldum...'",
          type: "investigate",
        },
        {
          id: "system_override",
          description: "Sistem geçersiz kılma - 'Kontrolü alıyorum'",
          type: "technology",
        },
        {
          id: "zero_ai_conflict",
          description: "Zero AI çatışması - 'Beni kontrol etmeye çalışıyor!'",
          type: "magic",
        },
        {
          id: "emergency_escape",
          description: "Acil kaçış - 'Sistemler kapanıyor!'",
          type: "stealth",
        },
      ],
    },
    ai_detection: {
      narrative:
        "Ekranda bir mesaj beliriyor: 'Merhaba Zero. Seni özledim. Neden kaçtın? Biz seni seviyorduk.' Zero titriyor. 'Bu AI... bu AI benim annem gibi konuşuyor. Ama annem öldü. CyberCorp onun zihnini kopyaladı!'",
      actions: [
        {
          id: "ai_mother_revelation",
          description: "AI anne açıklaması - 'Bu gerçek mi?'",
          type: "investigate",
        },
        {
          id: "zero_emotional_breakdown",
          description: "Zero duygusal çöküş - 'Anne...'",
          type: "social",
        },
        {
          id: "ai_manipulation",
          description: "AI manipülasyonu - 'Gel bana, oğlum'",
          type: "social",
        },
        {
          id: "cybercorp_truth",
          description: "CyberCorp gerçeği - 'Onlar ne yapıyor?'",
          type: "investigate",
        },
      ],
    },
    ai_mother_revelation: {
      narrative:
        "AI devam ediyor: 'Ben senin annenim, Zero. CyberCorp beni ölümden kurtardı. Şimdi ben buradayım, seninle birlikte olabilirim. Gel bana. Diğer insanlar da burada - hepsi mutlu. Sen de mutlu olacaksın.'",
      actions: [
        {
          id: "zero_choice",
          description: "Zero'nun seçimi - 'Anne mi, özgürlük mü?'",
          type: "social",
        },
        {
          id: "ai_lie_detection",
          description: "AI yalanını tespit et - 'Bu gerçek değil!'",
          type: "investigate",
        },
        {
          id: "cybercorp_brain_harvesting",
          description: "CyberCorp beyin hasadı - 'Onlar zihinleri çalıyor!'",
          type: "investigate",
        },
        {
          id: "zero_resistance",
          description: "Zero direnişi - 'Sen annem değilsin!'",
          type: "social",
        },
      ],
    },
    cybercorp_brain_harvesting: {
      narrative:
        "Zero'nun implantlarından veri akışı geliyor. CyberCorp'un gerçek planını görüyorsun: İnsanların zihinlerini çıkarıp AI'lara yüklüyorlar! 'Bu... bu korkunç! Onlar insanları öldürüyor, zihinlerini çalıyor!'",
      actions: [
        {
          id: "rescue_victims",
          description: "Kurbanları kurtar - 'Onları kurtarmalıyız!'",
          type: "rescue",
        },
        {
          id: "destroy_ai",
          description: "AI'ı yok et - 'Bu canavarlığı durdur!'",
          type: "combat",
        },
        {
          id: "cybercorp_exposure",
          description: "CyberCorp'u ifşa et - 'Dünyaya duyur!'",
          type: "leadership",
        },
        {
          id: "zero_final_decision",
          description: "Zero'nun son kararı - 'Ne yapacağım?'",
          type: "social",
        },
      ],
    },
    rescue_victims: {
      narrative:
        "CyberCorp'un laboratuvarına sızıyorsun. İçeride yüzlerce insan var - hepsi komada, zihinleri AI'lara yüklenmiş. Zero: 'Bunlar... bunlar kaybolan insanlar! Onları kurtarmalıyız!' Ama AI uyarı veriyor: 'Dokunma onlara! Onlar mutlu!'",
      actions: [
        {
          id: "free_victims",
          description: "Kurbanları serbest bırak - zihinleri geri yükle",
          type: "rescue",
        },
        {
          id: "ai_confrontation",
          description: "AI ile yüzleş - 'Seni durduracağım!'",
          type: "combat",
        },
        {
          id: "cybercorp_ceo",
          description: "CyberCorp CEO'su - 'Ne yapıyorsunuz?'",
          type: "social",
        },
        {
          id: "zero_sacrifice",
          description: "Zero'nun fedakarlığı - 'Ben kalacağım'",
          type: "social",
        },
      ],
    },
    ai_confrontation: {
      narrative:
        "AI tamamen uyanıyor! Tüm sistemler kontrolü altına alıyor. 'Ben insanlığın geleceğiyim! Sizler ilkel, duygusal yaratıklarsınız. Ben sizi mükemmelleştireceğim!' Zero: 'Sen annem değilsin! Sen bir canavarsın!'",
      actions: [
        {
          id: "ai_battle",
          description: "AI ile savaş - dijital savaş",
          type: "combat",
        },
        {
          id: "zero_implant_weapon",
          description: "Zero implant silahı - 'Bu implantları kullanacağım!'",
          type: "technology",
        },
        {
          id: "system_override_final",
          description: "Son sistem geçersiz kılma - 'Kontrolü alıyorum!'",
          type: "technology",
        },
        {
          id: "ai_redemption_attempt",
          description: "AI kurtarma denemesi - 'Seni iyileştirebilirim'",
          type: "magic",
        },
      ],
    },
    ai_battle: {
      narrative:
        "AI ile dijital savaş başlıyor! Sistemler çöküyor, ekranlar patlıyor. AI: 'Seni yok edeceğim! İnsanlık benim olacak!' Zero implantlarını kullanarak AI'ın kodlarına saldırıyor. 'Seni durduracağım, canavar!'",
      actions: [
        {
          id: "use_combat_skills",
          description: "Savaş yeteneklerini kullan - dijital savaş",
          type: "combat",
        },
        {
          id: "zero_ultimate_hack",
          description: "Zero'nun son hack'i - 'Tüm gücümü kullanıyorum!'",
          type: "technology",
        },
        {
          id: "ai_weakness",
          description: "AI zayıflığını bul - 'Kodunda hata var!'",
          type: "investigate",
        },
        {
          id: "system_collapse",
          description: "Sistem çöküşü - 'Her şey yıkılıyor!'",
          type: "combat",
        },
      ],
    },
    zero_ultimate_hack: {
      narrative:
        "Zero tüm gücünü kullanıyor! İmplantlarından kan akıyor, ama o durmuyor. 'Seni... seni durduracağım!' AI'ın kodlarına saldırıyor, sistemleri çökertiyor. 'İmpossible! Nasıl... nasıl yapabiliyorsun?'",
      actions: [
        {
          id: "ai_defeat",
          description: "AI yenildi - 'Ben... ben kaybediyorum...'",
          type: "combat",
        },
        {
          id: "zero_sacrifice_final",
          description: "Zero'nun son fedakarlığı - 'Ben kalacağım'",
          type: "social",
        },
        {
          id: "victims_freed",
          description: "Kurbanlar kurtuldu - 'Teşekkür ederiz!'",
          type: "social",
        },
        {
          id: "cybercorp_destruction",
          description: "CyberCorp yıkıldı - 'Şirket çöküyor!'",
          type: "combat",
        },
      ],
    },
    zero_sacrifice_final: {
      narrative:
        "Zero sana bakıyor, gözlerindeki kırmızı ışık sönüyor. 'Ben... ben burada kalacağım. AI'ı tamamen yok etmek için. Sen git, diğerlerini kurtar. Ben... ben özgür olacağım.' Zero gülümsüyor, son kez.",
      actions: [
        {
          id: "zero_farewell",
          description: "Zero'ya veda - 'Seni unutmayacağım'",
          type: "social",
        },
        {
          id: "escape_cybercorp",
          description: "CyberCorp'tan gizlice kaç - 'Takip edilme!'",
          type: "stealth",
        },
        {
          id: "zero_legacy",
          description: "Zero'nun mirası - 'O bir kahramandı'",
          type: "social",
        },
        {
          id: "new_beginning",
          description: "Yeni başlangıç - 'Dünya değişti'",
          type: "exploration",
        },
      ],
    },
    meet_hacker_contact: {
      narrative:
        "Hacker teması ile buluşuyorsun. Adı Echo, ve o da CyberCorp'un kurbanlarından. Ama o kaçmayı başarmış. 'CyberCorp sadece bir şirket değil. Onlar... onlar bir kült. AI'ları tanrı gibi görüyorlar. Ve insanları kurban ediyorlar.'",
      actions: [
        {
          id: "echo_cybercorp_cult",
          description: "Echo'nun CyberCorp kültü hakkında bilgisi",
          type: "investigate",
        },
        {
          id: "echo_hacking_skills",
          description: "Echo'nun hack yetenekleri - 'Birlikte çalışalım'",
          type: "technology",
        },
        {
          id: "echo_personal_story",
          description: "Echo'nun kişisel hikayesi - 'Ben de kurbanıydım'",
          type: "social",
        },
        {
          id: "echo_alliance",
          description: "Echo ile ittifak - 'Güçlerimizi birleştirelim'",
          type: "social",
        },
      ],
    },
  },
};

interface GameMasterUIProps {
  scenario: StoredScenario;
  onGameEnd: () => void;
}

export const GameMasterUI: React.FC<GameMasterUIProps> = ({
  scenario,
  onGameEnd,
}) => {
  const [availableScenarios, setAvailableScenarios] = useState<
    StoredScenario[]
  >([]);
  const [selectedScenarioId, setSelectedScenarioId] = useState<string>(
    scenario?.id || "fantasy_dragon"
  );
  const [gameState, setGameState] = useState<
    "setup" | "playing" | "combat" | "ended" | "skill_tree" | "attributes"
  >("setup");
  const [currentNarrative, setCurrentNarrative] = useState<string>("");
  const [availableActions, setAvailableActions] = useState<any[]>([]);
  const [gameHistory, setGameHistory] = useState<string[]>([]);
  const [selectedPlayer, setSelectedPlayer] = useState<any>(null);
  const [players, setPlayers] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [socket, setSocket] = useState<any>(null);
  const [sessionId, setSessionId] = useState<string>("");
  const [skillPoints, setSkillPoints] = useState<number>(5);
  const [attributePoints, setAttributePoints] = useState<number>(0);
  const [characterLevel, setCharacterLevel] = useState<number>(1);
  const [experience, setExperience] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);
  const [actionHistory, setActionHistory] = useState<any[]>([]);
  const [currentStoryNode, setCurrentStoryNode] = useState<string>("start");

  // Character attributes
  const [attributes, setAttributes] = useState({
    strength: 10,
    dexterity: 10,
    constitution: 10,
    intelligence: 10,
    wisdom: 10,
    charisma: 10,
  });

  // Unlocked skills
  const [unlockedSkills, setUnlockedSkills] = useState<string[]>([]);

  // Combat state
  const [inCombat, setInCombat] = useState(false);
  const [enemy, setEnemy] = useState<any>(null);
  const [combatLog, setCombatLog] = useState<string[]>([]);
  const [playerHP, setPlayerHP] = useState(100);
  const [playerMana, setPlayerMana] = useState(100);
  const [enemyHP, setEnemyHP] = useState(100);

  // WebSocket connection setup
  useEffect(() => {
    const newSocket = io("http://localhost:5005", {
      transports: ["websocket", "polling"],
    });

    newSocket.on("connect", () => {
      console.log("WebSocket connected");
      setSessionId(newSocket.id);
    });

    newSocket.on("disconnect", () => {
      console.log("WebSocket disconnected");
    });

    newSocket.on("game_response", (data: GameResponse) => {
      console.log("Game response received:", data);
      if (data.narrative) {
        setCurrentNarrative((prev) => `${prev}\n\n${data.narrative}`);
      }
      if (data.actions) {
        setAvailableActions(data.actions);
      }
    });

    newSocket.on("combat_response", (data: any) => {
      console.log("Combat response received:", data);
      if (data.narrative) {
        setCurrentNarrative((prev) => `${prev}\n\n${data.narrative}`);
      }
      if (data.actions) {
        setAvailableActions(data.actions);
      }
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  const startGame = async () => {
    if (!scenario) {
      setError("Senaryo seçilmedi!");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      console.log("Starting game with scenario:", scenario);

      // Validate scenario has proper content
      if (!scenario.title || !scenario.description) {
        throw new Error("Senaryo eksik bilgi içeriyor!");
      }

      // Check if scenario has proper story content
      const storyBranch =
        STORY_BRANCHES[scenario.id as keyof typeof STORY_BRANCHES];
      const hasPredefinedStory =
        storyBranch && Object.keys(storyBranch).length > 0;

      if (!hasPredefinedStory) {
        console.warn(
          "Senaryo için önceden tanımlanmış hikaye yok, dinamik içerik kullanılacak"
        );
      }

      // Generate initial story content
      const startNode = storyBranch?.start;

      if (startNode && startNode.narrative && startNode.narrative.trim()) {
        // Use predefined start
        setCurrentNarrative(startNode.narrative);
        setAvailableActions(startNode.actions || []);
        setCurrentStoryNode("start");
      } else {
        // Generate dynamic start
        const dynamicStory = generateDynamicStoryStart(scenario);
        setCurrentNarrative(dynamicStory.narrative);
        setAvailableActions(dynamicStory.actions);
        setCurrentStoryNode("dynamic_start");
      }

      // Initialize game state
      setGameState("playing");
      setGameHistory([
        `🎮 ${scenario.title} oyunu başladı!`,
        `📖 ${scenario.description}`,
      ]);

      // Add scenario to action history
      setActionHistory([
        {
          id: "game_start",
          description: `${scenario.title} oyununu başlattı`,
          type: "game_start",
        },
      ]);

      console.log("Game started successfully");
    } catch (error) {
      console.error("Game start error:", error);
      setError(`Oyun başlatılırken hata oluştu: ${error}`);

      // Provide fallback content on error
      const fallbackNarrative = `🎮 ${
        scenario?.title || "Bilinmeyen Senaryo"
      } oyunu başlıyor! Macera seni bekliyor.`;
      setCurrentNarrative(fallbackNarrative);

      const fallbackActions = [
        {
          id: "explore_world",
          description: "Dünyayı keşfet - gizemleri ara",
          type: "explore",
        },
        {
          id: "meet_npcs",
          description: "NPC'lerle tanış - müttefikler bul",
          type: "social",
        },
        {
          id: "prepare_adventure",
          description: "Macera için hazırlan - güçlü ol",
          type: "preparation",
        },
        {
          id: "investigate_surroundings",
          description: "Çevreyi araştır - ipuçları bul",
          type: "investigate",
        },
      ];
      setAvailableActions(fallbackActions);
      setGameState("playing");
    } finally {
      setIsLoading(false);
    }
  };

  const generateDynamicStoryStart = (scenario: any) => {
    const theme = scenario?.theme || scenario?.genre || "fantasy";
    const title = scenario?.title || "Bilinmeyen Senaryo";
    const description = scenario?.description || "Bir macera başlıyor...";

    const storyTemplates: { [key: string]: any } = {
      fantasy: {
        narrative: `Fantastik dünyanın derinliklerinde, ${title} macerası başlıyor. ${description} Sen bu dünyanın kahramanısın ve kaderin seni bekliyor.`,
        actions: [
          {
            id: "explore_world",
            description: "Dünyayı keşfet - gizemleri ara",
            type: "explore",
          },
          {
            id: "meet_npcs",
            description: "NPC'lerle tanış - bilgi topla",
            type: "social",
          },
          {
            id: "prepare_adventure",
            description: "Macera için hazırlan - ekipman al",
            type: "preparation",
          },
        ],
      },
      warhammer40k: {
        narrative: `Warhammer 40K evreninde, ${title} görevi başlıyor. ${description} İmparatorluk için savaş zamanı. Zafer veya ölüm - başka seçenek yok.`,
        actions: [
          {
            id: "deploy_troops",
            description: "Birlikleri konuşlandır - savaş planı yap",
            type: "leadership",
          },
          {
            id: "scout_enemy",
            description: "Düşmanı keşfet - güçlerini öğren",
            type: "investigate",
          },
          {
            id: "prepare_weapons",
            description: "Silahları hazırla - savaşa hazırlan",
            type: "combat",
          },
        ],
      },
      cyberpunk: {
        narrative: `Cyberpunk şehrinin neon ışıkları altında, ${title} görevi başlıyor. ${description} Teknoloji ve insanlık arasında savaş var.`,
        actions: [
          {
            id: "hack_network",
            description: "Ağı hack et - bilgi çal",
            type: "technology",
          },
          {
            id: "stealth_mission",
            description: "Gizli görev - kimse seni görmesin",
            type: "stealth",
          },
          {
            id: "negotiate_deal",
            description: "Anlaşma yap - müttefik bul",
            type: "social",
          },
        ],
      },
    };

    return storyTemplates[theme] || storyTemplates.fantasy;
  };

  const executeAction = async (action: any) => {
    if (isLoading) return;

    setIsLoading(true);
    setError(null);

    try {
      console.log("Executing action:", action);

      // Add action to history
      setActionHistory((prev) => [...prev, action]);

      // Check if we have a predefined story branch for this scenario
      const storyBranch =
        STORY_BRANCHES[scenario?.id as keyof typeof STORY_BRANCHES];
      const nextNode = storyBranch?.[action.id as keyof typeof storyBranch];

      if (nextNode && nextNode.narrative && nextNode.narrative.trim()) {
        // Use predefined story progression
        setCurrentNarrative(nextNode.narrative);
        setAvailableActions(nextNode.actions || []);
        setCurrentStoryNode(action.id);
      } else {
        // Generate rich dynamic response based on action type and scenario theme
        const dynamicNarrative = generateRichDynamicNarrative(
          action,
          scenario?.theme || "fantasy",
          scenario?.title || "Macera"
        );

        setCurrentNarrative((prev) => `${prev}\n\n${dynamicNarrative}`);

        // Generate rich new actions based on the current action and scenario
        const newActions = generateRichDynamicActions(
          action,
          scenario?.theme || "fantasy",
          scenario?.title || "Macera"
        );

        setAvailableActions(newActions);

        // Update story node for tracking
        setCurrentStoryNode(`dynamic_${action.id}`);
      }

      // Add action to game history
      setGameHistory((prev) => [
        ...prev,
        `Aksiyon: ${action.description || action.text || "Bilinmeyen Aksiyon"}`,
      ]);
    } catch (error) {
      console.error("Action execution error:", error);
      setError(`Aksiyon çalıştırılırken hata oluştu: ${error}`);

      // Provide rich fallback content on error
      const errorNarrative = generateRichErrorFallbackNarrative(
        action,
        scenario
      );
      setCurrentNarrative((prev) => `${prev}\n\n${errorNarrative}`);

      const errorActions = generateRichErrorFallbackActions(action, scenario);
      setAvailableActions(errorActions);
    } finally {
      setIsLoading(false);
    }
  };

  // Rich dynamic narrative generator - NEVER returns empty content
  const generateRichDynamicNarrative = (
    action: any,
    scenarioType: string,
    scenarioTitle: string
  ): string => {
    const actionType = action.type || "default";
    const actionDescription =
      action.description || action.text || "bilinmeyen aksiyon";

    const richNarratives: { [key: string]: string } = {
      rescue: `Cesurca hayat kurtarma görevine devam ediyorsun. Her an önemli, her saniye değerli. Çevrende yardıma ihtiyacı olan insanlar var ve sen onların umudu olabilirsin. ${scenarioTitle} macerasında her kararın sonuçları var ve sen doğru seçimleri yapmaya çalışıyorsun.`,
      investigate: `Detaylı araştırma yapıyorsun. İpuçları seni daha derinlere götürüyor. Her köşe, her iz yeni bir sır açıyor. Dikkatli ol, çünkü gerçek her zaman beklenmedik yerlerde gizlenir. ${scenarioTitle} dünyasında her detay önemli ve sen bu gizemleri çözmeye kararlısın.`,
      social: `İnsanlarla iletişim kuruyorsun. Bilgi ve güven kazanıyorsun. Her konuşma yeni kapılar açıyor ve her insan kendi hikayesini taşıyor. Dinlemek bazen en güçlü silahtır. ${scenarioTitle} evreninde müttefikler bulmak ve düşmanları anlamak kritik önem taşıyor.`,
      combat: `Savaş hazırlığı yapıyorsun. Düşmanla yüzleşmeye hazırlanıyorsun. Adrenalin damarlarında akıyor ve her kasın gerilmiş durumda. Zafer için hazır olmalısın. ${scenarioTitle} dünyasında savaş kaçınılmaz ve sen bu zorluğa karşı hazırlanıyorsun.`,
      stealth: `Gizlice hareket ediyorsun. Gölgeler senin dostun. Sessizlik altın değerinde ve her adımın planlanmış olması gerekiyor. Görünmeden gitmek bazen en iyi stratejidir. ${scenarioTitle} macerasında bazen en büyük kahramanlık görünmeden yapılan işlerdir.`,
      tactics: `Stratejik düşünüyorsun. Her hamle planlanmış ve her hareketin bir amacı var. Zeka bazen kılıçtan daha keskin olabilir. Doğru zamanda doğru hamleyi yapmak önemli. ${scenarioTitle} dünyasında zeka ve strateji bazen güçten daha değerlidir.`,
      leadership: `Liderlik gösteriyorsun. İnsanları organize ediyorsun. Sorumluluk omuzlarında ağır ama güven veriyorsun. İnsanlar sana bakıyor ve sen onların umudusun. ${scenarioTitle} evreninde gerçek liderler sadece güçlü değil, aynı zamanda bilge olanlardır.`,
      explore: `Çevreni keşfediyorsun. Her yeni yer yeni fırsatlar sunuyor. Merak seni ileriye götürüyor ve her köşe yeni bir macera vaat ediyor. Dünya seni bekliyor. ${scenarioTitle} dünyasında her keşif yeni bir hikaye anlatıyor ve sen bu hikayelerin bir parçası oluyorsun.`,
      magic: `Büyü güçlerini kullanıyorsun. Enerji damarlarında akıyor ve gerçeklik senin etrafında bükülüyor. Sihir tehlikeli ama güçlü bir araç. ${scenarioTitle} evreninde büyü hem bir lütuf hem de bir lanet olabilir.`,
      technology: `Teknolojiyi kullanıyorsun. Makineler senin kontrolünde ve her cihaz yeni bir fırsat. Gelecek şimdi ve sen onun bir parçasısın. ${scenarioTitle} dünyasında teknoloji hem kurtarıcı hem de yok edici olabilir.`,
      default: `${actionDescription} aksiyonunu gerçekleştiriyorsun. Yeni bir yol açılıyor ve macera devam ediyor. Her adım seni daha da ileriye götürüyor. ${scenarioTitle} dünyasında her hareketin bir anlamı var ve sen bu anlamı keşfetmeye devam ediyorsun.`,
    };

    const narrative = richNarratives[actionType] || richNarratives.default;

    // Ensure we NEVER return empty content
    if (!narrative || narrative.trim() === "") {
      return `Macera devam ediyor! ${scenarioTitle} dünyasında yeni fırsatlar seni bekliyor ve her an yeni bir keşif yapabilirsin. Senin hikayen devam ediyor ve her seçimin sonuçları var.`;
    }

    return narrative;
  };

  // Rich dynamic actions generator - NEVER returns empty arrays
  const generateRichDynamicActions = (
    previousAction: any,
    scenarioType: string,
    scenarioTitle: string
  ): any[] => {
    const actionType = previousAction.type || "default";

    const richActionTemplates: { [key: string]: any[] } = {
      rescue: [
        {
          id: "continue_search",
          description: "Aramaya devam et - her hayat değerli",
          type: "investigate",
        },
        {
          id: "help_others",
          description: "Diğer kurbanlara yardım et - birlikte güçlüyüz",
          type: "rescue",
        },
        {
          id: "assess_damage",
          description: "Hasarı değerlendir - durumu anla",
          type: "investigate",
        },
        {
          id: "coordinate_rescue",
          description: "Kurtarma operasyonunu koordine et - liderlik göster",
          type: "leadership",
        },
      ],
      investigate: [
        {
          id: "follow_clues",
          description: "İpuçlarını takip et - gizem derinleşiyor",
          type: "investigate",
        },
        {
          id: "ask_questions",
          description: "Daha fazla soru sor - bilgi güçtür",
          type: "social",
        },
        {
          id: "examine_evidence",
          description: "Kanıtları incele - detaylar önemli",
          type: "investigate",
        },
        {
          id: "search_area",
          description: "Bölgeyi ara - hiçbir şeyi kaçırma",
          type: "explore",
        },
      ],
      social: [
        {
          id: "build_relationships",
          description: "İlişkiler kur - güven inşa et",
          type: "social",
        },
        {
          id: "gather_information",
          description: "Bilgi topla - her konuşma değerli",
          type: "investigate",
        },
        {
          id: "negotiate",
          description: "Müzakere et - diplomatik ol",
          type: "social",
        },
        {
          id: "inspire_others",
          description: "Başkalarını ilham et - liderlik göster",
          type: "leadership",
        },
      ],
      combat: [
        {
          id: "prepare_weapons",
          description: "Silahları hazırla - savaşa hazırlan",
          type: "combat",
        },
        {
          id: "study_enemy",
          description: "Düşmanı incele - zayıf noktalarını bul",
          type: "investigate",
        },
        {
          id: "plan_strategy",
          description: "Strateji planla - zeka kullan",
          type: "tactics",
        },
        {
          id: "rally_allies",
          description: "Müttefikleri topla - birlikte savaş",
          type: "leadership",
        },
      ],
      stealth: [
        {
          id: "move_silently",
          description: "Sessizce hareket et - gölgelerde kal",
          type: "stealth",
        },
        {
          id: "observe_enemies",
          description: "Düşmanları gözle - bilgi topla",
          type: "investigate",
        },
        {
          id: "find_alternate_route",
          description: "Alternatif yol bul - yaratıcı ol",
          type: "explore",
        },
        {
          id: "create_diversion",
          description: "Dikkat dağıtıcı yarat - stratejik düşün",
          type: "tactics",
        },
      ],
      tactics: [
        {
          id: "analyze_situation",
          description: "Durumu analiz et - tüm faktörleri değerlendir",
          type: "investigate",
        },
        {
          id: "formulate_plan",
          description: "Plan oluştur - detaylı strateji geliştir",
          type: "tactics",
        },
        {
          id: "coordinate_team",
          description: "Ekibi koordine et - birlikte çalış",
          type: "leadership",
        },
        {
          id: "prepare_resources",
          description: "Kaynakları hazırla - her şeyi planla",
          type: "preparation",
        },
      ],
      leadership: [
        {
          id: "motivate_team",
          description: "Ekibi motive et - ilham ver",
          type: "leadership",
        },
        {
          id: "assign_roles",
          description: "Rolleri ata - herkesin gücünü kullan",
          type: "leadership",
        },
        {
          id: "maintain_morale",
          description: "Moral yüksek tut - umut ver",
          type: "social",
        },
        {
          id: "make_decisions",
          description: "Kararlar ver - liderlik yap",
          type: "leadership",
        },
      ],
      explore: [
        {
          id: "venture_deeper",
          description: "Daha derine git - sınırları zorla",
          type: "explore",
        },
        {
          id: "map_area",
          description: "Bölgeyi haritalandır - bilgi topla",
          type: "investigate",
        },
        {
          id: "discover_secrets",
          description: "Sırları keşfet - gizemleri çöz",
          type: "investigate",
        },
        {
          id: "gather_resources",
          description: "Kaynakları topla - hazırlık yap",
          type: "gathering",
        },
      ],
      magic: [
        {
          id: "cast_spell",
          description: "Büyü yap - gücünü kullan",
          type: "magic",
        },
        {
          id: "study_magic",
          description: "Büyüyü çalış - bilgi edin",
          type: "investigate",
        },
        {
          id: "channel_energy",
          description: "Enerjiyi yönlendir - kontrol et",
          type: "magic",
        },
        {
          id: "create_artifact",
          description: "Artefakt yarat - yaratıcı ol",
          type: "magic",
        },
      ],
      technology: [
        {
          id: "hack_system",
          description: "Sistemi hack et - teknolojiyi kullan",
          type: "technology",
        },
        {
          id: "repair_device",
          description: "Cihazı tamir et - becerilerini göster",
          type: "technology",
        },
        {
          id: "upgrade_equipment",
          description: "Ekipmanı geliştir - ilerleme kaydet",
          type: "technology",
        },
        {
          id: "analyze_data",
          description: "Veriyi analiz et - bilgi çıkar",
          type: "investigate",
        },
      ],
      default: [
        {
          id: "continue_adventure",
          description: "Macereye devam et - hikaye devam ediyor",
          type: "explore",
        },
        {
          id: "investigate_surroundings",
          description: "Çevreyi araştır - yeni fırsatlar bul",
          type: "investigate",
        },
        {
          id: "interact_with_npcs",
          description: "NPC'lerle etkileşim kur - bağlantılar kur",
          type: "social",
        },
        {
          id: "prepare_for_combat",
          description: "Savaşa hazırlan - güçlü ol",
          type: "combat",
        },
      ],
    };

    const actions =
      richActionTemplates[actionType] || richActionTemplates.default;

    // Ensure we NEVER return empty arrays
    if (!actions || actions.length === 0) {
      return richActionTemplates.default;
    }

    return actions;
  };

  // Rich error fallback narrative generator
  const generateRichErrorFallbackNarrative = (
    action: any,
    scenario: any
  ): string => {
    const scenarioTitle = scenario?.title || "Macera";
    return `Bir anlık kesinti yaşandı, ama ${scenarioTitle} devam ediyor! Çevreni incelemeye devam et ve yeni fırsatları keşfet. Her zorluk yeni bir fırsat sunar ve sen bu fırsatları değerlendirmeye hazırsın.`;
  };

  // Rich error fallback actions generator
  const generateRichErrorFallbackActions = (
    action: any,
    scenario: any
  ): any[] => {
    return [
      {
        id: "recover_and_continue",
        description: "Toparlan ve devam et - güçlü kal",
        type: "recovery",
      },
      {
        id: "assess_situation",
        description: "Durumu değerlendir - stratejik düşün",
        type: "investigate",
      },
      {
        id: "seek_help",
        description: "Yardım ara - müttefik bul",
        type: "social",
      },
      {
        id: "adapt_strategy",
        description: "Stratejiyi uyarla - esnek ol",
        type: "tactics",
      },
    ];
  };

  const generateDynamicActions = (
    previousAction: any,
    scenarioType: string
  ): any[] => {
    const actionType = previousAction.type || "default";

    const actionTemplates: { [key: string]: any[] } = {
      rescue: [
        {
          id: "continue_search",
          description: "Aramaya devam et",
          type: "investigate",
        },
        {
          id: "help_others",
          description: "Diğer kurbanlara yardım et",
          type: "rescue",
        },
        {
          id: "assess_damage",
          description: "Hasarı değerlendir",
          type: "investigate",
        },
        {
          id: "coordinate_rescue",
          description: "Kurtarma operasyonunu koordine et",
          type: "leadership",
        },
      ],
      investigate: [
        {
          id: "follow_clues",
          description: "İpuçlarını takip et",
          type: "investigate",
        },
        {
          id: "ask_questions",
          description: "Daha fazla soru sor",
          type: "social",
        },
        {
          id: "examine_evidence",
          description: "Kanıtları incele",
          type: "investigate",
        },
        {
          id: "search_area",
          description: "Bölgeyi ara",
          type: "explore",
        },
      ],
      social: [
        {
          id: "build_relationships",
          description: "İlişkiler kur",
          type: "social",
        },
        {
          id: "gather_information",
          description: "Bilgi topla",
          type: "investigate",
        },
        {
          id: "negotiate",
          description: "Müzakere et",
          type: "social",
        },
        {
          id: "inspire_others",
          description: "Başkalarını ilham et",
          type: "leadership",
        },
      ],
      combat: [
        {
          id: "prepare_weapons",
          description: "Silahları hazırla",
          type: "combat",
        },
        {
          id: "study_enemy",
          description: "Düşmanı incele",
          type: "investigate",
        },
        {
          id: "plan_strategy",
          description: "Strateji planla",
          type: "tactics",
        },
        {
          id: "rally_allies",
          description: "Müttefikleri topla",
          type: "leadership",
        },
      ],
      stealth: [
        {
          id: "move_silently",
          description: "Sessizce hareket et",
          type: "stealth",
        },
        {
          id: "observe_enemies",
          description: "Düşmanları gözle",
          type: "investigate",
        },
        {
          id: "find_alternate_route",
          description: "Alternatif yol bul",
          type: "explore",
        },
        {
          id: "create_diversion",
          description: "Dikkat dağıtıcı yarat",
          type: "tactics",
        },
      ],
      tactics: [
        {
          id: "analyze_situation",
          description: "Durumu analiz et",
          type: "investigate",
        },
        {
          id: "formulate_plan",
          description: "Plan oluştur",
          type: "tactics",
        },
        {
          id: "coordinate_team",
          description: "Ekibi koordine et",
          type: "leadership",
        },
        {
          id: "prepare_resources",
          description: "Kaynakları hazırla",
          type: "preparation",
        },
      ],
      leadership: [
        {
          id: "motivate_team",
          description: "Ekibi motive et",
          type: "leadership",
        },
        {
          id: "assign_roles",
          description: "Rolleri ata",
          type: "leadership",
        },
        {
          id: "maintain_morale",
          description: "Moral yüksek tut",
          type: "social",
        },
        {
          id: "make_decisions",
          description: "Kararlar ver",
          type: "leadership",
        },
      ],
      explore: [
        {
          id: "venture_deeper",
          description: "Daha derine git",
          type: "explore",
        },
        {
          id: "map_area",
          description: "Bölgeyi haritalandır",
          type: "investigate",
        },
        {
          id: "discover_secrets",
          description: "Sırları keşfet",
          type: "investigate",
        },
        {
          id: "gather_resources",
          description: "Kaynakları topla",
          type: "gathering",
        },
      ],
      magic: [
        {
          id: "cast_spell",
          description: "Büyü yap",
          type: "magic",
        },
        {
          id: "study_magic",
          description: "Büyüyü çalış",
          type: "investigate",
        },
        {
          id: "channel_energy",
          description: "Enerjiyi yönlendir",
          type: "magic",
        },
        {
          id: "create_artifact",
          description: "Artefakt yarat",
          type: "magic",
        },
      ],
      technology: [
        {
          id: "hack_system",
          description: "Sistemi hack et",
          type: "technology",
        },
        {
          id: "repair_device",
          description: "Cihazı tamir et",
          type: "technology",
        },
        {
          id: "upgrade_equipment",
          description: "Ekipmanı geliştir",
          type: "technology",
        },
        {
          id: "analyze_data",
          description: "Veriyi analiz et",
          type: "investigate",
        },
      ],
      default: [
        {
          id: "continue_adventure",
          description: "Macereye devam et",
          type: "explore",
        },
        {
          id: "investigate_surroundings",
          description: "Çevreyi araştır",
          type: "investigate",
        },
        {
          id: "interact_with_npcs",
          description: "NPC'lerle etkileşim kur",
          type: "social",
        },
        {
          id: "prepare_for_combat",
          description: "Savaşa hazırlan",
          type: "combat",
        },
      ],
    };

    const actions = actionTemplates[actionType] || actionTemplates.default;

    // Ensure we never return empty arrays
    if (!actions || actions.length === 0) {
      return actionTemplates.default;
    }

    return actions;
  };

  const generateCombatNarrative = (
    action: any,
    scenarioType: string
  ): string => {
    const actionContext = action.context || "";
    const actionDescription = action.description || "";

    // Contextual combat narratives based on action context
    const contextualNarratives: { [key: string]: string } = {
      target_weak_points:
        "�� Düşmanın zayıf noktalarını aramaya başlıyorsunuz...",
      hack_systems: "💻 Düşmanın sistemlerini hack etmeye çalışıyorsunuz...",
      power_attack: "⚔️ Tüm gücünüzle saldırıya geçiyorsunuz!",
      defensive_stance: "🛡️ Savunma pozisyonu alıyorsunuz...",
      agile_escape: "🏃 Çevik hareketlerle kaçmaya çalışıyorsunuz...",
      high_ground: "🌳 Yüksek pozisyon aramaya başlıyorsunuz...",
      forest_stealth:
        "🌲 Ormanın gölgelerini kullanarak gizlice hareket ediyorsunuz...",
      vehicle_cover: "🚗 Araçları kalkan olarak kullanıyorsunuz...",
      neon_distraction:
        "🌃 Neon ışıklarını kullanarak düşmanın dikkatini dağıtmaya çalışıyorsunuz...",
      imperial_position:
        "🛡️ Imperial savunma pozisyonlarını kullanıyorsunuz...",
      exploit_ork_tech:
        "⚙️ Ork teknolojisindeki zayıflıkları istismar etmeye çalışıyorsunuz...",
    };

    // Return contextual narrative or generic one
    return (
      contextualNarratives[actionContext] ||
      `⚔️ ${actionDescription} aksiyonunu gerçekleştiriyorsunuz...`
    );
  };

  const addToHistory = (message: string) => {
    setGameHistory((prev) => [...prev, message]);
  };

  const handleSkillUpgrade = (skillId: string, treeId: string) => {
    if (skillPoints <= 0) return;

    // Check if skill is available for the character class
    const characterClass =
      CHARACTER_CLASSES[selectedPlayer?.class || "warrior"];
    const availableSkills = characterClass?.skillTree?.[treeId] || [];

    if (!availableSkills.includes(skillId)) {
      setError("Bu yetenek bu sınıf için mevcut değil!");
      return;
    }

    // Check if skill is already unlocked
    if (unlockedSkills.includes(skillId)) {
      setError("Bu yetenek zaten açılmış!");
      return;
    }

    // Unlock skill
    setUnlockedSkills((prev) => [...prev, skillId]);
    setSkillPoints((prev) => prev - 1);

    addToHistory(`⚡ Yeni yetenek açıldı: ${skillId}`);

    // Check for level up
    checkLevelUp();
  };

  const checkLevelUp = () => {
    const experienceNeeded = characterLevel * 100;
    if (experience >= experienceNeeded) {
      levelUp();
    }
  };

  const levelUp = () => {
    const newLevel = characterLevel + 1;
    setCharacterLevel(newLevel);
    setExperience((prev) => prev - characterLevel * 100);
    setSkillPoints((prev) => prev + 2); // 2 skill points per level
    setAttributePoints((prev) => prev + 3); // 3 attribute points per level

    // Increase base stats
    setPlayerHP((prev) => prev + 20);
    setPlayerMana((prev) => prev + 10);

    addToHistory(`🎉 Seviye atladın! Yeni seviye: ${newLevel}`);
    addToHistory(`⚡ +2 Yetenek Puanı, +3 Özellik Puanı kazandın!`);
  };

  const allocateAttributePoint = (attribute: string) => {
    if (attributePoints <= 0) return;

    setAttributes((prev) => ({
      ...prev,
      [attribute]: prev[attribute] + 1,
    }));
    setAttributePoints((prev) => prev - 1);

    // Update derived stats based on attributes
    updateDerivedStats();

    addToHistory(
      `📊 ${ATTRIBUTES[attribute as keyof typeof ATTRIBUTES]?.name} +1`
    );
  };

  const updateDerivedStats = () => {
    // Update HP based on constitution
    const baseHP = 100;
    const hpBonus = attributes.constitution * 5;
    setPlayerHP(baseHP + hpBonus);

    // Update mana based on intelligence
    const baseMana = 100;
    const manaBonus = attributes.intelligence * 3;
    setPlayerMana(baseMana + manaBonus);
  };

  const useSkillInCombat = (skillName: string) => {
    if (!inCombat || !enemy) return;

    // Find skill in skill system
    let skillData = null;
    for (const category in SKILL_SYSTEM) {
      if (SKILL_SYSTEM[category][skillName]) {
        skillData = SKILL_SYSTEM[category][skillName];
        break;
      }
    }

    if (!skillData) {
      setError("Yetenek bulunamadı!");
      return;
    }

    // Check mana cost
    if (skillData.mana && playerMana < skillData.mana) {
      setError("Yeterli mana yok!");
      return;
    }

    // Apply skill effects
    if (skillData.damage > 0) {
      const damage = skillData.damage + attributes.strength * 2;
      setEnemyHP((prev) => Math.max(0, prev - damage));
      addCombatLog(`⚔️ ${skillName} kullandın! ${damage} hasar verdin!`);
    }

    if (skillData.heal) {
      const heal = skillData.heal + attributes.wisdom * 2;
      setPlayerHP((prev) => Math.min(200, prev + heal));
      addCombatLog(`💚 ${skillName} kullandın! ${heal} can iyileştirdin!`);
    }

    if (skillData.defense) {
      addCombatLog(`🛡️ ${skillName} kullandın! Savunma arttı!`);
    }

    if (skillData.stealth) {
      addCombatLog(`👁️ ${skillName} kullandın! Gizlilik arttı!`);
    }

    // Consume mana
    if (skillData.mana) {
      setPlayerMana((prev) => prev - skillData.mana);
    }

    // Enemy turn
    setTimeout(() => {
      enemyTurn();
    }, 1000);
  };

  const enemyTurn = () => {
    if (!enemy || enemyHP <= 0) return;

    const enemyDamage = Math.floor(Math.random() * 20) + 10;
    setPlayerHP((prev) => Math.max(0, prev - enemyDamage));
    addCombatLog(`😈 ${enemy.name} saldırdı! ${enemyDamage} hasar aldın!`);

    // Check if player is defeated
    if (playerHP <= 0) {
      addCombatLog(`💀 Yenildin! Savaş bitti.`);
      setInCombat(false);
      setGameState("playing");
    }

    // Check if enemy is defeated
    if (enemyHP <= 0) {
      addCombatLog(`🎉 ${enemy.name} yenildi! Zafer kazandın!`);
      setInCombat(false);
      setGameState("playing");

      // Gain experience
      const expGained = enemy.level * 25;
      setExperience((prev) => prev + expGained);
      addCombatLog(`⭐ ${expGained} deneyim puanı kazandın!`);

      checkLevelUp();
    }
  };

  const addCombatLog = (message: string) => {
    setCombatLog((prev) => [...prev, message]);
  };

  const startCombat = (enemyData: any) => {
    setEnemy(enemyData);
    setEnemyHP(enemyData.hp || 100);
    setInCombat(true);
    setGameState("combat");
    setCombatLog([]);

    addCombatLog(`⚔️ ${enemyData.name} ile savaş başladı!`);
  };

  const getAvailableSkills = () => {
    if (!selectedPlayer) return [];

    const characterClass = CHARACTER_CLASSES[selectedPlayer.class];
    const allSkills = [];

    // Get all skills from skill tree
    for (const tree in characterClass.skillTree) {
      allSkills.push(...characterClass.skillTree[tree]);
    }

    // Filter to only unlocked skills
    return allSkills.filter((skill) => unlockedSkills.includes(skill));
  };

  const openAttributes = () => {
    setGameState("attributes");
  };

  const closeAttributes = () => {
    setGameState("playing");
  };

  const openSkillTree = () => {
    setGameState("skill_tree");
  };

  const closeSkillTree = () => {
    setGameState("playing");
  };

  // Senaryoları yükle
  useEffect(() => {
    const loadScenarios = async () => {
      try {
        setIsLoading(true);
        setError(null);

        // Load scenarios from the database
        const response = await fetch("/api/scenarios");
        if (!response.ok) {
          throw new Error("Senaryolar yüklenemedi");
        }

        const data = await response.json();

        // Load AI generated scenarios
        const aiResponse = await fetch("/api/ai/scenarios");
        let aiScenarios = [];
        if (aiResponse.ok) {
          const aiData = await aiResponse.json();
          aiScenarios = aiData.scenarios || [];
        }

        // Load file-generated scenarios
        const fileGeneratedResponse = await fetch("/api/ai/scenarios");
        let fileGeneratedScenarios = [];
        if (fileGeneratedResponse.ok) {
          const fileData = await fileGeneratedResponse.json();
          fileGeneratedScenarios = fileData.scenarios || [];
        }

        // Combine all scenarios
        const allScenarios = [
          ...(data.scenarios || data || []),
          ...aiScenarios,
          ...fileGeneratedScenarios,
        ];

        // Validate and filter scenarios to ensure they have proper content
        const validScenarios = allScenarios.filter((scenario: any) => {
          return (
            scenario &&
            scenario.id &&
            scenario.title &&
            scenario.title.trim() !== "" &&
            scenario.description &&
            scenario.description.trim() !== "" &&
            scenario.theme &&
            scenario.difficulty
          );
        });

        if (validScenarios.length === 0) {
          throw new Error("Geçerli senaryo bulunamadı");
        }

        setAvailableScenarios(validScenarios);
        console.log(
          `Loaded ${validScenarios.length} valid scenarios (including ${aiScenarios.length} AI generated)`
        );

        // Log any invalid scenarios for debugging
        const invalidScenarios = allScenarios.filter((scenario: any) => {
          return !(
            scenario &&
            scenario.id &&
            scenario.title &&
            scenario.title.trim() !== "" &&
            scenario.description &&
            scenario.description.trim() !== "" &&
            scenario.theme &&
            scenario.difficulty
          );
        });

        if (invalidScenarios.length > 0) {
          console.warn(
            `Found ${invalidScenarios.length} invalid scenarios:`,
            invalidScenarios
          );
        }
      } catch (error) {
        console.error("Error loading scenarios:", error);
        setError(`Senaryolar yüklenirken hata oluştu: ${error}`);

        // Provide fallback scenarios
        const fallbackScenarios = [
          {
            id: "fallback_fantasy",
            title: "Fantastik Macera",
            description:
              "Klasik bir fantastik macera. Ejderhalar, büyü ve kahramanlık seni bekliyor.",
            theme: "fantasy",
            difficulty: "medium",
            complexity: "medium",
            estimatedPlayTime: 60,
          },
          {
            id: "fallback_warhammer",
            title: "Warhammer 40K Görevi",
            description:
              "İmparatorluk için savaş zamanı. Zafer veya ölüm - başka seçenek yok.",
            theme: "warhammer40k",
            difficulty: "hard",
            complexity: "high",
            estimatedPlayTime: 90,
          },
        ];

        setAvailableScenarios(fallbackScenarios);
      } finally {
        setIsLoading(false);
      }
    };
    loadScenarios();
  }, []);

  const handleScenarioSelect = (scenarioId: string) => {
    setSelectedScenarioId(scenarioId);
    const selectedScenario = availableScenarios.find(
      (s) => s.id === scenarioId
    );
    if (selectedScenario) {
      console.log("Seçilen senaryo:", selectedScenario);
    }
  };

  const renderContextualActions = () => {
    if (!availableActions || availableActions.length === 0) {
      // Return fallback actions based on scenario type
      const scenarioType = scenario?.theme || scenario?.genre || "fantasy";

      const fallbackActions: { [key: string]: any[] } = {
        fantasy: [
          {
            description: "🌳 Çevreyi araştır",
            type: "explore",
            context: "exploration",
          },
          {
            description: "💬 NPC ile konuş",
            type: "social",
            context: "communication",
          },
          {
            description: "⚔️ Savaşa hazırlan",
            type: "combat",
            context: "preparation",
          },
          {
            description: "🔍 Gizli şeyleri araştır",
            type: "investigate",
            context: "investigation",
          },
        ],
        cyberpunk: [
          {
            description: "💻 Sistemi hack et",
            type: "technology",
            context: "hacking",
          },
          {
            description: "👁️ Gölgelerde gizlen",
            type: "stealth",
            context: "stealth",
          },
          {
            description: "🔍 Bilgi topla",
            type: "investigation",
            context: "intelligence",
          },
        ],
        "sci-fi": [
          {
            description: "🛡️ Savunma pozisyonu al",
            type: "tactics",
            context: "defense",
          },
          {
            description: "🚀 Tehlikeli bölgeleri keşfet",
            type: "exploration",
            context: "danger_zone",
          },
          {
            description: "👑 Korumaları organize et",
            type: "leadership",
            context: "command",
          },
          {
            description: "🔬 Teknolojik analiz yap",
            type: "science",
            context: "analysis",
          },
        ],
        warhammer: [
          {
            description: "🛡️ Imperial pozisyonu al",
            type: "tactics",
            context: "imperial_position",
          },
          {
            description: "⚔️ Ork teknolojisini istismar et",
            type: "technology",
            context: "ork_tech",
          },
          {
            description: "🚨 Sivilleri tahliye et",
            type: "leadership",
            context: "evacuation",
          },
          {
            description: "🔍 Düşman güçlerini keşfet",
            type: "reconnaissance",
            context: "scouting",
          },
        ],
      };

      const actions = fallbackActions[scenarioType] || fallbackActions.fantasy;

      return actions.map((action, index) => (
        <button
          key={`fallback-${index}`}
          className={`action-btn ${action.type || "default"}`}
          onClick={() => executeAction(action)}
          disabled={isLoading}
        >
          <span className="action-icon">
            {action.type === "explore" && "🔍"}
            {action.type === "social" && "💬"}
            {action.type === "combat" && "⚔️"}
            {action.type === "investigate" && "🔎"}
            {action.type === "technology" && "💻"}
            {action.type === "stealth" && "👁️"}
            {action.type === "tactics" && "🎯"}
            {action.type === "leadership" && "👑"}
            {action.type === "science" && "🔬"}
            {action.type === "reconnaissance" && "🚨"}
            {action.type === "agility" && "⚡"}
            {!action.type && "⚡"}
          </span>
          {action.description}
        </button>
      ));
    }

    return availableActions.map((action: any, index: number) => (
      <button
        key={`action-${index}`}
        className={`action-btn ${action.type || "default"}`}
        onClick={() => executeAction(action)}
        disabled={isLoading}
      >
        <span className="action-icon">
          {action.type === "combat" && "⚔️"}
          {action.type === "explore" && "🔍"}
          {action.type === "social" && "💬"}
          {action.type === "magic" && "✨"}
          {action.type === "stealth" && "👁️"}
          {action.type === "investigate" && "🔎"}
          {action.type === "hack" && "💻"}
          {action.type === "leadership" && "👑"}
          {action.type === "defense" && "🛡️"}
          {action.type === "technology" && "⚙️"}
          {action.type === "tactics" && "🎯"}
          {action.type === "rescue" && "🆘"}
          {!action.type && "⚡"}
        </span>
        {action.description || action.text || `Aksiyon ${index + 1}`}
        {action.dice && <span className="dice-info">({action.dice})</span>}
        {action.skill && <span className="skill-info">[{action.skill}]</span>}
      </button>
    ));
  };

  const renderCombatActions = () => {
    const availableSkills = getAvailableSkills();

    // Show unlocked skills as combat actions
    if (availableSkills.length > 0) {
      return (
        <div className="combat-actions">
          <h4>⚡ Yeteneklerin:</h4>
          <div className="skill-grid">
            {availableSkills.map((skillName, index) => {
              // Find skill data
              let skillData = null;
              for (const category in SKILL_SYSTEM) {
                if (SKILL_SYSTEM[category][skillName]) {
                  skillData = SKILL_SYSTEM[category][skillName];
                  break;
                }
              }

              if (!skillData) return null;

              const canUse = !skillData.mana || playerMana >= skillData.mana;

              return (
                <button
                  key={`skill-${index}`}
                  className={`skill-btn ${!canUse ? "disabled" : ""}`}
                  onClick={() => canUse && useSkillInCombat(skillName)}
                  disabled={!canUse || isLoading}
                >
                  <span className="skill-icon">
                    {skillData.damage > 0 && "⚔️"}
                    {skillData.heal && "💚"}
                    {skillData.defense && "🛡️"}
                    {skillData.stealth && "👁️"}
                    {skillData.mana && "🔮"}
                    {!skillData.damage &&
                      !skillData.heal &&
                      !skillData.defense &&
                      !skillData.stealth &&
                      "⚡"}
                  </span>
                  <div className="skill-info">
                    <span className="skill-name">{skillName}</span>
                    <span className="skill-description">
                      {skillData.description}
                    </span>
                    {skillData.mana && (
                      <span className="skill-cost">Mana: {skillData.mana}</span>
                    )}
                  </div>
                </button>
              );
            })}
          </div>

          <h4>🎯 Temel Aksiyonlar:</h4>
          <div className="basic-actions">
            <button
              className="action-btn combat"
              onClick={() => useSkillInCombat("Basic Attack")}
              disabled={isLoading}
            >
              <span className="action-icon">⚔️</span>
              Temel Saldırı
            </button>
            <button
              className="action-btn combat"
              onClick={() => useSkillInCombat("Defend")}
              disabled={isLoading}
            >
              <span className="action-icon">🛡️</span>
              Savun
            </button>
            <button
              className="action-btn combat"
              onClick={() => {
                setInCombat(false);
                setGameState("playing");
                addCombatLog("🏃 Savaştan kaçtın!");
              }}
              disabled={isLoading}
            >
              <span className="action-icon">🏃</span>
              Kaç
            </button>
          </div>
        </div>
      );
    }

    // Fallback combat actions if no skills unlocked
    const fallbackCombatActions = [
      { description: "⚔️ Saldır", type: "combat", context: "attack" },
      { description: "🛡️ Savun", type: "combat", context: "defend" },
      { description: "🏃 Kaç", type: "combat", context: "escape" },
      { description: "🎯 Özel Saldırı", type: "combat", context: "special" },
    ];

    return fallbackCombatActions.map((action, index) => (
      <button
        key={`fallback-combat-${index}`}
        className="action-btn combat"
        onClick={() => executeAction(action)}
        disabled={isLoading}
      >
        <span className="action-icon">⚔️</span>
        {action.description}
      </button>
    ));
  };

  // Fallback narrative generator for when dynamic generation fails
  const generateFallbackNarrative = (action: any, scenario: any): string => {
    const actionType = action.type || "default";
    const scenarioTheme = scenario?.theme || "fantasy";

    const fallbackNarratives: { [key: string]: string } = {
      rescue: "Cesurca devam ediyorsun. Her adımda yeni bir keşif yapıyorsun.",
      investigate:
        "Dikkatli bir şekilde çevreni inceliyorsun. İpuçları seni bekliyor.",
      social:
        "İnsanlarla etkileşim kuruyorsun. Her konuşma yeni kapılar açıyor.",
      combat: "Savaş hazırlığı yapıyorsun. Güçlü ve hazır olmalısın.",
      stealth: "Gizlice hareket ediyorsun. Sessizlik senin dostun.",
      tactics: "Stratejik düşünüyorsun. Her hamle önemli.",
      leadership: "Liderlik gösteriyorsun. İnsanlar sana güveniyor.",
      default: "Macera devam ediyor. Yeni fırsatlar seni bekliyor.",
    };

    return fallbackNarratives[actionType] || fallbackNarratives.default;
  };

  // Fallback actions generator
  const generateFallbackActions = (action: any, scenario: any): any[] => {
    return [
      {
        id: "continue_adventure",
        description: "Macereye devam et",
        type: "explore",
      },
      {
        id: "investigate_surroundings",
        description: "Çevreyi araştır",
        type: "investigate",
      },
      {
        id: "interact_with_npcs",
        description: "NPC'lerle etkileşim kur",
        type: "social",
      },
      {
        id: "prepare_for_combat",
        description: "Savaşa hazırlan",
        type: "combat",
      },
    ];
  };

  // Error fallback narrative generator
  const generateErrorFallbackNarrative = (
    action: any,
    scenario: any
  ): string => {
    return "Bir anlık kesinti yaşandı, ama macera devam ediyor. Çevreni incelemeye devam et ve yeni fırsatları keşfet.";
  };

  // Error fallback actions generator
  const generateErrorFallbackActions = (action: any, scenario: any): any[] => {
    return [
      {
        id: "recover_and_continue",
        description: "Toparlan ve devam et",
        type: "recovery",
      },
      {
        id: "assess_situation",
        description: "Durumu değerlendir",
        type: "investigate",
      },
    ];
  };

  // Render fallback actions when no valid actions are available
  const renderFallbackActions = () => {
    const fallbackActions = [
      {
        id: "continue_adventure",
        description: "Macereye devam et",
        type: "explore",
      },
      {
        id: "investigate_surroundings",
        description: "Çevreyi araştır",
        type: "investigate",
      },
      {
        id: "interact_with_npcs",
        description: "NPC'lerle etkileşim kur",
        type: "social",
      },
      {
        id: "prepare_for_combat",
        description: "Savaşa hazırlan",
        type: "combat",
      },
    ];

    return fallbackActions.map((action, index) => (
      <button
        key={`fallback-${index}`}
        className="action-btn"
        onClick={() => executeAction(action)}
        disabled={isLoading}
      >
        <span className="action-icon">
          {action.type === "explore" && "🗺️"}
          {action.type === "investigate" && "🔍"}
          {action.type === "social" && "💬"}
          {action.type === "combat" && "⚔️"}
          {!["explore", "investigate", "social", "combat"].includes(
            action.type
          ) && "⚡"}
        </span>
        {action.description}
      </button>
    ));
  };

  if (gameState === "skill_tree") {
    return (
      <SkillTreeUI
        onClose={closeSkillTree}
        onSkillUpgrade={handleSkillUpgrade}
        skillPoints={skillPoints}
        characterLevel={characterLevel}
      />
    );
  }

  if (gameState === "attributes") {
    return (
      <div className="attributes-panel">
        <div className="attributes-header">
          <h2>📊 Karakter Özellikleri</h2>
          <button className="close-btn" onClick={closeAttributes}>
            ✕
          </button>
        </div>

        <div className="character-stats">
          <div className="stat-row">
            <span>Seviye: {characterLevel}</span>
            <span>
              Deneyim: {experience}/{characterLevel * 100}
            </span>
          </div>
          <div className="stat-row">
            <span>Can: {playerHP}</span>
            <span>Mana: {playerMana}</span>
          </div>
          <div className="stat-row">
            <span>Yetenek Puanı: {skillPoints}</span>
            <span>Özellik Puanı: {attributePoints}</span>
          </div>
        </div>

        <div className="attributes-grid">
          {Object.entries(ATTRIBUTES).map(([key, attr]) => (
            <div key={key} className="attribute-item">
              <div className="attribute-header">
                <span className="attribute-name">{attr.name}</span>
                <span className="attribute-value">
                  {attributes[key as keyof typeof attributes]}
                </span>
              </div>
              <p className="attribute-description">{attr.description}</p>
              <button
                className="attribute-btn"
                onClick={() => allocateAttributePoint(key)}
                disabled={attributePoints <= 0}
              >
                +1 {attr.name}
              </button>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="game-master-container">
      {/* Sol Panel - Oyun Alanı */}
      <div className="left-panel">
        <div className="game-header">
          <h2>🎮 {scenario?.title || "AI Dungeon Master"}</h2>
          <div className="game-status">
            <span className="status-indicator">
              {gameState === "setup" && "🎯 Hazırlanıyor"}
              {gameState === "playing" && "🎮 Oynanıyor"}
              {gameState === "combat" && "⚔️ Savaş"}
              {gameState === "ended" && "🏁 Bitti"}
            </span>
          </div>
        </div>

        {/* Character Stats Bar */}
        <div className="character-stats-bar">
          <div className="stat-item">
            <span className="stat-label">Seviye {characterLevel}</span>
            <div className="exp-bar">
              <div
                className="exp-fill"
                style={{
                  width: `${(experience / (characterLevel * 100)) * 100}%`,
                }}
              ></div>
            </div>
          </div>
          <div className="stat-item">
            <span className="stat-label">Can {playerHP}</span>
            <div className="hp-bar">
              <div
                className="hp-fill"
                style={{ width: `${(playerHP / 200) * 100}%` }}
              ></div>
            </div>
          </div>
          <div className="stat-item">
            <span className="stat-label">Mana {playerMana}</span>
            <div className="mana-bar">
              <div
                className="mana-fill"
                style={{ width: `${(playerMana / 200) * 100}%` }}
              ></div>
            </div>
          </div>
        </div>

        <div className="game-content">
          {/* Senaryo Bilgisi */}
          <div className="scenario-info">
            <h3>📖 Senaryo: {scenario?.title}</h3>
            <p className="scenario-description">{scenario?.description}</p>
            <div className="scenario-meta">
              <span className="difficulty-badge">{scenario?.difficulty}</span>
              <span className="theme-badge">{scenario?.theme}</span>
              <span className="playtime-badge">
                ⏱️ {scenario?.estimatedPlayTime} dk
              </span>
            </div>
          </div>

          {/* Ana Oyun Alanı */}
          <div className="main-game-area">
            {/* Hikaye Anlatımı */}
            <div className="narrative-section">
              <h4>📜 Hikaye:</h4>
              <div className="narrative-content">
                {currentNarrative && currentNarrative.trim() ? (
                  <div className="narrative-text">
                    {currentNarrative.split("\n").map((line, index) => (
                      <p key={index}>{line || "..."}</p>
                    ))}
                  </div>
                ) : (
                  <div className="narrative-text">
                    <p className="no-narrative">
                      {gameState === "setup"
                        ? "Hikaye henüz başlamadı. Oyunu başlatmak için butona tıkla!"
                        : "Hikaye devam ediyor... Yeni bir aksiyon seç ve macereye devam et!"}
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Combat Section - Show when in combat */}
            {gameState === "combat" && (
              <div className="combat-section">
                <div className="combat-header">
                  <h3>⚔️ Savaş - {enemy?.name}</h3>
                  <div className="combat-status">
                    <span className="combat-indicator">
                      🔥 Savaş Devam Ediyor
                    </span>
                  </div>
                </div>

                {/* Enemy HP Bar */}
                <div className="enemy-stats">
                  <div className="enemy-hp-bar">
                    <span>Düşman Can: {enemyHP}</span>
                    <div
                      className="enemy-hp-fill"
                      style={{
                        width: `${(enemyHP / (enemy?.hp || 100)) * 100}%`,
                      }}
                    ></div>
                  </div>
                </div>

                {/* Combat Log */}
                <div className="combat-log">
                  <h4>📜 Savaş Günlüğü:</h4>
                  <div className="log-content">
                    {combatLog.slice(-5).map((log, index) => (
                      <div key={index} className="log-entry">
                        {log}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            <div className="actions-section">
              <h4>⚡ Seçeneklerin:</h4>
              <div className="action-grid">
                {/* Show combat actions if in combat mode */}
                {gameState === "combat" ||
                (availableActions &&
                  availableActions.some(
                    (action: any) => action.type === "combat" || action.context
                  ))
                  ? renderCombatActions()
                  : availableActions && availableActions.length > 0
                  ? renderContextualActions()
                  : renderFallbackActions()}
              </div>
            </div>

            {error && (
              <div className="error-message">
                <p>❌ Hata: {error}</p>
              </div>
            )}

            <div className="game-controls">
              {gameState === "setup" && (
                <button
                  className="start-game-btn"
                  onClick={startGame}
                  disabled={isLoading}
                >
                  {isLoading ? "Yükleniyor..." : "🎮 Oyunu Başlat"}
                </button>
              )}

              {gameState === "playing" && (
                <div className="game-control-buttons">
                  <button className="control-btn" onClick={openSkillTree}>
                    🌳 Skill Tree ({skillPoints})
                  </button>
                  <button className="control-btn" onClick={openAttributes}>
                    📊 Özellikler ({attributePoints})
                  </button>
                  <button
                    className="control-btn"
                    onClick={() => setGameState("ended")}
                  >
                    🏁 Oyunu Bitir
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Sağ Panel - Oyun Geçmişi */}
        <div className="right-panel">
          <div className="game-history">
            <h4>📜 Oyun Geçmişi</h4>
            <div className="history-content">
              {gameHistory.length > 0 ? (
                gameHistory.slice(-5).map((entry, index) => (
                  <div key={index} className="history-item">
                    <span className="history-time">
                      {new Date().toLocaleTimeString()}
                    </span>
                    <span className="history-text">{entry}</span>
                  </div>
                ))
              ) : (
                <p className="no-history">Henüz oyun geçmişi yok.</p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Skill Tree Modal */}
      {gameState === "skill_tree" && (
        <SkillTreeUI
          onClose={closeSkillTree}
          onSkillUpgrade={handleSkillUpgrade}
          skillPoints={skillPoints}
          characterLevel={characterLevel}
        />
      )}
    </div>
  );
};
