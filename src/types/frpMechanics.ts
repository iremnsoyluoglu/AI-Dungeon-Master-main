import { FRPRPGScenario } from "./frpMechanics";

export interface FRPMechanics {
  npcInteractions: NPCInteraction[];
  decisionPoints: DecisionPoint[];
  combatSystem: CombatSystem;
  diceMechanics: DiceMechanics;
}

export interface NPCInteraction {
  id: string;
  name: string;
  dialogue: string;
  personality: string;
  role: string;
  dialogueOptions: DialogueOption[];
  consequences: Consequence[];
}

export interface DialogueOption {
  text: string;
  requiredSkill?: string;
  requiredStat?: string;
  diceRoll?: string;
  consequences: Consequence;
}

export interface Consequence {
  immediate: string;
  longTerm: string;
  skillCheck?: {
    skill: string;
    difficulty: number;
    success: string;
    failure: string;
  };
}

export interface DecisionPoint {
  id: string;
  title: string;
  description: string;
  choices: Choice[];
  requiredSkill?: string;
  requiredStat?: string;
  diceRoll?: string;
}

export interface Choice {
  text: string;
  requiredSkill?: string;
  requiredStat?: string;
  diceRoll?: string;
  consequences: Consequence;
  nextScene?: string;
}

export interface CombatSystem {
  initiativeSystem: InitiativeSystem;
  combatActions: CombatAction[];
  statusEffects: StatusEffect[];
  victoryConditions: VictoryCondition[];
  defeatConditions: DefeatCondition[];
  rewards: Reward[];
  penalties: Penalty[];
}

export interface InitiativeSystem {
  order: string[]; // Character IDs in initiative order
  currentRound: number;
  currentTurn: number;
  roundActions: RoundAction[];
}

export interface RoundAction {
  round: number;
  turn: number;
  characterId: string;
  action: CombatAction;
  diceRoll?: DiceRoll;
  result: string;
  statusEffectsApplied: StatusEffect[];
}

export interface CombatAction {
  id: string;
  name: string;
  type: "attack" | "defend" | "special" | "item" | "spell";
  description: string;
  diceRoll: DiceRoll;
  damageCalculation: DamageCalculation;
  statusEffects?: StatusEffect[];
  cooldown?: number;
  requirements?: {
    skill?: string;
    stat?: string;
    item?: string;
  };
}

export interface DiceRoll {
  diceType: string; // 'd6', 'd20', etc.
  numberOfDice: number;
  modifier: number;
  targetNumber?: number;
  advantage?: boolean;
  disadvantage?: boolean;
}

export interface DamageCalculation {
  baseDamage: number;
  diceRoll: DiceRoll;
  modifiers: {
    strength?: number;
    weapon?: number;
    magic?: number;
    critical?: number;
  };
  statusEffects?: StatusEffect[];
}

export interface StatusEffect {
  id: string;
  name: string;
  type: "buff" | "debuff" | "neutral";
  description: string;
  duration: number; // rounds
  effects: {
    hp?: number;
    attack?: number;
    defense?: number;
    speed?: number;
    accuracy?: number;
    resistance?: string[];
  };
  visualEffect?: string;
  removalCondition?: string;
}

export interface VictoryCondition {
  id: string;
  type:
    | "defeat_all_enemies"
    | "reach_location"
    | "complete_objective"
    | "survive_rounds";
  description: string;
  requirements: string[];
}

export interface DefeatCondition {
  id: string;
  type: "party_defeated" | "time_limit" | "objective_failed";
  description: string;
  requirements: string[];
}

export interface Reward {
  id: string;
  type: "experience" | "gold" | "item" | "skill_point" | "stat_increase";
  value: number;
  description: string;
}

export interface Penalty {
  id: string;
  type: "damage" | "status_effect" | "item_loss" | "stat_decrease";
  value: number;
  description: string;
}

export interface DiceMechanics {
  diceTypes: string[];
  customDice: CustomDice[];
  probabilityTables: ProbabilityTable[];
  criticalRules: {
    natural20: string;
    natural1: string;
    criticalRange: number[];
  };
}

