import { RPGScenario, StoredScenario } from '../types/scenarioStorage';
import { ComicData } from '../types/comic';

export interface ComprehensiveScenarioNode {
  id: string;
  title: string;
  text: string;
  backgroundImage?: string;
  choices: ComprehensiveChoice[];
  npcs?: NPC[];
  enemies?: Enemy[];
  items?: string[];
  combat?: boolean;
  ending?: boolean;
  plotTwist?: boolean;
  betrayal?: boolean;
  randomEvent?: boolean;
  consequences?: Consequence[];
  requirements?: Requirement[];
}

export interface ComprehensiveChoice {
  text: string;
  next: string;
  diceRoll?: {
    type: string;
    target: number;
    skill: string;
  };
  effect?: {
    karma?: number;
    health?: number;
    item?: string;
    relationship?: string;
  };
  plotTwist?: boolean;
  betrayal?: boolean;
  randomEvent?: boolean;
}

export interface NPC {
  name: string;
  type: string;
  personality: string;
  motivation: string;
  relationship: string;
  betrayal?: boolean;
  plotTwist?: boolean;
}

export interface Enemy {
  name: string;
  type: string;
  hp: number;
  attack: number;
  defense: number;
  specialAbilities: string[];
  statusEffects: string[];
}

export interface Consequence {
  type: string;
  description: string;
  effect: any;
}

export interface Requirement {
  type: string;
  value: any;
  description: string;
}

export class ComprehensiveScenarioGenerator {
  private plotTwistTemplates = [
    "NPC aslında düşman tarafında",
    "Görünen düşman aslında müttefik",
    "Gizli geçit keşfi",
    "Kayıp hazine bulma",
    "Eski teknoloji keşfi",
    "Gizli organizasyon üyeliği",
    "Alternatif gerçeklik",
    "Zaman yolculuğu",
    "Ruh transferi",
    "Genetik manipülasyon"
  ];

  private betrayalTemplates = [
    "Güvenilir NPC ihanet ediyor",
    "Müttefik gizli plan yapıyor",
    "Komutan yanlış karar veriyor",
    "Sihirli eşya lanetli çıkıyor",
    "Dost görünen düşman",
    "Yardım eden aslında tuzak kuruyor",
    "Ödül aslında ceza",
    "Kurtarılan aslında tehdit"
  ];

  private randomEventTemplates = [
    "Meteor yağmuru",
    "Zaman fırtınası",
    "Boyut geçidi açılması",
    "Eski tanrı uyanması",
    "Teknoloji çökmesi",
    "Sihir dalgalanması",
    "Yaratık sürüsü",
    "Doğal afet",
    "Uzaylı istilası",
    "Ruhların uyanması"
  ];

  generateComprehensiveScenario(theme: string, difficulty: string): ComprehensiveScenarioNode[] {
    const nodes: ComprehensiveScenarioNode[] = [];
    
    // Başlangıç sahnesi
    nodes.push(this.createOpeningScene(theme));
    
    // Ana hikaye dalları
    const mainBranches = this.createMainBranches(theme, difficulty);
    nodes.push(...mainBranches);
    
    // Plot twist'ler
    const plotTwistNodes = this.createPlotTwistNodes(theme);
    nodes.push(...plotTwistNodes);
    
    // İhanet senaryoları
    const betrayalNodes = this.createBetrayalNodes(theme);
    nodes.push(...betrayalNodes);
    
    // Rastgele olaylar
    const randomEventNodes = this.createRandomEventNodes(theme);
    nodes.push(...randomEventNodes);
    
    // Savaş sahneleri
    const combatNodes = this.createCombatNodes(theme, difficulty);
    nodes.push(...combatNodes);
    
    // Sonlar
    const endingNodes = this.createEndingNodes(theme);
    nodes.push(...endingNodes);
    
    return nodes;
  }

