import { ComprehensiveScenarioNode } from './ComprehensiveScenarioGenerator';

export interface Ending {
  id: string;
  title: string;
  description: string;
  type: 'victory' | 'tragic' | 'betrayal' | 'mystery' | 'sacrifice' | 'redemption' | 'corruption' | 'escape';
  requirements: {
    karma?: number;
    choices?: string[];
    items?: string[];
    relationships?: string[];
    hidden_flags?: string[];
  };
  consequences: {
    karma_change: number;
    item_rewards?: string[];
    relationship_changes?: { [key: string]: string };
    hidden_flags?: string[];
    unlock_content?: string[];
  };
  backgroundImage?: string;
  cinematic_description: string;
  epilogue?: string;
}

export interface HiddenFlag {
  id: string;
  name: string;
  description: string;
  trigger_conditions: string[];
  effects: string[];
}

export class MultipleEndingGenerator {
  private hiddenFlags: Map<string, HiddenFlag> = new Map();
  private endingTemplates: { [type: string]: string[] } = {
    victory: [
      "Kahraman olarak şehri kurtardın",
      "Büyük zafer kazandın",
      "Efsanevi başarı elde ettin",
      "Tüm tehditleri ortadan kaldırdın"
    ],
    tragic: [
      "Zafer kazandın ama büyük bedel ödedin",
      "Hayatta kaldın ama her şeyi kaybettin",
      "Görev tamamlandı ama arkadaşların öldü",
      "Başarılı oldun ama kalbin kırıldı"
    ],
    betrayal: [
      "Güvendiğin kişi seni ihanet etti",
      "Müttefikin aslında düşmandı",
      "Yardım ettiğin kişi seni tuzağa düşürdü",
      "Dost sandığın kişi gizli plan yapıyordu"
    ],
    mystery: [
      "Gizli gerçeği keşfettin",
      "Bilinmeyen bir sır ortaya çıktı",
      "Eski bir gizem çözüldü",
      "Karanlık bir sır aydınlandı"
    ],
    sacrifice: [
      "Başkaları için kendini feda ettin",
      "Şehri kurtarmak için hayatını verdin",
      "Sevdiklerin için kendini kurban ettin",
      "Büyük bedel ödedin ama kazandın"
    ],
    redemption: [
      "Geçmiş hatalarını telafi ettin",
      "Karanlık geçmişinden kurtuldun",
      "Yeni bir başlangıç yaptın",
      "İkinci şansı değerlendirdin"
    ],
    corruption: [
      "Güç seni bozdu",
      "Karanlık tarafa geçtin",
      "Kötülük seni ele geçirdi",
      "Güç uğruna her şeyi kaybettin"
    ],
    escape: [
      "Hayatta kaldın ama kaçtın",
      "Tehlikeden kurtuldun",
      "Savaştan çekildin",
      "Güvenli yere ulaştın"
    ]
  };

  constructor() {
    this.initializeHiddenFlags();
  }

  private initializeHiddenFlags(): void {
    // Gizli bayraklar oluştur
    const flags = [
      {
        id: "secret_ally",
        name: "Gizli Müttefik",
        description: "Görünmeyen bir müttefikin var",
        trigger_conditions: ["help_npc", "give_item", "show_mercy"],
        effects: ["unlock_good_ending", "extra_rewards"]
      },
      {
        id: "hidden_enemy",
        name: "Gizli Düşman",
        description: "Güvendiğin biri aslında düşman",
        trigger_conditions: ["trust_everyone", "ignore_warnings", "blind_faith"],
        effects: ["unlock_betrayal_ending", "lose_items"]
      },
      {
        id: "ancient_knowledge",
        name: "Antik Bilgi",
        description: "Eski bir sır keşfettin",
        trigger_conditions: ["explore_ruins", "read_ancient_texts", "solve_puzzle"],
        effects: ["unlock_mystery_ending", "gain_power"]
      },
      {
        id: "dark_power",
        name: "Karanlık Güç",
        description: "Tehlikeli güç kullandın",
        trigger_conditions: ["use_dark_magic", "accept_corruption", "embrace_evil"],
        effects: ["unlock_corruption_ending", "lose_sanity"]
      },
      {
        id: "heroic_sacrifice",
        name: "Kahramanca Fedakarlık",
        description: "Başkaları için kendini feda ettin",
        trigger_conditions: ["save_others", "take_damage", "self_sacrifice"],
        effects: ["unlock_sacrifice_ending", "gain_respect"]
      },
      {
        id: "redemption_arc",
        name: "Kurtuluş Yolu",
        description: "Geçmiş hatalarını telafi ettin",
        trigger_conditions: ["help_enemy", "show_mercy", "change_ways"],
        effects: ["unlock_redemption_ending", "gain_forgiveness"]
      }
    ];

    flags.forEach(flag => {
      this.hiddenFlags.set(flag.id, flag);
    });
  }