export interface CustomDice {
  name: string;
  sides: number;
  faces: string[];
  specialRules: string[];
}

export interface ProbabilityTable {
  name: string;
  diceRoll: DiceRoll;
  outcomes: {
    range: [number, number];
    result: string;
    probability: number;
  }[];
}

export interface FRPRPGScenario {
  title: string;
  theme: string;
  difficulty: string;
  scenes: FRPScene[];
  npcs: NPCInteraction[];
  combatEncounters: CombatEncounter[];
  diceMechanics: DiceMechanics;
}

export interface FRPScene {
  id: string;
  title: string;
  description: string;
  npcs: NPCInteraction[];
  decisionPoints: DecisionPoint[];
  combatEncounter?: CombatEncounter;
  rewards: Reward[];
  nextScenes: string[];
  environment: {
    name: string;
    description: string;
    effects: StatusEffect[];
    hazards: string[];
  };
}

export interface CombatEncounter {
  id: string;
  title: string;
  description: string;
  enemies: Enemy[];
  environment: {
    name: string;
    description: string;
    effects: StatusEffect[];
    hazards: string[];
  };
  initiativeSystem: InitiativeSystem;
  victoryConditions: VictoryCondition[];
  defeatConditions: DefeatCondition[];
  rewards: Reward[];
  penalties: Penalty[];
  rounds: CombatRound[];
}

export interface Enemy {
  id: string;
  name: string;
  hp: number;
  maxHp: number;
  attack: number;
  defense: number;
  speed: number;
  initiative: number;
  specialAbilities: CombatAction[];
  statusEffects: StatusEffect[];
  loot: Reward[];
  experience: number;
  description: string;
  aiBehavior: {
    aggressive: boolean;
    defensive: boolean;
    tactical: boolean;
    specialAbilityUsage: string;
  };
}

export interface CombatRound {
  roundNumber: number;
  turns: CombatTurn[];
  statusEffects: StatusEffect[];
  environmentalEffects: StatusEffect[];
}

export interface CombatTurn {
  turnNumber: number;
  characterId: string;
  action: CombatAction;
  diceRoll: DiceRoll;
  result: string;
  damageDealt?: number;
  statusEffectsApplied: StatusEffect[];
  statusEffectsRemoved: StatusEffect[];
}

export interface SkillTree {
  id: string;
  name: string;
  description: string;
  class: string;
  skills: SkillNode[];
  maxSkillPoints: number;
  currentSkillPoints: number;
}

export interface SkillNode {
  id: string;
  name: string;
  description: string;
  icon: string;
  level: number;
  maxLevel: number;
  cost: number;
  requirements: SkillRequirement[];
  effects: SkillEffect[];
  isUnlocked: boolean;
  isMaxed: boolean;
}

export interface SkillRequirement {
  type: "level" | "skill" | "stat";
  value: string | number;
  description: string;
}

export interface SkillEffect {
  type: "stat_boost" | "ability_unlock" | "passive_effect" | "active_ability";
  target: string;
  value: number;
  description: string;
}

