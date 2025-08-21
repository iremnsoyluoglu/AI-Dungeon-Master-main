module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  const { pathname } = new URL(req.url, `http://${req.headers.host}`);

  if (pathname === '/api/scenarios' && req.method === 'GET') {
    res.json({
      success: true,
      scenarios: [
        {
          id: "scenario_1",
          title: "🐉 Fantastik Macera",
          description: "Ejderhalar ve büyücüler dünyasında epik bir yolculuk",
          theme: "fantasy",
          difficulty: "medium",
          complexity: "medium",
          estimatedPlayTime: 60,
          source: "predefined",
          created_at: new Date().toISOString(),
        }
      ],
    });
    return;
  }

  if (pathname === '/api/ai/scenarios' && req.method === 'GET') {
    res.json({
      success: true,
      scenarios: [
        {
          id: "ai_1",
          title: "🤖 AI Üretilen Macera",
          description: "Yapay zeka tarafından üretilen özel macera",
          theme: "fantasy",
          difficulty: "medium",
          source: "ai_generated",
          created_at: new Date().toISOString(),
        },
      ],
    });
    return;
  }

  if (pathname === '/api/read-file' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => {
      try {
        const { fileContent } = JSON.parse(body);
        
        if (!fileContent) {
          res.status(400).json({ error: "Dosya içeriği gönderilmedi!" });
          return;
        }

        res.json({
          content: fileContent,
          fileName: "uploaded_file.txt",
          fileSize: fileContent.length,
        });
      } catch (error) {
        res.status(400).json({ error: "Geçersiz JSON" });
      }
    });
    return;
  }

  if (pathname === '/api/generate-scenario' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => {
      try {
        const { theme, difficulty, fileContent } = JSON.parse(body);

        const scenario = {
          id: `scenario_${Date.now()}`,
          title: `${theme} Macerası - ${difficulty}`,
          description: `Dosya içeriğinden üretilen ${theme} temalı ${difficulty} zorlukta senaryo`,
          theme: theme,
          difficulty: difficulty,
          complexity: difficulty,
          estimatedPlayTime: difficulty === "easy" ? 30 : difficulty === "medium" ? 60 : 90,
          fileContent: fileContent ? fileContent.substring(0, 200) + "..." : null,
          generatedAt: new Date().toISOString(),
          source: "file_generated",
          created_at: new Date().toISOString(),
          
          story_nodes: {
            start: {
              id: "start",
              title: "🚀 Dosya Macerasının Başlangıcı",
              description: `Dosya içeriğinden üretilen bu macerada kendini buluyorsun. ${theme} temalı ${difficulty} zorlukta bir yolculuk seni bekliyor.`,
              choices: [
                {
                  id: "explore_carefully",
                  text: "Dikkatli bir şekilde çevreyi keşfet",
                  nextNode: "careful_exploration",
                  effect: { stealth: 2, intelligence: 1 },
                },
                {
                  id: "rush_forward",
                  text: "Hızlıca ileri atıl",
                  nextNode: "rushed_encounter",
                  effect: { strength: 2, dexterity: 1 },
                },
                {
                  id: "seek_help",
                  text: "Yardım ara",
                  nextNode: "npc_encounter",
                  effect: { charisma: 2, wisdom: 1 },
                },
              ],
            },
            careful_exploration: {
              id: "careful_exploration",
              title: "🔍 Dikkatli Keşif",
              description: "Çevreyi dikkatli bir şekilde inceliyorsun. Dosya içeriğinden üretilen gizli geçitler ve tuzaklar fark ediyorsun.",
              choices: [
                {
                  id: "use_stealth",
                  text: "Gizlilik kullanarak ilerle",
                  nextNode: "stealth_mission",
                  effect: { stealth: 3, experience: 50 },
                },
                {
                  id: "disable_traps",
                  text: "Tuzakları etkisiz hale getir",
                  nextNode: "trap_discovery",
                  effect: { intelligence: 2, dexterity: 1 },
                },
              ],
            },
            rushed_encounter: {
              id: "rushed_encounter",
              title: "⚔️ Hızlı Karşılaşma",
              description: "Hızlı hareket etmen sonucu dosya içeriğinden üretilen beklenmedik bir düşmanla karşılaştın!",
              choices: [
                {
                  id: "fight_bravely",
                  text: "Cesurca savaş",
                  nextNode: "combat_scene_1",
                  effect: { strength: 3, combat_skill: 2 },
                },
                {
                  id: "tactical_retreat",
                  text: "Taktiksel geri çekil",
                  nextNode: "tactical_positioning",
                  effect: { wisdom: 2, dexterity: 1 },
                },
              ],
            },
            npc_encounter: {
              id: "npc_encounter",
              title: "👥 NPC Karşılaşması",
              description: "Dosya içeriğinden üretilen bir NPC ile karşılaştın. Size yardım etmek istiyor ama güvenilir mi?",
              choices: [
                {
                  id: "trust_npc",
                  text: "NPC'ye güven",
                  nextNode: "npc_alliance",
                  effect: { charisma: 2, npc_trust: 30 },
                },
                {
                  id: "be_cautious",
                  text: "İhtiyatlı ol",
                  nextNode: "cautious_interaction",
                  effect: { wisdom: 2, intelligence: 1 },
                },
              ],
            },
            combat_scene_1: {
              id: "combat_scene_1",
              title: "⚔️ Savaş Sahnesi - Dosya Düşmanı",
              description: "Dosya içeriğinden üretilen düşman ile karşı karşıyasın! Savaş başlıyor!",
              choices: [
                {
                  id: "heavy_attack",
                  text: "Ağır saldırı",
                  nextNode: "combat_victory",
                  effect: { strength: 3, damage: 25 },
                },
                {
                  id: "defensive_stance",
                  text: "Savunma pozisyonu",
                  nextNode: "defensive_victory",
                  effect: { constitution: 2, defense: 15 },
                },
              ],
            },
            npc_alliance: {
              id: "npc_alliance",
              title: "🤝 NPC İttifakı",
              description: "Dosya içeriğinden üretilen NPC ile ittifak kurdun. Birlikte daha güçlüsünüz.",
              choices: [
                {
                  id: "plan_together",
                  text: "Birlikte plan yap",
                  nextNode: "strategic_planning",
                  effect: { intelligence: 2, teamwork: 1 },
                },
                {
                  id: "split_up",
                  text: "Ayrı ayrı hareket et",
                  nextNode: "split_mission",
                  effect: { dexterity: 2, independence: 1 },
                },
              ],
            },
            strategic_planning: {
              id: "strategic_planning",
              title: "🧠 Stratejik Planlama",
              description: "NPC ile birlikte detaylı bir plan hazırladınız. Dosya içeriğinden üretilen düşmanın zayıf noktalarını belirlediniz.",
              choices: [
                {
                  id: "execute_plan",
                  text: "Planı uygula",
                  nextNode: "planned_attack",
                  effect: { intelligence: 3, strategy: 2 },
                },
                {
                  id: "adapt_plan",
                  text: "Planı değiştir",
                  nextNode: "adaptive_strategy",
                  effect: { wisdom: 2, flexibility: 1 },
                },
              ],
            },
            planned_attack: {
              id: "planned_attack",
              title: "🎯 Planlanmış Saldırı",
              description: "Hazırladığınız planı mükemmel bir şekilde uyguladınız. Dosya içeriğinden üretilen düşman şaşkın!",
              choices: [
                {
                  id: "finish_them",
                  text: "Düşmanı bitir",
                  nextNode: "ending_victory",
                  effect: { strength: 3, victory: 1 },
                },
                {
                  id: "show_mercy",
                  text: "Merhamet göster",
                  nextNode: "ending_redemption",
                  effect: { charisma: 2, wisdom: 2 },
                },
              ],
            },
            ending_victory: {
              id: "ending_victory",
              title: "🏆 Zafer Sonu",
              description: "Dosya içeriğinden üretilen macerada mükemmel bir zafer kazandın! Maceran başarıyla tamamlandı.",
              choices: [],
            },
            ending_redemption: {
              id: "ending_redemption",
              title: "🕊️ Kefaret Sonu",
              description: "Dosya içeriğinden üretilen macerada merhametin sayesinde düşmanın kalbini kazandın. Barış sağlandı.",
              choices: [],
            },
          },

          npc_relationships: {
            file_npc: {
              name: "Dosya NPC'si",
              trust_level: 0,
              quests_completed: 0,
              relationship_status: "stranger",
              ending_impact: "high",
            },
          },

          ending_variations: {
            victory: {
              requirements: { strength: 15, intelligence: 10 },
              description: "Zafer kazandın!",
            },
            redemption: {
              requirements: { charisma: 15, wisdom: 12 },
              description: "Merhametle kazandın!",
            },
            sacrifice: {
              requirements: { constitution: 18, charisma: 8 },
              description: "Fedakarlıkla kazandın!",
            },
          },
        };

        res.json({
          success: true,
          scenario: scenario,
          message: "Senaryo başarıyla üretildi!",
        });
      } catch (error) {
        res.status(400).json({ error: "Geçersiz JSON" });
      }
    });
    return;
  }

  if (pathname === '/api/health' && req.method === 'GET') {
    res.json({ status: "OK", timestamp: new Date().toISOString() });
    return;
  }

  if (pathname === '/' && req.method === 'GET') {
    res.json({ message: "AI Dungeon Master API is running!" });
    return;
  }

  res.status(404).json({ error: "Route not found" });
};