  generateMultipleEndings(scenario: any): Ending[] {
    const endings: Ending[] = [];
    const theme = scenario.theme || 'fantasy';
    
    // Ana sonlar
    endings.push(this.createVictoryEnding(theme));
    endings.push(this.createTragicEnding(theme));
    endings.push(this.createBetrayalEnding(theme));
    endings.push(this.createMysteryEnding(theme));
    
    // Gizli sonlar
    endings.push(this.createSacrificeEnding(theme));
    endings.push(this.createRedemptionEnding(theme));
    endings.push(this.createCorruptionEnding(theme));
    endings.push(this.createEscapeEnding(theme));
    
    return endings;
  }

  private createVictoryEnding(theme: string): Ending {
    const descriptions = {
      fantasy: "Ejderhayı yendin ve krallığı kurtardın. Halk seni kahraman olarak görüyor.",
      warhammer40k: "Orkları püskürttün ve Hive şehrini kurtardın. İmparator seni ödüllendiriyor.",
      scifi: "Uzaylı istilasını durdurdun ve galaksiyi kurtardın. Federasyon seni onurlandırıyor.",
      cyberpunk: "Korporasyonları devirdin ve şehri özgürleştirdin. Halk seni lider olarak seçiyor.",
      post_apocalyptic: "Mutant sürüsünü yendin ve insanlığın son kalelerini kurtardın."
    };

    return {
      id: "victory_ending",
      title: "Zafer",
      description: descriptions[theme as keyof typeof descriptions] || "Büyük zafer kazandın!",
      type: "victory",
      requirements: {
        karma: 50,
        choices: ["fight_bravely", "help_others", "make_sacrifices"],
        items: ["heroic_weapon"],
        relationships: ["trusted_ally"]
      },
      consequences: {
        karma_change: 25,
        item_rewards: ["Legendary Weapon", "Hero's Medal", "Royal Favor"],
        relationship_changes: { "king": "ally", "people": "worshipped" },
        hidden_flags: ["hero_status"],
        unlock_content: ["victory_epilogue", "hero_statue"]
      },
      backgroundImage: `${theme}_victory.jpg`,
      cinematic_description: "Güneş doğarken, zaferin tadını çıkarıyorsun. Halk seni alkışlıyor ve gelecek parlak görünüyor.",
      epilogue: "Sen artık bir efsanesin. Hikayen nesiller boyunca anlatılacak."
    };
  }

  private createTragicEnding(theme: string): Ending {
    const descriptions = {
      fantasy: "Ejderhayı yendin ama en değerli arkadaşını kaybettin. Zafer acı bir tat bıraktı.",
      warhammer40k: "Orkları püskürttün ama birçok asker öldü. Mara da öldü. Zafer bedeli ağır oldu.",
      scifi: "Uzaylıları yendin ama geminin mürettebatının çoğu öldü. Yalnız kaldın.",
      cyberpunk: "Korporasyonları devirdin ama en yakın arkadaşın ihanet etti. Güven kaybettin.",
      post_apocalyptic: "Mutantları yendin ama ailen öldü. Hayatta kaldın ama yalnız kaldın."
    };

    return {
      id: "tragic_ending",
      title: "Trajik Zafer",
      description: descriptions[theme as keyof typeof descriptions] || "Zafer kazandın ama büyük bedel ödedin.",
      type: "tragic",
      requirements: {
        karma: 30,
        choices: ["sacrifice_others", "ignore_warnings", "rush_into_battle"],
        relationships: ["lost_ally"]
      },
      consequences: {
        karma_change: -10,
        relationship_changes: { "survivors": "grateful_but_sad" },
        hidden_flags: ["survivor_guilt"],
        unlock_content: ["tragic_epilogue", "memorial_scene"]
      },
      backgroundImage: `${theme}_tragic.jpg`,
      cinematic_description: "Zafer kazandın ama yüzünde acı var. Kayıpların anısı seni takip ediyor.",
      epilogue: "Zafer acı bir tat bıraktı. Belki bir gün bu acıyı unutabilirsin."
    };
  }

