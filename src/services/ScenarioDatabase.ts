import { StoredScenario } from '../types/scenarioStorage';
import { EnhancedScenario, EnhancedScenarioManager } from './EnhancedScenarioManager';
import { ComprehensiveScenarioNode } from './ComprehensiveScenarioGenerator';

export interface ScenarioDatabaseConfig {
  enableBackgroundImages: boolean;
  enablePlotTwists: boolean;
  enableBetrayals: boolean;
  enableRandomEvents: boolean;
  defaultTheme: string;
  defaultDifficulty: string;
}

export class ScenarioDatabase {
  private enhancedManager: EnhancedScenarioManager;
  private config: ScenarioDatabaseConfig;
  private scenarios: Map<string, StoredScenario> = new Map();
  private enhancedScenarios: Map<string, EnhancedScenario> = new Map();

  constructor(config: ScenarioDatabaseConfig) {
    this.enhancedManager = new EnhancedScenarioManager();
    this.config = config;
  }

  // Tüm senaryoları yükle ve geliştir
  async initialize(): Promise<void> {
    console.log('🎯 Senaryo veritabanı başlatılıyor...');
    
    // Geliştirilmiş senaryoları oluştur
    await this.enhancedManager.enhanceAllScenarios();
    
    // Mevcut senaryoları geliştirilmiş versiyonlarla güncelle
    await this.upgradeExistingScenarios();
    
    console.log('✅ Senaryo veritabanı hazır!');
  }

  private async upgradeExistingScenarios(): Promise<void> {
    // Mevcut senaryoları al
    const existingScenarios = Array.from(this.scenarios.values());
    
    for (const scenario of existingScenarios) {
      // Her senaryoyu kapsamlı hale getir
      const enhancedScenario = await this.createEnhancedVersion(scenario);
      this.enhancedScenarios.set(enhancedScenario.id, enhancedScenario);
    }
  }

  private async createEnhancedVersion(scenario: StoredScenario): Promise<EnhancedScenario> {
    // Senaryo temasını belirle
    const theme = this.determineTheme(scenario);
    const difficulty = scenario.difficulty || 'medium';
    
    // Kapsamlı senaryo oluştur
    const enhancedScenario = this.enhancedManager.getEnhancedScenario(theme, difficulty);
    
    if (enhancedScenario) {
      return enhancedScenario;
    }

    // Eğer hazır senaryo yoksa, yeni oluştur
    return await this.enhancedManager.createEnhancedScenario(theme, difficulty);
  }

  private determineTheme(scenario: StoredScenario): string {
    const title = scenario.title.toLowerCase();
    const description = scenario.description.toLowerCase();
    
    if (title.includes('hive') || title.includes('ork') || title.includes('imperium') || 
        description.includes('warhammer') || description.includes('40k')) {
      return 'warhammer40k';
    }
    
    if (title.includes('fantasy') || title.includes('dragon') || title.includes('magic') ||
        description.includes('fantasy') || description.includes('magic')) {
      return 'fantasy';
    }
    
    if (title.includes('space') || title.includes('alien') || title.includes('galaxy') ||
        description.includes('space') || description.includes('alien')) {
      return 'scifi';
    }
    
    if (title.includes('cyber') || title.includes('neon') || title.includes('corp') ||
        description.includes('cyberpunk') || description.includes('neon')) {
      return 'cyberpunk';
    }
    
    if (title.includes('apocalypse') || title.includes('mutant') || title.includes('nuclear') ||
        description.includes('apocalypse') || description.includes('mutant')) {
      return 'post_apocalyptic';
    }
    
    return 'fantasy'; // Varsayılan tema
  }

  // Senaryo kaydet
  async saveScenario(scenario: StoredScenario, metadata: any, tags: string[]): Promise<StoredScenario> {
    const enhancedScenario = await this.createEnhancedVersion(scenario);
    this.enhancedScenarios.set(enhancedScenario.id, enhancedScenario);
    
    // Orijinal senaryoyu da kaydet
    this.scenarios.set(scenario.id, scenario);
    
    console.log(`💾 Senaryo kaydedildi: ${enhancedScenario.title}`);
    return scenario;
  }

  // Senaryo getir
  getScenario(id: string): StoredScenario | undefined {
    return this.scenarios.get(id);
  }

  // Geliştirilmiş senaryo getir
  getEnhancedScenario(id: string): EnhancedScenario | undefined {
    return this.enhancedScenarios.get(id);
  }

  // Tüm senaryoları getir
  getAllScenarios(): StoredScenario[] {
    return Array.from(this.scenarios.values());
  }

  // Tüm geliştirilmiş senaryoları getir
  getAllEnhancedScenarios(): EnhancedScenario[] {
    return Array.from(this.enhancedScenarios.values());
  }

  // Tema bazında senaryoları getir
  getScenariosByTheme(theme: string): EnhancedScenario[] {
    return this.getAllEnhancedScenarios().filter(scenario => scenario.theme === theme);
  }

  // Zorluk bazında senaryoları getir
  getScenariosByDifficulty(difficulty: string): EnhancedScenario[] {
    return this.getAllEnhancedScenarios().filter(scenario => scenario.difficulty === difficulty);
  }

  // Karmaşıklık bazında senaryoları getir
  getScenariosByComplexity(complexity: 'low' | 'medium' | 'high'): EnhancedScenario[] {
    return this.getAllEnhancedScenarios().filter(scenario => scenario.complexity === complexity);
  }

