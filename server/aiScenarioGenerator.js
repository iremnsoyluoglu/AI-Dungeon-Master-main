const fs = require('fs');
const path = require('path');

class AIScenarioGenerator {
  constructor() {
    this.aiScenariosPath = path.join(__dirname, '../data/ai_generated_scenarios.json');
    this.ensureAIScenariosFile();
  }

  ensureAIScenariosFile() {
    if (!fs.existsSync(this.aiScenariosPath)) {
      const initialData = {
        scenarios: []
      };
      fs.writeFileSync(this.aiScenariosPath, JSON.stringify(initialData, null, 2));
    }
  }

  async generateScenario(prompt, theme, difficulty, genre) {
    // Karmaşık AI scenario generation
    const scenarioId = `ai_${Date.now()}`;
    
    // Tema bazlı senaryo oluşturma
    const themeConfigs = {
      epic_fantasy: {
        title: `🐉 ${prompt} - Epik Fantazi Macerası`,
        description: `Ejderhalar, büyücüler ve destansı maceraların dünyasında ${prompt} ile başlayan epik bir yolculuk.`,
        enemies: ['Goblin Sürüsü', 'Ork Savaşçıları', 'Kara Büyücü', 'Antik Ejderha'],
        npcs: ['Bilge Büyücü Aldric', 'Savaşçı Lydia', 'Tüccar Thorin', 'Gizemli Yabancı']
      },
      cyberpunk_revolution: {
        title: `🌃 ${prompt} - Cyberpunk Devrimi`,
        description: `Neon ışıklar altında AI'lar, mega şirketler ve dijital savaşın ortasında ${prompt} ile başlayan devrim.`,
        enemies: ['Corp Güvenlik', 'Hacklenmiş Robotlar', 'AI Kontrolcü', 'Siber Ninja'],
        npcs: ['Netrunner Zara', 'Hacker Razor', 'Corp Ajan Maria', 'Underground Lider']
      },
      space_war: {
        title: `🚀 ${prompt} - Uzay Savaşı`,
        description: `Galaksiler arası çatışma ve uzay gemilerinin dünyasında ${prompt} ile başlayan kozmik savaş.`,
        enemies: ['Alien İstilacılar', 'Uzay Korsanları', 'Robot Ordusu', 'Kozmik Canavar'],
        npcs: ['Kaptan Kain', 'Teknisyen Maria', 'Alien Elçi', 'Uzay Tüccarı']
      }
    };

    const config = themeConfigs[theme] || themeConfigs.epic_fantasy;
    
    const scenario = {
      id: scenarioId,
      title: config.title,
      description: config.description,
      difficulty: difficulty || 'medium',
      estimatedPlayTime: Math.floor(Math.random() * 120) + 60,
      theme: theme || 'fantasy',
      genre: genre || 'adventure',
      complexity: difficulty === 'hard' ? 'high' : 'medium',
      source: 'ai_generated',
      created_at: new Date().toISOString(),
      
      // Karmaşık story nodes (5-7 karar noktası)
      story_nodes: {
        start: {
          id: 'start',
          title: '🚀 Maceranın Başlangıcı',
          description: `${prompt} ile başlayan bu tehlikeli yolculukta kendini buluyorsun. ${config.description}`,
          choices: [
            {
              id: 'explore_carefully',
              text: 'Dikkatli bir şekilde çevreyi keşfet',
              nextNode: 'careful_exploration',
              effect: { stealth: 2, intelligence: 1 }
            },
            {
              id: 'rush_forward',
              text: 'Hızlıca ileri atıl',
              nextNode: 'rushed_encounter',
              effect: { strength: 2, dexterity: 1 }
            },
            {
              id: 'seek_help',
              text: 'Yardım ara',
              nextNode: 'npc_encounter',
              effect: { charisma: 2, wisdom: 1 }
            }
          ]
        },
        
        careful_exploration: {
          id: 'careful_exploration',
          title: '🔍 Dikkatli Keşif',
          description: 'Çevreyi dikkatli bir şekilde inceliyorsun. Gizli geçitler ve tuzaklar fark ediyorsun.',
          choices: [
            {
              id: 'use_stealth',
              text: 'Gizlilik kullanarak ilerle',
              nextNode: 'stealth_mission',
              effect: { stealth: 3, experience: 50 }
            },
            {
              id: 'disable_traps',
              text: 'Tuzakları etkisiz hale getir',
              nextNode: 'trap_discovery',
              effect: { intelligence: 2, dexterity: 1 }
            }
          ]
        },
        
        rushed_encounter: {
          id: 'rushed_encounter',
          title: '⚔️ Hızlı Karşılaşma',
          description: 'Hızlı hareket etmen sonucu beklenmedik bir düşmanla karşılaştın!',
          choices: [
            {
              id: 'fight_bravely',
              text: 'Cesurca savaş',
              nextNode: 'combat_scene_1',
              effect: { strength: 3, combat_skill: 2 }
            },
            {
              id: 'tactical_retreat',
              text: 'Taktiksel geri çekil',
              nextNode: 'tactical_positioning',
              effect: { wisdom: 2, dexterity: 1 }
            }
          ]
        },
        
        npc_encounter: {
          id: 'npc_encounter',
          title: '👥 NPC Karşılaşması',
          description: `${config.npcs[0]} ile karşılaştın. Size yardım etmek istiyor ama güvenilir mi?`,
          choices: [
            {
              id: 'trust_npc',
              text: 'NPC\'ye güven',
              nextNode: 'npc_alliance',
              effect: { charisma: 2, npc_trust: 30 }
            },
            {
              id: 'be_cautious',
              text: 'İhtiyatlı ol',
              nextNode: 'cautious_interaction',
              effect: { wisdom: 2, intelligence: 1 }
            }
          ]
        },
        
        combat_scene_1: {
          id: 'combat_scene_1',
          title: '⚔️ Savaş Sahnesi - İlk Düşman',
          description: `${config.enemies[0]} ile karşı karşıyasın! Savaş başlıyor!`,
          choices: [
            {
              id: 'heavy_attack',
              text: 'Ağır saldırı',
              nextNode: 'combat_victory',
              effect: { strength: 3, damage: 25 }
            },
            {
              id: 'defensive_stance',
              text: 'Savunma pozisyonu',
              nextNode: 'defensive_victory',
              effect: { constitution: 2, defense: 15 }
            }
          ]
        },
        
        npc_alliance: {
          id: 'npc_alliance',
          title: '🤝 NPC İttifakı',
          description: `${config.npcs[0]} ile ittifak kurdun. Birlikte daha güçlüsünüz.`,
          choices: [
            {
              id: 'plan_together',
              text: 'Birlikte plan yap',
              nextNode: 'strategic_planning',
              effect: { intelligence: 2, teamwork: 1 }
            },
            {
              id: 'split_up',
              text: 'Ayrı ayrı hareket et',
              nextNode: 'split_mission',
              effect: { dexterity: 2, independence: 1 }
            }
          ]
        },
        
        strategic_planning: {
          id: 'strategic_planning',
          title: '🧠 Stratejik Planlama',
          description: 'NPC ile birlikte detaylı bir plan hazırladınız. Düşmanın zayıf noktalarını belirlediniz.',
          choices: [
            {
              id: 'execute_plan',
              text: 'Planı uygula',
              nextNode: 'planned_attack',
              effect: { intelligence: 3, strategy: 2 }
            },
            {
              id: 'adapt_plan',
              text: 'Planı değiştir',
              nextNode: 'adaptive_strategy',
              effect: { wisdom: 2, flexibility: 1 }
            }
          ]
        },
        
        planned_attack: {
          id: 'planned_attack',
          title: '🎯 Planlanmış Saldırı',
          description: 'Hazırladığınız planı mükemmel bir şekilde uyguladınız. Düşman şaşkın!',
          choices: [
            {
              id: 'finish_them',
              text: 'Düşmanı bitir',
              nextNode: 'ending_victory',
              effect: { strength: 3, victory: 1 }
            },
            {
              id: 'show_mercy',
              text: 'Merhamet göster',
              nextNode: 'ending_redemption',
              effect: { charisma: 2, wisdom: 2 }
            }
          ]
        },
        
        ending_victory: {
          id: 'ending_victory',
          title: '🏆 Zafer Sonu',
          description: 'Mükemmel bir zafer kazandın! Maceran başarıyla tamamlandı.',
          choices: []
        },
        
        ending_redemption: {
          id: 'ending_redemption',
          title: '🕊️ Kefaret Sonu',
          description: 'Merhametin sayesinde düşmanın kalbini kazandın. Barış sağlandı.',
          choices: []
        },
        
        ending_sacrifice: {
          id: 'ending_sacrifice',
          title: '⚰️ Fedakarlık Sonu',
          description: 'Büyük bir fedakarlıkla macerayı tamamladın. Kahramanlığın unutulmayacak.',
          choices: []
        }
      },
      
      // Combat scenes
      combat_scenes: [
        {
          id: 'combat_1',
          title: 'İlk Savaş',
          enemies: [config.enemies[0]],
          boss: null,
          rounds: 3,
          status_effects: ['poison', 'stun']
        },
        {
          id: 'combat_2',
          title: 'Boss Savaşı',
          enemies: [config.enemies[1], config.enemies[2]],
          boss: config.enemies[3],
          rounds: 5,
          status_effects: ['fire', 'ice', 'lightning']
        }
      ],
      
      // NPC relationships
      npc_relationships: {
        [config.npcs[0].toLowerCase().replace(' ', '_')]: {
          name: config.npcs[0],
          trust_level: 0,
          quests_completed: 0,
          relationship_status: 'stranger',
          ending_impact: 'high'
        },
        [config.npcs[1].toLowerCase().replace(' ', '_')]: {
          name: config.npcs[1],
          trust_level: 0,
          quests_completed: 0,
          relationship_status: 'stranger',
          ending_impact: 'medium'
        }
      },
      
      // Multiple endings
      ending_variations: {
        victory: {
          requirements: { strength: 15, intelligence: 10 },
          description: 'Zafer kazandın!'
        },
        redemption: {
          requirements: { charisma: 15, wisdom: 12 },
          description: 'Merhametle kazandın!'
        },
        sacrifice: {
          requirements: { constitution: 18, charisma: 8 },
          description: 'Fedakarlıkla kazandın!'
        }
      }
    };

    return scenario;
  }

  async saveScenario(scenario) {
    try {
      const data = JSON.parse(fs.readFileSync(this.aiScenariosPath, 'utf8'));
      data.scenarios.push(scenario);
      fs.writeFileSync(this.aiScenariosPath, JSON.stringify(data, null, 2));
      return true;
    } catch (error) {
      console.error('Error saving AI scenario:', error);
      return false;
    }
  }

  async getScenarios() {
    try {
      const data = JSON.parse(fs.readFileSync(this.aiScenariosPath, 'utf8'));
      return data.scenarios || [];
    } catch (error) {
      console.error('Error loading AI scenarios:', error);
      return [];
    }
  }
}

module.exports = new AIScenarioGenerator();