// Fantasy Classes Skill Trees
export const FANTASY_SKILL_TREES: SkillTree[] = [
  {
    id: "warrior_combat",
    name: "Savaşçı Savaş Ağacı",
    description:
      "Savaşçıların fiziksel savaş yeteneklerini geliştiren skill ağacı",
    class: "warrior",
    maxSkillPoints: 20,
    currentSkillPoints: 0,
    skills: [
      {
        id: "weapon_mastery",
        name: "Silah Ustalığı",
        description:
          "Tüm silahlarda +2 hasar bonusu. Seviye 3'te kritik vuruş şansı %10 artar.",
        icon: "⚔️",
        level: 0,
        maxLevel: 5,
        cost: 1,
        requirements: [
          { type: "level", value: 1, description: "Seviye 1 gerekli" },
        ],
        effects: [
          {
            type: "stat_boost",
            target: "damage",
            value: 2,
            description: "+2 hasar",
          },
          {
            type: "passive_effect",
            target: "critical_chance",
            value: 10,
            description: "Kritik vuruş şansı %10",
          },
        ],
        isUnlocked: true,
        isMaxed: false,
      },
      {
        id: "battle_rage",
        name: "Savaş Öfkesi",
        description:
          "HP %50'nin altındayken +5 hasar ve +3 savunma. Seviye 3'te öfke süresi uzar.",
        icon: "😤",
        level: 0,
        maxLevel: 3,
        cost: 2,
        requirements: [
          {
            type: "skill",
            value: "weapon_mastery",
            description: "Silah Ustalığı seviye 2 gerekli",
          },
        ],
        effects: [
          {
            type: "stat_boost",
            target: "damage",
            value: 5,
            description: "Düşük HP'de +5 hasar",
          },
          {
            type: "stat_boost",
            target: "defense",
            value: 3,
            description: "Düşük HP'de +3 savunma",
          },
        ],
        isUnlocked: false,
        isMaxed: false,
      },
      {
        id: "shield_wall",
        name: "Kalkan Duvarı",
        description:
          "Savunma modunda +5 savunma ve %20 hasar yansıtma. Seviye 3'te takım arkadaşlarını da korur.",
        icon: "🛡️",
        level: 0,
        maxLevel: 3,
        cost: 2,
        requirements: [
          { type: "level", value: 3, description: "Seviye 3 gerekli" },
        ],
        effects: [
          {
            type: "stat_boost",
            target: "defense",
            value: 5,
            description: "Savunma modunda +5",
          },
          {
            type: "passive_effect",
            target: "damage_reflection",
            value: 20,
            description: "%20 hasar yansıtma",
          },
        ],
        isUnlocked: false,
        isMaxed: false,
      },
    ],
  },
  {
    id: "mage_magic",
    name: "Büyücü Büyü Ağacı",
    description: "Büyücülerin büyü yeteneklerini geliştiren skill ağacı",
    class: "mage",
    maxSkillPoints: 20,
    currentSkillPoints: 0,
    skills: [
      {
        id: "elemental_mastery",
        name: "Element Ustalığı",
        description:
          "Ateş, buz ve şimşek büyülerinde +3 hasar. Seviye 3'te büyü maliyeti %20 azalır.",
        icon: "🔥",
        level: 0,
        maxLevel: 5,
        cost: 1,
        requirements: [
          { type: "level", value: 1, description: "Seviye 1 gerekli" },
        ],
        effects: [
          {
            type: "stat_boost",
            target: "magic_damage",
            value: 3,
            description: "+3 büyü hasarı",
          },
          {
            type: "passive_effect",
            target: "mana_cost_reduction",
            value: 20,
            description: "Büyü maliyeti %20 azalır",
          },
        ],
        isUnlocked: true,
        isMaxed: false,
      },
      {
        id: "arcane_burst",
        name: "Arcane Patlama",
        description:
          "Tüm düşmanlara hasar veren alan büyüsü. Seviye 3'te sersemletme efekti eklenir.",
        icon: "💥",
        level: 0,
        maxLevel: 3,
        cost: 3,
        requirements: [
          {
            type: "skill",
            value: "elemental_mastery",
            description: "Element Ustalığı seviye 3 gerekli",
          },
        ],
        effects: [
          {
            type: "ability_unlock",
            target: "arcane_burst",
            value: 1,
            description: "Arcane Patlama büyüsü açılır",
          },
          {
            type: "passive_effect",
            target: "stun_chance",
            value: 30,
            description: "%30 sersemletme şansı",
          },
        ],
        isUnlocked: false,
        isMaxed: false,
      },
      {
        id: "mana_shield",
        name: "Mana Kalkanı",
        description:
          "Mana kullanarak hasar engelleme. Seviye 3'te otomatik aktif olur.",
        icon: "🔮",
        level: 0,
        maxLevel: 3,
        cost: 2,
        requirements: [
          { type: "level", value: 5, description: "Seviye 5 gerekli" },
        ],
        effects: [
          {
            type: "ability_unlock",
            target: "mana_shield",
            value: 1,
            description: "Mana Kalkanı açılır",
          },
          {
            type: "passive_effect",
            target: "auto_shield",
            value: 1,
            description: "Otomatik kalkan",
          },
        ],
        isUnlocked: false,
        isMaxed: false,
      },
    ],
  },
  {
    id: "rogue_stealth",
    name: "Hırsız Gizlilik Ağacı",
    description:
      "Hırsızların gizlilik ve kritik vuruş yeteneklerini geliştiren skill ağacı",
    class: "rogue",
    maxSkillPoints: 20,
    currentSkillPoints: 0,
    skills: [
      {
        id: "stealth_mastery",
        name: "Gizlilik Ustalığı",
        description:
          "Gizlilik modunda %50 daha az tespit edilme. Seviye 3'te gizlilik sırasında +5 hasar.",
        icon: "👤",
        level: 0,
        maxLevel: 5,
        cost: 1,
        requirements: [
          { type: "level", value: 1, description: "Seviye 1 gerekli" },
        ],
        effects: [
          {
            type: "passive_effect",
            target: "stealth_bonus",
            value: 50,
            description: "%50 gizlilik bonusu",
          },
          {
            type: "stat_boost",
            target: "stealth_damage",
            value: 5,
            description: "Gizlilik sırasında +5 hasar",
          },
        ],
        isUnlocked: true,
        isMaxed: false,
      },
      {
        id: "backstab",
        name: "Sırtından Vuruş",
        description:
          "Gizlilik sırasında %200 kritik hasar. Seviye 3'te %50 şansla sersemletme.",
        icon: "🗡️",
        level: 0,
        maxLevel: 3,
        cost: 2,
        requirements: [
          {
            type: "skill",
            value: "stealth_mastery",
            description: "Gizlilik Ustalığı seviye 2 gerekli",
          },
        ],
        effects: [
          {
            type: "passive_effect",
            target: "backstab_damage",
            value: 200,
            description: "%200 kritik hasar",
          },
          {
            type: "passive_effect",
            target: "backstab_stun",
            value: 50,
            description: "%50 sersemletme şansı",
          },
        ],
        isUnlocked: false,
        isMaxed: false,
      },
      {
        id: "poison_mastery",
        name: "Zehir Ustalığı",
        description:
          "Zehirli silahlar %50 daha etkili. Seviye 3'te yeni zehir türleri açılır.",
        icon: "☠️",
        level: 0,
        maxLevel: 3,
        cost: 2,
        requirements: [
          { type: "level", value: 4, description: "Seviye 4 gerekli" },
        ],
        effects: [
          {
            type: "passive_effect",
            target: "poison_effectiveness",
            value: 50,
            description: "Zehir etkinliği %50 artar",
          },
          {
            type: "ability_unlock",
            target: "advanced_poisons",
            value: 1,
            description: "Gelişmiş zehirler açılır",
          },
        ],
        isUnlocked: false,
        isMaxed: false,
      },
    ],
  },
  {
    id: "priest_healing",
    name: "Rahip İyileştirme Ağacı",
    description:
      "Rahiplerin iyileştirme ve koruma yeteneklerini geliştiren skill ağacı",
    class: "priest",
    maxSkillPoints: 20,
    currentSkillPoints: 0,
    skills: [
      {
        id: "healing_mastery",
        name: "İyileştirme Ustalığı",
        description:
          "İyileştirme büyülerinde +5 HP ve %20 daha az mana maliyeti.",
        icon: "💚",
        level: 0,
        maxLevel: 5,
        cost: 1,
        requirements: [
          { type: "level", value: 1, description: "Seviye 1 gerekli" },
        ],
        effects: [
          {
            type: "stat_boost",
            target: "healing_power",
            value: 5,
            description: "+5 iyileştirme gücü",
          },
          {
            type: "passive_effect",
            target: "healing_cost_reduction",
            value: 20,
            description: "İyileştirme maliyeti %20 azalır",
          },
        ],
        isUnlocked: true,
        isMaxed: false,
      },
      {
        id: "divine_protection",
        name: "İlahi Koruma",
        description:
          "Takım arkadaşlarına +3 savunma veren koruma büyüsü. Seviye 3'te süre uzar.",
        icon: "✨",
        level: 0,
        maxLevel: 3,
        cost: 2,
        requirements: [
          {
            type: "skill",
            value: "healing_mastery",
            description: "İyileştirme Ustalığı seviye 2 gerekli",
          },
        ],
        effects: [
          {
            type: "ability_unlock",
            target: "divine_protection",
            value: 1,
            description: "İlahi Koruma büyüsü açılır",
          },
          {
            type: "stat_boost",
            target: "team_defense",
            value: 3,
            description: "Takım +3 savunma",
          },
        ],
        isUnlocked: false,
        isMaxed: false,
      },
      {
        id: "resurrection",
        name: "Diriliş",
        description:
          "Ölen takım arkadaşını canlandırma büyüsü. Seviye 3'te %50 HP ile canlanır.",
        icon: "🔄",
        level: 0,
        maxLevel: 3,
        cost: 5,
        requirements: [
          { type: "level", value: 10, description: "Seviye 10 gerekli" },
        ],
        effects: [
          {
            type: "ability_unlock",
            target: "resurrection",
            value: 1,
            description: "Diriliş büyüsü açılır",
          },
          {
            type: "passive_effect",
            target: "resurrection_hp",
            value: 50,
            description: "%50 HP ile canlanma",
          },
        ],
        isUnlocked: false,
        isMaxed: false,
      },
    ],
  },
];