  private createOpeningScene(theme: string): ComprehensiveScenarioNode {
    const themes = {
      fantasy: {
        title: "Fantastik Dünyada Uyanış",
        text: "Büyülü bir ormanda gözlerini açtın. Ağaçlar konuşuyor, yaratıklar her yerde. Sen kimsin ve neden buradasın?",
        backgroundImage: "fantasy_forest.jpg"
      },
      warhammer40k: {
        title: "İmparatorluk'ta Uyanış",
        text: "Hive şehrinin derinliklerinde uyandın. Makine sesleri, insan çığlıkları ve savaş gürültüleri. İmparator seni koruyor mu?",
        backgroundImage: "hive_city.jpg"
      },
      scifi: {
        title: "Uzay Gemisinde Uyanış",
        text: "Yabancı bir uzay gemisinde gözlerini açtın. Teknoloji bilinmeyen seviyede gelişmiş. Neredesin ve neden buradasın?",
        backgroundImage: "spaceship_interior.jpg"
      }
    };

    const themeData = themes[theme as keyof typeof themes] || themes.fantasy;

    return {
      id: "opening_scene",
      title: themeData.title,
      text: themeData.text,
      backgroundImage: themeData.backgroundImage,
      choices: [
        {
          text: "Çevreyi keşfet",
          next: "explore_environment",
          diceRoll: { type: "d20", target: 12, skill: "Perception" }
        },
        {
          text: "Yakındaki sesleri ara",
          next: "search_for_sounds",
          diceRoll: { type: "d20", target: 10, skill: "Investigation" }
        },
        {
          text: "Güvenli yer ara",
          next: "find_safe_place",
          diceRoll: { type: "d20", target: 8, skill: "Survival" }
        },
        {
          text: "Hemen kaç",
          next: "immediate_escape",
          diceRoll: { type: "d20", target: 15, skill: "Athletics" }
        }
      ],
      npcs: [],
      enemies: [],
      items: ["Harita", "Su", "Basit Silah"],
      combat: false,
      ending: false,
      plotTwist: false,
      betrayal: false,
      randomEvent: false
    };
  }

  private createMainBranches(theme: string, difficulty: string): ComprehensiveScenarioNode[] {
    const nodes: ComprehensiveScenarioNode[] = [];
    
    // Keşif sahnesi
    nodes.push({
      id: "explore_environment",
      title: "Çevre Keşfi",
      text: "Çevreyi keşfetmeye başladın. Garip işaretler ve izler var. Bir şeyler yaklaşıyor...",
      backgroundImage: `${theme}_exploration.jpg`,
      choices: [
        {
          text: "İzleri takip et",
          next: "follow_tracks",
          diceRoll: { type: "d20", target: 14, skill: "Tracking" }
        },
        {
          text: "İşaretleri incele",
          next: "examine_markers",
          diceRoll: { type: "d20", target: 12, skill: "Arcana" }
        },
        {
          text: "Gizli geçit ara",
          next: "search_secret_passage",
          diceRoll: { type: "d20", target: 16, skill: "Investigation" }
        },
        {
          text: "Geri dön",
          next: "return_to_start",
          effect: { karma: -5 }
        }
      ],
      npcs: [],
      enemies: [],
      items: [],
      combat: false,
      ending: false,
      plotTwist: false,
      betrayal: false,
      randomEvent: false
    });

    // NPC karşılaşması
    nodes.push({
      id: "npc_encounter",
      title: "NPC Karşılaşması",
      text: "Bir yolcu ile karşılaştın. Garip görünüyor ama yardım teklif ediyor. Güvenilir mi?",
      backgroundImage: `${theme}_npc_encounter.jpg`,
      choices: [
        {
          text: "Yardımı kabul et",
          next: "accept_help",
          effect: { karma: 5, relationship: "friendly" }
        },
        {
          text: "Şüpheli davran",
          next: "be_suspicious",
          diceRoll: { type: "d20", target: 13, skill: "Insight" }
        },
        {
          text: "Saldır",
          next: "attack_npc",
          effect: { karma: -10 },
          plotTwist: true
        },
        {
          text: "Kaç",
          next: "escape_from_npc",
          effect: { karma: -5 }
        }
      ],
      npcs: [{
        name: "Gizemli Yolcu",
        type: "Traveler",
        personality: "Mysterious",
        motivation: "Unknown",
        relationship: "neutral",
        betrayal: Math.random() > 0.7
      }],
      enemies: [],
      items: [],
      combat: false,
      ending: false,
      plotTwist: true,
      betrayal: false,
      randomEvent: false
    });

    return nodes;
  }