  private createBetrayalEnding(theme: string): Ending {
    const descriptions = {
      fantasy: "Güvendiğin büyücü aslında ejderhanın hizmetkârıydı. Seni tuzağa düşürdü.",
      warhammer40k: "Komutan Voss orklarla işbirliği yapıyordu. Tüm planlar yanlıştı.",
      scifi: "Gemideki mühendis uzaylıların ajanıydı. Seni yanlış yönlendirdi.",
      cyberpunk: "En yakın arkadaşın korporasyonların ajanıydı. Seni satmıştı.",
      post_apocalyptic: "Güvendiğin rehber mutantların lideriydi. Seni tuzağa düşürdü."
    };

    return {
      id: "betrayal_ending",
      title: "İhanet",
      description: descriptions[theme as keyof typeof descriptions] || "Güvendiğin kişi seni ihanet etti.",
      type: "betrayal",
      requirements: {
        karma: 20,
        choices: ["trust_everyone", "ignore_suspicious_behavior", "blind_faith"],
        hidden_flags: ["hidden_enemy"]
      },
      consequences: {
        karma_change: -20,
        relationship_changes: { "betrayer": "enemy", "others": "suspicious" },
        hidden_flags: ["trust_issues"],
        unlock_content: ["betrayal_epilogue", "revenge_quest"]
      },
      backgroundImage: `${theme}_betrayal.jpg`,
      cinematic_description: "Güvendiğin kişinin gerçek yüzünü gördün. İhanet acısı kalbini yakıyor.",
      epilogue: "Artık kimseye güvenemezsin. İhanet yarası derin."
    };
  }

  private createMysteryEnding(theme: string): Ending {
    const descriptions = {
      fantasy: "Antik tapınakta gizli bir sır keşfettin. Gerçek çok şaşırtıcı.",
      warhammer40k: "Hive'ın derinliklerinde eski bir teknoloji buldun. İmparatorluk bunu gizli tutmak istiyor.",
      scifi: "Uzaylı gemisinde insanlığın gerçek kökenini öğrendin. Şok edici gerçek.",
      cyberpunk: "Korporasyonların gizli dosyalarında toplumun gerçek yapısını gördün.",
      post_apocalyptic: "Mutantların aslında insanlığın evrimi olduğunu öğrendin."
    };

    return {
      id: "mystery_ending",
      title: "Gizli Gerçek",
      description: descriptions[theme as keyof typeof descriptions] || "Bilinmeyen bir sır keşfettin.",
      type: "mystery",
      requirements: {
        karma: 40,
        choices: ["explore_thoroughly", "investigate_clues", "solve_puzzles"],
        hidden_flags: ["ancient_knowledge"]
      },
      consequences: {
        karma_change: 15,
        item_rewards: ["Ancient Artifact", "Secret Knowledge"],
        hidden_flags: ["knows_truth"],
        unlock_content: ["mystery_epilogue", "secret_ending"]
      },
      backgroundImage: `${theme}_mystery.jpg`,
      cinematic_description: "Gerçeği öğrendin ama bu bilgi tehlikeli. Kimseye söyleyemezsin.",
      epilogue: "Bazen cehalet mutluluktur. Ama artık gerçeği biliyorsun."
    };
  }