// Warhammer Classes Skill Trees
export const WARHAMMER_SKILL_TREES: SkillTree[] = [
  {
    id: "space_marine_combat",
    name: "Space Marine Savaş Ağacı",
    description:
      "Space Marine'ların güçlü savaş yeteneklerini geliştiren skill ağacı",
    class: "space_marine",
    maxSkillPoints: 20,
    currentSkillPoints: 0,
    skills: [
      {
        id: "power_armor_mastery",
        name: "Güç Zırhı Ustalığı",
        description:
          "Güç zırhı ile +8 savunma ve +5 hasar. Seviye 3'te enerji kalkanı açılır.",
        icon: "🛡️",
        level: 0,
        maxLevel: 5,
        cost: 1,
        requirements: [
          { type: "level", value: 1, description: "Seviye 1 gerekli" },
        ],
        effects: [
          {
            type: "stat_boost",
            target: "defense",
            value: 8,
            description: "+8 savunma",
          },
          {
            type: "stat_boost",
            target: "damage",
            value: 5,
            description: "+5 hasar",
          },
        ],
        isUnlocked: true,
        isMaxed: false,
      },
      {
        id: "chainsword_expertise",
        name: "Zincir Kılıç Uzmanlığı",
        description:
          "Zincir kılıç ile %150 hasar ve %30 kanama şansı. Seviye 3'te çoklu hedef.",
        icon: "⚔️",
        level: 0,
        maxLevel: 3,
        cost: 2,
        requirements: [
          {
            type: "skill",
            value: "power_armor_mastery",
            description: "Güç Zırhı Ustalığı seviye 2 gerekli",
          },
        ],
        effects: [
          {
            type: "passive_effect",
            target: "chainsword_damage",
            value: 150,
            description: "%150 hasar",
          },
          {
            type: "passive_effect",
            target: "bleeding_chance",
            value: 30,
            description: "%30 kanama şansı",
          },
        ],
        isUnlocked: false,
        isMaxed: false,
      },
      {
        id: "bolter_mastery",
        name: "Bolter Ustalığı",
        description:
          "Bolter ile uzaktan saldırı +6 hasar. Seviye 3'te patlama hasarı eklenir.",
        icon: "🔫",
        level: 0,
        maxLevel: 3,
        cost: 2,
        requirements: [
          { type: "level", value: 3, description: "Seviye 3 gerekli" },
        ],
        effects: [
          {
            type: "stat_boost",
            target: "ranged_damage",
            value: 6,
            description: "+6 uzaktan hasar",
          },
          {
            type: "passive_effect",
            target: "explosive_damage",
            value: 1,
            description: "Patlama hasarı",
          },
        ],
        isUnlocked: false,
        isMaxed: false,
      },
    ],
  },
  {
    id: "tech_priest_technology",
    name: "Tech Priest Teknoloji Ağacı",
    description:
      "Tech Priest'lerin teknoloji ve makine kontrol yeteneklerini geliştiren skill ağacı",
    class: "tech_priest",
    maxSkillPoints: 20,
    currentSkillPoints: 0,
    skills: [
      {
        id: "machine_spirit_communion",
        name: "Makine Ruhu İletişimi",
        description:
          "Makinelerle iletişim kurma ve kontrol etme. Seviye 3'te uzaktan kontrol.",
        icon: "🤖",
        level: 0,
        maxLevel: 5,
        cost: 1,
        requirements: [
          { type: "level", value: 1, description: "Seviye 1 gerekli" },
        ],
        effects: [
          {
            type: "ability_unlock",
            target: "machine_control",
            value: 1,
            description: "Makine kontrolü açılır",
          },
          {
            type: "passive_effect",
            target: "remote_control",
            value: 1,
            description: "Uzaktan kontrol",
          },
        ],
        isUnlocked: true,
        isMaxed: false,
      },
      {
        id: "plasma_weaponry",
        name: "Plazma Silahları",
        description:
          "Plazma silahları ile +8 hasar ve %40 yanma şansı. Seviye 3'te aşırı ısınma koruması.",
        icon: "⚡",
        level: 0,
        maxLevel: 3,
        cost: 2,
        requirements: [
          {
            type: "skill",
            value: "machine_spirit_communion",
            description: "Makine Ruhu İletişimi seviye 2 gerekli",
          },
        ],
        effects: [
          {
            type: "stat_boost",
            target: "plasma_damage",
            value: 8,
            description: "+8 plazma hasarı",
          },
          {
            type: "passive_effect",
            target: "burn_chance",
            value: 40,
            description: "%40 yanma şansı",
          },
        ],
        isUnlocked: false,
        isMaxed: false,
      },
      {
        id: "servitor_control",
        name: "Servitor Kontrolü",
        description:
          "Servitor'ları kontrol etme ve yönlendirme. Seviye 3'te çoklu servitor kontrolü.",
        icon: "👾",
        level: 0,
        maxLevel: 3,
        cost: 3,
        requirements: [
          { type: "level", value: 5, description: "Seviye 5 gerekli" },
        ],
        effects: [
          {
            type: "ability_unlock",
            target: "servitor_control",
            value: 1,
            description: "Servitor kontrolü açılır",
          },
          {
            type: "passive_effect",
            target: "multiple_servitors",
            value: 1,
            description: "Çoklu servitor kontrolü",
          },
        ],
        isUnlocked: false,
        isMaxed: false,
      },
    ],
  },
  {
    id: "inquisitor_investigation",
    name: "Inquisitor Araştırma Ağacı",
    description:
      "Inquisitor'ların araştırma ve psikik yeteneklerini geliştiren skill ağacı",
    class: "inquisitor",
    maxSkillPoints: 20,
    currentSkillPoints: 0,
    skills: [
      {
        id: "psychic_mastery",
        name: "Psikik Ustalık",
        description:
          "Psikik güçler ile +6 hasar ve %30 sersemletme. Seviye 3'te zihin kontrolü.",
        icon: "🧠",
        level: 0,
        maxLevel: 5,
        cost: 1,
        requirements: [
          { type: "level", value: 1, description: "Seviye 1 gerekli" },
        ],
        effects: [
          {
            type: "stat_boost",
            target: "psychic_damage",
            value: 6,
            description: "+6 psikik hasar",
          },
          {
            type: "passive_effect",
            target: "psychic_stun",
            value: 30,
            description: "%30 psikik sersemletme",
          },
        ],
        isUnlocked: true,
        isMaxed: false,
      },
      {
        id: "truth_seeker",
        name: "Gerçek Arayıcısı",
        description:
          "Yalanları tespit etme ve gizli bilgileri ortaya çıkarma. Seviye 3'te zihin okuma.",
        icon: "🔍",
        level: 0,
        maxLevel: 3,
        cost: 2,
        requirements: [
          {
            type: "skill",
            value: "psychic_mastery",
            description: "Psikik Ustalık seviye 2 gerekli",
          },
        ],
        effects: [
          {
            type: "ability_unlock",
            target: "lie_detection",
            value: 1,
            description: "Yalan tespiti açılır",
          },
          {
            type: "ability_unlock",
            target: "mind_reading",
            value: 1,
            description: "Zihin okuma açılır",
          },
        ],
        isUnlocked: false,
        isMaxed: false,
      },
      {
        id: "exterminatus",
        name: "Exterminatus",
        description: "Güçlü yok etme büyüsü. Seviye 3'te alan hasarı artar.",
        icon: "💀",
        level: 0,
        maxLevel: 3,
        cost: 5,
        requirements: [
          { type: "level", value: 15, description: "Seviye 15 gerekli" },
        ],
        effects: [
          {
            type: "ability_unlock",
            target: "exterminatus",
            value: 1,
            description: "Exterminatus büyüsü açılır",
          },
          {
            type: "passive_effect",
            target: "area_damage",
            value: 200,
            description: "%200 alan hasarı",
          },
        ],
        isUnlocked: false,
        isMaxed: false,
      },
    ],
  },
  {
    id: "imperial_guard_tactics",
    name: "Imperial Guard Taktik Ağacı",
    description:
      "Imperial Guard'ların taktiksel savaş yeteneklerini geliştiren skill ağacı",
    class: "imperial_guard",
    maxSkillPoints: 20,
    currentSkillPoints: 0,
    skills: [
      {
        id: "squad_tactics",
        name: "Manga Taktikleri",
        description:
          "Takım arkadaşları ile +3 koordinasyon ve +2 hasar. Seviye 3'te taktiksel pozisyon.",
        icon: "👥",
        level: 0,
        maxLevel: 5,
        cost: 1,
        requirements: [
          { type: "level", value: 1, description: "Seviye 1 gerekli" },
        ],
        effects: [
          {
            type: "stat_boost",
            target: "team_coordination",
            value: 3,
            description: "+3 takım koordinasyonu",
          },
          {
            type: "stat_boost",
            target: "team_damage",
            value: 2,
            description: "+2 takım hasarı",
          },
        ],
        isUnlocked: true,
        isMaxed: false,
      },
      {
        id: "lasgun_mastery",
        name: "Lasgun Ustalığı",
        description:
          "Lasgun ile +4 hasar ve %25 isabet şansı. Seviye 3'te otomatik ateş.",
        icon: "🔫",
        level: 0,
        maxLevel: 3,
        cost: 2,
        requirements: [
          {
            type: "skill",
            value: "squad_tactics",
            description: "Manga Taktikleri seviye 2 gerekli",
          },
        ],
        effects: [
          {
            type: "stat_boost",
            target: "lasgun_damage",
            value: 4,
            description: "+4 lasgun hasarı",
          },
          {
            type: "passive_effect",
            target: "accuracy_bonus",
            value: 25,
            description: "%25 isabet bonusu",
          },
        ],
        isUnlocked: false,
        isMaxed: false,
      },
      {
        id: "defensive_positioning",
        name: "Savunma Pozisyonu",
        description:
          "Savunma modunda +6 savunma ve %40 hasar engelleme. Seviye 3'te takım koruması.",
        icon: "🏰",
        level: 0,
        maxLevel: 3,
        cost: 2,
        requirements: [
          { type: "level", value: 4, description: "Seviye 4 gerekli" },
        ],
        effects: [
          {
            type: "stat_boost",
            target: "defense",
            value: 6,
            description: "+6 savunma",
          },
          {
            type: "passive_effect",
            target: "damage_reduction",
            value: 40,
            description: "%40 hasar engelleme",
          },
        ],
        isUnlocked: false,
        isMaxed: false,
      },
    ],
  },
];