  private createPlotTwistNodes(theme: string): ComprehensiveScenarioNode[] {
    const nodes: ComprehensiveScenarioNode[] = [];
    
    // NPC ihaneti
    nodes.push({
      id: "npc_betrayal",
      title: "Beklenmedik İhanet",
      text: "Güvendiğin NPC aslında düşman tarafında! Seni tuzağa düşürdü. Ne yaparsın?",
      backgroundImage: `${theme}_betrayal.jpg`,
      choices: [
        {
          text: "Savaş",
          next: "fight_betrayer",
          diceRoll: { type: "d20", target: 15, skill: "Combat" },
          effect: { karma: 10 }
        },
        {
          text: "Kaç",
          next: "escape_betrayal",
          diceRoll: { type: "d20", target: 12, skill: "Athletics" }
        },
        {
          text: "Konuşmaya çalış",
          next: "talk_to_betrayer",
          diceRoll: { type: "d20", target: 18, skill: "Persuasion" }
        },
        {
          text: "Yardım iste",
          next: "call_for_help",
          diceRoll: { type: "d20", target: 14, skill: "Charisma" }
        }
      ],
      npcs: [],
      enemies: [{
        name: "İhanetçi NPC",
        type: "Betrayer",
        hp: 50,
        attack: 15,
        defense: 12,
        specialAbilities: ["Deception", "Stealth"],
        statusEffects: ["Poisoned", "Confused"]
      }],
      items: [],
      combat: true,
      ending: false,
      plotTwist: true,
      betrayal: true,
      randomEvent: false
    });

    return nodes;
  }

  private createBetrayalNodes(theme: string): ComprehensiveScenarioNode[] {
    const nodes: ComprehensiveScenarioNode[] = [];
    
    // Komutan ihaneti
    nodes.push({
      id: "commander_betrayal",
      title: "Komutanın İhaneti",
      text: "Komutanın aslında düşmanla işbirliği yaptığını öğrendin! Tüm planlar yanlış. Ne yaparsın?",
      backgroundImage: `${theme}_commander_betrayal.jpg`,
      choices: [
        {
          text: "Komutanı tutukla",
          next: "arrest_commander",
          diceRoll: { type: "d20", target: 16, skill: "Intimidation" }
        },
        {
          text: "Diğer askerleri uyar",
          next: "warn_soldiers",
          diceRoll: { type: "d20", target: 14, skill: "Persuasion" }
        },
        {
          text: "Gizli operasyon yap",
          next: "secret_operation",
          diceRoll: { type: "d20", target: 18, skill: "Stealth" }
        },
        {
          text: "Kaç ve rapor et",
          next: "escape_and_report",
          effect: { karma: 5 }
        }
      ],
      npcs: [{
        name: "İhanetçi Komutan",
        type: "Commander",
        personality: "Deceptive",
        motivation: "Power",
        relationship: "enemy",
        betrayal: true
      }],
      enemies: [],
      items: [],
      combat: false,
      ending: false,
      plotTwist: true,
      betrayal: true,
      randomEvent: false
    });

    return nodes;
  }

  private createRandomEventNodes(theme: string): ComprehensiveScenarioNode[] {
    const nodes: ComprehensiveScenarioNode[] = [];
    
    // Meteor yağmuru
    nodes.push({
      id: "meteor_shower",
      title: "Meteor Yağmuru",
      text: "Gökyüzünden meteorlar yağıyor! Dünya yanıyor, yaratıklar panik halinde. Ne yaparsın?",
      backgroundImage: `${theme}_meteor_shower.jpg`,
      choices: [
        {
          text: "Sığınak ara",
          next: "find_shelter",
          diceRoll: { type: "d20", target: 12, skill: "Survival" }
        },
        {
          text: "Meteorları incele",
          next: "examine_meteors",
          diceRoll: { type: "d20", target: 15, skill: "Arcana" }
        },
        {
          text: "Yaratıkları kurtar",
          next: "save_creatures",
          effect: { karma: 10 }
        },
        {
          text: "Kaç",
          next: "escape_meteor_shower",
          diceRoll: { type: "d20", target: 10, skill: "Athletics" }
        }
      ],
      npcs: [],
      enemies: [],
      items: [],
      combat: false,
      ending: false,
      plotTwist: false,
      betrayal: false,
      randomEvent: true
    });

    return nodes;
  }