  private createSacrificeEnding(theme: string): Ending {
    const descriptions = {
      fantasy: "Krallığı kurtarmak için kendini feda ettin. Sen bir efsane oldun.",
      warhammer40k: "Hive'ı kurtarmak için hayatını verdin. İmparator seni onurlandırıyor.",
      scifi: "Galaksiyi kurtarmak için gemiyi patlattın. Kahraman olarak anılıyorsun.",
      cyberpunk: "Şehri özgürleştirmek için kendini feda ettin. Halk seni unutmayacak.",
      post_apocalyptic: "İnsanlığın son umudunu kurtarmak için kendini kurban ettin."
    };

    return {
      id: "sacrifice_ending",
      title: "Kahramanca Fedakarlık",
      description: descriptions[theme as keyof typeof descriptions] || "Başkaları için kendini feda ettin.",
      type: "sacrifice",
      requirements: {
        karma: 80,
        choices: ["self_sacrifice", "save_others", "heroic_choice"],
        hidden_flags: ["heroic_sacrifice"]
      },
      consequences: {
        karma_change: 50,
        relationship_changes: { "everyone": "worshipped" },
        hidden_flags: ["immortal_legend"],
        unlock_content: ["sacrifice_epilogue", "hero_memorial"]
      },
      backgroundImage: `${theme}_sacrifice.jpg`,
      cinematic_description: "Son nefesini verirken, başkalarının güvenliğini sağladığını biliyorsun.",
      epilogue: "Sen artık ölümsüz bir efsanesin. Fedakarlığın asla unutulmayacak."
    };
  }

  private createRedemptionEnding(theme: string): Ending {
    const descriptions = {
      fantasy: "Geçmiş hatalarını telafi ettin. Yeni bir başlangıç yaptın.",
      warhammer40k: "Karanlık geçmişinden kurtuldun. İmparator seni affetti.",
      scifi: "Eski suçlarını telafi ettin. Federasyon seni yeniden kabul etti.",
      cyberpunk: "Korporasyon geçmişini unuttun. Halk seni affetti.",
      post_apocalyptic: "Mutant geçmişini aştın. İnsanlığa geri döndün."
    };

    return {
      id: "redemption_ending",
      title: "Kurtuluş",
      description: descriptions[theme as keyof typeof descriptions] || "Geçmiş hatalarını telafi ettin.",
      type: "redemption",
      requirements: {
        karma: 60,
        choices: ["help_enemy", "show_mercy", "change_ways"],
        hidden_flags: ["redemption_arc"]
      },
      consequences: {
        karma_change: 30,
        relationship_changes: { "former_enemies": "forgiven" },
        hidden_flags: ["redeemed_soul"],
        unlock_content: ["redemption_epilogue", "new_beginning"]
      },
      backgroundImage: `${theme}_redemption.jpg`,
      cinematic_description: "Geçmişinle yüzleştin ve yeni bir yol seçtin. Özgürsün.",
      epilogue: "İkinci şansını değerlendirdin. Artık temiz bir sayfa açabilirsin."
    };
  }

  private createCorruptionEnding(theme: string): Ending {
    const descriptions = {
      fantasy: "Güç seni bozdu. Karanlık tarafa geçtin.",
      warhammer40k: "Kaos'un gücü seni ele geçirdi. İmparatorluktan ayrıldın.",
      scifi: "Uzaylı teknolojisi seni değiştirdi. İnsanlığı terk ettin.",
      cyberpunk: "Korporasyon gücü seni bozdu. Halkı sattın.",
      post_apocalyptic: "Mutant gücü seni ele geçirdi. İnsanlığı unuttun."
    };

    return {
      id: "corruption_ending",
      title: "Yozlaşma",
      description: descriptions[theme as keyof typeof descriptions] || "Güç seni bozdu.",
      type: "corruption",
      requirements: {
        karma: -30,
        choices: ["use_dark_power", "accept_corruption", "embrace_evil"],
        hidden_flags: ["dark_power"]
      },
      consequences: {
        karma_change: -40,
        relationship_changes: { "former_allies": "enemies" },
        hidden_flags: ["corrupted_soul"],
        unlock_content: ["corruption_epilogue", "dark_path"]
      },
      backgroundImage: `${theme}_corruption.jpg`,
      cinematic_description: "Güç seni değiştirdi. Artık eski sen değilsin.",
      epilogue: "Karanlık yol seni bekliyor. Geri dönüş yok."
    };
  }