  // Background image desteği
  getBackgroundImage(scenarioId: string, nodeId: string): string | undefined {
    const scenario = this.enhancedScenarios.get(scenarioId);
    if (!scenario || !this.config.enableBackgroundImages) {
      return undefined;
    }
    
    return scenario.backgroundImages[nodeId];
  }

  // Plot twist'li senaryoları getir
  getScenariosWithPlotTwists(): EnhancedScenario[] {
    if (!this.config.enablePlotTwists) {
      return [];
    }
    
    return this.getAllEnhancedScenarios().filter(scenario => scenario.plotTwists.length > 0);
  }

  // İhanetli senaryoları getir
  getScenariosWithBetrayals(): EnhancedScenario[] {
    if (!this.config.enableBetrayals) {
      return [];
    }
    
    return this.getAllEnhancedScenarios().filter(scenario => scenario.betrayals.length > 0);
  }

  // Rastgele olaylı senaryoları getir
  getScenariosWithRandomEvents(): EnhancedScenario[] {
    if (!this.config.enableRandomEvents) {
      return [];
    }
    
    return this.getAllEnhancedScenarios().filter(scenario => scenario.randomEvents.length > 0);
  }

  // Senaryo istatistikleri
  getDatabaseStats(): {
    totalScenarios: number;
    enhancedScenarios: number;
    themes: { [theme: string]: number };
    difficulties: { [difficulty: string]: number };
    complexities: { [complexity: string]: number };
    averagePlayTime: number;
    totalPlotTwists: number;
    totalBetrayals: number;
    totalRandomEvents: number;
  } {
    const scenarios = this.getAllEnhancedScenarios();
    
    const themes: { [theme: string]: number } = {};
    const difficulties: { [difficulty: string]: number } = {};
    const complexities: { [complexity: string]: number } = {};
    
    let totalPlayTime = 0;
    let totalPlotTwists = 0;
    let totalBetrayals = 0;
    let totalRandomEvents = 0;
    
    scenarios.forEach(scenario => {
      // Tema sayıları
      themes[scenario.theme] = (themes[scenario.theme] || 0) + 1;
      
      // Zorluk sayıları
      difficulties[scenario.difficulty] = (difficulties[scenario.difficulty] || 0) + 1;
      
      // Karmaşıklık sayıları
      complexities[scenario.complexity] = (complexities[scenario.complexity] || 0) + 1;
      
      // Toplam değerler
      totalPlayTime += scenario.estimatedPlayTime;
      totalPlotTwists += scenario.plotTwists.length;
      totalBetrayals += scenario.betrayals.length;
      totalRandomEvents += scenario.randomEvents.length;
    });
    
    return {
      totalScenarios: this.scenarios.size,
      enhancedScenarios: scenarios.length,
      themes,
      difficulties,
      complexities,
      averagePlayTime: scenarios.length > 0 ? Math.round(totalPlayTime / scenarios.length) : 0,
      totalPlotTwists,
      totalBetrayals,
      totalRandomEvents
    };
  }

  // Senaryo önerileri
  getRecommendedScenarios(userPreferences: {
    preferredThemes: string[];
    preferredDifficulty: string;
    preferredComplexity: 'low' | 'medium' | 'high';
    maxPlayTime?: number;
  }): EnhancedScenario[] {
    let recommendations = this.enhancedManager.getRecommendedScenarios(userPreferences);
    
    // Oynama süresi filtresi
    if (userPreferences.maxPlayTime) {
      recommendations = recommendations.filter(scenario => 
        scenario.estimatedPlayTime <= userPreferences.maxPlayTime!
      );
    }
    
    // Karmaşıklık ve kaliteye göre sırala
    recommendations.sort((a, b) => {
      const aScore = a.plotTwists.length + a.betrayals.length + a.randomEvents.length;
      const bScore = b.plotTwists.length + b.betrayals.length + b.randomEvents.length;
      return bScore - aScore; // Yüksek skorlu olanları önce göster
    });
    
    return recommendations;
  }

  // Senaryo arama
  searchScenarios(query: string): EnhancedScenario[] {
    const searchTerm = query.toLowerCase();
    
    return this.getAllEnhancedScenarios().filter(scenario => 
      scenario.title.toLowerCase().includes(searchTerm) ||
      scenario.description.toLowerCase().includes(searchTerm) ||
      scenario.theme.toLowerCase().includes(searchTerm) ||
      scenario.plotTwists.some(twist => twist.toLowerCase().includes(searchTerm)) ||
      scenario.betrayals.some(betrayal => betrayal.toLowerCase().includes(searchTerm)) ||
      scenario.randomEvents.some(event => event.toLowerCase().includes(searchTerm))
    );
  }

  // Senaryo karşılaştırması
  compareScenarios(scenario1Id: string, scenario2Id: string) {
    return this.enhancedManager.compareScenarios(scenario1Id, scenario2Id);
  }

  // Senaryo sil
  deleteScenario(id: string): boolean {
    const originalDeleted = this.scenarios.delete(id);
    const enhancedDeleted = this.enhancedScenarios.delete(id);
    
    return originalDeleted || enhancedDeleted;
  }

  // Veritabanını temizle
  clearDatabase(): void {
    this.scenarios.clear();
    this.enhancedScenarios.clear();
  }

  // Konfigürasyon güncelle
  updateConfig(newConfig: Partial<ScenarioDatabaseConfig>): void {
    this.config = { ...this.config, ...newConfig };
  }
}