  private createCombatNodes(theme: string, difficulty: string): ComprehensiveScenarioNode[] {
    const nodes: ComprehensiveScenarioNode[] = [];
    
    // Ana savaş sahnesi
    nodes.push({
      id: "main_combat",
      title: "Ana Savaş",
      text: "Düşmanla karşı karşıyasın! Savaş başlıyor. Ne yaparsın?",
      backgroundImage: `${theme}_combat.jpg`,
      choices: [
        {
          text: "Saldır",
          next: "attack_enemy",
          diceRoll: { type: "d20", target: 14, skill: "Combat" }
        },
        {
          text: "Savun",
          next: "defend_against_enemy",
          diceRoll: { type: "d20", target: 12, skill: "Defense" }
        },
        {
          text: "Özel yetenek kullan",
          next: "use_special_ability",
          diceRoll: { type: "d20", target: 16, skill: "Arcana" }
        },
        {
          text: "Kaç",
          next: "escape_from_combat",
          diceRoll: { type: "d20", target: 13, skill: "Athletics" }
        }
      ],
      npcs: [],
      enemies: [{
        name: "Ana Düşman",
        type: "Boss",
        hp: difficulty === "hard" ? 100 : 60,
        attack: difficulty === "hard" ? 20 : 15,
        defense: difficulty === "hard" ? 18 : 12,
        specialAbilities: ["Fire Breath", "Teleport", "Summon Minions"],
        statusEffects: ["Burning", "Stunned", "Poisoned"]
      }],
      items: [],
      combat: true,
      ending: false,
      plotTwist: false,
      betrayal: false,
      randomEvent: false
    });

    return nodes;
  }

  private createEndingNodes(theme: string): ComprehensiveScenarioNode[] {
    const nodes: ComprehensiveScenarioNode[] = [];
    
    // Zafer sonu
    nodes.push({
      id: "victory_ending",
      title: "Zafer",
      text: "Düşmanı yendin! Kahraman oldun. Şehir kurtuldu ve sen ödüllendirildin.",
      backgroundImage: `${theme}_victory.jpg`,
      choices: [
        {
          text: "Ödülü kabul et",
          next: "accept_reward",
          effect: { karma: 15, item: "Legendary Weapon" }
        },
        {
          text: "Yeni maceraya çık",
          next: "start_new_adventure",
          effect: { karma: 10 }
        },
        {
          text: "Eve dön",
          next: "return_home",
          effect: { karma: 5 }
        }
      ],
      npcs: [],
      enemies: [],
      items: ["Legendary Weapon", "Gold", "Experience"],
      combat: false,
      ending: true,
      plotTwist: false,
      betrayal: false,
      randomEvent: false
    });

    // Trajik son
    nodes.push({
      id: "tragic_ending",
      title: "Trajik Son",
      text: "Savaşı kaybettin ama şehir kurtuldu. Arkadaşların öldü ama sen hayatta kaldın.",
      backgroundImage: `${theme}_tragic.jpg`,
      choices: [
        {
          text: "Yas tut",
          next: "mourn_losses",
          effect: { karma: 5 }
        },
        {
          text: "İntikam al",
          next: "seek_revenge",
          effect: { karma: -5 }
        },
        {
          text: "Yeni başlangıç yap",
          next: "new_beginning",
          effect: { karma: 0 }
        }
      ],
      npcs: [],
      enemies: [],
      items: [],
      combat: false,
      ending: true,
      plotTwist: false,
      betrayal: false,
      randomEvent: false
    });

    return nodes;
  }

  // Background image mapping
  getBackgroundImageForNode(nodeId: string, theme: string): string {
    const imageMap: { [key: string]: string } = {
      opening_scene: `${theme}_opening.jpg`,
      explore_environment: `${theme}_exploration.jpg`,
      npc_encounter: `${theme}_npc_encounter.jpg`,
      npc_betrayal: `${theme}_betrayal.jpg`,
      commander_betrayal: `${theme}_commander_betrayal.jpg`,
      meteor_shower: `${theme}_meteor_shower.jpg`,
      main_combat: `${theme}_combat.jpg`,
      victory_ending: `${theme}_victory.jpg`,
      tragic_ending: `${theme}_tragic.jpg`
    };

    return imageMap[nodeId] || `${theme}_default.jpg`;
  }
} 