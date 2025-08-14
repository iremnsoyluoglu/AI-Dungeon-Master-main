import { ComprehensiveScenarioGenerator, ComprehensiveScenarioNode } from './ComprehensiveScenarioGenerator';
import { RPGScenario, StoredScenario } from '../types/scenarioStorage';

export interface EnhancedScenario {
  id: string;
  title: string;
  description: string;
  theme: string;
  difficulty: string;
  nodes: ComprehensiveScenarioNode[];
  backgroundImages: { [nodeId: string]: string };
  plotTwists: string[];
  betrayals: string[];
  randomEvents: string[];
  totalBranches: number;
  estimatedPlayTime: number;
  complexity: 'low' | 'medium' | 'high';
}

export class EnhancedScenarioManager {
  private comprehensiveGenerator: ComprehensiveScenarioGenerator;
  private enhancedScenarios: Map<string, EnhancedScenario> = new Map();

  constructor() {
    this.comprehensiveGenerator = new ComprehensiveScenarioGenerator();
  }

  // Tüm senaryoları Hive seviyesinde kapsamlı hale getir
  async enhanceAllScenarios(): Promise<void> {
    const themes = ['fantasy', 'warhammer40k', 'scifi', 'cyberpunk', 'post_apocalyptic'];
    const difficulties = ['easy', 'medium', 'hard'];

    for (const theme of themes) {
      for (const difficulty of difficulties) {
        const scenarioId = `${theme}_${difficulty}_enhanced`;
        const enhancedScenario = await this.createEnhancedScenario(theme, difficulty);
        this.enhancedScenarios.set(scenarioId, enhancedScenario);
      }
    }
  }

  private async createEnhancedScenario(theme: string, difficulty: string): Promise<EnhancedScenario> {
    // Kapsamlı senaryo oluştur
    const nodes = this.comprehensiveGenerator.generateComprehensiveScenario(theme, difficulty);
    
    // Background image mapping
    const backgroundImages: { [nodeId: string]: string } = {};
    nodes.forEach(node => {
      if (node.backgroundImage) {
        backgroundImages[node.id] = node.backgroundImage;
      }
    });

    // Plot twist'leri topla
    const plotTwists = nodes
      .filter(node => node.plotTwist)
      .map(node => node.title);

    // İhanetleri topla
    const betrayals = nodes
      .filter(node => node.betrayal)
      .map(node => node.title);

    // Rastgele olayları topla
    const randomEvents = nodes
      .filter(node => node.randomEvent)
      .map(node => node.title);

    // Toplam dal sayısını hesapla
    const totalBranches = nodes.reduce((total, node) => total + node.choices.length, 0);

    // Tahmini oynama süresi
    const estimatedPlayTime = this.calculatePlayTime(nodes, difficulty);

    // Karmaşıklık seviyesi
    const complexity = this.calculateComplexity(nodes, difficulty);

    return {
      id: `${theme}_${difficulty}_enhanced`,
      title: this.generateScenarioTitle(theme, difficulty),
      description: this.generateScenarioDescription(theme, difficulty),
      theme,
      difficulty,
      nodes,
      backgroundImages,
      plotTwists,
      betrayals,
      randomEvents,
      totalBranches,
      estimatedPlayTime,
      complexity
    };
  }

  private generateScenarioTitle(theme: string, difficulty: string): string {
    const titles = {
      fantasy: {
        easy: "Büyülü Ormanın Sırları",
        medium: "Ejderha Avcısının Yolu",
        hard: "Karanlık Kule'nin Efendisi"
      },
      warhammer40k: {
        easy: "Hive Şehrinin Savunması",
        medium: "Ork İstilası",
        hard: "Kaos'un Gölgesi"
      },
      scifi: {
        easy: "Uzay Gemisinin Sırları",
        medium: "Yabancı İstilası",
        hard: "Galaktik Savaş"
      },
      cyberpunk: {
        easy: "Neon Şehrin Altı",
        medium: "Korporasyon Savaşı",
        hard: "Siberpunk Devrimi"
      },
      post_apocalyptic: {
        easy: "Kıyamet Sonrası",
        medium: "Mutant Sürüsü",
        hard: "Nükleer Kış"
      }
    };

    return titles[theme as keyof typeof titles]?.[difficulty as keyof typeof titles.fantasy] || "Bilinmeyen Macera";
  }

