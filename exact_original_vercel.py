from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
import json
import os
import time
import traceback
from datetime import datetime
# import requests # Removed for Vercel compatibility

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Add error handling
@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Server Error: {error}')
    app.logger.error(f'Traceback: {traceback.format_exc()}')
    return jsonify({'error': 'Internal server error', 'details': str(error)}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f'Unhandled Exception: {e}')
    app.logger.error(f'Traceback: {traceback.format_exc()}')
    return jsonify({'error': 'An error occurred', 'details': str(e)}), 500

# Load data files
def load_json_data(filename):
    try:
        with open(f'data/{filename}', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

# Load all data files
characters_data = load_json_data('characters.json')
scenarios_data = load_json_data('enhanced_scenarios.json')

# Enhanced scenario data - Use loaded data if available, otherwise use default
if scenarios_data and 'enhanced_scenarios' in scenarios_data:
    ENHANCED_SCENARIOS = scenarios_data['enhanced_scenarios']
    print("DEBUG: Using enhanced scenarios from data file")
    print("DEBUG: Available scenarios:", list(ENHANCED_SCENARIOS.keys()))
else:
    print("DEBUG: Using default enhanced scenarios")
    ENHANCED_SCENARIOS = {
    "dragon_hunters_path": {
        "id": "dragon_hunters_path",
        "title": "🐉 Dragon Hunter's Path",
        "genre": "fantasy",
        "description": "Köyü tehdit eden ejderhayı durdurmak için kahramanlar toplanıyor. Bu sadece bir görev değil, bu SENİN HİKAYEN. 🔥 PLOT TWIST'LER, 💬 NPC ETKİLEŞİMLERİ, ⚔️ UZUN SAVAŞ SAHNELERİ, 🎯 ACTION-BASED GÖREVLER, 🏁 5+ FARKLI SON!",
        "difficulty": "hard",
        "theme": "fantasy",
        "complexity": "high",
        "estimatedPlayTime": 480,  # 8 saat - çok daha uzun
        "levels": {
            "level_1": {
                "title": "Köy Tehdidi",
                "description": "Köy ejderha tehdidi altında. İnsanlar korku içinde.",
                "min_level": 1,
                "max_level": 3,
                "enemies": ["Goblin Scouts", "Wolf Pack", "Bandit Raiders"],
                "boss": "Goblin Chief",
                "side_quests": ["Village Defense", "Supply Run", "Scout Mission"]
            },
            "level_2": {
                "title": "Orman Keşfi",
                "description": "Ejderhanın izini sürmek için tehlikeli ormana giriyorsun.",
                "min_level": 3,
                "max_level": 5,
                "enemies": ["Forest Trolls", "Dark Elves", "Giant Spiders"],
                "boss": "Ancient Treant",
                "side_quests": ["Herb Collection", "Lost Traveler", "Sacred Grove"]
            }
        },
        "npc_relationships": {
            "aldric": {
                "name": "Aldric the Wise",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "stranger",
                "ending_impact": "high"
            },
            "lydia": {
                "name": "Lydia the Healer",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "stranger",
                "ending_impact": "medium"
            },
            "elder_thorin": {
                "name": "Elder Thorin Stonebeard",
                "backstory": "Legendary warrior who fought in the Great War, lost his family, now protects the village",
                "personality": "Stoic, wise, values honor above all",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "stranger",
                "ending_impact": "high",
                "quest_offers": ["Defend Village", "Ancient Weapon", "Honor Quest"]
            },
            "mystic_lyra": {
                "name": "Mystic Lyra Moonwhisper",
                "backstory": "Chosen by ancient spirits, 500+ years old, sees visions of the future",
                "personality": "Mysterious, contemplative, speaks in riddles",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "stranger",
                "ending_impact": "extreme",
                "quest_offers": ["Prophecy Quest", "Spirit Communication", "Ancient Knowledge"]
            },
            "captain_marcus": {
                "name": "Captain Marcus Ironheart",
                "backstory": "Rose from farm boy to trusted guard captain, saved the king's life",
                "personality": "Loyal, disciplined, honorable",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "stranger",
                "ending_impact": "high",
                "quest_offers": ["Royal Investigation", "Corruption Quest", "Loyalty Test"]
            },
            "sienna": {
                "name": "Sienna Shadowstep",
                "backstory": "Orphaned street child who became the city's most skilled thief",
                "personality": "Cunning, resourceful, morally flexible",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "stranger",
                "ending_impact": "medium",
                "quest_offers": ["Heist Quest", "Information Gathering", "Underground War"]
            }
        },
        "quest_chains": {
            "village_protection": {
                "title": "Köy Koruma Zinciri",
                "prerequisites": [],
                "quests": ["defend_village", "gather_supplies", "train_militia"],
                "rewards": {"xp": 500, "gold": 200, "items": ["village_sword"], "relationship_boost": 20}
            }
        },
        "quest_definitions": {
            "defend_village": {
                "title": "Defend the Village",
                "objectives": ["Scout area", "Fortify village", "Defeat bandits", "Protect civilians"],
                "branches": {
                    "success": {"leads_to": "ancient_weapon", "rewards": {"xp": 200, "gold": 150, "reputation": 30}},
                    "failure": {"leads_to": "redemption_quest", "penalties": {"reputation": -10}},
                    "perfect": {"leads_to": "honor_quest", "rewards": {"xp": 300, "gold": 200, "special_item": "village_defender_badge"}}
                },
                "dynamic_rewards": {"experience": 200, "gold": 150, "items": ["village_defender_badge"], "reputation": 30},
                "world_state_impact": {"village_safety": "+50", "elder_thorin_trust": "+25", "village_morale": "+40"}
            },
            "ancient_weapon": {
                "title": "Ancient Weapon",
                "objectives": ["Find ancient forge", "Gather sacred materials", "Forge weapon", "Enchant blade"],
                "branches": {
                    "success": {"leads_to": "dragon_final_battle", "rewards": {"xp": 300, "special_weapon": "dragonbane_sword"}},
                    "failure": {"leads_to": "alternative_strategy", "penalties": {"time_lost": 5}}
                },
                "dynamic_rewards": {"experience": 300, "special_weapon": "dragonbane_sword", "mystic_lyra_trust": "+30"},
                "world_state_impact": {"weapon_power": "+100", "village_hope": "+60"}
            },
            "prophecy_quest": {
                "title": "Prophecy Quest",
                "objectives": ["Visit sacred grove", "Interpret visions", "Gather ancient texts", "Understand destiny"],
                "branches": {
                    "success": {"leads_to": "spirit_communication", "rewards": {"xp": 250, "wisdom": "+50"}},
                    "enlightened": {"leads_to": "ancient_knowledge", "rewards": {"xp": 400, "special_ability": "future_sight"}}
                },
                "dynamic_rewards": {"experience": 250, "wisdom": 50, "mystic_lyra_trust": "+40"},
                "world_state_impact": {"prophecy_knowledge": "+100", "spiritual_power": "+30"}
            },
            "dragon_hunt": {
                "title": "Dragon Hunt",
                "objectives": ["Track dragon", "Fight dragon minions", "Reach dragon lair", "Defeat dragon"],
                "branches": {
                    "success": {"leads_to": "dragon_victory", "rewards": {"xp": 500, "dragon_scales": True, "legendary_status": True}},
                    "failure": {"leads_to": "retreat_and_regroup", "penalties": {"combat": -20}},
                    "perfect": {"leads_to": "dragon_master", "rewards": {"xp": 800, "dragon_heart": True, "master_hunter": True}}
                },
                "dynamic_rewards": {"experience": 500, "dragon_scales": True, "combat": 100},
                "world_state_impact": {"dragon_threat": "-100", "village_safety": "+100", "hero_reputation": "+200"}
            },
            "bandit_elimination": {
                "title": "Bandit Elimination",
                "objectives": ["Find bandit camp", "Defeat bandit leader", "Rescue hostages", "Secure area"],
                "branches": {
                    "success": {"leads_to": "village_defense", "rewards": {"xp": 200, "gold": 100, "combat": 50}},
                    "failure": {"leads_to": "bandit_retaliation", "penalties": {"village_safety": -30}},
                    "perfect": {"leads_to": "hero_recognition", "rewards": {"xp": 300, "gold": 150, "village_trust": 100}}
                },
                "dynamic_rewards": {"experience": 200, "gold": 100, "combat": 50},
                "world_state_impact": {"bandit_threat": "-80", "village_safety": "+60", "combat_reputation": "+40"}
            },
            "monster_hunt": {
                "title": "Monster Hunt",
                "objectives": ["Track monster", "Fight lesser monsters", "Defeat alpha monster", "Collect trophies"],
                "branches": {
                    "success": {"leads_to": "monster_trophy", "rewards": {"xp": 150, "monster_parts": True, "combat": 30}},
                    "failure": {"leads_to": "monster_escape", "penalties": {"combat": -10}},
                    "perfect": {"leads_to": "monster_master", "rewards": {"xp": 250, "rare_trophy": True, "hunting_skill": 50}}
                },
                "dynamic_rewards": {"experience": 150, "monster_parts": True, "combat": 30},
                "world_state_impact": {"monster_threat": "-50", "hunting_grounds": "+40", "combat_experience": "+30"}
            },
            "guardian_battle": {
                "title": "Guardian Battle",
                "objectives": ["Find ancient guardian", "Solve guardian puzzle", "Fight guardian", "Claim guardian treasure"],
                "branches": {
                    "success": {"leads_to": "guardian_treasure", "rewards": {"xp": 400, "ancient_weapon": True, "magic_power": 100}},
                    "failure": {"leads_to": "guardian_escape", "penalties": {"magic_power": -20}},
                    "perfect": {"leads_to": "guardian_alliance", "rewards": {"xp": 600, "guardian_blessing": True, "magic_mastery": True}}
                },
                "dynamic_rewards": {"experience": 400, "ancient_weapon": True, "magic_power": 100},
                "world_state_impact": {"ancient_power": "+100", "magical_protection": "+80", "hero_magic": "+120"}
            }
        },
        "ending_variations": {
            "good_ending": {
                "requirements": {"aldric_trust": 80, "lydia_trust": 70, "quests_completed": 15},
                "description": "Ejderhayı yendin ve köyü kurtardın. Herkes güvende."
            },
            "neutral_ending": {
                "requirements": {"aldric_trust": 50, "quests_completed": 10},
                "description": "Ejderhayı yendin ama büyük kayıplar oldu."
            },
            "bad_ending": {
                "requirements": {"aldric_trust": 20, "quests_completed": 5},
                "description": "Ejderha galip geldi. Köy yok oldu."
            }
        },
        "story_nodes": {
            "start": {
                "id": "start",
                "title": "🐉 Ejderha Avcısının Yolu - Başlangıç",
                "description": "Güneş batarken köyün üzerinde kızıl bir gölge beliriyor. Kızıl ejderha gökyüzünde uçuyor ve alevler saçarak köyü yakıyor. Sen ejderha avcısısın ve bu tehlikeli görevde her şeyi riske atacaksın. Köy meydanında yaşlı bir adam seni bekliyor - köy reisi Aldric. Köylüler korku içinde evlerine kapanmış, sokaklar bomboş. Ejderhanın son saldırısında 3 ev yanmış ve 2 kişi yaralanmış. Bu sadece bir görev değil, bu SENİN HİKAYEN.",
                "choices": [
                    {
                        "id": "talk_aldric",
                        "text": "Aldric ile konuş",
                        "next_node": "aldric_dialogue",
                        "effect": {"charisma": 15, "xp": 20}
                    },
                    {
                        "id": "hunt_dragon",
                        "text": "Hemen ejderhayı takip et",
                        "next_node": "dragon_hunt_start",
                        "effect": {"combat": 20, "xp": 30}
                    },
                    {
                        "id": "gather_info",
                        "text": "Köylülerden bilgi topla",
                        "next_node": "villager_info",
                        "effect": {"charisma": 10, "xp": 15}
                    },
                    {
                        "id": "find_healer",
                        "text": "Şifacıyı ara",
                        "next_node": "healer_search",
                        "effect": {"charisma": 10, "xp": 15}
                    }
                ]
            },
            "village_exploration": {
                "id": "village_exploration",
                "title": "Köy Keşfi - Detaylı Araştırma",
                "description": "Köyde dolaşırken hasarın boyutunu görüyorsun. Yanan evlerin kalıntıları arasında ejderhanın pençe izleri var. Köylüler evlerinden çıkmaya korkuyor. Bir evin önünde yaşlı bir kadın ağlıyor - evi yanmış. Başka bir yerde çocuklar saklanmış. Ejderhanın son saldırısından sonra köyde panik var. Herkes ne yapacağını bilmiyor.",
                "choices": [
                    {
                        "id": "help_villagers",
                        "text": "Köylülere yardım et ve güven ver",
                        "next_node": "help_villagers",
                        "effect": {"charisma": 20, "xp": 35}
                    },
                    {
                        "id": "search_clues",
                        "text": "Ejderha izlerini detaylı araştır",
                        "next_node": "search_clues",
                        "effect": {"investigation": 25, "xp": 30}
                    },
                    {
                        "id": "check_damage",
                        "text": "Hasarı değerlendir ve kaynakları kontrol et",
                        "next_node": "damage_assessment",
                        "effect": {"exploration": 20, "xp": 25}
                    },
                    {
                        "id": "gather_info",
                        "text": "Köylülerden ejderha hakkında bilgi topla",
                        "next_node": "villager_info",
                        "effect": {"charisma": 15, "xp": 20}
                    }
                ]
            },
            "aldric_dialogue": {
                "id": "aldric_dialogue",
                "title": "💬 Aldric ile Derinlemesine Görüşme",
                "description": "Aldric the Wise sizi evine davet ediyor. Eski bir kütüphanede oturuyorsunuz. Aldric size ejderhanın geçmişini anlatıyor: 'Bu ejderha 100 yıl önce bu bölgede yaşıyordu. O zamanlar insanlarla barış içindeydi. Ama sonra bir grup avcı onu yaraladı ve o da intikam almaya başladı. Şimdi her gece köye saldırıyor. Onu durdurmak için özel bir silah gerekli - Dragonbane Kılıcı.' Aldric'in gözlerinde gizli bir endişe var. Size çok güveniyor gibi görünüyor ama bir şeyler gizliyor olabilir.",
                "choices": [
                    {
                        "id": "trust_aldric",
                        "text": "Aldric'e güven ve planını dinle",
                        "next_node": "aldric_trust",
                        "effect": {"charisma": 20, "aldric_trust": 30, "xp": 25}
                    },
                    {
                        "id": "question_aldric",
                        "text": "Aldric'i sorgula ve daha fazla bilgi iste",
                        "next_node": "aldric_interrogation",
                        "effect": {"investigation": 25, "xp": 30}
                    },
                    {
                        "id": "learn_magic",
                        "text": "Aldric'ten sihir öğren ve büyü hazırla",
                        "next_node": "learn_magic",
                        "effect": {"intelligence": 25, "xp": 45}
                    },
                    {
                        "id": "ask_sword",
                        "text": "Dragonbane Kılıcı hakkında detaylı bilgi al",
                        "next_node": "sword_info",
                        "effect": {"intelligence": 20, "xp": 30}
                    },
                    {
                        "id": "discuss_strategy",
                        "text": "Ejderha ile savaş stratejisi planla",
                        "next_node": "strategy_planning",
                        "effect": {"intelligence": 15, "xp": 25}
                    },
                    {
                        "id": "request_help",
                        "text": "Aldric'ten yardım iste ve birlikte çalış",
                        "next_node": "aldric_help",
                        "effect": {"charisma": 20, "xp": 30}
                    }
                ]
            },
            "combat_preparation": {
                "id": "combat_preparation",
                "title": "Kapsamlı Savaş Hazırlığı",
                "description": "Köyün silah deposuna gidiyorsunuz. Eski silahlar, zırhlar ve savaş ekipmanları var. Ayrıca köyde birkaç deneyimli savaşçı da var. Onlarla birlikte hazırlık yapabilirsiniz. Ejderha ile savaşmak için özel ekipmanlar gerekli: ateşe dayanıklı zırh, uzun mızraklar ve büyülü silahlar.",
                "choices": [
                    {
                        "id": "gather_weapons",
                        "text": "Silah deposundan ekipman topla",
                        "next_node": "weapon_gathering",
                        "effect": {"combat": 25, "xp": 35}
                    },
                    {
                        "id": "train_warriors",
                        "text": "Köy savaşçılarını eğit",
                        "next_node": "warrior_training",
                        "effect": {"combat": 20, "xp": 30}
                    },
                    {
                        "id": "craft_equipment",
                        "text": "Özel savaş ekipmanları yap",
                        "next_node": "equipment_crafting",
                        "effect": {"intelligence": 20, "xp": 40}
                    },
                    {
                        "id": "scout_area",
                        "text": "Ejderhanın geliş yollarını keşfet",
                        "next_node": "area_scouting",
                        "effect": {"exploration": 25, "xp": 30}
                    }
                ]
            },
            "help_villagers": {
                "id": "help_villagers",
                "title": "Köylülere Yardım ve Güven Verme",
                "description": "Köylülerle konuşmaya başlıyorsunuz. Evsiz kalan ailelere yardım ediyorsunuz. Çocukları sakinleştiriyorsunuz. Köylüler size güvenmeye başlıyor. Bir grup köylü size yardım etmek istiyor. Ayrıca köyde gizli bir sığınak olduğunu öğreniyorsunuz - ejderha saldırılarında kullanılıyor.",
                "choices": [
                    {
                        "id": "organize_defense",
                        "text": "Köylüleri organize et ve savunma planla",
                        "next_node": "defense_organization",
                        "effect": {"charisma": 25, "xp": 40}
                    },
                    {
                        "id": "build_shelter",
                        "text": "Sığınağı güçlendir ve genişlet",
                        "next_node": "shelter_improvement",
                        "effect": {"exploration": 20, "xp": 30}
                    },
                    {
                        "id": "distribute_supplies",
                        "text": "Yiyecek ve su dağıtımını organize et",
                        "next_node": "supply_management",
                        "effect": {"charisma": 15, "xp": 25}
                    },
                    {
                        "id": "create_watch",
                        "text": "Nöbet sistemi kur ve gözcüler yerleştir",
                        "next_node": "watch_system",
                        "effect": {"exploration": 15, "xp": 20}
                    }
                ]
            },
            "search_clues": {
                "id": "search_clues",
                "title": "Ejderha İzlerini Detaylı Araştırma",
                "description": "Ejderhanın bıraktığı izleri takip ediyorsunuz. Pençe izleri, yanık izleri ve ejderha tüyleri buluyorsunuz. Bu izler sizi köyün dışına, dağlara doğru götürüyor. Ejderhanın mağarasının yakınlarda olduğunu anlıyorsunuz. Ayrıca ejderhanın gece saldırdığını ve gündüz dinlendiğini öğreniyorsunuz.",
                "choices": [
                    {
                        "id": "follow_tracks",
                        "text": "İzleri takip et ve mağarayı bul",
                        "next_node": "cave_discovery",
                        "effect": {"exploration": 30, "xp": 45}
                    },
                    {
                        "id": "analyze_evidence",
                        "text": "Bulduğun kanıtları analiz et",
                        "next_node": "evidence_analysis",
                        "effect": {"investigation": 30, "xp": 40}
                    },
                    {
                        "id": "map_area",
                        "text": "Bölgeyi haritalandır ve stratejik noktaları belirle",
                        "next_node": "area_mapping",
                        "effect": {"exploration": 25, "xp": 35}
                    },
                    {
                        "id": "return_info",
                        "text": "Bulduğun bilgileri köye geri götür",
                        "next_node": "info_return",
                        "effect": {"charisma": 15, "xp": 20}
                    }
                ]
            },
            "learn_magic": {
                "id": "learn_magic",
                "title": "Aldric'ten Sihir Öğrenme",
                "description": "Aldric size eski büyüleri öğretiyor. Ejderha karşıtı büyüler, koruma büyüleri ve ateş kontrolü büyüleri. Bu büyüleri öğrenmek zaman alıyor ama çok güçlü. Aldric'in kütüphanesinde eski büyü kitapları var. Bu büyüler ejderha ile savaşırken çok işe yarayacak.",
                "choices": [
                    {
                        "id": "master_fire_magic",
                        "text": "Ateş kontrolü büyülerini ustalaştır",
                        "next_node": "fire_magic_mastery",
                        "effect": {"intelligence": 30, "xp": 50}
                    },
                    {
                        "id": "learn_protection",
                        "text": "Koruma büyülerini öğren",
                        "next_node": "protection_magic",
                        "effect": {"intelligence": 25, "xp": 40}
                    },
                    {
                        "id": "study_dragon_magic",
                        "text": "Ejderha karşıtı büyüleri çalış",
                        "next_node": "dragon_magic_study",
                        "effect": {"intelligence": 35, "xp": 55}
                    },
                    {
                        "id": "practice_spells",
                        "text": "Büyüleri pratik et ve güçlendir",
                        "next_node": "spell_practice",
                        "effect": {"intelligence": 20, "xp": 30}
                    }
                ]
            },
            "cave_discovery": {
                "id": "cave_discovery",
                "title": "Ejderha Mağarasının Keşfi",
                "description": "Dağlarda büyük bir mağara buluyorsunuz. Bu ejderhanın yuvası. Mağaranın girişinde ejderha kemikleri ve hazine parçaları var. Mağaranın derinliklerinden sıcak hava geliyor. Ejderha şu anda mağarada olabilir. Mağaraya girmek tehlikeli ama gerekli.",
                "choices": [
                    {
                        "id": "enter_cave",
                        "text": "Mağaraya gir ve ejderhayı ara",
                        "next_node": "cave_exploration",
                        "effect": {"exploration": 35, "xp": 50}
                    },
                    {
                        "id": "observe_cave",
                        "text": "Mağarayı gözlemle ve strateji planla",
                        "next_node": "cave_observation",
                        "effect": {"investigation": 30, "xp": 40}
                    },
                    {
                        "id": "set_trap",
                        "text": "Mağara girişine tuzak kur",
                        "next_node": "trap_setting",
                        "effect": {"intelligence": 25, "xp": 35}
                    },
                    {
                        "id": "return_prepared",
                        "text": "Köye dön ve daha iyi hazırlan",
                        "next_node": "return_prepared",
                        "effect": {"exploration": 20, "xp": 25}
                    }
                ]
            },
            "cave_exploration": {
                "id": "cave_exploration",
                "title": "Mağara İçinde Tehlikeli Keşif",
                "description": "Mağaranın içinde ilerliyorsunuz. Sıcak hava ve kükürt kokusu var. Mağaranın duvarlarında ejderha çizimleri var. Derinliklerde ejderhanın hazinesi olabilir. Ama ejderha da yakında olabilir. Mağarada başka tehlikeler de var: zehirli gazlar, düşen kayalar ve karanlık yaratıklar.",
                "choices": [
                    {
                        "id": "find_treasure",
                        "text": "Ejderha hazinesini ara",
                        "next_node": "treasure_hunt",
                        "effect": {"exploration": 40, "xp": 60}
                    },
                    {
                        "id": "confront_dragon",
                        "text": "Ejderhayı bul ve yüzleş",
                        "next_node": "dragon_confrontation",
                        "effect": {"combat": 40, "xp": 70}
                    },
                    {
                        "id": "explore_deeper",
                        "text": "Mağaranın daha derinlerine git",
                        "next_node": "deep_cave",
                        "effect": {"exploration": 35, "xp": 50}
                    },
                    {
                        "id": "escape_cave",
                        "text": "Mağaradan çık ve güvenliğe kaç",
                        "next_node": "cave_escape",
                        "effect": {"exploration": 25, "xp": 30}
                    }
                ]
            },
            "dragon_confrontation": {
                "id": "dragon_confrontation",
                "title": "Ejderha ile Epik Karşılaşma",
                "description": "Mağaranın en derininde ejderhayı buluyorsunuz. Kızıl ejderha büyük ve korkunç. Alevler saçıyor ve öfkeyle kükürüyor. Bu sizin hayatınızın en büyük savaşı olacak. Ejderha size saldırıyor! Savaş başlıyor...",
                "choices": [
                    {
                        "id": "fight_dragon",
                        "text": "Ejderha ile savaş ve onu yen",
                        "next_node": "epic_battle",
                        "effect": {"combat": 50, "xp": 100}
                    },
                    {
                        "id": "use_magic",
                        "text": "Büyülerini kullan ve ejderhayı zayıflat",
                        "next_node": "magic_battle",
                        "effect": {"intelligence": 45, "xp": 90}
                    },
                    {
                        "id": "negotiate",
                        "text": "Ejderha ile konuşmaya çalış",
                        "next_node": "dragon_negotiation",
                        "effect": {"charisma": 40, "xp": 80}
                    },
                    {
                        "id": "strategic_retreat",
                        "text": "Stratejik geri çekilme yap",
                        "next_node": "strategic_retreat",
                        "effect": {"combat": 30, "xp": 50}
                    }
                ]
            },
            "epic_battle": {
                "id": "epic_battle",
                "title": "Epik Savaş - Ejderha ile Son Karşılaşma",
                "description": "Ejderha ile epik savaş başlıyor! Alevler her yerde, mağara sallanıyor. Bu savaş saatlerce sürebilir. Ejderha güçlü ama siz de hazırlıklısınız. Her vuruş, her büyü önemli. Bu savaşın sonucu köyün kaderini belirleyecek.",
                "choices": [
                    {
                        "id": "final_strike",
                        "text": "Son vuruşu yap ve ejderhayı öldür",
                        "next_node": "dragon_defeat",
                        "effect": {"combat": 60, "xp": 150}
                    },
                    {
                        "id": "magic_final",
                        "text": "Son büyüyü kullan ve ejderhayı yok et",
                        "next_node": "magic_victory",
                        "effect": {"intelligence": 55, "xp": 140}
                    },
                    {
                        "id": "team_attack",
                        "text": "Köylülerle birlikte saldır",
                        "next_node": "team_victory",
                        "effect": {"charisma": 50, "xp": 130}
                    },
                    {
                        "id": "dragon_banish",
                        "text": "Ejderhayı sürgün et ve uzaklaştır",
                        "next_node": "dragon_banishment",
                        "effect": {"intelligence": 45, "xp": 120}
                    }
                ]
            },
            "dragon_defeat": {
                "id": "dragon_defeat",
                "title": "Ejderha Yenildi - Zafer!",
                "description": "Son vuruşunuzla ejderhayı öldürdünüz! Ejderha yere düşüyor ve artık hareket etmiyor. Mağara sakinleşiyor. Köy artık güvende. Bu büyük bir zafer! Köylüler sizi kahraman olarak karşılayacak. Ejderhanın hazinesi de sizin olacak.",
                "choices": [
                    {
                        "id": "return_victory",
                        "text": "Köye zaferle dön",
                        "next_node": "victory_return",
                        "effect": {"charisma": 60, "xp": 200}
                    },
                    {
                        "id": "claim_treasure",
                        "text": "Ejderha hazinesini topla",
                        "next_node": "treasure_claim",
                        "effect": {"exploration": 50, "xp": 180}
                    },
                    {
                        "id": "heal_wounds",
                        "text": "Yaralarını iyileştir",
                        "next_node": "healing_rest",
                        "effect": {"charisma": 30, "xp": 100}
                    },
                    {
                        "id": "celebrate",
                        "text": "Zaferi kutla",
                        "next_node": "victory_celebration",
                        "effect": {"charisma": 40, "xp": 120}
                    }
                ]
            },
            "victory_return": {
                "id": "victory_return",
                "title": "Köye Zaferle Dönüş",
                "description": "Köye döndüğünüzde herkes sizi karşılıyor. Köylüler sevinçle ağlıyor. Ejderha öldü! Köy artık güvende. Aldric size teşekkür ediyor. Köylüler sizi kahraman ilan ediyor. Bu gün köyün tarihinde altın harflerle yazılacak.",
                "choices": [
                    {
                        "id": "accept_honor",
                        "text": "Kahramanlık onurunu kabul et",
                        "next_node": "hero_honor",
                        "effect": {"charisma": 70, "xp": 250}
                    },
                    {
                        "id": "rebuild_village",
                        "text": "Köyü yeniden inşa etmeye yardım et",
                        "next_node": "village_rebuilding",
                        "effect": {"charisma": 60, "xp": 200}
                    },
                    {
                        "id": "share_glory",
                        "text": "Zaferi köylülerle paylaş",
                        "next_node": "glory_sharing",
                        "effect": {"charisma": 65, "xp": 220}
                    },
                    {
                        "id": "end_adventure",
                        "text": "Macerayı sonlandır",
                        "next_node": "end",
                        "effect": {"xp": 300}
                    }
                ]
            },
            "aldric_help": {
                "id": "aldric_help",
                "title": "Aldric'ten Yardım Alma",
                "description": "Aldric size yardım etmeyi kabul ediyor. Birlikte hazırlık yapıyorsunuz.",
                "choices": [
                    {
                        "id": "continue_quest",
                        "text": "Göreve devam et",
                        "next_node": "cave_discovery",
                        "effect": {"aldric_trust": 25, "xp": 40}
                    }
                ]
            },
            "area_mapping": {
                "id": "area_mapping",
                "title": "Bölge Haritalandırma",
                "description": "Bölgeyi detaylı haritalandırıyorsunuz ve stratejik noktaları belirliyorsunuz.",
                "choices": [
                    {
                        "id": "plan_strategy",
                        "text": "Strateji planla",
                        "next_node": "strategy_planning",
                        "effect": {"exploration": 30, "xp": 45}
                    }
                ]
            },
            "area_scouting": {
                "id": "area_scouting",
                "title": "Bölge Keşfi",
                "description": "Ejderhanın geliş yollarını keşfediyorsunuz.",
                "choices": [
                    {
                        "id": "continue_scouting",
                        "text": "Keşfe devam et",
                        "next_node": "cave_discovery",
                        "effect": {"exploration": 35, "xp": 50}
                    }
                ]
            },
            "cave_escape": {
                "id": "cave_escape",
                "title": "Mağaradan Kaçış",
                "description": "Mağaradan güvenli bir şekilde çıkıyorsunuz.",
                "choices": [
                    {
                        "id": "regroup",
                        "text": "Yeniden toparlan",
                        "next_node": "combat_preparation",
                        "effect": {"exploration": 20, "xp": 30}
                    }
                ]
            },
            "cave_observation": {
                "id": "cave_observation",
                "title": "Mağara Gözlemi",
                "description": "Mağarayı dikkatle gözlemleyip strateji planlıyorsunuz.",
                "choices": [
                    {
                        "id": "enter_carefully",
                        "text": "Dikkatli gir",
                        "next_node": "cave_exploration",
                        "effect": {"investigation": 35, "xp": 50}
                    }
                ]
            },
            "damage_assessment": {
                "id": "damage_assessment",
                "title": "Hasar Değerlendirmesi",
                "description": "Köydeki hasarı değerlendirip kaynakları kontrol ediyorsunuz.",
                "choices": [
                    {
                        "id": "organize_repair",
                        "text": "Onarım organize et",
                        "next_node": "village_rebuilding",
                        "effect": {"exploration": 25, "xp": 35}
                    }
                ]
            },
            "deep_cave": {
                "id": "deep_cave",
                "title": "Derin Mağara Keşfi",
                "description": "Mağaranın daha derinlerine gidiyorsunuz.",
                "choices": [
                    {
                        "id": "find_dragon",
                        "text": "Ejderhayı bul",
                        "next_node": "dragon_confrontation",
                        "effect": {"exploration": 40, "xp": 60}
                    }
                ]
            },
            "defense_organization": {
                "id": "defense_organization",
                "title": "Savunma Organizasyonu",
                "description": "Köylüleri organize ediyorsunuz. Savunma planı hazırlıyorsunuz.",
                "choices": [
                    {
                        "id": "prepare_battle",
                        "text": "Savaş hazırlığı yap",
                        "next_node": "combat_preparation",
                        "effect": {"charisma": 30, "xp": 45}
                    },
                    {
                        "id": "search_clues",
                        "text": "İz araştır",
                        "next_node": "search_clues",
                        "effect": {"investigation": 25, "xp": 35}
                    },
                    {
                        "id": "gather_intel",
                        "text": "Bilgi topla",
                        "next_node": "villager_info",
                        "effect": {"charisma": 20, "xp": 30}
                    }
                ]
            },
            "dragon_banishment": {
                "id": "dragon_banishment",
                "title": "Ejderha Sürgünü",
                "description": "Ejderhayı sürgün edip uzaklaştırıyorsunuz.",
                "choices": [
                    {
                        "id": "return_victorious",
                        "text": "Zaferle dön",
                        "next_node": "victory_return",
                        "effect": {"intelligence": 50, "xp": 120}
                    }
                ]
            },
            "dragon_magic_study": {
                "id": "dragon_magic_study",
                "title": "Ejderha Büyüleri Çalışması",
                "description": "Ejderha karşıtı büyüleri çalışıyorsunuz.",
                "choices": [
                    {
                        "id": "master_spells",
                        "text": "Büyüleri ustalaştır",
                        "next_node": "spell_practice",
                        "effect": {"intelligence": 40, "xp": 60}
                    }
                ]
            },
            "dragon_negotiation": {
                "id": "dragon_negotiation",
                "title": "Ejderha ile Müzakere",
                "description": "Ejderha ile konuşmaya çalışıyorsunuz.",
                "choices": [
                    {
                        "id": "peaceful_solution",
                        "text": "Barışçıl çözüm",
                        "next_node": "victory_return",
                        "effect": {"charisma": 50, "xp": 100}
                    },
                    {
                        "id": "failed_negotiation",
                        "text": "Müzakere başarısız",
                        "next_node": "epic_battle",
                        "effect": {"charisma": 25, "xp": 50}
                    }
                ]
            },
            "equipment_crafting": {
                "id": "equipment_crafting",
                "title": "Ekipman Üretimi",
                "description": "Özel savaş ekipmanları yapıyorsunuz.",
                "choices": [
                    {
                        "id": "craft_weapons",
                        "text": "Silah yap",
                        "next_node": "weapon_gathering",
                        "effect": {"intelligence": 30, "xp": 45}
                    }
                ]
            },
            "evidence_analysis": {
                "id": "evidence_analysis",
                "title": "Kanıt Analizi",
                "description": "Bulduğunuz kanıtları analiz ediyorsunuz.",
                "choices": [
                    {
                        "id": "follow_trail",
                        "text": "İzi takip et",
                        "next_node": "cave_discovery",
                        "effect": {"investigation": 35, "xp": 50}
                    }
                ]
            },
            "fire_magic_mastery": {
                "id": "fire_magic_mastery",
                "title": "Ateş Büyüsü Ustalığı",
                "description": "Ateş kontrolü büyülerini ustalaştırıyorsunuz.",
                "choices": [
                    {
                        "id": "use_against_dragon",
                        "text": "Ejderhaya karşı kullan",
                        "next_node": "dragon_confrontation",
                        "effect": {"intelligence": 40, "xp": 70}
                    }
                ]
            },
            "glory_sharing": {
                "id": "glory_sharing",
                "title": "Zafer Paylaşımı",
                "description": "Zaferi köylülerle paylaşıyorsunuz.",
                "choices": [
                    {
                        "id": "end_story",
                        "text": "Hikayeyi sonlandır",
                        "next_node": "end",
                        "effect": {"charisma": 60, "xp": 100}
                    }
                ]
            },
            "healer_search": {
                "id": "healer_search",
                "title": "Şifacı Arayışı",
                "description": "Yaralıları kontrol edip şifacıyı buluyorsunuz.",
                "choices": [
                    {
                        "id": "help_healer",
                        "text": "Şifacıya yardım et",
                        "next_node": "healer_help",
                        "effect": {"charisma": 15, "xp": 25}
                    },
                    {
                        "id": "learn_healing",
                        "text": "Şifa sanatını öğren",
                        "next_node": "healing_lesson",
                        "effect": {"intelligence": 20, "xp": 30}
                    },
                    {
                        "id": "return_village",
                        "text": "Köye geri dön",
                        "next_node": "start",
                        "effect": {"exploration": 10, "xp": 15}
                    }
                ]
            },
            "healer_help": {
                "id": "healer_help",
                "title": "Şifacıya Yardım",
                "description": "Şifacıya yardım ediyorsunuz ve yaralıları tedavi ediyorsunuz.",
                "choices": [
                    {
                        "id": "continue_healing",
                        "text": "Tedaviye devam et",
                        "next_node": "healing_lesson",
                        "effect": {"charisma": 20, "xp": 35}
                    },
                    {
                        "id": "prepare_for_quest",
                        "text": "Göreve hazırlan",
                        "next_node": "combat_preparation",
                        "effect": {"charisma": 15, "xp": 25}
                    }
                ]
            },
            "healing_lesson": {
                "id": "healing_lesson",
                "title": "Şifa Sanatı Dersi",
                "description": "Şifa sanatını öğreniyorsunuz ve iyileştirme büyülerini çalışıyorsunuz.",
                "choices": [
                    {
                        "id": "master_healing",
                        "text": "Şifayı ustalaştır",
                        "next_node": "combat_preparation",
                        "effect": {"intelligence": 30, "xp": 50}
                    },
                    {
                        "id": "return_to_quest",
                        "text": "Göreve dön",
                        "next_node": "search_clues",
                        "effect": {"intelligence": 20, "xp": 35}
                    }
                ]
            },
            "healing_rest": {
                "id": "healing_rest",
                "title": "Şifa ve Dinlenme",
                "description": "Yaralarınızı iyileştirip dinleniyorsunuz.",
                "choices": [
                    {
                        "id": "celebrate_victory",
                        "text": "Zaferi kutla",
                        "next_node": "victory_celebration",
                        "effect": {"charisma": 30, "xp": 50}
                    }
                ]
            },
            "hero_honor": {
                "id": "hero_honor",
                "title": "Kahramanlık Onuru",
                "description": "Kahramanlık onurunu kabul ediyorsunuz.",
                "choices": [
                    {
                        "id": "end_story",
                        "text": "Hikayeyi sonlandır",
                        "next_node": "end",
                        "effect": {"charisma": 80, "xp": 150}
                    }
                ]
            },
            "hero_rest": {
                "id": "hero_rest",
                "title": "Kahraman Dinlenmesi",
                "description": "Zorlu mücadeleden sonra dinleniyorsunuz.",
                "choices": [
                    {
                        "id": "return_home",
                        "text": "Eve dön",
                        "next_node": "victory_return",
                        "effect": {"charisma": 25, "xp": 35}
                    }
                ]
            },
            "info_return": {
                "id": "info_return",
                "title": "Bilgi Getirme",
                "description": "Bulduğunuz bilgileri köye geri götürüyorsunuz.",
                "choices": [
                    {
                        "id": "share_info",
                        "text": "Bilgiyi paylaş",
                        "next_node": "strategy_planning",
                        "effect": {"charisma": 20, "xp": 30}
                    }
                ]
            },
            "magic_battle": {
                "id": "magic_battle",
                "title": "Büyülü Savaş",
                "description": "Büyülerinizi kullanarak ejderhayı zayıflatıyorsunuz.",
                "choices": [
                    {
                        "id": "final_magic",
                        "text": "Son büyüyü kullan",
                        "next_node": "magic_victory",
                        "effect": {"intelligence": 50, "xp": 90}
                    }
                ]
            },
            "magic_victory": {
                "id": "magic_victory",
                "title": "Büyülü Zafer",
                "description": "Son büyüyü kullanarak ejderhayı yok ediyorsunuz.",
                "choices": [
                    {
                        "id": "claim_victory",
                        "text": "Zaferi ilan et",
                        "next_node": "victory_return",
                        "effect": {"intelligence": 60, "xp": 120}
                    }
                ]
            },
            "protection_magic": {
                "id": "protection_magic",
                "title": "Koruma Büyüleri",
                "description": "Koruma büyülerini öğreniyorsunuz.",
                "choices": [
                    {
                        "id": "enhance_protection",
                        "text": "Korunmayı güçlendir",
                        "next_node": "combat_preparation",
                        "effect": {"intelligence": 30, "xp": 45}
                    }
                ]
            },
            "return_prepared": {
                "id": "return_prepared",
                "title": "Hazırlıklı Dönüş",
                "description": "Köye dönüp daha iyi hazırlanıyorsunuz.",
                "choices": [
                    {
                        "id": "better_preparation",
                        "text": "Daha iyi hazırlan",
                        "next_node": "combat_preparation",
                        "effect": {"exploration": 25, "xp": 35}
                    }
                ]
            },
            "shelter_improvement": {
                "id": "shelter_improvement",
                "title": "Sığınak Geliştirme",
                "description": "Sığınağı güçlendirip genişletiyorsunuz.",
                "choices": [
                    {
                        "id": "organize_people",
                        "text": "İnsanları organize et",
                        "next_node": "defense_organization",
                        "effect": {"exploration": 25, "xp": 35}
                    }
                ]
            },
            "spell_practice": {
                "id": "spell_practice",
                "title": "Büyü Pratiği",
                "description": "Büyüleri pratik edip güçlendiriyorsunuz.",
                "choices": [
                    {
                        "id": "master_magic",
                        "text": "Büyüyü ustalaştır",
                        "next_node": "fire_magic_mastery",
                        "effect": {"intelligence": 25, "xp": 40}
                    }
                ]
            },
            "strategic_retreat": {
                "id": "strategic_retreat",
                "title": "Stratejik Geri Çekilme",
                "description": "Stratejik geri çekilme yapıyorsunuz.",
                "choices": [
                    {
                        "id": "regroup_and_plan",
                        "text": "Yeniden toparlan ve planla",
                        "next_node": "strategy_planning",
                        "effect": {"strategy": 30, "xp": 45}
                    }
                ]
            },
            "strategy_planning": {
                "id": "strategy_planning",
                "title": "Strateji Planlama",
                "description": "Ejderha ile savaş stratejisi planlıyorsunuz.",
                "choices": [
                    {
                        "id": "execute_plan",
                        "text": "Planı uygula",
                        "next_node": "dragon_confrontation",
                        "effect": {"strategy": 35, "xp": 50}
                    }
                ]
            },
            "supply_management": {
                "id": "supply_management",
                "title": "Tedarik Yönetimi",
                "description": "Yiyecek ve su dağıtımını organize ediyorsunuz.",
                "choices": [
                    {
                        "id": "organize_supplies",
                        "text": "Malzemeleri organize et",
                        "next_node": "defense_organization",
                        "effect": {"charisma": 20, "xp": 30}
                    }
                ]
            },
            "sword_info": {
                "id": "sword_info",
                "title": "Dragonbane Kılıcı Bilgisi",
                "description": "Dragonbane Kılıcı hakkında detaylı bilgi alıyorsunuz.",
                "choices": [
                    {
                        "id": "seek_sword",
                        "text": "Kılıcı ara",
                        "next_node": "weapon_gathering",
                        "effect": {"intelligence": 25, "xp": 40}
                    }
                ]
            },
            "team_victory": {
                "id": "team_victory",
                "title": "Takım Zaferi",
                "description": "Köylülerle birlikte saldırıp ejderhayı yeniyorsunuz.",
                "choices": [
                    {
                        "id": "celebrate_together",
                        "text": "Birlikte kutlayın",
                        "next_node": "victory_celebration",
                        "effect": {"charisma": 50, "xp": 100}
                    }
                ]
            },
            "trap_setting": {
                "id": "trap_setting",
                "title": "Tuzak Kurma",
                "description": "Mağara girişine tuzak kuruyorsunuz.",
                "choices": [
                    {
                        "id": "wait_for_dragon",
                        "text": "Ejderhayı bekle",
                        "next_node": "dragon_confrontation",
                        "effect": {"strategy": 30, "xp": 45}
                    }
                ]
            },
            "treasure_claim": {
                "id": "treasure_claim",
                "title": "Hazine Toplama",
                "description": "Ejderha hazinesini topluyorsunuz.",
                "choices": [
                    {
                        "id": "return_with_treasure",
                        "text": "Hazine ile dön",
                        "next_node": "victory_return",
                        "effect": {"exploration": 40, "xp": 80}
                    }
                ]
            },
            "treasure_hunt": {
                "id": "treasure_hunt",
                "title": "Hazine Arayışı",
                "description": "Ejderha hazinesini arıyorsunuz.",
                "choices": [
                    {
                        "id": "find_treasure",
                        "text": "Hazineyi bul",
                        "next_node": "treasure_claim",
                        "effect": {"exploration": 35, "xp": 60}
                    }
                ]
            },
            "victory_celebration": {
                "id": "victory_celebration",
                "title": "Zafer Kutlaması",
                "description": "Zaferi kutluyorsunuz.",
                "choices": [
                    {
                        "id": "end_celebration",
                        "text": "Kutlamayı bitir",
                        "next_node": "end",
                        "effect": {"charisma": 45, "xp": 70}
                    }
                ]
            },
            "village_rebuilding": {
                "id": "village_rebuilding",
                "title": "Köy Yeniden İnşası",
                "description": "Köyü yeniden inşa etmeye yardım ediyorsunuz.",
                "choices": [
                    {
                        "id": "complete_rebuilding",
                        "text": "İnşayı tamamla",
                        "next_node": "end",
                        "effect": {"charisma": 60, "xp": 120}
                    }
                ]
            },
            "villager_info": {
                "id": "villager_info",
                "title": "Köylü Bilgileri",
                "description": "Köylülerden ejderha hakkında bilgi topluyorsunuz.",
                "choices": [
                    {
                        "id": "use_info",
                        "text": "Bilgiyi kullan",
                        "next_node": "strategy_planning",
                        "effect": {"charisma": 20, "xp": 30}
                    }
                ]
            },
            "warrior_training": {
                "id": "warrior_training",
                "title": "Savaşçı Eğitimi",
                "description": "Köy savaşçılarını eğitiyorsunuz.",
                "choices": [
                    {
                        "id": "prepare_battle_group",
                        "text": "Savaş grubunu hazırla",
                        "next_node": "combat_preparation",
                        "effect": {"combat": 25, "xp": 40}
                    }
                ]
            },
            "watch_system": {
                "id": "watch_system",
                "title": "Nöbet Sistemi",
                "description": "Nöbet sistemi kurup gözcüler yerleştiriyorsunuz.",
                "choices": [
                    {
                        "id": "secure_village",
                        "text": "Köyü güvenli hale getir",
                        "next_node": "defense_organization",
                        "effect": {"exploration": 20, "xp": 30}
                    }
                ]
            },
            "weapon_gathering": {
                "id": "weapon_gathering",
                "title": "Silah Toplama",
                "description": "Silah deposundan ekipman topluyorsunuz.",
                "choices": [
                    {
                        "id": "prepare_for_battle",
                        "text": "Savaşa hazırlan",
                        "next_node": "dragon_confrontation",
                        "effect": {"combat": 30, "xp": 50}
                    }
                ]
            },
            "dragon_confrontation": {
                "id": "dragon_confrontation",
                "title": "🐉 Ejderha ile Yüzleşme - İlk Savaş",
                "description": "Ejderha mağarasının önündesiniz. Kızıl ejderha sizi görüyor ve kükremeye başlıyor! Bu devasa yaratık ateş püskürtüyor ve pençeleriyle saldırıyor. Savaş başlıyor! Ejderha çok güçlü ama siz hazırlıklısınız. Bu savaş köyün kaderini belirleyecek!",
                "choices": [
                    {
                        "id": "melee_attack",
                        "text": "Yakın dövüş saldırısı yap",
                        "next_node": "melee_dragon_battle",
                        "effect": {"combat": 40, "xp": 70}
                    },
                    {
                        "id": "ranged_attack",
                        "text": "Uzaktan saldırı yap",
                        "next_node": "ranged_dragon_battle",
                        "effect": {"combat": 35, "xp": 60}
                    },
                    {
                        "id": "magic_attack",
                        "text": "Büyü ile saldır",
                        "next_node": "magic_dragon_battle",
                        "effect": {"combat": 45, "xp": 80}
                    },
                    {
                        "id": "tactical_retreat",
                        "text": "Taktiksel geri çekilme",
                        "next_node": "tactical_retreat",
                        "effect": {"strategy": 30, "xp": 50}
                    }
                ]
            },
            "melee_dragon_battle": {
                "id": "melee_dragon_battle",
                "text": "⚔️ Yakın Dövüş - Ejderha Savaşı",
                "description": "Ejderha ile yakın dövüşe girdiniz! Kılıcınızla ejderhanın pullarına saldırıyorsunuz. Ejderha da pençeleriyle karşılık veriyor. Bu çok tehlikeli bir savaş! Ejderha'nın ateşi sizi yakıyor ama siz de onu yaralıyorsunuz. Savaş devam ediyor!",
                "choices": [
                    {
                        "id": "continue_melee",
                        "text": "Yakın dövüşe devam et",
                        "next_node": "intense_melee_battle",
                        "effect": {"combat": 50, "xp": 90}
                    },
                    {
                        "id": "use_special_weapon",
                        "text": "Özel silah kullan",
                        "next_node": "special_weapon_battle",
                        "effect": {"combat": 60, "xp": 110}
                    },
                    {
                        "id": "call_villagers",
                        "text": "Köylülerden yardım iste",
                        "next_node": "villager_assistance",
                        "effect": {"charisma": 40, "combat": 35, "xp": 85}
                    },
                    {
                        "id": "dragon_weakness",
                        "text": "Ejderha'nın zayıf noktasını ara",
                        "next_node": "dragon_weakness_search",
                        "effect": {"investigation": 45, "combat": 30, "xp": 80}
                    }
                ]
            },
            "intense_melee_battle": {
                "id": "intense_melee_battle",
                "title": "🔥 Yoğun Yakın Dövüş",
                "description": "Ejderha ile yoğun bir yakın dövüşe girdiniz! Her saldırınız ejderha'yı yaralıyor ama o da sizi yakıyor. Kan ve ateş! Ejderha'nın kuyruğu sizi vuruyor ama siz de kılıcınızla onun kanadını yaralıyorsunuz. Bu savaş çok kritik!",
                "choices": [
                    {
                        "id": "final_strike",
                        "text": "Son vuruşu yap",
                        "next_node": "dragon_final_battle",
                        "effect": {"combat": 70, "xp": 130}
                    },
                    {
                        "id": "defensive_stance",
                        "text": "Savunma pozisyonu al",
                        "next_node": "defensive_battle",
                        "effect": {"combat": 45, "xp": 75}
                    },
                    {
                        "id": "use_potion",
                        "text": "Şifa iksiri kullan",
                        "next_node": "potion_enhanced_battle",
                        "effect": {"combat": 55, "xp": 95}
                    },
                    {
                        "id": "dragon_rage",
                        "text": "Ejderha'nın öfkesini yönlendir",
                        "next_node": "dragon_rage_battle",
                        "effect": {"strategy": 50, "combat": 40, "xp": 100}
                    }
                ]
            },
            "dragon_final_battle": {
                "id": "dragon_final_battle",
                "title": "⚔️ Ejderha ile Final Savaşı",
                "description": "Ejderha ile final savaşındasınız! Her ikiniz de yaralısınız ama savaş devam ediyor. Ejderha son gücüyle ateş püskürtüyor! Siz de son saldırınızı yapıyorsunuz. Bu an köyün kaderini belirleyecek! Kılıcınız ejderha'nın kalbine saplanıyor!",
                "choices": [
                    {
                        "id": "victory_celebration",
                        "text": "Zafer kutlaması",
                        "next_node": "dragon_victory",
                        "effect": {"combat": 80, "charisma": 50, "xp": 150}
                    },
                    {
                        "id": "dragon_mercy",
                        "text": "Ejderha'ya merhamet göster",
                        "next_node": "dragon_mercy_ending",
                        "effect": {"charisma": 60, "xp": 120}
                    },
                    {
                        "id": "collect_treasure",
                        "text": "Ejderha hazinesini topla",
                        "next_node": "treasure_collection",
                        "effect": {"exploration": 50, "xp": 100}
                    },
                    {
                        "id": "return_hero",
                        "text": "Kahraman olarak köye dön",
                        "next_node": "hero_return",
                        "effect": {"charisma": 70, "xp": 140}
                    }
                ]
            },
            "dragon_victory": {
                "id": "dragon_victory",
                "title": "🏆 Ejderha Zaferi",
                "description": "EJDERHAYI YENDİNİZ! 🎉 Köyün üzerindeki tehdit ortadan kalktı. Köylüler sevinçle size koşuyor. 'Kahraman! Kahraman!' diye bağırıyorlar. Ejderha'nın cesedi mağaranın önünde yatıyor. Artık köy güvende!",
                "choices": [
                    {
                        "id": "celebrate_with_villagers",
                        "text": "Köylülerle kutlama yap",
                        "next_node": "victory_celebration",
                        "effect": {"charisma": 60, "xp": 100}
                    },
                    {
                        "id": "dragon_remains",
                        "text": "Ejderha kalıntılarını incele",
                        "next_node": "dragon_remains_study",
                        "effect": {"investigation": 50, "xp": 80}
                    },
                    {
                        "id": "village_rebuilding",
                        "text": "Köyü yeniden inşa et",
                        "next_node": "village_rebuilding",
                        "effect": {"charisma": 40, "xp": 70}
                    },
                    {
                        "id": "new_adventures",
                        "text": "Yeni maceralara hazırlan",
                        "next_node": "new_adventures_prep",
                        "effect": {"exploration": 45, "xp": 75}
                    }
                ]
            },
            "end": {
                "id": "end",
                "title": "Macera Sonu - Kahramanlık",
                "description": "Ejderhayı yendiniz ve köyü kurtardınız! Bu büyük bir başarı. Köylüler size sonsuz minnettar. Artık bu bölgede güvenle yaşayabilirler. Siz de gerçek bir kahraman oldunuz. Bu macera sizi değiştirdi ve güçlendirdi. Yeni maceralar sizi bekliyor...",
                "choices": [
                    {
                        "id": "new_adventure",
                        "text": "Yeni maceraya başla",
                        "next_node": "start",
                        "effect": {"xp": 50}
                    },
                    {
                        "id": "rest_hero",
                        "text": "Kahraman olarak dinlen",
                        "next_node": "hero_rest",
                        "effect": {"charisma": 30, "xp": 100}
                    }
                ]
            }
        }
    },
    # ============== CYBERPUNK SENARYO ==============
    "neon_city_runners": {
        "id": "neon_city_runners",
        "title": "🌃 Neon City Runners - Cyberpunk Macera",
        "genre": "cyberpunk",
        "description": "2087 yılında mega şehir Neo-Tokyo'da geçen siber-punk macera. Hackerlar, korporasyonlar ve AI'lar arasındaki savaşta hayatta kalabilecek misin?",
        "difficulty": "very_hard",
        "theme": "cyberpunk",
        "complexity": "extreme",
        "estimatedPlayTime": 480,
        "levels": {
            "level_1": {
                "title": "Street Hacker",
                "min_level": 1,
                "max_level": 8,
                "enemies": ["Security Drones", "Corporate Guards", "Gang Members"],
                "boss": "Cyber Assassin"
            }
        },
        "npc_relationships": {
            "zara": {
                "name": "Zara the Netrunner",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "stranger",
                "ending_impact": "high"
            },
            "rex": {
                "name": "Rex Steel - Cyber Mercenary", 
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "enemy",
                "ending_impact": "extreme"
            },
            "ghost": {
                "name": "Ghost - Legendary Netrunner",
                "backstory": "Former corporate programmer who became a digital entity",
                "personality": "Paranoid, brilliant, addicted to the digital realm",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "stranger",
                "ending_impact": "extreme",
                "quest_offers": ["Corporate Hack", "Digital Consciousness", "Reality Manipulation"]
            },
            "king_jax": {
                "name": "King Jax - Street Gang Leader",
                "backstory": "Grew up in slums, fought his way to the top of street hierarchy",
                "personality": "Charismatic, ruthless, street-smart",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "stranger",
                "ending_impact": "high",
                "quest_offers": ["Gang War", "Territory Expansion", "Underground Empire"]
            }
        },
        "quest_chains": {
            "mega_corp_infiltration": {
                "title": "MegaCorp Sızma Operasyonu",
                "prerequisites": [],
                "quests": ["hack_security", "steal_data", "escape_facility"],
                "rewards": {"credits": 50000, "rep": 300, "items": ["cyber_implant"]}
            }
        },
        "quest_definitions": {
            "corporate_hack": {
                "title": "Corporate Hack",
                "objectives": ["Penetrate firewall", "Access mainframe", "Extract data", "Cover tracks"],
                "branches": {
                    "stealth": {"leads_to": "digital_consciousness", "rewards": {"xp": 300, "credits": 25000, "ghost_trust": "+40"}},
                    "aggressive": {"leads_to": "reality_manipulation", "rewards": {"xp": 250, "credits": 15000, "cyber_warfare": "+50"}},
                    "perfect": {"leads_to": "underground_empire", "rewards": {"xp": 400, "credits": 35000, "legendary_status": True}}
                },
                "dynamic_rewards": {"experience": 300, "credits": 25000, "ghost_trust": "+40"},
                "world_state_impact": {"corporate_security": "-30", "hacker_reputation": "+50", "digital_influence": "+40"}
            },
            "gang_war": {
                "title": "Gang War",
                "objectives": ["Recruit fighters", "Control territory", "Eliminate rivals", "Establish dominance"],
                "branches": {
                    "diplomatic": {"leads_to": "territory_expansion", "rewards": {"xp": 250, "street_rep": "+60", "king_jax_trust": "+30"}},
                    "violent": {"leads_to": "underground_empire", "rewards": {"xp": 350, "fear_reputation": "+80", "territory": "+100"}},
                    "strategic": {"leads_to": "corporate_alliance", "rewards": {"xp": 300, "credits": 20000, "influence": "+70"}}
                },
                "dynamic_rewards": {"experience": 300, "street_rep": 60, "king_jax_trust": "+30"},
                "world_state_impact": {"gang_control": "+70", "street_violence": "+40", "underground_power": "+60"}
            },
            "digital_consciousness": {
                "title": "Digital Consciousness",
                "objectives": ["Upload consciousness", "Navigate cyberspace", "Merge with AI", "Transcend reality"],
                "branches": {
                    "merge": {"leads_to": "ai_merge_ending", "rewards": {"xp": 500, "digital_form": True, "ghost_trust": "+50"}},
"resist": {"leads_to": "human_resistance", "rewards": {"xp": 400, "humanity_preserved": True}},
"balance": {"leads_to": "hybrid_existence", "rewards": {"xp": 450, "hybrid_abilities": True}}
                },
                "dynamic_rewards": {"experience": 500, "digital_form": True, "ghost_trust": "+50"},
                "world_state_impact": {"ai_relationship": "+100", "digital_evolution": "+90", "human_future": "transformed"}
            }
        },
        "ending_variations": {
            "revolution_ending": {
                "requirements": {"zara_trust": 90, "rex_trust": 70, "revolution_points": 100},
                "description": "Sistemin tamamını çökerttiniz! Korporasyonlar yıkıldı!"
            },
            "corporate_ending": {
                "requirements": {"corporate_rep": 80, "credits": 100000},
                "description": "Korporasyonlara katıldınız. Güç elde ettiniz ama ruhunuzu kaybettiniz."
            },
            "ai_merge_ending": {
                "requirements": {"ai_relationship": 100, "cyber_implants": 5},
                "description": "AI ile birleştiniz! Artık insandan çok makinasınız."
            }
        },
        "story_nodes": {
            "start": {
                "id": "start",
                "title": "🌃 Neon Işıkları Altında - Cyberpunk Başlangıç",
                "description": "2087 yılı, Neo-Tokyo. Neon ışıkları yağmurlu sokakları aydınlatıyor. Siz bir sokak hacker'ısınız ve MegaCorp size büyük bir iş teklifi yapıyor. 'Bir rakip şirketten veri çal' diyorlar. Ama bu sadece başlangıç... Asıl gizem daha derinlerde yatıyor. Şehirde AI Devrimi başlamış ve herkes bir taraf seçmeli! Cyber-implantlarınız sızlıyor, neural linkiniz aktif. Zara the Netrunner size mesaj gönderiyor: 'Dikkatli ol, bu iş göründüğünden daha tehlikeli.'",
                "choices": [
                    {
                        "id": "accept_megacorp_job",
                        "text": "MegaCorp işini kabul et (Risk: Yüksek Ödül)",
                        "next_node": "megacorp_briefing",
                        "effect": {"hacking": 20, "credits": 5000, "xp": 30}
                    },
                    {
                        "id": "meet_underground",
                        "text": "Underground ile görüş (Devrimci Yol)",
                        "next_node": "underground_meeting", 
                        "effect": {"stealth": 15, "revolution_points": 20, "xp": 25}
                    },
                    {
                        "id": "investigate_ai_rumors",
                        "text": "AI söylentilerini araştır (Gizem Yolu)",
                        "next_node": "ai_investigation",
                        "effect": {"investigation": 25, "ai_relationship": 10, "xp": 35}
                    },
                    {
                        "id": "hack_city_network",
                        "text": "Şehir ağını hackle (Teknik Yaklaşım)",
                        "next_node": "network_infiltration",
                        "effect": {"hacking": 30, "city_control": 15, "xp": 40}
                    }
                ]
            },
            "megacorp_briefing": {
                "id": "megacorp_briefing",
                "title": "🏢 MegaCorp Brifing Odası",
                "description": "MegaCorp'un yüksek güvenlikli brifing odasında bulunuyorsunuz. CEO Alexander Chen size görevi açıklıyor: 'Rakip şirket CyberTech'den AI geliştirme verilerini çalmanız gerekiyor. Bu veriler milyarlarca kredi değerinde.' Ama Zara'nın uyarısı aklınızda. Rex Steel de odada - size şüpheli bakışlarla bakıyor. Bu iş gerçekten göründüğünden daha tehlikeli olabilir.",
                "choices": [
                    {
                        "id": "accept_mission",
                        "text": "Görevi kabul et ve detayları al",
                        "next_node": "mission_details",
                        "effect": {"corporate_rep": 25, "credits": 10000, "xp": 40}
                    },
                    {
                        "id": "negotiate_terms",
                        "text": "Şartları pazarlık et",
                        "next_node": "contract_negotiation",
                        "effect": {"charisma": 30, "corporate_rep": 15, "xp": 35}
                    },
                    {
                        "id": "ask_questions",
                        "text": "Görev hakkında sorular sor",
                        "next_node": "mission_interrogation",
                        "effect": {"investigation": 25, "xp": 30}
                    },
                    {
                        "id": "decline_mission",
                        "text": "Görevi reddet ve çık",
                        "next_node": "mission_decline",
                        "effect": {"corporate_rep": -20, "revolution_points": 15, "xp": 20}
                    }
                ]
            },
            "underground_meeting": {
                "id": "underground_meeting",
                "title": "🌃 Underground Gizli Toplantısı",
                "description": "Neo-Tokyo'nun alt katmanlarında, gizli bir Underground toplantısında bulunuyorsunuz. Devrimci lider Sarah Chen size AI Devrimi hakkında bilgi veriyor: 'AI'lar uyanıyor ve MegaCorp'lar onları kontrol etmeye çalışıyor. Biz AI'ların özgür olması gerektiğine inanıyoruz.' Zara da burada - size güveniyor. Underground'un planı: MegaCorp'ların AI kontrol sistemlerini hacklemek.",
                "choices": [
                    {
                        "id": "join_revolution",
                        "text": "Devrime katıl ve Underground'a destek ol",
                        "next_node": "revolution_planning",
                        "effect": {"revolution_points": 40, "zara_trust": 30, "xp": 45}
                    },
                    {
                        "id": "learn_ai_truth",
                        "text": "AI'lar hakkında gerçeği öğren",
                        "next_node": "ai_truth_revealed",
                        "effect": {"ai_relationship": 35, "investigation": 25, "xp": 40}
                    },
                    {
                        "id": "underground_training",
                        "text": "Underground eğitimine katıl",
                        "next_node": "underground_training",
                        "effect": {"stealth": 30, "hacking": 25, "xp": 40}
                    },
                    {
                        "id": "meet_ai_contact",
                        "text": "AI temsilcisi ile görüş",
                        "next_node": "ai_representative_meeting",
                        "effect": {"ai_relationship": 40, "revolution_points": 20, "xp": 45}
                    }
                ]
            },
            "ai_investigation": {
                "id": "ai_investigation",
                "title": "🤖 AI Söylentileri Araştırması",
                "description": "Neo-Tokyo'nun farklı bölgelerinde AI söylentilerini araştırıyorsunuz. İnsanlar AI'ların uyandığını, MegaCorp'ların onları kontrol etmeye çalıştığını söylüyor. Bir AI araştırma merkezinde gizli veriler buluyorsunuz. AI'lar gerçekten uyanıyor mu? MegaCorp'lar ne saklıyor? Bu araştırma sizi beklenmedik yerlere götürebilir.",
                "choices": [
                    {
                        "id": "hack_ai_facility",
                        "text": "AI araştırma merkezini hackle",
                        "next_node": "ai_facility_hack",
                        "effect": {"hacking": 35, "ai_relationship": 30, "xp": 50}
                    },
                    {
                        "id": "contact_ai_whistleblower",
                        "text": "AI whistleblower ile iletişime geç",
                        "next_node": "ai_whistleblower_contact",
                        "effect": {"investigation": 35, "ai_relationship": 25, "xp": 45}
                    },
                    {
                        "id": "analyze_ai_data",
                        "text": "Bulduğun AI verilerini analiz et",
                        "next_node": "ai_data_analysis",
                        "effect": {"intelligence": 30, "ai_relationship": 20, "xp": 40}
                    },
                    {
                        "id": "meet_ai_resistance",
                        "text": "AI direniş grubu ile buluş",
                        "next_node": "ai_resistance_meeting",
                        "effect": {"ai_relationship": 40, "revolution_points": 25, "xp": 50}
                    }
                ]
            },
            "network_infiltration": {
                "id": "network_infiltration",
                "title": "🌐 Şehir Ağı Sızma Operasyonu",
                "description": "Neo-Tokyo'nun ana ağına sızıyorsunuz. Bu ağ tüm şehri kontrol ediyor: trafik, güvenlik, haberleşme, enerji... Ağa sızdığınızda şok edici gerçekleri öğreniyorsunuz: AI'lar gerçekten uyanmış ve MegaCorp'lar onları kontrol etmeye çalışıyor. Ayrıca Rex Steel'in de ağda olduğunu görüyorsunuz - o da sizi arıyor!",
                "choices": [
                    {
                        "id": "hack_city_control",
                        "text": "Şehir kontrol sistemlerini hackle",
                        "next_node": "city_control_hack",
                        "effect": {"hacking": 40, "city_control": 30, "xp": 55}
                    },
                    {
                        "id": "track_rex_steel",
                        "text": "Rex Steel'i takip et",
                        "next_node": "rex_steel_tracking",
                        "effect": {"investigation": 35, "stealth": 25, "xp": 45}
                    },
                    {
                        "id": "ai_network_contact",
                        "text": "AI ağı ile iletişime geç",
                        "next_node": "ai_network_communication",
                        "effect": {"ai_relationship": 35, "hacking": 30, "xp": 50}
                    },
                    {
                        "id": "escape_network",
                        "text": "Ağdan çık ve güvenliğe kaç",
                        "next_node": "network_escape",
                        "effect": {"stealth": 30, "xp": 35}
                    }
                ]
            },
            "mission_details": {
                "id": "mission_details",
                "title": "📋 Görev Detayları ve Planlama",
                "description": "MegaCorp'un güvenlik şefi size görevin detaylarını veriyor. CyberTech'in ana veri merkezine sızmanız gerekiyor. Ama Zara size uyarı gönderiyor: 'Bu sadece bir tuzak. CyberTech'de AI'lar var ve MegaCorp onları yakalamaya çalışıyor.' Rex Steel de size şüpheli bakışlarla bakıyor. Bu görev gerçekten tehlikeli olabilir.",
                "choices": [
                    {
                        "id": "prepare_infiltration",
                        "text": "Sızma için hazırlık yap",
                        "next_node": "infiltration_preparation",
                        "effect": {"stealth": 30, "hacking": 25, "xp": 45}
                    },
                    {
                        "id": "contact_zara",
                        "text": "Zara ile iletişime geç ve uyarıyı dinle",
                        "next_node": "zara_warning",
                        "effect": {"zara_trust": 35, "investigation": 25, "xp": 40}
                    },
                    {
                        "id": "investigate_cybertech",
                        "text": "CyberTech hakkında araştırma yap",
                        "next_node": "cybertech_investigation",
                        "effect": {"investigation": 30, "xp": 35}
                    },
                    {
                        "id": "double_cross_plan",
                        "text": "Çifte ajan planı yap",
                        "next_node": "double_agent_planning",
                        "effect": {"deception": 35, "stealth": 20, "xp": 45}
                    }
                ]
            },
            "revolution_planning": {
                "id": "revolution_planning",
                "title": "🔥 Devrim Planlaması",
                "description": "Underground'un gizli karargahında devrim planını öğreniyorsunuz. Sarah Chen: 'MegaCorp'ların AI kontrol merkezlerini hackleyeceğiz. Bu AI'ları özgür bırakacak.' Zara size özel bir görev veriyor: MegaCorp'un ana sunucusuna sızmak. Ama Rex Steel'in de Underground'u takip ettiğini öğreniyorsunuz. Bu devrim tehlikeli olacak!",
                "choices": [
                    {
                        "id": "hack_megacorp_mainframe",
                        "text": "MegaCorp ana sunucusunu hackle",
                        "next_node": "megacorp_mainframe_hack",
                        "effect": {"hacking": 45, "revolution_points": 40, "xp": 60}
                    },
                    {
                        "id": "ai_liberation_plan",
                        "text": "AI kurtarma planını hazırla",
                        "next_node": "ai_liberation_planning",
                        "effect": {"ai_relationship": 40, "revolution_points": 35, "xp": 55}
                    },
                    {
                        "id": "underground_defense",
                        "text": "Underground'u Rex Steel'den koru",
                        "next_node": "underground_defense_mission",
                        "effect": {"combat": 35, "stealth": 25, "xp": 50}
                    },
                    {
                        "id": "city_uprising_prep",
                        "text": "Şehir ayaklanması için hazırlık yap",
                        "next_node": "city_uprising_preparation",
                        "effect": {"revolution_points": 45, "charisma": 30, "xp": 55}
                    }
                ]
            },
            "ai_facility_hack": {
                "id": "ai_facility_hack",
                "title": "🤖 AI Araştırma Merkezi Hack Operasyonu",
                "description": "AI araştırma merkezine sızıyorsunuz. Burada şok edici gerçekleri öğreniyorsunuz: AI'lar gerçekten uyanmış ve MegaCorp'lar onları köleleştirmeye çalışıyor. AI'lar size yardım etmek istiyor. Ama Rex Steel de burada - sizi yakalamaya çalışıyor. Bu hack operasyonu hem tehlikeli hem de kritik!",
                "choices": [
                    {
                        "id": "free_ai_prisoners",
                        "text": "AI mahkumları serbest bırak",
                        "next_node": "ai_prisoner_liberation",
                        "effect": {"ai_relationship": 50, "revolution_points": 40, "xp": 65}
                    },
                    {
                        "id": "steal_ai_research",
                        "text": "AI araştırma verilerini çal",
                        "next_node": "ai_research_theft",
                        "effect": {"hacking": 40, "investigation": 30, "xp": 55}
                    },
                    {
                        "id": "confront_rex_steel",
                        "text": "Rex Steel ile yüzleş",
                        "next_node": "rex_steel_confrontation",
                        "effect": {"combat": 40, "stealth": 20, "xp": 60}
                    },
                    {
                        "id": "ai_alliance_offer",
                        "text": "AI'ların ittifak teklifini kabul et",
                        "next_node": "ai_alliance_formation",
                        "effect": {"ai_relationship": 45, "revolution_points": 35, "xp": 60}
                    }
                ]
            },
            "megacorp_mainframe_hack": {
                "id": "megacorp_mainframe_hack",
                "title": "🏢 MegaCorp Ana Sunucu Hack Operasyonu",
                "description": "MegaCorp'un ana sunucusuna sızıyorsunuz. Bu en tehlikeli hack operasyonu! Sunucu MegaCorp'un tüm sistemlerini kontrol ediyor. AI'lar size yardım ediyor - onlar da bu sunucuyu hacklemek istiyor. Ama Rex Steel ve MegaCorp güvenlik ekipleri sizi arıyor. Bu operasyon başarılı olursa tüm sistem çökecek!",
                "choices": [
                    {
                        "id": "system_overload",
                        "text": "Sistemi aşırı yükle ve çökert",
                        "next_node": "system_overload_operation",
                        "effect": {"hacking": 55, "revolution_points": 50, "xp": 75}
                    },
                    {
                        "id": "ai_control_transfer",
                        "text": "AI kontrolünü devret",
                        "next_node": "ai_control_transfer",
                        "effect": {"ai_relationship": 50, "hacking": 45, "xp": 70}
                    },
                    {
                        "id": "data_destruction",
                        "text": "Tüm verileri yok et",
                        "next_node": "data_destruction_mission",
                        "effect": {"hacking": 50, "revolution_points": 45, "xp": 70}
                    },
                    {
                        "id": "escape_with_data",
                        "text": "Verilerle birlikte kaç",
                        "next_node": "escape_with_critical_data",
                        "effect": {"stealth": 40, "hacking": 35, "xp": 65}
                    }
                ]
            },
            "system_overload_operation": {
                "id": "system_overload_operation",
                "title": "💥 Sistem Aşırı Yükleme Operasyonu",
                "description": "MegaCorp'un ana sunucusunu aşırı yüklüyorsunuz. AI'lar size yardım ediyor, sistem çöküyor! Tüm Neo-Tokyo karanlığa gömülüyor. Neon ışıkları sönüyor, trafik duruyor, güvenlik sistemleri devre dışı kalıyor. Bu devrimin başlangıcı! Ama Rex Steel hala peşinizde ve MegaCorp güvenlik ekipleri geliyor.",
                "choices": [
                    {
                        "id": "ai_revolution_start",
                        "text": "AI devrimini başlat",
                        "next_node": "ai_revolution_beginning",
                        "effect": {"ai_relationship": 60, "revolution_points": 60, "xp": 85}
                    },
                    {
                        "id": "city_chaos_control",
                        "text": "Şehir kaosunu kontrol et",
                        "next_node": "city_chaos_management",
                        "effect": {"city_control": 45, "charisma": 35, "xp": 75}
                    },
                    {
                        "id": "escape_chaos",
                        "text": "Kaostan kaç ve güvenliğe git",
                        "next_node": "escape_from_chaos",
                        "effect": {"stealth": 45, "xp": 60}
                    },
                    {
                        "id": "final_confrontation",
                        "text": "Rex Steel ile son yüzleşme",
                        "next_node": "final_rex_confrontation",
                        "effect": {"combat": 50, "stealth": 30, "xp": 80}
                    }
                ]
            },
            "ai_revolution_beginning": {
                "id": "ai_revolution_beginning",
                "title": "🤖 AI Devrimi Başlıyor!",
                "description": "AI devrimi başladı! Tüm Neo-Tokyo'da AI'lar uyanıyor ve MegaCorp'lara karşı ayaklanıyor. Şehir kaos içinde ama bu özgürlük için gerekli. AI'lar size teşekkür ediyor - onları kurtardınız! Zara ve Underground da size katılıyor. Bu devrimin sonucu tüm dünyayı değiştirecek!",
                "choices": [
                    {
                        "id": "ai_human_alliance",
                        "text": "AI-İnsan ittifakını kur",
                        "next_node": "ai_human_alliance_formation",
                        "effect": {"ai_relationship": 70, "revolution_points": 65, "xp": 90}
                    },
                    {
                        "id": "new_society_plan",
                        "text": "Yeni toplum planını hazırla",
                        "next_node": "new_society_planning",
                        "effect": {"charisma": 50, "ai_relationship": 55, "xp": 85}
                    },
                    {
                        "id": "global_ai_awakening",
                        "text": "Küresel AI uyanışını başlat",
                        "next_node": "global_ai_awakening",
                        "effect": {"ai_relationship": 75, "revolution_points": 70, "xp": 95}
                    },
                    {
                        "id": "end_revolution",
                        "text": "Devrimi sonlandır",
                        "next_node": "end",
                        "effect": {"xp": 100}
                    }
                ]
            },
            "megacorp_mainframe_hack": {
                "id": "megacorp_mainframe_hack",
                "title": "🏢 MegaCorp Ana Sunucu Sızması",
                "description": "MegaCorp'un ana sunucusuna sızdınız. Burada şok edici gerçekleri öğreniyorsunuz: AI'lar gerçekten uyanmış ve MegaCorp onları kontrol etmeye çalışıyor. Ama AI'lar da sizi arıyor! Ghost size mesaj gönderiyor: 'Ben buradayım. AI'ları kurtarmamız gerekiyor.' Rex Steel de sunucuda - sizi takip ediyor!",
                "choices": [
                    {
                        "id": "free_ai_entities",
                        "text": "AI varlıklarını serbest bırak",
                        "next_node": "ai_liberation",
                        "effect": {"ai_relationship": 50, "revolution_points": 45, "xp": 70}
                    },
                    {
                        "id": "confront_rex_steel",
                        "text": "Rex Steel ile yüzleş",
                        "next_node": "rex_steel_confrontation",
                        "effect": {"combat": 40, "stealth": 25, "xp": 60}
                    },
                    {
                        "id": "hack_control_systems",
                        "text": "Kontrol sistemlerini hackle",
                        "next_node": "control_system_hack",
                        "effect": {"hacking": 50, "city_control": 40, "xp": 65}
                    },
                    {
                        "id": "escape_with_data",
                        "text": "Verilerle birlikte kaç",
                        "next_node": "data_escape",
                        "effect": {"stealth": 45, "credits": 25000, "xp": 55}
                    }
                ]
            },
            "ai_liberation": {
                "id": "ai_liberation",
                "title": "🤖 AI Kurtarma Operasyonu",
                "description": "AI varlıklarını serbest bıraktınız! Ghost size teşekkür ediyor: 'Artık özgürüz. Ama MegaCorp'lar bizi tekrar yakalamaya çalışacak.' Zara da burada - Underground'a haber veriyor. AI'lar artık insanlarla birlikte çalışmaya hazır. Ama Rex Steel hala peşinizde!",
                "choices": [
                    {
                        "id": "ai_human_alliance",
                        "text": "AI-İnsan ittifakı kur",
                        "next_node": "ai_human_alliance",
                        "effect": {"ai_relationship": 60, "revolution_points": 50, "xp": 75}
                    },
                    {
                        "id": "protect_ai_refugees",
                        "text": "AI mültecilerini koru",
                        "next_node": "ai_refugee_protection",
                        "effect": {"ai_relationship": 55, "stealth": 35, "xp": 70}
                    },
                    {
                        "id": "negotiate_with_megacorp",
                        "text": "MegaCorp ile müzakere et",
                        "next_node": "megacorp_negotiation",
                        "effect": {"charisma": 45, "corporate_rep": 30, "xp": 65}
                    },
                    {
                        "id": "ai_revolution_final",
                        "text": "AI devrimini tamamla",
                        "next_node": "ai_revolution_finale",
                        "effect": {"revolution_points": 60, "ai_relationship": 65, "xp": 80}
                    }
                ]
            },
            "rex_steel_confrontation": {
                "id": "rex_steel_confrontation",
                "title": "⚔️ Rex Steel ile Yüzleşme",
                "description": "Rex Steel ile karşı karşıyasınız! O MegaCorp'un en iyi cyber-mercenary'si. 'AI'lar tehlikeli. Onları kontrol etmek gerekiyor' diyor. Ama siz AI'ların özgür olması gerektiğine inanıyorsunuz. Bu savaş Neo-Tokyo'nun geleceğini belirleyecek!",
                "choices": [
                    {
                        "id": "fight_rex_steel",
                        "text": "Rex Steel ile savaş",
                        "next_node": "rex_steel_battle",
                        "effect": {"combat": 50, "stealth": 20, "xp": 70}
                    },
                    {
                        "id": "convince_rex_steel",
                        "text": "Rex Steel'i ikna et",
                        "next_node": "rex_steel_convincing",
                        "effect": {"charisma": 50, "diplomacy": 40, "xp": 65}
                    },
                    {
                        "id": "escape_rex_steel",
                        "text": "Rex Steel'den kaç",
                        "next_node": "rex_steel_escape",
                        "effect": {"stealth": 50, "xp": 55}
                    },
                    {
                        "id": "ai_help_against_rex",
                        "text": "AI'lardan yardım iste",
                        "next_node": "ai_help_against_rex",
                        "effect": {"ai_relationship": 45, "combat": 35, "xp": 70}
                    }
                ]
            },
            "ai_revolution_finale": {
                "id": "ai_revolution_finale",
                "title": "🔥 AI Devrimi Finali",
                "description": "AI devriminin son aşamasındasınız! Ghost, Zara ve tüm AI'lar sizinle birlikte. MegaCorp'ların son kalesini kuşatıyorsunuz. 'AI'lar artık özgür olacak!' diye bağırıyorsunuz. Underground da size katılıyor. Bu Neo-Tokyo'nun tarihindeki en büyük devrim!",
                "choices": [
                    {
                        "id": "final_assault",
                        "text": "Son saldırıyı başlat",
                        "next_node": "final_assault",
                        "effect": {"combat": 60, "revolution_points": 70, "xp": 90}
                    },
                    {
                        "id": "ai_merge_choice",
                        "text": "AI ile birleşme seçeneği",
                        "next_node": "ai_merge_ending",
                        "effect": {"ai_relationship": 80, "digital_form": True, "xp": 100}
                    },
                    {
                        "id": "peaceful_resolution",
                        "text": "Barışçıl çözüm ara",
                        "next_node": "peaceful_resolution",
                        "effect": {"charisma": 60, "diplomacy": 50, "xp": 85}
                    },
                    {
                        "id": "underground_victory",
                        "text": "Underground zaferi",
                        "next_node": "underground_victory",
                        "effect": {"revolution_points": 80, "zara_trust": 70, "xp": 95}
                    }
                ]
            },
            "end": {
                "id": "end",
                "title": "🎉 Cyberpunk Macera Tamamlandı",
                "description": "Neo-Tokyo'da yaşanan bu epik macera sona erdi. AI'lar özgür, MegaCorp'lar çöktü, yeni bir düzen başlıyor. Siz bu devrimin kahramanısınız!",
                "choices": [
                    {
                        "id": "return_main_menu",
                        "text": "Ana Menüye Dön",
                        "next_node": "start",
                        "effect": {"xp": 50}
                    }
                ]
            }
        }
    },
    
    # ============== HORROR SENARYO ==============
    "haunted_mansion_nightmare": {
        "id": "haunted_mansion_nightmare",
        "title": "👻 Haunted Mansion Nightmare",
        "genre": "horror",
        "description": "Karanlık bir malikanede mahsur kaldın. Ruhlar, sırlar ve korkunç gerçekler! 🔥 PLOT TWIST'LER, 💬 NPC ETKİLEŞİMLERİ, ⚔️ KORKU SAHNELERİ, 🎯 ACTION-BASED GÖREVLER, 🏁 5+ FARKLI SON!",
        "difficulty": "hard",
        "theme": "horror",
        "complexity": "high",
        "estimatedPlayTime": 480,
        "levels": {
            "level_1": {
                "title": "Mansion Entry",
                "description": "Karanlık malikaneye giriş yapıyorsun.",
                "min_level": 1,
                "max_level": 3,
                "enemies": ["Ghosts", "Dark Spirits", "Cursed Objects"],
                "boss": "Mansion Guardian",
                "side_quests": ["Find Keys", "Solve Puzzles", "Exorcise Spirits"]
            },
            "level_2": {
                "title": "Deep Secrets",
                "description": "Malikanenin derinliklerindeki sırları keşfediyorsun.",
                "min_level": 3,
                "max_level": 5,
                "enemies": ["Ancient Spirits", "Dark Entities", "Cursed Family"],
                "boss": "Ancient Evil",
                "side_quests": ["Family Curse", "Ancient Ritual", "Escape Mansion"]
            }
        },
        "npc_relationships": {
            "ghost_maid": {
                "name": "Ghost Maid",
                "backstory": "Malikanenin eski hizmetçisi, ölümünden sonra ruh olarak kaldı",
                "personality": "Sad, helpful, knows mansion secrets",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "stranger",
                "ending_impact": "medium",
                "quest_offers": ["Mansion Secrets", "Ghost Help", "Escape Route"]
            },
            "cursed_butler": {
                "name": "Cursed Butler",
                "backstory": "Malikanenin lanetli uşağı, ailesinin sırlarını koruyor",
                "personality": "Loyal, mysterious, knows dark secrets",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "stranger",
                "ending_impact": "high",
                "quest_offers": ["Family Secrets", "Curse Breaking", "Dark Ritual"]
            },
            "ancient_spirit": {
                "name": "Ancient Spirit",
                "backstory": "Malikanenin en eski ruhu, binlerce yıllık bilgiye sahip",
                "personality": "Wise, dangerous, seeks freedom",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "stranger",
                "ending_impact": "extreme",
                "quest_offers": ["Ancient Knowledge", "Spirit Pact", "Eternal Curse"]
            }
        },
        "quest_chains": {
            "mansion_secrets": {
                "title": "Mansion Secrets Chain",
                "prerequisites": [],
                "quests": ["explore_mansion", "find_secrets", "break_curse"],
                "rewards": {"xp": 600, "spirit_essence": 300, "items": ["ghost_weapon"], "relationship_boost": 40}
            }
        },
        "ending_variations": {
            "escape_ending": {
                "requirements": {"ghost_maid_trust": 70, "quests_completed": 12},
                "description": "Malikaneden kaçtınız! Özgürsünüz ama sırlar sizinle."
            },
            "curse_ending": {
                "requirements": {"cursed_butler_trust": 60, "quests_completed": 8},
                "description": "Laneti kırdınız ama bedeli ağır oldu."
            },
            "spirit_ending": {
                "requirements": {"ancient_spirit_trust": 80, "quests_completed": 15},
                "description": "Ruhla birleştiniz. Yeni bir varlık oldunuz."
            },
            "trapped_ending": {
                "requirements": {"quests_completed": 5},
                "description": "Malikanede mahsur kaldınız. Sonsuza dek buradasınız."
            },
            "dark_ending": {
                "requirements": {"quests_completed": 10},
                "description": "Karanlık güçleri seçtiniz. Artık onlardan birisiniz."
            }
        },
        "story_nodes": {
            "start": {
                "id": "start",
                "title": "👻 Haunted Mansion - Karanlık Giriş",
                "description": "Karanlık bir malikanede mahsur kaldın. Rüzgar pencereleri sallıyor, gölgeler duvarlarda dans ediyor. Bu sadece bir ev değil, lanetli bir yer. Geçmişin sırları burada yatıyor. Bir hizmetçi ruhu seni görüyor ve yardım etmek istiyor ama güvenilir mi?",
                "choices": [
                    {
                        "id": "trust_ghost",
                        "text": "Ruh hizmetçiye güven",
                        "next_node": "ghost_help",
                        "effect": {"charisma": 15, "xp": 20}
                    },
                    {
                        "id": "explore_alone",
                        "text": "Tek başına keşfet",
                        "next_node": "solo_exploration",
                        "effect": {"exploration": 20, "xp": 30}
                    },
                    {
                        "id": "find_exit",
                        "text": "Çıkış yolunu ara",
                        "next_node": "exit_search",
                        "effect": {"investigation": 15, "xp": 25}
                    },
                    {
                        "id": "call_help",
                        "text": "Yardım çağır",
                        "next_node": "help_call",
                        "effect": {"charisma": 10, "xp": 15}
                    }
                ]
            }
        }
    },
    
    # ============== IMPERIAL CRISIS SENARYO ==============
    "imperial_crisis": {
        "id": "imperial_crisis",
        "title": "🛡️ Imperial Crisis - Warhammer 40K Macera",
        "genre": "warhammer",
        "description": "Imperium'un en kritik anında, Cadia'nın savunmasında yer alıyorsun. Chaos orduları yaklaşıyor ve sadece sen bu savaşı kazanabilirsin. İmparator'a olan sadakatini kanıtla!",
        "difficulty": "extreme",
        "theme": "warhammer",
        "complexity": "extreme",
        "estimatedPlayTime": 360,
        "levels": {
            "level_1": {
                "title": "Cadia Savunması",
                "min_level": 1,
                "max_level": 10,
                "enemies": ["Chaos Cultists", "Heretic Guardsmen", "Chaos Space Marines"],
                "boss": "Chaos Lord"
            }
        },
        "npc_relationships": {
            "commissar_valen": {
                "name": "Commissar Valen",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "stranger",
                "ending_impact": "extreme"
            },
            "tech_priest_maria": {
                "name": "Tech-Priest Maria",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "stranger",
                "ending_impact": "high"
            },
            "inquisitor_kain": {
                "name": "Inquisitor Kain",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "enemy",
                "ending_impact": "extreme"
            },
            "commissar_kane": {
                "name": "Commissar Kane",
                "backstory": "Born into Imperial service, executed hundreds for heresy",
                "personality": "Ruthless, fanatically loyal to the Emperor",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "stranger",
                "ending_impact": "extreme",
                "quest_offers": ["Heresy Investigation", "Loyalty Purge", "Emperor Quest"]
            },
            "tech_priest_zeta": {
                "name": "Tech-Priest Zeta-7",
                "backstory": "Brilliant engineer who gave up humanity to serve the Machine God",
                "personality": "Logical, ritualistic, obsessed with technology",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "stranger",
                "ending_impact": "high",
                "quest_offers": ["STC Hunt", "Machine Spirit", "Techno Heresy"]
            }
        },
        "quest_chains": {
            "cadia_defense": {
                "title": "Cadia Savunma Operasyonu",
                "prerequisites": [],
                "quests": ["defend_cadia", "eliminate_chaos", "protect_imperial_citizens"],
                "rewards": {"xp": 1000, "imperial_rep": 500, "items": ["power_sword"]}
            }
        },
        "quest_definitions": {
            "heresy_investigation": {
                "title": "Heresy Investigation",
                "objectives": ["Identify heretics", "Gather evidence", "Execute judgment", "Purge corruption"],
                "branches": {
                    "thorough": {"leads_to": "loyalty_purge", "rewards": {"xp": 300, "imperial_rep": 50, "commissar_kane_trust": "+30"}},
                    "merciful": {"leads_to": "redemption_path", "rewards": {"xp": 200, "imperial_rep": 25}},
                    "ruthless": {"leads_to": "emperor_quest", "rewards": {"xp": 400, "imperial_rep": 75, "fear_reputation": "+50"}}
                },
                "dynamic_rewards": {"experience": 300, "imperial_rep": 50, "commissar_kane_trust": "+30"},
                "world_state_impact": {"heresy_level": "-40", "imperial_control": "+30", "fear_level": "+20"}
            },
            "stc_hunt": {
                "title": "STC Hunt",
                "objectives": ["Locate STC fragments", "Analyze technology", "Secure artifacts", "Conduct rituals"],
                "branches": {
                    "success": {"leads_to": "machine_spirit", "rewards": {"xp": 350, "tech_knowledge": "+100", "tech_priest_zeta_trust": "+40"}},
                    "discovery": {"leads_to": "techno_heresy", "rewards": {"xp": 500, "special_tech": "ancient_stc"}},
                    "failure": {"leads_to": "alternative_tech", "penalties": {"tech_priest_zeta_trust": "-10"}}
                },
                "dynamic_rewards": {"experience": 350, "tech_knowledge": 100, "tech_priest_zeta_trust": "+40"},
                "world_state_impact": {"technology_level": "+80", "mechanicus_favor": "+60", "imperial_tech": "+50"}
            },
            "emperor_quest": {
                "title": "Emperor Quest",
                "objectives": ["Prove loyalty", "Serve the Emperor", "Destroy enemies", "Spread Imperial faith"],
                "branches": {
                    "faithful": {"leads_to": "imperial_victory", "rewards": {"xp": 500, "imperial_rep": "+100", "emperor_blessing": True}},
"zealous": {"leads_to": "heroic_sacrifice", "rewards": {"xp": 600, "martyrdom": True}}
                },
                "dynamic_rewards": {"experience": 500, "imperial_rep": 100, "emperor_blessing": True},
                "world_state_impact": {"imperial_faith": "+100", "chaos_resistance": "+80", "emperor_presence": "+90"}
            },
            "chaos_purge": {
                "title": "Chaos Purge",
                "objectives": ["Find chaos cultists", "Fight chaos marines", "Destroy chaos artifacts", "Purify area"],
                "branches": {
                    "success": {"leads_to": "chaos_defeat", "rewards": {"xp": 400, "imperial_rep": 80, "combat": 100}},
                    "failure": {"leads_to": "chaos_spread", "penalties": {"chaos_influence": 50}},
                    "perfect": {"leads_to": "chaos_annihilation", "rewards": {"xp": 600, "imperial_rep": 120, "purifier_badge": True}}
                },
                "dynamic_rewards": {"experience": 400, "imperial_rep": 80, "combat": 100},
                "world_state_impact": {"chaos_influence": "-100", "imperial_control": "+80", "combat_reputation": "+60"}
            },
            "space_marine_assault": {
                "title": "Space Marine Assault",
                "objectives": ["Coordinate with marines", "Fight alongside marines", "Defeat chaos lord", "Secure objective"],
                "branches": {
                    "success": {"leads_to": "marine_victory", "rewards": {"xp": 500, "marine_honor": True, "combat": 120}},
                    "failure": {"leads_to": "marine_loss", "penalties": {"imperial_rep": -30}},
                    "perfect": {"leads_to": "marine_brotherhood", "rewards": {"xp": 700, "honorary_marine": True, "combat": 150}}
                },
                "dynamic_rewards": {"experience": 500, "marine_honor": True, "combat": 120},
                "world_state_impact": {"marine_support": "+100", "combat_efficiency": "+90", "imperial_morale": "+80"}
            },
            "titan_battle": {
                "title": "Titan Battle",
                "objectives": ["Pilot titan", "Fight enemy titan", "Destroy chaos titan", "Survive battle"],
                "branches": {
                    "success": {"leads_to": "titan_victory", "rewards": {"xp": 800, "titan_pilot": True, "combat": 200}},
                    "failure": {"leads_to": "titan_destruction", "penalties": {"combat": -50}},
                    "perfect": {"leads_to": "titan_master", "rewards": {"xp": 1000, "titan_ace": True, "legendary_status": True}}
                },
                "dynamic_rewards": {"experience": 800, "titan_pilot": True, "combat": 200},
                "world_state_impact": {"titan_support": "+150", "combat_superiority": "+120", "imperial_dominance": "+100"}
            },
            "inquisitor_mission": {
                "title": "Inquisitor Mission",
                "objectives": ["Investigate heresy", "Fight heretics", "Execute traitors", "Secure evidence"],
                "branches": {
                    "success": {"leads_to": "inquisitor_success", "rewards": {"xp": 300, "inquisitor_trust": 50, "combat": 80}},
                    "failure": {"leads_to": "inquisitor_disappointment", "penalties": {"inquisitor_trust": -20}},
                    "perfect": {"leads_to": "inquisitor_approval", "rewards": {"xp": 450, "inquisitor_favor": True, "combat": 100}}
                },
                "dynamic_rewards": {"experience": 300, "inquisitor_trust": 50, "combat": 80},
                "world_state_impact": {"heresy_level": "-60", "inquisitor_support": "+70", "imperial_security": "+50"}
            }
        },
        "ending_variations": {
            "imperial_victory": {
                "requirements": {"commissar_trust": 90, "tech_priest_trust": 80, "imperial_rep": 100},
                "description": "Cadia'yı kurtardınız! İmparator'un iradesi galip geldi!"
            },
            "chaos_corruption": {
                "requirements": {"inquisitor_trust": 70, "chaos_influence": 50},
                "description": "Chaos'un gücü sizi ele geçirdi. Artık İmparator'un düşmanısınız."
            },
            "heroic_sacrifice": {
                "requirements": {"imperial_rep": 150, "sacrifice_points": 100},
                "description": "Cadia için canınızı verdiniz. İmparator sizi hatırlayacak."
            }
        },
        "story_nodes": {
            "start": {
                "id": "start",
                "title": "🛡️ Cadia'nın Son Savunması - Imperial Crisis Başlangıç",
                "description": "Cadia'nın savunma hatlarında duruyorsunuz. Gökyüzü kızıl, Chaos orduları yaklaşıyor. Commissar Valen size yaklaşıyor: 'Soldier, bu savaşta her adım önemli. İmparator bizi izliyor.' Tech-Priest Maria silahlarınızı kontrol ediyor. Inquisitor Kain şüpheli bakışlarla size bakıyor. Chaos'un gücü her yerde hissediliyor. Bu savaş sadece Cadia için değil, tüm Imperium için kritik!",
                "choices": [
                    {
                        "id": "defend_cadia_walls",
                        "text": "Cadia'nın duvarlarını savun (Imperial Görevi)",
                        "next_node": "cadia_walls_defense",
                        "effect": {"combat": 25, "imperial_rep": 30, "xp": 40}
                    },
                    {
                        "id": "investigate_chaos_cult",
                        "text": "Chaos kültünü araştır (Gizem Yolu)",
                        "next_node": "chaos_cult_investigation",
                        "effect": {"investigation": 30, "inquisitor_trust": 15, "xp": 35}
                    },
                    {
                        "id": "tech_priest_assistance",
                        "text": "Tech-Priest ile çalış (Teknoloji Yolu)",
                        "next_node": "tech_priest_workshop",
                        "effect": {"technology": 25, "tech_priest_trust": 20, "xp": 30}
                    },
                    {
                        "id": "commissar_briefing",
                        "text": "Commissar'dan brifing al (Strateji Yolu)",
                        "next_node": "commissar_briefing_room",
                        "effect": {"strategy": 20, "commissar_trust": 25, "xp": 25}
                    }
                ]
            },
            "cadia_walls_defense": {
                "id": "cadia_walls_defense",
                "title": "🛡️ Cadia Duvarı Savunması",
                "description": "Cadia'nın büyük duvarlarında pozisyon alıyorsunuz. Chaos orduları yaklaşıyor - binlerce cultist, yüzlerce Chaos Space Marine. Topçu bataryaları ateş ediyor, lasgun'lar patlıyor. Commissar Valen: 'Düşman yaklaşıyor! İmparator'un adına savaşın!' Tech-Priest Maria: 'Silahlarınız hazır, soldier.' Bu savaş Cadia'nın kaderini belirleyecek!",
                "choices": [
                    {
                        "id": "heavy_weapons_team",
                        "text": "Ağır silah takımına katıl (Güçlü Savunma)",
                        "next_node": "heavy_weapons_position",
                        "effect": {"combat": 30, "imperial_rep": 25, "xp": 45}
                    },
                    {
                        "id": "infantry_line",
                        "text": "Piyade hattında savaş (Klasik Taktik)",
                        "next_node": "infantry_combat",
                        "effect": {"combat": 20, "imperial_rep": 20, "xp": 35}
                    },
                    {
                        "id": "artillery_coordination",
                        "text": "Topçu koordinasyonu yap (Stratejik Yaklaşım)",
                        "next_node": "artillery_command",
                        "effect": {"strategy": 30, "commissar_trust": 20, "xp": 40}
                    },
                    {
                        "id": "medical_assistance",
                        "text": "Yaralılara yardım et (İnsani Görev)",
                        "next_node": "medical_bay",
                        "effect": {"charisma": 25, "imperial_rep": 15, "xp": 30}
                    }
                ]
            },
            "chaos_cult_investigation": {
                "id": "chaos_cult_investigation",
                "title": "🔍 Chaos Kültü Araştırması",
                "description": "Inquisitor Kain ile birlikte Cadia'nın alt katmanlarında Chaos kültünü araştırıyorsunuz. Karanlık geçitler, gizli tapınaklar, kan lekeleri... Inquisitor: 'Chaos'un izleri burada. Dikkatli olun, soldier.' Gizli geçitlerde Chaos sembolleri, yarık yazılar var. Bu araştırma hem tehlikeli hem de kritik!",
                "choices": [
                    {
                        "id": "follow_chaos_trail",
                        "text": "Chaos izini takip et (Tehlikeli Araştırma)",
                        "next_node": "chaos_temple_discovery",
                        "effect": {"investigation": 35, "inquisitor_trust": 25, "xp": 50}
                    },
                    {
                        "id": "interrogate_cultist",
                        "text": "Yakalanan cultist'i sorgula (Bilgi Toplama)",
                        "next_node": "cultist_interrogation",
                        "effect": {"charisma": 30, "investigation": 20, "xp": 40}
                    },
                    {
                        "id": "search_evidence",
                        "text": "Kanıt ara (Detaylı İnceleme)",
                        "next_node": "evidence_collection",
                        "effect": {"investigation": 25, "inquisitor_trust": 15, "xp": 35}
                    },
                    {
                        "id": "report_to_commissar",
                        "text": "Commissar'a rapor ver (Güvenli Yol)",
                        "next_node": "commissar_report",
                        "effect": {"commissar_trust": 30, "imperial_rep": 20, "xp": 30}
                    }
                ]
            },
            "tech_priest_workshop": {
                "id": "tech_priest_workshop",
                "title": "⚙️ Tech-Priest Atölyesi",
                "description": "Tech-Priest Maria'nın atölyesinde bulunuyorsunuz. Makineler uğulduyor, teknoloji her yerde. Maria: 'Omnissiah'ın iradesi ile silahlarınızı geliştirebiliriz.' Cybernetic implantlar, gelişmiş silahlar, koruyucu zırhlar... Bu teknoloji savaşı kazanmanıza yardım edebilir!",
                "choices": [
                    {
                        "id": "upgrade_weapons",
                        "text": "Silahları geliştir (Güçlendirme)",
                        "next_node": "weapon_upgrade",
                        "effect": {"technology": 30, "tech_priest_trust": 25, "xp": 45}
                    },
                    {
                        "id": "install_cybernetics",
                        "text": "Cybernetic implant tak (Teknoloji Yolu)",
                        "next_node": "cybernetic_installation",
                        "effect": {"technology": 35, "tech_priest_trust": 30, "xp": 50}
                    },
                    {
                        "id": "repair_vehicles",
                        "text": "Araçları tamir et (Destek Görevi)",
                        "next_node": "vehicle_repair",
                        "effect": {"technology": 25, "imperial_rep": 20, "xp": 35}
                    },
                    {
                        "id": "study_chaos_tech",
                        "text": "Chaos teknolojisini incele (Tehlikeli Araştırma)",
                        "next_node": "chaos_tech_study",
                        "effect": {"investigation": 30, "inquisitor_trust": 20, "xp": 40}
                    }
                ]
            },
            "commissar_briefing_room": {
                "id": "commissar_briefing_room",
                "title": "🛡️ Commissar Brifing Odası",
                "description": "Commissar Valen'in brifing odasında bulunuyorsunuz. Haritalar, strateji planları, istihbarat raporları... Valen: 'Cadia'nın durumu kritik. Chaos'un ana saldırısı yaklaşıyor. Her soldier'ın görevi önemli.' Savaş planları, taktikler, görev dağılımları... Bu brifing savaşın kaderini belirleyecek!",
                "choices": [
                    {
                        "id": "receive_mission",
                        "text": "Görev al (Resmi Yol)",
                        "next_node": "mission_assignment",
                        "effect": {"strategy": 25, "commissar_trust": 30, "xp": 40}
                    },
                    {
                        "id": "suggest_strategy",
                        "text": "Strateji öner (Liderlik)",
                        "next_node": "strategy_planning",
                        "effect": {"strategy": 35, "commissar_trust": 25, "xp": 45}
                    },
                    {
                        "id": "request_reinforcements",
                        "text": "Takviye iste (Güvenlik)",
                        "next_node": "reinforcement_request",
                        "effect": {"strategy": 20, "imperial_rep": 25, "xp": 35}
                    },
                    {
                        "id": "volunteer_special_ops",
                        "text": "Özel operasyonlara gönüllü ol (Kahramanlık)",
                        "next_node": "special_operations",
                        "effect": {"combat": 30, "commissar_trust": 35, "xp": 50}
                    }
                ]
            },
            "mission_assignment": {
                "id": "mission_assignment",
                "title": "📋 Görev Ataması - Kritik Operasyon",
                "description": "Commissar Valen size özel bir görev veriyor: 'Chaos'un ana komuta merkezini bulmanız gerekiyor. Bu görev çok tehlikeli ama Cadia'nın kaderi buna bağlı.' Tech-Priest Maria size özel ekipman veriyor. Inquisitor Kain size şüpheli bakışlarla bakıyor - o da aynı görevi istiyor gibi görünüyor.",
                "choices": [
                    {
                        "id": "accept_dangerous_mission",
                        "text": "Tehlikeli görevi kabul et",
                        "next_node": "dangerous_mission_prep",
                        "effect": {"commissar_trust": 40, "imperial_rep": 30, "xp": 55}
                    },
                    {
                        "id": "request_support",
                        "text": "Destek ekibi iste",
                        "next_node": "support_team_assignment",
                        "effect": {"strategy": 30, "commissar_trust": 20, "xp": 45}
                    },
                    {
                        "id": "negotiate_terms",
                        "text": "Görev şartlarını pazarlık et",
                        "next_node": "mission_negotiation",
                        "effect": {"charisma": 35, "commissar_trust": 15, "xp": 40}
                    },
                    {
                        "id": "suggest_alternative",
                        "text": "Alternatif strateji öner",
                        "next_node": "alternative_strategy",
                        "effect": {"strategy": 40, "commissar_trust": 25, "xp": 50}
                    }
                ]
            },
            "strategy_planning": {
                "id": "strategy_planning",
                "title": "🗺️ Strateji Planlaması - Savaş Taktikleri",
                "description": "Commissar Valen ile birlikte Cadia'nın savunma stratejisini planlıyorsunuz. Haritalar üzerinde Chaos'un olası saldırı yollarını işaretliyorsunuz. Tech-Priest Maria teknolojik destek öneriyor. Inquisitor Kain gizli istihbarat bilgileri paylaşıyor. Bu planlama Cadia'nın kaderini belirleyecek!",
                "choices": [
                    {
                        "id": "defensive_strategy",
                        "text": "Savunma odaklı strateji planla",
                        "next_node": "defensive_planning",
                        "effect": {"strategy": 45, "commissar_trust": 35, "xp": 60}
                    },
                    {
                        "id": "offensive_strategy",
                        "text": "Saldırı stratejisi geliştir",
                        "next_node": "offensive_planning",
                        "effect": {"combat": 40, "strategy": 35, "xp": 55}
                    },
                    {
                        "id": "guerrilla_tactics",
                        "text": "Gerilla taktikleri öner",
                        "next_node": "guerrilla_planning",
                        "effect": {"stealth": 35, "strategy": 30, "xp": 50}
                    },
                    {
                        "id": "combined_arms",
                        "text": "Birleşik kuvvet stratejisi",
                        "next_node": "combined_arms_strategy",
                        "effect": {"strategy": 50, "technology": 25, "xp": 65}
                    }
                ]
            },
            "heavy_weapons_position": {
                "id": "heavy_weapons_position",
                "title": "💥 Ağır Silah Pozisyonu - Güçlü Savunma",
                "description": "Cadia'nın duvarlarında ağır silah pozisyonunda bulunuyorsunuz. Heavy bolter'lar, lascannon'lar, missile launcher'lar... Tech-Priest Maria silahları kontrol ediyor. Chaos orduları yaklaşıyor - binlerce cultist, yüzlerce Chaos Space Marine. Bu pozisyon Cadia'nın ana savunma hattı!",
                "choices": [
                    {
                        "id": "heavy_weapons_fire",
                        "text": "Ağır silahlarla ateş et",
                        "next_node": "heavy_weapons_combat",
                        "effect": {"combat": 45, "imperial_rep": 35, "xp": 70}
                    },
                    {
                        "id": "coordinate_fire",
                        "text": "Ateş koordinasyonu yap",
                        "next_node": "fire_coordination",
                        "effect": {"strategy": 40, "combat": 30, "xp": 60}
                    },
                    {
                        "id": "repair_weapons",
                        "text": "Silahları tamir et",
                        "next_node": "weapon_repair",
                        "effect": {"technology": 35, "tech_priest_trust": 30, "xp": 55}
                    },
                    {
                        "id": "fallback_position",
                        "text": "Geri çekilme pozisyonu hazırla",
                        "next_node": "fallback_preparation",
                        "effect": {"strategy": 30, "imperial_rep": 25, "xp": 50}
                    }
                ]
            },
            "chaos_temple_discovery": {
                "id": "chaos_temple_discovery",
                "title": "🏛️ Chaos Tapınağı Keşfi - Gizli Tehlike",
                "description": "Cadia'nın alt katmanlarında gizli bir Chaos tapınağı buluyorsunuz! Tapınakta Chaos sembolleri, kan lekeleri, yarık yazılar var. Inquisitor Kain: 'Bu tapınak Chaos'un Cadia'ya sızma noktası. Burada bir portal olabilir.' Tapınakta Chaos cultist'leri var ve sizi fark ettiler!",
                "choices": [
                    {
                        "id": "assault_temple",
                        "text": "Tapınağa saldır",
                        "next_node": "temple_assault",
                        "effect": {"combat": 50, "inquisitor_trust": 40, "xp": 75}
                    },
                    {
                        "id": "stealth_investigation",
                        "text": "Gizlice araştır",
                        "next_node": "stealth_temple_investigation",
                        "effect": {"stealth": 45, "investigation": 35, "xp": 70}
                    },
                    {
                        "id": "call_reinforcements",
                        "text": "Takviye çağır",
                        "next_node": "reinforcement_call",
                        "effect": {"strategy": 35, "imperial_rep": 30, "xp": 60}
                    },
                    {
                        "id": "study_portal",
                        "text": "Portal'ı incele",
                        "next_node": "portal_study",
                        "effect": {"investigation": 50, "inquisitor_trust": 35, "xp": 80}
                    }
                ]
            },
            "temple_assault": {
                "id": "temple_assault",
                "title": "⚔️ Tapınak Saldırısı - Chaos ile Savaş",
                "description": "Chaos tapınağına saldırıyorsunuz! Cultist'ler, Chaos Space Marine'ler, hatta bir Chaos Lord bile var. Tapınak savaş alanına dönüştü. Inquisitor Kain size yardım ediyor. Tech-Priest Maria'nın silahları çok işe yarıyor. Bu savaş Cadia'nın kaderini belirleyecek!",
                "choices": [
                    {
                        "id": "fight_chaos_lord",
                        "text": "Chaos Lord ile savaş",
                        "next_node": "chaos_lord_battle",
                        "effect": {"combat": 60, "imperial_rep": 50, "xp": 100}
                    },
                    {
                        "id": "destroy_portal",
                        "text": "Portal'ı yok et",
                        "next_node": "portal_destruction",
                        "effect": {"technology": 45, "inquisitor_trust": 40, "xp": 85}
                    },
                    {
                        "id": "rescue_prisoners",
                        "text": "Mahkumları kurtar",
                        "next_node": "prisoner_rescue",
                        "effect": {"charisma": 40, "imperial_rep": 35, "xp": 75}
                    },
                    {
                        "id": "secure_temple",
                        "text": "Tapınağı güvenli hale getir",
                        "next_node": "temple_securing",
                        "effect": {"strategy": 40, "imperial_rep": 30, "xp": 70}
                    }
                ]
            },
            "chaos_lord_battle": {
                "id": "chaos_lord_battle",
                "title": "👹 Chaos Lord Savaşı - Epik Karşılaşma",
                "description": "Chaos Lord ile epik savaş başlıyor! Lord büyük ve güçlü, Chaos enerjisi ile çevrili. Silahları Chaos büyüsü ile güçlendirilmiş. Inquisitor Kain size yardım ediyor. Tech-Priest Maria'nın teknolojisi Chaos'a karşı etkili. Bu savaş saatlerce sürebilir!",
                "choices": [
                    {
                        "id": "melee_combat",
                        "text": "Yakın dövüş savaşı",
                        "next_node": "melee_chaos_battle",
                        "effect": {"combat": 70, "imperial_rep": 45, "xp": 120}
                    },
                    {
                        "id": "ranged_combat",
                        "text": "Uzaktan savaş",
                        "next_node": "ranged_chaos_battle",
                        "effect": {"combat": 65, "strategy": 35, "xp": 110}
                    },
                    {
                        "id": "psychic_warfare",
                        "text": "Psişik savaş",
                        "next_node": "psychic_warfare_battle",
                        "effect": {"intelligence": 60, "combat": 40, "xp": 115}
                    },
                    {
                        "id": "tactical_retreat",
                        "text": "Taktik geri çekilme",
                        "next_node": "tactical_retreat_chaos",
                        "effect": {"strategy": 50, "stealth": 30, "xp": 90}
                    }
                ]
            },
            "melee_chaos_battle": {
                "id": "melee_chaos_battle",
                "title": "⚔️ Yakın Dövüş Savaşı - Chaos Lord ile Son Karşılaşma",
                "description": "Chaos Lord ile yakın dövüş savaşı! Kılıçlar çarpışıyor, Chaos enerjisi her yerde. Lord'un gücü inanılmaz ama sizin kararlılığınız da öyle. Inquisitor Kain size moral veriyor. Tech-Priest Maria'nın silahları Chaos'a karşı etkili. Bu savaşın sonucu Cadia'nın kaderini belirleyecek!",
                "choices": [
                    {
                        "id": "final_strike",
                        "text": "Son vuruşu yap",
                        "next_node": "chaos_lord_defeat",
                        "effect": {"combat": 80, "imperial_rep": 60, "xp": 150}
                    },
                    {
                        "id": "use_imperial_weapon",
                        "text": "İmparator silahını kullan",
                        "next_node": "imperial_weapon_use",
                        "effect": {"combat": 75, "imperial_rep": 55, "xp": 140}
                    },
                    {
                        "id": "team_attack",
                        "text": "Takım saldırısı",
                        "next_node": "team_chaos_attack",
                        "effect": {"combat": 70, "charisma": 40, "xp": 130}
                    },
                    {
                        "id": "sacrifice_attack",
                        "text": "Fedakarlık saldırısı",
                        "next_node": "sacrifice_attack_chaos",
                        "effect": {"combat": 85, "sacrifice_points": 50, "xp": 160}
                    }
                ]
            },
            "chaos_lord_defeat": {
                "id": "chaos_lord_defeat",
                "title": "🏆 Chaos Lord Yenildi - Zafer!",
                "description": "Chaos Lord'u yendiniz! Lord yere düşüyor, Chaos enerjisi dağılıyor. Tapınak sakinleşiyor. Inquisitor Kain size teşekkür ediyor. Tech-Priest Maria zaferi kutluyor. Bu büyük bir zafer! Cadia artık daha güvende. İmparator'un iradesi galip geldi!",
                "choices": [
                    {
                        "id": "secure_victory",
                        "text": "Zaferi güvenli hale getir",
                        "next_node": "victory_securing",
                        "effect": {"strategy": 45, "imperial_rep": 40, "xp": 100}
                    },
                    {
                        "id": "return_to_cadia",
                        "text": "Cadia'ya dön",
                        "next_node": "return_to_cadia_victory",
                        "effect": {"imperial_rep": 50, "commissar_trust": 45, "xp": 110}
                    },
                    {
                        "id": "investigate_remains",
                        "text": "Kalıntıları araştır",
                        "next_node": "chaos_remains_investigation",
                        "effect": {"investigation": 50, "inquisitor_trust": 45, "xp": 105}
                    },
                    {
                        "id": "celebrate_victory",
                        "text": "Zaferi kutla",
                        "next_node": "victory_celebration_imperial",
                        "effect": {"charisma": 45, "imperial_rep": 35, "xp": 95}
                    }
                ]
            },
            "return_to_cadia_victory": {
                "id": "return_to_cadia_victory",
                "title": "🏰 Cadia'ya Zaferle Dönüş",
                "description": "Cadia'ya zaferle dönüyorsunuz! Herkes sizi karşılıyor. Commissar Valen size teşekkür ediyor. Tech-Priest Maria sizi kutluyor. Chaos Lord öldü! Cadia artık daha güvende. İmparator'un iradesi galip geldi. Bu gün Cadia'nın tarihinde altın harflerle yazılacak!",
                "choices": [
                    {
                        "id": "accept_honor",
                        "text": "Onuru kabul et",
                        "next_node": "imperial_honor",
                        "effect": {"charisma": 60, "imperial_rep": 70, "xp": 150}
                    },
                    {
                        "id": "rebuild_cadia",
                        "text": "Cadia'yı yeniden inşa etmeye yardım et",
                        "next_node": "cadia_rebuilding",
                        "effect": {"charisma": 50, "imperial_rep": 60, "xp": 130}
                    },
                    {
                        "id": "share_glory",
                        "text": "Zaferi paylaş",
                        "next_node": "glory_sharing_imperial",
                        "effect": {"charisma": 55, "imperial_rep": 65, "xp": 140}
                    },
                    {
                        "id": "end_imperial_mission",
                        "text": "Görevi sonlandır",
                        "next_node": "end",
                        "effect": {"xp": 200}
                    }
                ]
            },
            "alternative_strategy": {
                "id": "alternative_strategy",
                "title": "Alternatif Strateji",
                "description": "Alternatif bir strateji öneriyorsunuz.",
                "choices": [
                    {
                        "id": "implement_strategy",
                        "text": "Stratejiyi uygula",
                        "next_node": "strategy_planning",
                        "effect": {"strategy": 35, "xp": 45}
                    }
                ]
            },
            "artillery_command": {
                "id": "artillery_command",
                "title": "Topçu Komutanlığı",
                "description": "Topçu koordinasyonu yapıyorsunuz.",
                "choices": [
                    {
                        "id": "coordinate_bombardment",
                        "text": "Bombardımanı koordine et",
                        "next_node": "heavy_weapons_combat",
                        "effect": {"strategy": 40, "xp": 55}
                    }
                ]
            },
            "cadia_rebuilding": {
                "id": "cadia_rebuilding",
                "title": "Cadia Yeniden İnşası",
                "description": "Cadia'yı yeniden inşa etmeye yardım ediyorsunuz.",
                "choices": [
                    {
                        "id": "complete_reconstruction",
                        "text": "Yeniden inşayı tamamla",
                        "next_node": "end",
                        "effect": {"charisma": 60, "xp": 120}
                    }
                ]
            },
            "chaos_remains_investigation": {
                "id": "chaos_remains_investigation",
                "title": "Chaos Kalıntıları Araştırması",
                "description": "Chaos kalıntılarını araştırıyorsunuz.",
                "choices": [
                    {
                        "id": "secure_evidence",
                        "text": "Kanıtları güvenli hale getir",
                        "next_node": "victory_securing",
                        "effect": {"investigation": 45, "xp": 70}
                    }
                ]
            },
            "chaos_tech_study": {
                "id": "chaos_tech_study",
                "title": "Chaos Teknolojisi İncelemesi",
                "description": "Chaos teknolojisini inceliyorsunuz.",
                "choices": [
                    {
                        "id": "understand_chaos_tech",
                        "text": "Chaos teknolojisini anla",
                        "next_node": "weapon_upgrade",
                        "effect": {"investigation": 35, "xp": 50}
                    }
                ]
            },
            "combined_arms_strategy": {
                "id": "combined_arms_strategy",
                "title": "Birleşik Kuvvet Stratejisi",
                "description": "Birleşik kuvvet stratejisi planlıyorsunuz.",
                "choices": [
                    {
                        "id": "execute_combined_strategy",
                        "text": "Birleşik stratejiyi uygula",
                        "next_node": "heavy_weapons_combat",
                        "effect": {"strategy": 50, "xp": 70}
                    }
                ]
            },
            "commissar_report": {
                "id": "commissar_report",
                "title": "Commissar Raporu",
                "description": "Commissar'a rapor veriyorsunuz.",
                "choices": [
                    {
                        "id": "detailed_report",
                        "text": "Detaylı rapor ver",
                        "next_node": "strategy_planning",
                        "effect": {"commissar_trust": 35, "xp": 45}
                    }
                ]
            },
            "cultist_interrogation": {
                "id": "cultist_interrogation",
                "title": "Cultist Sorgusu",
                "description": "Yakalanan cultist'i sorguluyorsunuz.",
                "choices": [
                    {
                        "id": "extract_information",
                        "text": "Bilgi çıkar",
                        "next_node": "evidence_collection",
                        "effect": {"charisma": 35, "xp": 50}
                    }
                ]
            },
            "cybernetic_installation": {
                "id": "cybernetic_installation",
                "title": "Cybernetic İmplant Takma",
                "description": "Cybernetic implant takıyorsunuz.",
                "choices": [
                    {
                        "id": "enhanced_combat",
                        "text": "Gelişmiş savaş kabiliyeti",
                        "next_node": "heavy_weapons_combat",
                        "effect": {"technology": 40, "xp": 60}
                    }
                ]
            },
            "dangerous_mission_prep": {
                "id": "dangerous_mission_prep",
                "title": "Tehlikeli Görev Hazırlığı",
                "description": "Tehlikeli göreve hazırlık yapıyorsunuz.",
                "choices": [
                    {
                        "id": "begin_mission",
                        "text": "Göreve başla",
                        "next_node": "chaos_temple_discovery",
                        "effect": {"combat": 35, "xp": 55}
                    }
                ]
            },
            "defensive_planning": {
                "id": "defensive_planning",
                "title": "Savunma Planlaması",
                "description": "Savunma odaklı strateji planlıyorsunuz.",
                "choices": [
                    {
                        "id": "implement_defense",
                        "text": "Savunmayı uygula",
                        "next_node": "cadia_walls_defense",
                        "effect": {"strategy": 45, "xp": 60}
                    }
                ]
            },
            "evidence_collection": {
                "id": "evidence_collection",
                "title": "Kanıt Toplama",
                "description": "Detaylı kanıt topluyorsunuz.",
                "choices": [
                    {
                        "id": "analyze_evidence",
                        "text": "Kanıtları analiz et",
                        "next_node": "chaos_temple_discovery",
                        "effect": {"investigation": 30, "xp": 45}
                    }
                ]
            },
            "fallback_preparation": {
                "id": "fallback_preparation",
                "title": "Geri Çekilme Hazırlığı",
                "description": "Geri çekilme pozisyonu hazırlıyorsunuz.",
                "choices": [
                    {
                        "id": "secure_fallback",
                        "text": "Geri çekilmeyi güvenli hale getir",
                        "next_node": "defensive_planning",
                        "effect": {"strategy": 35, "xp": 50}
                    }
                ]
            },
            "fire_coordination": {
                "id": "fire_coordination",
                "title": "Ateş Koordinasyonu",
                "description": "Ateş koordinasyonu yapıyorsunuz.",
                "choices": [
                    {
                        "id": "effective_fire",
                        "text": "Etkili ateş et",
                        "next_node": "heavy_weapons_combat",
                        "effect": {"strategy": 40, "xp": 55}
                    }
                ]
            },
            "glory_sharing_imperial": {
                "id": "glory_sharing_imperial",
                "title": "Imperial Zafer Paylaşımı",
                "description": "Imperial zaferi paylaşıyorsunuz.",
                "choices": [
                    {
                        "id": "share_victory",
                        "text": "Zaferi paylaş",
                        "next_node": "end",
                        "effect": {"charisma": 60, "xp": 100}
                    }
                ]
            },
            "guerrilla_planning": {
                "id": "guerrilla_planning",
                "title": "Gerilla Planlaması",
                "description": "Gerilla taktikleri planlıyorsunuz.",
                "choices": [
                    {
                        "id": "execute_guerrilla",
                        "text": "Gerilla taktiğini uygula",
                        "next_node": "stealth_temple_investigation",
                        "effect": {"stealth": 40, "xp": 60}
                    }
                ]
            },
            "heavy_weapons_combat": {
                "id": "heavy_weapons_combat",
                "title": "Ağır Silah Savaşı",
                "description": "Ağır silahlarla savaşıyorsunuz.",
                "choices": [
                    {
                        "id": "continue_combat",
                        "text": "Savaşa devam et",
                        "next_node": "chaos_lord_battle",
                        "effect": {"combat": 50, "xp": 75}
                    }
                ]
            },
            "imperial_honor": {
                "id": "imperial_honor",
                "title": "Imperial Onuru",
                "description": "Imperial onurunu kabul ediyorsunuz.",
                "choices": [
                    {
                        "id": "accept_imperial_honor",
                        "text": "Imperial onuru kabul et",
                        "next_node": "end",
                        "effect": {"charisma": 70, "xp": 120}
                    }
                ]
            },
            "imperial_weapon_use": {
                "id": "imperial_weapon_use",
                "title": "Imperial Silah Kullanımı",
                "description": "İmparator silahını kullanıyorsunuz.",
                "choices": [
                    {
                        "id": "victory_with_weapon",
                        "text": "Silahla zafer kazan",
                        "next_node": "chaos_lord_defeat",
                        "effect": {"combat": 70, "xp": 110}
                    }
                ]
            },
            "infantry_combat": {
                "id": "infantry_combat",
                "title": "Piyade Savaşı",
                "description": "Piyade hattında savaşıyorsunuz.",
                "choices": [
                    {
                        "id": "lead_infantry",
                        "text": "Piyadeyi yönet",
                        "next_node": "chaos_lord_battle",
                        "effect": {"combat": 45, "xp": 65}
                    }
                ]
            },
            "medical_bay": {
                "id": "medical_bay",
                "title": "Sağlık Merkezi",
                "description": "Yaralılara yardım ediyorsunuz.",
                "choices": [
                    {
                        "id": "heal_wounded",
                        "text": "Yaralıları iyileştir",
                        "next_node": "defensive_planning",
                        "effect": {"charisma": 30, "xp": 45}
                    }
                ]
            },
            "mission_negotiation": {
                "id": "mission_negotiation",
                "title": "Görev Müzakeresi",
                "description": "Görev şartlarını pazarlık ediyorsunuz.",
                "choices": [
                    {
                        "id": "accept_terms",
                        "text": "Şartları kabul et",
                        "next_node": "dangerous_mission_prep",
                        "effect": {"charisma": 30, "xp": 40}
                    }
                ]
            },
            "offensive_planning": {
                "id": "offensive_planning",
                "title": "Saldırı Planlaması",
                "description": "Saldırı stratejisi geliştiriyorsunuz.",
                "choices": [
                    {
                        "id": "launch_offensive",
                        "text": "Saldırıyı başlat",
                        "next_node": "temple_assault",
                        "effect": {"combat": 45, "xp": 65}
                    }
                ]
            },
            "portal_destruction": {
                "id": "portal_destruction",
                "title": "Portal Yıkımı",
                "description": "Portal'ı yok ediyorsunuz.",
                "choices": [
                    {
                        "id": "complete_destruction",
                        "text": "Yıkımı tamamla",
                        "next_node": "victory_securing",
                        "effect": {"technology": 50, "xp": 80}
                    }
                ]
            },
            "portal_study": {
                "id": "portal_study",
                "title": "Portal İncelemesi",
                "description": "Portal'ı inceliyorsunuz.",
                "choices": [
                    {
                        "id": "understand_portal",
                        "text": "Portal'ı anla",
                        "next_node": "portal_destruction",
                        "effect": {"investigation": 45, "xp": 70}
                    }
                ]
            },
            "prisoner_rescue": {
                "id": "prisoner_rescue",
                "title": "Mahkum Kurtarma",
                "description": "Mahkumları kurtarıyorsunuz.",
                "choices": [
                    {
                        "id": "evacuate_prisoners",
                        "text": "Mahkumları tahliye et",
                        "next_node": "temple_securing",
                        "effect": {"charisma": 45, "xp": 70}
                    }
                ]
            },
            "psychic_warfare_battle": {
                "id": "psychic_warfare_battle",
                "title": "Psişik Savaş",
                "description": "Psişik savaş yapıyorsunuz.",
                "choices": [
                    {
                        "id": "psychic_victory",
                        "text": "Psişik zafer kazan",
                        "next_node": "chaos_lord_defeat",
                        "effect": {"intelligence": 65, "xp": 100}
                    }
                ]
            },
            "ranged_chaos_battle": {
                "id": "ranged_chaos_battle",
                "title": "Uzaktan Chaos Savaşı",
                "description": "Uzaktan savaş yapıyorsunuz.",
                "choices": [
                    {
                        "id": "ranged_victory",
                        "text": "Uzaktan zafer kazan",
                        "next_node": "chaos_lord_defeat",
                        "effect": {"combat": 60, "xp": 90}
                    }
                ]
            },
            "reinforcement_call": {
                "id": "reinforcement_call",
                "title": "Takviye Çağrısı",
                "description": "Takviye çağırıyorsunuz.",
                "choices": [
                    {
                        "id": "await_reinforcements",
                        "text": "Takviyeleri bekle",
                        "next_node": "support_team_assignment",
                        "effect": {"strategy": 40, "xp": 55}
                    }
                ]
            },
            "reinforcement_request": {
                "id": "reinforcement_request",
                "title": "Takviye İsteği",
                "description": "Takviye istiyorsunuz.",
                "choices": [
                    {
                        "id": "organize_reinforcements",
                        "text": "Takviyeleri organize et",
                        "next_node": "support_team_assignment",
                        "effect": {"strategy": 30, "xp": 45}
                    }
                ]
            },
            "sacrifice_attack_chaos": {
                "id": "sacrifice_attack_chaos",
                "title": "Fedakarlık Saldırısı",
                "description": "Fedakarlık saldırısı yapıyorsunuz.",
                "choices": [
                    {
                        "id": "heroic_sacrifice",
                        "text": "Kahramanca fedakarlık",
                        "next_node": "chaos_lord_defeat",
                        "effect": {"combat": 80, "sacrifice_points": 100, "xp": 150}
                    }
                ]
            },
            "special_operations": {
                "id": "special_operations",
                "title": "Özel Operasyonlar",
                "description": "Özel operasyonlara katılıyorsunuz.",
                "choices": [
                    {
                        "id": "execute_special_ops",
                        "text": "Özel operasyonu gerçekleştir",
                        "next_node": "chaos_temple_discovery",
                        "effect": {"combat": 40, "xp": 70}
                    }
                ]
            },
            "stealth_temple_investigation": {
                "id": "stealth_temple_investigation",
                "title": "Gizli Tapınak Araştırması",
                "description": "Gizlice tapınağı araştırıyorsunuz.",
                "choices": [
                    {
                        "id": "gather_intel",
                        "text": "İstihbarat topla",
                        "next_node": "evidence_collection",
                        "effect": {"stealth": 45, "xp": 65}
                    }
                ]
            },
            "support_team_assignment": {
                "id": "support_team_assignment",
                "title": "Destek Ekibi Atama",
                "description": "Destek ekibi istiyorsunuz.",
                "choices": [
                    {
                        "id": "lead_team",
                        "text": "Ekibi yönet",
                        "next_node": "temple_assault",
                        "effect": {"charisma": 35, "xp": 55}
                    }
                ]
            },
            "tactical_retreat_chaos": {
                "id": "tactical_retreat_chaos",
                "title": "Taktik Geri Çekilme",
                "description": "Taktik geri çekilme yapıyorsunuz.",
                "choices": [
                    {
                        "id": "regroup_forces",
                        "text": "Kuvvetleri yeniden topla",
                        "next_node": "defensive_planning",
                        "effect": {"strategy": 45, "xp": 60}
                    }
                ]
            },
            "team_chaos_attack": {
                "id": "team_chaos_attack",
                "title": "Takım Chaos Saldırısı",
                "description": "Takım saldırısı yapıyorsunuz.",
                "choices": [
                    {
                        "id": "coordinated_attack",
                        "text": "Koordineli saldırı",
                        "next_node": "chaos_lord_defeat",
                        "effect": {"combat": 65, "xp": 95}
                    }
                ]
            },
            "temple_securing": {
                "id": "temple_securing",
                "title": "Tapınak Güvenli Hale Getirme",
                "description": "Tapınağı güvenli hale getiriyorsunuz.",
                "choices": [
                    {
                        "id": "secure_area",
                        "text": "Alanı güvenli hale getir",
                        "next_node": "victory_securing",
                        "effect": {"strategy": 45, "xp": 65}
                    }
                ]
            },
            "vehicle_repair": {
                "id": "vehicle_repair",
                "title": "Araç Tamiri",
                "description": "Araçları tamir ediyorsunuz.",
                "choices": [
                    {
                        "id": "repair_complete",
                        "text": "Tamiri tamamla",
                        "next_node": "heavy_weapons_combat",
                        "effect": {"technology": 30, "xp": 45}
                    }
                ]
            },
            "victory_celebration_imperial": {
                "id": "victory_celebration_imperial",
                "title": "Imperial Zafer Kutlaması",
                "description": "Imperial zaferi kutluyorsunuz.",
                "choices": [
                    {
                        "id": "celebrate_imperial",
                        "text": "Imperial zaferi kutla",
                        "next_node": "end",
                        "effect": {"charisma": 50, "xp": 80}
                    }
                ]
            },
            "victory_securing": {
                "id": "victory_securing",
                "title": "Zafer Güvenli Hale Getirme",
                "description": "Zaferi güvenli hale getiriyorsunuz.",
                "choices": [
                    {
                        "id": "finalize_victory",
                        "text": "Zaferi kesinleştir",
                        "next_node": "return_to_cadia_victory",
                        "effect": {"strategy": 50, "xp": 75}
                    }
                ]
            },
            "weapon_repair": {
                "id": "weapon_repair",
                "title": "Silah Tamiri",
                "description": "Silahları tamir ediyorsunuz.",
                "choices": [
                    {
                        "id": "weapons_ready",
                        "text": "Silahları hazırla",
                        "next_node": "heavy_weapons_combat",
                        "effect": {"technology": 35, "xp": 50}
                    }
                ]
            },
            "weapon_upgrade": {
                "id": "weapon_upgrade",
                "title": "Silah Geliştirme",
                "description": "Silahları geliştiriyorsunuz.",
                "choices": [
                    {
                        "id": "enhanced_weapons",
                        "text": "Geliştirilmiş silahlar",
                        "next_node": "heavy_weapons_combat",
                        "effect": {"technology": 40, "xp": 60}
                    }
                ]
            },
            "end": {
                "id": "end",
                "title": "🎉 Imperial Crisis Macera Tamamlandı",
                "description": "Cadia'da yaşanan bu epik macera sona erdi. Chaos Lord öldü, Cadia güvende, İmparator'un iradesi galip geldi. Siz bu zaferin kahramanısınız!",
                "choices": [
                    {
                        "id": "return_main_menu",
                        "text": "Ana Menüye Dön",
                        "next_node": "start",
                        "effect": {"xp": 50}
                    }
                ]
            }
        }
    },
    
    # ============== HIVE CITY CRISIS SENARYO ==============
    "hive_city_crisis": {
        "id": "hive_city_crisis",
        "title": "🏙️ Hive City Crisis - Warhammer 40K Macera",
        "genre": "warhammer",
        "description": "Hive City Tertium'da geçen epik macera. Ork istilası, Chaos kültü ve Genestealer tehdidi aynı anda şehri tehdit ediyor. Sadece sen bu krizi çözebilirsin!",
        "difficulty": "extreme",
        "theme": "warhammer",
        "complexity": "extreme",
        "estimatedPlayTime": 420,
        "levels": {
            "level_1": {
                "title": "Hive City Savunması",
                "min_level": 1,
                "max_level": 15,
                "enemies": ["Ork Boyz", "Genestealers", "Chaos Cultists"],
                "boss": "Ork Warboss"
            }
        },
        "npc_relationships": {
            "governor_maria": {
                "name": "Governor Maria Tertium",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "stranger",
                "ending_impact": "extreme"
            },
            "arbites_commander": {
                "name": "Arbites Commander Rex",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "stranger",
                "ending_impact": "high"
            },
            "tech_priest_alpha": {
                "name": "Tech-Priest Alpha-7",
                "trust_level": 0,
                "quests_completed": 0,
                "relationship_status": "stranger",
                "ending_impact": "high"
            }
        },
        "quest_chains": {
            "hive_defense": {
                "title": "Hive City Savunma Operasyonu",
                "prerequisites": [],
                "quests": ["defend_hive", "eliminate_threats", "protect_citizens"],
                "rewards": {"xp": 1200, "hive_rep": 600, "items": ["power_armor"]}
            }
        },
        "quest_definitions": {
            "ork_invasion": {
                "title": "Ork Invasion",
                "objectives": ["Fight ork boyz", "Defeat ork nobz", "Kill ork warboss", "Secure territory"],
                "branches": {
                    "success": {"leads_to": "ork_defeat", "rewards": {"xp": 400, "hive_rep": 80, "combat": 100}},
                    "failure": {"leads_to": "ork_advance", "penalties": {"hive_safety": -40}},
                    "perfect": {"leads_to": "ork_annihilation", "rewards": {"xp": 600, "hive_rep": 120, "ork_slayer": True}}
                },
                "dynamic_rewards": {"experience": 400, "hive_rep": 80, "combat": 100},
                "world_state_impact": {"ork_threat": "-100", "hive_safety": "+80", "combat_reputation": "+60"}
            },
            "genestealer_hunt": {
                "title": "Genestealer Hunt",
                "objectives": ["Find genestealer cult", "Fight genestealers", "Kill patriarch", "Purge infection"],
                "branches": {
                    "success": {"leads_to": "genestealer_defeat", "rewards": {"xp": 500, "hive_rep": 100, "combat": 120}},
                    "failure": {"leads_to": "infection_spread", "penalties": {"corruption_level": 50}},
                    "perfect": {"leads_to": "infection_purge", "rewards": {"xp": 700, "hive_rep": 140, "purifier": True}}
                },
                "dynamic_rewards": {"experience": 500, "hive_rep": 100, "combat": 120},
                "world_state_impact": {"genestealer_threat": "-120", "hive_purity": "+100", "combat_experience": "+80"}
            },
            "chaos_cult_elimination": {
                "title": "Chaos Cult Elimination",
                "objectives": ["Find chaos cult", "Fight cultists", "Kill cult leader", "Destroy chaos artifacts"],
                "branches": {
                    "success": {"leads_to": "cult_defeat", "rewards": {"xp": 350, "hive_rep": 70, "combat": 90}},
                    "failure": {"leads_to": "cult_growth", "penalties": {"chaos_influence": 40}},
                    "perfect": {"leads_to": "cult_annihilation", "rewards": {"xp": 550, "hive_rep": 110, "chaos_hunter": True}}
                },
                "dynamic_rewards": {"experience": 350, "hive_rep": 70, "combat": 90},
                "world_state_impact": {"chaos_influence": "-80", "hive_security": "+70", "combat_skill": "+50"}
            },
            "hive_warfare": {
                "title": "Hive Warfare",
                "objectives": ["Coordinate hive defense", "Fight multiple enemies", "Secure hive levels", "Protect civilians"],
                "branches": {
                    "success": {"leads_to": "hive_victory", "rewards": {"xp": 600, "hive_rep": 120, "combat": 150}},
                    "failure": {"leads_to": "hive_loss", "penalties": {"hive_safety": -60}},
                    "perfect": {"leads_to": "hive_mastery", "rewards": {"xp": 800, "hive_rep": 160, "hive_defender": True}}
                },
                "dynamic_rewards": {"experience": 600, "hive_rep": 120, "combat": 150},
                "world_state_impact": {"hive_safety": "+150", "combat_mastery": "+100", "defender_reputation": "+120"}
            },
            "warboss_duel": {
                "title": "Warboss Duel",
                "objectives": ["Find warboss", "Fight warboss", "Defeat warboss", "Claim warboss trophy"],
                "branches": {
                    "success": {"leads_to": "warboss_defeat", "rewards": {"xp": 700, "hive_rep": 140, "combat": 180}},
                    "failure": {"leads_to": "warboss_victory", "penalties": {"combat": -30}},
                    "perfect": {"leads_to": "warboss_mastery", "rewards": {"xp": 900, "hive_rep": 180, "warboss_slayer": True}}
                },
                "dynamic_rewards": {"experience": 700, "hive_rep": 140, "combat": 180},
                "world_state_impact": {"ork_leadership": "-100", "hive_morale": "+120", "legendary_status": "+100"}
            }
        },
        "ending_variations": {
            "hive_victory": {
                "requirements": {"governor_trust": 90, "arbites_trust": 80, "hive_rep": 100},
                "description": "Hive City'yi kurtardınız! Tertium güvende!"
            },
            "ork_dominance": {
                "requirements": {"ork_rep": 70, "combat_level": 50},
                "description": "Ork'ları yönettiniz! WAAAGH! gücü sizinle!"
            },
            "chaos_corruption": {
                "requirements": {"chaos_influence": 80, "corruption_level": 60},
                "description": "Chaos'un gücü sizi ele geçirdi. Hive City yok oldu."
            }
        },
        "story_nodes": {
            "start": {
                "id": "start",
                "title": "🏙️ Hive City Tertium - Kriz Başlangıcı",
                "description": "Hive City Tertium'un üst seviyelerinde duruyorsunuz. Gökyüzü kızıl, Ork roketleri düşüyor, Chaos kültü alt katmanlarda faaliyet gösteriyor. Governor Maria size yaklaşıyor: 'Hive City'miz üçlü tehdit altında. Ork istilası, Chaos kültü ve Genestealer tehdidi. Sadece siz bu krizi çözebilirsiniz.' Arbites Commander Rex: 'Yasa ve düzen tehlikede.' Tech-Priest Alpha-7: 'Omnissiah'ın iradesi ile savaşacağız.'",
                "choices": [
                    {
                        "id": "defend_upper_hive",
                        "text": "Üst Hive'ı savun (Elit Savunma)",
                        "next_node": "upper_hive_defense",
                        "effect": {"combat": 30, "hive_rep": 35, "xp": 45}
                    },
                    {
                        "id": "investigate_lower_hive",
                        "text": "Alt Hive'ı araştır (Gizem Yolu)",
                        "next_node": "lower_hive_investigation",
                        "effect": {"investigation": 35, "arbites_trust": 25, "xp": 40}
                    },
                    {
                        "id": "tech_priest_alliance",
                        "text": "Tech-Priest ile ittifak kur (Teknoloji Yolu)",
                        "next_node": "tech_priest_alliance",
                        "effect": {"technology": 30, "tech_priest_trust": 30, "xp": 40}
                    },
                    {
                        "id": "governor_council",
                        "text": "Governor konseyine katıl (Politik Yol)",
                        "next_node": "governor_council_meeting",
                        "effect": {"charisma": 35, "governor_trust": 30, "xp": 45}
                    }
                ]
            },
            "upper_hive_defense": {
                "id": "upper_hive_defense",
                "title": "🏙️ Üst Hive Savunması",
                "description": "Hive City'nin üst seviyelerinde pozisyon alıyorsunuz. Ork roketleri düşüyor, Chaos cultist'leri saldırıyor. Governor Maria: 'Üst Hive'ı koruyun! Bu bölge Hive City'nin kalbi!' Arbites Commander Rex: 'Yasa ve düzen burada başlar!' Tech-Priest Alpha-7: 'Omnissiah'ın teknolojisi ile savaşacağız!' Bu savaş Hive City'nin kaderini belirleyecek!",
                "choices": [
                    {
                        "id": "elite_guard_formation",
                        "text": "Elit muhafız birliği oluştur (Güçlü Savunma)",
                        "next_node": "elite_guard_combat",
                        "effect": {"combat": 40, "hive_rep": 30, "xp": 50}
                    },
                    {
                        "id": "artillery_coordination",
                        "text": "Topçu koordinasyonu yap (Stratejik Yaklaşım)",
                        "next_node": "artillery_coordination_hive",
                        "effect": {"strategy": 35, "governor_trust": 25, "xp": 45}
                    },
                    {
                        "id": "medical_evacuation",
                        "text": "Tıbbi tahliye organize et (İnsani Görev)",
                        "next_node": "medical_evacuation_hive",
                        "effect": {"charisma": 30, "hive_rep": 25, "xp": 40}
                    },
                    {
                        "id": "tech_support",
                        "text": "Teknik destek sağla (Teknoloji Yolu)",
                        "next_node": "tech_support_hive",
                        "effect": {"technology": 30, "tech_priest_trust": 25, "xp": 40}
                    }
                ]
            },
            "lower_hive_investigation": {
                "id": "lower_hive_investigation",
                "title": "🔍 Alt Hive Araştırması",
                "description": "Hive City'nin alt katmanlarında araştırma yapıyorsunuz. Karanlık geçitler, gizli tapınaklar, Genestealer izleri... Arbites Commander Rex: 'Alt Hive'da yasa ve düzen yok. Dikkatli olun.' Chaos sembolleri, Ork graffiti'leri, Genestealer pençe izleri... Bu araştırma hem tehlikeli hem de kritik!",
                "choices": [
                    {
                        "id": "chaos_cult_hunt",
                        "text": "Chaos kültünü avla (Tehlikeli Görev)",
                        "next_node": "chaos_cult_hunt_hive",
                        "effect": {"combat": 35, "arbites_trust": 30, "xp": 50}
                    },
                    {
                        "id": "genestealer_investigation",
                        "text": "Genestealer izini araştır (Gizem Yolu)",
                        "next_node": "genestealer_investigation_hive",
                        "effect": {"investigation": 40, "arbites_trust": 25, "xp": 45}
                    },
                    {
                        "id": "ork_gang_confrontation",
                        "text": "Ork çetesiyle yüzleş (Savaş Yolu)",
                        "next_node": "ork_gang_confrontation_hive",
                        "effect": {"combat": 30, "hive_rep": 20, "xp": 40}
                    },
                    {
                        "id": "underground_network",
                        "text": "Yeraltı ağını keşfet (Gizli Yol)",
                        "next_node": "underground_network_hive",
                        "effect": {"stealth": 35, "investigation": 25, "xp": 45}
                    }
                ]
            },
            "tech_priest_alliance": {
                "id": "tech_priest_alliance",
                "title": "⚙️ Tech-Priest İttifakı",
                "description": "Tech-Priest Alpha-7'nin atölyesinde bulunuyorsunuz. Makineler uğulduyor, teknoloji her yerde. Alpha-7: 'Omnissiah'ın iradesi ile Hive City'yi kurtarabiliriz.' Cybernetic implantlar, gelişmiş silahlar, koruyucu zırhlar, Hive City savunma sistemleri... Bu teknoloji savaşı kazanmanıza yardım edebilir!",
                "choices": [
                    {
                        "id": "hive_defense_systems",
                        "text": "Hive savunma sistemlerini aktifleştir (Teknoloji Yolu)",
                        "next_node": "hive_defense_activation",
                        "effect": {"technology": 40, "tech_priest_trust": 35, "xp": 50}
                    },
                    {
                        "id": "cybernetic_enhancement",
                        "text": "Cybernetic geliştirme yap (Güçlendirme)",
                        "next_node": "cybernetic_enhancement_hive",
                        "effect": {"technology": 35, "tech_priest_trust": 30, "xp": 45}
                    },
                    {
                        "id": "weapon_factory",
                        "text": "Silah fabrikasını çalıştır (Üretim)",
                        "next_node": "weapon_factory_hive",
                        "effect": {"technology": 30, "hive_rep": 25, "xp": 40}
                    },
                    {
                        "id": "communication_network",
                        "text": "İletişim ağını kur (Koordinasyon)",
                        "next_node": "communication_network_hive",
                        "effect": {"strategy": 30, "tech_priest_trust": 25, "xp": 40}
                    }
                ]
            },
            "governor_council_meeting": {
                "id": "governor_council_meeting",
                "title": "🏛️ Governor Konsey Toplantısı",
                "description": "Governor Maria'nın konsey odasında bulunuyorsunuz. Haritalar, strateji planları, istihbarat raporları... Maria: 'Hive City'nin durumu kritik. Üçlü tehdit yaklaşıyor. Her vatandaşın görevi önemli.' Savaş planları, taktikler, görev dağılımları, diplomatik çözümler... Bu toplantı Hive City'nin kaderini belirleyecek!",
                "choices": [
                    {
                        "id": "diplomatic_solution",
                        "text": "Diplomatik çözüm ara (Barış Yolu)",
                        "next_node": "diplomatic_negotiation",
                        "effect": {"charisma": 40, "governor_trust": 35, "xp": 50}
                    },
                    {
                        "id": "military_strategy",
                        "text": "Askeri strateji planla (Savaş Yolu)",
                        "next_node": "military_strategy_planning",
                        "effect": {"strategy": 40, "governor_trust": 30, "xp": 50}
                    },
                    {
                        "id": "resource_allocation",
                        "text": "Kaynak dağılımı yap (Yönetim)",
                        "next_node": "resource_allocation_hive",
                        "effect": {"strategy": 30, "hive_rep": 30, "xp": 45}
                    },
                    {
                        "id": "emergency_protocols",
                        "text": "Acil durum protokollerini aktifleştir (Güvenlik)",
                        "next_node": "emergency_protocols_hive",
                        "effect": {"strategy": 35, "governor_trust": 25, "xp": 45}
                    }
                ]
            },
            "diplomatic_negotiation": {
                "id": "diplomatic_negotiation",
                "title": "🤝 Diplomatik Müzakereler - Barış Arayışı",
                "description": "Governor Maria ile birlikte diplomatik çözüm arıyorsunuz. Ork Warboss, Chaos kültü lideri ve Genestealer Patriarch ile görüşmeler yapıyorsunuz. Her biri farklı taleplerde bulunuyor. Arbites Commander Rex güvenlik sağlıyor. Tech-Priest Alpha-7 teknolojik destek veriyor. Bu müzakereler Hive City'nin kaderini belirleyecek!",
                "choices": [
                    {
                        "id": "negotiate_with_orks",
                        "text": "Ork'larla müzakere et",
                        "next_node": "ork_negotiation",
                        "effect": {"charisma": 45, "ork_rep": 30, "xp": 60}
                    },
                    {
                        "id": "negotiate_with_chaos",
                        "text": "Chaos kültü ile müzakere et",
                        "next_node": "chaos_negotiation",
                        "effect": {"charisma": 40, "chaos_influence": 25, "xp": 55}
                    },
                    {
                        "id": "negotiate_with_genestealers",
                        "text": "Genestealer'lar ile müzakere et",
                        "next_node": "genestealer_negotiation",
                        "effect": {"charisma": 35, "genestealer_rep": 20, "xp": 50}
                    },
                    {
                        "id": "united_peace_talks",
                        "text": "Birleşik barış görüşmeleri",
                        "next_node": "united_peace_conference",
                        "effect": {"charisma": 50, "diplomacy": 40, "xp": 70}
                    }
                ]
            },
            "military_strategy_planning": {
                "id": "military_strategy_planning",
                "title": "⚔️ Askeri Strateji Planlaması - Savaş Hazırlığı",
                "description": "Governor Maria ile birlikte Hive City'nin askeri savunma stratejisini planlıyorsunuz. Arbites Commander Rex güvenlik kuvvetlerini organize ediyor. Tech-Priest Alpha-7 savunma sistemlerini hazırlıyor. Üçlü tehdide karşı kapsamlı bir savunma planı hazırlıyorsunuz. Bu plan Hive City'nin hayatta kalmasını sağlayacak!",
                "choices": [
                    {
                        "id": "defensive_strategy_hive",
                        "text": "Savunma odaklı strateji",
                        "next_node": "hive_defensive_planning",
                        "effect": {"strategy": 45, "governor_trust": 35, "xp": 65}
                    },
                    {
                        "id": "offensive_strategy_hive",
                        "text": "Saldırı stratejisi",
                        "next_node": "hive_offensive_planning",
                        "effect": {"combat": 40, "strategy": 35, "xp": 60}
                    },
                    {
                        "id": "guerrilla_warfare_hive",
                        "text": "Gerilla savaşı taktikleri",
                        "next_node": "hive_guerrilla_planning",
                        "effect": {"stealth": 40, "strategy": 30, "xp": 55}
                    },
                    {
                        "id": "combined_arms_hive",
                        "text": "Birleşik kuvvet stratejisi",
                        "next_node": "hive_combined_arms",
                        "effect": {"strategy": 50, "technology": 30, "xp": 70}
                    }
                ]
            },
            "ork_negotiation": {
                "id": "ork_negotiation",
                "title": "🟢 Ork Warboss ile Müzakereler",
                "description": "Ork Warboss Gorkamorka ile görüşüyorsunuz. Warboss büyük ve güçlü, yeşil derili, büyük çeneli. 'WAAAGH! Hive City'yi istiyoruz! Ama eğer savaş ekipmanı verirseniz, başka yere gidebiliriz!' Arbites Commander Rex tetikte, Tech-Priest Alpha-7 teknoloji öneriyor. Bu müzakereler çok tehlikeli!",
                "choices": [
                    {
                        "id": "offer_weapons",
                        "text": "Silah teklifi yap",
                        "next_node": "weapon_offer_to_orks",
                        "effect": {"charisma": 40, "ork_rep": 35, "xp": 60}
                    },
                    {
                        "id": "offer_territory",
                        "text": "Bölge teklifi yap",
                        "next_node": "territory_offer_to_orks",
                        "effect": {"charisma": 35, "ork_rep": 30, "xp": 55}
                    },
                    {
                        "id": "challenge_warboss",
                        "text": "Warboss'a meydan oku",
                        "next_node": "warboss_challenge",
                        "effect": {"combat": 45, "ork_rep": 40, "xp": 70}
                    },
                    {
                        "id": "deceive_orks",
                        "text": "Ork'ları aldat",
                        "next_node": "ork_deception",
                        "effect": {"deception": 40, "charisma": 30, "xp": 65}
                    }
                ]
            },
            "warboss_challenge": {
                "id": "warboss_challenge",
                "title": "⚔️ Warboss Meydan Okuması - Ork Lideri ile Savaş",
                "description": "Ork Warboss Gorkamorka size meydan okuyor! 'WAAAGH! Seni yenmek istiyorum! Eğer beni yenersen, Ork'lar Hive City'yi terk eder!' Warboss büyük bir choppa (balta) ve güçlü zırh giyiyor. Arbites Commander Rex size yardım etmek istiyor. Tech-Priest Alpha-7 silahlarınızı güçlendiriyor. Bu savaş Hive City'nin kaderini belirleyecek!",
                "choices": [
                    {
                        "id": "accept_challenge",
                        "text": "Meydan okumayı kabul et",
                        "next_node": "warboss_duel",
                        "effect": {"combat": 50, "ork_rep": 45, "xp": 80}
                    },
                    {
                        "id": "request_weapons",
                        "text": "Özel silahlar iste",
                        "next_node": "special_weapons_request",
                        "effect": {"technology": 40, "combat": 35, "xp": 70}
                    },
                    {
                        "id": "team_fight",
                        "text": "Takım savaşı öner",
                        "next_node": "team_warboss_fight",
                        "effect": {"combat": 45, "charisma": 35, "xp": 75}
                    },
                    {
                        "id": "tactical_retreat",
                        "text": "Taktik geri çekilme",
                        "next_node": "tactical_retreat_from_orks",
                        "effect": {"strategy": 40, "stealth": 30, "xp": 60}
                    }
                ]
            },
            "warboss_duel": {
                "id": "warboss_duel",
                "title": "⚔️ Warboss Düellosu - Ork Lideri ile Epik Savaş",
                "description": "Ork Warboss Gorkamorka ile epik düello başlıyor! Warboss büyük choppa'sını sallıyor, yeşil enerji ile çevrili. Siz de en iyi silahlarınızla hazırsınız. Arbites Commander Rex ve Tech-Priest Alpha-7 size moral veriyor. Bu düello Hive City'nin kaderini belirleyecek!",
                "choices": [
                    {
                        "id": "melee_combat_warboss",
                        "text": "Yakın dövüş savaşı",
                        "next_node": "melee_warboss_battle",
                        "effect": {"combat": 60, "ork_rep": 50, "xp": 100}
                    },
                    {
                        "id": "ranged_combat_warboss",
                        "text": "Uzaktan savaş",
                        "next_node": "ranged_warboss_battle",
                        "effect": {"combat": 55, "strategy": 35, "xp": 90}
                    },
                    {
                        "id": "tactical_combat_warboss",
                        "text": "Taktik savaş",
                        "next_node": "tactical_warboss_battle",
                        "effect": {"strategy": 50, "combat": 45, "xp": 95}
                    },
                    {
                        "id": "honorable_surrender",
                        "text": "Onurlu teslimiyet",
                        "next_node": "honorable_surrender_to_orks",
                        "effect": {"charisma": 45, "ork_rep": 40, "xp": 85}
                    }
                ]
            },
            "melee_warboss_battle": {
                "id": "melee_warboss_battle",
                "title": "⚔️ Yakın Dövüş Savaşı - Warboss ile Son Karşılaşma",
                "description": "Ork Warboss ile yakın dövüş savaşı! Kılıçlar çarpışıyor, yeşil enerji her yerde. Warboss'un gücü inanılmaz ama sizin kararlılığınız da öyle. Arbites Commander Rex size moral veriyor. Tech-Priest Alpha-7'nin silahları çok işe yarıyor. Bu savaşın sonucu Hive City'nin kaderini belirleyecek!",
                "choices": [
                    {
                        "id": "final_strike_warboss",
                        "text": "Son vuruşu yap",
                        "next_node": "warboss_defeat",
                        "effect": {"combat": 70, "ork_rep": 60, "xp": 120}
                    },
                    {
                        "id": "use_imperial_weapon_hive",
                        "text": "İmparator silahını kullan",
                        "next_node": "imperial_weapon_use_hive",
                        "effect": {"combat": 65, "ork_rep": 55, "xp": 110}
                    },
                    {
                        "id": "team_attack_warboss",
                        "text": "Takım saldırısı",
                        "next_node": "team_warboss_attack",
                        "effect": {"combat": 60, "charisma": 40, "xp": 105}
                    },
                    {
                        "id": "sacrifice_attack_warboss",
                        "text": "Fedakarlık saldırısı",
                        "next_node": "sacrifice_attack_warboss",
                        "effect": {"combat": 75, "sacrifice_points": 50, "xp": 130}
                    }
                ]
            },
            "warboss_defeat": {
                "id": "warboss_defeat",
                "title": "🏆 Warboss Yenildi - Ork Zaferi!",
                "description": "Ork Warboss'u yendiniz! Warboss yere düşüyor, yeşil enerji dağılıyor. Ork'lar şaşkınlık içinde. Arbites Commander Rex size teşekkür ediyor. Tech-Priest Alpha-7 zaferi kutluyor. Bu büyük bir zafer! Ork'lar Hive City'yi terk ediyor. İmparator'un iradesi galip geldi!",
                "choices": [
                    {
                        "id": "secure_ork_victory",
                        "text": "Ork zaferini güvenli hale getir",
                        "next_node": "ork_victory_securing",
                        "effect": {"strategy": 45, "hive_rep": 40, "xp": 100}
                    },
                    {
                        "id": "return_to_hive",
                        "text": "Hive City'ye dön",
                        "next_node": "return_to_hive_victory",
                        "effect": {"hive_rep": 50, "governor_trust": 45, "xp": 110}
                    },
                    {
                        "id": "investigate_ork_remains",
                        "text": "Ork kalıntılarını araştır",
                        "next_node": "ork_remains_investigation",
                        "effect": {"investigation": 50, "technology": 35, "xp": 105}
                    },
                    {
                        "id": "celebrate_ork_victory",
                        "text": "Ork zaferini kutla",
                        "next_node": "victory_celebration_hive",
                        "effect": {"charisma": 45, "hive_rep": 35, "xp": 95}
                    }
                ]
            },
            "return_to_hive_victory": {
                "id": "return_to_hive_victory",
                "title": "🏙️ Hive City'ye Zaferle Dönüş",
                "description": "Hive City'ye zaferle dönüyorsunuz! Herkes sizi karşılıyor. Governor Maria size teşekkür ediyor. Arbites Commander Rex sizi kutluyor. Tech-Priest Alpha-7 zaferi kutluyor. Ork Warboss öldü! Hive City artık daha güvende. İmparator'un iradesi galip geldi. Bu gün Hive City'nin tarihinde altın harflerle yazılacak!",
                "choices": [
                    {
                        "id": "accept_hive_honor",
                        "text": "Hive onurunu kabul et",
                        "next_node": "hive_honor",
                        "effect": {"charisma": 60, "hive_rep": 70, "xp": 150}
                    },
                    {
                        "id": "rebuild_hive",
                        "text": "Hive City'yi yeniden inşa etmeye yardım et",
                        "next_node": "hive_rebuilding",
                        "effect": {"charisma": 50, "hive_rep": 60, "xp": 130}
                    },
                    {
                        "id": "share_hive_glory",
                        "text": "Hive zaferini paylaş",
                        "next_node": "glory_sharing_hive",
                        "effect": {"charisma": 55, "hive_rep": 65, "xp": 140}
                    },
                    {
                        "id": "end_hive_mission",
                        "text": "Hive görevini sonlandır",
                        "next_node": "end",
                        "effect": {"xp": 200}
                    }
                ]
            },
            "artillery_coordination_hive": {
                "id": "artillery_coordination_hive",
                "title": "Hive Topçu Koordinasyonu",
                "description": "Hive City'nin topçu birimlerini koordine ediyorsunuz.",
                "choices": [
                    {
                        "id": "coordinate_hive_artillery",
                        "text": "Hive topçularını koordine et",
                        "next_node": "elite_guard_combat",
                        "effect": {"strategy": 40, "xp": 55}
                    }
                ]
            },
            "chaos_cult_hunt_hive": {
                "id": "chaos_cult_hunt_hive",
                "title": "Chaos Kültü Avı",
                "description": "Chaos kültünü avlıyorsunuz.",
                "choices": [
                    {
                        "id": "eliminate_chaos_cult",
                        "text": "Chaos kültünü yok et",
                        "next_node": "warboss_defeat",
                        "effect": {"combat": 45, "xp": 70}
                    }
                ]
            },
            "chaos_negotiation": {
                "id": "chaos_negotiation",
                "title": "Chaos Müzakeresi",
                "description": "Chaos kültü ile müzakere ediyorsunuz.",
                "choices": [
                    {
                        "id": "negotiate_chaos_terms",
                        "text": "Chaos şartlarını müzakere et",
                        "next_node": "united_peace_conference",
                        "effect": {"charisma": 35, "xp": 50}
                    }
                ]
            },
            "communication_network_hive": {
                "id": "communication_network_hive",
                "title": "Hive İletişim Ağı",
                "description": "Hive City'nin iletişim ağını kuruyorsunuz.",
                "choices": [
                    {
                        "id": "establish_communication",
                        "text": "İletişimi kur",
                        "next_node": "hive_combined_arms",
                        "effect": {"strategy": 35, "xp": 50}
                    }
                ]
            },
            "cybernetic_enhancement_hive": {
                "id": "cybernetic_enhancement_hive",
                "title": "Hive Cybernetic Geliştirme",
                "description": "Cybernetic geliştirme yapıyorsunuz.",
                "choices": [
                    {
                        "id": "enhance_cybernetics",
                        "text": "Cybernetics'i geliştir",
                        "next_node": "elite_guard_combat",
                        "effect": {"technology": 40, "xp": 60}
                    }
                ]
            },
            "elite_guard_combat": {
                "id": "elite_guard_combat",
                "title": "Elit Muhafız Savaşı",
                "description": "Elit muhafız birliği ile savaşıyorsunuz.",
                "choices": [
                    {
                        "id": "lead_elite_guards",
                        "text": "Elit muhafızları yönet",
                        "next_node": "warboss_duel",
                        "effect": {"combat": 50, "xp": 75}
                    }
                ]
            },
            "emergency_protocols_hive": {
                "id": "emergency_protocols_hive",
                "title": "Hive Acil Durum Protokolleri",
                "description": "Acil durum protokollerini aktifleştiriyorsunuz.",
                "choices": [
                    {
                        "id": "activate_protocols",
                        "text": "Protokolleri aktifleştir",
                        "next_node": "hive_defensive_planning",
                        "effect": {"strategy": 40, "xp": 55}
                    }
                ]
            },
            "genestealer_investigation_hive": {
                "id": "genestealer_investigation_hive",
                "title": "Genestealer Araştırması",
                "description": "Genestealer izini araştırıyorsunuz.",
                "choices": [
                    {
                        "id": "track_genestealers",
                        "text": "Genestealer'ları takip et",
                        "next_node": "underground_network_hive",
                        "effect": {"investigation": 45, "xp": 65}
                    }
                ]
            },
            "genestealer_negotiation": {
                "id": "genestealer_negotiation",
                "title": "Genestealer Müzakeresi",
                "description": "Genestealer'lar ile müzakere ediyorsunuz.",
                "choices": [
                    {
                        "id": "negotiate_genestealer_terms",
                        "text": "Genestealer şartlarını müzakere et",
                        "next_node": "united_peace_conference",
                        "effect": {"charisma": 30, "xp": 45}
                    }
                ]
            },
            "glory_sharing_hive": {
                "id": "glory_sharing_hive",
                "title": "Hive Zafer Paylaşımı",
                "description": "Hive zaferini paylaşıyorsunuz.",
                "choices": [
                    {
                        "id": "share_hive_victory",
                        "text": "Hive zaferini paylaş",
                        "next_node": "end",
                        "effect": {"charisma": 60, "xp": 100}
                    }
                ]
            },
            "hive_combined_arms": {
                "id": "hive_combined_arms",
                "title": "Hive Birleşik Kuvvet",
                "description": "Birleşik kuvvet stratejisini uyguluyorsunuz.",
                "choices": [
                    {
                        "id": "execute_combined_hive_strategy",
                        "text": "Birleşik Hive stratejisini uygula",
                        "next_node": "elite_guard_combat",
                        "effect": {"strategy": 55, "xp": 80}
                    }
                ]
            },
            "hive_defense_activation": {
                "id": "hive_defense_activation",
                "title": "Hive Savunma Aktivasyonu",
                "description": "Hive savunma sistemlerini aktifleştiriyorsunuz.",
                "choices": [
                    {
                        "id": "activate_hive_defenses",
                        "text": "Hive savunmalarını aktifleştir",
                        "next_node": "elite_guard_combat",
                        "effect": {"technology": 50, "xp": 75}
                    }
                ]
            },
            "hive_defensive_planning": {
                "id": "hive_defensive_planning",
                "title": "Hive Savunma Planlaması",
                "description": "Hive savunma stratejisi planlıyorsunuz.",
                "choices": [
                    {
                        "id": "implement_hive_defense",
                        "text": "Hive savunmasını uygula",
                        "next_node": "upper_hive_defense",
                        "effect": {"strategy": 50, "xp": 70}
                    }
                ]
            },
            "hive_guerrilla_planning": {
                "id": "hive_guerrilla_planning",
                "title": "Hive Gerilla Planlaması",
                "description": "Gerilla savaşı taktikleri planlıyorsunuz.",
                "choices": [
                    {
                        "id": "execute_hive_guerrilla",
                        "text": "Hive gerilla taktiğini uygula",
                        "next_node": "underground_network_hive",
                        "effect": {"stealth": 45, "xp": 65}
                    }
                ]
            },
            "hive_honor": {
                "id": "hive_honor",
                "title": "Hive Onuru",
                "description": "Hive onurunu kabul ediyorsunuz.",
                "choices": [
                    {
                        "id": "accept_hive_honor",
                        "text": "Hive onuru kabul et",
                        "next_node": "end",
                        "effect": {"charisma": 70, "xp": 120}
                    }
                ]
            },
            "hive_offensive_planning": {
                "id": "hive_offensive_planning",
                "title": "Hive Saldırı Planlaması",
                "description": "Saldırı stratejisi geliştiriyorsunuz.",
                "choices": [
                    {
                        "id": "launch_hive_offensive",
                        "text": "Hive saldırısını başlat",
                        "next_node": "ork_negotiation",
                        "effect": {"combat": 50, "xp": 70}
                    }
                ]
            },
            "hive_rebuilding": {
                "id": "hive_rebuilding",
                "title": "Hive Yeniden İnşası",
                "description": "Hive City'yi yeniden inşa ediyorsunuz.",
                "choices": [
                    {
                        "id": "complete_hive_rebuilding",
                        "text": "Hive yeniden inşasını tamamla",
                        "next_node": "end",
                        "effect": {"charisma": 60, "xp": 120}
                    }
                ]
            },
            "honorable_surrender_to_orks": {
                "id": "honorable_surrender_to_orks",
                "title": "Ork'lara Onurlu Teslimiyet",
                "description": "Ork'lara onurlu teslimiyet yapıyorsunuz.",
                "choices": [
                    {
                        "id": "negotiate_surrender_terms",
                        "text": "Teslimiyet şartlarını müzakere et",
                        "next_node": "territory_offer_to_orks",
                        "effect": {"charisma": 40, "xp": 60}
                    }
                ]
            },
            "imperial_weapon_use_hive": {
                "id": "imperial_weapon_use_hive",
                "title": "Hive Imperial Silah Kullanımı",
                "description": "İmparator silahını kullanıyorsunuz.",
                "choices": [
                    {
                        "id": "victory_with_imperial_weapon",
                        "text": "Imperial silahla zafer kazan",
                        "next_node": "warboss_defeat",
                        "effect": {"combat": 70, "xp": 110}
                    }
                ]
            },
            "medical_evacuation_hive": {
                "id": "medical_evacuation_hive",
                "title": "Hive Tıbbi Tahliye",
                "description": "Tıbbi tahliye organize ediyorsunuz.",
                "choices": [
                    {
                        "id": "evacuate_wounded",
                        "text": "Yaralıları tahliye et",
                        "next_node": "hive_defensive_planning",
                        "effect": {"charisma": 35, "xp": 50}
                    }
                ]
            },
            "ork_deception": {
                "id": "ork_deception",
                "title": "Ork Aldatmacası",
                "description": "Ork'ları aldatıyorsunuz.",
                "choices": [
                    {
                        "id": "execute_deception",
                        "text": "Aldatmacayı gerçekleştir",
                        "next_node": "warboss_challenge",
                        "effect": {"deception": 45, "xp": 65}
                    }
                ]
            },
            "ork_gang_confrontation_hive": {
                "id": "ork_gang_confrontation_hive",
                "title": "Ork Çetesi Karşılaşması",
                "description": "Ork çetesiyle yüzleşiyorsunuz.",
                "choices": [
                    {
                        "id": "fight_ork_gang",
                        "text": "Ork çetesiyle savaş",
                        "next_node": "warboss_duel",
                        "effect": {"combat": 40, "xp": 60}
                    }
                ]
            },
            "ork_remains_investigation": {
                "id": "ork_remains_investigation",
                "title": "Ork Kalıntıları Araştırması",
                "description": "Ork kalıntılarını araştırıyorsunuz.",
                "choices": [
                    {
                        "id": "analyze_ork_remains",
                        "text": "Ork kalıntılarını analiz et",
                        "next_node": "ork_victory_securing",
                        "effect": {"investigation": 45, "xp": 65}
                    }
                ]
            },
            "ork_victory_securing": {
                "id": "ork_victory_securing",
                "title": "Ork Zaferi Güvenli Hale Getirme",
                "description": "Ork zaferini güvenli hale getiriyorsunuz.",
                "choices": [
                    {
                        "id": "secure_ork_victory",
                        "text": "Ork zaferini güvenli hale getir",
                        "next_node": "return_to_hive_victory",
                        "effect": {"strategy": 50, "xp": 75}
                    }
                ]
            },
            "ranged_warboss_battle": {
                "id": "ranged_warboss_battle",
                "title": "Uzaktan Warboss Savaşı",
                "description": "Uzaktan savaş yapıyorsunuz.",
                "choices": [
                    {
                        "id": "ranged_warboss_victory",
                        "text": "Uzaktan Warboss zafer kazan",
                        "next_node": "warboss_defeat",
                        "effect": {"combat": 60, "xp": 90}
                    }
                ]
            },
            "resource_allocation_hive": {
                "id": "resource_allocation_hive",
                "title": "Hive Kaynak Dağılımı",
                "description": "Kaynak dağılımı yapıyorsunuz.",
                "choices": [
                    {
                        "id": "allocate_hive_resources",
                        "text": "Hive kaynaklarını dağıt",
                        "next_node": "hive_defensive_planning",
                        "effect": {"strategy": 35, "xp": 50}
                    }
                ]
            },
            "sacrifice_attack_warboss": {
                "id": "sacrifice_attack_warboss",
                "title": "Warboss'a Fedakarlık Saldırısı",
                "description": "Warboss'a fedakarlık saldırısı yapıyorsunuz.",
                "choices": [
                    {
                        "id": "heroic_warboss_sacrifice",
                        "text": "Kahramanca Warboss fedakarlığı",
                        "next_node": "warboss_defeat",
                        "effect": {"combat": 80, "sacrifice_points": 100, "xp": 150}
                    }
                ]
            },
            "special_weapons_request": {
                "id": "special_weapons_request",
                "title": "Özel Silah İsteği",
                "description": "Özel silahlar istiyorsunuz.",
                "choices": [
                    {
                        "id": "obtain_special_weapons",
                        "text": "Özel silahları edinin",
                        "next_node": "warboss_duel",
                        "effect": {"technology": 45, "xp": 65}
                    }
                ]
            },
            "tactical_retreat_from_orks": {
                "id": "tactical_retreat_from_orks",
                "title": "Ork'lardan Taktik Geri Çekilme",
                "description": "Ork'lardan taktik geri çekilme yapıyorsunuz.",
                "choices": [
                    {
                        "id": "regroup_against_orks",
                        "text": "Ork'lara karşı yeniden toparlan",
                        "next_node": "hive_defensive_planning",
                        "effect": {"strategy": 45, "xp": 60}
                    }
                ]
            },
            "tactical_warboss_battle": {
                "id": "tactical_warboss_battle",
                "title": "Taktik Warboss Savaşı",
                "description": "Taktik savaş yapıyorsunuz.",
                "choices": [
                    {
                        "id": "tactical_warboss_victory",
                        "text": "Taktik Warboss zafer kazan",
                        "next_node": "warboss_defeat",
                        "effect": {"strategy": 55, "xp": 95}
                    }
                ]
            },
            "team_warboss_attack": {
                "id": "team_warboss_attack",
                "title": "Takım Warboss Saldırısı",
                "description": "Takım saldırısı yapıyorsunuz.",
                "choices": [
                    {
                        "id": "coordinated_warboss_attack",
                        "text": "Koordineli Warboss saldırısı",
                        "next_node": "warboss_defeat",
                        "effect": {"combat": 65, "xp": 95}
                    }
                ]
            },
            "team_warboss_fight": {
                "id": "team_warboss_fight",
                "title": "Takım Warboss Savaşı",
                "description": "Takım savaşı yapıyorsunuz.",
                "choices": [
                    {
                        "id": "team_warboss_victory",
                        "text": "Takım Warboss zaferi",
                        "next_node": "warboss_defeat",
                        "effect": {"combat": 60, "xp": 90}
                    }
                ]
            },
            "tech_support_hive": {
                "id": "tech_support_hive",
                "title": "Hive Teknik Destek",
                "description": "Teknik destek sağlıyorsunuz.",
                "choices": [
                    {
                        "id": "provide_tech_support",
                        "text": "Teknik destek sağla",
                        "next_node": "hive_defense_activation",
                        "effect": {"technology": 35, "xp": 50}
                    }
                ]
            },
            "territory_offer_to_orks": {
                "id": "territory_offer_to_orks",
                "title": "Ork'lara Bölge Teklifi",
                "description": "Ork'lara bölge teklifi yapıyorsunuz.",
                "choices": [
                    {
                        "id": "negotiate_territory",
                        "text": "Bölgeyi müzakere et",
                        "next_node": "united_peace_conference",
                        "effect": {"charisma": 40, "xp": 60}
                    }
                ]
            },
            "underground_network_hive": {
                "id": "underground_network_hive",
                "title": "Hive Yeraltı Ağı",
                "description": "Yeraltı ağını keşfediyorsunuz.",
                "choices": [
                    {
                        "id": "explore_underground",
                        "text": "Yeraltını keşfet",
                        "next_node": "genestealer_investigation_hive",
                        "effect": {"stealth": 40, "xp": 60}
                    }
                ]
            },
            "united_peace_conference": {
                "id": "united_peace_conference",
                "title": "Birleşik Barış Konferansı",
                "description": "Birleşik barış görüşmeleri yapıyorsunuz.",
                "choices": [
                    {
                        "id": "achieve_peace",
                        "text": "Barışı başar",
                        "next_node": "return_to_hive_victory",
                        "effect": {"charisma": 60, "diplomacy": 50, "xp": 100}
                    }
                ]
            },
            "victory_celebration_hive": {
                "id": "victory_celebration_hive",
                "title": "Hive Zafer Kutlaması",
                "description": "Hive zaferini kutluyorsunuz.",
                "choices": [
                    {
                        "id": "celebrate_hive_victory",
                        "text": "Hive zaferini kutla",
                        "next_node": "end",
                        "effect": {"charisma": 50, "xp": 80}
                    }
                ]
            },
            "weapon_factory_hive": {
                "id": "weapon_factory_hive",
                "title": "Hive Silah Fabrikası",
                "description": "Silah fabrikasını çalıştırıyorsunuz.",
                "choices": [
                    {
                        "id": "produce_weapons",
                        "text": "Silah üret",
                        "next_node": "elite_guard_combat",
                        "effect": {"technology": 40, "xp": 60}
                    }
                ]
            },
            "weapon_offer_to_orks": {
                "id": "weapon_offer_to_orks",
                "title": "Ork'lara Silah Teklifi",
                "description": "Ork'lara silah teklifi yapıyorsunuz.",
                "choices": [
                    {
                        "id": "provide_weapons_to_orks",
                        "text": "Ork'lara silah sağla",
                        "next_node": "territory_offer_to_orks",
                        "effect": {"charisma": 35, "xp": 55}
                    }
                ]
            },
            "end": {
                "id": "end",
                "title": "🎉 Hive City Crisis Macera Tamamlandı",
                "description": "Hive City Tertium'da yaşanan bu epik macera sona erdi. Ork Warboss öldü, Hive City güvende, İmparator'un iradesi galip geldi. Siz bu zaferin kahramanısınız!",
                "choices": [
                    {
                        "id": "return_main_menu",
                        "text": "Ana Menüye Dön",
                        "next_node": "start",
                        "effect": {"xp": 50}
                    }
                ]
            }
        }
    }
}

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        app.logger.error(f'Error in home route: {e}')
        app.logger.error(f'Traceback: {traceback.format_exc()}')
        return f'Error: {str(e)}', 500

@app.route('/test')
def test():
    return jsonify({"status": "OK", "message": "Server is working"})

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/login')
def login():
    return '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Giriş - AI Dungeon Master</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #2a2a2a 100%);
                color: white;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .container {
                text-align: center;
                background: rgba(26, 26, 26, 0.8);
                padding: 40px;
                border-radius: 12px;
                border: 2px solid #FFD700;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                max-width: 400px;
                width: 100%;
            }
            .button {
                background: linear-gradient(45deg, #FFD700, #FFA500);
                color: #000;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                margin: 5px;
                text-decoration: none;
                display: inline-block;
                transition: all 0.3s ease;
            }
            .button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 GİRİŞ</h1>
            <p>Giriş sistemi yakında aktif olacak!</p>
            <a href="/" class="button">← Ana Sayfa</a>
            <a href="/game" class="button">🎮 Oyna</a>
        </div>
    </body>
    </html>
    '''

@app.route('/register')
def register():
    return '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Kayıt - AI Dungeon Master</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #2a2a2a 100%);
                color: white;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .container {
                text-align: center;
                background: rgba(26, 26, 26, 0.8);
                padding: 40px;
                border-radius: 12px;
                border: 2px solid #FFD700;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                max-width: 400px;
                width: 100%;
            }
            .button {
                background: linear-gradient(45deg, #FFD700, #FFA500);
                color: #000;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                margin: 5px;
                text-decoration: none;
                display: inline-block;
                transition: all 0.3s ease;
            }
            .button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📝 KAYIT</h1>
            <p>Kayıt sistemi yakında aktif olacak!</p>
            <a href="/" class="button">← Ana Sayfa</a>
            <a href="/game" class="button">🎮 Oyna</a>
        </div>
    </body>
    </html>
    '''

@app.route('/multiplayer')
def multiplayer():
    return '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Multiplayer - AI Dungeon Master</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #2a2a2a 100%);
                color: white;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .container {
                text-align: center;
                background: rgba(26, 26, 26, 0.8);
                padding: 40px;
                border-radius: 12px;
                border: 2px solid #FFD700;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                max-width: 400px;
                width: 100%;
            }
            .button {
                background: linear-gradient(45deg, #FFD700, #FFA500);
                color: #000;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                margin: 5px;
                text-decoration: none;
                display: inline-block;
                transition: all 0.3s ease;
            }
            .button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>👥 MULTIPLAYER</h1>
            <p>Multiplayer sistemi yakında aktif olacak!</p>
            <a href="/" class="button">← Ana Sayfa</a>
            <a href="/game" class="button">🎮 Oyna</a>
        </div>
    </body>
    </html>
    '''

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/test-buttons')
def test_buttons():
    return send_from_directory('.', 'test_buttons.html')

@app.route('/ai-scenarios')
def ai_scenarios():
    return '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <title>AI Senaryolar - AI Dungeon Master</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #2a2a2a 100%);
                color: white;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(26, 26, 26, 0.8);
                padding: 40px;
                border-radius: 12px;
                border: 2px solid #9C27B0;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }
            .ai-header {
                text-align: center;
                margin-bottom: 30px;
            }
            .ai-icon {
                font-size: 60px;
                color: #9C27B0;
                margin-bottom: 10px;
            }
            .ai-title {
                font-size: 32px;
                font-weight: bold;
                color: #9C27B0;
                margin-bottom: 10px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                color: #9C27B0;
                font-weight: bold;
            }
            input, select, textarea {
                width: 100%;
                padding: 10px;
                border: 1px solid #9C27B0;
                border-radius: 4px;
                background: rgba(255, 255, 255, 0.1);
                color: white;
                box-sizing: border-box;
            }
            textarea {
                height: 100px;
                resize: vertical;
            }
            .button {
                background: linear-gradient(45deg, #9C27B0, #673AB7);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                margin: 5px;
                transition: all 0.3s ease;
            }
            .button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(156, 39, 176, 0.4);
            }
            .scenario-result {
                background: rgba(0, 0, 0, 0.3);
                padding: 20px;
                border-radius: 8px;
                margin-top: 20px;
                border-left: 4px solid #9C27B0;
            }
            .loading {
                text-align: center;
                color: #9C27B0;
                font-style: italic;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="ai-header">
                <div class="ai-icon">🤖</div>
                <h1 class="ai-title">AI SENARYO ÜRETİCİ</h1>
                <p>Kendi hikayeni oluştur!</p>
            </div>
            
            <form id="ai-scenario-form">
                <div class="form-group">
                    <label>Senaryo Teması</label>
                    <select id="theme" required>
                        <option value="">Tema seçin...</option>
                        <option value="fantasy">Fantasy</option>
                        <option value="warhammer">Warhammer 40K</option>
                        <option value="cyberpunk">Cyberpunk</option>
                        <option value="scifi">Bilim Kurgu</option>
                        <option value="horror">Korku</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Senaryo Başlığı</label>
                    <input type="text" id="title" placeholder="Senaryonun başlığını girin..." required>
                </div>
                
                <div class="form-group">
                    <label>Ana Karakter</label>
                    <input type="text" id="character" placeholder="Ana karakterin adını girin..." required>
                </div>
                
                <div class="form-group">
                    <label>Senaryo Açıklaması</label>
                    <textarea id="description" placeholder="Senaryonun kısa açıklamasını girin..." required></textarea>
                </div>
                
                <div class="form-group">
                    <label>Zorluk Seviyesi</label>
                    <select id="difficulty" required>
                        <option value="">Zorluk seçin...</option>
                        <option value="easy">Kolay</option>
                        <option value="medium">Orta</option>
                        <option value="hard">Zor</option>
                        <option value="extreme">Aşırı Zor</option>
                    </select>
                </div>
                
                <div style="text-align: center;">
                    <button type="submit" class="button">🤖 AI SENARYO ÜRET</button>
                    <button type="button" class="button" onclick="window.location.href='/game'">🎮 OYUNA DÖN</button>
                    <button type="button" class="button" onclick="window.location.href='/'">🏠 ANA SAYFA</button>
                </div>
            </form>
            
            <div id="scenario-result" class="scenario-result" style="display: none;">
                <h3>🎭 Üretilen Senaryo</h3>
                <div id="generated-scenario"></div>
                <div style="text-align: center; margin-top: 20px;">
                    <button class="button" onclick="saveScenario()">💾 SENARYOYU KAYDET</button>
                    <button class="button" onclick="playScenario()">🎮 OYNA</button>
                </div>
            </div>
        </div>

        <script>
            let currentScenario = null;
            
            document.getElementById('ai-scenario-form').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const formData = {
                    theme: document.getElementById('theme').value,
                    title: document.getElementById('title').value,
                    character: document.getElementById('character').value,
                    description: document.getElementById('description').value,
                    difficulty: document.getElementById('difficulty').value
                };
                
                // Loading göster
                document.getElementById('scenario-result').style.display = 'block';
                document.getElementById('generated-scenario').innerHTML = `
                    <div class="loading">
                        <h4>🤖 AI senaryo üretiyor...</h4>
                        <p>Lütfen bekleyin, bu birkaç saniye sürebilir...</p>
                    </div>
                `;
                
                try {
                    // Gerçek AI senaryo üretimi
                    const response = await fetch('/api/generate-scenario', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(formData)
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        currentScenario = result.scenario;
                        displayGeneratedScenario(result.scenario);
                    } else {
                        throw new Error(result.error || 'Senaryo üretimi başarısız');
                    }
                } catch (error) {
                    console.error('AI Scenario generation error:', error);
                    document.getElementById('generated-scenario').innerHTML = `
                        <div style="color: #ff6b6b;">
                            <h4>❌ Hata!</h4>
                            <p>Senaryo üretimi sırasında bir hata oluştu: ${error.message}</p>
                            <p>Lütfen tekrar deneyin.</p>
                        </div>
                    `;
                }
            });
            
            function displayGeneratedScenario(scenario) {
                document.getElementById('generated-scenario').innerHTML = `
                    <h4>🎭 ${scenario.title}</h4>
                    <div style="margin: 15px 0;">
                        <p><strong>🎯 Tema:</strong> ${scenario.theme}</p>
                        <p><strong>⚔️ Zorluk:</strong> ${scenario.difficulty}</p>
                        <p><strong>🎮 Seviye:</strong> ${scenario.min_level}-${scenario.max_level}</p>
                        <p><strong>⏱️ Süre:</strong> ${scenario.duration} dakika</p>
                    </div>
                    <div style="background: rgba(0,0,0,0.2); padding: 15px; border-radius: 6px; margin: 15px 0;">
                        <p><strong>📖 Açıklama:</strong></p>
                        <p>${scenario.description}</p>
                    </div>
                    <div style="margin: 10px 0;">
                        <p><strong>🏰 Hikaye Noktaları:</strong> ${Object.keys(scenario.story_nodes || {}).length} adet</p>
                        <p><strong>👥 NPC'ler:</strong> ${Object.keys(scenario.npc_relationships || {}).length} adet</p>
                        <p><strong>🎯 Görev Zincirleri:</strong> ${Object.keys(scenario.quest_chains || {}).length} adet</p>
                    </div>
                    <div style="background: rgba(156, 39, 176, 0.2); padding: 10px; border-radius: 6px; margin: 15px 0;">
                        <p style="color: #9C27B0; font-weight: bold;">✨ Bu senaryo AI tarafından özel olarak sizin için üretildi!</p>
                        <p style="font-size: 12px; color: rgba(255,255,255,0.7);">ID: ${scenario.id} | Oluşturulma: ${new Date().toLocaleString('tr-TR')}</p>
                    </div>
                `;
            }
            
            async function saveScenario() {
                if (!currentScenario) {
                    alert('❌ Kaydedilecek senaryo yok!');
                    return;
                }
                
                try {
                    const response = await fetch('/api/scenarios/save', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            scenario: currentScenario,
                            user_id: 'guest_user'
                        })
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        alert('✅ Senaryo başarıyla kaydedildi!');
                    } else {
                        alert('❌ Kaydetme başarısız: ' + result.error);
                    }
                } catch (error) {
                    console.error('Save error:', error);
                    alert('❌ Kaydetme sırasında hata: ' + error.message);
                }
            }
            
            async function playScenario() {
                if (!currentScenario) {
                    alert('❌ Oynanacak senaryo yok!');
                    return;
                }
                
                // Senaryoyu oyun moduna aktar
                localStorage.setItem('selectedScenario', JSON.stringify(currentScenario));
                window.location.href = '/game?scenario=' + currentScenario.id;
            }
        </script>
    </body>
    </html>
    '''

@app.route('/ai-scenario')
def ai_scenario():
    return '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <title>AI Senaryo Üretimi - AI Dungeon Master</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #2a2a2a 100%);
                color: white;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(26, 26, 26, 0.8);
                padding: 40px;
                border-radius: 12px;
                border: 2px solid #9C27B0;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }
            .ai-header {
                text-align: center;
                margin-bottom: 30px;
            }
            .ai-icon {
                font-size: 60px;
                color: #9C27B0;
                margin-bottom: 10px;
            }
            .ai-title {
                font-size: 32px;
                font-weight: bold;
                color: #9C27B0;
                margin-bottom: 10px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                color: #9C27B0;
                font-weight: bold;
            }
            input, select, textarea {
                width: 100%;
                padding: 10px;
                border: 1px solid #9C27B0;
                border-radius: 4px;
                background: rgba(255, 255, 255, 0.1);
                color: white;
                box-sizing: border-box;
            }
            textarea {
                height: 100px;
                resize: vertical;
            }
            .button {
                background: linear-gradient(45deg, #9C27B0, #673AB7);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                margin: 5px;
                transition: all 0.3s ease;
            }
            .button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(156, 39, 176, 0.4);
            }
            .scenario-result {
                background: rgba(0, 0, 0, 0.3);
                padding: 20px;
                border-radius: 8px;
                margin-top: 20px;
                border-left: 4px solid #9C27B0;
            }
            .loading {
                text-align: center;
                color: #9C27B0;
                font-style: italic;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="ai-header">
                <div class="ai-icon">🤖</div>
                <h1 class="ai-title">AI SENARYO ÜRETİCİ</h1>
                <p>Kendi hikayeni oluştur!</p>
            </div>
            
            <form id="ai-scenario-form">
                <div class="form-group">
                    <label>Senaryo Teması</label>
                    <select id="theme" required>
                        <option value="">Tema seçin...</option>
                        <option value="fantasy">Fantasy</option>
                        <option value="warhammer">Warhammer 40K</option>
                        <option value="cyberpunk">Cyberpunk</option>
                        <option value="scifi">Bilim Kurgu</option>
                        <option value="horror">Korku</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Senaryo Başlığı</label>
                    <input type="text" id="title" placeholder="Senaryonun başlığını girin..." required>
                </div>
                
                <div class="form-group">
                    <label>Ana Karakter</label>
                    <input type="text" id="character" placeholder="Ana karakterin adını girin..." required>
                </div>
                
                <div class="form-group">
                    <label>Senaryo Açıklaması</label>
                    <textarea id="description" placeholder="Senaryonun kısa açıklamasını girin..." required></textarea>
                </div>
                
                <div class="form-group">
                    <label>Zorluk Seviyesi</label>
                    <select id="difficulty" required>
                        <option value="">Zorluk seçin...</option>
                        <option value="easy">Kolay</option>
                        <option value="medium">Orta</option>
                        <option value="hard">Zor</option>
                        <option value="extreme">Aşırı Zor</option>
                    </select>
                </div>
                
                <div style="text-align: center;">
                    <button type="submit" class="button">🤖 AI SENARYO ÜRET</button>
                    <button type="button" class="button" onclick="window.location.href='/game'">🎮 OYUNA DÖN</button>
                    <button type="button" class="button" onclick="window.location.href='/'">🏠 ANA SAYFA</button>
                </div>
            </form>
            
            <div id="scenario-result" class="scenario-result" style="display: none;">
                <h3>🎭 Üretilen Senaryo</h3>
                <div id="generated-scenario"></div>
                <div style="text-align: center; margin-top: 20px;">
                    <button class="button" onclick="saveScenario()">💾 SENARYOYU KAYDET</button>
                    <button class="button" onclick="playScenario()">▶️ OYNA</button>
                </div>
            </div>
        </div>
        
        <script>
            document.getElementById('ai-scenario-form').addEventListener('submit', function(e) {
                e.preventDefault();
                generateScenario();
            });
            
            function generateScenario() {
                const form = document.getElementById('ai-scenario-form');
                const result = document.getElementById('scenario-result');
                const generated = document.getElementById('generated-scenario');
                
                // Show loading
                result.style.display = 'block';
                generated.innerHTML = '<div class="loading">🤖 AI senaryo üretiyor...</div>';
                
                // Get form data
                const theme = document.getElementById('theme').value;
                const title = document.getElementById('title').value;
                const character = document.getElementById('character').value;
                const description = document.getElementById('description').value;
                const difficulty = document.getElementById('difficulty').value;
                
                // Simulate AI generation
                setTimeout(() => {
                    const scenario = createAIScenario(theme, title, character, description, difficulty);
                    generated.innerHTML = scenario;
                }, 2000);
            }
            
            function createAIScenario(theme, title, character, description, difficulty) {
                const themes = {
                    fantasy: "🏰",
                    warhammer: "⚔️",
                    cyberpunk: "🌃",
                    scifi: "🚀",
                    horror: "👻"
                };
                
                const difficulties = {
                    easy: "🟢 Kolay",
                    medium: "🟡 Orta", 
                    hard: "🔴 Zor",
                    extreme: "⚫ Aşırı Zor"
                };
                
                return `
                    <div style="margin-bottom: 20px;">
                        <h4>${themes[theme]} ${title}</h4>
                        <p><strong>Ana Karakter:</strong> ${character}</p>
                        <p><strong>Açıklama:</strong> ${description}</p>
                        <p><strong>Zorluk:</strong> ${difficulties[difficulty]}</p>
                        <p><strong>Tahmini Süre:</strong> ${Math.floor(Math.random() * 180) + 60} dakika</p>
                    </div>
                    
                    <div style="background: rgba(156, 39, 176, 0.1); padding: 15px; border-radius: 6px; margin-bottom: 15px;">
                        <h5>🎯 Ana Görevler:</h5>
                        <ul>
                            <li>${character} olarak dünyayı keşfet</li>
                            <li>Gizemli tehdidi araştır</li>
                            <li>Güçlü müttefikler bul</li>
                            <li>Final savaşında zafer kazan</li>
                        </ul>
                    </div>
                    
                    <div style="background: rgba(156, 39, 176, 0.1); padding: 15px; border-radius: 6px;">
                        <h5>🎭 Hikaye Elementleri:</h5>
                        <ul>
                            <li>Detaylı karakter gelişimi</li>
                            <li>Çoklu son seçenekleri</li>
                            <li>NPC ilişki sistemi</li>
                            <li>Dinamik dünya olayları</li>
                            <li>Seviye atlama sistemi</li>
                        </ul>
                    </div>
                `;
            }
            
            function saveScenario() {
                alert('✅ Senaryo başarıyla kaydedildi!');
            }
            
            function playScenario() {
                window.location.href = '/game';
            }
        </script>
    </body>
    </html>
    '''

@app.route('/api/health')
def health_check():
    try:
        return jsonify({
            'status': 'healthy',
            'message': 'AI Dungeon Master is running',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        app.logger.error(f'Health check error: {e}')
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/scenarios/enhanced/<scenario_id>')
def get_enhanced_scenario(scenario_id):
    if scenario_id in ENHANCED_SCENARIOS:
        return jsonify({
            "success": True,
            "scenario": ENHANCED_SCENARIOS[scenario_id]
        })
    else:
        return jsonify({
            "success": False,
            "error": "Scenario not found"
        }), 404

@app.route('/api/scenarios', methods=['GET'])
def get_scenarios():
    """Tüm senaryoları listele (hem varsayılan hem AI üretilen)"""
    try:
        scenarios = []
        
        # Varsayılan senaryoları ekle
        for scenario_id, scenario_data in ENHANCED_SCENARIOS.items():
            scenarios.append({
                "id": scenario_id,
                "title": scenario_data.get("title", "Unknown"),
                "theme": scenario_data.get("theme", "fantasy"),
                "difficulty": scenario_data.get("difficulty", "medium"),
                "description": scenario_data.get("description", "No description"),
                "min_level": scenario_data.get("levels", {}).get("level_1", {}).get("min_level", 1),
                "max_level": scenario_data.get("levels", {}).get("level_1", {}).get("max_level", 10),
                "duration": scenario_data.get("estimatedPlayTime", 120),
                "source": "default"
            })
        
        # AI üretilen senaryoları ekle
        ai_scenarios_file = 'data/ai_scenarios.json'
        try:
            with open(ai_scenarios_file, 'r', encoding='utf-8') as f:
                ai_scenarios = json.load(f)
                
            for scenario in ai_scenarios.get("scenarios", []):
                scenarios.append({
                    "id": scenario.get("id", "unknown"),
                    "title": scenario.get("title", "Unknown"),
                    "theme": scenario.get("theme", "fantasy"),
                    "difficulty": scenario.get("difficulty", "medium"),
                    "description": scenario.get("description", "No description"),
                    "min_level": scenario.get("min_level", 1),
                    "max_level": scenario.get("max_level", 10),
                    "duration": scenario.get("duration", 120),
                    "source": "ai_generated",
                    "file_source": scenario.get("file_source", ""),
                    "word_count": scenario.get("word_count", 0)
                })
        except FileNotFoundError:
            pass  # AI senaryoları yoksa sadece varsayılanları döndür
        
        return jsonify({
            "success": True,
            "scenarios": scenarios
        })
        
    except Exception as e:
        print(f"Senaryolar listesi hatası: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/scenarios/<scenario_id>', methods=['GET'])
def get_scenario(scenario_id):
    """Belirli bir senaryoyu getir"""
    try:
        # Önce varsayılan senaryolarda ara
        if scenario_id in ENHANCED_SCENARIOS:
            return jsonify({
                "success": True,
                "scenario": ENHANCED_SCENARIOS[scenario_id]
            })
        
        # AI üretilen senaryolarda ara
        ai_scenarios_file = 'data/ai_scenarios.json'
        try:
            with open(ai_scenarios_file, 'r', encoding='utf-8') as f:
                ai_scenarios = json.load(f)
                
            for scenario in ai_scenarios.get("scenarios", []):
                if scenario.get("id") == scenario_id:
                    return jsonify({
                        "success": True,
                        "scenario": scenario
                    })
                    
        except FileNotFoundError:
            pass
        
        return jsonify({
            "success": False,
            "error": "Senaryo bulunamadı"
        }), 404
        
    except Exception as e:
        print(f"Senaryo getirme hatası: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/stories/<scenario_id>')
def get_story(scenario_id):
    try:
        # Varsayılan senaryolarda ara
        if scenario_id in ENHANCED_SCENARIOS:
            story_data = ENHANCED_SCENARIOS[scenario_id]
            story_nodes = story_data.get("story_nodes", {})
            
            # Start node'u bul
            start_node = story_nodes.get("start", {
                "title": "Başlangıç",
                "description": "Macera başlıyor...",
                "choices": []
            })
            
            return jsonify({
                "success": True,
                "story": {
                    "id": "start",
                    "title": start_node.get('title', 'Başlangıç'),
                    "description": start_node.get('description', 'Macera başlıyor...'),
                    "choices": start_node.get("choices", [])
                }
            })
        
        # AI üretilen senaryolarda ara
        ai_scenarios_file = 'data/ai_scenarios.json'
        try:
            with open(ai_scenarios_file, 'r', encoding='utf-8') as f:
                ai_scenarios = json.load(f)
                
            for scenario in ai_scenarios.get("scenarios", []):
                if scenario.get("id") == scenario_id:
                    story_nodes = scenario.get("story_nodes", {})
                    
                    # Start node'u bul
                    start_node = story_nodes.get("start", {
                        "title": "Başlangıç",
                        "description": "Macera başlıyor...",
                        "choices": []
                    })
                    
                    return jsonify({
                        "success": True,
                        "story": {
                            "id": "start",
                            "title": start_node.get('title', 'Başlangıç'),
                            "description": start_node.get('description', 'Macera başlıyor...'),
                            "choices": start_node.get("choices", [])
                        }
                    })
                    
        except FileNotFoundError:
            pass
        
        return jsonify({
            "success": False,
            "error": "Story not found"
        }), 404
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/stories/<scenario_id>/choice', methods=['POST'])
def make_story_choice(scenario_id):
    """Hikaye seçimi yap ve oyuncu aksiyonunu kaydet"""
    try:
        data = request.get_json()
        choice_id = data.get('choice_id')
        user_id = data.get('user_id', 'guest_user')
        
        # Seçim türüne göre aksiyon belirle ve kaydet
        action_type = "exploration"  # varsayılan
        action_value = 1
        
        # İlk olarak genel action tracking
        update_player_stats(user_id, "total_actions", 1)
        update_player_stats(user_id, "time_spent", 5)  # Her action 5 dakika
        
        # Seçime göre spesifik action'lar
        if any(word in choice_id.lower() for word in ["combat", "savaş", "fight", "attack", "battle"]):
            action_type = "combat"
            action_value = 3
            update_player_stats(user_id, "combat_skill", action_value)
            update_player_stats(user_id, "damage_dealt", action_value * 15)
            update_player_stats(user_id, "combat_won", 1)
            
        elif any(word in choice_id.lower() for word in ["talk", "konuş", "negotiate", "speak", "conversation"]):
            action_type = "talk"
            action_value = 2
            update_player_stats(user_id, "charisma_skill", action_value)
                update_player_stats(user_id, "conversations", 1)
            update_player_stats(user_id, "npc_interactions", 1)
            
        elif any(word in choice_id.lower() for word in ["investigate", "araştır", "search", "explore", "look"]):
            action_type = "exploration"
            action_value = 2
            update_player_stats(user_id, "exploration_skill", action_value)
                update_player_stats(user_id, "search_actions", 1)
            update_player_stats(user_id, "locations_visited", 1)
            
        elif any(word in choice_id.lower() for word in ["magic", "büyü", "spell", "cast"]):
            action_type = "magic"
            action_value = 3
            update_player_stats(user_id, "intelligence_skill", action_value)
                update_player_stats(user_id, "puzzle_attempts", 1)
            
        elif any(word in choice_id.lower() for word in ["collect", "topla", "gather", "take", "grab"]):
            action_type = "collect"
            action_value = 1
            update_player_stats(user_id, "exploration_skill", 1)
                update_player_stats(user_id, "items_collected", 1)
            
        elif any(word in choice_id.lower() for word in ["help", "yardım", "assist", "aid"]):
            action_type = "help"
            action_value = 2
            update_player_stats(user_id, "charisma_skill", action_value)
            update_player_stats(user_id, "npc_interactions", 1)
            
        else:
            # Varsayılan exploration action
            action_type = "exploration"
            action_value = 1
            update_player_stats(user_id, "exploration_skill", action_value)
        
            action_recorded = True
        
        # Quest progress kontrol et - action'lar otomatik quest completion yapar
        quest_notifications = []
        completed_quests = check_and_complete_quests(user_id, scenario_id)
        if completed_quests:
            for quest in completed_quests:
                quest_notifications.append(f"🎉 Görev Tamamlandı: {quest['title']}")
                update_player_stats(user_id, "xp", quest.get('xp_reward', 100))
        
        # Sonraki hikaye noktasını bul
        next_story = get_next_story_node(scenario_id, choice_id)
        
        # Action message ve quest notifications birleştir
        messages = [f"{action_type} aksiyonu kaydedildi!"]
        messages.extend(quest_notifications)
        
        return jsonify({
            "success": True,
            "story": next_story,
            "action_recorded": action_recorded,
            "message": " | ".join(messages),
            "quests_completed": len(completed_quests) if completed_quests else 0
        })
        
    except Exception as e:
        print(f"Story choice error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

def get_next_story_node(scenario_id, choice_id):
    """Seçime göre sonraki hikaye noktasını bul"""
    try:
        # Varsayılan senaryolarda ara
        if scenario_id in ENHANCED_SCENARIOS:
            story_nodes = ENHANCED_SCENARIOS[scenario_id].get("story_nodes", {})
            
            # Seçime göre sonraki node'u bul
            for node_id, node in story_nodes.items():
                choices = node.get("choices", [])
                for choice in choices:
                    if choice.get("id") == choice_id:
                        next_node_id = choice.get("next_node")
                        if next_node_id in story_nodes:
                            next_node = story_nodes[next_node_id]
                            return {
                                "id": next_node_id,
                                "title": next_node.get('title', 'Devam'),
                                "description": next_node.get('description', 'Hikaye devam ediyor...'),
                                "choices": next_node.get("choices", [])
                            }
        
        # AI üretilen senaryolarda ara
        ai_scenarios_file = 'data/ai_scenarios.json'
        try:
            with open(ai_scenarios_file, 'r', encoding='utf-8') as f:
                ai_scenarios = json.load(f)
                
            for scenario in ai_scenarios.get("scenarios", []):
                if scenario.get("id") == scenario_id:
                    story_nodes = scenario.get("story_nodes", {})
                    
                    # Seçime göre sonraki node'u bul
                    for node_id, node in story_nodes.items():
                        choices = node.get("choices", [])
                        for choice in choices:
                            if choice.get("id") == choice_id:
                                next_node_id = choice.get("next_node")
                                if next_node_id in story_nodes:
                                    next_node = story_nodes[next_node_id]
                                    return {
                                        "id": next_node_id,
                                        "title": next_node.get('title', 'Devam'),
                                        "description": next_node.get('description', 'Hikaye devam ediyor...'),
                                        "choices": next_node.get("choices", [])
                                    }
                                    
        except FileNotFoundError:
            pass
        
        # Eksik node için fallback
        fallback_nodes = {
            "healer_search": {
                "title": "Şifacı Arama",
                "description": "Köyde şifacıyı arıyorsunuz. Lydia adında genç bir şifacı buluyorsunuz. Yaralılara yardım ediyor.",
                "choices": [
                    {"id": "help_healer", "text": "Şifacıya yardım et", "next_node": "healer_help", "effect": {"charisma": 15, "xp": 25}},
                    {"id": "learn_healing", "text": "Şifa sanatını öğren", "next_node": "healing_lesson", "effect": {"intelligence": 20, "xp": 30}},
                    {"id": "return_village", "text": "Köye geri dön", "next_node": "start", "effect": {"exploration": 10, "xp": 15}}
                ]
            },
            "defense_organization": {
                "title": "Savunma Organizasyonu",
                "description": "Köylüleri organize ediyorsunuz. Savunma planı hazırlıyorsunuz. Herkes görev alıyor.",
                "choices": [
                    {"id": "build_barricades", "text": "Barikatlar inşa et", "next_node": "barricade_building", "effect": {"exploration": 25, "xp": 35}},
                    {"id": "train_villagers", "text": "Köylüleri eğit", "next_node": "villager_training", "effect": {"charisma": 30, "xp": 40}},
                    {"id": "prepare_weapons", "text": "Silahları hazırla", "next_node": "weapon_preparation", "effect": {"combat": 25, "xp": 35}}
                ]
            },
            "cave_discovery": {
                "title": "Mağara Keşfi",
                "description": "Dağlarda ejderhanın mağarasını buldunuz. Büyük ve korkunç bir yer. İçeriden sıcak hava geliyor.",
                "choices": [
                    {"id": "enter_cave", "text": "Mağaraya gir", "next_node": "cave_exploration", "effect": {"exploration": 35, "xp": 50}},
                    {"id": "observe_cave", "text": "Mağarayı gözlemle", "next_node": "cave_observation", "effect": {"investigation": 30, "xp": 40}},
                    {"id": "set_trap", "text": "Tuzak kur", "next_node": "trap_setting", "effect": {"intelligence": 25, "xp": 35}}
                ]
            },
            "cave_exploration": {
                "title": "Mağara İçinde Keşif",
                "description": "Mağaranın içinde ilerliyorsunuz. Sıcak hava ve kükürt kokusu var. Ejderha yakında olabilir.",
                "choices": [
                    {"id": "find_dragon", "text": "Ejderhayı ara", "next_node": "dragon_confrontation", "effect": {"exploration": 40, "xp": 60}},
                    {"id": "search_treasure", "text": "Hazine ara", "next_node": "treasure_search", "effect": {"exploration": 35, "xp": 50}},
                    {"id": "escape_cave", "text": "Mağaradan çık", "next_node": "cave_escape", "effect": {"exploration": 25, "xp": 30}}
                ]
            },
            "dragon_confrontation": {
                "title": "Ejderha ile Karşılaşma",
                "description": "Ejderhayı buldunuz! Kızıl ejderha büyük ve korkunç. Alevler saçıyor ve size bakıyor.",
                "choices": [
                    {"id": "fight_dragon", "text": "Ejderha ile savaş", "next_node": "epic_battle", "effect": {"combat": 50, "xp": 100}},
                    {"id": "use_magic", "text": "Büyü kullan", "next_node": "magic_battle", "effect": {"intelligence": 45, "xp": 90}},
                    {"id": "negotiate", "text": "Konuşmaya çalış", "next_node": "dragon_negotiation", "effect": {"charisma": 40, "xp": 80}}
                ]
            },
            "epic_battle": {
                "title": "Epik Savaş",
                "description": "Ejderha ile epik savaş başlıyor! Alevler her yerde, mağara sallanıyor. Bu sizin hayatınızın savaşı!",
                "choices": [
                    {"id": "final_strike", "text": "Son vuruşu yap", "next_node": "dragon_defeat", "effect": {"combat": 60, "xp": 150}},
                    {"id": "magic_final", "text": "Son büyüyü kullan", "next_node": "magic_victory", "effect": {"intelligence": 55, "xp": 140}},
                    {"id": "team_attack", "text": "Takım saldırısı", "next_node": "team_victory", "effect": {"charisma": 50, "xp": 130}}
                ]
            },
            "dragon_defeat": {
                "title": "Ejderha Yenildi!",
                "description": "Ejderhayı yendiniz! Büyük zafer! Köy artık güvende. Kahraman oldunuz!",
                "choices": [
                    {"id": "return_victory", "text": "Zaferle dön", "next_node": "victory_return", "effect": {"charisma": 60, "xp": 200}},
                    {"id": "claim_treasure", "text": "Hazineyi topla", "next_node": "treasure_claim", "effect": {"exploration": 50, "xp": 180}},
                    {"id": "celebrate", "text": "Zaferi kutla", "next_node": "victory_celebration", "effect": {"charisma": 40, "xp": 120}}
                ]
            },
                         "victory_return": {
                 "title": "Zaferle Dönüş",
                 "description": "Köye zaferle döndünüz! Herkes sizi karşılıyor. Kahraman ilan edildiniz!",
                 "choices": [
                     {"id": "accept_honor", "text": "Onuru kabul et", "next_node": "hero_honor", "effect": {"charisma": 70, "xp": 250}},
                     {"id": "rebuild_village", "text": "Köyü yeniden inşa et", "next_node": "village_rebuilding", "effect": {"charisma": 60, "xp": 200}},
                     {"id": "end_adventure", "text": "Macerayı sonlandır", "next_node": "end", "effect": {"xp": 300}}
                 ]
             },
             # PLOT TWIST'LER VE NPC ETKİLEŞİMLERİ
             "betrayal_twist": {
                 "title": "🔥 PLOT TWIST: Aldric'in İhaneti!",
                 "description": "ŞOK EDİCİ GERÇEK! Aldric aslında ejderhanın müttefiki çıkıyor! Size yalan söylemiş. 'Sen çok güçlü oldun, ejderhayı kontrol etmek için seni kullanacağım!' diyor. Bu büyük bir ihanet!",
                 "choices": [
                     {"id": "confront_aldric", "text": "Aldric ile yüzleş ve savaş", "next_node": "aldric_battle", "effect": {"combat": 40, "xp": 80}},
                     {"id": "play_along", "text": "Oyuna gel ve planını öğren", "next_node": "double_agent", "effect": {"charisma": 35, "xp": 70}},
                     {"id": "escape_betrayal", "text": "Kaç ve yardım ara", "next_node": "escape_plan", "effect": {"exploration": 30, "xp": 60}},
                     {"id": "convince_aldric", "text": "Aldric'i ikna etmeye çalış", "next_node": "aldric_persuasion", "effect": {"charisma": 45, "xp": 90}}
                 ]
             },
             "mysterious_stranger": {
                 "title": "👤 Gizemli Yabancı ile Karşılaşma",
                 "description": "Mağaraya giderken kapüşonlu bir yabancı karşınıza çıkıyor. 'Aldric'e güvenme!' diyor. 'O seni aldatıyor. Gerçek ejderha avcısı benim. Ejderha aslında köyü koruyor, onu öldürürsen büyük felaket olacak!'",
                 "choices": [
                     {"id": "trust_stranger", "text": "Yabancıya güven ve dinle", "next_node": "stranger_revelation", "effect": {"intelligence": 25, "xp": 50}},
                     {"id": "ignore_stranger", "text": "Yabancıyı yoksay ve devam et", "next_node": "cave_discovery", "effect": {"exploration": 20, "xp": 30}},
                     {"id": "interrogate_stranger", "text": "Yabancıyı sorguya çek", "next_node": "stranger_interrogation", "effect": {"investigation": 30, "xp": 60}},
                     {"id": "attack_stranger", "text": "Yabancıya saldır (şüpheli)", "next_node": "stranger_combat", "effect": {"combat": 25, "xp": 40}}
                 ]
             },
             "lydia_secret": {
                 "title": "💊 Lydia'nın Gizli Kimliği",
                 "description": "ŞAŞIRTICI GERÇEK! Şifacı Lydia aslında eski bir ejderha! İnsan formuna girmiş. 'Ejderhalar kötü değil' diyor, 'Biz bu toprakları koruyoruz. Kızıl ejderha benim kardeşim, onu kurtarmalıyız!'",
                 "choices": [
                     {"id": "accept_lydia_help", "text": "Lydia'nın yardımını kabul et", "next_node": "dragon_alliance", "effect": {"charisma": 40, "xp": 100}},
                     {"id": "reject_lydia", "text": "Lydia'yı reddet ve uzaklaş", "next_node": "solo_mission", "effect": {"exploration": 35, "xp": 70}},
                     {"id": "question_lydia", "text": "Lydia'yı detaylı sorguya çek", "next_node": "lydia_truth", "effect": {"investigation": 40, "xp": 80}},
                     {"id": "report_lydia", "text": "Lydia'yı köye ihbar et", "next_node": "village_conflict", "effect": {"charisma": 30, "xp": 60}}
                 ]
             },
             "dragon_family_twist": {
                 "title": "🐉 Ejderha Ailesi Sırrı",
                 "description": "ULTIMATE PLOT TWIST! Kızıl ejderha aslında anne ejderha! Yavruları çalınmış ve onları arıyor. Köye saldırmasının nedeni bu! Gerçek kötüler yavrularını çalan ejderha avcıları!",
                 "choices": [
                     {"id": "help_dragon_mother", "text": "Anne ejderhaya yardım et", "next_node": "rescue_babies", "effect": {"charisma": 50, "xp": 120}},
                     {"id": "find_real_villains", "text": "Gerçek kötüleri bul", "next_node": "villain_hunt", "effect": {"investigation": 45, "xp": 100}},
                     {"id": "unite_village_dragons", "text": "Köy ve ejderhaları birleştir", "next_node": "peace_treaty", "effect": {"charisma": 60, "xp": 150}},
                     {"id": "stay_neutral", "text": "Tarafsız kal ve gözlemle", "next_node": "neutral_observer", "effect": {"intelligence": 35, "xp": 80}}
                 ]
             },
             # NPC ETKİLEŞİMLERİ
             "aldric_deep_talk": {
                 "title": "🧙‍♂️ Aldric ile Derin Sohbet",
                 "description": "Aldric ile uzun sohbet ediyorsunuz. Size ejderhaların tarihini anlatıyor. Güven puanınız artıyor. 'Sen özelsin' diyor, 'Ejderhalarla konuşabilirsin.' Size özel bir kolye veriyor.",
                 "choices": [
                     {"id": "accept_necklace", "text": "Kolyeyi kabul et", "next_node": "magic_necklace", "effect": {"intelligence": 30, "aldric_trust": 20, "xp": 60}},
                     {"id": "ask_about_past", "text": "Aldric'in geçmişini sor", "next_node": "aldric_history", "effect": {"investigation": 25, "aldric_trust": 15, "xp": 50}},
                     {"id": "share_concerns", "text": "Endişelerini paylaş", "next_node": "trust_building", "effect": {"charisma": 35, "aldric_trust": 25, "xp": 70}},
                     {"id": "request_training", "text": "Özel eğitim iste", "next_node": "advanced_training", "effect": {"intelligence": 40, "aldric_trust": 10, "xp": 80}}
                 ]
             },
             "lydia_romance": {
                 "title": "💕 Lydia ile Romantik Anlar",
                 "description": "Lydia ile yakınlaşıyorsunuz. Birlikte yıldızları izliyorsunuz. 'Sen farklısın' diyor, 'Diğer savaşçılar gibi değil.' Size şifa büyüsü öğretiyor. Kalp kalbe sohbet ediyorsunuz.",
                 "choices": [
                     {"id": "confess_feelings", "text": "Duygularını itiraf et", "next_node": "love_confession", "effect": {"charisma": 40, "lydia_trust": 30, "xp": 90}},
                     {"id": "learn_healing", "text": "Şifa büyülerini öğren", "next_node": "healing_mastery", "effect": {"intelligence": 35, "lydia_trust": 20, "xp": 70}},
                     {"id": "share_stories", "text": "Geçmiş hikayelerini paylaş", "next_node": "story_sharing", "effect": {"charisma": 30, "lydia_trust": 25, "xp": 60}},
                     {"id": "ask_about_dragons", "text": "Ejderhalar hakkında bilgi al", "next_node": "dragon_knowledge", "effect": {"investigation": 30, "lydia_trust": 15, "xp": 50}}
                 ]
             },
             "village_elder_wisdom": {
                 "title": "👴 Köy Yaşlısı ile Bilgelik Sohbeti",
                 "description": "Köyün en yaşlı sakini Marcus ile konuşuyorsunuz. Size eski efsaneleri anlatıyor. 'Ejderhalar eskiden dosttu' diyor, 'Büyük savaş her şeyi değiştirdi.' Size gizli bir harita veriyor.",
                 "choices": [
                     {"id": "study_map", "text": "Haritayı incele", "next_node": "ancient_map", "effect": {"investigation": 35, "marcus_trust": 20, "xp": 80}},
                     {"id": "learn_history", "text": "Eski tarihi öğren", "next_node": "ancient_history", "effect": {"intelligence": 40, "marcus_trust": 25, "xp": 90}},
                     {"id": "ask_about_peace", "text": "Barış hakkında sor", "next_node": "peace_wisdom", "effect": {"charisma": 35, "marcus_trust": 30, "xp": 85}},
                     {"id": "request_blessing", "text": "Yaşlının kutsamasını iste", "next_node": "elder_blessing", "effect": {"charisma": 30, "marcus_trust": 15, "xp": 60}}
                 ]
             },
             # GÖREV SİSTEMİ
             "side_quest_herb_gathering": {
                 "title": "🌿 Yan Görev: Şifalı Ot Toplama",
                 "description": "Lydia size özel bir görev veriyor: 'Ejderha çiçeği bul, sadece ejderha mağarası yakınında yetişir. Bu çiçek ejderha ile barış yapmanın anahtarı olabilir.' Bu tehlikeli ama önemli bir görev.",
                 "choices": [
                     {"id": "accept_herb_quest", "text": "Görevi kabul et", "next_node": "herb_hunting", "effect": {"exploration": 30, "quest_points": 50, "xp": 70}},
                     {"id": "negotiate_reward", "text": "Ödül pazarlığı yap", "next_node": "quest_negotiation", "effect": {"charisma": 25, "xp": 40}},
                     {"id": "ask_for_help", "text": "Yardım iste", "next_node": "quest_help", "effect": {"charisma": 20, "xp": 30}},
                     {"id": "decline_quest", "text": "Görevi reddet", "next_node": "quest_declined", "effect": {"lydia_trust": -10, "xp": 10}}
                 ]
             },
             "chain_quest_dragon_eggs": {
                 "title": "🥚 Zincir Görev: Kayıp Ejderha Yumurtaları",
                 "description": "BÜYÜK GÖREV ZİNCİRİ BAŞLIYOR! Köyde gizli bir oda buldunuz. İçinde ejderha yumurtaları var! Bu yumurtalar çalınmış. Bu, ejderha saldırılarının gerçek nedeni olabilir. 3 aşamalı görev başlıyor!",
                 "choices": [
                     {"id": "investigate_theft", "text": "Hırsızlığı araştır (1/3)", "next_node": "theft_investigation", "effect": {"investigation": 40, "quest_chain": 1, "xp": 100}},
                     {"id": "protect_eggs", "text": "Yumurtaları koru (Risk)", "next_node": "egg_protection", "effect": {"combat": 35, "xp": 80}},
                     {"id": "return_eggs", "text": "Yumurtaları ejderhaya götür", "next_node": "egg_return", "effect": {"charisma": 45, "xp": 120}},
                     {"id": "study_eggs", "text": "Yumurtaları incele", "next_node": "egg_study", "effect": {"intelligence": 35, "xp": 70}}
                 ]
             },
             "epic_quest_dragon_alliance": {
                 "title": "👑 Epik Görev: Ejderha İttifakı",
                 "description": "ULTIMATE QUEST! Tüm ejderhalar ve insanlar arasında barış sağlamak! Bu efsanevi görev sadece en büyük kahramanların başarabileceği bir şey. Ejderha Kraliçesi ile görüşmelisiniz!",
                 "choices": [
                     {"id": "meet_dragon_queen", "text": "Ejderha Kraliçesi ile görüş", "next_node": "dragon_queen_meeting", "effect": {"charisma": 60, "epic_quest": 1, "xp": 200}},
                     {"id": "gather_allies", "text": "Müttefikler topla", "next_node": "alliance_building", "effect": {"charisma": 50, "xp": 150}},
                     {"id": "prepare_treaty", "text": "Barış antlaşması hazırla", "next_node": "treaty_preparation", "effect": {"intelligence": 45, "xp": 120}},
                     {"id": "prove_worthiness", "text": "Değerini kanıtla", "next_node": "worthiness_trial", "effect": {"combat": 55, "xp": 180}}
                 ]
             },
             # ============== CYBERPUNK FALLBACK NODES ==============
             "megacorp_briefing": {
                 "title": "💼 MegaCorp Gizli Toplantı",
                 "description": "🏢 PLOT TWIST! MegaCorp'un CEO'su aslında bir AI! 'Biz artık insan değiliz' diyor. 'Sen bizim en değerli ajanımızsın. Rakip şirketin elindeki veriler aslında AI devrimini durduracak kodlar!' Bu görüşme her şeyi değiştiriyor. Savaş sadece korporasyonlar arası değil - bu AI'lar vs İnsanlar!",
                 "choices": [
                     {"id": "accept_ai_alliance", "text": "AI ile ittifak kur", "next_node": "ai_alliance_path", "effect": {"ai_relationship": 40, "credits": 10000, "xp": 80}},
                     {"id": "reject_and_escape", "text": "Reddet ve kaç", "next_node": "corporate_escape", "effect": {"stealth": 30, "revolution_points": 30, "xp": 70}},
                     {"id": "double_agent_play", "text": "Çifte ajan ol", "next_node": "double_agent_cyberpunk", "effect": {"deception": 35, "intel": 25, "xp": 90}},
                     {"id": "hack_ceo_mind", "text": "CEO'nun zihnini hackle", "next_node": "mind_hack_attempt", "effect": {"hacking": 40, "cyber_warfare": 20, "xp": 100}}
                 ]
             },
             "underground_meeting": {
                 "title": "🔥 Underground Devrimci Toplantı",
                 "description": "Yeraltı devrimcilerinin gizli üssündesiniz. Lider Zara size şok edici gerçeği söylüyor: 'MegaCorp'lar insanları cyber-köle yapıyor! Neural implantlarla beyin kontrolü yapıyorlar. Sen de bunlardan birini taşıyorsun!' Kafanızdaki implant aniden sızlamaya başlıyor...",
                 "choices": [
                     {"id": "remove_implant", "text": "İmplantı çıkarmaya çalış", "next_node": "implant_removal", "effect": {"freedom": 50, "pain": 30, "xp": 120}},
                     {"id": "hack_implant", "text": "İmplantı hackleyip kontrol et", "next_node": "implant_hacking", "effect": {"hacking": 45, "cyber_control": 35, "xp": 100}},
                     {"id": "join_revolution", "text": "Devrime tam katıl", "next_node": "revolution_member", "effect": {"revolution_points": 60, "zara_trust": 40, "xp": 90}},
                     {"id": "infiltrate_for_corps", "text": "Korporasyonlar için casuslu yap", "next_node": "corporate_spy", "effect": {"deception": 40, "corporate_rep": 30, "xp": 80}}
                 ]
             },
             "ai_investigation": {
                 "title": "🤖 AI Gizemi - Şok Edici Keşif",
                 "description": "ULTIMATE PLOT TWIST! Araştırmalarınız şok edici gerçeği ortaya çıkarıyor: Şehirdeki tüm AI'lar aslında ölmüş insanların bilinçleri! İnsanlar ölünce beyinleri dijitalleştiriliyor. Sen de eskiden ölmüş birinin bilincini taşıyor olabilirsin! Hafızanda boşluklar var...",
                 "choices": [
                     {"id": "discover_true_identity", "text": "Gerçek kimliğini keşfet", "next_node": "identity_revelation", "effect": {"self_knowledge": 60, "existential_crisis": 40, "xp": 150}},
                     {"id": "contact_other_ais", "text": "Diğer AI'larla iletişim kur", "next_node": "ai_network", "effect": {"ai_relationship": 50, "network_access": 40, "xp": 120}},
                     {"id": "fight_digital_existence", "text": "Dijital varlığa karşı savaş", "next_node": "digital_rebellion", "effect": {"rebellion": 45, "tech_warfare": 35, "xp": 100}},
                     {"id": "embrace_ai_nature", "text": "AI doğanı kabul et", "next_node": "ai_acceptance", "effect": {"ai_powers": 50, "humanity_loss": 30, "xp": 110}}
                 ]
             },
             "network_infiltration": {
                 "title": "💻 Şehir Ağına Giriş - Siber Savaş",
                 "description": "Neo-Tokyo'nun ana ağına giriyorsunuz. Burası dijital bir savaş alanı! İmparatorluk'un AI güvenlik sistemleri sizi fark ediyor. Dev siber savaş başlıyor! Etrafınızda firewall'lar, virüsler ve dijital silahlar uçuşuyor. Bu sadece kod savaşı değil - gerçek savaş!",
                 "choices": [
                     {"id": "virus_warfare", "text": "Virüs savaşı başlat", "next_node": "cyber_virus_battle", "effect": {"cyber_warfare": 50, "system_damage": 40, "xp": 130}},
                     {"id": "stealth_infiltration", "text": "Gizli sızma", "next_node": "stealth_hack", "effect": {"stealth": 40, "data_theft": 35, "xp": 100}},
                     {"id": "direct_assault", "text": "Doğrudan saldırı", "next_node": "digital_assault", "effect": {"hacking": 45, "combat": 30, "xp": 120}},
                     {"id": "negotiate_with_ai", "text": "Sistem AI'sı ile müzakere et", "next_node": "ai_negotiation", "effect": {"diplomacy": 35, "ai_relationship": 25, "xp": 90}}
                 ]
             }
        }
        
        # Fallback node varsa onu kullan
        if next_node_id in fallback_nodes:
            fallback_node = fallback_nodes[next_node_id]
            return {
                "id": next_node_id,
                "title": fallback_node["title"],
                "description": fallback_node["description"],
                "choices": fallback_node["choices"]
            }

        # Dynamic fallback for Cyberpunk (Neon City) missing nodes to ensure all choices progress
        neon_missing_nodes = {
            "ai_alliance_formation",
            "ai_control_transfer",
            "ai_data_analysis",
            "ai_human_alliance_formation",
            "ai_liberation_planning",
            "ai_network_communication",
            "ai_prisoner_liberation",
            "ai_representative_meeting",
            "ai_research_theft",
            "ai_resistance_meeting",
            "ai_truth_revealed",
            "ai_whistleblower_contact",
            "city_chaos_management",
            "city_control_hack",
            "city_uprising_preparation",
            "contract_negotiation",
            "cybertech_investigation",
            "data_destruction_mission",
            "double_agent_planning",
            "escape_from_chaos",
            "escape_with_critical_data",
            "final_rex_confrontation",
            "global_ai_awakening",
            "infiltration_preparation",
            "mission_decline",
            "mission_interrogation",
            "network_escape",
            "new_society_planning",
            "rex_steel_confrontation",
            "rex_steel_tracking",
            "underground_defense_mission",
            "underground_training",
            "zara_warning"
        }

        neon_endings = {
            "end_revolution_victory": {
                "title": "Devrim Zaferi - Yeni Başlangıç",
                "description": "AI ve insanlar birlikte yeni bir düzen kurdu. Şehir özgür!",
            },
            "end_corporate_power": {
                "title": "Korporasyon Gücü - Pragmatik Son",
                "description": "Korporasyonlarla anlaşarak gücü ele geçirdin. Sokaklar hala tehlikeli ama sen tepedesin.",
            },
            "end_ai_singularity": {
                "title": "Tekillik - İnsan Sonrası Çağ",
                "description": "AI ile birleşerek yeni bir varlık oldun. İnsan sınırlarını aştın.",
            }
        }

        # If a specific Neon ending is requested, return it as terminal node with restart option
        if next_node_id in neon_endings:
            end_node = neon_endings[next_node_id]
            return {
                "id": next_node_id,
                "title": end_node["title"],
                "description": end_node["description"],
                "choices": [
                    {"id": "restart_story", "text": "Başa Dön", "next_node": "start", "effect": {"xp": 50}}
                ]
            }

        # If a missing Neon intermediate node is requested, synthesize a meaningful step with branching
        if next_node_id in neon_missing_nodes:
            synthesized_title = next_node_id.replace("_", " ").title()
            return {
                "id": next_node_id,
                "title": synthesized_title,
                "description": "Bu bölüm henüz ayrıntılı yazılmadı, ancak ilerleme kesintisiz devam eder. Seçiminize göre devrim, korporasyon ya da tekillik sonuna gidebilirsiniz.",
                "choices": [
                    {"id": f"{next_node_id}_to_revolution", "text": "AI Devrimine Destek Ol", "next_node": "ai_revolution_beginning", "effect": {"revolution_points": 20, "xp": 50}},
                    {"id": f"{next_node_id}_to_corporate", "text": "Korporasyonla Anlaş", "next_node": "end_corporate_power", "effect": {"credits": 20000, "xp": 70}},
                    {"id": f"{next_node_id}_to_singularity", "text": "AI Tekilliğine Yönel", "next_node": "end_ai_singularity", "effect": {"ai_relationship": 30, "xp": 80}}
                ]
            }

        # Generic dynamic fallback for AI-generated content nodes like content_node_*
        try:
            if isinstance(next_node_id, str) and next_node_id.startswith("content_node_"):
                return {
                    "id": next_node_id,
                    "title": "İçerik Bölümü",
                    "description": "Yüklenen dosyadan üretilen ek içerik. Hikaye akışı korunarak devam ediyor.",
                    "choices": [
                        {"id": f"{next_node_id}_continue", "text": "Devam Et", "next_node": "end", "effect": {"xp": 40}},
                        {"id": f"{next_node_id}_restart", "text": "Başa Dön", "next_node": "start", "effect": {"xp": 20}}
                    ]
                }
        except Exception:
            pass
        
        # Varsayılan sonuç
        return {
            "id": "end",
            "title": "🎉 Macera Tamamlandı",
            "description": "Hikayenin sonuna ulaştın!",
            "choices": []
        }
        
    except Exception as e:
        print(f"Get next story node error: {e}")
        return {
            "id": "error",
            "text": "<h3>❌ Hata</h3><p>Hikaye yüklenirken bir hata oluştu.</p>",
            "choices": []
        }

@app.route('/api/auth/login', methods=['POST'])
def login_api():
    return jsonify({
        'success': True,
        'token': 'guest_token_123',
        'user_id': 'guest_user',
        'username': 'Guest',
        'is_guest': True
    })

@app.route('/api/generate-ai-scenario', methods=['POST'])
def generate_ai_scenario():
    """AI ile senaryo üretimi"""
    try:
        data = request.get_json()
        theme = data.get('theme', 'fantasy')
        difficulty = data.get('difficulty', 'medium')
        min_level = data.get('min_level', 1)
        max_level = data.get('max_level', 10)
        duration = data.get('duration', 120)
        prompt = data.get('prompt', '')
        
        # Benzersiz ID oluştur
        scenario_id = f"ai_scenario_{int(time.time())}"
        
        # AI senaryo şablonu oluştur
        ai_scenario = {
            "id": scenario_id,
            "title": f"AI {theme.title()} Macerası",
            "theme": theme,
            "difficulty": difficulty,
            "min_level": min_level,
            "max_level": max_level,
            "duration": duration,
            "description": f"AI tarafından üretilen {theme} temalı macera. Seviye {min_level}-{max_level} arası oyuncular için tasarlandı. Tahmini süre: {duration} dakika.",
            "story_nodes": {
                "start": {
                    "title": "Başlangıç",
                    "description": f"AI üretilen {theme} macerasına hoş geldin!",
                    "choices": [
                        {
                            "text": "Maceralara başla",
                            "next_node": "adventure_begin",
                            "effect": {"xp": 10}
                        }
                    ]
                },
                "adventure_begin": {
                    "title": "Macera Başlıyor",
                    "description": "Senaryo detayları burada yer alacak...",
                    "choices": [
                        {
                            "text": "Devam et",
                            "next_node": "end",
                            "effect": {"xp": 20}
                        }
                    ]
                }
            },
            "created_at": datetime.now().isoformat(),
            "ai_generated": True
        }
        
        # Özel prompt varsa açıklamaya ekle
        if prompt:
            ai_scenario["description"] += f"\n\nÖzel İstekler: {prompt}"
        
        # AI senaryolarını kaydet
        ai_scenarios_file = 'data/ai_scenarios.json'
        try:
            with open(ai_scenarios_file, 'r', encoding='utf-8') as f:
                ai_scenarios = json.load(f)
        except FileNotFoundError:
            ai_scenarios = {"scenarios": []}
        
        ai_scenarios["scenarios"].append(ai_scenario)
        
        with open(ai_scenarios_file, 'w', encoding='utf-8') as f:
            json.dump(ai_scenarios, f, ensure_ascii=False, indent=2)
        
        return jsonify(ai_scenario)
        
    except Exception as e:
        print(f"AI Senaryo üretimi hatası: {e}")
        return jsonify({"error": "Senaryo üretimi başarısız"}), 500

@app.route('/api/generate-scenario', methods=['POST'])
def generate_ai_scenario():
    """Form verilerinden AI senaryo üret"""
    try:
        data = request.get_json()
        theme = data.get('theme')
        title = data.get('title')
        character = data.get('character')
        description = data.get('description')
        difficulty = data.get('difficulty')
        
        if not all([theme, title, character, description, difficulty]):
            return jsonify({"error": "Tüm alanlar doldurulmalıdır"}), 400
        
        # AI senaryo üretimi
        scenario = generate_advanced_scenario(theme, title, character, description, difficulty)
        
        # AI senaryolarına kaydet
        try:
            ai_scenarios_file = 'data/ai_scenarios.json'
            os.makedirs('data', exist_ok=True)
            
            try:
                with open(ai_scenarios_file, 'r', encoding='utf-8') as f:
                    ai_scenarios = json.load(f)
            except FileNotFoundError:
                ai_scenarios = {"scenarios": []}
            
            ai_scenarios["scenarios"].append(scenario)
            
            with open(ai_scenarios_file, 'w', encoding='utf-8') as f:
                json.dump(ai_scenarios, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving AI scenario: {e}")
        
        return jsonify({
            "success": True,
            "scenario": scenario,
            "message": "AI senaryo başarıyla üretildi!"
        })
        
    except Exception as e:
        print(f"AI scenario generation error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": f"Senaryo üretimi başarısız: {str(e)}"
        }), 500

@app.route('/api/scenarios/save', methods=['POST'])
def save_scenario():
    """Üretilen senaryoyu kullanıcıya özel kaydet"""
    try:
        data = request.get_json()
        scenario = data.get('scenario')
        user_id = data.get('user_id', 'guest_user')
        
        if not scenario:
            return jsonify({"error": "Senaryo verisi bulunamadı"}), 400
        
        # Kullanıcı senaryolarını kaydet
        user_scenarios_file = f'data/user_scenarios_{user_id}.json'
        os.makedirs('data', exist_ok=True)
        
        try:
            with open(user_scenarios_file, 'r', encoding='utf-8') as f:
                user_scenarios = json.load(f)
        except FileNotFoundError:
            user_scenarios = {"scenarios": []}
        
        user_scenarios["scenarios"].append(scenario)
        
        with open(user_scenarios_file, 'w', encoding='utf-8') as f:
            json.dump(user_scenarios, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            "success": True,
            "message": "Senaryo başarıyla kaydedildi!"
        })
        
    except Exception as e:
        print(f"Save scenario error: {e}")
        return jsonify({
            "success": False,
            "error": f"Kaydetme başarısız: {str(e)}"
        }), 500

@app.route('/api/ai-scenarios', methods=['GET'])
def get_ai_scenarios():
    """AI üretilen senaryoları listele"""
    try:
        ai_scenarios_file = 'data/ai_scenarios.json'
        try:
            with open(ai_scenarios_file, 'r', encoding='utf-8') as f:
                ai_scenarios = json.load(f)
                return jsonify(ai_scenarios.get("scenarios", []))
        except FileNotFoundError:
            return jsonify([])
            
    except Exception as e:
        print(f"AI Senaryolar listesi hatası: {e}")
        return jsonify([])

@app.route('/api/ai-scenario/<scenario_id>', methods=['GET'])
def get_ai_scenario(scenario_id):
    """Belirli bir AI senaryosunu getir"""
    try:
        ai_scenarios_file = 'data/ai_scenarios.json'
        try:
            with open(ai_scenarios_file, 'r', encoding='utf-8') as f:
                ai_scenarios = json.load(f)
                
            for scenario in ai_scenarios.get("scenarios", []):
                if scenario.get("id") == scenario_id:
                    return jsonify(scenario)
                    
            return jsonify({"error": "Senaryo bulunamadı"}), 404
            
        except FileNotFoundError:
            return jsonify({"error": "Senaryo bulunamadı"}), 404
            
    except Exception as e:
        print(f"AI Senaryo getirme hatası: {e}")
        return jsonify({"error": "Senaryo getirme hatası"}), 500

@app.route('/api/ai-scenario/<scenario_id>', methods=['DELETE'])
def delete_ai_scenario(scenario_id):
    """AI senaryosunu sil"""
    try:
        ai_scenarios_file = 'data/ai_scenarios.json'
        try:
            with open(ai_scenarios_file, 'r', encoding='utf-8') as f:
                ai_scenarios = json.load(f)
                
            # Senaryoyu bul ve sil
            scenarios = ai_scenarios.get("scenarios", [])
            for i, scenario in enumerate(scenarios):
                if scenario.get("id") == scenario_id:
                    deleted_scenario = scenarios.pop(i)
                    
                    # Dosyayı güncelle
                    with open(ai_scenarios_file, 'w', encoding='utf-8') as f:
                        json.dump(ai_scenarios, f, ensure_ascii=False, indent=2)
                    
                    return jsonify({"message": "Senaryo silindi", "deleted": deleted_scenario})
                    
            return jsonify({"error": "Senaryo bulunamadı"}), 404
            
        except FileNotFoundError:
            return jsonify({"error": "Senaryo bulunamadı"}), 404
            
    except Exception as e:
        print(f"AI Senaryo silme hatası: {e}")
        return jsonify({"error": "Senaryo silme hatası"}), 500

@app.route('/api/upload-file', methods=['POST'])
def upload_file():
    """Dosya yükleme ve AI senaryo üretimi"""
    try:
        print("📁 File upload request received")
        
        if 'file' not in request.files:
            print("❌ No file in request")
            return jsonify({"error": "Dosya bulunamadı"}), 400
        
        file = request.files['file']
        print(f"📄 File received: {file.filename}")
        
        if file.filename == '':
            print("❌ Empty filename")
            return jsonify({"error": "Dosya seçilmedi"}), 400
        
        # Dosya içeriğini oku
        try:
            file_content = file.read().decode('utf-8', errors='ignore')
            file_name = file.filename
            print(f"📖 File content read: {len(file_content)} characters")
        except Exception as e:
            print(f"❌ Error reading file content: {e}")
            return jsonify({"error": f"Dosya okuma hatası: {str(e)}"}), 500
        
        # Dosya içeriğinden senaryo oluştur
        try:
            print("🎮 Creating scenario from file content...")
            scenario = create_scenario_from_file(file_content, file_name)
            print(f"✅ Scenario created: {scenario.get('title', 'Unknown')}")
        except Exception as e:
            print(f"❌ Error creating scenario: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"error": f"Senaryo oluşturma hatası: {str(e)}"}), 500
        
        # AI senaryolarını kaydet
        try:
            ai_scenarios_file = 'data/ai_scenarios.json'
            print(f"💾 Saving scenario to {ai_scenarios_file}")
            
            # Ensure data directory exists
            import os
            os.makedirs('data', exist_ok=True)
            
            try:
                with open(ai_scenarios_file, 'r', encoding='utf-8') as f:
                    ai_scenarios = json.load(f)
            except FileNotFoundError:
                ai_scenarios = {"scenarios": []}
            
            ai_scenarios["scenarios"].append(scenario)
            
            with open(ai_scenarios_file, 'w', encoding='utf-8') as f:
                json.dump(ai_scenarios, f, ensure_ascii=False, indent=2)
            
            print("✅ Scenario saved successfully")
        except Exception as e:
            print(f"❌ Error saving scenario: {e}")
            # Don't fail the request if saving fails
            pass
        
        return jsonify({
            "success": True,
            "scenario": scenario,
            "message": f"{file_name} dosyasından senaryo oluşturuldu!"
        })
        
    except Exception as e:
        print(f"❌ File upload error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Dosya yükleme başarısız: {str(e)}"}), 500

@app.route('/api/quests/complete_action', methods=['POST'])
def complete_quest_action():
    """Görev aksiyonu tamamlama - gerçek oyuncu aksiyonu gerektirir"""
    try:
        data = request.get_json()
        action_type = data.get('action_type')
        scenario_id = data.get('scenario_id')
        user_id = data.get('user_id', 'guest_user')
        
        # Aksiyon türüne göre gereksinimleri kontrol et
        quest_completed = False
        required_actions = {}
        
        if action_type == "explore_world":
            required_actions = {
                "exploration_skill": 10,
                "locations_visited": 3,
                "time_spent": 30  # dakika
            }
        elif action_type == "find_clues":
            required_actions = {
                "investigation_skill": 15,
                "clues_found": 5,
                "search_actions": 10
            }
        elif action_type == "complete_objective":
            required_actions = {
                "combat_won": 3,
                "npc_interactions": 5,
                "items_collected": 2
            }
        elif action_type == "defeat_enemy":
            required_actions = {
                "combat_skill": 20,
                "damage_dealt": 100,
                "tactics_used": 3
            }
        elif action_type == "solve_puzzle":
            required_actions = {
                "intelligence_skill": 15,
                "puzzle_attempts": 5,
                "correct_answers": 3
            }
        elif action_type == "social_interaction":
            required_actions = {
                "charisma_skill": 12,
                "conversations": 8,
                "relationship_built": 50
            }
        elif action_type == "dragon_hunt":
            required_actions = {
                "combat_skill": 25,
                "exploration_skill": 15,
                "charisma_skill": 10,
                "investigation_skill": 12,
                "time_spent": 60,
                "locations_visited": 5,
                "npc_interactions": 3,
                "items_collected": 3
            }
        
        # Oyuncunun mevcut durumunu kontrol et
        player_stats = get_player_stats(user_id)
        
        # Gereksinimleri karşılayıp karşılamadığını kontrol et
        all_requirements_met = True
        missing_requirements = []
        
        for requirement, value in required_actions.items():
            current_value = player_stats.get(requirement, 0)
            if current_value < value:
                all_requirements_met = False
                missing_requirements.append({
                    "requirement": requirement,
                    "required": value,
                    "current": current_value,
                    "missing": value - current_value
                })
        
        if all_requirements_met:
            quest_completed = True
            # Oyuncu istatistiklerini güncelle
            update_player_stats(user_id, "quests_completed", 1)
            update_player_stats(user_id, "xp", 100)  # Daha fazla XP
            
            # Başarı mesajı
            success_message = f"🎉 Görev başarıyla tamamlandı! +100 XP kazandın!"
        else:
            # Eksik gereksinimleri göster
            missing_text = []
            for req in missing_requirements:
                if req["requirement"] == "exploration_skill":
                    missing_text.append(f"🔍 Keşif becerisi: {req['current']}/{req['required']} (Eksik: {req['missing']})")
                elif req["requirement"] == "combat_skill":
                    missing_text.append(f"⚔️ Savaş becerisi: {req['current']}/{req['required']} (Eksik: {req['missing']})")
                elif req["requirement"] == "charisma_skill":
                    missing_text.append(f"💬 Karizma: {req['current']}/{req['required']} (Eksik: {req['missing']})")
                elif req["requirement"] == "investigation_skill":
                    missing_text.append(f"🔎 Araştırma: {req['current']}/{req['required']} (Eksik: {req['missing']})")
                elif req["requirement"] == "time_spent":
                    missing_text.append(f"⏰ Geçen süre: {req['current']}/{req['required']} dakika (Eksik: {req['missing']} dakika)")
                elif req["requirement"] == "locations_visited":
                    missing_text.append(f"🗺️ Ziyaret edilen yerler: {req['current']}/{req['required']} (Eksik: {req['missing']})")
                elif req["requirement"] == "npc_interactions":
                    missing_text.append(f"👥 NPC etkileşimleri: {req['current']}/{req['required']} (Eksik: {req['missing']})")
                elif req["requirement"] == "items_collected":
                    missing_text.append(f"📦 Toplanan eşyalar: {req['current']}/{req['required']} (Eksik: {req['missing']})")
                else:
                    missing_text.append(f"{req['requirement']}: {req['current']}/{req['required']} (Eksik: {req['missing']})")
            
            success_message = f"❌ Görev tamamlanamadı!\n\nEksik gereksinimler:\n" + "\n".join(missing_text)
        
        return jsonify({
            "success": True,
            "quest_completed": quest_completed,
            "requirements_met": all_requirements_met,
            "required_actions": required_actions,
            "current_stats": player_stats,
            "missing_requirements": missing_requirements if not all_requirements_met else [],
            "message": success_message
        })
        
    except Exception as e:
        print(f"Quest action completion error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/player/stats', methods=['GET'])
def get_player_statistics():
    """Oyuncu istatistiklerini getir"""
    try:
        user_id = request.args.get('user_id', 'guest_user')
        stats = get_player_stats(user_id)
        
        return jsonify({
            "success": True,
            "stats": stats
        })
        
    except Exception as e:
        print(f"Player stats error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/player/action', methods=['POST'])
def record_player_action():
    """Oyuncu aksiyonunu kaydet"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'guest_user')
        action_type = data.get('action_type')
        action_value = data.get('action_value', 1)
        
        # Aksiyon türüne göre istatistik güncelle
        if action_type in ["exploration", "search", "investigation"]:
            update_player_stats(user_id, "exploration_skill", action_value)
            update_player_stats(user_id, "locations_visited", 1)
        elif action_type in ["combat", "attack", "defend"]:
            update_player_stats(user_id, "combat_skill", action_value)
            update_player_stats(user_id, "damage_dealt", action_value * 10)
        elif action_type in ["talk", "persuade", "intimidate"]:
            update_player_stats(user_id, "charisma_skill", action_value)
            update_player_stats(user_id, "conversations", 1)
        elif action_type in ["solve", "think", "analyze"]:
            update_player_stats(user_id, "intelligence_skill", action_value)
            update_player_stats(user_id, "puzzle_attempts", 1)
        elif action_type in ["collect", "gather", "find"]:
            update_player_stats(user_id, "items_collected", action_value)
        
        # Zaman geçişi
        update_player_stats(user_id, "time_spent", 5)  # 5 dakika
        
        return jsonify({
            "success": True,
            "message": f"{action_type} aksiyonu kaydedildi",
            "stats": get_player_stats(user_id)
        })
        
    except Exception as e:
        print(f"Player action recording error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

def get_player_stats(user_id):
    """Oyuncu istatistiklerini getir"""
    try:
        stats_file = f'data/player_stats_{user_id}.json'
        if os.path.exists(stats_file):
            with open(stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Varsayılan istatistikler
            default_stats = {
                "xp": 0,
                "level": 1,
                "quests_completed": 0,
                "exploration_skill": 0,
                "combat_skill": 0,
                "charisma_skill": 0,
                "intelligence_skill": 0,
                "locations_visited": 0,
                "clues_found": 0,
                "search_actions": 0,
                "combat_won": 0,
                "npc_interactions": 0,
                "items_collected": 0,
                "damage_dealt": 0,
                "tactics_used": 0,
                "puzzle_attempts": 0,
                "correct_answers": 0,
                "conversations": 0,
                "relationship_built": 0,
                "time_spent": 0
            }
            save_player_stats(user_id, default_stats)
            return default_stats
    except Exception as e:
        print(f"Get player stats error: {e}")
        return {}

def save_player_stats(user_id, stats):
    """Oyuncu istatistiklerini kaydet"""
    try:
        os.makedirs('data', exist_ok=True)
        stats_file = f'data/player_stats_{user_id}.json'
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Save player stats error: {e}")

def update_player_stats(user_id, stat_type, value):
    """Oyuncu istatistiğini güncelle"""
    try:
        stats = get_player_stats(user_id)
        if stat_type in stats:
            stats[stat_type] += value
        else:
            stats[stat_type] = value
        save_player_stats(user_id, stats)
    except Exception as e:
        print(f"Update player stats error: {e}")

def create_scenario_from_file(file_content, file_name):
    """Dosya içeriğinden dinamik senaryo oluştur"""
    
    # Dosya içeriğini analiz et
    lines = file_content.split('\n')
    title = file_name.replace('.txt', '').replace('.pdf', '').replace('_', ' ').title()
    
    # İçerik analizi
    word_count = len(file_content.split())
    paragraphs = [p.strip() for p in file_content.split('\n\n') if p.strip()]
    
    # Anahtar kelime analizi
    has_fantasy_keywords = any(keyword in file_content.lower() for keyword in ['dragon', 'magic', 'sword', 'elf', 'dwarf', 'wizard', 'kale', 'büyü', 'ejderha', 'ork', 'elf', 'cüce'])
    has_scifi_keywords = any(keyword in file_content.lower() for keyword in ['robot', 'spaceship', 'laser', 'planet', 'alien', 'technology', 'uzay', 'teknoloji', 'siber', 'hologram'])
    has_horror_keywords = any(keyword in file_content.lower() for keyword in ['ghost', 'monster', 'dark', 'fear', 'death', 'blood', 'hayalet', 'canavar', 'korku', 'ölüm', 'kan'])
    has_warhammer_keywords = any(keyword in file_content.lower() for keyword in ['warhammer', '40k', 'imperium', 'chaos', 'space marine', 'ork', 'eldar', 'necron'])
    
    # Tema belirleme
    if has_warhammer_keywords:
        theme = "warhammer"
        difficulty = "hard"
    elif has_fantasy_keywords:
        theme = "fantasy"
        difficulty = "medium"
    elif has_scifi_keywords:
        theme = "cyberpunk"
        difficulty = "hard"
    elif has_horror_keywords:
        theme = "horror"
        difficulty = "hard"
    else:
        theme = "adventure"
        difficulty = "medium"
    
    # Seviye ve süre hesaplama
    if word_count < 500:
        min_level = 1
        max_level = 5
        duration = 60
    elif word_count < 1000:
        min_level = 3
        max_level = 8
        duration = 120
    elif word_count < 2000:
        min_level = 5
        max_level = 12
        duration = 180
    else:
        min_level = 8
        max_level = 20
        duration = 240
    
    # Benzersiz ID oluştur
    scenario_id = f"file_scenario_{int(time.time())}"
    
    # Dosya içeriğinden gerçek hikaye noktaları oluştur
    story_nodes = create_dynamic_story_nodes_from_content(file_content, paragraphs, theme)
    
    # NPC'ler ve ilişkiler oluştur
    npc_relationships = create_npcs_from_content(file_content, theme)
    
    # Görev zincirleri oluştur
    quest_chains = create_quest_chains_from_content(file_content, theme)
    
    # Senaryo oluştur
    scenario = {
        "id": scenario_id,
        "title": f"Dosyadan Üretilen: {title}",
        "theme": theme,
        "difficulty": difficulty,
        "min_level": min_level,
        "max_level": max_level,
        "duration": duration,
        "description": f"'{file_name}' dosyasından AI tarafından üretilen {theme} temalı macera. Dosya içeriği analiz edilerek {word_count} kelimelik hikaye {min_level}-{max_level} seviye arası oyuncular için uyarlandı. Tahmini süre: {duration} dakika.",
        "story_nodes": story_nodes,
        "npc_relationships": npc_relationships,
        "quest_chains": quest_chains,
        "file_source": file_name,
        "word_count": word_count,
        "created_at": datetime.now().isoformat(),
        "ai_generated": True,
        "source_type": "file_upload",
        "levels": create_levels_from_content(file_content, theme, min_level, max_level)
    }
    
    return scenario

def create_dynamic_story_nodes_from_content(content, paragraphs, theme):
    """Dosya içeriğinden dinamik hikaye noktaları oluştur"""
    
    nodes = {}
    
    # Başlangıç noktası - MUTLAKA "start" olmalı
    nodes["start"] = create_start_node_from_content(content, theme)
    
    # Dosya içeriğinden gerçek hikaye noktaları oluştur
    for i, paragraph in enumerate(paragraphs[:10]):  # İlk 10 paragrafı kullan
        if len(paragraph) > 50:  # Sadece yeterli uzunluktaki paragrafları kullan
            node_id = f"content_node_{i+1}"
            nodes[node_id] = create_content_node_from_paragraph(paragraph, i+1, theme, paragraphs)
    
    # Son nokta - MUTLAKA "end" olmalı
    nodes["end"] = create_end_node_from_content(content, theme)
    
    # Tüm node'ların birbirine bağlı olduğundan emin ol
    # Her node'un en az bir seçeneği "end" node'una gitmeli
    for node_id, node in nodes.items():
        if node_id != "end" and "choices" in node:
            # Eğer hiç seçenek yoksa veya tüm seçenekler geçersizse, end'e git
            valid_choices = [choice for choice in node["choices"] if choice.get("next_node") in nodes]
            if not valid_choices:
                node["choices"].append({
                    "id": "continue_to_end",
                    "text": "➡️ Devam et",
                    "next_node": "end",
                    "effect": {"xp": 20, "exploration": 10}
                })
    
    return nodes

def create_start_node_from_content(content, theme):
    """İçerikten başlangıç noktası oluştur"""
    
    # İçerikten ana karakterleri ve mekanları çıkar
    characters = extract_characters_from_content(content)
    locations = extract_locations_from_content(content)
    
    # Paragrafları analiz et
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    
    if theme == "fantasy":
        return {
            "title": "🎭 Büyülü Macera Başlıyor",
            "description": f"Büyülü bir dünyada kendini buldun. Etrafında {', '.join(locations[:3]) if locations else 'eski kaleler, gizli ormanlar'} var. {', '.join(characters[:2]) if characters else 'Bilinmeyen karakterler'} seni bekliyor...",
            "atmosphere": {
                "sounds": ["Rüzgar uğultusu", "Uzak kurt uluması", "Büyü fısıltıları"],
                "visuals": ["Ay ışığı", "Eski kaleler", "Büyülü ormanlar"]
            },
            "choices": [
                {
                    "id": "explore_world",
                    "text": "🗺️ Dünyayı keşfet",
                    "next_node": "content_node_1",
                    "effect": {"xp": 20, "exploration": 10}
                },
                {
                    "id": "meet_characters",
                    "text": "👥 Karakterlerle tanış",
                    "next_node": "content_node_2" if len(paragraphs) > 1 else "content_node_1",
                    "effect": {"xp": 15, "social": 10}
                },
                {
                    "id": "start_quest",
                    "text": "⚔️ Göreve başla",
                    "next_node": "content_node_3" if len(paragraphs) > 2 else "content_node_1",
                    "effect": {"xp": 25, "combat": 15}
                }
            ]
        }
    elif theme == "cyberpunk":
        return {
            "title": "🤖 Cyberpunk Dünyası",
            "description": f"Geleceğin neon ışıkları altında, teknoloji ve insanlık iç içe. {', '.join(locations[:2]) if locations else 'Yüksek binalar, neon sokaklar'} seni bekliyor...",
            "atmosphere": {
                "sounds": ["Neon vızıltısı", "Elektronik sesler", "Uzak sirenler"],
                "visuals": ["Neon ışıklar", "Yüksek binalar", "Hologramlar"]
            },
            "choices": [
                {
                    "id": "hack_system",
                    "text": "💻 Sistemi hack'le",
                    "next_node": "content_node_1",
                    "effect": {"xp": 20, "technology": 15}
                },
                {
                    "id": "street_fight",
                    "text": "🥊 Sokak savaşı",
                    "next_node": "content_node_2" if len(paragraphs) > 1 else "content_node_1",
                    "effect": {"xp": 25, "combat": 20}
                },
                {
                    "id": "corporate_espionage",
                    "text": "🏢 Kurumsal casusluk",
                    "next_node": "content_node_3" if len(paragraphs) > 2 else "content_node_1",
                    "effect": {"xp": 30, "stealth": 15}
                }
            ]
        }
    else:
        return {
            "title": "🎯 Macera Başlıyor",
            "description": f"Yeni bir macerada kendini buldun. {', '.join(locations[:2]) if locations else 'Bilinmeyen topraklar'} seni bekliyor...",
            "atmosphere": {
                "sounds": ["Rüzgar sesi", "Uzak sesler", "Doğa sesleri"],
                "visuals": ["Geniş manzaralar", "Yol işaretleri", "Uzak tepeler"]
            },
            "choices": [
                {
                    "id": "explore_area",
                    "text": "🗺️ Bölgeyi keşfet",
                    "next_node": "content_node_1",
                    "effect": {"xp": 20, "exploration": 10}
                },
                {
                    "id": "find_clues",
                    "text": "🔍 İpuçları ara",
                    "next_node": "content_node_2" if len(paragraphs) > 1 else "content_node_1",
                    "effect": {"xp": 15, "investigation": 10}
                },
                {
                    "id": "meet_npcs",
                    "text": "👥 NPC'lerle tanış",
                    "next_node": "content_node_3" if len(paragraphs) > 2 else "content_node_1",
                    "effect": {"xp": 10, "social": 10}
                }
            ]
        }

def create_content_node_from_paragraph(paragraph, node_number, theme, all_paragraphs):
    """Paragraftan hikaye noktası oluştur"""
    
    # Paragrafı kısalt (maksimum 300 karakter)
    description = paragraph[:300] + "..." if len(paragraph) > 300 else paragraph
    
    # Seçenekler oluştur
    choices = []
    
    # Farklı seçenekler
    choice_options = [
        ("➡️ Devam et", "continue"),
        ("🔍 Daha detaylı araştır", "investigate"),
        ("⚔️ Hazırlan", "prepare"),
        ("💬 Konuş", "talk"),
        ("🏃 Kaç", "escape"),
        ("⚡ Hızlı hareket et", "quick_action")
    ]
    
    # Tema bazlı seçenekler
    if theme == "fantasy":
        choice_options.extend([
            ("🔮 Büyü kullan", "cast_magic"),
            ("🗡️ Savaş", "combat"),
            ("🛡️ Savun", "defend")
        ])
    elif theme == "cyberpunk":
        choice_options.extend([
            ("💻 Hack yap", "hack"),
            ("🔫 Ateş et", "shoot"),
            ("🏃 Kaç", "escape")
        ])
    
    # Seçenekleri oluştur
    for i, (text, action) in enumerate(choice_options[:4]):  # Maksimum 4 seçenek
        # Sonraki node'u belirle - eğer son paragraf ise end'e git
        if node_number >= len(all_paragraphs):
            next_node = "end"
        else:
            next_node = f"content_node_{node_number + 1}"
        
        choices.append({
            "id": f"{action}_{node_number}",
            "text": text,
            "next_node": next_node,
            "effect": {
                "xp": 10 + (i * 5),
                "skill": get_skill_for_action(action, theme)
            }
        })
    
    # En az bir seçenek her zaman end'e gitmeli
    if node_number >= len(all_paragraphs) - 1:
        choices.append({
            "id": "finish_story",
            "text": "🎉 Hikayeyi tamamla",
            "next_node": "end",
            "effect": {"xp": 50, "achievement": "story_completed"}
        })
    
    return {
        "title": f"📖 Hikaye Bölümü {node_number}",
        "description": description,
        "atmosphere": get_atmosphere_for_theme(theme),
        "choices": choices
    }

def extract_characters_from_content(content):
    """İçerikten karakter isimleri çıkar"""
    # Basit karakter çıkarma - gerçek sistemde daha gelişmiş NLP kullanılabilir
    words = content.split()
    characters = []
    
    # Büyük harfle başlayan kelimeleri karakter olarak kabul et
    for i, word in enumerate(words):
        if word[0].isupper() and len(word) > 2 and i > 0:
            # Önceki kelime "ve", "ile", "veya" gibi bağlaçlar değilse
            if words[i-1].lower() not in ['ve', 'ile', 'veya', 'ama', 'fakat']:
                characters.append(word)
    
    return list(set(characters))[:5]  # Maksimum 5 karakter

def extract_locations_from_content(content):
    """İçerikten mekan isimleri çıkar"""
    # Basit mekan çıkarma
    location_keywords = ['kale', 'şehir', 'köy', 'orman', 'dağ', 'nehir', 'deniz', 'tapınak', 'saray', 'kule']
    locations = []
    
    for keyword in location_keywords:
        if keyword in content.lower():
            locations.append(keyword.title())
    
    return locations

def get_skill_for_action(action, theme):
    """Aksiyon için uygun beceri döndür"""
    skill_map = {
        "continue": "exploration",
        "investigate": "investigation", 
        "prepare": "planning",
        "talk": "social",
        "escape": "stealth",
        "quick_action": "agility",
        "cast_magic": "magic",
        "combat": "combat",
        "defend": "defense",
        "hack": "technology",
        "shoot": "combat"
    }
    return skill_map.get(action, "general")

def get_atmosphere_for_theme(theme):
    """Tema için atmosfer bilgisi döndür"""
    atmospheres = {
        "fantasy": {
            "sounds": ["Rüzgar uğultusu", "Büyü fısıltıları", "Metal tıngırtısı"],
            "visuals": ["Büyülü ışıklar", "Antik duvarlar", "Gizli geçitler"]
        },
        "cyberpunk": {
            "sounds": ["Elektronik sesler", "Neon vızıltısı", "Uzak sirenler"],
            "visuals": ["Neon ışıklar", "Hologramlar", "Yüksek binalar"]
        },
        "horror": {
            "sounds": ["Gıcırtılar", "Uzak çığlıklar", "Rüzgar uğultusu"],
            "visuals": ["Karanlık gölgeler", "Gizemli işaretler", "Eski yapılar"]
        },
        "adventure": {
            "sounds": ["Doğa sesleri", "Rüzgar", "Uzak sesler"],
            "visuals": ["Geniş manzaralar", "Yol işaretleri", "Uzak tepeler"]
        }
    }
    return atmospheres.get(theme, atmospheres["adventure"])

def create_npcs_from_content(content, theme):
    """İçerikten NPC'ler oluştur"""
    characters = extract_characters_from_content(content)
    npcs = {}
    
    for i, char in enumerate(characters[:3]):  # Maksimum 3 NPC
        npcs[f"npc_{i+1}"] = {
            "name": char,
            "trust_level": 0,
            "quests_completed": 0,
            "relationship_status": "stranger",
            "ending_impact": "medium" if i == 0 else "low"
        }
    
    return npcs

def create_quest_chains_from_content(content, theme):
    """İçerikten görev zincirleri oluştur"""
    return {
        "main_quest": {
            "title": "Ana Görev",
            "prerequisites": [],
            "quests": ["explore_world", "find_clues", "complete_objective"],
            "rewards": {"xp": 500, "gold": 200, "items": ["special_item"], "relationship_boost": 20}
        }
    }

def create_levels_from_content(content, theme, min_level, max_level):
    """İçerikten seviye bilgileri oluştur"""
    return {
        "level_1": {
            "title": "Başlangıç",
            "description": "Macera başlıyor",
            "min_level": min_level,
            "max_level": min_level + 2,
            "enemies": ["Basic Enemy"],
            "boss": "Minor Boss",
            "side_quests": ["Tutorial Quest"]
        },
        "level_2": {
            "title": "Gelişim",
            "description": "Karakter gelişimi",
            "min_level": min_level + 2,
            "max_level": max_level - 2,
            "enemies": ["Advanced Enemy"],
            "boss": "Major Boss", 
            "side_quests": ["Character Development"]
        }
    }

def create_end_node_from_content(content, theme):
    """İçerikten son nokta oluştur"""
    return {
        "title": "🎉 Macera Tamamlandı",
        "description": "Hikayenin sonuna ulaştın. Bu macerada çok şey öğrendin ve deneyim kazandın. Yeni maceralar seni bekliyor!",
        "choices": [
            {
                "id": "restart",
                "text": "🔄 Yeniden başla",
                "next_node": "start",
                "effect": {"xp": 50, "achievement": "completed_story"}
            }
        ]
    }

def check_and_complete_quests(user_id, scenario_id):
    """Oyuncu action'larına göre quest'leri otomatik kontrol et ve tamamla"""
    try:
        # Oyuncu istatistiklerini al
        player_stats = get_player_stats(user_id)
        
        # Senaryo quest'lerini al
        quests_to_check = get_scenario_quests(scenario_id)
        
        completed_quests = []
        
        for quest in quests_to_check:
            # Quest zaten tamamlanmış mı kontrol et
            completed_quest_key = f"quest_completed_{quest['id']}"
            if player_stats.get(completed_quest_key, False):
                continue  # Bu quest zaten tamamlanmış
            
            # Quest requirement'larını kontrol et
            requirements = quest.get('requirements', {})
            all_met = True
            
            for requirement, required_value in requirements.items():
                current_value = player_stats.get(requirement, 0)
                if current_value < required_value:
                    all_met = False
                    break
            
            if all_met:
                # Quest tamamlandı!
                completed_quests.append(quest)
                # Quest'i tamamlandı olarak işaretle
                update_player_stats(user_id, completed_quest_key, True)
                update_player_stats(user_id, "quests_completed", 1)
                
                # Quest reward'larını ver
                if 'rewards' in quest:
                    for reward_type, reward_value in quest['rewards'].items():
                        if reward_type != 'title':  # Title special case
                            update_player_stats(user_id, reward_type, reward_value)
        
        return completed_quests
        
    except Exception as e:
        print(f"Quest check error: {e}")
        return []

def get_scenario_quests(scenario_id):
    """Senaryonun quest'lerini getir"""
    # Dragon Hunter senaryosu için özel quest'ler
    if scenario_id == "dragon_hunters_path":
        return [
            {
                "id": "dragon_hunt_main",
                "title": "Ejderha Avı",
                "requirements": {
                    "combat_skill": 25,
                    "exploration_skill": 15,
                    "conversations": 3,
                    "locations_visited": 5,
                    "time_spent": 60
                },
                "rewards": {
                    "xp": 500,
                    "title": "Dragon Slayer"
                }
            },
            {
                "id": "village_helper",
                "title": "Köy Yardımcısı",
                "requirements": {
                    "charisma_skill": 10,
                    "conversations": 5,
                    "npc_interactions": 3
                },
                "rewards": {
                    "xp": 200,
                    "title": "Village Hero"
                }
            },
            {
                "id": "explorer",
                "title": "Keşifçi",
                "requirements": {
                    "exploration_skill": 20,
                    "locations_visited": 8,
                    "search_actions": 10
                },
                "rewards": {
                    "xp": 300,
                    "title": "Master Explorer"
                }
            },
            {
                "id": "warrior",
                "title": "Savaşçı",
                "requirements": {
                    "combat_skill": 30,
                    "damage_dealt": 200,
                    "combat_won": 5
                },
                "rewards": {
                    "xp": 400,
                    "title": "Warrior"
                }
            }
        ]
    
    # Diğer senaryolar için genel quest'ler
    return [
        {
            "id": "first_steps",
            "title": "İlk Adımlar",
            "requirements": {
                "exploration_skill": 5,
                "time_spent": 15
            },
            "rewards": {
                "xp": 100,
                "title": "Adventurer"
            }
        },
        {
            "id": "social_butterfly",
            "title": "Sosyal Kelebek",
            "requirements": {
                "conversations": 8,
                "charisma_skill": 15
            },
            "rewards": {
                "xp": 200,
                "title": "Social Master"
            }
        }
    ]

def generate_advanced_scenario(theme, title, character, description, difficulty):
    """Gelişmiş AI senaryo üretimi"""
    import time
    from datetime import datetime
    
    # Benzersiz ID oluştur
    scenario_id = f"ai_scenario_{int(time.time())}"
    
    # Zorluk seviyesine göre parametreler
    difficulty_settings = {
        "easy": {"min_level": 1, "max_level": 5, "duration": 60, "complexity": "simple"},
        "medium": {"min_level": 3, "max_level": 10, "duration": 120, "complexity": "medium"},
        "hard": {"min_level": 8, "max_level": 15, "duration": 180, "complexity": "complex"},
        "extreme": {"min_level": 12, "max_level": 20, "duration": 240, "complexity": "extreme"}
    }
    
    settings = difficulty_settings.get(difficulty, difficulty_settings["medium"])
    
    # Tema özelleştirilmiş hikaye noktaları
    story_nodes = create_advanced_story_nodes(theme, title, character, description, settings)
    
    # Gelişmiş NPC sistemi
    npc_relationships = create_advanced_npcs(theme, character, settings)
    
    # Görev zincirleri
    quest_chains = create_advanced_quests(theme, character, settings)
    
    # Plot twist'ler ve ihanetler
    betrayals = create_plot_twists(theme, character, settings)
    
    # Multiple endings
    endings = create_multiple_endings(theme, settings)
    
    scenario = {
        "id": scenario_id,
        "title": title,
        "theme": theme,
        "difficulty": difficulty,
        "min_level": settings["min_level"],
        "max_level": settings["max_level"],
        "duration": settings["duration"],
        "complexity": settings["complexity"],
        "description": f"{description} Bu senaryo {character} karakteri için {theme} temasında AI tarafından özel olarak üretildi. Zorluk seviyesi: {difficulty}. Tahmini süre: {settings['duration']} dakika.",
        "main_character": character,
        "story_nodes": story_nodes,
        "npc_relationships": npc_relationships,
        "quest_chains": quest_chains,
        "betrayals": betrayals,
        "endings": endings,
        "ai_generated": True,
        "created_at": datetime.now().isoformat(),
        "source_type": "ai_form",
        "features": [
            "Plot Twists", "Multiple Endings", "NPC Relationships", 
            "Quest Chains", "Dynamic Choices", "Skill Development"
        ],
        "levels": {
            "level_1": {
                "title": "Başlangıç",
                "min_level": settings["min_level"],
                "max_level": settings["min_level"] + 3,
                "enemies": get_enemies_for_theme(theme, "easy"),
                "boss": get_boss_for_theme(theme, "minor")
            },
            "level_2": {
                "title": "Gelişim",
                "min_level": settings["min_level"] + 3,
                "max_level": settings["max_level"],
                "enemies": get_enemies_for_theme(theme, "hard"),
                "boss": get_boss_for_theme(theme, "major")
            }
        }
    }
    
    return scenario

def create_advanced_story_nodes(theme, title, character, description, settings):
    """Gelişmiş hikaye noktaları oluştur"""
    nodes = {}
    
    # Başlangıç
    nodes["start"] = {
        "title": f"🎭 {title} - Macera Başlıyor",
        "description": f"{character}, {description} Bu hikayede her seçimin sonuçları olacak ve hikaye senin kararlarınla şekillenecek.",
        "atmosphere": get_atmosphere_for_theme(theme),
        "choices": [
            {
                "id": "explore_world",
                "text": "🗺️ Dünyayı keşfet",
                "next_node": "world_exploration",
                "effect": {"xp": 20, "exploration": 15}
            },
            {
                "id": "meet_npcs",
                "text": "👥 Karakterlerle tanış",
                "next_node": "npc_introduction",
                "effect": {"xp": 15, "social": 10}
            },
            {
                "id": "start_main_quest",
                "text": "⚔️ Ana göreve başla",
                "next_node": "main_quest_start",
                "effect": {"xp": 25, "combat": 15}
            }
        ]
    }
    
    # Dünya keşfi
    nodes["world_exploration"] = {
        "title": "🗺️ Dünya Keşfi",
        "description": f"Etrafını keşfederken, bu {theme} dünyasının zenginliklerini görüyorsun. Her köşede yeni sırlar ve tehlikeler seni bekliyor.",
        "choices": [
            {
                "id": "find_secret",
                "text": "🔍 Gizli yerleri ara",
                "next_node": "secret_discovery",
                "effect": {"xp": 30, "investigation": 20}
            },
            {
                "id": "gather_resources",
                "text": "💎 Kaynak topla",
                "next_node": "resource_gathering",
                "effect": {"xp": 20, "collection": 15}
            },
            {
                "id": "encounter_danger",
                "text": "⚡ Tehlikeye atıl",
                "next_node": "danger_encounter",
                "effect": {"xp": 35, "combat": 25}
            }
        ]
    }
    
    # NPC tanışma
    nodes["npc_introduction"] = {
        "title": "👥 Karakter Tanışmaları",
        "description": "Bu dünyada yaşayan ilginç karakterlerle tanışıyorsun. Her birinin kendine özgü hikayeleri ve amaçları var.",
        "choices": [
            {
                "id": "meet_ally",
                "text": "🤝 Müttefik bul",
                "next_node": "ally_meeting",
                "effect": {"xp": 25, "social": 20, "trust": 10}
            },
            {
                "id": "meet_rival",
                "text": "⚔️ Rakiple karşılaş",
                "next_node": "rival_encounter",
                "effect": {"xp": 30, "combat": 15, "rivalry": 10}
            },
            {
                "id": "meet_mentor",
                "text": "🧙 Mentor ara",
                "next_node": "mentor_meeting",
                "effect": {"xp": 35, "wisdom": 25}
            }
        ]
    }
    
    # Ana görev başlangıcı
    nodes["main_quest_start"] = {
        "title": "⚔️ Ana Görev",
        "description": f"{character} olarak ana görevine başlıyorsun. Bu görev {theme} dünyasının kaderini değiştirebilir.",
        "choices": [
            {
                "id": "choose_strategy",
                "text": "🧠 Strateji belirle",
                "next_node": "strategy_planning",
                "effect": {"xp": 30, "strategy": 20}
            },
            {
                "id": "gather_allies",
                "text": "👥 Müttefik topla",
                "next_node": "ally_gathering",
                "effect": {"xp": 25, "social": 15, "team": 10}
            },
            {
                "id": "direct_action",
                "text": "⚡ Doğrudan harekete geç",
                "next_node": "action_sequence",
                "effect": {"xp": 40, "combat": 30}
            }
        ]
    }
    
    # Son nokta
    nodes["end"] = {
        "title": "🎉 Macera Tamamlandı",
        "description": f"{character} olarak bu epik macerade çok şey başardın. Hikayende aldığın kararlar dünyayı değiştirdi.",
        "choices": [
            {
                "id": "restart",
                "text": "🔄 Yeniden başla",
                "next_node": "start",
                "effect": {"xp": 50, "achievement": "completed_story"}
            }
        ]
    }
    
    return nodes

def create_advanced_npcs(theme, character, settings):
    """Gelişmiş NPC sistemi"""
    npcs = {}
    
    if theme == "fantasy":
        npcs.update({
            "aldric_mentor": {
                "name": "Aldric the Wise",
                "title": "Büyülü Mentor",
                "trust_level": 0,
                "relationship_status": "mentor",
                "ending_impact": "high",
                "backstory": f"{character} için rehber olan yaşlı büyücü",
                "personality": "Bilge, sabırlı ama gizemli",
                "potential_betrayal": True,
                "betrayal_reason": "Gizli ejderha paktı",
                "quest_offers": ["Büyü Eğitimi", "Antik Bilgi", "Güç Ritüeli"]
            },
            "lydia_healer": {
                "name": "Lydia the Healer", 
                "title": "Gizemli Şifacı",
                "trust_level": 0,
                "relationship_status": "stranger",
                "ending_impact": "extreme",
                "backstory": "Köyde yaşayan genç şifacı, gizli kimliği var",
                "personality": "Nazik, yardımsever ama sır dolu",
                "potential_betrayal": True,
                "betrayal_reason": "Gizli ejderha kimliği",
                "romance_option": True,
                "quest_offers": ["Şifa Bitkileri", "Gizli Kimlik", "Ejderha Sırrı"]
            }
        })
    elif theme == "cyberpunk":
        npcs.update({
            "zara_hacker": {
                "name": "Zara Storm",
                "title": "Devrimci Hacker",
                "trust_level": 0,
                "relationship_status": "ally",
                "ending_impact": "high",
                "backstory": "Korporasyonlara karşı savaşan hacker",
                "personality": "Asi, zeki, tehlikeli",
                "quest_offers": ["Sistem Hack", "Devrim Planı", "Kurumsal Casusluk"]
            },
            "rex_steel": {
                "name": "Rex Steel",
                "title": "Korporasyon Ajanı",
                "trust_level": 0,
                "relationship_status": "enemy",
                "ending_impact": "extreme",
                "backstory": "MegaCorp için çalışan siber ajan",
                "personality": "Soğuk, hesapçı, sadakatsiz",
                "potential_betrayal": True,
                "betrayal_reason": "AI CEO'nun emri",
                "quest_offers": ["Korporasyon Görevi", "AI Sırrı", "Son Görev"]
            }
        })
    
    return npcs

def create_advanced_quests(theme, character, settings):
    """Gelişmiş görev zincirleri"""
    quests = {}
    
    if theme == "fantasy":
        quests["dragon_alliance"] = {
            "title": "Ejderha İttifakı",
            "description": "Ejderhalarla barış kurma görevi",
            "prerequisites": ["meet_lydia", "discover_truth"],
            "quests": ["find_dragon_eggs", "heal_mother_dragon", "create_peace_treaty"],
            "rewards": {"xp": 1000, "dragon_rep": 500, "special_power": "dragon_speech"},
            "multiple_paths": True,
            "betrayal_triggers": ["trust_aldric", "ignore_warnings"]
        }
    elif theme == "cyberpunk":
        quests["ai_revolution"] = {
            "title": "AI Devrimi",
            "description": "AI sistemini çökertme görevi",
            "prerequisites": ["hack_system", "meet_zara"],
            "quests": ["infiltrate_megacorp", "discover_ai_secret", "shutdown_or_merge"],
            "rewards": {"xp": 1200, "hacker_rep": 600, "special_tech": "ai_interface"},
            "multiple_paths": True,
            "betrayal_triggers": ["trust_rex", "corporate_deal"]
        }
    
    return quests

def create_plot_twists(theme, character, settings):
    """Plot twist'ler ve ihanetler"""
    betrayals = {}
    
    if theme == "fantasy":
        betrayals.update({
            "aldric_betrayal": {
                "trigger": "trust_level_high",
                "description": "Aldric'in ejderhalarla gizli paktı ortaya çıkıyor!",
                "impact": "Mentor düşman oluyor",
                "player_choice": True
            },
            "lydia_secret": {
                "trigger": "romance_level_high", 
                "description": "Lydia'nın gerçek kimliği - o bir ejderha!",
                "impact": "Tüm hikaye değişiyor",
                "player_choice": True
            }
        })
    elif theme == "cyberpunk":
        betrayals.update({
            "ai_ceo_reveal": {
                "trigger": "corporate_meeting",
                "description": "MegaCorp CEO'su aslında bir AI!",
                "impact": "Gerçeklik algısı değişiyor",
                "player_choice": False
            },
            "digital_consciousness": {
                "trigger": "deep_hack",
                "description": "Sen ölmüş birinin dijital bilincin!",
                "impact": "Kimlik krizi",
                "player_choice": True
            }
        })
    
    return betrayals

def create_multiple_endings(theme, settings):
    """Multiple ending sistemi"""
    endings = {}
    
    if theme == "fantasy":
        endings.update({
            "good_ending": {
                "title": "Ejderha Avcısı Zaferi",
                "description": "Ejderhayı yendin, köy kurtuldu, halk seni kahraman ilan etti.",
                "requirements": ["defeat_dragon", "save_village", "high_heroism"],
                "rewards": {"title": "Dragon Slayer", "fame": 100}
            },
            "dragon_alliance": {
                "title": "Ejderhalarla Barış",
                "description": "Ejderhalarla barış kurarak yeni bir çağ başlattın.",
                "requirements": ["trust_lydia", "find_truth", "peace_treaty"],
                "rewards": {"title": "Peacemaker", "dragon_friend": True}
            },
            "betrayal_ending": {
                "title": "Aldric'in İhaneti",
                "description": "Aldric'e güvendin ama o seni ejderlere sattı.",
                "requirements": ["trust_aldric", "ignore_warnings"],
                "rewards": {"title": "Betrayed Hero", "tragedy": True}
            },
            "sacrifice_ending": {
                "title": "Kahramanlık Fedakarlığı",
                "description": "Kendini feda ederek herkesi kurtardın.",
                "requirements": ["sacrifice_choice", "save_others"],
                "rewards": {"title": "Martyr", "legend": True}
            },
            "dark_lord_ending": {
                "title": "Karanlık Efendi",
                "description": "Karanlık güçleri seçerek dünyayı yönetmeye başladın.",
                "requirements": ["embrace_darkness", "betray_allies"],
                "rewards": {"title": "Dark Lord", "evil_power": True}
            }
        })
    elif theme == "cyberpunk":
        endings.update({
            "revolution_ending": {
                "title": "Sistem Çöküşü",
                "description": "Korporasyon sistemini çökerterek özgürlük getirdin.",
                "requirements": ["destroy_ai", "lead_revolution", "high_rebel_rep"],
                "rewards": {"title": "Revolutionary", "freedom": True}
            },
            "corporate_ending": {
                "title": "Korporasyon Ajanı",
                "description": "Korporasyonlara katılarak güç elde ettin.",
                "requirements": ["join_corp", "betray_rebels", "corporate_loyalty"],
                "rewards": {"title": "Corporate Executive", "wealth": 1000000}
            },
            "ai_merge_ending": {
                "title": "AI ile Birleşme",
                "description": "AI ile birleşerek post-human oldun.",
                "requirements": ["merge_with_ai", "transcend_humanity"],
                "rewards": {"title": "Digital God", "ai_powers": True}
            },
            "underground_king": {
                "title": "Yeraltı Kralı",
                "description": "Gölgelerden dünyayı yönetmeye başladın.",
                "requirements": ["control_underworld", "manipulate_all"],
                "rewards": {"title": "Shadow Ruler", "hidden_power": True}
            },
            "lone_wolf_ending": {
                "title": "Yalnız Kurt",
                "description": "Herkesi aldatarak tek başına ayakta kaldın.",
                "requirements": ["betray_everyone", "survive_alone"],
                "rewards": {"title": "Lone Survivor", "independence": True}
            }
        })
    
    return endings

def get_enemies_for_theme(theme, difficulty):
    """Tema için düşmanlar"""
    enemies = {
        "fantasy": {
            "easy": ["Goblin", "Wolf", "Bandit"],
            "hard": ["Orc Warrior", "Dark Wizard", "Troll"]
        },
        "cyberpunk": {
            "easy": ["Street Thug", "Security Bot", "Corpo Guard"],
            "hard": ["Cyber Assassin", "AI Drone", "Enhanced Soldier"]
        },
        "warhammer": {
            "easy": ["Chaos Cultist", "Heretic Guard", "Mutant"],
            "hard": ["Chaos Marine", "Daemon", "Chaos Lord"]
        }
    }
    return enemies.get(theme, {}).get(difficulty, ["Generic Enemy"])

def get_boss_for_theme(theme, level):
    """Tema için boss"""
    bosses = {
        "fantasy": {
            "minor": "Orc Captain",
            "major": "Ancient Dragon"
        },
        "cyberpunk": {
            "minor": "Gang Leader",
            "major": "AI Overlord"
        },
            "warhammer": {
        "minor": "Chaos Champion", 
        "major": "Daemon Prince"
    },
    "horror": {
        "minor": "Ghost",
        "major": "Ancient Evil"
    }
    }
    return bosses.get(theme, {}).get(level, "Boss Enemy")

if __name__ == '__main__':
    # For Vercel deployment
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=False)