  private createEscapeEnding(theme: string): Ending {
    const descriptions = {
      fantasy: "Savaştan kaçtın. Hayatta kaldın ama onurunu kaybettin.",
      warhammer40k: "Hive'dan kaçtın. Hayatta kaldın ama görevini terk ettin.",
      scifi: "Gemiden kaçtın. Hayatta kaldın ama mürettebatı terk ettin.",
      cyberpunk: "Şehirden kaçtın. Hayatta kaldın ama halkı terk ettin.",
      post_apocalyptic: "Savaştan kaçtın. Hayatta kaldın ama insanlığı terk ettin."
    };

    return {
      id: "escape_ending",
      title: "Kaçış",
      description: descriptions[theme as keyof typeof descriptions] || "Tehlikeden kaçtın.",
      type: "escape",
      requirements: {
        karma: -20,
        choices: ["run_away", "avoid_conflict", "self_preservation"],
        relationships: ["abandoned_allies"]
      },
      consequences: {
        karma_change: -15,
        relationship_changes: { "abandoned": "despised" },
        hidden_flags: ["coward_status"],
        unlock_content: ["escape_epilogue", "shame_quest"]
      },
      backgroundImage: `${theme}_escape.jpg`,
      cinematic_description: "Tehlikeden kaçtın ama yüzünde utanç var. Onurunu kaybettin.",
      epilogue: "Hayatta kaldın ama onurunu kaybettin. Bu utanç seni takip edecek."
    };
  }

  // Gizli bayrakları kontrol et
  checkHiddenFlags(playerChoices: string[], playerKarma: number, playerItems: string[]): string[] {
    const triggeredFlags: string[] = [];
    
    this.hiddenFlags.forEach((flag, flagId) => {
      let shouldTrigger = false;
      
      // Trigger koşullarını kontrol et
      flag.trigger_conditions.forEach(condition => {
        if (playerChoices.includes(condition) || 
            (condition === "high_karma" && playerKarma > 50) ||
            (condition === "low_karma" && playerKarma < -20)) {
          shouldTrigger = true;
        }
      });
      
      if (shouldTrigger) {
        triggeredFlags.push(flagId);
      }
    });
    
    return triggeredFlags;
  }

  // Sonuçları hesapla
  calculateEnding(playerChoices: string[], playerKarma: number, playerItems: string[], playerRelationships: { [key: string]: string }): Ending {
    const hiddenFlags = this.checkHiddenFlags(playerChoices, playerKarma, playerItems);
    
    // Karma bazlı sonlar
    if (playerKarma >= 80 && hiddenFlags.includes("heroic_sacrifice")) {
      return this.createSacrificeEnding("fantasy");
    }
    
    if (playerKarma >= 60 && hiddenFlags.includes("redemption_arc")) {
      return this.createRedemptionEnding("fantasy");
    }
    
    if (playerKarma <= -30 && hiddenFlags.includes("dark_power")) {
      return this.createCorruptionEnding("fantasy");
    }
    
    if (playerKarma <= -20 && playerChoices.includes("run_away")) {
      return this.createEscapeEnding("fantasy");
    }
    
    // Seçim bazlı sonlar
    if (playerChoices.includes("trust_everyone") && hiddenFlags.includes("hidden_enemy")) {
      return this.createBetrayalEnding("fantasy");
    }
    
    if (playerChoices.includes("explore_thoroughly") && hiddenFlags.includes("ancient_knowledge")) {
      return this.createMysteryEnding("fantasy");
    }
    
    // Karma bazlı ana sonlar
    if (playerKarma >= 50) {
      return this.createVictoryEnding("fantasy");
    } else if (playerKarma >= 30) {
      return this.createTragicEnding("fantasy");
    } else {
      return this.createEscapeEnding("fantasy");
    }
  }
} 