  private generateScenarioDescription(theme: string, difficulty: string): string {
    const descriptions = {
      fantasy: {
        easy: "Büyülü bir dünyada başlayan macera. Ormanlar, yaratıklar ve gizli hazineler seni bekliyor.",
        medium: "Ejderhalar ve büyücülerle dolu tehlikeli bir yolculuk. Güç ve bilgelik arasında seçim yap.",
        hard: "Karanlık güçlerin hüküm sürdüğü bir dünya. En büyük sınavlar seni bekliyor."
      },
      warhammer40k: {
        easy: "İmparatorluk'un bir köşesinde başlayan savunma görevi. Orklar yaklaşıyor!",
        medium: "Ork sürüsü şehri kuşattı. Tek umut sensin!",
        hard: "Kaos'un güçleri her yerde. İmparatorluk'un son umudu sensin."
      },
      scifi: {
        easy: "Bilinmeyen bir uzay gemisinde uyandın. Teknoloji ve gizemler seni bekliyor.",
        medium: "Yabancı ırklar galaksiyi istila ediyor. İnsanlığın son umudu sensin!",
        hard: "Galaktik savaşın ortasındasın. Tüm galaksinin kaderi senin elinde."
      },
      cyberpunk: {
        easy: "Neon ışıkların altında gizli bir dünya. Korporasyonlar ve hackerlar.",
        medium: "Korporasyonlar arası savaş. Teknoloji ve güç mücadelesi.",
        hard: "Siberpunk devrimi başlıyor. Sistemin sonu geliyor."
      },
      post_apocalyptic: {
        easy: "Kıyamet sonrası dünyada hayatta kalma mücadelesi.",
        medium: "Mutant sürüleri her yerde. İnsanlığın son kaleleri.",
        hard: "Nükleer kışın ortasında. Dünyanın son umudu sensin."
      }
    };

    return descriptions[theme as keyof typeof descriptions]?.[difficulty as keyof typeof descriptions.fantasy] || "Bilinmeyen bir macera seni bekliyor.";
  }

  private calculatePlayTime(nodes: ComprehensiveScenarioNode[], difficulty: string): number {
    const baseTime = nodes.length * 2; // Her node için 2 dakika
    const difficultyMultiplier = {
      easy: 0.8,
      medium: 1.0,
      hard: 1.5
    };
    
    return Math.round(baseTime * difficultyMultiplier[difficulty as keyof typeof difficultyMultiplier]);
  }

  private calculateComplexity(nodes: ComprehensiveScenarioNode[], difficulty: string): 'low' | 'medium' | 'high' {
    const plotTwistCount = nodes.filter(n => n.plotTwist).length;
    const betrayalCount = nodes.filter(n => n.betrayal).length;
    const randomEventCount = nodes.filter(n => n.randomEvent).length;
    
    const complexityScore = plotTwistCount + betrayalCount + randomEventCount + nodes.length;
    
    if (complexityScore < 10) return 'low';
    if (complexityScore < 20) return 'medium';
    return 'high';
  }

  // Senaryo getir
  getEnhancedScenario(theme: string, difficulty: string): EnhancedScenario | undefined {
    const scenarioId = `${theme}_${difficulty}_enhanced`;
    return this.enhancedScenarios.get(scenarioId);
  }

  // Tüm geliştirilmiş senaryoları getir
  getAllEnhancedScenarios(): EnhancedScenario[] {
    return Array.from(this.enhancedScenarios.values());
  }

  // Senaryo istatistikleri
  getScenarioStats(theme: string, difficulty: string): {
    totalNodes: number;
    plotTwistCount: number;
    betrayalCount: number;
    randomEventCount: number;
    combatNodes: number;
    endingNodes: number;
    averageChoicesPerNode: number;
  } {
    const scenario = this.getEnhancedScenario(theme, difficulty);
    if (!scenario) {
      return {
        totalNodes: 0,
        plotTwistCount: 0,
        betrayalCount: 0,
        randomEventCount: 0,
        combatNodes: 0,
        endingNodes: 0,
        averageChoicesPerNode: 0
      };
    }

    const nodes = scenario.nodes;
    const totalChoices = nodes.reduce((total, node) => total + node.choices.length, 0);

    return {
      totalNodes: nodes.length,
      plotTwistCount: nodes.filter(n => n.plotTwist).length,
      betrayalCount: nodes.filter(n => n.betrayal).length,
      randomEventCount: nodes.filter(n => n.randomEvent).length,
      combatNodes: nodes.filter(n => n.combat).length,
      endingNodes: nodes.filter(n => n.ending).length,
      averageChoicesPerNode: totalChoices / nodes.length
    };
  }

  // Background image desteği
  getBackgroundImageForNode(scenarioId: string, nodeId: string): string | undefined {
    const scenario = this.enhancedScenarios.get(scenarioId);
    return scenario?.backgroundImages[nodeId];
  }

  // Senaryo önerileri
  getRecommendedScenarios(userPreferences: {
    preferredThemes: string[];
    preferredDifficulty: string;
    preferredComplexity: 'low' | 'medium' | 'high';
  }): EnhancedScenario[] {
    return this.getAllEnhancedScenarios().filter(scenario => {
      const themeMatch = userPreferences.preferredThemes.includes(scenario.theme);
      const difficultyMatch = scenario.difficulty === userPreferences.preferredDifficulty;
      const complexityMatch = scenario.complexity === userPreferences.preferredComplexity;
      
      return themeMatch && difficultyMatch && complexityMatch;
    });
  }

  // Senaryo karşılaştırması
  compareScenarios(scenario1Id: string, scenario2Id: string): {
    scenario1: EnhancedScenario;
    scenario2: EnhancedScenario;
    comparison: {
      complexity: string;
      playTime: string;
      plotTwists: string;
      betrayals: string;
      randomEvents: string;
    };
  } {
    const scenario1 = this.enhancedScenarios.get(scenario1Id);
    const scenario2 = this.enhancedScenarios.get(scenario2Id);

    if (!scenario1 || !scenario2) {
      throw new Error('Senaryo bulunamadı');
    }

    return {
      scenario1,
      scenario2,
      comparison: {
        complexity: scenario1.complexity === scenario2.complexity ? 'Eşit' : 
                   scenario1.complexity === 'high' ? 'Senaryo 1 daha karmaşık' : 'Senaryo 2 daha karmaşık',
        playTime: scenario1.estimatedPlayTime === scenario2.estimatedPlayTime ? 'Eşit' :
                 scenario1.estimatedPlayTime > scenario2.estimatedPlayTime ? 'Senaryo 1 daha uzun' : 'Senaryo 2 daha uzun',
        plotTwists: scenario1.plotTwists.length === scenario2.plotTwists.length ? 'Eşit' :
                   scenario1.plotTwists.length > scenario2.plotTwists.length ? 'Senaryo 1 daha fazla plot twist' : 'Senaryo 2 daha fazla plot twist',
        betrayals: scenario1.betrayals.length === scenario2.betrayals.length ? 'Eşit' :
                  scenario1.betrayals.length > scenario2.betrayals.length ? 'Senaryo 1 daha fazla ihanet' : 'Senaryo 2 daha fazla ihanet',
        randomEvents: scenario1.randomEvents.length === scenario2.randomEvents.length ? 'Eşit' :
                     scenario1.randomEvents.length > scenario2.randomEvents.length ? 'Senaryo 1 daha fazla rastgele olay' : 'Senaryo 2 daha fazla rastgele olay'
      }
    };
  }
} 