import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class CampaignManager:
    def __init__(self):
        self.campaigns = {}
        self.load_campaigns()
    
    def load_campaigns(self):
        """Kampanyaları yükle - şu anda boş"""
        self.campaigns = {}
        
        # Ejderha Efendilerinin Dönüşü kampanyasını ekle
        dragon_campaign = {
            "id": "dragon_lords",
            "name": "🐉 Ejderha Efendilerinin Dönüşü",
            "type": "fantasy",
            "description": "Beş büyük ejderha efendisi uyanıyor. Krallığı kurtar!",
            "scenes": [
                {
                    "id": "intro",
                    "title": "Krallığın Son Baharı",
                    "description": "Güneşin bile görünmeye çekindiği bir sabah... Gökyüzünde kara bulutlar dönüyor, kuzey dağlarından gelen duman krallığın üzerine bir kefen gibi iniyor. Beş büyük ejderha efendisi, yüz yıllık uykularından uyanıyor. Ve onların en büyüğü, en öfkelisi... Pyraxis... Kızıl Alevin Efendisi... yeniden gökyüzüne yükseliyor. Krallık düşerken, bir umut beliriyor: Sen ve senin gibi seçilmiş birkaç kahraman...",
                    "background": "/static/images/pyraxisfam.jpg",
                    "choices": [
                        {
                            "id": "continue",
                            "text": "Devam Et",
                            "result": "Yolculuğa başlıyorsun...",
                            "next_scene": "burned_village"
                        }
                    ]
                },
                {
                    "id": "burned_village",
                    "title": "Yanık Köy",
                    "description": "Alevlerle örtülmüş bir köy. Tahtadan yapılmış evler kül olmuş, hava yanık et ve is kokusuyla dolu. Çığlıklar hâlâ yankılanıyor. Binalar hâlâ çökerken, köylüler sokaklarda panik içinde koşuyor. Ejderha gitmiş... ama korku kalmış.",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {
                            "id": "calm_villagers",
                            "text": "Köylüleri Sakinleştir",
                            "result": "Birkaç çocuğun ağlaması, yaşlı bir adamın bayılması... Onlara umut oldun. 50 altın ve Pyraxis'in yuvası hakkında ipucu kazandın.",
                            "next_scene": "forest_path"
                        },
                        {
                            "id": "run_forest",
                            "text": "Ormana Kaç",
                            "result": "Sıcaklığa dayanamayarak ormanın derinliklerine kaçtın. Orada ejderha yuvası haritası buldun.",
                            "next_scene": "forest_path"
                        },
                        {
                            "id": "search_ruins",
                            "text": "Enkaz Ara",
                            "result": "Yıkılan evlerin altında bir müttefik buldun: Cüce savaşçı Borin.",
                            "next_scene": "new_ally"
                        },
                        {
                            "id": "go_smoke",
                            "text": "Dumana Git",
                            "result": "Dumanın geldiği yere doğru cesaretle ilerledin. Pyraxis'in gölgesini uzaktan gördün, ama onunla yüzleşmek için henüz hazır değilsin. Bir ipucu buldun ve ormana geri döndün.",
                            "next_scene": "forest_path"
                        }
                    ]
                },
                {
                    "id": "forest_path",
                    "title": "Orman Yolu",
                    "description": "Yolun seni getirdiği orman, sessizliğin içinde bir uğultu taşıyor. Kuşlar susmuş, rüzgâr bile fısıldıyor gibi. Bu doğa değil... büyü. Belki antik, belki lanetli. Ya da seni bir seçim yapmaya zorluyor.",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {
                            "id": "follow_sounds",
                            "text": "Sesleri Takip Et",
                            "result": "Ağaçların arasında bir ışık hüzmesi gördün. Yarım-elf bir büyücü seni bekliyordu. Yeni bir büyü öğrendin: Buz Zırhı.",
                            "effect": "item:spellbook, buff:ice_armor, gain_xp:2",
                            "next_scene": "mountain_pass"
                        },
                        {
                            "id": "hide",
                            "text": "Saklan",
                            "result": "Bir hayvanın izini buldun, küçük bir ödül kazandın ve yoluna devam ettin.",
                            "effect": "item:apple, gain_xp:1",
                            "next_scene": "mountain_pass"
                        },
                        {
                            "id": "challenge",
                            "text": "Meydan Oku",
                            "result": "Kılıcını çekip karanlığa bağırdın. Ork Savaşı başladı!",
                            "combat": True,
                            "enemy": "Ork Savaşçısı",
                            "next_scene": "mountain_pass"
                        },
                        {
                            "id": "find_other_way",
                            "text": "Geri Dön",
                            "result": "Gece çok karanlık, sesler tuzak olabilir diye geri döndün. Güvendesin ama eski bir harita buldun.",
                            "effect": "item:ancient_map, gain_xp:1",
                            "next_scene": "safe_route"
                        }
                    ]
                },
                {
                    "id": "mountain_pass",
                    "title": "Dağ Geçidi",
                    "description": "Sisli ve sarp bir dağ geçidindesin. Yolun ikiye ayrılıyor: biri tehlikeli bir uçurumdan, diğeri eski bir köprüden geçiyor.",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {
                            "id": "cliff_path",
                            "text": "Uçurum Yolunu Seç",
                            "result": "Dikkatlice ilerledin, ama bir kaya yuvarlandı! Refleks testi: Zar at! Bir taş buldun ve yoluna devam ettin.",
                            "effect": "item:old_stone, gain_xp:1",
                            "next_scene": "ancient_ruins"
                        },
                        {
                            "id": "bridge_path",
                            "text": "Eski Köprüden Geç",
                            "result": "Köprü gıcırdıyor, ama geçmeyi başardın. Bir hazine sandığı buldun!",
                            "effect": "item:random_loot, gain_xp:2",
                            "next_scene": "ancient_ruins"
                        }
                    ]
                },
                {
                    "id": "ancient_ruins",
                    "title": "Kadim Harabeler",
                    "description": "Yıkık taşlar, eski yazıtlar ve puslu bir hava... Burada bir sır saklı. Bir ruh bekçisiyle karşılaşıyorsun.",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {
                            "id": "talk_guardian",
                            "text": "Ruh Bekçisiyle Konuş",
                            "result": "Bekçi sana bir bilmece soruyor. Doğru cevaplarsan bir anahtar kazanırsın!",
                            "effect": "item:old_key, gain_xp:2",
                            "next_scene": "spirit_guardian_riddle"
                        },
                        {
                            "id": "fight_guardian",
                            "text": "Bekçiyle Savaş",
                            "result": "Zorlu bir dövüşten sonra galip geldin. Yorgunsun ama yolun açıldı.",
                            "combat": True,
                            "enemy": "Ruh Bekçisi",
                            "next_scene": "final_pyraxis_prep"
                        }
                    ]
                },
                {
                    "id": "new_ally",
                    "title": "Yeni Müttefik",
                    "description": "Cüce savaşçı Borin sana katıldı. Güçlü, cesur ve deneyimli bir dost.",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {
                            "id": "continue_with_ally",
                            "text": "Orman Yoluna Devam Et",
                            "result": "Borin ile birlikte orman yoluna devam ediyorsun.",
                            "next_scene": "forest_path"
                        }
                    ]
                },
                {
                    "id": "early_fight",
                    "title": "Erken Karşılaşma: Pyraxis",
                    "description": "Dumanın kaynağına yaklaştın. Devasa kanatlarıyla Pyraxis'i uzaktan gördün, ama onunla yüzleşmek için henüz hazır değilsin. Hayatta kalmak için geri çekildin.",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {
                            "id": "escape_early",
                            "text": "Kaç",
                            "result": "Pyraxis'ten kaçmayı başardın, ama suçluluk duygusu peşini bırakmıyor.",
                            "next_scene": "safe_route"
                        }
                    ]
                },
                {
                    "id": "orc_fight",
                    "title": "Ork Savaşı",
                    "description": "Göl Ormanı'nın Savaş Lideri Grug ile karşı karşıyasın! Kılıcını çek, dövüş başlıyor!",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {
                            "id": "attack_ork",
                            "text": "Saldır",
                            "result": "Grug yenildi, yolun Pyraxis'e açıldı.",
                            "next_scene": "final_pyraxis_prep",
                            "combat": True
                        },
                        {
                            "id": "escape_ork",
                            "text": "Kaç",
                            "result": "Grug seni takip ediyor ama kaçmayı başardın.",
                            "next_scene": "safe_route"
                        }
                    ]
                },
                {
                    "id": "safe_route",
                    "title": "Güvenli Rota",
                    "description": "Zorlu bir geceyi atlattın. Hayattasın ancak yolun uzadı. Bir köylüyle karşılaştın ve küçük bir ödül aldın.",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {
                            "id": "return_to_forest",
                            "text": "Orman Yoluna Geri Dön",
                            "result": "Güvenli rotadan orman yoluna geri döndün. Bir köylü sana elma verdi.",
                            "effect": "item:apple, gain_xp:1",
                            "next_scene": "forest_path"
                        }
                    ]
                },
                {
                    "id": "final_pyraxis_prep",
                    "title": "Pyraxis'in Mağarasına Hazırlık",
                    "description": "Ork liderini yendin ve Pyraxis'in mağarasına giden yolu buldun. Son hazırlıklarını yapıyorsun. Bu, büyük final öncesi son şansın!",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {
                            "id": "face_pyraxis",
                            "text": "Pyraxis ile Yüzleş",
                            "result": "Pyraxis ile büyük final savaşı başlıyor!",
                            "next_scene": "pyraxis_confrontation"
                        }
                    ]
                },
                {
                    "id": "boss_fight",
                    "title": "BOSS DÖVÜŞÜ: Pyraxis – Alevin Efendisi",
                    "description": "Kuzey Dağları'nın karla kaplı zirvesinde Pyraxis seni bekliyor. Gözleri alev, nefesi ölüm. Uçuyor, ateş nefesi ile saldırıyor!",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {
                            "id": "attack_boss",
                            "text": "Saldır",
                            "result": "Pyraxis'i yendin! Krallık sana minnettar, Ejderha Avcısı oldun.",
                            "next_scene": "victory",
                            "combat": True
                        },
                        {
                            "id": "escape_boss",
                            "text": "Kaç",
                            "result": "Pyraxis geri döndü. Sen hayattasın ama suçluluk duygusu peşini bırakmıyor.",
                            "next_scene": "escape"
                        }
                    ]
                },
                {
                    "id": "dragon_lair",
                    "title": "Ejderha İni",
                    "description": "Ejderha kralının gizli inine ulaştın. Burada hazineler ve tehlikeler var!",
                    "background": "/static/images/dragon_lair.jpg",
                    "choices": [
                        {"id": "explore_lair", "text": "İni Keşfet", "effect": "item:dragon_treasure, gain_xp:4", "next_scene": "dragon_elite_guard"},
                        {"id": "stealth_approach", "text": "Gizlice Yaklaş", "effect": "buff:stealth_bonus", "next_scene": "dragon_elite_guard"},
                        {"id": "fight_lair_guards", "text": "İn Muhafızlarıyla Savaş", "combat": True, "enemy": "Dragon Lair Guards", "next_scene": "dragon_elite_guard"},
                        {"id": "call_allies", "text": "Müttefikleri Çağır", "effect": "ally:dragon_hunters", "next_scene": "dragon_elite_guard"}
                    ]
                },
                {
                    "id": "dragon_elite_guard",
                    "title": "Ejderha Elit Muhafızları",
                    "description": "Ejderha kralının elit muhafızları karşında! Bu sıra tabanlı kombat çok zorlu!",
                    "background": "/static/images/dragon_elite_guard.jpg",
                    "choices": [
                        {"id": "fight_elite_guard", "text": "Elit Muhafızlarla Savaş", "combat": True, "enemy": "Dragon Elite Guard", "next_scene": "dragon_war_machine"},
                        {"id": "use_legendary_weapon", "text": "Efsanevi Silahı Kullan", "effect": "buff:legendary_power", "combat": True, "enemy": "Dragon Elite Guard", "next_scene": "dragon_war_machine"},
                        {"id": "tactical_retreat", "text": "Taktik Geri Çekilme", "next_scene": "regroup"},
                        {"id": "call_reinforcements", "text": "Takviye Çağır", "effect": "ally:imperial_elite", "next_scene": "dragon_war_machine"}
                    ]
                },
                {
                    "id": "dragon_war_machine",
                    "title": "Ejderha Savaş Makinesi",
                    "description": "Ejderha kralının savaş makinesi karşında! Bu devasa makine sıra tabanlı kombat ile yok edilmeli!",
                    "background": "/static/images/dragon_war_machine.jpg",
                    "choices": [
                        {"id": "fight_war_machine", "text": "Savaş Makinesiyle Savaş", "combat": True, "enemy": "Dragon War Machine", "next_scene": "dragon_king_preparation"},
                        {"id": "target_weak_points", "text": "Zayıf Noktaları Hedefle", "effect": "buff:precision_bonus", "combat": True, "enemy": "Dragon War Machine", "next_scene": "dragon_king_preparation"},
                        {"id": "use_explosives", "text": "Patlayıcı Kullan", "effect": "buff:explosive_bonus", "combat": True, "enemy": "Dragon War Machine", "next_scene": "dragon_king_preparation"},
                        {"id": "call_tank_support", "text": "Tank Desteği Çağır", "effect": "ally:imperial_tanks", "next_scene": "dragon_king_preparation"}
                    ]
                },
                {
                    "id": "dragon_king_preparation",
                    "title": "Ejderha Kralına Hazırlık",
                    "description": "Ejderha kralına karşı son hazırlıklarını yapıyorsun. Bu savaş senin için!",
                    "background": "/static/images/dragon_king_prep.jpg",
                    "choices": [
                        {"id": "prepare_weapons", "text": "Silahları Hazırla", "effect": "buff:weapon_preparation", "next_scene": "final_battle"},
                        {"id": "meditate_gods", "text": "Tanrılara Meditasyon", "effect": "buff:divine_blessing", "next_scene": "final_battle"},
                        {"id": "coordinate_allies", "text": "Müttefikleri Koordine Et", "effect": "ally:final_allies", "next_scene": "final_battle"},
                        {"id": "study_dragon_king", "text": "Ejderha Kralını Araştır", "effect": "item:dragon_king_intel", "next_scene": "final_battle"}
                    ]
                },
                {
                    "id": "side_mission_dragon_hunters",
                    "title": "Yan Görev: Ejderha Avcıları",
                    "description": "Diğer ejderha avcıları ile karşılaştın. Onlarla birlikte çalışabilirsin!",
                    "background": "/static/images/dragon_hunters.jpg",
                    "choices": [
                        {"id": "join_hunters", "text": "Avcılara Katıl", "effect": "ally:dragon_hunters, gain_xp:3", "next_scene": "side_mission_dragon_artifacts"},
                        {"id": "compete_hunters", "text": "Avcılarla Yarış", "effect": "buff:competition_bonus", "next_scene": "side_mission_dragon_artifacts"},
                        {"id": "fight_hunters", "text": "Avcılarla Savaş", "combat": True, "enemy": "Dragon Hunters", "next_scene": "side_mission_dragon_artifacts"},
                        {"id": "negotiate_hunters", "text": "Avcılarla Müzakere", "effect": "karma:+5", "next_scene": "side_mission_dragon_artifacts"}
                    ]
                },
                {
                    "id": "side_mission_dragon_artifacts",
                    "title": "Yan Görev: Ejderha Artefaktları",
                    "description": "Ejderha kralının gizli artefakt deposunu keşfettin. Burada güçlü silahlar var!",
                    "background": "/static/images/dragon_artifacts.jpg",
                    "choices": [
                        {"id": "steal_artifacts", "text": "Artefaktları Çal", "effect": "item:dragon_artifacts", "next_scene": "side_mission_dragon_library"},
                        {"id": "study_artifacts", "text": "Artefaktları İncele", "effect": "item:artifact_knowledge", "next_scene": "side_mission_dragon_library"},
                        {"id": "fight_artifact_guards", "text": "Artefakt Muhafızlarıyla Savaş", "combat": True, "enemy": "Artifact Guards", "next_scene": "side_mission_dragon_library"},
                        {"id": "bless_artifacts", "text": "Artefaktları Kutsa", "effect": "karma:+10", "next_scene": "side_mission_dragon_library"}
                    ]
                },
                {
                    "id": "side_mission_dragon_library",
                    "title": "Yan Görev: Ejderha Kütüphanesi",
                    "description": "Ejderha kralının gizli kütüphanesini keşfettin. Burada eski sırlar var!",
                    "background": "/static/images/dragon_library.jpg",
                    "choices": [
                        {"id": "read_books", "text": "Kitapları Oku", "effect": "item:ancient_knowledge, gain_xp:4", "next_scene": "side_mission_dragon_prison"},
                        {"id": "steal_books", "text": "Kitapları Çal", "effect": "item:stolen_books", "next_scene": "side_mission_dragon_prison"},
                        {"id": "fight_library_guards", "text": "Kütüphane Muhafızlarıyla Savaş", "combat": True, "enemy": "Library Guards", "next_scene": "side_mission_dragon_prison"},
                        {"id": "study_library", "text": "Kütüphaneyi İncele", "effect": "buff:knowledge_power", "next_scene": "side_mission_dragon_prison"}
                    ]
                },
                {
                    "id": "side_mission_dragon_prison",
                    "title": "Yan Görev: Ejderha Hapishanesi",
                    "description": "Ejderha kralının hapishanesini keşfettin. Burada mahkumlar var!",
                    "background": "/static/images/dragon_prison.jpg",
                    "choices": [
                        {"id": "free_prisoners", "text": "Mahkumları Serbest Bırak", "effect": "ally:freed_prisoners, gain_xp:4", "next_scene": "side_mission_final"},
                        {"id": "interrogate_prisoners", "text": "Mahkumları Sorgula", "effect": "item:prisoner_intel", "next_scene": "side_mission_final"},
                        {"id": "fight_prison_guards", "text": "Hapishane Muhafızlarıyla Savaş", "combat": True, "enemy": "Prison Guards", "next_scene": "side_mission_final"},
                        {"id": "negotiate_prisoners", "text": "Mahkumlarla Müzakere", "effect": "karma:+5", "next_scene": "side_mission_final"}
                    ]
                },
                {
                    "id": "side_mission_final",
                    "title": "Yan Görev: Son Direniş",
                    "description": "Ejderha kralının son direniş noktası. Bu yeri ele geçirmek çok önemli!",
                    "background": "/static/images/final_resistance.jpg",
                    "choices": [
                        {"id": "attack_resistance", "text": "Direnişe Saldır", "combat": True, "enemy": "Final Resistance", "next_scene": "victory"},
                        {"id": "hack_resistance", "text": "Direnişi Hack Et", "effect": "buff:resistance_control", "next_scene": "victory"},
                        {"id": "negotiate_resistance", "text": "Direnişle Müzakere", "effect": "karma:+5", "next_scene": "victory"},
                        {"id": "call_allies", "text": "Müttefikleri Çağır", "effect": "ally:final_allies", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "dragon_hunter_guild",
                    "title": "Ejderha Avcısı Loncası",
                    "description": "Ejderha avcıları loncasına ulaştın. Burada güçlü avcılar var!",
                    "background": "/static/images/dragon_hunter_guild.jpg",
                    "choices": [
                        {"id": "join_guild", "text": "Loncaya Katıl", "effect": "ally:hunter_guild, gain_xp:4", "next_scene": "dragon_hunter_training"},
                        {"id": "learn_hunting_skills", "text": "Avcılık Becerilerini Öğren", "effect": "buff:hunting_skills", "next_scene": "dragon_hunter_training"},
                        {"id": "fight_guild_members", "text": "Lonca Üyeleriyle Savaş", "combat": True, "enemy": "Guild Members", "next_scene": "dragon_hunter_training"},
                        {"id": "negotiate_guild", "text": "Loncayla Müzakere", "effect": "karma:+5", "next_scene": "dragon_hunter_training"}
                    ]
                },
                {
                    "id": "dragon_hunter_training",
                    "title": "Ejderha Avcısı Eğitimi",
                    "description": "Ejderha avcısı eğitim merkezine ulaştın. Burada güçlü eğitmenler var!",
                    "background": "/static/images/dragon_hunter_training.jpg",
                    "choices": [
                        {"id": "train_with_masters", "text": "Ustalarla Eğitim Al", "effect": "gain_xp:5, buff:master_training", "next_scene": "dragon_hunter_weapons"},
                        {"id": "learn_advanced_skills", "text": "Gelişmiş Beceriler Öğren", "effect": "buff:advanced_skills", "next_scene": "dragon_hunter_weapons"},
                        {"id": "fight_training_masters", "text": "Eğitmenlerle Savaş", "combat": True, "enemy": "Training Masters", "next_scene": "dragon_hunter_weapons"},
                        {"id": "study_training_manuals", "text": "Eğitim Kitaplarını Oku", "effect": "item:training_manuals", "next_scene": "dragon_hunter_weapons"}
                    ]
                },
                {
                    "id": "dragon_hunter_weapons",
                    "title": "Ejderha Avcısı Silahları",
                    "description": "Ejderha avcısı silah deposuna ulaştın. Burada güçlü silahlar var!",
                    "background": "/static/images/dragon_hunter_weapons.jpg",
                    "choices": [
                        {"id": "get_dragon_weapons", "text": "Ejderha Silahları Al", "effect": "item:dragon_weapons", "next_scene": "dragon_hunter_armor"},
                        {"id": "craft_weapons", "text": "Silah Yap", "effect": "buff:weapon_crafting", "next_scene": "dragon_hunter_armor"},
                        {"id": "fight_weapon_guards", "text": "Silah Muhafızlarıyla Savaş", "combat": True, "enemy": "Weapon Guards", "next_scene": "dragon_hunter_armor"},
                        {"id": "study_weapon_lore", "text": "Silah Lore'unu Öğren", "effect": "item:weapon_lore", "next_scene": "dragon_hunter_armor"}
                    ]
                },
                {
                    "id": "dragon_hunter_armor",
                    "title": "Ejderha Avcısı Zırhı",
                    "description": "Ejderha avcısı zırh deposuna ulaştın. Burada güçlü zırhlar var!",
                    "background": "/static/images/dragon_hunter_armor.jpg",
                    "choices": [
                        {"id": "get_dragon_armor", "text": "Ejderha Zırhı Al", "effect": "item:dragon_armor", "next_scene": "dragon_hunter_potions"},
                        {"id": "craft_armor", "text": "Zırh Yap", "effect": "buff:armor_crafting", "next_scene": "dragon_hunter_potions"},
                        {"id": "fight_armor_guards", "text": "Zırh Muhafızlarıyla Savaş", "combat": True, "enemy": "Armor Guards", "next_scene": "dragon_hunter_potions"},
                        {"id": "study_armor_lore", "text": "Zırh Lore'unu Öğren", "effect": "item:armor_lore", "next_scene": "dragon_hunter_potions"}
                    ]
                },
                {
                    "id": "dragon_hunter_potions",
                    "title": "Ejderha Avcısı İksirleri",
                    "description": "Ejderha avcısı iksir laboratuvarına ulaştın. Burada güçlü iksirler var!",
                    "background": "/static/images/dragon_hunter_potions.jpg",
                    "choices": [
                        {"id": "get_dragon_potions", "text": "Ejderha İksirleri Al", "effect": "item:dragon_potions", "next_scene": "dragon_hunter_scrolls"},
                        {"id": "brew_potions", "text": "İksir Yap", "effect": "buff:potion_brewing", "next_scene": "dragon_hunter_scrolls"},
                        {"id": "fight_potion_guards", "text": "İksir Muhafızlarıyla Savaş", "combat": True, "enemy": "Potion Guards", "next_scene": "dragon_hunter_scrolls"},
                        {"id": "study_potion_lore", "text": "İksir Lore'unu Öğren", "effect": "item:potion_lore", "next_scene": "dragon_hunter_scrolls"}
                    ]
                },
                {
                    "id": "dragon_hunter_scrolls",
                    "title": "Ejderha Avcısı Tomarları",
                    "description": "Ejderha avcısı tomarlar kütüphanesine ulaştın. Burada güçlü tomarlar var!",
                    "background": "/static/images/dragon_hunter_scrolls.jpg",
                    "choices": [
                        {"id": "get_dragon_scrolls", "text": "Ejderha Tomarları Al", "effect": "item:dragon_scrolls", "next_scene": "dragon_hunter_maps"},
                        {"id": "study_scrolls", "text": "Tomarları İncele", "effect": "buff:scroll_knowledge", "next_scene": "dragon_hunter_maps"},
                        {"id": "fight_scroll_guards", "text": "Tomar Muhafızlarıyla Savaş", "combat": True, "enemy": "Scroll Guards", "next_scene": "dragon_hunter_maps"},
                        {"id": "copy_scrolls", "text": "Tomarları Kopyala", "effect": "item:scroll_copies", "next_scene": "dragon_hunter_maps"}
                    ]
                },
                {
                    "id": "dragon_hunter_maps",
                    "title": "Ejderha Avcısı Haritaları",
                    "description": "Ejderha avcısı harita odasına ulaştın. Burada gizli haritalar var!",
                    "background": "/static/images/dragon_hunter_maps.jpg",
                    "choices": [
                        {"id": "get_dragon_maps", "text": "Ejderha Haritaları Al", "effect": "item:dragon_maps", "next_scene": "dragon_hunter_spells"},
                        {"id": "study_maps", "text": "Haritaları İncele", "effect": "buff:map_knowledge", "next_scene": "dragon_hunter_spells"},
                        {"id": "fight_map_guards", "text": "Harita Muhafızlarıyla Savaş", "combat": True, "enemy": "Map Guards", "next_scene": "dragon_hunter_spells"},
                        {"id": "copy_maps", "text": "Haritaları Kopyala", "effect": "item:map_copies", "next_scene": "dragon_hunter_spells"}
                    ]
                },
                {
                    "id": "dragon_hunter_spells",
                    "title": "Ejderha Avcısı Büyüleri",
                    "description": "Ejderha avcısı büyü okuluna ulaştın. Burada güçlü büyüler var!",
                    "background": "/static/images/dragon_hunter_spells.jpg",
                    "choices": [
                        {"id": "learn_dragon_spells", "text": "Ejderha Büyülerini Öğren", "effect": "buff:dragon_spells", "next_scene": "dragon_hunter_rituals"},
                        {"id": "study_spells", "text": "Büyüleri İncele", "effect": "buff:spell_knowledge", "next_scene": "dragon_hunter_rituals"},
                        {"id": "fight_spell_guards", "text": "Büyü Muhafızlarıyla Savaş", "combat": True, "enemy": "Spell Guards", "next_scene": "dragon_hunter_rituals"},
                        {"id": "practice_spells", "text": "Büyüleri Pratik Et", "effect": "buff:spell_practice", "next_scene": "dragon_hunter_rituals"}
                    ]
                },
                {
                    "id": "dragon_hunter_rituals",
                    "title": "Ejderha Avcısı Ritüelleri",
                    "description": "Ejderha avcısı ritüel odasına ulaştın. Burada güçlü ritüeller var!",
                    "background": "/static/images/dragon_hunter_rituals.jpg",
                    "choices": [
                        {"id": "learn_dragon_rituals", "text": "Ejderha Ritüellerini Öğren", "effect": "buff:dragon_rituals", "next_scene": "dragon_hunter_talismans"},
                        {"id": "study_rituals", "text": "Ritüelleri İncele", "effect": "buff:ritual_knowledge", "next_scene": "dragon_hunter_talismans"},
                        {"id": "fight_ritual_guards", "text": "Ritüel Muhafızlarıyla Savaş", "combat": True, "enemy": "Ritual Guards", "next_scene": "dragon_hunter_talismans"},
                        {"id": "perform_rituals", "text": "Ritüelleri Gerçekleştir", "effect": "buff:ritual_power", "next_scene": "dragon_hunter_talismans"}
                    ]
                },
                {
                    "id": "dragon_hunter_talismans",
                    "title": "Ejderha Avcısı Tılsımları",
                    "description": "Ejderha avcısı tılsım odasına ulaştın. Burada güçlü tılsımlar var!",
                    "background": "/static/images/dragon_hunter_talismans.jpg",
                    "choices": [
                        {"id": "get_dragon_talismans", "text": "Ejderha Tılsımları Al", "effect": "item:dragon_talismans", "next_scene": "dragon_hunter_final_prep"},
                        {"id": "craft_talismans", "text": "Tılsım Yap", "effect": "buff:talisman_crafting", "next_scene": "dragon_hunter_final_prep"},
                        {"id": "fight_talisman_guards", "text": "Tılsım Muhafızlarıyla Savaş", "combat": True, "enemy": "Talisman Guards", "next_scene": "dragon_hunter_final_prep"},
                        {"id": "study_talisman_lore", "text": "Tılsım Lore'unu Öğren", "effect": "item:talisman_lore", "next_scene": "dragon_hunter_final_prep"}
                    ]
                },
                {
                    "id": "dragon_hunter_final_prep",
                    "title": "Ejderha Avcısı Son Hazırlık",
                    "description": "Ejderha avcısı son hazırlık odasına ulaştın. Burada son hazırlıklar yapılıyor!",
                    "background": "/static/images/dragon_hunter_final_prep.jpg",
                    "choices": [
                        {"id": "prepare_equipment", "text": "Ekipmanı Hazırla", "effect": "buff:equipment_prep", "next_scene": "dragon_hunter_final_battle"},
                        {"id": "meditate_preparation", "text": "Hazırlık Meditasyonu", "effect": "buff:meditation_prep", "next_scene": "dragon_hunter_final_battle"},
                        {"id": "coordinate_hunters", "text": "Avcıları Koordine Et", "effect": "ally:coordinated_hunters", "next_scene": "dragon_hunter_final_battle"},
                        {"id": "study_dragon_lore", "text": "Ejderha Lore'unu Öğren", "effect": "item:dragon_lore", "next_scene": "dragon_hunter_final_battle"}
                    ]
                },
                {
                    "id": "dragon_hunter_final_battle",
                    "title": "Ejderha Avcısı Son Savaş",
                    "description": "Ejderha avcısı son savaşı başladı! Bu sıra tabanlı kombat senin için!",
                    "background": "/static/images/dragon_hunter_final_battle.jpg",
                    "choices": [
                        {"id": "fight_final_battle", "text": "Son Savaşta Savaş", "combat": True, "enemy": "Dragon Hunter Final Boss", "next_scene": "victory"},
                        {"id": "use_hunter_skills", "text": "Avcı Becerilerini Kullan", "effect": "buff:hunter_power", "combat": True, "enemy": "Dragon Hunter Final Boss", "next_scene": "victory"},
                        {"id": "call_hunter_allies", "text": "Avcı Müttefiklerini Çağır", "effect": "ally:hunter_allies", "combat": True, "enemy": "Dragon Hunter Final Boss", "next_scene": "victory"},
                        {"id": "negotiate_final", "text": "Son Müzakere", "effect": "karma:+15", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "dragon_hunter_guild_hall",
                    "title": "Ejderha Avcısı Lonca Salonu",
                    "description": "Ejderha Avcısı Loncası'nın büyük salonuna ulaştın. Burada güçlü avcılar var!",
                    "background": "/static/images/dragon_hunter_guild_hall.jpg",
                    "choices": [
                        {"id": "join_hunter_guild", "text": "Loncaya Katıl", "effect": "ally:hunter_guild, gain_xp:5", "next_scene": "dragon_hunter_training_grounds"},
                        {"id": "learn_guild_lore", "text": "Lonca Lore'unu Öğren", "effect": "buff:guild_lore", "next_scene": "dragon_hunter_training_grounds"},
                        {"id": "fight_guild_master", "text": "Lonca Ustası ile Savaş", "combat": True, "enemy": "Guild Master", "next_scene": "dragon_hunter_training_grounds"},
                        {"id": "receive_guild_blessing", "text": "Lonca Kutsaması Al", "effect": "buff:guild_blessing", "next_scene": "dragon_hunter_training_grounds"}
                    ]
                },
                {
                    "id": "dragon_hunter_training_grounds",
                    "title": "Ejderha Avcısı Eğitim Alanı",
                    "description": "Ejderha Avcısı eğitim alanına ulaştın. Burada güçlü eğitmenler var!",
                    "background": "/static/images/dragon_hunter_training_grounds.jpg",
                    "choices": [
                        {"id": "train_with_masters", "text": "Ustalarla Eğitim Al", "effect": "ally:training_masters, gain_xp:4", "next_scene": "dragon_hunter_weapon_smith"},
                        {"id": "learn_combat_skills", "text": "Savaş Becerilerini Öğren", "effect": "buff:combat_skills", "next_scene": "dragon_hunter_weapon_smith"},
                        {"id": "fight_training_master", "text": "Eğitmen ile Savaş", "combat": True, "enemy": "Training Master", "next_scene": "dragon_hunter_weapon_smith"},
                        {"id": "study_training_lore", "text": "Eğitim Lore'unu Öğren", "effect": "item:training_lore", "next_scene": "dragon_hunter_weapon_smith"}
                    ]
                },
                {
                    "id": "dragon_hunter_weapon_smith",
                    "title": "Ejderha Avcısı Silah Ustası",
                    "description": "Ejderha Avcısı silah ustasına ulaştın. Burada güçlü silahlar var!",
                    "background": "/static/images/dragon_hunter_weapon_smith.jpg",
                    "choices": [
                        {"id": "get_dragon_weapons", "text": "Ejderha Silahları Al", "effect": "item:dragon_weapons", "next_scene": "dragon_hunter_armor_smith"},
                        {"id": "learn_weapon_crafting", "text": "Silah Yapımını Öğren", "effect": "buff:weapon_crafting", "next_scene": "dragon_hunter_armor_smith"},
                        {"id": "fight_weapon_smith", "text": "Silah Ustası ile Savaş", "combat": True, "enemy": "Weapon Smith", "next_scene": "dragon_hunter_armor_smith"},
                        {"id": "study_weapon_lore", "text": "Silah Lore'unu Öğren", "effect": "item:weapon_lore", "next_scene": "dragon_hunter_armor_smith"}
                    ]
                },
                {
                    "id": "dragon_hunter_armor_smith",
                    "title": "Ejderha Avcısı Zırh Ustası",
                    "description": "Ejderha Avcısı zırh ustasına ulaştın. Burada güçlü zırhlar var!",
                    "background": "/static/images/dragon_hunter_armor_smith.jpg",
                    "choices": [
                        {"id": "get_dragon_armor", "text": "Ejderha Zırhı Al", "effect": "item:dragon_armor", "next_scene": "dragon_hunter_potion_master"},
                        {"id": "learn_armor_crafting", "text": "Zırh Yapımını Öğren", "effect": "buff:armor_crafting", "next_scene": "dragon_hunter_potion_master"},
                        {"id": "fight_armor_smith", "text": "Zırh Ustası ile Savaş", "combat": True, "enemy": "Armor Smith", "next_scene": "dragon_hunter_potion_master"},
                        {"id": "study_armor_lore", "text": "Zırh Lore'unu Öğren", "effect": "item:armor_lore", "next_scene": "dragon_hunter_potion_master"}
                    ]
                },
                {
                    "id": "dragon_hunter_potion_master",
                    "title": "Ejderha Avcısı İksir Ustası",
                    "description": "Ejderha Avcısı iksir ustasına ulaştın. Burada güçlü iksirler var!",
                    "background": "/static/images/dragon_hunter_potion_master.jpg",
                    "choices": [
                        {"id": "get_dragon_potions", "text": "Ejderha İksirleri Al", "effect": "item:dragon_potions", "next_scene": "dragon_hunter_scroll_master"},
                        {"id": "learn_potion_brewing", "text": "İksir Yapımını Öğren", "effect": "buff:potion_brewing", "next_scene": "dragon_hunter_scroll_master"},
                        {"id": "fight_potion_master", "text": "İksir Ustası ile Savaş", "combat": True, "enemy": "Potion Master", "next_scene": "dragon_hunter_scroll_master"},
                        {"id": "study_potion_lore", "text": "İksir Lore'unu Öğren", "effect": "item:potion_lore", "next_scene": "dragon_hunter_scroll_master"}
                    ]
                },
                {
                    "id": "dragon_hunter_scroll_master",
                    "title": "Ejderha Avcısı Tomar Ustası",
                    "description": "Ejderha Avcısı tomar ustasına ulaştın. Burada güçlü tomar büyüleri var!",
                    "background": "/static/images/dragon_hunter_scroll_master.jpg",
                    "choices": [
                        {"id": "get_dragon_scrolls", "text": "Ejderha Tomarları Al", "effect": "item:dragon_scrolls", "next_scene": "dragon_hunter_map_master"},
                        {"id": "learn_scroll_crafting", "text": "Tomar Yapımını Öğren", "effect": "buff:scroll_crafting", "next_scene": "dragon_hunter_map_master"},
                        {"id": "fight_scroll_master", "text": "Tomar Ustası ile Savaş", "combat": True, "enemy": "Scroll Master", "next_scene": "dragon_hunter_map_master"},
                        {"id": "study_scroll_lore", "text": "Tomar Lore'unu Öğren", "effect": "item:scroll_lore", "next_scene": "dragon_hunter_map_master"}
                    ]
                },
                {
                    "id": "dragon_hunter_map_master",
                    "title": "Ejderha Avcısı Harita Ustası",
                    "description": "Ejderha Avcısı harita ustasına ulaştın. Burada güçlü haritalar var!",
                    "background": "/static/images/dragon_hunter_map_master.jpg",
                    "choices": [
                        {"id": "get_dragon_maps", "text": "Ejderha Haritaları Al", "effect": "item:dragon_maps", "next_scene": "dragon_hunter_spell_master"},
                        {"id": "learn_map_crafting", "text": "Harita Yapımını Öğren", "effect": "buff:map_crafting", "next_scene": "dragon_hunter_spell_master"},
                        {"id": "fight_map_master", "text": "Harita Ustası ile Savaş", "combat": True, "enemy": "Map Master", "next_scene": "dragon_hunter_spell_master"},
                        {"id": "study_map_lore", "text": "Harita Lore'unu Öğren", "effect": "item:map_lore", "next_scene": "dragon_hunter_spell_master"}
                    ]
                },
                {
                    "id": "dragon_hunter_spell_master",
                    "title": "Ejderha Avcısı Büyü Ustası",
                    "description": "Ejderha Avcısı büyü ustasına ulaştın. Burada güçlü büyüler var!",
                    "background": "/static/images/dragon_hunter_spell_master.jpg",
                    "choices": [
                        {"id": "learn_dragon_spells", "text": "Ejderha Büyülerini Öğren", "effect": "buff:dragon_spells, gain_xp:5", "next_scene": "dragon_hunter_ritual_master"},
                        {"id": "get_spell_scrolls", "text": "Büyü Tomarları Al", "effect": "item:spell_scrolls", "next_scene": "dragon_hunter_ritual_master"},
                        {"id": "fight_spell_master", "text": "Büyü Ustası ile Savaş", "combat": True, "enemy": "Spell Master", "next_scene": "dragon_hunter_ritual_master"},
                        {"id": "study_spell_lore", "text": "Büyü Lore'unu Öğren", "effect": "item:spell_lore", "next_scene": "dragon_hunter_ritual_master"}
                    ]
                },
                {
                    "id": "dragon_hunter_ritual_master",
                    "title": "Ejderha Avcısı Ritüel Ustası",
                    "description": "Ejderha Avcısı ritüel ustasına ulaştın. Burada güçlü ritüeller var!",
                    "background": "/static/images/dragon_hunter_ritual_master.jpg",
                    "choices": [
                        {"id": "learn_dragon_rituals", "text": "Ejderha Ritüellerini Öğren", "effect": "buff:dragon_rituals, gain_xp:5", "next_scene": "dragon_hunter_talisman_master"},
                        {"id": "perform_ritual", "text": "Ritüel Gerçekleştir", "effect": "buff:ritual_power", "next_scene": "dragon_hunter_talisman_master"},
                        {"id": "fight_ritual_master", "text": "Ritüel Ustası ile Savaş", "combat": True, "enemy": "Ritual Master", "next_scene": "dragon_hunter_talisman_master"},
                        {"id": "study_ritual_lore", "text": "Ritüel Lore'unu Öğren", "effect": "item:ritual_lore", "next_scene": "dragon_hunter_talisman_master"}
                    ]
                },
                {
                    "id": "dragon_hunter_talisman_master",
                    "title": "Ejderha Avcısı Tılsım Ustası",
                    "description": "Ejderha Avcısı tılsım ustasına ulaştın. Burada güçlü tılsımlar var!",
                    "background": "/static/images/dragon_hunter_talisman_master.jpg",
                    "choices": [
                        {"id": "get_dragon_talismans", "text": "Ejderha Tılsımları Al", "effect": "item:dragon_talismans", "next_scene": "dragon_hunter_final_prep"},
                        {"id": "learn_talisman_crafting", "text": "Tılsım Yapımını Öğren", "effect": "buff:talisman_crafting", "next_scene": "dragon_hunter_final_prep"},
                        {"id": "fight_talisman_master", "text": "Tılsım Ustası ile Savaş", "combat": True, "enemy": "Talisman Master", "next_scene": "dragon_hunter_final_prep"},
                        {"id": "study_talisman_lore", "text": "Tılsım Lore'unu Öğren", "effect": "item:talisman_lore", "next_scene": "dragon_hunter_final_prep"}
                    ]
                },
                {
                    "id": "dragon_hunter_final_prep",
                    "title": "Ejderha Avcısı Son Hazırlık",
                    "description": "Ejderha Avcısı son hazırlık odasına ulaştın. Burada son hazırlıklar yapılıyor!",
                    "background": "/static/images/dragon_hunter_final_prep.jpg",
                    "choices": [
                        {"id": "final_equipment_check", "text": "Son Ekipman Kontrolü", "effect": "buff:final_preparation, gain_xp:6", "next_scene": "dragon_hunter_final_battle"},
                        {"id": "final_strategy_meeting", "text": "Son Strateji Toplantısı", "effect": "buff:strategy_bonus", "next_scene": "dragon_hunter_final_battle"},
                        {"id": "final_blessing", "text": "Son Kutsama", "effect": "buff:final_blessing", "next_scene": "dragon_hunter_final_battle"},
                        {"id": "final_ritual", "text": "Son Ritüel", "effect": "buff:final_ritual_power", "next_scene": "dragon_hunter_final_battle"}
                    ]
                },
                {
                    "id": "dragon_hunter_final_battle",
                    "title": "Ejderha Avcısı Son Savaş",
                    "description": "Ejderha Avcısı son savaşı başladı! Bu sıra tabanlı kombat senin için!",
                    "background": "/static/images/dragon_hunter_final_battle.jpg",
                    "choices": [
                        {"id": "fight_final_dragon", "text": "Son Ejderha ile Savaş", "combat": True, "enemy": "Ancient Dragon", "next_scene": "victory"},
                        {"id": "use_hunter_tactics", "text": "Avcı Taktiklerini Kullan", "effect": "buff:hunter_power", "combat": True, "enemy": "Ancient Dragon", "next_scene": "victory"},
                        {"id": "call_hunter_allies", "text": "Avcı Müttefiklerini Çağır", "effect": "ally:hunter_allies", "combat": True, "enemy": "Ancient Dragon", "next_scene": "victory"},
                        {"id": "negotiate_dragon", "text": "Ejderha ile Müzakere", "effect": "karma:+15", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "side_mission_dragon_hunters",
                    "title": "Yan Görev: Ejderha Avcıları",
                    "description": "Diğer ejderha avcılarıyla birlikte çalışarak daha güçlü hale gel!",
                    "background": "/static/images/side_mission_dragon_hunters.jpg",
                    "choices": [
                        {"id": "join_hunter_party", "text": "Avcı Partisine Katıl", "effect": "ally:hunter_party, gain_xp:4", "next_scene": "side_mission_dragon_artifacts"},
                        {"id": "learn_party_tactics", "text": "Parti Taktiklerini Öğren", "effect": "buff:party_tactics", "next_scene": "side_mission_dragon_artifacts"},
                        {"id": "fight_hunter_rival", "text": "Rakip Avcı ile Savaş", "combat": True, "enemy": "Hunter Rival", "next_scene": "side_mission_dragon_artifacts"},
                        {"id": "study_hunter_lore", "text": "Avcı Lore'unu Öğren", "effect": "item:hunter_lore", "next_scene": "side_mission_dragon_artifacts"}
                    ]
                },
                {
                    "id": "side_mission_dragon_artifacts",
                    "title": "Yan Görev: Ejderha Artefaktları",
                    "description": "Kadim ejderha artefaktlarını topla ve güç kazan!",
                    "background": "/static/images/side_mission_dragon_artifacts.jpg",
                    "choices": [
                        {"id": "collect_artifacts", "text": "Artefaktları Topla", "effect": "item:dragon_artifacts, gain_xp:4", "next_scene": "side_mission_dragon_library"},
                        {"id": "study_artifacts", "text": "Artefaktları İncele", "effect": "buff:artifact_knowledge", "next_scene": "side_mission_dragon_library"},
                        {"id": "fight_artifact_guardian", "text": "Artefakt Bekçisi ile Savaş", "combat": True, "enemy": "Artifact Guardian", "next_scene": "side_mission_dragon_library"},
                        {"id": "learn_artifact_lore", "text": "Artefakt Lore'unu Öğren", "effect": "item:artifact_lore", "next_scene": "side_mission_dragon_library"}
                    ]
                },
                {
                    "id": "side_mission_dragon_library",
                    "title": "Yan Görev: Ejderha Kütüphanesi",
                    "description": "Ejderha kütüphanesinde kadim bilgileri keşfet!",
                    "background": "/static/images/side_mission_dragon_library.jpg",
                    "choices": [
                        {"id": "study_dragon_lore", "text": "Ejderha Lore'unu Öğren", "effect": "buff:dragon_lore, gain_xp:4", "next_scene": "side_mission_dragon_prison"},
                        {"id": "find_secret_tomes", "text": "Gizli Tomarları Bul", "effect": "item:secret_tomes", "next_scene": "side_mission_dragon_prison"},
                        {"id": "fight_library_guardian", "text": "Kütüphane Bekçisi ile Savaş", "combat": True, "enemy": "Library Guardian", "next_scene": "side_mission_dragon_prison"},
                        {"id": "learn_library_lore", "text": "Kütüphane Lore'unu Öğren", "effect": "item:library_lore", "next_scene": "side_mission_dragon_prison"}
                    ]
                },
                {
                    "id": "side_mission_dragon_prison",
                    "title": "Yan Görev: Ejderha Hapishanesi",
                    "description": "Ejderha hapishanesinde esir avcıları kurtar!",
                    "background": "/static/images/side_mission_dragon_prison.jpg",
                    "choices": [
                        {"id": "rescue_captured_hunters", "text": "Esir Avcıları Kurtar", "effect": "ally:rescued_hunters, gain_xp:5", "next_scene": "side_mission_final"},
                        {"id": "fight_prison_guards", "text": "Hapishane Muhafızları ile Savaş", "combat": True, "enemy": "Prison Guards", "next_scene": "side_mission_final"},
                        {"id": "learn_prison_lore", "text": "Hapishane Lore'unu Öğren", "effect": "item:prison_lore", "next_scene": "side_mission_final"},
                        {"id": "study_prison_secrets", "text": "Hapishane Sırlarını İncele", "effect": "buff:prison_knowledge", "next_scene": "side_mission_final"}
                    ]
                },
                {
                    "id": "side_mission_final",
                    "title": "Yan Görev: Son Direniş",
                    "description": "Yan görevlerin son direnişi! Bu sıra tabanlı kombat senin için!",
                    "background": "/static/images/side_mission_final.jpg",
                    "choices": [
                        {"id": "fight_side_mission_boss", "text": "Yan Görev Boss'u ile Savaş", "combat": True, "enemy": "Side Mission Boss", "next_scene": "victory"},
                        {"id": "use_side_tactics", "text": "Yan Görev Taktiklerini Kullan", "effect": "buff:side_power", "combat": True, "enemy": "Side Mission Boss", "next_scene": "victory"},
                        {"id": "call_side_allies", "text": "Yan Görev Müttefiklerini Çağır", "effect": "ally:side_allies", "combat": True, "enemy": "Side Mission Boss", "next_scene": "victory"},
                        {"id": "negotiate_side_boss", "text": "Yan Görev Boss'u ile Müzakere", "effect": "karma:+10", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "betrayal_scene",
                    "title": "Rehberin İhaneti",
                    "description": "Güvendiğin rehber aslında ejderhaların hizmetkârıydı! Seni tuzağa düşürmek istiyor!",
                    "background": "/static/images/betrayal_scene.jpg",
                    "choices": [
                        {"id": "fight_traitor_guide", "text": "Hain Rehberle Savaş", "combat": True, "enemy": "Traitor Guide", "next_scene": "victory"},
                        {"id": "expose_traitor", "text": "Haini Açığa Çıkar", "effect": "buff:expose_bonus", "next_scene": "victory"},
                        {"id": "forgive_traitor", "text": "Haini Affet", "effect": "karma:+10", "next_scene": "victory"},
                        {"id": "use_truth_spell", "text": "Gerçek Büyüsü Kullan", "effect": "buff:truth_reveal", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "dragon_hunter_ancient_ruins",
                    "title": "Ejderha Avcısı Antik Harabeler",
                    "description": "Ejderha avcılarının antik harabelerine ulaştın. Burada kadim bilgiler var!",
                    "background": "/static/images/dragon_hunter_ancient_ruins.jpg",
                    "choices": [
                        {"id": "explore_ancient_ruins", "text": "Antik Harabeleri Keşfet", "effect": "item:ancient_knowledge, gain_xp:5", "next_scene": "dragon_hunter_crystal_cave"},
                        {"id": "fight_ruin_guardian", "text": "Harabe Bekçisi ile Savaş", "combat": True, "enemy": "Ruin Guardian", "next_scene": "dragon_hunter_crystal_cave"},
                        {"id": "study_ancient_lore", "text": "Antik Lore'u Öğren", "effect": "buff:ancient_lore", "next_scene": "dragon_hunter_crystal_cave"},
                        {"id": "collect_ancient_artifacts", "text": "Antik Artefaktları Topla", "effect": "item:ancient_artifacts", "next_scene": "dragon_hunter_crystal_cave"}
                    ]
                },
                {
                    "id": "dragon_hunter_crystal_cave",
                    "title": "Ejderha Avcısı Kristal Mağara",
                    "description": "Ejderha avcılarının kristal mağarasına ulaştın. Burada güçlü kristaller var!",
                    "background": "/static/images/dragon_hunter_crystal_cave.jpg",
                    "choices": [
                        {"id": "mine_crystals", "text": "Kristalleri Kaz", "effect": "item:dragon_crystals, gain_xp:4", "next_scene": "dragon_hunter_volcanic_forge"},
                        {"id": "fight_crystal_golem", "text": "Kristal Golem ile Savaş", "combat": True, "enemy": "Crystal Golem", "next_scene": "dragon_hunter_volcanic_forge"},
                        {"id": "study_crystal_lore", "text": "Kristal Lore'unu Öğren", "effect": "buff:crystal_lore", "next_scene": "dragon_hunter_volcanic_forge"},
                        {"id": "craft_crystal_weapon", "text": "Kristal Silah Yap", "effect": "item:crystal_weapon", "next_scene": "dragon_hunter_volcanic_forge"}
                    ]
                },
                {
                    "id": "dragon_hunter_volcanic_forge",
                    "title": "Ejderha Avcısı Volkanik Forge",
                    "description": "Ejderha avcılarının volkanik forge'una ulaştın. Burada güçlü silahlar dövülüyor!",
                    "background": "/static/images/dragon_hunter_volcanic_forge.jpg",
                    "choices": [
                        {"id": "forge_dragon_weapon", "text": "Ejderha Silahı Döv", "effect": "item:forged_dragon_weapon, gain_xp:5", "next_scene": "dragon_hunter_ice_citadel"},
                        {"id": "fight_forge_master", "text": "Forge Ustası ile Savaş", "combat": True, "enemy": "Forge Master", "next_scene": "dragon_hunter_ice_citadel"},
                        {"id": "learn_forge_lore", "text": "Forge Lore'unu Öğren", "effect": "buff:forge_lore", "next_scene": "dragon_hunter_ice_citadel"},
                        {"id": "study_forge_secrets", "text": "Forge Sırlarını İncele", "effect": "item:forge_secrets", "next_scene": "dragon_hunter_ice_citadel"}
                    ]
                },
                {
                    "id": "dragon_hunter_ice_citadel",
                    "title": "Ejderha Avcısı Buz Kalesi",
                    "description": "Ejderha avcılarının buz kalesine ulaştın. Burada buz ejderhaları var!",
                    "background": "/static/images/dragon_hunter_ice_citadel.jpg",
                    "choices": [
                        {"id": "fight_ice_dragon", "text": "Buz Ejderhası ile Savaş", "combat": True, "enemy": "Ice Dragon", "next_scene": "dragon_hunter_desert_oasis"},
                        {"id": "learn_ice_magic", "text": "Buz Büyüsünü Öğren", "effect": "buff:ice_magic, gain_xp:4", "next_scene": "dragon_hunter_desert_oasis"},
                        {"id": "study_ice_lore", "text": "Buz Lore'unu Öğren", "effect": "buff:ice_lore", "next_scene": "dragon_hunter_desert_oasis"},
                        {"id": "collect_ice_artifacts", "text": "Buz Artefaktlarını Topla", "effect": "item:ice_artifacts", "next_scene": "dragon_hunter_desert_oasis"}
                    ]
                },
                {
                    "id": "dragon_hunter_desert_oasis",
                    "title": "Ejderha Avcısı Çöl Vahası",
                    "description": "Ejderha avcılarının çöl vahasına ulaştın. Burada kum ejderhaları var!",
                    "background": "/static/images/dragon_hunter_desert_oasis.jpg",
                    "choices": [
                        {"id": "fight_sand_dragon", "text": "Kum Ejderhası ile Savaş", "combat": True, "enemy": "Sand Dragon", "next_scene": "dragon_hunter_underwater_city"},
                        {"id": "learn_sand_magic", "text": "Kum Büyüsünü Öğren", "effect": "buff:sand_magic, gain_xp:4", "next_scene": "dragon_hunter_underwater_city"},
                        {"id": "study_desert_lore", "text": "Çöl Lore'unu Öğren", "effect": "buff:desert_lore", "next_scene": "dragon_hunter_underwater_city"},
                        {"id": "collect_desert_artifacts", "text": "Çöl Artefaktlarını Topla", "effect": "item:desert_artifacts", "next_scene": "dragon_hunter_underwater_city"}
                    ]
                },
                {
                    "id": "dragon_hunter_underwater_city",
                    "title": "Ejderha Avcısı Sualtı Şehri",
                    "description": "Ejderha avcılarının sualtı şehrine ulaştın. Burada su ejderhaları var!",
                    "background": "/static/images/dragon_hunter_underwater_city.jpg",
                    "choices": [
                        {"id": "fight_water_dragon", "text": "Su Ejderhası ile Savaş", "combat": True, "enemy": "Water Dragon", "next_scene": "dragon_hunter_sky_fortress"},
                        {"id": "learn_water_magic", "text": "Su Büyüsünü Öğren", "effect": "buff:water_magic, gain_xp:4", "next_scene": "dragon_hunter_sky_fortress"},
                        {"id": "study_underwater_lore", "text": "Sualtı Lore'unu Öğren", "effect": "buff:underwater_lore", "next_scene": "dragon_hunter_sky_fortress"},
                        {"id": "collect_water_artifacts", "text": "Su Artefaktlarını Topla", "effect": "item:water_artifacts", "next_scene": "dragon_hunter_sky_fortress"}
                    ]
                },
                {
                    "id": "dragon_hunter_sky_fortress",
                    "title": "Ejderha Avcısı Gökyüzü Kalesi",
                    "description": "Ejderha avcılarının gökyüzü kalesine ulaştın. Burada rüzgar ejderhaları var!",
                    "background": "/static/images/dragon_hunter_sky_fortress.jpg",
                    "choices": [
                        {"id": "fight_wind_dragon", "text": "Rüzgar Ejderhası ile Savaş", "combat": True, "enemy": "Wind Dragon", "next_scene": "dragon_hunter_lightning_tower"},
                        {"id": "learn_wind_magic", "text": "Rüzgar Büyüsünü Öğren", "effect": "buff:wind_magic, gain_xp:4", "next_scene": "dragon_hunter_lightning_tower"},
                        {"id": "study_sky_lore", "text": "Gökyüzü Lore'unu Öğren", "effect": "buff:sky_lore", "next_scene": "dragon_hunter_lightning_tower"},
                        {"id": "collect_sky_artifacts", "text": "Gökyüzü Artefaktlarını Topla", "effect": "item:sky_artifacts", "next_scene": "dragon_hunter_lightning_tower"}
                    ]
                },
                {
                    "id": "dragon_hunter_lightning_tower",
                    "title": "Ejderha Avcısı Şimşek Kulesi",
                    "description": "Ejderha avcılarının şimşek kulesine ulaştın. Burada şimşek ejderhaları var!",
                    "background": "/static/images/dragon_hunter_lightning_tower.jpg",
                    "choices": [
                        {"id": "fight_lightning_dragon", "text": "Şimşek Ejderhası ile Savaş", "combat": True, "enemy": "Lightning Dragon", "next_scene": "dragon_hunter_poison_swamp"},
                        {"id": "learn_lightning_magic", "text": "Şimşek Büyüsünü Öğren", "effect": "buff:lightning_magic, gain_xp:4", "next_scene": "dragon_hunter_poison_swamp"},
                        {"id": "study_lightning_lore", "text": "Şimşek Lore'unu Öğren", "effect": "buff:lightning_lore", "next_scene": "dragon_hunter_poison_swamp"},
                        {"id": "collect_lightning_artifacts", "text": "Şimşek Artefaktlarını Topla", "effect": "item:lightning_artifacts", "next_scene": "dragon_hunter_poison_swamp"}
                    ]
                },
                {
                    "id": "dragon_hunter_poison_swamp",
                    "title": "Ejderha Avcısı Zehir Bataklığı",
                    "description": "Ejderha avcılarının zehir bataklığına ulaştın. Burada zehir ejderhaları var!",
                    "background": "/static/images/dragon_hunter_poison_swamp.jpg",
                    "choices": [
                        {"id": "fight_poison_dragon", "text": "Zehir Ejderhası ile Savaş", "combat": True, "enemy": "Poison Dragon", "next_scene": "dragon_hunter_ghost_manor"},
                        {"id": "learn_poison_magic", "text": "Zehir Büyüsünü Öğren", "effect": "buff:poison_magic, gain_xp:4", "next_scene": "dragon_hunter_ghost_manor"},
                        {"id": "study_poison_lore", "text": "Zehir Lore'unu Öğren", "effect": "buff:poison_lore", "next_scene": "dragon_hunter_ghost_manor"},
                        {"id": "collect_poison_artifacts", "text": "Zehir Artefaktlarını Topla", "effect": "item:poison_artifacts", "next_scene": "dragon_hunter_ghost_manor"}
                    ]
                },
                {
                    "id": "dragon_hunter_ghost_manor",
                    "title": "Ejderha Avcısı Hayalet Malikane",
                    "description": "Ejderha avcılarının hayalet malikanesine ulaştın. Burada hayalet ejderhaları var!",
                    "background": "/static/images/dragon_hunter_ghost_manor.jpg",
                    "choices": [
                        {"id": "fight_ghost_dragon", "text": "Hayalet Ejderhası ile Savaş", "combat": True, "enemy": "Ghost Dragon", "next_scene": "dragon_hunter_chaos_realm"},
                        {"id": "learn_ghost_magic", "text": "Hayalet Büyüsünü Öğren", "effect": "buff:ghost_magic, gain_xp:4", "next_scene": "dragon_hunter_chaos_realm"},
                        {"id": "study_ghost_lore", "text": "Hayalet Lore'unu Öğren", "effect": "buff:ghost_lore", "next_scene": "dragon_hunter_chaos_realm"},
                        {"id": "collect_ghost_artifacts", "text": "Hayalet Artefaktlarını Topla", "effect": "item:ghost_artifacts", "next_scene": "dragon_hunter_chaos_realm"}
                    ]
                },
                {
                    "id": "dragon_hunter_chaos_realm",
                    "title": "Ejderha Avcısı Kaos Alemi",
                    "description": "Ejderha avcılarının kaos alemine ulaştın. Burada kaos ejderhaları var!",
                    "background": "/static/images/dragon_hunter_chaos_realm.jpg",
                    "choices": [
                        {"id": "fight_chaos_dragon", "text": "Kaos Ejderhası ile Savaş", "combat": True, "enemy": "Chaos Dragon", "next_scene": "dragon_hunter_order_realm"},
                        {"id": "learn_chaos_magic", "text": "Kaos Büyüsünü Öğren", "effect": "buff:chaos_magic, gain_xp:4", "next_scene": "dragon_hunter_order_realm"},
                        {"id": "study_chaos_lore", "text": "Kaos Lore'unu Öğren", "effect": "buff:chaos_lore", "next_scene": "dragon_hunter_order_realm"},
                        {"id": "collect_chaos_artifacts", "text": "Kaos Artefaktlarını Topla", "effect": "item:chaos_artifacts", "next_scene": "dragon_hunter_order_realm"}
                    ]
                },
                {
                    "id": "dragon_hunter_order_realm",
                    "title": "Ejderha Avcısı Düzen Alemi",
                    "description": "Ejderha avcılarının düzen alemine ulaştın. Burada düzen ejderhaları var!",
                    "background": "/static/images/dragon_hunter_order_realm.jpg",
                    "choices": [
                        {"id": "fight_order_dragon", "text": "Düzen Ejderhası ile Savaş", "combat": True, "enemy": "Order Dragon", "next_scene": "dragon_hunter_time_temple"},
                        {"id": "learn_order_magic", "text": "Düzen Büyüsünü Öğren", "effect": "buff:order_magic, gain_xp:4", "next_scene": "dragon_hunter_time_temple"},
                        {"id": "study_order_lore", "text": "Düzen Lore'unu Öğren", "effect": "buff:order_lore", "next_scene": "dragon_hunter_time_temple"},
                        {"id": "collect_order_artifacts", "text": "Düzen Artefaktlarını Topla", "effect": "item:order_artifacts", "next_scene": "dragon_hunter_time_temple"}
                    ]
                },
                {
                    "id": "dragon_hunter_time_temple",
                    "title": "Ejderha Avcısı Zaman Tapınağı",
                    "description": "Ejderha avcılarının zaman tapınağına ulaştın. Burada zaman ejderhaları var!",
                    "background": "/static/images/dragon_hunter_time_temple.jpg",
                    "choices": [
                        {"id": "fight_time_dragon", "text": "Zaman Ejderhası ile Savaş", "combat": True, "enemy": "Time Dragon", "next_scene": "dragon_hunter_space_station"},
                        {"id": "learn_time_magic", "text": "Zaman Büyüsünü Öğren", "effect": "buff:time_magic, gain_xp:4", "next_scene": "dragon_hunter_space_station"},
                        {"id": "study_time_lore", "text": "Zaman Lore'unu Öğren", "effect": "buff:time_lore", "next_scene": "dragon_hunter_space_station"},
                        {"id": "collect_time_artifacts", "text": "Zaman Artefaktlarını Topla", "effect": "item:time_artifacts", "next_scene": "dragon_hunter_space_station"}
                    ]
                },
                {
                    "id": "dragon_hunter_space_station",
                    "title": "Ejderha Avcısı Uzay İstasyonu",
                    "description": "Ejderha avcılarının uzay istasyonuna ulaştın. Burada uzay ejderhaları var!",
                    "background": "/static/images/dragon_hunter_space_station.jpg",
                    "choices": [
                        {"id": "fight_space_dragon", "text": "Uzay Ejderhası ile Savaş", "combat": True, "enemy": "Space Dragon", "next_scene": "dragon_hunter_quantum_realm"},
                        {"id": "learn_space_magic", "text": "Uzay Büyüsünü Öğren", "effect": "buff:space_magic, gain_xp:4", "next_scene": "dragon_hunter_quantum_realm"},
                        {"id": "study_space_lore", "text": "Uzay Lore'unu Öğren", "effect": "buff:space_lore", "next_scene": "dragon_hunter_quantum_realm"},
                        {"id": "collect_space_artifacts", "text": "Uzay Artefaktlarını Topla", "effect": "item:space_artifacts", "next_scene": "dragon_hunter_quantum_realm"}
                    ]
                },
                {
                    "id": "dragon_hunter_quantum_realm",
                    "title": "Ejderha Avcısı Kuantum Alemi",
                    "description": "Ejderha avcılarının kuantum alemine ulaştın. Burada kuantum ejderhaları var!",
                    "background": "/static/images/dragon_hunter_quantum_realm.jpg",
                    "choices": [
                        {"id": "fight_quantum_dragon", "text": "Kuantum Ejderhası ile Savaş", "combat": True, "enemy": "Quantum Dragon", "next_scene": "dragon_hunter_plot_twist_scene"},
                        {"id": "learn_quantum_magic", "text": "Kuantum Büyüsünü Öğren", "effect": "buff:quantum_magic, gain_xp:4", "next_scene": "dragon_hunter_plot_twist_scene"},
                        {"id": "study_quantum_lore", "text": "Kuantum Lore'unu Öğren", "effect": "buff:quantum_lore", "next_scene": "dragon_hunter_plot_twist_scene"},
                        {"id": "collect_quantum_artifacts", "text": "Kuantum Artefaktlarını Topla", "effect": "item:quantum_artifacts", "next_scene": "dragon_hunter_plot_twist_scene"}
                    ]
                },
                {
                    "id": "dragon_hunter_plot_twist_scene",
                    "title": "Ejderha Sırrı",
                    "description": "Ejderhaların gerçek sırrını keşfettin! Bu bilgi tehlikeli ama güçlü!",
                    "background": "/static/images/plot_twist_scene.jpg",
                    "choices": [
                        {"id": "use_dragon_secret", "text": "Ejderha Sırrını Kullan", "effect": "buff:dragon_power, gain_xp:6", "next_scene": "victory"},
                        {"id": "hide_dragon_secret", "text": "Sırrı Gizle", "effect": "buff:stealth_bonus", "next_scene": "victory"},
                        {"id": "share_dragon_secret", "text": "Sırrı Paylaş", "effect": "ally:secret_keepers", "next_scene": "victory"},
                        {"id": "study_dragon_secret", "text": "Sırrı İncele", "effect": "item:dragon_knowledge", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "victory",
                    "title": "Zafer",
                    "description": "Pyraxis yere çakılıyor. Gökyüzü aydınlanıyor. Krallık seni kahraman ilan ediyor. Ejderha Avcısı unvanını kazandın!",
                    "choices": []
                },
                {
                    "id": "pyraxis_confrontation",
                    "title": "Pyraxis ile Yüzleşme",
                    "description": "Kuzey Dağları'nın zirvesinde Pyraxis karşında! Gözleri alev, nefesi ölüm. Bu senin en büyük sınavın!",
                    "background": "/static/images/dragon_lair.jpg",
                    "choices": [
                        {
                            "id": "final_battle",
                            "text": "Son Savaş",
                            "result": "Pyraxis ile epik final savaşı! Krallığın kaderi senin ellerinde!",
                            "next_scene": "boss_fight",
                            "combat": True,
                            "enemy": "Pyraxis - Alevin Efendisi"
                        },
                        {
                            "id": "negotiate",
                            "text": "Müzakere Et",
                            "result": "Pyraxis ile konuşmaya çalıştın ama başarısız oldun. Savaş kaçınılmaz!",
                            "next_scene": "boss_fight"
                        }
                    ]
                },
                {
                    "id": "escape",
                    "title": "Kaçış",
                    "description": "Hayatta kaldın, ancak Pyraxis geri döndü. Savaş başka bir gün için ertelendi. Suçluluk duygusu seni bırakmıyor... Fakat yolun bitmedi! Önünde yeni bölgeler ve maceralar var.",
                    "choices": [
                        {"id": "go_lost_forest", "text": "Kayıp Orman'a Git", "next_scene": "lost_forest"},
                        {"id": "go_ruined_village", "text": "Terkedilmiş Köy'e Git", "next_scene": "ruined_village"},
                        {"id": "go_temple", "text": "Kutsal Tapınak'a Git", "next_scene": "sacred_temple"},
                        {"id": "go_cave", "text": "Gizli Mağara'ya Git", "next_scene": "hidden_cave"}
                    ]
                },
                # --- Yeni bölgeler ve dallanan akışlar ---
                {
                    "id": "lost_forest",
                    "title": "Kayıp Orman",
                    "description": "Sisli, büyülü bir orman. Orman ruhları, goblinler ve gizemli bir büyücüyle karşılaşabilirsin.",
                    "background": "/static/images/forest.jpg",
                    "choices": [
                        {"id": "explore_forest", "text": "Ormanı Keşfet", "next_scene": "forest_encounter"},
                        {"id": "find_goblin", "text": "Goblinleri Ara", "result": "Bir goblinle karşılaştın, onunla savaşabilir veya dost olabilirsin.", "effect": "item:mushroom, gain_xp:2", "next_scene": "goblin_encounter"},
                        {"id": "return_escape", "text": "Kaçış Noktasına Dön", "effect": "item:herbs, gain_xp:1", "next_scene": "escape"}
                    ]
                },
                {
                    "id": "goblin_encounter",
                    "title": "Goblin Karşılaşması",
                    "description": "Bir goblinle karşılaştın. Savaşabilir, dost olabilir veya onu kandırabilirsin.",
                    "background": "/static/images/forest.jpg",
                    "choices": [
                        {"id": "fight_goblin", "text": "Goblinle Savaş", "result": "Goblin'i yendin, bir iksir ve XP kazandın.", "effect": "item:healing_potion, gain_xp:5", "combat": True, "enemy": "Goblin", "next_scene": "forest_encounter"},
                        {"id": "befriend_goblin", "text": "Goblinle Dost Ol", "result": "Goblin sana bir ipucu ve mantar verdi.", "effect": "item:mushroom, relationship:Goblin:+3, gain_xp:2", "next_scene": "forest_encounter"},
                        {"id": "trick_goblin", "text": "Goblin'i Kandır", "result": "Goblin'i kandırdın, altın ve XP kazandın.", "effect": "gain_gold:10, gain_xp:3", "next_scene": "forest_encounter"}
                    ]
                },
                {
                    "id": "goblin_reencounter",
                    "title": "Goblin ile Yeniden Karşılaşma",
                    "description": "Daha önce karşılaştığın goblin tekrar karşında. İlişkinize göre farklı tepki verecek.",
                    "background": "/static/images/forest.jpg",
                    "choices": [
                        {"id": "goblin_friend", "text": "Dostça Selamla (İlişki > 2)", "result": "Goblin seni dostça karşıladı ve gizli bir hazineye götürdü!", "effect": "item:rare_gem, gain_xp:10", "condition": "relationship:Goblin:>2", "next_scene": "forest_path"},
                        {"id": "goblin_neutral", "text": "Nötr Davran (İlişki -2 ile 2 arası)", "result": "Goblin seni selamladı, küçük bir ödül verdi.", "effect": "item:mushroom, gain_xp:3", "condition": "relationship:Goblin:>=-2,<=2", "next_scene": "forest_path"},
                        {"id": "goblin_hostile", "text": "Düşmanca Yaklaş (İlişki < -2)", "result": "Goblin sana saldırdı!", "effect": "combat:true, enemy:Goblin", "condition": "relationship:Goblin:<-2", "next_scene": "goblin_encounter"}
                    ]
                },
                {
                    "id": "ruined_village",
                    "title": "Terkedilmiş Köy",
                    "description": "Yıkık evler, hayatta kalanlar ve bir mini-boss ile karşılaşma şansı.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "search_village", "text": "Köyü Araştır", "next_scene": "village_encounter"},
                        {"id": "help_survivors", "text": "Hayatta Kalanlara Yardım Et", "result": "Bir çocuğu kurtardın, köylüler sana minnettar. Bir iksir ve XP kazandın.", "effect": "item:healing_potion, gain_xp:5, relationship:Villagers:+3", "next_scene": "village_encounter"},
                        {"id": "return_escape", "text": "Kaçış Noktasına Dön", "effect": "item:apple, gain_xp:1", "next_scene": "escape"}
                    ]
                },
                {
                    "id": "village_encounter",
                    "title": "Köyde Karşılaşma",
                    "description": "Köy meydanında bir mini-boss olan 'Kara Şövalye' ve yaşlı bir bilgeyle karşılaştın.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "fight_black_knight", "text": "Kara Şövalye ile Savaş", "result": "Kara Şövalye'yi yendin, özel bir zırh ve XP kazandın.", "effect": "item:black_armor, gain_xp:20", "combat": True, "enemy": "Kara Şövalye", "next_scene": "werewolf_confrontation"},
                        {"id": "talk_scholar", "text": "Yaşlı Bilgeyle Konuş", "result": "Bilge sana bir bilmece sordu. Doğru cevaplarsan büyülü bir kitap kazanırsın!", "effect": "item:spellbook, gain_xp:10", "next_scene": "old_scholar"},
                        {"id": "help_villagers", "text": "Köylülere Yardım Et", "result": "Köylüler sana minnettarlıkla bir anahtar ve XP verdi.", "effect": "item:old_key, gain_xp:5, relationship:Villagers:+2", "next_scene": "old_scholar"}
                    ]
                },
                {
                    "id": "druid_reencounter",
                    "title": "Druid Thalya ile Yeniden Karşılaşma",
                    "description": "Ormanda Thalya ile tekrar karşılaştın. Önceki seçimlerine göre sana farklı davranacak.",
                    "background": "/static/images/forest.jpg",
                    "choices": [
                        {"id": "druid_grateful", "text": "Thalya'nın Minnettarlığı (İlişki > 2)", "result": "Thalya sana özel bir iksir ve büyülü bir tılsım verdi.", "effect": "item:magic_amulet, item:healing_potion, gain_xp:8", "condition": "relationship:Druid:>2", "next_scene": "lost_forest"},
                        {"id": "druid_neutral", "text": "Thalya ile Sohbet Et (İlişki -2 ile 2 arası)", "result": "Thalya ile sohbet ettin, küçük bir bilgi verdi.", "effect": "gain_xp:2", "condition": "relationship:Druid:>=-2,<=2", "next_scene": "lost_forest"},
                        {"id": "druid_hostile", "text": "Thalya'nın Düşmanlığı (İlişki < -2)", "result": "Thalya sana büyüyle saldırdı!", "effect": "combat:true, enemy:Druid", "condition": "relationship:Druid:<-2", "next_scene": "forest_encounter"}
                    ]
                },
                {
                    "id": "sacred_temple",
                    "title": "Kutsal Tapınak",
                    "description": "Büyülü tuzaklar, rahipler ve kutsal bir eşya. Belki de bir yan görev.",
                    "background": "/static/images/temple.jpg",
                    "choices": [
                        {"id": "explore_temple", "text": "Tapınağı Keşfet", "next_scene": "temple_encounter"},
                        {"id": "pray", "text": "Dua Et", "result": "Duan kabul edildi, 10 XP kazandın ve tapınaktan huzurla ayrıldın.", "effect": "gain_xp:10", "next_scene": "escape"},
                        {"id": "return_escape", "text": "Kaçış Noktasına Dön", "effect": "item:herbs, gain_xp:1", "next_scene": "escape"}
                    ]
                },
                {
                    "id": "temple_encounter",
                    "title": "Tapınakta Karşılaşma",
                    "description": "Tapınakta bir rahip, bir büyülü tuzak ve kutsal bir sandık var.",
                    "background": "/static/images/temple.jpg",
                    "choices": [
                        {"id": "help_priest", "text": "Rahibe Yardım Et", "result": "Rahip sana kutsal bir kalkan verdi ve 50 XP kazandın!", "effect": "gain_xp:50, item:holy_shield", "next_scene": "holy_temple"},
                        {"id": "disarm_magic_trap", "text": "Büyülü Tuzağı Etkisizleştir", "result": "Tuzağı etkisizleştirdin, kutsal sandığı açabilirsin.", "effect": "gain_xp:10", "next_scene": "holy_temple"},
                        {"id": "open_holy_chest", "text": "Kutsal Sandığı Aç", "result": "Sandıktan kutsal bir asa ve XP kazandın.", "effect": "item:holy_staff, gain_xp:20", "next_scene": "holy_temple"}
                    ]
                },
                {
                    "id": "holy_temple",
                    "title": "Kutsal Tapınak",
                    "description": "Beyaz taşlardan yapılmış, ışıkla dolu bir tapınak. İçeride bir rahip seni bekliyor.",
                    "background": "/static/images/temple.jpg",
                    "choices": [
                        {
                            "id": "help_priest",
                            "text": "Rahibe Yardım Et",
                            "result": "Rahip sana kutsal bir kalkan verdi ve 50 XP kazandın!",
                            "effect": "gain_xp:50, item:holy_shield",
                            "scene_end": True,
                            "next_scene": "escape"
                        },
                        {
                            "id": "steal_relic",
                            "text": "Kutsal Eşyayı Çal",
                            "result": "Kutsal eşyayı çaldın ama lanetlendin! 20 XP kaybettin.",
                            "effect": "lose_xp:20, item:cursed_relic",
                            "scene_end": True,
                            "next_scene": "escape"
                        },
                        {
                            "id": "pray",
                            "text": "Dua Et",
                            "result": "Duan kabul edildi, 10 XP kazandın ve tapınaktan huzurla ayrıldın.",
                            "effect": "gain_xp:10",
                            "scene_end": True,
                            "next_scene": "escape"
                        }
                    ]
                },
                {
                    "id": "forest_encounter",
                    "title": "Ormanda Karşılaşma",
                    "description": "Karanlık ormanda sisli patikada ilerlerken eski bir druid olan 'Thalya' ile karşılaşırsın.",
                    "background": "/static/images/forest.jpg",
                    "choices": [
                        {
                            "id": "help_druid",
                            "text": "Druid'e yardım teklif et (İyi)",
                            "result": "Thalya sana minnettarlıkla bir iksir verir. Saygısını kazandın.",
                            "effect": "gain_potion, gain_xp:2",
                            "npc_reaction": "minör buff + saygı kazanılır",
                            "next_scene": "lost_forest"
                        },
                        {
                            "id": "ignore_druid",
                            "text": "Druid'i görmezden gel (Nötr)",
                            "result": "Yoluna devam ediyorsun. Ormanda bir mantar buldun.",
                            "effect": "item:mushroom, gain_xp:1",
                            "next_scene": "lost_forest"
                        },
                        {
                            "id": "steal_druid",
                            "text": "Druid'in malzemelerini çal (Kötü)",
                            "result": "Thalya seni fark etmeden bazı otları çaldın. Ancak güvenini kaybettin.",
                            "effect": "gain_item:herbs, lose_npc_trust, gain_xp:1",
                            "npc_reaction": "gelecekte yardım etmez",
                            "next_scene": "lost_forest"
                        }
                    ]
                },
                {
                    "id": "mysterious_traveler",
                    "title": "Gizemli Yolcu",
                    "description": "Ormanda bir ateş başında oturan pelerinli bir yolcu ile karşılaştın. Gözleri parlıyor, elinde eski bir harita var.",
                    "background": "/static/images/forest.jpg",
                    "choices": [
                        {
                            "id": "talk_traveler",
                            "text": "Yolcu ile konuş",
                            "result": "Yolcu sana eski bir harita verdi. Yeni bir gizli bölge açıldı!",
                            "effect": "item:ancient_map, gain_xp:10",
                            "next_scene": "forest_path"
                        },
                        {
                            "id": "threaten_traveler",
                            "text": "Yolcuyu tehdit et",
                            "result": "Yolcu korktu ve sana bir iksir verdi, sonra kaçtı.",
                            "effect": "item:mysterious_potion, gain_xp:5",
                            "next_scene": "forest_path"
                        },
                        {
                            "id": "ignore_traveler",
                            "text": "Yolcuyu görmezden gel",
                            "result": "Yoluna devam ettin, yolun kenarında bir elma buldun.",
                            "effect": "item:apple, gain_xp:1",
                            "next_scene": "forest_path"
                        }
                    ]
                },
                {
                    "id": "merchant_encounter",
                    "title": "Gezgin Tüccar",
                    "description": "Yolda bir tüccar arabasıyla karşılaştın. Tüccar sana gülümseyerek yaklaşıyor.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {
                            "id": "buy_potion",
                            "text": "İksir satın al (20 altın)",
                            "result": "20 altın karşılığında bir iyileştirme iksiri aldın.",
                            "effect": "lose_gold:20, item:healing_potion",
                            "next_scene": "forest_path"
                        },
                        {
                            "id": "haggle_merchant",
                            "text": "Pazarlık yap",
                            "result": "Tüccar fiyatı düşürdü! 10 altına bir iksir aldın.",
                            "effect": "lose_gold:10, item:healing_potion, gain_xp:2",
                            "next_scene": "forest_path"
                        },
                        {
                            "id": "rob_merchant",
                            "text": "Tüccarı soy",
                            "result": "Tüccarı soydun, 50 altın ve rastgele bir eşya aldın. Ama kötü şöhret kazandın!",
                            "effect": "gain_gold:50, item:random_loot, lose_xp:5",
                            "next_scene": "forest_path"
                        },
                        {
                            "id": "help_merchant",
                            "text": "Tüccara yardım et",
                            "result": "Tüccar sana minnettar kaldı ve özel bir tılsım verdi.",
                            "effect": "item:charm_of_gratitude, gain_xp:8",
                            "next_scene": "forest_path"
                        }
                    ]
                },
                {
                    "id": "old_scholar",
                    "title": "Yaşlı Bilge",
                    "description": "Köy meydanında eski kitaplar satan yaşlı bir bilgeyle karşılaştın. Sana bir bilmece sordu.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {
                            "id": "answer_riddle_right",
                            "text": "Doğru cevap ver",
                            "result": "Bilge sana bir büyü kitabı ve 15 XP verdi!",
                            "effect": "item:spellbook, gain_xp:15",
                            "next_scene": "ruined_village"
                        },
                        {
                            "id": "answer_riddle_wrong",
                            "text": "Yanlış cevap ver",
                            "result": "Bilge başını salladı ve seni uyardı. 5 XP kaybettin ama eski bir taş buldun.",
                            "effect": "lose_xp:5, item:old_stone",
                            "next_scene": "ruined_village"
                        },
                        {
                            "id": "buy_book",
                            "text": "Kitap satın al (30 altın)",
                            "result": "30 altına eski bir kitap aldın. Bilge sana bir ipucu verdi.",
                            "effect": "lose_gold:30, gain_xp:5, item:clue_scroll",
                            "next_scene": "ruined_village"
                        }
                    ]
                },
                {
                    "id": "blacksmith_event",
                    "title": "Demirciyle Anlaşma",
                    "description": "Köyün demircisi sana özel bir silah teklif ediyor. Ama karşılığında yardım istiyor.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {
                            "id": "help_blacksmith",
                            "text": "Demirciye yardım et",
                            "result": "Demirci sana özel bir kılıç yaptı ve saldırı buff'ı kazandın!",
                            "effect": "item:special_sword, buff:attack_up, relationship:Blacksmith:+5",
                            "next_scene": "ruined_village"
                        },
                        {
                            "id": "refuse_blacksmith",
                            "text": "Yardımı reddet",
                            "result": "Demirci kırıldı, ünün azaldı.",
                            "effect": "reputation:-5, relationship:Blacksmith:-5",
                            "next_scene": "ruined_village"
                        }
                    ]
                },
                {
                    "id": "blacksmith_reencounter",
                    "title": "Demirci ile Yeniden Karşılaşma",
                    "description": "Köyde demirciyle tekrar karşılaştın. İlişkinize göre sana özel bir silah veya ceza verebilir.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "blacksmith_gift", "text": "Demircinin Hediyesi (İlişki > 2)", "result": "Demirci sana efsanevi bir kılıç verdi!", "effect": "item:legendary_sword, gain_xp:12", "condition": "relationship:Blacksmith:>2", "next_scene": "ruined_village"},
                        {"id": "blacksmith_neutral", "text": "Demirciyle Sohbet Et (İlişki -2 ile 2 arası)", "result": "Demirciyle sohbet ettin, küçük bir ipucu verdi.", "effect": "gain_xp:2", "condition": "relationship:Blacksmith:>=-2,<=2", "next_scene": "ruined_village"},
                        {"id": "blacksmith_hostile", "text": "Demircinin Düşmanlığı (İlişki < -2)", "result": "Demirci sana eski bir silah verdi ve köyden kovdu.", "effect": "item:rusty_sword, lose_xp:3", "condition": "relationship:Blacksmith:<-2", "next_scene": "ruined_village"}
                    ]
                },
                {
                    "id": "poisoned_well",
                    "title": "Zehirli Kuyu",
                    "description": "Köydeki kuyuya birinin zehir attığı söyleniyor. Araştırmak ister misin?",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {
                            "id": "investigate_well",
                            "text": "Kuyuyu araştır",
                            "result": "Kuyudan çıkan gazdan etkilendin, zehirlendin! Ama köylülerin güvenini kazandın.",
                            "effect": "debuff:poisoned, reputation:+10",
                            "next_scene": "ruined_village"
                        },
                        {
                            "id": "ignore_well",
                            "text": "Kuyuyu görmezden gel",
                            "result": "Köylüler sana biraz soğuk bakıyor.",
                            "effect": "reputation:-2",
                            "next_scene": "ruined_village"
                        }
                    ]
                },
                {
                    "id": "bard_encounter",
                    "title": "Gezgin Ozan",
                    "description": "Bir ozan köy meydanında şarkı söylüyor. Ona katılmak ister misin?",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {
                            "id": "sing_with_bard",
                            "text": "Ozanla şarkı söyle",
                            "result": "Harika bir performans sergiledin! Ünün arttı, moral buff'ı kazandın.",
                            "effect": "reputation:+7, buff:moral_boost, relationship:Bard:+3",
                            "next_scene": "ruined_village"
                        },
                        {
                            "id": "insult_bard",
                            "text": "Ozanı aşağıla",
                            "result": "Ozan ve köylüler sana kızdı, ünün azaldı.",
                            "effect": "reputation:-8, relationship:Bard:-5",
                            "next_scene": "ruined_village"
                        }
                    ]
                },
                {
                    "id": "bard_reencounter",
                    "title": "Ozan ile Yeniden Karşılaşma",
                    "description": "Köy meydanında ozanla tekrar karşılaştın. İlişkinize göre sana özel bir şarkı veya ceza verebilir.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "bard_song", "text": "Ozanın Özel Şarkısı (İlişki > 2)", "result": "Ozan sana özel bir şarkı söyledi, moralin ve XP'n arttı.", "effect": "buff:moral_boost, gain_xp:7", "condition": "relationship:Bard:>2", "next_scene": "ruined_village"},
                        {"id": "bard_neutral", "text": "Ozanla Sohbet Et (İlişki -2 ile 2 arası)", "result": "Ozanla sohbet ettin, küçük bir bilgi verdi.", "effect": "gain_xp:2", "condition": "relationship:Bard:>=-2,<=2", "next_scene": "ruined_village"},
                        {"id": "bard_hostile", "text": "Ozanın Düşmanlığı (İlişki < -2)", "result": "Ozan seni köylülere kötüledi, ünün azaldı.", "effect": "reputation:-5, lose_xp:2", "condition": "relationship:Bard:<-2", "next_scene": "ruined_village"}
                    ]
                },
                {
                    "id": "forest_fairy_event",
                    "title": "Orman Perisi'nin Lütfu",
                    "description": "Ormanda ilerlerken, daha önce yaptığın iyilikler sayesinde Orman Perisi ortaya çıkıyor. Sana sihirli bir tılsım ve koruyucu bir büyü veriyor.",
                    "background": "/static/images/forest.jpg",
                    "choices": [
                        {
                            "id": "accept_fairy_gift",
                            "text": "Perinin hediyesini kabul et",
                            "result": "Orman Perisi sana 'fairy_charm' verdi ve koruyucu büyüyle kutsadı.",
                            "effect": "item:fairy_charm, buff:fairy_protection",
                            "next_scene": "forest_path"
                        },
                        {
                            "id": "thank_fairy",
                            "text": "Periye teşekkür et",
                            "result": "Peri sana minnettarlıkla gülümsedi. İçin huzurla doldu.",
                            "effect": "buff:calm_mind",
                            "next_scene": "forest_path"
                        }
                    ]
                },
                {
                    "id": "join_pyraxis_ending",
                    "title": "Karanlık Tarafın Zaferi",
                    "description": "Kötü seçimlerin sonucunda Pyraxis'in yanında yer aldın. Krallık karanlığa gömüldü, sen ise Pyraxis'in sağ kolu oldun. Artık yeni bir çağ başlıyor... kötülüğün çağı.",
                    "choices": []
                },
                {
                    "id": "victory_evil",
                    "title": "Karanlık Zafer",
                    "description": "Kötü seçimler yaptın ama Pyraxis'e karşı savaştın. Brakk'ın yardımıyla Pyraxis'i yendin. Krallık seni korkuyla anacak, ama kötülüğün gölgesi hâlâ peşinde.",
                    "choices": []
                },
                {
                    "id": "victory_neutral",
                    "title": "Yalnız Kahraman",
                    "description": "Ne iyi ne kötü oldun, kendi yolunu seçtin. Pyraxis'i tek başına yendin. Krallık seni saygıyla anacak, ama yalnızlığın gölgesi hep yanında olacak.",
                    "choices": []
                },
                {
                    "id": "victory_good_fairy",
                    "title": "Işığın Zaferi",
                    "description": "Tüm seçimlerinde iyiliği seçtin. Orman Perisi'nin yardımıyla Pyraxis'i yendin. Krallık aydınlandı, adın efsane oldu. Doğa ve insanlar sana minnettar.",
                    "choices": []
                },
                {
                    "id": "heroic_sacrifice",
                    "title": "Kahramanca Fedakarlık",
                    "description": "Pyraxis'i yenmek için son gücünü kullandın ve kendini feda ettin. Krallık kurtuldu, adın efsane oldu. Ama senin hikayen burada sona erdi.",
                    "choices": []
                },
                {
                    "id": "deal_with_pyraxis",
                    "title": "Ejderha ile Anlaşma",
                    "description": "Pyraxis ile bir anlaşma yaptın. Krallığın bir kısmı ejderhaya bırakıldı, kalanlar ise barış içinde yaşadı. Ne tam zafer, ne tam yenilgi.",
                    "choices": []
                },
                {
                    "id": "redemption_ending",
                    "title": "Merhametin Gücü",
                    "description": "Pyraxis'e merhamet gösterdin ve onu iyileştirdin. Ejderha, krallığın koruyucusu oldu. Barış ve umut çağı başladı.",
                    "choices": []
                },
                {
                    "id": "escape_ending",
                    "title": "Kaçış",
                    "description": "Pyraxis ile yüzleşmekten vazgeçtin ve kaçtın. Krallık karanlığa gömüldü, ama sen hayatta kaldın. Vicdanınla baş başa kaldın.",
                    "choices": []
                },
                {
                    "id": "cursed_ending",
                    "title": "Lanetli Zafer",
                    "description": "Pyraxis'i yendin ama yasak güçler kullandığın için lanetlendin. Krallık kurtuldu, ama sen sonsuz bir yalnızlığa mahkum oldun.",
                    "choices": []
                },
                # YENİ SAHNE: Haydut Saldırısı
                {
                    "id": "bandit_fight",
                    "title": "Haydut Saldırısı",
                    "description": "Köy çıkışında bir grup haydut yolunu kesti. Savaş başlıyor! (Tur bazlı, skill seçmeli savaş)",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {
                            "id": "fight_bandits",
                            "text": "Savaş!",
                            "result": "Haydutlarla tur bazlı skill seçmeli bir savaşa girdin.",
                            "combat": True,
                            "enemy": "Haydut",
                            "next_scene": "bandit_leader_confrontation"
                        }
                    ]
                },
                # YENİ SAHNE: Orman Ruh Lideri
                {
                    "id": "forest_spirit_boss",
                    "title": "Orman Ruh Lideri",
                    "description": "Ormanın derinliklerinde, ruh lideriyle karşılaştın. Savaş başlıyor! (Tur bazlı, skill seçmeli savaş)",
                    "background": "/static/images/forest.jpg",
                    "choices": [
                        {
                            "id": "fight_forest_spirit",
                            "text": "Savaş!",
                            "result": "Orman Ruh Lideri ile tur bazlı skill seçmeli bir savaşa girdin.",
                            "combat": True,
                            "enemy": "Orman Ruhu",
                            "next_scene": "mountain_troll_confrontation"
                        }
                    ]
                },
                # YENİ SAHNE: Dağ Trolü
                {
                    "id": "mountain_troll_boss",
                    "title": "Dağ Trolü",
                    "description": "Dağ geçidinde dev bir trol yolunu kesti. Savaş başlıyor! (Tur bazlı, skill seçmeli savaş)",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {
                            "id": "fight_mountain_troll",
                            "text": "Savaş!",
                            "result": "Dağ Trolü ile tur bazlı skill seçmeli bir savaşa girdin.",
                            "combat": True,
                            "enemy": "Dağ Trolü",
                            "next_scene": "ancient_ruins"
                        }
                    ]
                },
                # YENİ SAHNE: Ruh Bekçisi
                {
                    "id": "spirit_guardian_boss",
                    "title": "Ruh Bekçisi",
                    "description": "Kadim harabelerde bir ruh bekçisiyle karşılaştın. Savaş başlıyor! (Tur bazlı, skill seçmeli savaş)",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {
                            "id": "fight_spirit_guardian",
                            "text": "Savaş!",
                            "result": "Ruh Bekçisi ile tur bazlı skill seçmeli bir savaşa girdin.",
                            "combat": True,
                            "enemy": "Ruh Bekçisi",
                            "next_scene": "final_pyraxis_prep"
                        }
                    ]
                },
                {
                    "id": "pyraxis_boss_fight",
                    "title": "Pyraxis ile Büyük Savaş",
                    "description": "Sonunda Pyraxis'in mağarasına ulaştın. Büyük final başlıyor! (Tur bazlı, skill seçmeli savaş)",
                    "background": "/static/images/pyraxisfam.jpg",
                    "choices": [
                        {
                            "id": "fight_pyraxis",
                            "text": "Pyraxis ile savaş!",
                            "result": "Pyraxis ile tur bazlı skill seçmeli büyük bir savaşa girdin.",
                            "combat": True,
                            "enemy": "Pyraxis",
                            "next_scene": "boss_fight"
                        }
                    ]
                },
                {
                    "id": "forest_path_puzzle",
                    "title": "Orman Yolu Bulmacası",
                    "description": "Yolun ortasında eski bir taş anıt ve üzerinde bir bilmece var. Çözersen ödül kazanırsın.",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {"id": "solve_puzzle", "text": "Bilmecenin Cevabını Dene", "result": "Doğru cevabı verdin! Gizli bir bölme açıldı, bir iksir ve XP kazandın.", "effect": "item:healing_potion, gain_xp:7", "next_scene": "mountain_pass"},
                        {"id": "fail_puzzle", "text": "Yanlış Cevap Ver", "result": "Yanlış cevap verdin, tuzak tetiklendi ve HP kaybettin.", "effect": "lose_hp:8, gain_xp:1", "next_scene": "mountain_pass"}
                    ]
                },
                {
                    "id": "mountain_pass_miniboss",
                    "title": "Dağ Geçidi Mini-Boss",
                    "description": "Geçitte dev bir taş golemi yolunu kesti. Savaşmak ya da zekanla alt etmek mümkün.",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {"id": "fight_golem", "text": "Goleme Saldır", "result": "Taş golemini yendin, değerli bir taş ve XP kazandın.", "effect": "item:rare_gem, gain_xp:15", "combat": True, "enemy": "Taş Golemi", "next_scene": "mountain_troll_confrontation"},
                        {"id": "outsmart_golem", "text": "Golemi Kandır", "result": "Golemi zekanla kandırdın, yolun açıldı ve XP kazandın.", "effect": "gain_xp:10", "next_scene": "mountain_troll_confrontation"}
                    ]
                },
                {
                    "id": "ancient_ruins_puzzle",
                    "title": "Kadim Harabeler Bulmacası",
                    "description": "Harabelerde eski bir yazıt var. Doğru çözersen gizli bir oda açılır.",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {"id": "solve_ruins_puzzle", "text": "Yazıtı Çöz", "result": "Yazıtı çözdün, gizli odadan büyülü bir asa ve XP kazandın.", "effect": "item:magic_staff, gain_xp:12", "next_scene": "spirit_guardian_confrontation"},
                        {"id": "fail_ruins_puzzle", "text": "Yanlış Deneme", "result": "Yanlış denedin, tuzak tetiklendi ve HP kaybettin.", "effect": "lose_hp:10, gain_xp:1", "next_scene": "spirit_guardian_confrontation"}
                    ]
                },
                {
                    "id": "hidden_cave_miniboss",
                    "title": "Gizli Mağara Mini-Boss",
                    "description": "Mağaranın derinliklerinde dev bir örümcek var. Savaşabilir veya tuzak kurabilirsin.",
                    "background": "/static/images/cave.jpg",
                    "choices": [
                        {"id": "fight_spider", "text": "Dev Örümcekle Savaş", "result": "Dev örümceği yendin, zehirli diş ve XP kazandın.", "effect": "item:spider_fang, gain_xp:14", "combat": True, "enemy": "Dev Örümcek", "next_scene": "spider_confrontation"},
                        {"id": "set_trap", "text": "Tuzak Kur", "result": "Tuzak kurdun, örümceği tuzağa düşürdün ve XP kazandın.", "effect": "gain_xp:8, item:web_silk", "next_scene": "spider_confrontation"}
                    ]
                },
                {
                    "id": "sacred_temple_miniboss",
                    "title": "Kutsal Tapınak Mini-Boss",
                    "description": "Tapınağın kutsal odasında bir hayalet muhafız var. Savaşabilir veya dua ederek yatıştırabilirsin.",
                    "background": "/static/images/temple.jpg",
                    "choices": [
                        {"id": "fight_ghost_guardian", "text": "Hayalet Muhafızla Savaş", "result": "Hayalet muhafızı yendin, kutsal bir tılsım ve XP kazandın.", "effect": "item:holy_amulet, gain_xp:16", "combat": True, "enemy": "Hayalet Muhafız", "next_scene": "ghost_guardian_confrontation"},
                        {"id": "pray_for_peace", "text": "Dua Et ve Yatıştır", "result": "Duan kabul edildi, hayalet huzura kavuştu ve XP kazandın.", "effect": "gain_xp:10, item:blessed_scroll", "next_scene": "holy_temple"}
                    ]
                },
                {
                    "id": "burned_village_puzzle",
                    "title": "Yanık Köy Bulmacası",
                    "description": "Köyde yıkıntılar arasında eski bir sandık ve üzerinde bir bilmece var.",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {"id": "solve_burned_puzzle", "text": "Bilmecenin Cevabını Dene", "result": "Doğru cevabı verdin! Sandıktan altın ve XP kazandın.", "effect": "gain_gold:30, gain_xp:6", "next_scene": "forest_path"},
                        {"id": "fail_burned_puzzle", "text": "Yanlış Cevap Ver", "result": "Yanlış cevap verdin, sandık tuzaklı çıktı ve HP kaybettin.", "effect": "lose_hp:7, gain_xp:1", "next_scene": "forest_path"}
                    ]
                },
                {
                    "id": "new_ally_miniboss",
                    "title": "Yeni Müttefik Mini-Boss",
                    "description": "Borin ile ilerlerken bir mağara trolü yolunu kesti. Savaş ya da Borin ile birlikte tuzak kur.",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {"id": "fight_troll", "text": "Trol ile Savaş", "result": "Trolü yendiniz, Borin ile birlikte XP ve ödül kazandınız.", "effect": "item:troll_club, gain_xp:13", "combat": True, "enemy": "Mağara Trolü", "next_scene": "forest_path"},
                        {"id": "set_trap_with_borin", "text": "Borin ile Tuzak Kur", "result": "Trolü tuzağa düşürdünüz, XP ve altın kazandınız.", "effect": "gain_xp:8, gain_gold:15", "next_scene": "forest_path"}
                    ]
                },
                {
                    "id": "safe_route_puzzle",
                    "title": "Güvenli Rota Bulmacası",
                    "description": "Yol kenarında eski bir taşta bir bilmece var. Çözersen ödül kazanırsın.",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {"id": "solve_safe_puzzle", "text": "Bilmecenin Cevabını Dene", "result": "Doğru cevabı verdin! Bir iksir ve XP kazandın.", "effect": "item:healing_potion, gain_xp:5", "next_scene": "forest_path"},
                        {"id": "fail_safe_puzzle", "text": "Yanlış Cevap Ver", "result": "Yanlış cevap verdin, tuzak tetiklendi ve HP kaybettin.", "effect": "lose_hp:5, gain_xp:1", "next_scene": "forest_path"}
                    ]
                },
                {
                    "id": "early_fight_miniboss",
                    "title": "Erken Karşılaşma Mini-Boss",
                    "description": "Pyraxis'in gölgesinde bir alev ruhu ortaya çıktı. Savaş ya da kaç.",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {"id": "fight_fire_spirit", "text": "Alev Ruhu ile Savaş", "result": "Alev ruhunu yendin, ateş kristali ve XP kazandın.", "effect": "item:fire_crystal, gain_xp:11", "combat": True, "enemy": "Alev Ruhu", "next_scene": "safe_route"},
                        {"id": "escape_fire_spirit", "text": "Kaç", "result": "Alev ruhundan kaçtın, az da olsa XP kazandın.", "effect": "gain_xp:2", "next_scene": "safe_route"}
                    ]
                },
                {
                    "id": "orc_fight_puzzle",
                    "title": "Ork Savaşı Bulmacası",
                    "description": "Ork lideri Grug, savaş öncesi bir bilmece soruyor. Doğru cevaplarsan avantaj kazanırsın.",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {"id": "solve_ork_puzzle", "text": "Bilmecenin Cevabını Dene", "result": "Doğru cevabı verdin, savaşta avantaj kazandın ve XP aldın.", "effect": "buff:attack_up, gain_xp:6", "next_scene": "orc_fight"},
                        {"id": "fail_ork_puzzle", "text": "Yanlış Cevap Ver", "result": "Yanlış cevap verdin, Grug seni küçümsedi ama XP kazandın.", "effect": "gain_xp:2", "next_scene": "orc_fight"}
                    ]
                },
                {
                    "id": "spirit_guardian_boss_puzzle",
                    "title": "Ruh Bekçisi Bulmacası",
                    "description": "Ruh Bekçisi savaş öncesi bir bilmece soruyor. Doğru cevaplarsan savaşta avantaj kazanırsın.",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {"id": "solve_spirit_puzzle", "text": "Bilmecenin Cevabını Dene", "result": "Doğru cevabı verdin, savaşta avantaj kazandın ve XP aldın.", "effect": "buff:defense_up, gain_xp:7", "next_scene": "spirit_guardian_boss"},
                        {"id": "fail_spirit_puzzle", "text": "Yanlış Cevap Ver", "result": "Yanlış cevap verdin, ruh bekçisi seni küçümsedi ama XP kazandın.", "effect": "gain_xp:2", "next_scene": "spirit_guardian_boss"}
                    ]
                },
                {
                    "id": "bandit_fight_miniboss",
                    "title": "Haydut Saldırısı Mini-Boss",
                    "description": "Haydutların lideriyle savaş ya da onu kandır.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "fight_bandit_leader", "text": "Haydut Lideriyle Savaş", "result": "Haydut liderini yendin, değerli bir yüzük ve XP kazandın.", "effect": "item:bandit_ring, gain_xp:12", "combat": True, "enemy": "Haydut Lideri", "next_scene": "forest_path"},
                        {"id": "trick_bandit_leader", "text": "Haydut Liderini Kandır", "result": "Lideri kandırdın, altın ve XP kazandın.", "effect": "gain_gold:20, gain_xp:6", "next_scene": "forest_path"}
                    ]
                },
                {
                    "id": "forest_spirit_boss_puzzle",
                    "title": "Orman Ruh Lideri Bulmacası",
                    "description": "Orman ruhu savaş öncesi bir bilmece soruyor. Doğru cevaplarsan avantaj kazanırsın.",
                    "background": "/static/images/forest.jpg",
                    "choices": [
                        {"id": "solve_forest_spirit_puzzle", "text": "Bilmecenin Cevabını Dene", "result": "Doğru cevabı verdin, savaşta avantaj kazandın ve XP aldın.", "effect": "buff:magic_up, gain_xp:7", "next_scene": "forest_spirit_confrontation"},
                        {"id": "fail_forest_spirit_puzzle", "text": "Yanlış Cevap Ver", "result": "Yanlış cevap verdin, orman ruhu seni küçümsedi ama XP kazandın.", "effect": "gain_xp:2", "next_scene": "forest_spirit_confrontation"}
                    ]
                },
                {
                    "id": "village_encounter_miniboss",
                    "title": "Köyde Mini-Boss",
                    "description": "Köy meydanında bir kurt adam ortaya çıktı. Savaş ya da köylülerle birlikte tuzak kur.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "fight_werewolf", "text": "Kurt Adamla Savaş", "result": "Kurt adamı yendin, gümüş pençe ve XP kazandın.", "effect": "item:silver_claw, gain_xp:13", "combat": True, "enemy": "Kurt Adam", "next_scene": "old_scholar"},
                        {"id": "set_trap_with_villagers", "text": "Köylülerle Tuzak Kur", "result": "Kurt adamı tuzağa düşürdünüz, XP ve altın kazandınız.", "effect": "gain_xp:8, gain_gold:12", "next_scene": "old_scholar"}
                    ]
                },
                {
                    "id": "old_scholar_puzzle",
                    "title": "Yaşlı Bilge Bulmacası",
                    "description": "Bilge yeni bir bilmece sordu. Doğru cevaplarsan büyülü bir tılsım kazanırsın.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "solve_scholar_puzzle", "text": "Bilmecenin Cevabını Dene", "result": "Doğru cevabı verdin, büyülü bir tılsım ve XP kazandın.", "effect": "item:magic_amulet, gain_xp:9", "next_scene": "ruined_village"},
                        {"id": "fail_scholar_puzzle", "text": "Yanlış Cevap Ver", "result": "Yanlış cevap verdin, bilge seni uyardı ama XP kazandın.", "effect": "gain_xp:2", "next_scene": "ruined_village"}
                    ]
                },
                {
                    "id": "blacksmith_event_miniboss",
                    "title": "Demirci Mini-Boss",
                    "description": "Demirci dükkanında bir metal golem ortaya çıktı. Savaş ya da demirciyle birlikte tuzak kur.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "fight_metal_golem", "text": "Metal Golemle Savaş", "result": "Metal golemi yendin, özel bir çekiç ve XP kazandın.", "effect": "item:smith_hammer, gain_xp:14", "combat": True, "enemy": "Metal Golem", "next_scene": "ruined_village"},
                        {"id": "set_trap_with_blacksmith", "text": "Demirciyle Tuzak Kur", "result": "Golemi tuzağa düşürdünüz, XP ve altın kazandınız.", "effect": "gain_xp:8, gain_gold:10", "next_scene": "ruined_village"}
                    ]
                },
                {
                    "id": "poisoned_well_puzzle",
                    "title": "Zehirli Kuyu Bulmacası",
                    "description": "Kuyunun başında eski bir yazıt var. Doğru çözersen ödül kazanırsın.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "solve_well_puzzle", "text": "Yazıtı Çöz", "result": "Yazıtı çözdün, iksir ve XP kazandın.", "effect": "item:antidote, gain_xp:6", "next_scene": "ruined_village"},
                        {"id": "fail_well_puzzle", "text": "Yanlış Deneme", "result": "Yanlış denedin, zehirlendin ve XP kaybettin.", "effect": "debuff:poisoned, lose_xp:2", "next_scene": "ruined_village"}
                    ]
                },
                {
                    "id": "bard_encounter_miniboss",
                    "title": "Ozan Mini-Boss",
                    "description": "Ozanın şarkısı bir hayalet ruhu çağırdı. Savaş ya da ozanla birlikte şarkı söyleyerek ruhu yatıştır.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "fight_ghost", "text": "Hayaletle Savaş", "result": "Hayalet ruhunu yendin, eski bir nota ve XP kazandın.", "effect": "item:ancient_note, gain_xp:10", "combat": True, "enemy": "Hayalet Ruh", "next_scene": "ruined_village"},
                        {"id": "sing_with_bard_again", "text": "Ozanla Şarkı Söyle", "result": "Ozanla birlikte şarkı söyledin, ruh huzura kavuştu ve XP kazandın.", "effect": "gain_xp:7, item:blessed_lyric", "next_scene": "ruined_village"}
                    ]
                },
                {
                    "id": "forest_fairy_event_puzzle",
                    "title": "Orman Perisi Bulmacası",
                    "description": "Orman perisi bir bilmece sordu. Doğru cevaplarsan özel bir tılsım kazanırsın.",
                    "background": "/static/images/forest.jpg",
                    "choices": [
                        {"id": "solve_fairy_puzzle", "text": "Bilmecenin Cevabını Dene", "result": "Doğru cevabı verdin, peri sana özel bir tılsım ve XP verdi.", "effect": "item:fairy_amulet, gain_xp:8", "next_scene": "forest_path"},
                        {"id": "fail_fairy_puzzle", "text": "Yanlış Cevap Ver", "result": "Yanlış cevap verdin, peri üzgün ama XP kazandın.", "effect": "gain_xp:2", "next_scene": "forest_path"}
                    ]
                },
                {
                    "id": "mysterious_traveler_miniboss",
                    "title": "Gizemli Yolcu Mini-Boss",
                    "description": "Yolcunun gerçek kimliği ortaya çıktı: bir suikastçı! Savaş ya da yolcuyu kandır.",
                    "background": "/static/images/forest.jpg",
                    "choices": [
                        {"id": "fight_assassin", "text": "Suikastçı ile Savaş", "result": "Suikastçıyı yendin, gizli bir hançer ve XP kazandın.", "effect": "item:secret_dagger, gain_xp:12", "combat": True, "enemy": "Suikastçı", "next_scene": "forest_path"},
                        {"id": "trick_assassin", "text": "Suikastçıyı Kandır", "result": "Suikastçıyı kandırdın, altın ve XP kazandın.", "effect": "gain_gold:18, gain_xp:6", "next_scene": "forest_path"}
                    ]
                },
                {
                    "id": "merchant_encounter_puzzle",
                    "title": "Tüccar Bulmacası",
                    "description": "Tüccar bir bilmece sordu. Doğru cevaplarsan indirimli eşya alırsın.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "solve_merchant_puzzle", "text": "Bilmecenin Cevabını Dene", "result": "Doğru cevabı verdin, tüccardan indirimli eşya ve XP kazandın.", "effect": "item:discount_voucher, gain_xp:5", "next_scene": "forest_path"},
                        {"id": "fail_merchant_puzzle", "text": "Yanlış Cevap Ver", "result": "Yanlış cevap verdin, tüccar üzgün ama XP kazandın.", "effect": "gain_xp:2", "next_scene": "forest_path"}
                    ]
                },
                {
                    "id": "villagers_reencounter",
                    "title": "Köylülerle Yeniden Karşılaşma",
                    "description": "Daha önce yardım ettiğin veya zarar verdiğin köylülerle tekrar karşılaştın.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "villagers_grateful", "text": "Köylülerin Minnettarlığı (İlişki > 2)", "result": "Köylüler sana minnettar, özel bir iksir ve altın verdiler.", "effect": "item:elixir, gain_gold:20, gain_xp:8", "condition": "relationship:Villagers:>2", "next_scene": "ruined_village"},
                        {"id": "villagers_neutral", "text": "Köylülerle Sohbet Et (İlişki -2 ile 2 arası)", "result": "Köylülerle sohbet ettin, küçük bir bilgi aldın.", "effect": "gain_xp:2", "condition": "relationship:Villagers:>=-2,<=2", "next_scene": "ruined_village"},
                        {"id": "villagers_hostile", "text": "Köylülerin Düşmanlığı (İlişki < -2)", "result": "Köylüler seni köyden kovdu, XP kaybettin.", "effect": "lose_xp:4", "condition": "relationship:Villagers:<-2", "next_scene": "ruined_village"}
                    ]
                },
                {
                    "id": "priest_reencounter",
                    "title": "Rahiple Yeniden Karşılaşma",
                    "description": "Kutsal tapınağta rahiple tekrar karşılaştın. İlişkinize göre farklı ödüller veya cezalar var.",
                    "background": "/static/images/temple.jpg",
                    "choices": [
                        {"id": "priest_blessing", "text": "Rahibin Lütfu (İlişki > 2)", "result": "Rahip seni kutsadı, kutsal bir tılsım ve XP verdi.", "effect": "item:blessed_amulet, gain_xp:10", "condition": "relationship:Priest:>2", "next_scene": "holy_temple"},
                        {"id": "priest_neutral", "text": "Rahiple Sohbet Et (İlişki -2 ile 2 arası)", "result": "Rahiple sohbet ettin, küçük bir bilgi aldın.", "effect": "gain_xp:2", "condition": "relationship:Priest:>=-2,<=2", "next_scene": "holy_temple"},
                        {"id": "priest_hostile", "text": "Rahibin Düşmanlığı (İlişki < -2)", "result": "Rahip seni lanetledi, XP kaybettin.", "effect": "debuff:cursed, lose_xp:5", "condition": "relationship:Priest:<-2", "next_scene": "holy_temple"}
                    ]
                },
                {
                    "id": "forest_fairy_reencounter",
                    "title": "Orman Perisi ile Yeniden Karşılaşma",
                    "description": "Orman perisiyle tekrar karşılaştın. İlişkinize göre özel bir büyü veya ceza alabilirsin.",
                    "background": "/static/images/forest.jpg",
                    "choices": [
                        {"id": "fairy_blessing", "text": "Perinin Lütfu (İlişki > 2)", "result": "Peri sana koruyucu bir büyü ve XP verdi.", "effect": "buff:fairy_protection, gain_xp:9", "condition": "relationship:ForestFairy:>2", "next_scene": "forest_path"},
                        {"id": "fairy_neutral", "text": "Periyle Sohbet Et (İlişki -2 ile 2 arası)", "result": "Periyle sohbet ettin, küçük bir bilgi aldın.", "effect": "gain_xp:2", "condition": "relationship:ForestFairy:>=-2,<=2", "next_scene": "forest_path"},
                        {"id": "fairy_hostile", "text": "Perinin Düşmanlığı (İlişki < -2)", "result": "Peri seni lanetledi, XP kaybettin.", "effect": "debuff:cursed, lose_xp:4", "condition": "relationship:ForestFairy:<-2", "next_scene": "forest_path"}
                    ]
                },
                {
                    "id": "merchant_reencounter",
                    "title": "Tüccarla Yeniden Karşılaşma",
                    "description": "Gezgin tüccarla tekrar karşılaştın. İlişkinize göre indirimli eşya veya ceza alabilirsin.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "merchant_discount", "text": "Tüccarın İndirimi (İlişki > 2)", "result": "Tüccar sana indirimli eşya ve XP verdi.", "effect": "item:discount_voucher, gain_xp:6", "condition": "relationship:Merchant:>2", "next_scene": "forest_path"},
                        {"id": "merchant_neutral", "text": "Tüccarla Sohbet Et (İlişki -2 ile 2 arası)", "result": "Tüccarla sohbet ettin, küçük bir bilgi aldın.", "effect": "gain_xp:2", "condition": "relationship:Merchant:>=-2,<=2", "next_scene": "forest_path"},
                        {"id": "merchant_hostile", "text": "Tüccarın Düşmanlığı (İlişki < -2)", "result": "Tüccar seni dolandırdı, altın kaybettin.", "effect": "lose_gold:10, lose_xp:2", "condition": "relationship:Merchant:<-2", "next_scene": "forest_path"}
                    ]
                },
                {
                    "id": "old_scholar_reencounter",
                    "title": "Yaşlı Bilge ile Yeniden Karşılaşma",
                    "description": "Yaşlı bilgeyle tekrar karşılaştın. İlişkinize göre özel bir kitap veya ceza alabilirsin.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "scholar_gift", "text": "Bilgenin Hediyesi (İlişki > 2)", "result": "Bilge sana büyülü bir kitap ve XP verdi.", "effect": "item:magic_book, gain_xp:8", "condition": "relationship:OldScholar:>2", "next_scene": "ruined_village"},
                        {"id": "scholar_neutral", "text": "Bilgeyle Sohbet Et (İlişki -2 ile 2 arası)", "result": "Bilgeyle sohbet ettin, küçük bir bilgi aldın.", "effect": "gain_xp:2", "condition": "relationship:OldScholar:>=-2,<=2", "next_scene": "ruined_village"},
                        {"id": "scholar_hostile", "text": "Bilgenin Düşmanlığı (İlişki < -2)", "result": "Bilge seni azarladı, XP kaybettin.", "effect": "lose_xp:3", "condition": "relationship:OldScholar:<-2", "next_scene": "ruined_village"}
                    ]
                },
                {
                    "id": "forest_spirit_reencounter",
                    "title": "Orman Ruhu ile Yeniden Karşılaşma",
                    "description": "Orman ruhuyla tekrar karşılaştın. İlişkinize göre özel bir büyü veya ceza alabilirsin.",
                    "background": "/static/images/forest.jpg",
                    "choices": [
                        {"id": "spirit_blessing", "text": "Ruhun Lütfu (İlişki > 2)", "result": "Orman ruhu sana koruyucu bir büyü ve XP verdi.", "effect": "buff:spirit_protection, gain_xp:9", "condition": "relationship:ForestSpirit:>2", "next_scene": "mountain_pass"},
                        {"id": "spirit_neutral", "text": "Ruhla Sohbet Et (İlişki -2 ile 2 arası)", "result": "Ruhla sohbet ettin, küçük bir bilgi aldın.", "effect": "gain_xp:2", "condition": "relationship:ForestSpirit:>=-2,<=2", "next_scene": "mountain_pass"},
                        {"id": "spirit_hostile", "text": "Ruhun Düşmanlığı (İlişki < -2)", "result": "Orman ruhu seni lanetledi, XP kaybettin.", "effect": "debuff:cursed, lose_xp:4", "condition": "relationship:ForestSpirit:<-2", "next_scene": "mountain_pass"}
                    ]
                },
                {
                    "id": "spirit_guardian_reencounter",
                    "title": "Ruh Bekçisi ile Yeniden Karşılaşma",
                    "description": "Ruh bekçisiyle tekrar karşılaştın. İlişkinize göre özel bir anahtar veya ceza alabilirsin.",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {"id": "guardian_gift", "text": "Bekçinin Hediyesi (İlişki > 2)", "result": "Ruh bekçisi sana eski bir anahtar ve XP verdi.", "effect": "item:ancient_key, gain_xp:7", "condition": "relationship:SpiritGuardian:>2", "next_scene": "ancient_ruins"},
                        {"id": "guardian_neutral", "text": "Bekçiyle Sohbet Et (İlişki -2 ile 2 arası)", "result": "Bekçiyle sohbet ettin, küçük bir bilgi aldın.", "effect": "gain_xp:2", "condition": "relationship:SpiritGuardian:>=-2,<=2", "next_scene": "ancient_ruins"},
                        {"id": "guardian_hostile", "text": "Bekçinin Düşmanlığı (İlişki < -2)", "result": "Ruh bekçisi seni lanetledi, XP kaybettin.", "effect": "debuff:cursed, lose_xp:4", "condition": "relationship:SpiritGuardian:<-2", "next_scene": "ancient_ruins"}
                    ]
                },
                # ... her bölge için encounter ve mini-boss sahneleri ...
                # ... oyuncu istediği kadar keşif yapabilir, boss dövüşü sadece finalde açılır ...
                {
                    "id": "goblin_intro",
                    "title": "Goblin'in Hikayesi",
                    "description": "Bu goblin, ormanın derinliklerinde yalnız büyümüş, zekası ve kurnazlığıyla hayatta kalmış. İnsanlara karşı temkinli ama adil davrananlara sadık bir dost olabilir.",
                    "background": "/static/images/forest.jpg",
                    "choices": [
                        {"id": "continue_goblin_intro", "text": "Devam Et", "next_scene": "goblin_encounter"}
                    ]
                },
                {
                    "id": "druid_intro",
                    "title": "Druid Thalya'nın Hikayesi",
                    "description": "Thalya, ormanın kadim koruyucularından biri. Doğayla konuşabilen, iyiliğe değer veren bir büyücü. Ancak ihanete uğrarsa affı yoktur.",
                    "background": "/static/images/forest.jpg",
                    "choices": [
                        {"id": "continue_druid_intro", "text": "Devam Et", "next_scene": "forest_encounter"}
                    ]
                },
                {
                    "id": "blacksmith_intro",
                    "title": "Demirci'nin Hikayesi",
                    "description": "Köyün demircisi, ailesinin nesillerdir koruduğu bir geleneğin son temsilcisi. Silah yapımında usta, ama güvenini kaybedenlere karşı acımasızdır.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "continue_blacksmith_intro", "text": "Devam Et", "next_scene": "blacksmith_event"}
                    ]
                },
                {
                    "id": "bard_intro",
                    "title": "Gezgin Ozan'ın Hikayesi",
                    "description": "Ozan, diyar diyar gezen, şarkılarıyla hem neşe hem de hüzün taşıyan bir sanatçı. Dostlarına ilham, düşmanlarına ise hiciv sunar.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "continue_bard_intro", "text": "Devam Et", "next_scene": "bard_encounter"}
                    ]
                },
                {
                    "id": "villagers_intro",
                    "title": "Köylülerin Hikayesi",
                    "description": "Bu köylüler, savaş ve felaketlerle sarsılmış, hayatta kalmak için birbirine tutunan sade insanlar. Yardıma muhtaçlar ama iyiliği unutmazlar.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "continue_villagers_intro", "text": "Devam Et", "next_scene": "village_encounter"}
                    ]
                },
                {
                    "id": "priest_intro",
                    "title": "Rahibin Hikayesi",
                    "description": "Kutsal tapınağın rahibi, eski metinleri ve kutsal güçleriyle tanınır. Merhametli ama adaletten şaşmaz, kötülüğe karşı serttir.",
                    "background": "/static/images/temple.jpg",
                    "choices": [
                        {"id": "continue_priest_intro", "text": "Devam Et", "next_scene": "holy_temple"}
                    ]
                },
                {
                    "id": "forest_fairy_intro",
                    "title": "Orman Perisi'nin Hikayesi",
                    "description": "Orman perisi, doğanın ruhu ve iyiliğin simgesi. Sadece saf kalplilere görünür, kötülüğe ise asla yardım etmez.",
                    "background": "/static/images/forest.jpg",
                    "choices": [
                        {"id": "continue_fairy_intro", "text": "Devam Et", "next_scene": "forest_fairy_event"}
                    ]
                },
                {
                    "id": "merchant_intro",
                    "title": "Gezgin Tüccarın Hikayesi",
                    "description": "Tüccar, diyar diyar dolaşan, her türlü malı bulabilen kurnaz bir gezgin. Pazarlıkta usta, ama güvenini kazananlara cömerttir.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "continue_merchant_intro", "text": "Devam Et", "next_scene": "merchant_encounter"}
                    ]
                },
                {
                    "id": "old_scholar_intro",
                    "title": "Yaşlı Bilgenin Hikayesi",
                    "description": "Yaşlı bilge, eski kitapların ve unutulmuş sırların bekçisi. Bilgeliğiyle yol gösterir, ama sabırsızlara karşı hoşgörüsüzdür.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "continue_scholar_intro", "text": "Devam Et", "next_scene": "old_scholar"}
                    ]
                },
                {
                    "id": "forest_spirit_intro",
                    "title": "Orman Ruhunun Hikayesi",
                    "description": "Orman ruhu, doğanın dengesini koruyan kadim bir varlık. Doğaya zarar verenleri affetmez, iyilik yapanlara ise lütuf sunar.",
                    "background": "/static/images/forest.jpg",
                    "choices": [
                        {"id": "continue_forest_spirit_intro", "text": "Devam Et", "next_scene": "forest_spirit_boss"}
                    ]
                },
                {
                    "id": "spirit_guardian_intro",
                    "title": "Ruh Bekçisinin Hikayesi",
                    "description": "Kadim harabelerin ruh bekçisi, geçmişin sırlarını ve kayıp anahtarları korur. Sadece bilge ve cesur olanlara yol gösterir.",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {"id": "continue_spirit_guardian_intro", "text": "Devam Et", "next_scene": "spirit_guardian_boss"}
                    ]
                },
                {
                    "id": "goblin_dialogue",
                    "title": "Goblin ile Diyalog",
                    "description": "Goblin: 'Sen de kimsin? Ormanda ne arıyorsun? Buralar tehlikelidir!'",
                    "background": "/static/images/forest.jpg",
                    "choices": [
                        {"id": "continue_goblin_dialogue", "text": "Devam Et", "next_scene": "goblin_encounter"}
                    ]
                },
                # Orman Ruhu için
                {
                    "id": "forest_spirit_confrontation",
                    "title": "Orman Ruhu ile Yüzleşme",
                    "description": "Ormanın derinliklerinde, ruh lideri karşında beliriyor.\n\nOrman Ruhu: 'Bu ormanın sırlarını koruyorum. Niyetin nedir, yolcu?'",
                    "background": "/static/images/forest.jpg",
                    "choices": [
                        {"id": "spirit_persuade", "text": "İkna etmeye çalış: 'Ormanın sırlarına zarar vermeyeceğim.'", "result": "Ruh seni dikkatle dinledi ama şüpheli.", "effect": "reputation:+3", "next_scene": "forest_spirit_boss"},
                        {"id": "spirit_intimidate", "text": "Korkut: 'Yolumdan çekil, yoksa pişman olursun.'", "result": "Ruh öfkelendi, savaş kaçınılmaz.", "effect": "reputation:-2", "next_scene": "forest_spirit_boss"},
                        {"id": "spirit_bluff", "text": "Blöf yap: 'Ormanda senden daha güçlü dostlarım var.'", "result": "Ruh blöfünü yedi mi emin değil.", "effect": "reputation:-1", "next_scene": "forest_spirit_boss"},
                        {"id": "spirit_flee", "text": "Kaçmaya çalış", "result": "Kaçmaya çalıştın ama orman seni bırakmadı.", "effect": "lose_hp:5", "next_scene": "forest_spirit_boss"},
                        {"id": "spirit_attack", "text": "Doğrudan saldır!", "result": "Ruh liderine saldırdın. Savaş başlıyor!", "effect": "", "next_scene": "forest_spirit_boss"}
                    ]
                },
                # Dağ Trolü için
                {
                    "id": "mountain_troll_confrontation",
                    "title": "Dağ Trolü ile Yüzleşme",
                    "description": "Dağ geçidinde dev bir trol yolunu kesti.\n\nTrol: 'Kimse geçemez! Ya bana hazine ver ya da dövüş!'",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {"id": "troll_bargain", "text": "Pazarlık yap: 'Sana altın vereyim, yolumu aç.'", "result": "Trol altını aldı ama hâlâ şüpheli.", "effect": "lose_gold:20", "next_scene": "mountain_troll_boss"},
                        {"id": "troll_intimidate", "text": "Korkut: 'Seni kolayca alt edebilirim.'", "result": "Trol öfkelendi, savaş kaçınılmaz.", "effect": "reputation:-2", "next_scene": "mountain_troll_boss"},
                        {"id": "troll_bluff", "text": "Blöf yap: 'Arkamda bir ordu var.'", "result": "Trol blöfünü yedi mi emin değil.", "effect": "reputation:-1", "next_scene": "mountain_troll_boss"},
                        {"id": "troll_flee", "text": "Kaçmaya çalış", "result": "Kaçmaya çalıştın ama trol seni yakaladı.", "effect": "lose_hp:7", "next_scene": "mountain_troll_boss"},
                        {"id": "troll_attack", "text": "Doğrudan saldır!", "result": "Trole saldırdın. Savaş başlıyor!", "effect": "", "next_scene": "mountain_troll_boss"}
                    ]
                },
                # Ruh Bekçisi için
                {
                    "id": "spirit_guardian_confrontation",
                    "title": "Ruh Bekçisi ile Yüzleşme",
                    "description": "Kadim harabelerde bir ruh bekçisiyle karşılaştın.\n\nRuh Bekçisi: 'Bu toprakların sırlarını koruyorum. Niyetin nedir, yolcu?'",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {"id": "guardian_persuade", "text": "İkna etmeye çalış: 'Sadece bilgi arıyorum.'", "result": "Bekçi seni dikkatle dinledi ama şüpheli.", "effect": "reputation:+2", "next_scene": "spirit_guardian_boss"},
                        {"id": "guardian_intimidate", "text": "Korkut: 'Yolumdan çekil, yoksa pişman olursun.'", "result": "Bekçi öfkelendi, savaş kaçınılmaz.", "effect": "reputation:-2", "next_scene": "spirit_guardian_boss"},
                        {"id": "guardian_bluff", "text": "Blöf yap: 'Beni durduramazsın.'", "result": "Bekçi blöfünü yedi mi emin değil.", "effect": "reputation:-1", "next_scene": "spirit_guardian_boss"},
                        {"id": "guardian_flee", "text": "Kaçmaya çalış", "result": "Kaçmaya çalıştın ama bekçi seni yakaladı.", "effect": "lose_hp:6", "next_scene": "spirit_guardian_boss"},
                        {"id": "guardian_attack", "text": "Doğrudan saldır!", "result": "Bekçiye saldırdın. Savaş başlıyor!", "effect": "", "next_scene": "spirit_guardian_boss"}
                    ]
                },
                # Haydut Lideri için
                {
                    "id": "bandit_leader_confrontation",
                    "title": "Haydut Lideri ile Yüzleşme",
                    "description": "Haydutların lideri yolunu kesti.\n\nHaydut Lideri: 'Buradan geçmek istiyorsan ya altın ya da kan!'",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "bandit_bargain", "text": "Pazarlık yap: 'Sana altın vereyim, yolumu aç.'", "result": "Haydut altını aldı ama hâlâ şüpheli.", "effect": "lose_gold:15", "next_scene": "bandit_fight_miniboss"},
                        {"id": "bandit_intimidate", "text": "Korkut: 'Seni kolayca alt edebilirim.'", "result": "Haydut öfkelendi, savaş kaçınılmaz.", "effect": "reputation:-2", "next_scene": "bandit_fight_miniboss"},
                        {"id": "bandit_bluff", "text": "Blöf yap: 'Arkamda bir ordu var.'", "result": "Haydut blöfünü yedi mi emin değil.", "effect": "reputation:-1", "next_scene": "bandit_fight_miniboss"},
                        {"id": "bandit_flee", "text": "Kaçmaya çalış", "result": "Kaçmaya çalıştın ama haydut seni yakaladı.", "effect": "lose_hp:5", "next_scene": "bandit_fight_miniboss"},
                        {"id": "bandit_attack", "text": "Doğrudan saldır!", "result": "Haydut liderine saldırdın. Savaş başlıyor!", "effect": "", "next_scene": "bandit_fight_miniboss"}
                    ]
                },
                # Kurt Adam için
                {
                    "id": "werewolf_confrontation",
                    "title": "Kurt Adam ile Yüzleşme",
                    "description": "Köy meydanında bir kurt adam ortaya çıktı.\n\nKurt Adam: 'Bu köy benim! Ya dövüş ya da kaç!'",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "werewolf_intimidate", "text": "Korkut: 'Seni kolayca alt edebilirim.'", "result": "Kurt adam öfkelendi, savaş kaçınılmaz.", "effect": "reputation:-2", "next_scene": "village_encounter_miniboss"},
                        {"id": "werewolf_bluff", "text": "Blöf yap: 'Gümüş silahım var.'", "result": "Kurt adam blöfünü yedi mi emin değil.", "effect": "reputation:-1", "next_scene": "village_encounter_miniboss"},
                        {"id": "werewolf_flee", "text": "Kaçmaya çalış", "result": "Kaçmaya çalıştın ama kurt adam seni yakaladı.", "effect": "lose_hp:6", "next_scene": "village_encounter_miniboss"},
                        {"id": "werewolf_attack", "text": "Doğrudan saldır!", "result": "Kurt adama saldırdın. Savaş başlıyor!", "effect": "", "next_scene": "village_encounter_miniboss"}
                    ]
                },
                # Dev Örümcek için
                {
                    "id": "spider_confrontation",
                    "title": "Dev Örümcek ile Yüzleşme",
                    "description": "Mağaranın derinliklerinde dev bir örümcek var.\n\nÖrümcek: 'Tısss... Burası benim bölgem!'",
                    "background": "/static/images/cave.jpg",
                    "choices": [
                        {"id": "spider_intimidate", "text": "Korkut: 'Seni kolayca alt edebilirim.'", "result": "Örümcek öfkelendi, savaş kaçınılmaz.", "effect": "reputation:-2", "next_scene": "hidden_cave_miniboss"},
                        {"id": "spider_bluff", "text": "Blöf yap: 'Ateş büyüm var.'", "result": "Örümcek blöfünü yedi mi emin değil.", "effect": "reputation:-1", "next_scene": "hidden_cave_miniboss"},
                        {"id": "spider_flee", "text": "Kaçmaya çalış", "result": "Kaçmaya çalıştın ama örümcek seni yakaladı.", "effect": "lose_hp:6", "next_scene": "hidden_cave_miniboss"},
                        {"id": "spider_attack", "text": "Doğrudan saldır!", "result": "Örümceğe saldırdın. Savaş başlıyor!", "effect": "", "next_scene": "hidden_cave_miniboss"}
                    ]
                },
                # Hayalet Muhafız için
                {
                    "id": "ghost_guardian_confrontation",
                    "title": "Hayalet Muhafız ile Yüzleşme",
                    "description": "Tapınağın kutsal odasında bir hayalet muhafız var.\n\nHayalet: 'Bu tapınağı korumakla görevliyim. Niyetin nedir?'",
                    "background": "/static/images/temple.jpg",
                    "choices": [
                        {"id": "ghost_persuade", "text": "İkna etmeye çalış: 'Kutsal emanete zarar vermeyeceğim.'", "result": "Hayalet seni dikkatle dinledi ama şüpheli.", "effect": "reputation:+2", "next_scene": "sacred_temple_miniboss"},
                        {"id": "ghost_intimidate", "text": "Korkut: 'Seni kolayca alt edebilirim.'", "result": "Hayalet öfkelendi, savaş kaçınılmaz.", "effect": "reputation:-2", "next_scene": "sacred_temple_miniboss"},
                        {"id": "ghost_bluff", "text": "Blöf yap: 'Kutsal büyüm var.'", "result": "Hayalet blöfünü yedi mi emin değil.", "effect": "reputation:-1", "next_scene": "sacred_temple_miniboss"},
                        {"id": "ghost_flee", "text": "Kaçmaya çalış", "result": "Kaçmaya çalıştın ama hayalet seni yakaladı.", "effect": "lose_hp:6", "next_scene": "sacred_temple_miniboss"},
                        {"id": "ghost_attack", "text": "Doğrudan saldır!", "result": "Hayalet muhafıza saldırdın. Savaş başlıyor!", "effect": "", "next_scene": "sacred_temple_miniboss"}
                    ]
                },
                # Dağ Trolü ile Yeniden Karşılaşma
                {
                    "id": "mountain_troll_reencounter",
                    "title": "Dağ Trolü ile Yeniden Karşılaşma",
                    "description": "Daha önce karşılaştığın dağ trolü tekrar yolunu kesti. İlişkinize göre farklı tepki verecek.",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {"id": "troll_friend", "text": "Trolün Dostluğu (İlişki > 2)", "result": "Trol sana bir hazine verdi!", "effect": "item:giant_gem, gain_xp:10", "condition": "relationship:MountainTroll:>2", "next_scene": "ancient_ruins"},
                        {"id": "troll_neutral", "text": "Trolle Sohbet Et (İlişki -2 ile 2 arası)", "result": "Trol sana bir ipucu verdi.", "effect": "gain_xp:2", "condition": "relationship:MountainTroll:>=-2,<=2", "next_scene": "ancient_ruins"},
                        {"id": "troll_hostile", "text": "Trolün Düşmanlığı (İlişki < -2)", "result": "Trol sana saldırdı!", "effect": "combat:true, enemy:Dağ Trolü", "condition": "relationship:MountainTroll:<-2", "next_scene": "mountain_troll_boss"}
                    ]
                },
                # Haydut Lideri ile Yeniden Karşılaşma
                {
                    "id": "bandit_leader_reencounter",
                    "title": "Haydut Lideri ile Yeniden Karşılaşma",
                    "description": "Haydut lideriyle tekrar karşılaştın. İlişkinize göre farklı ödüller veya tuzaklar var.",
                    "background": "/static/images/village.jpg",
                    "choices": [
                        {"id": "bandit_gift", "text": "Haydutun Hediyesi (İlişki > 2)", "result": "Haydut lideri sana gizli bir hazine verdi!", "effect": "item:bandit_treasure, gain_xp:8", "condition": "relationship:BanditLeader:>2", "next_scene": "forest_path"},
                        {"id": "bandit_neutral", "text": "Haydutla Sohbet Et (İlişki -2 ile 2 arası)", "result": "Haydut lideriyle sohbet ettin, küçük bir bilgi aldın.", "effect": "gain_xp:2", "condition": "relationship:BanditLeader:>=-2,<=2", "next_scene": "forest_path"},
                        {"id": "bandit_hostile", "text": "Haydutun Tuzaklı Saldırısı (İlişki < -2)", "result": "Haydut lideri sana tuzak kurdu, altın kaybettin.", "effect": "lose_gold:10, lose_xp:3", "condition": "relationship:BanditLeader:<-2", "next_scene": "forest_path"}
                    ]
                },
                # Dev Örümcek ile Yeniden Karşılaşma
                {
                    "id": "spider_reencounter",
                    "title": "Dev Örümcek ile Yeniden Karşılaşma",
                    "description": "Dev örümcek tekrar karşında. İlişkinize göre farklı ödüller veya tehlikeler var.",
                    "background": "/static/images/cave.jpg",
                    "choices": [
                        {"id": "spider_gift", "text": "Örümceğin Hediyesi (İlişki > 2)", "result": "Örümcek sana nadir bir ipek verdi!", "effect": "item:rare_silk, gain_xp:7", "condition": "relationship:Spider:>2", "next_scene": "hidden_cave"},
                        {"id": "spider_neutral", "text": "Örümcekle Sohbet Et (İlişki -2 ile 2 arası)", "result": "Örümcekle iletişim kurdun, küçük bir bilgi aldın.", "effect": "gain_xp:2", "condition": "relationship:Spider:>=-2,<=2", "next_scene": "hidden_cave"},
                        {"id": "spider_hostile", "text": "Örümceğin Saldırısı (İlişki < -2)", "result": "Örümcek seni zehirledi, HP kaybettin.", "effect": "lose_hp:10, debuff:poisoned", "condition": "relationship:Spider:<-2", "next_scene": "hidden_cave"}
                    ]
                },
                # Pyraxis final savaşında yardımcı olacak NPC altyapısı (örnek)
                {
                    "id": "final_battle_allies",
                    "title": "Son Savaşta Müttefikler",
                    "description": "Pyraxis ile savaşırken, geçmişte iyi ilişkiler kurduğun bazı NPC'ler yanında savaşıyor!",
                    "background": "/static/images/pyraxisfam.jpg",
                    "choices": [
                        {"id": "with_goblin", "text": "Dost Goblin yanında!", "result": "Goblin, Pyraxis'e karşı cesurca savaşıyor.", "effect": "buff:attack_up", "condition": "relationship:Goblin:>2", "next_scene": "pyraxis_boss_fight"},
                        {"id": "with_blacksmith", "text": "Demirci yanında!", "result": "Demirci, sana özel bir silah verdi.", "effect": "item:legendary_sword", "condition": "relationship:Blacksmith:>2", "next_scene": "pyraxis_boss_fight"},
                        {"id": "with_fairy", "text": "Orman Perisi yanında!", "result": "Peri, seni koruyucu bir büyüyle sardı.", "effect": "buff:fairy_protection", "condition": "relationship:ForestFairy:>2", "next_scene": "pyraxis_boss_fight"}
                    ]
                },
                {
                    "id": "spirit_guardian_riddle",
                    "title": "Ruh Bekçisi'nin Bilmecesi",
                    "description": "Bekçi: 'Bana doğru cevabı ver, anahtar senin olsun. Yanlış cevaplarsan savaş başlar.'",
                    "background": "/static/images/background.jpg",
                    "choices": [
                        {"id": "answer_correct", "text": "Doğru cevap ver", "result": "Anahtarı aldın!", "effect": "item:old_key, gain_xp:2", "next_scene": "final_pyraxis_prep"},
                        {"id": "answer_wrong", "text": "Yanlış cevap ver", "result": "Bekçi öfkelendi, savaş başlıyor!", "combat": True, "enemy": "Ruh Bekçisi", "next_scene": "final_pyraxis_prep"}
                    ]
                },
                {
                    "id": "hidden_cave",
                    "title": "Gizli Mağara",
                    "description": "Karanlık ve nemli bir mağara. İçeride gizli hazineler ve tehlikeler olabilir.",
                    "background": "/static/images/cave.jpg",
                    "choices": [
                        {"id": "explore_cave", "text": "Mağarayı Keşfet", "next_scene": "cave_encounter"},
                        {"id": "search_treasure", "text": "Hazine Ara", "effect": "item:rare_gem, gain_xp:10", "next_scene": "cave_encounter"},
                        {"id": "return_escape", "text": "Kaçış Noktasına Dön", "effect": "item:ancient_map, gain_xp:10", "next_scene": "escape"}
                    ]
                },
                {
                    "id": "cave_encounter",
                    "title": "Mağara Karşılaşması",
                    "description": "Mağaranın derinliklerinde gizli bir hazine odası buldun!",
                    "background": "/static/images/cave.jpg",
                    "choices": [
                        {"id": "take_treasure", "text": "Hazineyi Al", "effect": "item:legendary_sword, gain_xp:15", "next_scene": "escape"},
                        {"id": "leave_treasure", "text": "Hazineyi Bırak", "effect": "karma:+5, gain_xp:5", "next_scene": "escape"},
                        {"id": "fight_guardian", "text": "Bekçiyle Savaş", "combat": True, "enemy": "Mağara Bekçisi", "next_scene": "escape"}
                    ]
                }
            ],
            "boss": {
                "name": "Kırmızı Ejderha Pyraxis",
                "hp": 300,
                "attack": 120,
                "defense": 80,
                "abilities": ["Ateş Nefesi", "Pençe Saldırısı", "Uçma"],
                "description": "Beş ejderha efendisinden en güçlüsü. Ateş nefesi ve pençe saldırılarıyla ünlü."
            }
        }
        
        # Warhammer 40K kampanyası ekle (Genişletilmiş - 20+ sahne)
        warhammer_campaign = {
            "id": "warhammer_40k",
            "name": "⚔️ Warhammer 40K: Ork İstilası",
            "type": "sci-fi",
            "description": "Imperium'un sınırlarında Ork tehdidi büyüyor. Space Marine olarak görev yap! Cadia'nın savunması senin elinde! Plot twist'ler, ihanetler ve rastgele olaylar seni bekliyor. Sıra tabanlı kombat ve betrayal mekanikleri ile zenginleştirilmiş hikaye.",
            "scenes": [
                {
                    "id": "intro",
                    "title": "Imperial Base - Cadia",
                    "description": "Cadia'nın sınır karakolunda görevlendirildin. Ork sinyalleri yaklaşıyor... Gökyüzünde yeşil bulutlar dönüyor, uzaktan Ork savaş çığlıkları duyuluyor. Warboss Gorkamorka'nın ordusu Cadia'ya doğru ilerliyor. Sen, seçilmiş Space Marine, bu tehdidi durdurmak için buradasın.",
                    "background": "/static/images/imperial_base.jpg",
                    "choices": [
                        {"id": "report_commander", "text": "Komutana Rapor Ver", "next_scene": "mission_briefing"},
                        {"id": "check_equipment", "text": "Ekipmanı Kontrol Et", "effect": "item:bolter, gain_xp:5", "next_scene": "mission_briefing"},
                        {"id": "pray_emperor", "text": "İmparator'a Dua Et", "effect": "buff:faith_bonus, gain_xp:3", "next_scene": "mission_briefing"},
                        {"id": "inspect_defenses", "text": "Savunmaları İncele", "effect": "item:defense_map, gain_xp:2", "next_scene": "mission_briefing"}
                    ]
                },
                {
                    "id": "mission_briefing",
                    "title": "Görev Brifingi",
                    "description": "Komutan seni çağırıyor. Ork istilası başladı, görev açık. Warboss Gorkamorka'nın 50,000 Ork'u Cadia'ya doğru ilerliyor. Sen ve senin gibi seçilmiş Space Marine'lar bu tehdidi durdurmak için görevlendirildin.",
                    "background": "/static/images/command_center.jpg",
                    "choices": [
                        {"id": "accept_mission", "text": "Görevi Kabul Et", "next_scene": "defense_preparation"},
                        {"id": "ask_details", "text": "Detayları Sor", "effect": "gain_xp:2", "next_scene": "defense_preparation"},
                        {"id": "request_backup", "text": "Takviye İste", "effect": "ally:imperial_guard", "next_scene": "defense_preparation"},
                        {"id": "strategic_planning", "text": "Stratejik Planlama", "effect": "buff:tactical_advantage", "next_scene": "defense_preparation"}
                    ]
                },
                {
                    "id": "defense_preparation",
                    "title": "Savunma Hazırlığı",
                    "description": "Cadia'nın savunma hatlarını hazırlıyorsun. Ork ordusu yaklaşıyor, her dakika önemli. Imperial Guard birlikleri pozisyon alıyor, topçu bataryaları yerleştiriliyor.",
                    "background": "/static/images/defense_line.jpg",
                    "choices": [
                        {"id": "fortify_position", "text": "Pozisyonu Güçlendir", "effect": "buff:defense_bonus", "next_scene": "ork_scout_patrol"},
                        {"id": "set_traps", "text": "Tuzaklar Kur", "effect": "buff:ambush_bonus", "next_scene": "ork_scout_patrol"},
                        {"id": "coordinate_artillery", "text": "Topçuyu Koordine Et", "effect": "buff:artillery_support", "next_scene": "ork_scout_patrol"},
                        {"id": "inspire_troops", "text": "Birlikleri Motive Et", "effect": "buff:morale_boost", "next_scene": "ork_scout_patrol"}
                    ]
                },
                {
                    "id": "ork_scout_patrol",
                    "title": "Ork Keşif Devriyesi",
                    "description": "İlk Ork keşif devriyesi geldi! Küçük bir grup Ork Boyz savunma hatlarını test ediyor. Bu sadece başlangıç...",
                    "background": "/static/images/ork_scout.jpg",
                    "choices": [
                        {"id": "engage_scouts", "text": "Keşif Devriyesiyle Savaş", "combat": True, "enemy": "Ork Scouts", "next_scene": "main_ork_force"},
                        {"id": "let_them_pass", "text": "Geçmelerine İzin Ver", "effect": "gain_xp:1", "next_scene": "main_ork_force"},
                        {"id": "ambush_scouts", "text": "Pusu Kur", "effect": "buff:surprise_attack", "combat": True, "enemy": "Ork Scouts", "next_scene": "main_ork_force"},
                        {"id": "interrogate_captive", "text": "Esir Al ve Sorgula", "effect": "item:intel_data, gain_xp:3", "next_scene": "main_ork_force"}
                    ]
                },
                {
                    "id": "main_ork_force",
                    "title": "Ana Ork Gücü",
                    "description": "Ana Ork ordusu geldi! Gökyüzü yeşil bulutlarla kaplandı, Warboss Gorkamorka'nın savaş çığlıkları yankılanıyor. 50,000 Ork Cadia'ya saldırıyor!",
                    "background": "/static/images/ork_army.jpg",
                    "choices": [
                        {"id": "hold_defense_line", "text": "Savunma Hattını Tut", "combat": True, "enemy": "Ork Horde", "next_scene": "warboss_reveal"},
                        {"id": "counter_attack", "text": "Karşı Saldırı", "combat": True, "enemy": "Ork Elite", "next_scene": "warboss_reveal"},
                        {"id": "artillery_barrage", "text": "Topçu Saldırısı", "effect": "buff:artillery_support", "next_scene": "warboss_reveal"},
                        {"id": "tactical_retreat", "text": "Taktik Geri Çekilme", "next_scene": "regroup"}
                    ]
                },
                {
                    "id": "warboss_reveal",
                    "title": "Warboss Gorkamorka'nın Görünüşü",
                    "description": "Savaşın ortasında Warboss Gorkamorka göründü! 5 metre boyunda, yeşil derili, devasa silahlarla donanmış. Bu savaş senin için!",
                    "background": "/static/images/warboss.jpg",
                    "choices": [
                        {"id": "challenge_warboss", "text": "Warboss'u Meydan Oku", "combat": True, "enemy": "Warboss Gorkamorka", "next_scene": "victory"},
                        {"id": "use_psychic", "text": "Psi Gücü Kullan", "effect": "buff:psychic_boost", "combat": True, "enemy": "Warboss Gorkamorka", "next_scene": "victory"},
                        {"id": "call_reinforcements", "text": "Takviye Çağır", "effect": "ally:space_marines", "next_scene": "victory"},
                        {"id": "tactical_retreat", "text": "Taktik Geri Çekilme", "next_scene": "regroup"}
                    ]
                },
                {
                    "id": "ork_camp",
                    "title": "Ork Kampı",
                    "description": "Ork kampına ulaştın. Warboss Gorkamorka seni bekliyor!",
                    "background": "/static/images/ork_camp.jpg",
                    "choices": [
                        {"id": "stealth_approach", "text": "Gizlice Yaklaş", "next_scene": "stealth_mission"},
                        {"id": "direct_assault", "text": "Doğrudan Saldır", "combat": True, "enemy": "Ork Boyz", "next_scene": "warboss_confrontation"},
                        {"id": "call_artillery", "text": "Topçu Desteği Çağır", "effect": "buff:artillery_support", "next_scene": "warboss_confrontation"}
                    ]
                },
                {
                    "id": "warboss_confrontation",
                    "title": "Warboss ile Yüzleşme",
                    "description": "Warboss Gorkamorka karşında! Bu savaş senin için!",
                    "background": "/static/images/warboss.jpg",
                    "choices": [
                        {"id": "fight_warboss", "text": "Warboss ile Savaş", "combat": True, "enemy": "Warboss Gorkamorka", "next_scene": "victory"},
                        {"id": "use_psychic", "text": "Psi Gücü Kullan", "effect": "buff:psychic_boost", "combat": True, "enemy": "Warboss Gorkamorka", "next_scene": "victory"},
                        {"id": "tactical_retreat", "text": "Taktik Geri Çekilme", "next_scene": "regroup"}
                    ]
                },
                {
                    "id": "betrayal_reveal",
                    "title": "İhanetin Ortaya Çıkışı",
                    "description": "Komutan Voss'un aslında Orklarla işbirliği yaptığını öğrendin! Bu ihanet seni şok etti. Artık kimseye güvenemezsin.",
                    "background": "/static/images/betrayal.jpg",
                    "choices": [
                        {"id": "confront_betrayer", "text": "Haini Yüzleştir", "effect": "karma:+5", "next_scene": "betrayal_combat"},
                        {"id": "gather_evidence", "text": "Kanıt Topla", "effect": "item:betrayal_evidence", "next_scene": "betrayal_combat"},
                        {"id": "warn_allies", "text": "Müttefikleri Uyar", "effect": "ally:loyal_soldiers", "next_scene": "betrayal_combat"},
                        {"id": "secret_plan", "text": "Gizli Plan Yap", "effect": "buff:stealth_advantage", "next_scene": "betrayal_combat"}
                    ]
                },
                {
                    "id": "betrayal_combat",
                    "title": "Hainle Savaş",
                    "description": "Komutan Voss ile yüzleşiyorsun. Bu sıra tabanlı kombat senin için! İhanetin bedelini ödeyecek!",
                    "background": "/static/images/betrayal_combat.jpg",
                    "choices": [
                        {"id": "fight_betrayer", "text": "Hainle Savaş", "combat": True, "enemy": "Traitor Commander", "next_scene": "ork_artillery"},
                        {"id": "use_evidence", "text": "Kanıtı Kullan", "effect": "buff:evidence_bonus", "combat": True, "enemy": "Traitor Commander", "next_scene": "ork_artillery"},
                        {"id": "call_loyalists", "text": "Sadık Askerleri Çağır", "effect": "ally:loyal_forces", "combat": True, "enemy": "Traitor Commander", "next_scene": "ork_artillery"},
                        {"id": "psychic_attack", "text": "Psi Saldırısı", "effect": "buff:psychic_rage", "combat": True, "enemy": "Traitor Commander", "next_scene": "ork_artillery"}
                    ]
                },
                {
                    "id": "ork_artillery",
                    "title": "Ork Topçusu",
                    "description": "Ork topçusu pozisyonları tespit ettin. Bu tehdidi yok etmek için sıra tabanlı kombat başlıyor!",
                    "background": "/static/images/ork_artillery.jpg",
                    "choices": [
                        {"id": "attack_artillery", "text": "Topçuyu Saldır", "combat": True, "enemy": "Ork Artillery", "next_scene": "ork_elite_guard"},
                        {"id": "stealth_approach", "text": "Gizlice Yaklaş", "effect": "buff:stealth_bonus", "combat": True, "enemy": "Ork Artillery", "next_scene": "ork_elite_guard"},
                        {"id": "call_airstrike", "text": "Hava Saldırısı Çağır", "effect": "buff:airstrike_support", "next_scene": "ork_elite_guard"},
                        {"id": "coordinate_counter", "text": "Karşı Topçu Koordine Et", "effect": "buff:counter_artillery", "next_scene": "ork_elite_guard"}
                    ]
                },
                {
                    "id": "ork_elite_guard",
                    "title": "Ork Elit Muhafızları",
                    "description": "Warboss'un elit muhafızlarıyla karşılaştın. Bu sıra tabanlı kombat çok zorlu olacak!",
                    "background": "/static/images/ork_elite.jpg",
                    "choices": [
                        {"id": "fight_elite_guard", "text": "Elit Muhafızlarla Savaş", "combat": True, "enemy": "Ork Elite Guard", "next_scene": "ork_war_machine"},
                        {"id": "use_heavy_weapons", "text": "Ağır Silahları Kullan", "effect": "buff:heavy_weapon_bonus", "combat": True, "enemy": "Ork Elite Guard", "next_scene": "ork_war_machine"},
                        {"id": "tactical_retreat", "text": "Taktik Geri Çekilme", "next_scene": "regroup"},
                        {"id": "call_reinforcements", "text": "Takviye Çağır", "effect": "ally:imperial_elite", "next_scene": "ork_war_machine"}
                    ]
                },
                {
                    "id": "ork_war_machine",
                    "title": "Ork Savaş Makinesi",
                    "description": "Ork savaş makinesi karşında! Bu devasa makine sıra tabanlı kombat ile yok edilmeli!",
                    "background": "/static/images/ork_war_machine.jpg",
                    "choices": [
                        {"id": "fight_war_machine", "text": "Savaş Makinesiyle Savaş", "combat": True, "enemy": "Ork War Machine", "next_scene": "warboss_preparation"},
                        {"id": "target_weak_points", "text": "Zayıf Noktaları Hedefle", "effect": "buff:precision_bonus", "combat": True, "enemy": "Ork War Machine", "next_scene": "warboss_preparation"},
                        {"id": "use_explosives", "text": "Patlayıcı Kullan", "effect": "buff:explosive_bonus", "combat": True, "enemy": "Ork War Machine", "next_scene": "warboss_preparation"},
                        {"id": "call_tank_support", "text": "Tank Desteği Çağır", "effect": "ally:imperial_tanks", "next_scene": "warboss_preparation"}
                    ]
                },
                {
                    "id": "warboss_preparation",
                    "title": "Warboss'a Hazırlık",
                    "description": "Warboss Gorkamorka'ya karşı son hazırlıklarını yapıyorsun. Bu savaş senin için!",
                    "background": "/static/images/warboss_prep.jpg",
                    "choices": [
                        {"id": "prepare_weapons", "text": "Silahları Hazırla", "effect": "buff:weapon_preparation", "next_scene": "warboss_confrontation"},
                        {"id": "meditate_emperor", "text": "İmparator'a Meditasyon", "effect": "buff:divine_blessing", "next_scene": "warboss_confrontation"},
                        {"id": "coordinate_allies", "text": "Müttefikleri Koordine Et", "effect": "ally:final_allies", "next_scene": "warboss_confrontation"},
                        {"id": "study_warboss", "text": "Warboss'u Araştır", "effect": "item:warboss_intel", "next_scene": "warboss_confrontation"}
                    ]
                },
                {
                    "id": "victory",
                    "title": "Zafer",
                    "description": "Ork tehdidi bertaraf edildi! Warboss Gorkamorka öldü, Ork ordusu dağıldı. Imperium seni kahraman ilan ediyor. Cadia güvende!",
                    "choices": []
                },
                {
                    "id": "stealth_mission",
                    "title": "Gizli Görev",
                    "description": "Ork kampına gizlice sızdın. Warboss'un planlarını öğrenmek için yakından gözlem yapıyorsun.",
                    "background": "/static/images/stealth_mission.jpg",
                    "choices": [
                        {"id": "infiltrate_deeper", "text": "Daha Derine Sız", "effect": "item:intel_data, gain_xp:3", "next_scene": "warboss_confrontation"},
                        {"id": "plant_explosives", "text": "Patlayıcı Yerleştir", "effect": "buff:explosive_support", "next_scene": "warboss_confrontation"},
                        {"id": "signal_attack", "text": "Saldırı Sinyali Ver", "effect": "ally:imperial_forces", "next_scene": "warboss_confrontation"}
                    ]
                },
                {
                    "id": "regroup",
                    "title": "Yeniden Toplanma",
                    "description": "Taktik geri çekilme sonrası güçlerini topladın. Yeni bir plan yapman gerekiyor.",
                    "background": "/static/images/regroup.jpg",
                    "choices": [
                        {"id": "plan_ambush", "text": "Pusu Planla", "effect": "buff:ambush_bonus", "next_scene": "warboss_confrontation"},
                        {"id": "call_reinforcements", "text": "Takviye Çağır", "effect": "ally:space_marines", "next_scene": "warboss_confrontation"},
                        {"id": "direct_assault", "text": "Doğrudan Saldır", "combat": True, "enemy": "Ork Elite", "next_scene": "warboss_confrontation"}
                    ]
                }
            ]
        }
        
        # Cyberpunk kampanyası ekle (Genişletilmiş - 20+ sahne)
        cyberpunk_campaign = {
            "id": "cyberpunk_2077",
            "name": "🌃 Cyberpunk 2077: Night City",
            "type": "cyberpunk",
            "description": "Night City'de yeni bir hack görevi. Netrunner olarak çalış! Arasaka'nın gizli projelerini ortaya çıkar! Plot twist'ler, ihanetler ve rastgele olaylar seni bekliyor. Sıra tabanlı kombat ve betrayal mekanikleri ile zenginleştirilmiş hikaye.",
            "scenes": [
                {
                    "id": "intro",
                    "title": "Night City - Arasaka Tower",
                    "description": "Arasaka Tower'ın önündesin. Yeni bir hack görevi var. Arasaka'nın gizli projelerini ortaya çıkarmak için buradayısın. Night City'nin neon ışıkları altında, bu görev senin için!",
                    "background": "/static/images/night_city.jpg",
                    "choices": [
                        {"id": "enter_tower", "text": "Tower'a Gir", "next_scene": "security_breach"},
                        {"id": "hack_security", "text": "Güvenlik Sistemini Hack Et", "effect": "buff:stealth_mode", "next_scene": "security_breach"},
                        {"id": "find_ally", "text": "Müttefik Ara", "effect": "ally:netrunner", "next_scene": "security_breach"},
                        {"id": "reconnaissance", "text": "Keşif Yap", "effect": "item:security_blueprint, gain_xp:2", "next_scene": "security_breach"}
                    ]
                },
                {
                    "id": "security_breach",
                    "title": "Güvenlik İhlali",
                    "description": "Tower'ın içindesin. Arasaka güvenlik sistemi aktif. Her köşede güvenlik kameraları, her koridorda Arasaka muhafızları var. Bu görev dikkat gerektiriyor.",
                    "background": "/static/images/arasaka_tower.jpg",
                    "choices": [
                        {"id": "stealth_mode", "text": "Gizli Mod", "next_scene": "elevator_ride"},
                        {"id": "hack_robots", "text": "Robotları Hack Et", "effect": "ally:security_robots", "next_scene": "elevator_ride"},
                        {"id": "fight_guards", "text": "Muhafızlarla Savaş", "combat": True, "enemy": "Arasaka Guards", "next_scene": "elevator_ride"},
                        {"id": "hack_cameras", "text": "Kamerları Hack Et", "effect": "buff:stealth_enhanced", "next_scene": "elevator_ride"}
                    ]
                },
                {
                    "id": "elevator_ride",
                    "title": "Asansör Yolculuğu",
                    "description": "Arasaka Tower'ın asansöründesin. Yukarı çıkıyorsun, her kat daha tehlikeli. Arasaka'nın gizli laboratuvarları üst katlarda.",
                    "background": "/static/images/elevator.jpg",
                    "choices": [
                        {"id": "hack_elevator", "text": "Asansörü Hack Et", "effect": "buff:fast_access", "next_scene": "data_heist"},
                        {"id": "stealth_ride", "text": "Gizlice Çık", "effect": "buff:stealth_mode", "next_scene": "data_heist"},
                        {"id": "fight_guards", "text": "Muhafızlarla Savaş", "combat": True, "enemy": "Arasaka Elite", "next_scene": "data_heist"},
                        {"id": "use_ventilation", "text": "Havalandırma Kullan", "effect": "item:ventilation_map", "next_scene": "data_heist"}
                    ]
                },
                {
                    "id": "data_heist",
                    "title": "Veri Hırsızlığı",
                    "description": "Ana veri bankasına ulaştın. Kritik verileri çalman gerekiyor. Arasaka'nın gizli projeleri burada saklanıyor.",
                    "background": "/static/images/data_center.jpg",
                    "choices": [
                        {"id": "hack_mainframe", "text": "Ana Bilgisayarı Hack Et", "effect": "item:classified_data", "next_scene": "security_override"},
                        {"id": "copy_data", "text": "Veriyi Kopyala", "effect": "item:stolen_data", "next_scene": "security_override"},
                        {"id": "destroy_data", "text": "Veriyi Yok Et", "effect": "karma:-10", "next_scene": "security_override"}
                    ]
                },
                {
                    "id": "secret_laboratory",
                    "title": "Gizli Laboratuvar",
                    "description": "Arasaka'nın gizli laboratuvarına ulaştın. Burada insan deneyleri yapılıyor. Etik olmayan projeler burada geliştiriliyor.",
                    "background": "/static/images/laboratory.jpg",
                    "choices": [
                        {"id": "hack_computers", "text": "Bilgisayarları Hack Et", "effect": "item:research_data", "next_scene": "security_override"},
                        {"id": "free_subjects", "text": "Denekleri Kurtar", "effect": "karma:+10, gain_xp:5", "next_scene": "security_override"},
                        {"id": "steal_prototype", "text": "Prototip Çal", "effect": "item:cyberware_prototype", "next_scene": "security_override"},
                        {"id": "destroy_lab", "text": "Laboratuvarı Yok Et", "effect": "karma:-5, gain_xp:3", "next_scene": "security_override"}
                    ]
                },
                {
                    "id": "security_override",
                    "title": "Güvenlik Sistemi Geçersiz Kılma",
                    "description": "Arasaka'nın güvenlik sistemi seni tespit etti. Hızlı hareket etmen gerekiyor. Alarm çalıyor, muhafızlar geliyor!",
                    "background": "/static/images/security_override.jpg",
                    "choices": [
                        {"id": "hack_override", "text": "Sistemi Hack Et", "effect": "buff:system_control", "next_scene": "boss_confrontation"},
                        {"id": "stealth_override", "text": "Gizlice Geç", "effect": "buff:stealth_enhanced", "next_scene": "boss_confrontation"},
                        {"id": "fight_override", "text": "Savaşarak Geç", "combat": True, "enemy": "Security AI", "next_scene": "boss_confrontation"}
                    ]
                },
                {
                    "id": "boss_confrontation",
                    "title": "Arasaka Yöneticisi ile Yüzleşme",
                    "description": "Arasaka'nın yöneticisi seni bekliyor. Bu savaş senin için!",
                    "background": "/static/images/boss_room.jpg",
                    "choices": [
                        {"id": "fight_boss", "text": "Yönetici ile Savaş", "combat": True, "enemy": "Arasaka Director", "next_scene": "escape"},
                        {"id": "hack_boss", "text": "Yöneticiyi Hack Et", "effect": "buff:mind_control", "next_scene": "escape"},
                        {"id": "negotiate_boss", "text": "Müzakere Et", "effect": "karma:+5", "next_scene": "escape"}
                    ]
                },
                {
                    "id": "escape",
                    "title": "Kaçış",
                    "description": "Arasaka Tower'dan kaçman gerekiyor. Helikopter bekliyor!",
                    "background": "/static/images/helicopter.jpg",
                    "choices": [
                        {"id": "rooftop_escape", "text": "Çatıdan Kaç", "next_scene": "mission_complete"},
                        {"id": "underground_escape", "text": "Yeraltından Kaç", "effect": "item:underground_map", "next_scene": "mission_complete"},
                        {"id": "fight_escape", "text": "Savaşarak Kaç", "combat": True, "enemy": "Arasaka Elite", "next_scene": "mission_complete"}
                    ]
                },
                {
                    "id": "ai_betrayal",
                    "title": "AI'nın İhaneti",
                    "description": "Arasaka'nın AI sistemi aslında seni izliyordu! Bu ihanet seni şok etti. Artık sisteme güvenemezsin.",
                    "background": "/static/images/ai_betrayal.jpg",
                    "choices": [
                        {"id": "confront_ai", "text": "AI ile Yüzleş", "effect": "karma:+5", "next_scene": "ai_combat"},
                        {"id": "hack_ai_system", "text": "AI Sistemini Hack Et", "effect": "buff:ai_control", "next_scene": "ai_combat"},
                        {"id": "warn_allies", "text": "Müttefikleri Uyar", "effect": "ally:loyal_hackers", "next_scene": "ai_combat"},
                        {"id": "secret_counter", "text": "Gizli Karşı Plan", "effect": "buff:stealth_advantage", "next_scene": "ai_combat"}
                    ]
                },
                {
                    "id": "ai_combat",
                    "title": "AI ile Savaş",
                    "description": "Arasaka'nın AI sistemi ile yüzleşiyorsun. Bu sıra tabanlı kombat senin için!",
                    "background": "/static/images/ai_combat.jpg",
                    "choices": [
                        {"id": "fight_ai", "text": "AI ile Savaş", "combat": True, "enemy": "Rogue AI", "next_scene": "corporate_security"},
                        {"id": "use_cyber_weapon", "text": "Siber Silahı Kullan", "effect": "buff:cyber_power", "combat": True, "enemy": "Rogue AI", "next_scene": "corporate_security"},
                        {"id": "call_hackers", "text": "Hacker'ları Çağır", "effect": "ally:hacker_network", "combat": True, "enemy": "Rogue AI", "next_scene": "corporate_security"},
                        {"id": "psychic_hack", "text": "Psi Hack Saldırısı", "effect": "buff:psychic_hack", "combat": True, "enemy": "Rogue AI", "next_scene": "corporate_security"}
                    ]
                },
                {
                    "id": "corporate_security",
                    "title": "Şirket Güvenlik Sistemi",
                    "description": "Arasaka'nın gelişmiş güvenlik sistemiyle karşılaştın. Bu sıra tabanlı kombat çok zorlu!",
                    "background": "/static/images/corporate_security.jpg",
                    "choices": [
                        {"id": "fight_security", "text": "Güvenlik Sistemiyle Savaş", "combat": True, "enemy": "Corporate Security", "next_scene": "cyber_dragon"},
                        {"id": "hack_security", "text": "Güvenlik Sistemini Hack Et", "effect": "buff:security_control", "combat": True, "enemy": "Corporate Security", "next_scene": "cyber_dragon"},
                        {"id": "stealth_approach", "text": "Gizlice Yaklaş", "effect": "buff:stealth_enhanced", "combat": True, "enemy": "Corporate Security", "next_scene": "cyber_dragon"},
                        {"id": "call_reinforcements", "text": "Takviye Çağır", "effect": "ally:cyber_revolution", "next_scene": "cyber_dragon"}
                    ]
                },
                {
                    "id": "cyber_dragon",
                    "title": "Siber Ejderha",
                    "description": "Arasaka'nın siber ejderha sistemi karşında! Bu devasa AI sıra tabanlı kombat ile yok edilmeli!",
                    "background": "/static/images/cyber_dragon.jpg",
                    "choices": [
                        {"id": "fight_cyber_dragon", "text": "Siber Ejderhayla Savaş", "combat": True, "enemy": "Cyber Dragon", "next_scene": "final_preparation"},
                        {"id": "hack_dragon", "text": "Ejderhayı Hack Et", "effect": "buff:dragon_control", "combat": True, "enemy": "Cyber Dragon", "next_scene": "final_preparation"},
                        {"id": "use_cyber_weapon", "text": "Siber Silahı Kullan", "effect": "buff:cyber_weapon_bonus", "combat": True, "enemy": "Cyber Dragon", "next_scene": "final_preparation"},
                        {"id": "call_ai_support", "text": "AI Desteği Çağır", "effect": "ally:friendly_ai", "next_scene": "final_preparation"}
                    ]
                },
                {
                    "id": "final_preparation",
                    "title": "Son Hazırlık",
                    "description": "Arasaka'nın ana sistemini yok etmek için son hazırlıklarını yapıyorsun. Bu savaş senin için!",
                    "background": "/static/images/final_prep.jpg",
                    "choices": [
                        {"id": "prepare_cyber_weapons", "text": "Siber Silahları Hazırla", "effect": "buff:cyber_weapon_prep", "next_scene": "boss_confrontation"},
                        {"id": "meditate_net", "text": "Net'e Meditasyon", "effect": "buff:net_blessing", "next_scene": "boss_confrontation"},
                        {"id": "coordinate_hackers", "text": "Hacker'ları Koordine Et", "effect": "ally:final_hackers", "next_scene": "boss_confrontation"},
                        {"id": "study_corporate", "text": "Şirketi Araştır", "effect": "item:corporate_intel", "next_scene": "boss_confrontation"}
                    ]
                },
                {
                    "id": "arasaka_director",
                    "title": "Arasaka Direktörü ile Yüzleşme",
                    "description": "Arasaka'nın gizli direktörü ile karşılaştın. Bu kişi tüm planların arkasındaki beyin!",
                    "background": "/static/images/arasaka_director.jpg",
                    "choices": [
                        {"id": "confront_director", "text": "Direktörle Yüzleş", "effect": "gain_xp:5", "next_scene": "final_boss_battle"},
                        {"id": "hack_director", "text": "Direktörü Hack Et", "effect": "buff:director_control", "next_scene": "final_boss_battle"},
                        {"id": "negotiate_director", "text": "Müzakere Et", "effect": "karma:+10", "next_scene": "final_boss_battle"},
                        {"id": "call_reinforcements", "text": "Takviye Çağır", "effect": "ally:cyber_revolution", "next_scene": "final_boss_battle"}
                    ]
                },
                {
                    "id": "final_boss_battle",
                    "title": "Son Boss Savaşı",
                    "description": "Arasaka'nın en güçlü AI sistemi karşında! Bu sıra tabanlı kombat senin için!",
                    "background": "/static/images/final_boss.jpg",
                    "choices": [
                        {"id": "fight_final_boss", "text": "Son Boss ile Savaş", "combat": True, "enemy": "Arasaka Final AI", "next_scene": "mission_complete"},
                        {"id": "hack_final_system", "text": "Son Sistemi Hack Et", "effect": "buff:ultimate_hack", "combat": True, "enemy": "Arasaka Final AI", "next_scene": "mission_complete"},
                        {"id": "sacrifice_cyber", "text": "Sibernetik Gücünü Feda Et", "effect": "karma:+15", "combat": True, "enemy": "Arasaka Final AI", "next_scene": "mission_complete"},
                        {"id": "call_ai_revolution", "text": "AI Devrimini Çağır", "effect": "ally:ai_revolution", "combat": True, "enemy": "Arasaka Final AI", "next_scene": "mission_complete"}
                    ]
                },
                {
                    "id": "side_mission_hackers",
                    "title": "Yan Görev: Hacker'ları Kurtar",
                    "description": "Underground hacker'ları Arasaka'nın elinde. Onları kurtarmak için yan görev!",
                    "background": "/static/images/hacker_rescue.jpg",
                    "choices": [
                        {"id": "rescue_hackers", "text": "Hacker'ları Kurtar", "effect": "ally:rescued_hackers, gain_xp:3", "next_scene": "side_mission_ai_lab"},
                        {"id": "negotiate_rescue", "text": "Müzakere ile Kurtar", "effect": "karma:+5", "next_scene": "side_mission_ai_lab"},
                        {"id": "stealth_rescue", "text": "Gizlice Kurtar", "effect": "buff:stealth_enhanced", "next_scene": "side_mission_ai_lab"},
                        {"id": "fight_rescue", "text": "Savaşarak Kurtar", "combat": True, "enemy": "Arasaka Guards", "next_scene": "side_mission_ai_lab"}
                    ]
                },
                {
                    "id": "side_mission_ai_lab",
                    "title": "Yan Görev: AI Laboratuvarı",
                    "description": "Arasaka'nın gizli AI laboratuvarını keşfet. Burada önemli bilgiler var!",
                    "background": "/static/images/ai_lab_secret.jpg",
                    "choices": [
                        {"id": "explore_lab", "text": "Laboratuvarı Keşfet", "effect": "item:ai_research_data, gain_xp:4", "next_scene": "side_mission_corporate_spy"},
                        {"id": "hack_lab_systems", "text": "Lab Sistemlerini Hack Et", "effect": "buff:ai_knowledge", "next_scene": "side_mission_corporate_spy"},
                        {"id": "steal_data", "text": "Veriyi Çal", "effect": "item:classified_ai_data", "next_scene": "side_mission_corporate_spy"},
                        {"id": "fight_lab_guards", "text": "Lab Muhafızlarıyla Savaş", "combat": True, "enemy": "Lab Security", "next_scene": "side_mission_corporate_spy"}
                    ]
                },
                {
                    "id": "side_mission_corporate_spy",
                    "title": "Yan Görev: Şirket Casusu",
                    "description": "Arasaka'ya sızmış bir casus ile karşılaştın. Bu kişi önemli bilgiler verebilir!",
                    "background": "/static/images/corporate_spy.jpg",
                    "choices": [
                        {"id": "help_spy", "text": "Casusa Yardım Et", "effect": "ally:corporate_spy, gain_xp:3", "next_scene": "side_mission_cyber_weapons"},
                        {"id": "interrogate_spy", "text": "Casusu Sorgula", "effect": "item:spy_intel", "next_scene": "side_mission_cyber_weapons"},
                        {"id": "betray_spy", "text": "Casusu Ele Ver", "effect": "karma:-10", "next_scene": "side_mission_cyber_weapons"},
                        {"id": "fight_spy", "text": "Casusla Savaş", "combat": True, "enemy": "Corporate Spy", "next_scene": "side_mission_cyber_weapons"}
                    ]
                },
                {
                    "id": "side_mission_cyber_weapons",
                    "title": "Yan Görev: Siber Silahlar",
                    "description": "Arasaka'nın gelişmiş siber silah deposunu keşfet. Bu silahlar çok güçlü!",
                    "background": "/static/images/cyber_weapons.jpg",
                    "choices": [
                        {"id": "steal_weapons", "text": "Silahları Çal", "effect": "item:advanced_cyber_weapon", "next_scene": "side_mission_ai_core"},
                        {"id": "hack_weapons", "text": "Silahları Hack Et", "effect": "buff:weapon_control", "next_scene": "side_mission_ai_core"},
                        {"id": "destroy_weapons", "text": "Silahları Yok Et", "effect": "karma:+5", "next_scene": "side_mission_ai_core"},
                        {"id": "fight_weapon_guards", "text": "Silah Muhafızlarıyla Savaş", "combat": True, "enemy": "Weapon Guards", "next_scene": "side_mission_ai_core"}
                    ]
                },
                {
                    "id": "side_mission_ai_core",
                    "title": "Yan Görev: AI Çekirdeği",
                    "description": "Arasaka'nın AI çekirdek sistemine ulaştın. Bu sistem tüm AI'ları kontrol ediyor!",
                    "background": "/static/images/ai_core.jpg",
                    "choices": [
                        {"id": "hack_core", "text": "Çekirdeği Hack Et", "effect": "buff:ai_core_control", "next_scene": "side_mission_final"},
                        {"id": "destroy_core", "text": "Çekirdeği Yok Et", "effect": "karma:+10", "next_scene": "side_mission_final"},
                        {"id": "study_core", "text": "Çekirdeği İncele", "effect": "item:ai_core_data", "next_scene": "side_mission_final"},
                        {"id": "fight_core_guard", "text": "Çekirdek Muhafızıyla Savaş", "combat": True, "enemy": "AI Core Guardian", "next_scene": "side_mission_final"}
                    ]
                },
                {
                    "id": "side_mission_final",
                    "title": "Yan Görev: Son Direniş",
                    "description": "Arasaka'nın son direniş noktası. Bu yeri ele geçirmek çok önemli!",
                    "background": "/static/images/final_resistance.jpg",
                    "choices": [
                        {"id": "attack_resistance", "text": "Direnişe Saldır", "combat": True, "enemy": "Final Resistance", "next_scene": "mission_complete"},
                        {"id": "hack_resistance", "text": "Direnişi Hack Et", "effect": "buff:resistance_control", "next_scene": "mission_complete"},
                        {"id": "negotiate_resistance", "text": "Direnişle Müzakere", "effect": "karma:+5", "next_scene": "mission_complete"},
                        {"id": "call_allies", "text": "Müttefikleri Çağır", "effect": "ally:final_allies", "next_scene": "mission_complete"}
                    ]
                },
                {
                    "id": "night_city_underground",
                    "title": "Night City Yeraltı",
                    "description": "Night City'nin yeraltı tünellerine ulaştın. Burada gizli hacker'lar ve yeraltı ağları var!",
                    "background": "/static/images/underground_tunnels.jpg",
                    "choices": [
                        {"id": "explore_underground", "text": "Yeraltını Keşfet", "effect": "item:underground_map, gain_xp:3", "next_scene": "hacker_meeting"},
                        {"id": "stealth_approach", "text": "Gizlice Yaklaş", "effect": "buff:stealth_bonus", "next_scene": "hacker_meeting"},
                        {"id": "fight_underground_guards", "text": "Yeraltı Muhafızlarıyla Savaş", "combat": True, "enemy": "Underground Guards", "next_scene": "hacker_meeting"},
                        {"id": "call_underground_allies", "text": "Yeraltı Müttefiklerini Çağır", "effect": "ally:underground_network", "next_scene": "hacker_meeting"}
                    ]
                },
                {
                    "id": "hacker_meeting",
                    "title": "Hacker Toplantısı",
                    "description": "Night City'nin en ünlü hacker'ları ile karşılaştın. Bu kişiler çok güçlü!",
                    "background": "/static/images/hacker_meeting.jpg",
                    "choices": [
                        {"id": "join_hackers", "text": "Hacker'lara Katıl", "effect": "ally:elite_hackers, gain_xp:4", "next_scene": "cyber_market"},
                        {"id": "compete_hackers", "text": "Hacker'larla Yarış", "effect": "buff:competition_bonus", "next_scene": "cyber_market"},
                        {"id": "fight_hackers", "text": "Hacker'larla Savaş", "combat": True, "enemy": "Elite Hackers", "next_scene": "cyber_market"},
                        {"id": "negotiate_hackers", "text": "Hacker'larla Müzakere", "effect": "karma:+5", "next_scene": "cyber_market"}
                    ]
                },
                {
                    "id": "cyber_market",
                    "title": "Siber Pazar",
                    "description": "Night City'nin gizli siber pazarını keşfettin. Burada her şey satılıyor!",
                    "background": "/static/images/cyber_market.jpg",
                    "choices": [
                        {"id": "buy_cyber_weapons", "text": "Siber Silahlar Satın Al", "effect": "item:advanced_cyber_weapons", "next_scene": "cyber_clinic"},
                        {"id": "sell_information", "text": "Bilgi Sat", "effect": "gain_xp:4", "next_scene": "cyber_clinic"},
                        {"id": "fight_market_guards", "text": "Pazar Muhafızlarıyla Savaş", "combat": True, "enemy": "Market Guards", "next_scene": "cyber_clinic"},
                        {"id": "negotiate_market", "text": "Pazarla Müzakere", "effect": "karma:+5", "next_scene": "cyber_clinic"}
                    ]
                },
                {
                    "id": "cyber_clinic",
                    "title": "Siber Klinik",
                    "description": "Night City'nin en iyi siber kliniğini keşfettin. Burada gelişmiş implantlar var!",
                    "background": "/static/images/cyber_clinic.jpg",
                    "choices": [
                        {"id": "get_cyber_implants", "text": "Siber İmplant Tak", "effect": "buff:cyber_enhancement", "next_scene": "corporate_spy"},
                        {"id": "heal_cyber_damage", "text": "Siber Hasarı Tedavi Et", "effect": "buff:health_restored", "next_scene": "corporate_spy"},
                        {"id": "fight_clinic_guards", "text": "Klinik Muhafızlarıyla Savaş", "combat": True, "enemy": "Clinic Guards", "next_scene": "corporate_spy"},
                        {"id": "hack_clinic_systems", "text": "Klinik Sistemlerini Hack Et", "effect": "buff:clinic_control", "next_scene": "corporate_spy"}
                    ]
                },
                {
                    "id": "corporate_spy",
                    "title": "Şirket Casusu",
                    "description": "Arasaka'ya sızmış bir casus ile karşılaştın. Bu kişi önemli bilgiler verebilir!",
                    "background": "/static/images/corporate_spy.jpg",
                    "choices": [
                        {"id": "help_spy", "text": "Casusa Yardım Et", "effect": "ally:corporate_spy, gain_xp:3", "next_scene": "cyber_gang"},
                        {"id": "interrogate_spy", "text": "Casusu Sorgula", "effect": "item:spy_intel", "next_scene": "cyber_gang"},
                        {"id": "betray_spy", "text": "Casusu Ele Ver", "effect": "karma:-10", "next_scene": "cyber_gang"},
                        {"id": "fight_spy", "text": "Casusla Savaş", "combat": True, "enemy": "Corporate Spy", "next_scene": "cyber_gang"}
                    ]
                },
                {
                    "id": "cyber_gang",
                    "title": "Siber Çete",
                    "description": "Night City'nin en tehlikeli siber çetesi ile karşılaştın. Bu çete çok güçlü!",
                    "background": "/static/images/cyber_gang.jpg",
                    "choices": [
                        {"id": "join_gang", "text": "Çeteye Katıl", "effect": "ally:cyber_gang, gain_xp:4", "next_scene": "cyber_arena"},
                        {"id": "fight_gang", "text": "Çeteyle Savaş", "combat": True, "enemy": "Cyber Gang", "next_scene": "cyber_arena"},
                        {"id": "negotiate_gang", "text": "Çeteyle Müzakere", "effect": "karma:+5", "next_scene": "cyber_arena"},
                        {"id": "infiltrate_gang", "text": "Çeteye Sız", "effect": "buff:infiltration_bonus", "next_scene": "cyber_arena"}
                    ]
                },
                {
                    "id": "cyber_arena",
                    "title": "Siber Arena",
                    "description": "Night City'nin ünlü siber arenasına ulaştın. Burada savaşçılar dövüşüyor!",
                    "background": "/static/images/cyber_arena.jpg",
                    "choices": [
                        {"id": "fight_in_arena", "text": "Arenada Dövüş", "combat": True, "enemy": "Arena Champion", "next_scene": "cyber_temple"},
                        {"id": "bet_on_fights", "text": "Dövüşlere Bahis Yap", "effect": "gain_xp:3", "next_scene": "cyber_temple"},
                        {"id": "challenge_champion", "text": "Şampiyonu Meydan Oku", "effect": "buff:challenge_bonus", "next_scene": "cyber_temple"},
                        {"id": "join_arena", "text": "Arenaya Katıl", "effect": "ally:arena_fighters", "next_scene": "cyber_temple"}
                    ]
                },
                {
                    "id": "cyber_temple",
                    "title": "Siber Tapınak",
                    "description": "Night City'nin gizli siber tapınağını keşfettin. Burada eski teknolojiler var!",
                    "background": "/static/images/cyber_temple.jpg",
                    "choices": [
                        {"id": "explore_temple", "text": "Tapınağı Keşfet", "effect": "item:ancient_tech, gain_xp:4", "next_scene": "cyber_monastery"},
                        {"id": "meditate_temple", "text": "Tapınakta Meditasyon", "effect": "buff:spiritual_blessing", "next_scene": "cyber_monastery"},
                        {"id": "fight_temple_guards", "text": "Tapınak Muhafızlarıyla Savaş", "combat": True, "enemy": "Temple Guards", "next_scene": "cyber_monastery"},
                        {"id": "study_temple", "text": "Tapınağı İncele", "effect": "item:temple_knowledge", "next_scene": "cyber_monastery"}
                    ]
                },
                {
                    "id": "cyber_monastery",
                    "title": "Siber Manastır",
                    "description": "Night City'nin gizli siber manastırını keşfettin. Burada bilge keşişler var!",
                    "background": "/static/images/cyber_monastery.jpg",
                    "choices": [
                        {"id": "learn_from_monks", "text": "Keşişlerden Öğren", "effect": "gain_xp:5, buff:wisdom_blessing", "next_scene": "cyber_library"},
                        {"id": "meditate_with_monks", "text": "Keşişlerle Meditasyon", "effect": "buff:meditation_bonus", "next_scene": "cyber_library"},
                        {"id": "fight_monastery_guards", "text": "Manastır Muhafızlarıyla Savaş", "combat": True, "enemy": "Monastery Guards", "next_scene": "cyber_library"},
                        {"id": "join_monastery", "text": "Manastıra Katıl", "effect": "ally:cyber_monks", "next_scene": "cyber_library"}
                    ]
                },
                {
                    "id": "cyber_library",
                    "title": "Siber Kütüphane",
                    "description": "Night City'nin gizli siber kütüphanesini keşfettin. Burada eski bilgiler var!",
                    "background": "/static/images/cyber_library.jpg",
                    "choices": [
                        {"id": "read_books", "text": "Kitapları Oku", "effect": "item:ancient_knowledge, gain_xp:4", "next_scene": "cyber_laboratory"},
                        {"id": "steal_books", "text": "Kitapları Çal", "effect": "item:stolen_books", "next_scene": "cyber_laboratory"},
                        {"id": "fight_library_guards", "text": "Kütüphane Muhafızlarıyla Savaş", "combat": True, "enemy": "Library Guards", "next_scene": "cyber_laboratory"},
                        {"id": "study_library", "text": "Kütüphaneyi İncele", "effect": "buff:knowledge_power", "next_scene": "cyber_laboratory"}
                    ]
                },
                {
                    "id": "cyber_laboratory",
                    "title": "Siber Laboratuvar",
                    "description": "Night City'nin gizli siber laboratuvarını keşfettin. Burada gelişmiş teknolojiler var!",
                    "background": "/static/images/cyber_laboratory.jpg",
                    "choices": [
                        {"id": "steal_technology", "text": "Teknolojileri Çal", "effect": "item:advanced_tech", "next_scene": "cyber_prison"},
                        {"id": "study_technology", "text": "Teknolojileri İncele", "effect": "item:tech_knowledge", "next_scene": "cyber_prison"},
                        {"id": "fight_lab_guards", "text": "Lab Muhafızlarıyla Savaş", "combat": True, "enemy": "Lab Guards", "next_scene": "cyber_prison"},
                        {"id": "hack_lab_systems", "text": "Lab Sistemlerini Hack Et", "effect": "buff:lab_control", "next_scene": "cyber_prison"}
                    ]
                },
                {
                    "id": "cyber_prison",
                    "title": "Siber Hapishane",
                    "description": "Night City'nin gizli siber hapishanesini keşfettin. Burada mahkumlar var!",
                    "background": "/static/images/cyber_prison.jpg",
                    "choices": [
                        {"id": "free_prisoners", "text": "Mahkumları Serbest Bırak", "effect": "ally:freed_prisoners, gain_xp:4", "next_scene": "cyber_factory"},
                        {"id": "interrogate_prisoners", "text": "Mahkumları Sorgula", "effect": "item:prisoner_intel", "next_scene": "cyber_factory"},
                        {"id": "fight_prison_guards", "text": "Hapishane Muhafızlarıyla Savaş", "combat": True, "enemy": "Prison Guards", "next_scene": "cyber_factory"},
                        {"id": "negotiate_prisoners", "text": "Mahkumlarla Müzakere", "effect": "karma:+5", "next_scene": "cyber_factory"}
                    ]
                },
                {
                    "id": "cyber_factory",
                    "title": "Siber Fabrika",
                    "description": "Night City'nin gizli siber fabrikasını keşfettin. Burada robotlar üretiliyor!",
                    "background": "/static/images/cyber_factory.jpg",
                    "choices": [
                        {"id": "sabotage_factory", "text": "Fabrikayı Sabote Et", "effect": "buff:sabotage_bonus", "next_scene": "cyber_warehouse"},
                        {"id": "hack_factory_systems", "text": "Fabrika Sistemlerini Hack Et", "effect": "buff:factory_control", "next_scene": "cyber_warehouse"},
                        {"id": "fight_factory_robots", "text": "Fabrika Robotlarıyla Savaş", "combat": True, "enemy": "Factory Robots", "next_scene": "cyber_warehouse"},
                        {"id": "steal_factory_tech", "text": "Fabrika Teknolojisini Çal", "effect": "item:factory_tech", "next_scene": "cyber_warehouse"}
                    ]
                },
                {
                    "id": "cyber_warehouse",
                    "title": "Siber Depo",
                    "description": "Night City'nin gizli siber deposunu keşfettin. Burada her şey saklanıyor!",
                    "background": "/static/images/cyber_warehouse.jpg",
                    "choices": [
                        {"id": "explore_warehouse", "text": "Depoyu Keşfet", "effect": "item:warehouse_loot, gain_xp:4", "next_scene": "cyber_bunker"},
                        {"id": "steal_warehouse_goods", "text": "Depo Mallarını Çal", "effect": "item:stolen_goods", "next_scene": "cyber_bunker"},
                        {"id": "fight_warehouse_guards", "text": "Depo Muhafızlarıyla Savaş", "combat": True, "enemy": "Warehouse Guards", "next_scene": "cyber_bunker"},
                        {"id": "hack_warehouse_systems", "text": "Depo Sistemlerini Hack Et", "effect": "buff:warehouse_control", "next_scene": "cyber_bunker"}
                    ]
                },
                {
                    "id": "cyber_bunker",
                    "title": "Siber Sığınak",
                    "description": "Night City'nin gizli siber sığınağını keşfettin. Burada sığınmacılar var!",
                    "background": "/static/images/cyber_bunker.jpg",
                    "choices": [
                        {"id": "help_refugees", "text": "Sığınmacılara Yardım Et", "effect": "ally:refugees, gain_xp:3", "next_scene": "cyber_control_center"},
                        {"id": "negotiate_refugees", "text": "Sığınmacılarla Müzakere", "effect": "karma:+5", "next_scene": "cyber_control_center"},
                        {"id": "fight_bunker_guards", "text": "Sığınak Muhafızlarıyla Savaş", "combat": True, "enemy": "Bunker Guards", "next_scene": "cyber_control_center"},
                        {"id": "hack_bunker_systems", "text": "Sığınak Sistemlerini Hack Et", "effect": "buff:bunker_control", "next_scene": "cyber_control_center"}
                    ]
                },
                {
                    "id": "cyber_control_center",
                    "title": "Siber Kontrol Merkezi",
                    "description": "Night City'nin gizli siber kontrol merkezini keşfettin. Buradan tüm sistemi kontrol edebilirsin!",
                    "background": "/static/images/cyber_control_center.jpg",
                    "choices": [
                        {"id": "hack_control_systems", "text": "Kontrol Sistemlerini Hack Et", "effect": "buff:city_control", "next_scene": "cyber_final_battle"},
                        {"id": "take_control", "text": "Kontrolü Ele Geçir", "effect": "ally:control_team", "next_scene": "cyber_final_battle"},
                        {"id": "fight_control_guards", "text": "Kontrol Merkezi Muhafızlarıyla Savaş", "combat": True, "enemy": "Control Guards", "next_scene": "cyber_final_battle"},
                        {"id": "negotiate_control", "text": "Kontrol Merkeziyle Müzakere", "effect": "karma:+10", "next_scene": "cyber_final_battle"}
                    ]
                },
                {
                    "id": "cyber_final_battle",
                    "title": "Siber Son Savaş",
                    "description": "Night City'nin son savaşı başladı! Bu sıra tabanlı kombat senin için!",
                    "background": "/static/images/cyber_final_battle.jpg",
                    "choices": [
                        {"id": "fight_final_battle", "text": "Son Savaşta Savaş", "combat": True, "enemy": "Cyber Final Boss", "next_scene": "mission_complete"},
                        {"id": "hack_final_systems", "text": "Son Sistemleri Hack Et", "effect": "buff:final_hack", "combat": True, "enemy": "Cyber Final Boss", "next_scene": "mission_complete"},
                        {"id": "call_final_allies", "text": "Son Müttefikleri Çağır", "effect": "ally:final_allies", "combat": True, "enemy": "Cyber Final Boss", "next_scene": "mission_complete"},
                        {"id": "negotiate_final", "text": "Son Müzakere", "effect": "karma:+15", "next_scene": "mission_complete"}
                    ]
                },
                {
                    "id": "mission_complete",
                    "title": "Görev Tamamlandı",
                    "description": "Night City'de yeni bir efsane doğdu. Netrunner olarak ünün arttı!",
                    "choices": []
                }
            ]
        }
        
        # Hive City kampanyası ekle
        hive_campaign = {
            "id": "hive_city_defense",
            "name": "🏙️ Hive Şehrinin Savunması",
            "type": "warhammer40k",
            "description": "Hive şehri kaos istilası altında. Senin seçimlerin şehrin kaderini belirleyecek. Plot twist'ler ve ihanetler her yerde. Seçimlerinin sonuçlarını ancak sonunda öğreneceksin.",
            "scenes": [
                {
                    "id": "intro",
                    "title": "Hive Şehrinde Uyanış",
                    "description": "Hive şehrinin 47. seviyesinde, karanlık bir odada gözlerini açtın. Yukarıdan gelen patlamalar ve çığlıklar... Şehir saldırı altında. Ork istilası başladı ve sen, seçilmiş asker, bu tehdidi durdurmak için buradasın.",
                    "background": "/static/images/hive_city.jpg",
                    "choices": [
                        {"id": "check_equipment", "text": "Ekipmanı Kontrol Et", "effect": "item:lasgun, gain_xp:3", "next_scene": "upper_levels"},
                        {"id": "pray_emperor", "text": "İmparator'a Dua Et", "effect": "buff:faith_bonus, gain_xp:2", "next_scene": "upper_levels"},
                        {"id": "help_civilians", "text": "Sivillere Yardım Et", "effect": "karma:+5, gain_xp:2", "next_scene": "upper_levels"},
                        {"id": "find_commander", "text": "Komutanı Ara", "effect": "gain_xp:1", "next_scene": "upper_levels"}
                    ]
                },
                {
                    "id": "upper_levels",
                    "title": "Üst Seviyeler",
                    "description": "Üst seviyelere çıktın. Hive'ın 23. seviyesi kaos içinde. İnsanlar panik halinde kaçışıyor. Bir subay seni görüyor ve koşarak geliyor.",
                    "background": "/static/images/hive_upper_levels.jpg",
                    "choices": [
                        {"id": "report_to_officer", "text": "Subaya Rapor Ver", "next_scene": "command_center"},
                        {"id": "evacuate_civilians", "text": "Sivilleri Tahliye Et", "effect": "karma:+3, gain_xp:2", "next_scene": "command_center"},
                        {"id": "fight_orks", "text": "Orklarla Savaş", "combat": True, "enemy": "Ork Boyz", "next_scene": "command_center"},
                        {"id": "find_weapons", "text": "Silah Ara", "effect": "item:plasma_gun", "next_scene": "command_center"}
                    ]
                },
                {
                    "id": "command_center",
                    "title": "Komuta Merkezi",
                    "description": "Komuta merkezine ulaştın. Komutan Voss seni bekliyor. Hive şehri tamamen kuşatılmış durumda. Warboss Gorgutz'un ordusu şehre saldırıyor.",
                    "background": "/static/images/hive_command_center.jpg",
                    "choices": [
                        {"id": "accept_mission", "text": "Görevi Kabul Et", "next_scene": "defense_preparation"},
                        {"id": "ask_details", "text": "Detayları Sor", "effect": "gain_xp:2", "next_scene": "defense_preparation"},
                        {"id": "request_backup", "text": "Takviye İste", "effect": "ally:imperial_guard", "next_scene": "defense_preparation"},
                        {"id": "strategic_planning", "text": "Stratejik Planlama", "effect": "buff:tactical_advantage", "next_scene": "defense_preparation"}
                    ]
                },
                {
                    "id": "defense_preparation",
                    "title": "Savunma Hazırlığı",
                    "description": "Hive şehrinin savunma hatlarını hazırlıyorsun. Ork ordusu yaklaşıyor, her dakika önemli. Imperial Guard birlikleri pozisyon alıyor.",
                    "background": "/static/images/hive_command_center.jpg",
                    "choices": [
                        {"id": "fortify_position", "text": "Pozisyonu Güçlendir", "effect": "buff:defense_bonus", "next_scene": "ork_scout_patrol"},
                        {"id": "set_traps", "text": "Tuzaklar Kur", "effect": "buff:ambush_bonus", "next_scene": "ork_scout_patrol"},
                        {"id": "coordinate_artillery", "text": "Topçuyu Koordine Et", "effect": "buff:artillery_support", "next_scene": "ork_scout_patrol"},
                        {"id": "inspire_troops", "text": "Birlikleri Motive Et", "effect": "buff:morale_boost", "next_scene": "ork_scout_patrol"}
                    ]
                },
                {
                    "id": "ork_scout_patrol",
                    "title": "Ork Keşif Devriyesi",
                    "description": "İlk Ork keşif devriyesi geldi! Küçük bir grup Ork Boyz savunma hatlarını test ediyor. Bu sadece başlangıç...",
                    "background": "/static/images/hive_upper_levels.jpg",
                    "choices": [
                        {"id": "engage_scouts", "text": "Keşif Devriyesiyle Savaş", "combat": True, "enemy": "Ork Scouts", "next_scene": "main_ork_force"},
                        {"id": "let_them_pass", "text": "Geçmelerine İzin Ver", "effect": "gain_xp:1", "next_scene": "main_ork_force"},
                        {"id": "ambush_scouts", "text": "Pusu Kur", "effect": "buff:surprise_attack", "combat": True, "enemy": "Ork Scouts", "next_scene": "main_ork_force"},
                        {"id": "interrogate_captive", "text": "Esir Al ve Sorgula", "effect": "item:intel_data, gain_xp:3", "next_scene": "main_ork_force"}
                    ]
                },
                {
                    "id": "main_ork_force",
                    "title": "Ana Ork Gücü",
                    "description": "Ana Ork ordusu geldi! Gökyüzü yeşil bulutlarla kaplandı, Warboss Gorgutz'un savaş çığlıkları yankılanıyor. 50,000 Ork Hive şehrine saldırıyor!",
                    "background": "/static/images/hive_battle.jpg",
                    "choices": [
                        {"id": "hold_defense_line", "text": "Savunma Hattını Tut", "combat": True, "enemy": "Ork Horde", "next_scene": "warboss_reveal"},
                        {"id": "counter_attack", "text": "Karşı Saldırı", "combat": True, "enemy": "Ork Elite", "next_scene": "warboss_reveal"},
                        {"id": "artillery_barrage", "text": "Topçu Saldırısı", "effect": "buff:artillery_support", "next_scene": "warboss_reveal"},
                        {"id": "tactical_retreat", "text": "Taktik Geri Çekilme", "next_scene": "regroup"}
                    ]
                },
                {
                    "id": "warboss_reveal",
                    "title": "Warboss Gorgutz'un Görünüşü",
                    "description": "Savaşın ortasında Warboss Gorgutz göründü! 5 metre boyunda, yeşil derili, devasa silahlarla donanmış. Bu savaş senin için!",
                    "background": "/static/images/hive_battle.jpg",
                    "choices": [
                        {"id": "challenge_warboss", "text": "Warboss'u Meydan Oku", "combat": True, "enemy": "Warboss Gorgutz", "next_scene": "victory"},
                        {"id": "use_psychic", "text": "Psi Gücü Kullan", "effect": "buff:psychic_boost", "combat": True, "enemy": "Warboss Gorgutz", "next_scene": "victory"},
                        {"id": "call_reinforcements", "text": "Takviye Çağır", "effect": "ally:space_marines", "next_scene": "victory"},
                        {"id": "tactical_retreat", "text": "Taktik Geri Çekilme", "next_scene": "regroup"}
                    ]
                },
                {
                    "id": "hive_underground",
                    "title": "Hive Yeraltı Tünelleri",
                    "description": "Hive şehrinin yeraltı tünellerine ulaştın. Burada Ork sabotajcıları var!",
                    "background": "/static/images/hive_underground.jpg",
                    "choices": [
                        {"id": "explore_tunnels", "text": "Tünelleri Keşfet", "effect": "item:tunnel_map, gain_xp:3", "next_scene": "ork_saboteurs"},
                        {"id": "stealth_approach", "text": "Gizlice Yaklaş", "effect": "buff:stealth_bonus", "next_scene": "ork_saboteurs"},
                        {"id": "fight_saboteurs", "text": "Sabotajcılarla Savaş", "combat": True, "enemy": "Ork Saboteurs", "next_scene": "ork_saboteurs"},
                        {"id": "call_reinforcements", "text": "Takviye Çağır", "effect": "ally:underground_forces", "next_scene": "ork_saboteurs"}
                    ]
                },
                {
                    "id": "ork_saboteurs",
                    "title": "Ork Sabotajcıları",
                    "description": "Hive'ın kritik sistemlerini sabote etmeye çalışan Ork sabotajcıları!",
                    "background": "/static/images/ork_saboteurs.jpg",
                    "choices": [
                        {"id": "fight_saboteurs", "text": "Sabotajcılarla Savaş", "combat": True, "enemy": "Ork Saboteurs", "next_scene": "hive_reactor"},
                        {"id": "hack_systems", "text": "Sistemleri Hack Et", "effect": "buff:system_control", "next_scene": "hive_reactor"},
                        {"id": "stealth_eliminate", "text": "Gizlice Yok Et", "effect": "buff:stealth_enhanced", "next_scene": "hive_reactor"},
                        {"id": "call_tech_support", "text": "Teknik Desteği Çağır", "effect": "ally:tech_team", "next_scene": "hive_reactor"}
                    ]
                },
                {
                    "id": "hive_reactor",
                    "title": "Hive Reaktörü",
                    "description": "Hive şehrinin güç reaktörü tehlikede! Ork sabotajcıları reaktörü patlatmaya çalışıyor.",
                    "background": "/static/images/hive_reactor.jpg",
                    "choices": [
                        {"id": "stabilize_reactor", "text": "Reaktörü Stabilize Et", "effect": "item:reactor_data, gain_xp:4", "next_scene": "ork_elite_guard"},
                        {"id": "hack_reactor", "text": "Reaktörü Hack Et", "effect": "buff:reactor_control", "next_scene": "ork_elite_guard"},
                        {"id": "fight_reactor_guards", "text": "Reaktör Muhafızlarıyla Savaş", "combat": True, "enemy": "Reactor Guards", "next_scene": "ork_elite_guard"},
                        {"id": "call_engineers", "text": "Mühendisleri Çağır", "effect": "ally:engineering_team", "next_scene": "ork_elite_guard"}
                    ]
                },
                {
                    "id": "ork_elite_guard",
                    "title": "Ork Elit Muhafızları",
                    "description": "Warboss'un elit muhafızları Hive'ın üst seviyelerinde! Bu sıra tabanlı kombat çok zorlu!",
                    "background": "/static/images/ork_elite_guard.jpg",
                    "choices": [
                        {"id": "fight_elite_guard", "text": "Elit Muhafızlarla Savaş", "combat": True, "enemy": "Ork Elite Guard", "next_scene": "hive_command_center"},
                        {"id": "use_heavy_weapons", "text": "Ağır Silahları Kullan", "effect": "buff:heavy_weapon_bonus", "combat": True, "enemy": "Ork Elite Guard", "next_scene": "hive_command_center"},
                        {"id": "tactical_retreat", "text": "Taktik Geri Çekilme", "next_scene": "regroup"},
                        {"id": "call_reinforcements", "text": "Takviye Çağır", "effect": "ally:imperial_elite", "next_scene": "hive_command_center"}
                    ]
                },
                {
                    "id": "hive_command_center",
                    "title": "Hive Komuta Merkezi",
                    "description": "Hive'ın ana komuta merkezi. Burada Warboss'un planlarını öğrenebilirsin!",
                    "background": "/static/images/hive_command.jpg",
                    "choices": [
                        {"id": "hack_command_systems", "text": "Komuta Sistemlerini Hack Et", "effect": "item:command_data, gain_xp:5", "next_scene": "warboss_preparation"},
                        {"id": "steal_intelligence", "text": "İstihbarat Çal", "effect": "item:ork_intelligence", "next_scene": "warboss_preparation"},
                        {"id": "fight_command_guards", "text": "Komuta Muhafızlarıyla Savaş", "combat": True, "enemy": "Command Guards", "next_scene": "warboss_preparation"},
                        {"id": "call_intelligence", "text": "İstihbarat Ekibini Çağır", "effect": "ally:intelligence_team", "next_scene": "warboss_preparation"}
                    ]
                },
                {
                    "id": "warboss_preparation",
                    "title": "Warboss'a Hazırlık",
                    "description": "Warboss Gorgutz'a karşı son hazırlıklarını yapıyorsun. Bu savaş senin için!",
                    "background": "/static/images/warboss_prep.jpg",
                    "choices": [
                        {"id": "prepare_weapons", "text": "Silahları Hazırla", "effect": "buff:weapon_preparation", "next_scene": "warboss_confrontation"},
                        {"id": "meditate_emperor", "text": "İmparator'a Meditasyon", "effect": "buff:divine_blessing", "next_scene": "warboss_confrontation"},
                        {"id": "coordinate_allies", "text": "Müttefikleri Koordine Et", "effect": "ally:final_allies", "next_scene": "warboss_confrontation"},
                        {"id": "study_warboss", "text": "Warboss'u Araştır", "effect": "item:warboss_intel", "next_scene": "warboss_confrontation"}
                    ]
                },
                {
                    "id": "side_mission_civilians",
                    "title": "Yan Görev: Sivilleri Kurtar",
                    "description": "Hive'da mahsur kalmış siviller var. Onları kurtarmak için yan görev!",
                    "background": "/static/images/civilians.jpg",
                    "choices": [
                        {"id": "rescue_civilians", "text": "Sivilleri Kurtar", "effect": "ally:rescued_civilians, gain_xp:3", "next_scene": "side_mission_medical"},
                        {"id": "negotiate_rescue", "text": "Müzakere ile Kurtar", "effect": "karma:+5", "next_scene": "side_mission_medical"},
                        {"id": "stealth_rescue", "text": "Gizlice Kurtar", "effect": "buff:stealth_enhanced", "next_scene": "side_mission_medical"},
                        {"id": "fight_rescue", "text": "Savaşarak Kurtar", "combat": True, "enemy": "Ork Raiders", "next_scene": "side_mission_medical"}
                    ]
                },
                {
                    "id": "side_mission_medical",
                    "title": "Yan Görev: Tıbbi Merkez",
                    "description": "Hive'ın tıbbi merkezi tehlikede. Yaralıları kurtarmak için buradayısın!",
                    "background": "/static/images/medical_center.jpg",
                    "choices": [
                        {"id": "secure_medical", "text": "Tıbbi Merkezi Güvenli Hale Getir", "effect": "ally:medical_team, gain_xp:4", "next_scene": "side_mission_armory"},
                        {"id": "hack_medical_systems", "text": "Tıbbi Sistemleri Hack Et", "effect": "buff:medical_control", "next_scene": "side_mission_armory"},
                        {"id": "fight_medical_guards", "text": "Tıbbi Muhafızlarla Savaş", "combat": True, "enemy": "Medical Guards", "next_scene": "side_mission_armory"},
                        {"id": "call_medics", "text": "Doktorları Çağır", "effect": "ally:medical_support", "next_scene": "side_mission_armory"}
                    ]
                },
                {
                    "id": "side_mission_armory",
                    "title": "Yan Görev: Cephanelik",
                    "description": "Hive'ın cephaneliği. Burada güçlü silahlar var!",
                    "background": "/static/images/armory.jpg",
                    "choices": [
                        {"id": "secure_armory", "text": "Cephaneliği Güvenli Hale Getir", "effect": "item:advanced_weapons", "next_scene": "side_mission_communications"},
                        {"id": "hack_armory_systems", "text": "Cephanelik Sistemlerini Hack Et", "effect": "buff:weapon_control", "next_scene": "side_mission_communications"},
                        {"id": "fight_armory_guards", "text": "Cephanelik Muhafızlarıyla Savaş", "combat": True, "enemy": "Armory Guards", "next_scene": "side_mission_communications"},
                        {"id": "call_weapon_team", "text": "Silah Ekibini Çağır", "effect": "ally:weapon_support", "next_scene": "side_mission_communications"}
                    ]
                },
                {
                    "id": "side_mission_communications",
                    "title": "Yan Görev: İletişim Merkezi",
                    "description": "Hive'ın iletişim merkezi. Buradan tüm sistemi koordine edebilirsin!",
                    "background": "/static/images/communications.jpg",
                    "choices": [
                        {"id": "hack_communications", "text": "İletişim Sistemlerini Hack Et", "effect": "buff:communication_control", "next_scene": "side_mission_final"},
                        {"id": "secure_communications", "text": "İletişimi Güvenli Hale Getir", "effect": "ally:communication_team", "next_scene": "side_mission_final"},
                        {"id": "fight_comm_guards", "text": "İletişim Muhafızlarıyla Savaş", "combat": True, "enemy": "Communication Guards", "next_scene": "side_mission_final"},
                        {"id": "call_tech_support", "text": "Teknik Desteği Çağır", "effect": "ally:tech_support", "next_scene": "side_mission_final"}
                    ]
                },
                {
                    "id": "side_mission_final",
                    "title": "Yan Görev: Son Direniş",
                    "description": "Hive'ın son direniş noktası. Bu yeri ele geçirmek çok önemli!",
                    "background": "/static/images/final_resistance.jpg",
                    "choices": [
                        {"id": "attack_resistance", "text": "Direnişe Saldır", "combat": True, "enemy": "Final Resistance", "next_scene": "victory"},
                        {"id": "hack_resistance", "text": "Direnişi Hack Et", "effect": "buff:resistance_control", "next_scene": "victory"},
                        {"id": "negotiate_resistance", "text": "Direnişle Müzakere", "effect": "karma:+5", "next_scene": "victory"},
                        {"id": "call_allies", "text": "Müttefikleri Çağır", "effect": "ally:final_allies", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "hive_commissar_office",
                    "title": "Commissar Ofisi",
                    "description": "Hive'ın Commissar ofisine ulaştın. Burada güçlü Commissar var!",
                    "background": "/static/images/hive_commissar_office.jpg",
                    "choices": [
                        {"id": "meet_commissar", "text": "Commissar ile Görüş", "effect": "ally:hive_commissar, gain_xp:4", "next_scene": "hive_priest_chapel"},
                        {"id": "learn_discipline", "text": "Disiplin Öğren", "effect": "buff:discipline_power", "next_scene": "hive_priest_chapel"},
                        {"id": "fight_commissar", "text": "Commissar ile Savaş", "combat": True, "enemy": "Hive Commissar", "next_scene": "hive_priest_chapel"},
                        {"id": "receive_commissar_blessing", "text": "Commissar Kutsaması Al", "effect": "buff:commissar_blessing", "next_scene": "hive_priest_chapel"}
                    ]
                },
                {
                    "id": "hive_priest_chapel",
                    "title": "Hive Rahip Şapeli",
                    "description": "Hive'ın rahip şapeline ulaştın. Burada güçlü rahipler var!",
                    "background": "/static/images/hive_priest_chapel.jpg",
                    "choices": [
                        {"id": "pray_with_priest", "text": "Rahiple Dua Et", "effect": "buff:priest_blessing, gain_xp:4", "next_scene": "hive_ogryn_barracks"},
                        {"id": "learn_faith", "text": "İmparator İnancını Öğren", "effect": "buff:faith_power", "next_scene": "hive_ogryn_barracks"},
                        {"id": "fight_priest", "text": "Rahiple Savaş", "combat": True, "enemy": "Hive Priest", "next_scene": "hive_ogryn_barracks"},
                        {"id": "receive_priest_blessing", "text": "Rahip Kutsaması Al", "effect": "buff:divine_protection", "next_scene": "hive_ogryn_barracks"}
                    ]
                },
                {
                    "id": "hive_ogryn_barracks",
                    "title": "Hive Ogryn Kışlası",
                    "description": "Hive'ın Ogryn kışlasına ulaştın. Burada güçlü Ogryn'ler var!",
                    "background": "/static/images/hive_ogryn_barracks.jpg",
                    "choices": [
                        {"id": "train_with_ogryns", "text": "Ogryn'lerle Eğitim Al", "effect": "ally:hive_ogryns, gain_xp:5", "next_scene": "hive_ratling_snipers"},
                        {"id": "learn_ogryn_strength", "text": "Ogryn Gücünü Öğren", "effect": "buff:ogryn_strength", "next_scene": "hive_ratling_snipers"},
                        {"id": "fight_ogryn", "text": "Ogryn ile Savaş", "combat": True, "enemy": "Hive Ogryn", "next_scene": "hive_ratling_snipers"},
                        {"id": "study_ogryn_lore", "text": "Ogryn Lore'unu Öğren", "effect": "item:ogryn_lore", "next_scene": "hive_ratling_snipers"}
                    ]
                },
                {
                    "id": "hive_ratling_snipers",
                    "title": "Hive Ratling Keskin Nişancıları",
                    "description": "Hive'ın Ratling keskin nişancılarına ulaştın. Burada güçlü Ratling'ler var!",
                    "background": "/static/images/hive_ratling_snipers.jpg",
                    "choices": [
                        {"id": "train_with_ratlings", "text": "Ratling'lerle Eğitim Al", "effect": "ally:hive_ratlings, gain_xp:4", "next_scene": "hive_psyker_circle"},
                        {"id": "learn_sniper_skills", "text": "Keskin Nişancı Becerilerini Öğren", "effect": "buff:sniper_skills", "next_scene": "hive_psyker_circle"},
                        {"id": "fight_ratling", "text": "Ratling ile Savaş", "combat": True, "enemy": "Hive Ratling", "next_scene": "hive_psyker_circle"},
                        {"id": "study_ratling_lore", "text": "Ratling Lore'unu Öğren", "effect": "item:ratling_lore", "next_scene": "hive_psyker_circle"}
                    ]
                },
                {
                    "id": "hive_psyker_circle",
                    "title": "Hive Psiker Çemberi",
                    "description": "Hive'ın psiker çemberine ulaştın. Burada güçlü psikerler var!",
                    "background": "/static/images/hive_psyker_circle.jpg",
                    "choices": [
                        {"id": "join_psyker_circle", "text": "Psiker Çemberine Katıl", "effect": "ally:hive_psykers, gain_xp:5", "next_scene": "hive_tech_priest_forge"},
                        {"id": "learn_psychic_powers", "text": "Psi Güçlerini Öğren", "effect": "buff:psychic_powers", "next_scene": "hive_tech_priest_forge"},
                        {"id": "fight_psyker", "text": "Psiker ile Savaş", "combat": True, "enemy": "Hive Psyker", "next_scene": "hive_tech_priest_forge"},
                        {"id": "study_warp_lore", "text": "Warp Lore'unu Öğren", "effect": "item:warp_lore", "next_scene": "hive_tech_priest_forge"}
                    ]
                },
                {
                    "id": "hive_tech_priest_forge",
                    "title": "Hive Tek Rahip Forge'u",
                    "description": "Hive'ın tek rahip forge'una ulaştın. Burada güçlü teknoloji var!",
                    "background": "/static/images/hive_tech_priest_forge.jpg",
                    "choices": [
                        {"id": "join_tech_priest", "text": "Tek Rahibe Katıl", "effect": "ally:hive_tech_priests, gain_xp:5", "next_scene": "hive_adeptus_arbites"},
                        {"id": "learn_tech_lore", "text": "Tek Lore'unu Öğren", "effect": "buff:tech_lore", "next_scene": "hive_adeptus_arbites"},
                        {"id": "fight_tech_priest", "text": "Tek Rahip ile Savaş", "combat": True, "enemy": "Hive Tech Priest", "next_scene": "hive_adeptus_arbites"},
                        {"id": "study_machine_spirit", "text": "Makine Ruhunu İncele", "effect": "item:machine_spirit_lore", "next_scene": "hive_adeptus_arbites"}
                    ]
                },
                {
                    "id": "hive_adeptus_arbites",
                    "title": "Hive Adeptus Arbites",
                    "description": "Hive'ın Adeptus Arbites ofisine ulaştın. Burada güçlü yargıçlar var!",
                    "background": "/static/images/hive_adeptus_arbites.jpg",
                    "choices": [
                        {"id": "join_arbites", "text": "Arbites'e Katıl", "effect": "ally:hive_arbites, gain_xp:4", "next_scene": "hive_inquisition_chamber"},
                        {"id": "learn_law", "text": "İmparatorluk Yasasını Öğren", "effect": "buff:law_power", "next_scene": "hive_inquisition_chamber"},
                        {"id": "fight_arbites", "text": "Arbites ile Savaş", "combat": True, "enemy": "Hive Arbites", "next_scene": "hive_inquisition_chamber"},
                        {"id": "study_law_lore", "text": "Yasa Lore'unu Öğren", "effect": "item:law_lore", "next_scene": "hive_inquisition_chamber"}
                    ]
                },
                {
                    "id": "hive_inquisition_chamber",
                    "title": "Hive Engizisyon Odası",
                    "description": "Hive'ın engizisyon odasına ulaştın. Burada güçlü engizisyoncular var!",
                    "background": "/static/images/hive_inquisition_chamber.jpg",
                    "choices": [
                        {"id": "join_inquisition", "text": "Engizisyona Katıl", "effect": "ally:hive_inquisition, gain_xp:6", "next_scene": "hive_assassin_temple"},
                        {"id": "learn_inquisition_lore", "text": "Engizisyon Lore'unu Öğren", "effect": "buff:inquisition_power", "next_scene": "hive_assassin_temple"},
                        {"id": "fight_inquisitor", "text": "Engizisyoncu ile Savaş", "combat": True, "enemy": "Hive Inquisitor", "next_scene": "hive_assassin_temple"},
                        {"id": "study_heresy_lore", "text": "Sapkınlık Lore'unu Öğren", "effect": "item:heresy_lore", "next_scene": "hive_assassin_temple"}
                    ]
                },
                {
                    "id": "hive_assassin_temple",
                    "title": "Hive Suikastçı Tapınağı",
                    "description": "Hive'ın suikastçı tapınağına ulaştın. Burada güçlü suikastçılar var!",
                    "background": "/static/images/hive_assassin_temple.jpg",
                    "choices": [
                        {"id": "join_assassins", "text": "Suikastçılara Katıl", "effect": "ally:hive_assassins, gain_xp:6", "next_scene": "hive_ork_warboss_final"},
                        {"id": "learn_assassin_skills", "text": "Suikastçı Becerilerini Öğren", "effect": "buff:assassin_skills", "next_scene": "hive_ork_warboss_final"},
                        {"id": "fight_assassin", "text": "Suikastçı ile Savaş", "combat": True, "enemy": "Hive Assassin", "next_scene": "hive_ork_warboss_final"},
                        {"id": "study_assassin_lore", "text": "Suikastçı Lore'unu Öğren", "effect": "item:assassin_lore", "next_scene": "hive_ork_warboss_final"}
                    ]
                },
                {
                    "id": "hive_ork_warboss_final",
                    "title": "Hive Ork Warboss Final Savaşı",
                    "description": "Ork Warboss Gorgutz ile son savaş! Bu sıra tabanlı kombat senin için!",
                    "background": "/static/images/hive_ork_warboss_final.jpg",
                    "choices": [
                        {"id": "fight_warboss", "text": "Warboss ile Savaş", "combat": True, "enemy": "Ork Warboss Gorgutz", "next_scene": "victory"},
                        {"id": "use_hive_tactics", "text": "Hive Taktiklerini Kullan", "effect": "buff:hive_power", "combat": True, "enemy": "Ork Warboss Gorgutz", "next_scene": "victory"},
                        {"id": "call_hive_allies", "text": "Hive Müttefiklerini Çağır", "effect": "ally:hive_allies", "combat": True, "enemy": "Ork Warboss Gorgutz", "next_scene": "victory"},
                        {"id": "negotiate_warboss", "text": "Warboss ile Müzakere", "effect": "karma:+15", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "hive_underground_tunnels",
                    "title": "Hive Yeraltı Tünelleri",
                    "description": "Hive'ın yeraltı tünellerini keşfettin. Burada gizli geçitler var!",
                    "background": "/static/images/hive_underground_tunnels.jpg",
                    "choices": [
                        {"id": "explore_underground", "text": "Yeraltını Keşfet", "effect": "item:underground_map, gain_xp:3", "next_scene": "hive_ork_saboteurs"},
                        {"id": "fight_underground_orks", "text": "Yeraltı Orklarıyla Savaş", "combat": True, "enemy": "Underground Orks", "next_scene": "hive_ork_saboteurs"},
                        {"id": "find_secret_passage", "text": "Gizli Geçit Bul", "effect": "buff:secret_passage", "next_scene": "hive_ork_saboteurs"},
                        {"id": "call_underground_help", "text": "Yeraltı Yardımı Çağır", "effect": "ally:underground_help", "next_scene": "hive_ork_saboteurs"}
                    ]
                },
                {
                    "id": "hive_ork_saboteurs",
                    "title": "Ork Sabotajcıları",
                    "description": "Ork sabotajcılarıyla karşılaştın. Bu tehlikeli Ork'lar!",
                    "background": "/static/images/hive_ork_saboteurs.jpg",
                    "choices": [
                        {"id": "fight_ork_saboteurs", "text": "Ork Sabotajcılarıyla Savaş", "combat": True, "enemy": "Ork Saboteurs", "next_scene": "hive_reactor"},
                        {"id": "interrogate_saboteur", "text": "Sabotajcıyı Sorgula", "effect": "item:saboteur_intel, gain_xp:3", "next_scene": "hive_reactor"},
                        {"id": "disable_sabotage", "text": "Sabotajı Engelle", "effect": "buff:sabotage_prevention", "next_scene": "hive_reactor"},
                        {"id": "track_saboteurs", "text": "Sabotajcıları Takip Et", "effect": "item:saboteur_trail", "next_scene": "hive_reactor"}
                    ]
                },
                {
                    "id": "hive_reactor",
                    "title": "Hive Reaktörü",
                    "description": "Hive'ın reaktörüne ulaştın. Bu kritik tesis tehlikede!",
                    "background": "/static/images/hive_reactor.jpg",
                    "choices": [
                        {"id": "secure_reactor", "text": "Reaktörü Güvenli Hale Getir", "effect": "buff:reactor_secure, gain_xp:4", "next_scene": "hive_ork_elite_guard"},
                        {"id": "fight_reactor_orks", "text": "Reaktör Orklarıyla Savaş", "combat": True, "enemy": "Reactor Orks", "next_scene": "hive_ork_elite_guard"},
                        {"id": "repair_reactor", "text": "Reaktörü Tamir Et", "effect": "buff:reactor_repair", "next_scene": "hive_ork_elite_guard"},
                        {"id": "call_tech_priest", "text": "Tek Rahibi Çağır", "effect": "ally:tech_priest", "next_scene": "hive_ork_elite_guard"}
                    ]
                },
                {
                    "id": "hive_ork_elite_guard",
                    "title": "Ork Elit Muhafızları",
                    "description": "Ork Elit Muhafızlarıyla karşılaştın. Bu güçlü Ork savaşçıları!",
                    "background": "/static/images/hive_ork_elite_guard.jpg",
                    "choices": [
                        {"id": "fight_ork_elite", "text": "Ork Elit Muhafızlarıyla Savaş", "combat": True, "enemy": "Ork Elite Guard", "next_scene": "hive_command_center"},
                        {"id": "use_tactical_advantage", "text": "Taktik Avantaj Kullan", "effect": "buff:tactical_advantage", "combat": True, "enemy": "Ork Elite Guard", "next_scene": "hive_command_center"},
                        {"id": "call_special_forces", "text": "Özel Kuvvetleri Çağır", "effect": "buff:special_forces", "next_scene": "hive_command_center"},
                        {"id": "use_psychic_powers", "text": "Psi Gücü Kullan", "effect": "buff:psychic_boost", "combat": True, "enemy": "Ork Elite Guard", "next_scene": "hive_command_center"}
                    ]
                },
                {
                    "id": "hive_command_center",
                    "title": "Hive Komuta Merkezi",
                    "description": "Hive'ın komuta merkezine ulaştın. Bu kritik kontrol noktası!",
                    "background": "/static/images/hive_command_center.jpg",
                    "choices": [
                        {"id": "secure_command_center", "text": "Komuta Merkezini Güvenli Hale Getir", "effect": "buff:command_secure, gain_xp:4", "next_scene": "hive_warboss_preparation"},
                        {"id": "fight_command_orks", "text": "Komuta Merkezi Orklarıyla Savaş", "combat": True, "enemy": "Command Orks", "next_scene": "hive_warboss_preparation"},
                        {"id": "coordinate_defense", "text": "Savunmayı Koordine Et", "effect": "buff:defense_coordination", "next_scene": "hive_warboss_preparation"},
                        {"id": "call_commander", "text": "Komutanı Çağır", "effect": "ally:commander", "next_scene": "hive_warboss_preparation"}
                    ]
                },
                {
                    "id": "hive_warboss_preparation",
                    "title": "Warboss'a Hazırlık",
                    "description": "Warboss Gorgutz'a karşı son hazırlıkları yapıyorsun. Bu savaş senin için!",
                    "background": "/static/images/hive_warboss_preparation.jpg",
                    "choices": [
                        {"id": "final_equipment_check", "text": "Son Ekipman Kontrolü", "effect": "buff:final_preparation, gain_xp:6", "next_scene": "hive_warboss_final"},
                        {"id": "final_strategy_meeting", "text": "Son Strateji Toplantısı", "effect": "buff:strategy_bonus", "next_scene": "hive_warboss_final"},
                        {"id": "final_blessing", "text": "Son Kutsama", "effect": "buff:final_blessing", "next_scene": "hive_warboss_final"},
                        {"id": "final_ritual", "text": "Son Ritüel", "effect": "buff:final_ritual_power", "next_scene": "hive_warboss_final"}
                    ]
                },
                {
                    "id": "hive_warboss_final",
                    "title": "Hive Warboss Final Savaşı",
                    "description": "Warboss Gorgutz ile son savaş! Bu sıra tabanlı kombat senin için!",
                    "background": "/static/images/hive_warboss_final.jpg",
                    "choices": [
                        {"id": "fight_warboss", "text": "Warboss ile Savaş", "combat": True, "enemy": "Warboss Gorgutz", "next_scene": "victory"},
                        {"id": "use_hive_tactics", "text": "Hive Taktiklerini Kullan", "effect": "buff:hive_power", "combat": True, "enemy": "Warboss Gorgutz", "next_scene": "victory"},
                        {"id": "call_hive_allies", "text": "Hive Müttefiklerini Çağır", "effect": "ally:hive_allies", "combat": True, "enemy": "Warboss Gorgutz", "next_scene": "victory"},
                        {"id": "negotiate_warboss", "text": "Warboss ile Müzakere", "effect": "karma:+15", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "side_mission_civilians",
                    "title": "Yan Görev: Sivilleri Kurtar",
                    "description": "Hive'da mahsur kalan sivilleri kurtar!",
                    "background": "/static/images/side_mission_civilians.jpg",
                    "choices": [
                        {"id": "rescue_civilians", "text": "Sivilleri Kurtar", "effect": "ally:rescued_civilians, gain_xp:4", "next_scene": "side_mission_medical"},
                        {"id": "escort_civilians", "text": "Sivilleri Escort Et", "effect": "buff:escort_bonus", "next_scene": "side_mission_medical"},
                        {"id": "fight_civilian_threats", "text": "Sivil Tehditleriyle Savaş", "combat": True, "enemy": "Civilian Threats", "next_scene": "side_mission_medical"},
                        {"id": "negotiate_civilians", "text": "Sivillerle Müzakere", "effect": "karma:+5", "next_scene": "side_mission_medical"}
                    ]
                },
                {
                    "id": "side_mission_medical",
                    "title": "Yan Görev: Tıbbi Merkez",
                    "description": "Hive'ın tıbbi merkezine yardım et!",
                    "background": "/static/images/side_mission_medical.jpg",
                    "choices": [
                        {"id": "help_medical_staff", "text": "Tıbbi Personele Yardım Et", "effect": "ally:medical_staff, gain_xp:4", "next_scene": "side_mission_armory"},
                        {"id": "learn_medical_skills", "text": "Tıbbi Becerileri Öğren", "effect": "buff:medical_skills", "next_scene": "side_mission_armory"},
                        {"id": "fight_medical_threats", "text": "Tıbbi Tehditleriyle Savaş", "combat": True, "enemy": "Medical Threats", "next_scene": "side_mission_armory"},
                        {"id": "negotiate_medical", "text": "Tıbbi Personelle Müzakere", "effect": "karma:+5", "next_scene": "side_mission_armory"}
                    ]
                },
                {
                    "id": "side_mission_armory",
                    "title": "Yan Görev: Cephanelik",
                    "description": "Hive'ın cephaneliğine yardım et!",
                    "background": "/static/images/side_mission_armory.jpg",
                    "choices": [
                        {"id": "help_armory_staff", "text": "Cephanelik Personeline Yardım Et", "effect": "ally:armory_staff, gain_xp:4", "next_scene": "side_mission_communications"},
                        {"id": "learn_weapon_skills", "text": "Silah Becerilerini Öğren", "effect": "buff:weapon_skills", "next_scene": "side_mission_communications"},
                        {"id": "fight_armory_threats", "text": "Cephanelik Tehditleriyle Savaş", "combat": True, "enemy": "Armory Threats", "next_scene": "side_mission_communications"},
                        {"id": "negotiate_armory", "text": "Cephanelik Personelle Müzakere", "effect": "karma:+5", "next_scene": "side_mission_communications"}
                    ]
                },
                {
                    "id": "side_mission_communications",
                    "title": "Yan Görev: İletişim Merkezi",
                    "description": "Hive'ın iletişim merkezine yardım et!",
                    "background": "/static/images/side_mission_communications.jpg",
                    "choices": [
                        {"id": "help_comm_staff", "text": "İletişim Personeline Yardım Et", "effect": "ally:comm_staff, gain_xp:4", "next_scene": "side_mission_final"},
                        {"id": "learn_comm_skills", "text": "İletişim Becerilerini Öğren", "effect": "buff:comm_skills", "next_scene": "side_mission_final"},
                        {"id": "fight_comm_threats", "text": "İletişim Tehditleriyle Savaş", "combat": True, "enemy": "Comm Threats", "next_scene": "side_mission_final"},
                        {"id": "negotiate_comm", "text": "İletişim Personelle Müzakere", "effect": "karma:+5", "next_scene": "side_mission_final"}
                    ]
                },
                {
                    "id": "side_mission_final",
                    "title": "Yan Görev: Son Direniş",
                    "description": "Yan görevlerin son direnişi! Bu sıra tabanlı kombat senin için!",
                    "background": "/static/images/side_mission_final.jpg",
                    "choices": [
                        {"id": "fight_side_mission_boss", "text": "Yan Görev Boss'u ile Savaş", "combat": True, "enemy": "Side Mission Boss", "next_scene": "victory"},
                        {"id": "use_side_tactics", "text": "Yan Görev Taktiklerini Kullan", "effect": "buff:side_power", "combat": True, "enemy": "Side Mission Boss", "next_scene": "victory"},
                        {"id": "call_side_allies", "text": "Yan Görev Müttefiklerini Çağır", "effect": "ally:side_allies", "combat": True, "enemy": "Side Mission Boss", "next_scene": "victory"},
                        {"id": "negotiate_side_boss", "text": "Yan Görev Boss'u ile Müzakere", "effect": "karma:+10", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "betrayal_scene",
                    "title": "Hive İhaneti",
                    "description": "Hive'da bir ihanet ortaya çıktı! Seni arkadan vuran bir müttefik var!",
                    "background": "/static/images/betrayal_scene.jpg",
                    "choices": [
                        {"id": "fight_traitor", "text": "Hainle Savaş", "combat": True, "enemy": "Traitor", "next_scene": "victory"},
                        {"id": "expose_traitor", "text": "Haini Açığa Çıkar", "effect": "buff:expose_bonus", "next_scene": "victory"},
                        {"id": "forgive_traitor", "text": "Haini Affet", "effect": "karma:+10", "next_scene": "victory"},
                        {"id": "use_psychic_truth", "text": "Psi Gücüyle Gerçeği Bul", "effect": "buff:truth_reveal", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "victory",
                    "title": "Zafer",
                    "description": "Orkları püskürttün! Warboss Gorgutz'u öldürdün! Hive şehri kurtuldu. Sen bir kahraman oldun. Komutan Voss seni ödüllendiriyor ve terfi ettiriyor.",
                    "background": "/static/images/hive_victory.jpg",
                    "choices": []
                },
                {
                    "id": "regroup",
                    "title": "Yeniden Toplanma",
                    "description": "Taktik geri çekilme sonrası güçlerini topladın. Yeni bir plan yapman gerekiyor. Warboss Gorgutz hala tehdit oluşturuyor.",
                    "background": "/static/images/hive_command_center.jpg",
                    "choices": [
                        {"id": "plan_ambush", "text": "Pusu Planla", "effect": "buff:ambush_bonus", "next_scene": "warboss_confrontation"},
                        {"id": "call_reinforcements", "text": "Takviye Çağır", "effect": "ally:space_marines", "next_scene": "warboss_confrontation"},
                        {"id": "direct_assault", "text": "Doğrudan Saldır", "combat": True, "enemy": "Ork Elite", "next_scene": "warboss_confrontation"}
                    ]
                },
                {
                    "id": "warboss_confrontation",
                    "title": "Warboss ile Yüzleşme",
                    "description": "Warboss Gorgutz karşında! Bu savaş senin için!",
                    "background": "/static/images/hive_battle.jpg",
                    "choices": [
                        {"id": "fight_warboss", "text": "Warboss ile Savaş", "combat": True, "enemy": "Warboss Gorgutz", "next_scene": "victory"},
                        {"id": "use_psychic", "text": "Psi Gücü Kullan", "effect": "buff:psychic_boost", "combat": True, "enemy": "Warboss Gorgutz", "next_scene": "victory"},
                        {"id": "tactical_retreat", "text": "Taktik Geri Çekilme", "next_scene": "regroup"}
                    ]
                }
            ]
        }
        
        # Kampanyaları ekle
        self.campaigns["dragon_lords"] = dragon_campaign
        self.campaigns["warhammer_40k"] = warhammer_campaign
        self.campaigns["cyberpunk_2077"] = cyberpunk_campaign
        # Büyülü Ormanın Gizemleri kampanyası ekle
        forest_mystery_campaign = {
            "id": "forest_mystery",
            "name": "🌲 Büyülü Ormanın Gizemleri",
            "type": "fantasy",
            "description": "Büyülü bir ormanda kaybolmuş bir köy var. Köylüler kaybolmuş ve ağaçlar konuşuyor. Bu gizemi çözebilir misin? Plot twist'ler, ihanetler ve rastgele olaylar seni bekliyor.",
            "scenes": [
                {
                    "id": "intro",
                    "title": "Kayıp Köy",
                    "description": "Büyülü ormanın derinliklerinde kayıp bir köy buldun. Köylüler kaybolmuş ve ağaçlar konuşuyor. Bu gizemi çözmen gerekiyor.",
                    "background": "/static/images/fantasy_forest.jpg",
                    "choices": [
                        {"id": "explore_village", "text": "Köyü Keşfet", "next_scene": "village_investigation"},
                        {"id": "talk_to_trees", "text": "Ağaçlarla Konuş", "effect": "gain_xp:2", "next_scene": "village_investigation"},
                        {"id": "find_guide", "text": "Rehber Ara", "effect": "ally:forest_guide", "next_scene": "village_investigation"},
                        {"id": "pray_nature", "text": "Doğaya Dua Et", "effect": "buff:nature_blessing", "next_scene": "village_investigation"}
                    ]
                },
                {
                    "id": "village_investigation",
                    "title": "Köy Araştırması",
                    "description": "Köyde araştırma yapıyorsun. Günlükler ve izler köylülerin ağaçlara dönüştüğünü gösteriyor. Bu lanet nasıl kaldırılır?",
                    "background": "/static/images/fantasy_village.jpg",
                    "choices": [
                        {"id": "read_diary", "text": "Günlüğü Oku", "effect": "item:ancient_diary, gain_xp:3", "next_scene": "guide_encounter"},
                        {"id": "examine_trees", "text": "Ağaçları İncele", "effect": "gain_xp:2", "next_scene": "guide_encounter"},
                        {"id": "search_ruins", "text": "Harabeleri Ara", "effect": "item:ancient_staff", "next_scene": "guide_encounter"},
                        {"id": "call_spirits", "text": "Ruhları Çağır", "effect": "buff:spirit_communication", "next_scene": "guide_encounter"}
                    ]
                },
                {
                    "id": "guide_encounter",
                    "title": "Rehber Karşılaşması",
                    "description": "Ormanın rehberi seni buldu. Köylüleri kurtarmak için antik ritüeli yapman gerekiyor. Ama rehber güvenilir mi?",
                    "background": "/static/images/fantasy_ancient_tree.jpg",
                    "choices": [
                        {"id": "trust_guide", "text": "Rehbere Güven", "next_scene": "ritual_preparation"},
                        {"id": "question_guide", "text": "Rehberi Sorgula", "effect": "gain_xp:2", "next_scene": "ritual_preparation"},
                        {"id": "follow_guide", "text": "Rehberi Takip Et", "effect": "ally:forest_guide", "next_scene": "ritual_preparation"},
                        {"id": "investigate_guide", "text": "Rehberi Araştır", "effect": "item:guide_secret", "next_scene": "ritual_preparation"}
                    ]
                },
                {
                    "id": "ritual_preparation",
                    "title": "Ritüel Hazırlığı",
                    "description": "Antik ritüeli yapmak için hazırlanıyorsun. Köylüleri kurtarmak için doğanın gücünü kullanman gerekiyor.",
                    "background": "/static/images/fantasy_ancient_tree.jpg",
                    "choices": [
                        {"id": "prepare_ritual", "text": "Ritüeli Hazırla", "effect": "buff:ritual_power", "next_scene": "guide_betrayal"},
                        {"id": "gather_ingredients", "text": "Malzemeleri Topla", "effect": "item:ritual_ingredients", "next_scene": "guide_betrayal"},
                        {"id": "study_ancient_texts", "text": "Antik Metinleri Oku", "effect": "gain_xp:3", "next_scene": "guide_betrayal"},
                        {"id": "meditate_nature", "text": "Doğayla Meditasyon", "effect": "buff:nature_connection", "next_scene": "guide_betrayal"}
                    ]
                },
                {
                    "id": "guide_betrayal",
                    "title": "Rehberin İhaneti",
                    "description": "Rehber aslında orman tanrısının düşmanıydı! Seni tuzağa düşürmek istiyor. Bu savaş senin için!",
                    "background": "/static/images/fantasy_spirit.jpg",
                    "choices": [
                        {"id": "fight_guide", "text": "Rehberle Savaş", "combat": True, "enemy": "Evil Guide", "next_scene": "forest_spirit"},
                        {"id": "use_ancient_staff", "text": "Antik Asayı Kullan", "effect": "buff:ancient_power", "combat": True, "enemy": "Evil Guide", "next_scene": "forest_spirit"},
                        {"id": "call_nature", "text": "Doğayı Çağır", "effect": "ally:forest_spirits", "combat": True, "enemy": "Evil Guide", "next_scene": "forest_spirit"},
                        {"id": "escape_betrayal", "text": "Kaç", "next_scene": "forest_spirit"}
                    ]
                },
                {
                    "id": "forest_spirit",
                    "title": "Orman Ruhu",
                    "description": "Orman tanrısı seni çağırıyor. Köylüleri kurtarmak için onunla anlaşman gerekiyor.",
                    "background": "/static/images/fantasy_spirit.jpg",
                    "choices": [
                        {"id": "negotiate_spirit", "text": "Ruhla Müzakere Et", "effect": "karma:+5", "next_scene": "final_ritual"},
                        {"id": "offer_sacrifice", "text": "Fedakarlık Öner", "effect": "buff:sacrifice_power", "next_scene": "final_ritual"},
                        {"id": "challenge_spirit", "text": "Ruhu Meydan Oku", "combat": True, "enemy": "Forest Spirit", "next_scene": "final_ritual"},
                        {"id": "plead_mercy", "text": "Merhamet Dile", "effect": "karma:+3", "next_scene": "final_ritual"}
                    ]
                },
                {
                    "id": "final_ritual",
                    "title": "Son Ritüel",
                    "description": "Köylüleri kurtarmak için son ritüeli yapıyorsun. Doğanın gücü seninle!",
                    "background": "/static/images/fantasy_battle.jpg",
                    "choices": [
                        {"id": "perform_ritual", "text": "Ritüeli Yap", "effect": "buff:ritual_success", "next_scene": "victory"},
                        {"id": "sacrifice_power", "text": "Gücünü Feda Et", "effect": "karma:+10", "next_scene": "victory"},
                        {"id": "use_ancient_staff", "text": "Antik Asayı Kullan", "effect": "item:ancient_staff", "next_scene": "victory"},
                        {"id": "call_all_spirits", "text": "Tüm Ruhları Çağır", "effect": "ally:all_spirits", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "forest_ancient_tree",
                    "title": "Antik Ağaç",
                    "description": "Ormanın en eski ağacına ulaştın. Bu ağaç ormanın tüm sırlarını biliyor!",
                    "background": "/static/images/ancient_tree.jpg",
                    "choices": [
                        {"id": "communicate_tree", "text": "Ağaçla İletişim Kur", "effect": "item:ancient_wisdom, gain_xp:4", "next_scene": "forest_spirit_boss"},
                        {"id": "meditate_tree", "text": "Ağaçta Meditasyon", "effect": "buff:nature_blessing", "next_scene": "forest_spirit_boss"},
                        {"id": "study_tree", "text": "Ağacı İncele", "effect": "item:tree_knowledge", "next_scene": "forest_spirit_boss"},
                        {"id": "pray_tree", "text": "Ağaca Dua Et", "effect": "buff:divine_connection", "next_scene": "forest_spirit_boss"}
                    ]
                },
                {
                    "id": "forest_spirit_boss",
                    "title": "Orman Ruhu Boss Savaşı",
                    "description": "Ormanın en güçlü ruhu karşında! Bu sıra tabanlı kombat senin için!",
                    "background": "/static/images/forest_spirit_boss.jpg",
                    "choices": [
                        {"id": "fight_forest_spirit", "text": "Orman Ruhuyla Savaş", "combat": True, "enemy": "Ancient Forest Spirit", "next_scene": "forest_ritual"},
                        {"id": "use_nature_magic", "text": "Doğa Sihrini Kullan", "effect": "buff:nature_power", "combat": True, "enemy": "Ancient Forest Spirit", "next_scene": "forest_ritual"},
                        {"id": "negotiate_spirit", "text": "Ruhla Müzakere Et", "effect": "karma:+10", "next_scene": "forest_ritual"},
                        {"id": "call_forest_allies", "text": "Orman Müttefiklerini Çağır", "effect": "ally:forest_creatures", "next_scene": "forest_ritual"}
                    ]
                },
                {
                    "id": "forest_ritual",
                    "title": "Orman Ritüeli",
                    "description": "Ormanın eski ritüelini gerçekleştirmek için hazırlanıyorsun. Bu ritüel ormanı kurtaracak!",
                    "background": "/static/images/forest_ritual.jpg",
                    "choices": [
                        {"id": "prepare_ritual", "text": "Ritüeli Hazırla", "effect": "buff:ritual_preparation", "next_scene": "final_ritual"},
                        {"id": "gather_ingredients", "text": "Malzemeleri Topla", "effect": "item:ritual_ingredients", "next_scene": "final_ritual"},
                        {"id": "study_ritual", "text": "Ritüeli Araştır", "effect": "gain_xp:3", "next_scene": "final_ritual"},
                        {"id": "call_ritual_helpers", "text": "Ritüel Yardımcılarını Çağır", "effect": "ally:ritual_helpers", "next_scene": "final_ritual"}
                    ]
                },
                {
                    "id": "side_mission_lost_villagers",
                    "title": "Yan Görev: Kayıp Köylüler",
                    "description": "Ormanın derinliklerinde kayıp köylüler var. Onları bulmak için yan görev!",
                    "background": "/static/images/lost_villagers.jpg",
                    "choices": [
                        {"id": "search_villagers", "text": "Köylüleri Ara", "effect": "ally:rescued_villagers, gain_xp:3", "next_scene": "side_mission_forest_creatures"},
                        {"id": "track_villagers", "text": "Köylülerin İzini Sür", "effect": "item:tracking_skills", "next_scene": "side_mission_forest_creatures"},
                        {"id": "ask_forest_help", "text": "Ormanın Yardımını İste", "effect": "buff:forest_guidance", "next_scene": "side_mission_forest_creatures"},
                        {"id": "fight_forest_threats", "text": "Orman Tehditleriyle Savaş", "combat": True, "enemy": "Forest Threats", "next_scene": "side_mission_forest_creatures"}
                    ]
                },
                {
                    "id": "side_mission_forest_creatures",
                    "title": "Yan Görev: Orman Yaratıkları",
                    "description": "Ormanın gizli yaratıkları ile karşılaştın. Bu yaratıklar ormanın koruyucuları!",
                    "background": "/static/images/forest_creatures.jpg",
                    "choices": [
                        {"id": "befriend_creatures", "text": "Yaratıklarla Arkadaş Ol", "effect": "ally:forest_creatures, gain_xp:4", "next_scene": "side_mission_ancient_ruins"},
                        {"id": "study_creatures", "text": "Yaratıkları İncele", "effect": "item:creature_knowledge", "next_scene": "side_mission_ancient_ruins"},
                        {"id": "fight_creatures", "text": "Yaratıklarla Savaş", "combat": True, "enemy": "Forest Creatures", "next_scene": "side_mission_ancient_ruins"},
                        {"id": "negotiate_creatures", "text": "Yaratıklarla Müzakere", "effect": "karma:+5", "next_scene": "side_mission_ancient_ruins"}
                    ]
                },
                {
                    "id": "side_mission_ancient_ruins",
                    "title": "Yan Görev: Antik Harabeler",
                    "description": "Ormanın derinliklerinde antik harabeler keşfettin. Burada eski sırlar var!",
                    "background": "/static/images/ancient_ruins.jpg",
                    "choices": [
                        {"id": "explore_ruins", "text": "Harabeleri Keşfet", "effect": "item:ancient_artifacts, gain_xp:4", "next_scene": "side_mission_mystical_pool"},
                        {"id": "study_ruins", "text": "Harabeleri İncele", "effect": "item:ruin_knowledge", "next_scene": "side_mission_mystical_pool"},
                        {"id": "fight_ruin_guardians", "text": "Hariye Muhafızlarıyla Savaş", "combat": True, "enemy": "Ruin Guardians", "next_scene": "side_mission_mystical_pool"},
                        {"id": "hack_ruin_systems", "text": "Hariye Sistemlerini Hack Et", "effect": "buff:ruin_control", "next_scene": "side_mission_mystical_pool"}
                    ]
                },
                {
                    "id": "side_mission_mystical_pool",
                    "title": "Yan Görev: Mistik Havuz",
                    "description": "Ormanın mistik havuzuna ulaştın. Bu havuz şifa verici güçlere sahip!",
                    "background": "/static/images/mystical_pool.jpg",
                    "choices": [
                        {"id": "drink_pool_water", "text": "Havuz Suyundan İç", "effect": "buff:healing_power", "next_scene": "side_mission_final"},
                        {"id": "study_pool", "text": "Havuzu İncele", "effect": "item:pool_knowledge", "next_scene": "side_mission_final"},
                        {"id": "fight_pool_guardian", "text": "Havuz Muhafızıyla Savaş", "combat": True, "enemy": "Pool Guardian", "next_scene": "side_mission_final"},
                        {"id": "bless_pool", "text": "Havuzu Kutsa", "effect": "karma:+10", "next_scene": "side_mission_final"}
                    ]
                },
                {
                    "id": "side_mission_final",
                    "title": "Yan Görev: Son Gizem",
                    "description": "Ormanın son gizemini çözmek için buradayısın. Bu gizem ormanın kaderini belirleyecek!",
                    "background": "/static/images/final_mystery.jpg",
                    "choices": [
                        {"id": "solve_mystery", "text": "Gizemi Çöz", "effect": "item:mystery_solution, gain_xp:5", "next_scene": "victory"},
                        {"id": "study_mystery", "text": "Gizemi Araştır", "effect": "buff:mystery_knowledge", "next_scene": "victory"},
                        {"id": "fight_mystery_guardian", "text": "Gizem Muhafızıyla Savaş", "combat": True, "enemy": "Mystery Guardian", "next_scene": "victory"},
                        {"id": "call_mystery_help", "text": "Gizem Yardımını Çağır", "effect": "ally:mystery_helpers", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "forest_ancient_ruins",
                    "title": "Antik Orman Harabeleri",
                    "description": "Ormanın derinliklerinde antik harabeler keşfettin. Burada eski sırlar var!",
                    "background": "/static/images/forest_ancient_ruins.jpg",
                    "choices": [
                        {"id": "explore_ruins", "text": "Harabeleri Keşfet", "effect": "item:ancient_artifacts, gain_xp:4", "next_scene": "forest_mystical_pool"},
                        {"id": "study_ruins", "text": "Harabeleri İncele", "effect": "item:ruin_knowledge", "next_scene": "forest_mystical_pool"},
                        {"id": "fight_ruin_guardians", "text": "Hariye Muhafızlarıyla Savaş", "combat": True, "enemy": "Ruin Guardians", "next_scene": "forest_mystical_pool"},
                        {"id": "meditate_ruins", "text": "Harabelerde Meditasyon", "effect": "buff:ancient_wisdom", "next_scene": "forest_mystical_pool"}
                    ]
                },
                {
                    "id": "forest_mystical_pool",
                    "title": "Mistik Orman Havuzu",
                    "description": "Ormanın mistik havuzuna ulaştın. Bu havuz şifa verici güçlere sahip!",
                    "background": "/static/images/forest_mystical_pool.jpg",
                    "choices": [
                        {"id": "drink_pool_water", "text": "Havuz Suyundan İç", "effect": "buff:healing_power", "next_scene": "forest_sacred_grove"},
                        {"id": "study_pool", "text": "Havuzu İncele", "effect": "item:pool_knowledge", "next_scene": "forest_sacred_grove"},
                        {"id": "fight_pool_guardian", "text": "Havuz Muhafızıyla Savaş", "combat": True, "enemy": "Pool Guardian", "next_scene": "forest_sacred_grove"},
                        {"id": "bless_pool", "text": "Havuzu Kutsa", "effect": "karma:+10", "next_scene": "forest_sacred_grove"}
                    ]
                },
                {
                    "id": "forest_sacred_grove",
                    "title": "Kutsal Orman Korusu",
                    "description": "Ormanın kutsal korusuna ulaştın. Burada eski ağaçlar ve ruhlar var!",
                    "background": "/static/images/forest_sacred_grove.jpg",
                    "choices": [
                        {"id": "pray_grove", "text": "Koruda Dua Et", "effect": "buff:divine_blessing", "next_scene": "forest_elven_city"},
                        {"id": "meditate_grove", "text": "Koruda Meditasyon", "effect": "buff:spiritual_peace", "next_scene": "forest_elven_city"},
                        {"id": "fight_grove_guardians", "text": "Koru Muhafızlarıyla Savaş", "combat": True, "enemy": "Grove Guardians", "next_scene": "forest_elven_city"},
                        {"id": "study_grove", "text": "Koruyu İncele", "effect": "item:grove_knowledge", "next_scene": "forest_elven_city"}
                    ]
                },
                {
                    "id": "forest_elven_city",
                    "title": "Elf Şehri",
                    "description": "Ormanın gizli elf şehrini keşfettin. Burada güçlü elf'ler var!",
                    "background": "/static/images/forest_elven_city.jpg",
                    "choices": [
                        {"id": "join_elves", "text": "Elf'lere Katıl", "effect": "ally:elven_warriors, gain_xp:5", "next_scene": "forest_druid_circle"},
                        {"id": "negotiate_elves", "text": "Elf'lerle Müzakere", "effect": "karma:+5", "next_scene": "forest_druid_circle"},
                        {"id": "fight_elves", "text": "Elf'lerle Savaş", "combat": True, "enemy": "Elven Warriors", "next_scene": "forest_druid_circle"},
                        {"id": "learn_elven_magic", "text": "Elf Sihrini Öğren", "effect": "buff:elven_magic", "next_scene": "forest_druid_circle"}
                    ]
                },
                {
                    "id": "forest_druid_circle",
                    "title": "Druid Çemberi",
                    "description": "Ormanın gizli druid çemberini keşfettin. Burada güçlü druid'ler var!",
                    "background": "/static/images/forest_druid_circle.jpg",
                    "choices": [
                        {"id": "join_druids", "text": "Druid'lere Katıl", "effect": "ally:druid_circle, gain_xp:5", "next_scene": "forest_fairy_kingdom"},
                        {"id": "learn_druid_magic", "text": "Druid Sihrini Öğren", "effect": "buff:druid_magic", "next_scene": "forest_fairy_kingdom"},
                        {"id": "fight_druids", "text": "Druid'lerle Savaş", "combat": True, "enemy": "Druid Circle", "next_scene": "forest_fairy_kingdom"},
                        {"id": "negotiate_druids", "text": "Druid'lerle Müzakere", "effect": "karma:+5", "next_scene": "forest_fairy_kingdom"}
                    ]
                },
                {
                    "id": "forest_fairy_kingdom",
                    "title": "Peri Krallığı",
                    "description": "Ormanın gizli peri krallığını keşfettin. Burada güçlü periler var!",
                    "background": "/static/images/forest_fairy_kingdom.jpg",
                    "choices": [
                        {"id": "join_fairies", "text": "Perilere Katıl", "effect": "ally:fairy_kingdom, gain_xp:5", "next_scene": "forest_centaur_herd"},
                        {"id": "learn_fairy_magic", "text": "Peri Sihrini Öğren", "effect": "buff:fairy_magic", "next_scene": "forest_centaur_herd"},
                        {"id": "fight_fairies", "text": "Perilerle Savaş", "combat": True, "enemy": "Fairy Kingdom", "next_scene": "forest_centaur_herd"},
                        {"id": "negotiate_fairies", "text": "Perilerle Müzakere", "effect": "karma:+5", "next_scene": "forest_centaur_herd"}
                    ]
                },
                {
                    "id": "forest_centaur_herd",
                    "title": "Kentaur Sürüsü",
                    "description": "Ormanın gizli kentaur sürüsünü keşfettin. Burada güçlü kentaur'lar var!",
                    "background": "/static/images/forest_centaur_herd.jpg",
                    "choices": [
                        {"id": "join_centaurs", "text": "Kentaur'lara Katıl", "effect": "ally:centaur_herd, gain_xp:5", "next_scene": "forest_dryad_grove"},
                        {"id": "learn_centaur_skills", "text": "Kentaur Becerilerini Öğren", "effect": "buff:centaur_skills", "next_scene": "forest_dryad_grove"},
                        {"id": "fight_centaurs", "text": "Kentaur'larla Savaş", "combat": True, "enemy": "Centaur Herd", "next_scene": "forest_dryad_grove"},
                        {"id": "negotiate_centaurs", "text": "Kentaur'larla Müzakere", "effect": "karma:+5", "next_scene": "forest_dryad_grove"}
                    ]
                },
                {
                    "id": "forest_dryad_grove",
                    "title": "Dryad Korusu",
                    "description": "Ormanın gizli dryad korusunu keşfettin. Burada güçlü dryad'lar var!",
                    "background": "/static/images/forest_dryad_grove.jpg",
                    "choices": [
                        {"id": "join_dryads", "text": "Dryad'lara Katıl", "effect": "ally:dryad_grove, gain_xp:5", "next_scene": "forest_unicorn_meadow"},
                        {"id": "learn_dryad_magic", "text": "Dryad Sihrini Öğren", "effect": "buff:dryad_magic", "next_scene": "forest_unicorn_meadow"},
                        {"id": "fight_dryads", "text": "Dryad'larla Savaş", "combat": True, "enemy": "Dryad Grove", "next_scene": "forest_unicorn_meadow"},
                        {"id": "negotiate_dryads", "text": "Dryad'larla Müzakere", "effect": "karma:+5", "next_scene": "forest_unicorn_meadow"}
                    ]
                },
                {
                    "id": "forest_unicorn_meadow",
                    "title": "Unicorn Çayırı",
                    "description": "Ormanın gizli unicorn çayırını keşfettin. Burada güçlü unicorn'lar var!",
                    "background": "/static/images/forest_unicorn_meadow.jpg",
                    "choices": [
                        {"id": "befriend_unicorns", "text": "Unicorn'larla Arkadaş Ol", "effect": "ally:unicorn_herd, gain_xp:5", "next_scene": "forest_griffin_nest"},
                        {"id": "ride_unicorn", "text": "Unicorn'a Bin", "effect": "buff:unicorn_ride", "next_scene": "forest_griffin_nest"},
                        {"id": "fight_unicorns", "text": "Unicorn'larla Savaş", "combat": True, "enemy": "Unicorn Herd", "next_scene": "forest_griffin_nest"},
                        {"id": "negotiate_unicorns", "text": "Unicorn'larla Müzakere", "effect": "karma:+5", "next_scene": "forest_griffin_nest"}
                    ]
                },
                {
                    "id": "forest_griffin_nest",
                    "title": "Griffin Yuvası",
                    "description": "Ormanın gizli griffin yuvasını keşfettin. Burada güçlü griffin'ler var!",
                    "background": "/static/images/forest_griffin_nest.jpg",
                    "choices": [
                        {"id": "befriend_griffins", "text": "Griffin'lerle Arkadaş Ol", "effect": "ally:griffin_flock, gain_xp:5", "next_scene": "forest_phoenix_roost"},
                        {"id": "ride_griffin", "text": "Griffin'e Bin", "effect": "buff:griffin_ride", "next_scene": "forest_phoenix_roost"},
                        {"id": "fight_griffins", "text": "Griffin'lerle Savaş", "combat": True, "enemy": "Griffin Flock", "next_scene": "forest_phoenix_roost"},
                        {"id": "negotiate_griffins", "text": "Griffin'lerle Müzakere", "effect": "karma:+5", "next_scene": "forest_phoenix_roost"}
                    ]
                },
                {
                    "id": "forest_phoenix_roost",
                    "title": "Phoenix Tüneği",
                    "description": "Ormanın gizli phoenix tüneğini keşfettin. Burada güçlü phoenix'ler var!",
                    "background": "/static/images/forest_phoenix_roost.jpg",
                    "choices": [
                        {"id": "befriend_phoenix", "text": "Phoenix'le Arkadaş Ol", "effect": "ally:phoenix_flock, gain_xp:6", "next_scene": "forest_dragon_lair"},
                        {"id": "ride_phoenix", "text": "Phoenix'e Bin", "effect": "buff:phoenix_ride", "next_scene": "forest_dragon_lair"},
                        {"id": "fight_phoenix", "text": "Phoenix'le Savaş", "combat": True, "enemy": "Phoenix Flock", "next_scene": "forest_dragon_lair"},
                        {"id": "negotiate_phoenix", "text": "Phoenix'le Müzakere", "effect": "karma:+10", "next_scene": "forest_dragon_lair"}
                    ]
                },
                {
                    "id": "forest_dragon_lair",
                    "title": "Orman Ejderha İni",
                    "description": "Ormanın gizli ejderha inini keşfettin. Burada güçlü ejderhalar var!",
                    "background": "/static/images/forest_dragon_lair.jpg",
                    "choices": [
                        {"id": "befriend_dragon", "text": "Ejderhayla Arkadaş Ol", "effect": "ally:forest_dragon, gain_xp:6", "next_scene": "forest_ancient_temple"},
                        {"id": "ride_dragon", "text": "Ejderhaya Bin", "effect": "buff:dragon_ride", "next_scene": "forest_ancient_temple"},
                        {"id": "fight_dragon", "text": "Ejderhayla Savaş", "combat": True, "enemy": "Forest Dragon", "next_scene": "forest_ancient_temple"},
                        {"id": "negotiate_dragon", "text": "Ejderhayla Müzakere", "effect": "karma:+10", "next_scene": "forest_ancient_temple"}
                    ]
                },
                {
                    "id": "forest_ancient_temple",
                    "title": "Antik Orman Tapınağı",
                    "description": "Ormanın gizli antik tapınağını keşfettin. Burada eski sırlar var!",
                    "background": "/static/images/forest_ancient_temple.jpg",
                    "choices": [
                        {"id": "explore_temple", "text": "Tapınağı Keşfet", "effect": "item:ancient_secrets, gain_xp:6", "next_scene": "forest_final_battle"},
                        {"id": "study_temple", "text": "Tapınağı İncele", "effect": "item:temple_knowledge", "next_scene": "forest_final_battle"},
                        {"id": "fight_temple_guardians", "text": "Tapınak Muhafızlarıyla Savaş", "combat": True, "enemy": "Temple Guardians", "next_scene": "forest_final_battle"},
                        {"id": "meditate_temple", "text": "Tapınakta Meditasyon", "effect": "buff:ancient_blessing", "next_scene": "forest_final_battle"}
                    ]
                },
                {
                    "id": "forest_final_battle",
                    "title": "Orman Son Savaş",
                    "description": "Ormanın son savaşı başladı! Bu sıra tabanlı kombat senin için!",
                    "background": "/static/images/forest_final_battle.jpg",
                    "choices": [
                        {"id": "fight_final_battle", "text": "Son Savaşta Savaş", "combat": True, "enemy": "Forest Final Boss", "next_scene": "victory"},
                        {"id": "use_nature_magic", "text": "Doğa Sihrini Kullan", "effect": "buff:nature_power", "combat": True, "enemy": "Forest Final Boss", "next_scene": "victory"},
                        {"id": "call_forest_allies", "text": "Orman Müttefiklerini Çağır", "effect": "ally:forest_allies", "combat": True, "enemy": "Forest Final Boss", "next_scene": "victory"},
                        {"id": "negotiate_final", "text": "Son Müzakere", "effect": "karma:+15", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "victory",
                    "title": "Zafer",
                    "description": "Köylüleri kurtardın ve ormanı iyileştirdin. Orman tanrısı seni koruyucu olarak seçti.",
                    "background": "/static/images/fantasy_victory.jpg",
                    "choices": []
                }
            ]
        }
        
        # Ork İstilası: Son Savunma kampanyası ekle
        ork_invasion_campaign = {
            "id": "ork_invasion_defense",
            "name": "⚔️ Ork İstilası: Son Savunma",
            "type": "warhammer40k",
            "description": "Ork Waaagh! İmparatorluk dünyasına geliyor. Space Marine olarak son savunmayı yap! Plot twist'ler, ihanetler ve rastgele olaylar seni bekliyor.",
            "scenes": [
                {
                    "id": "intro",
                    "title": "İmparatorluk Dünyası",
                    "description": "İmparatorluk dünyasında görevlendirildin. Ork Waaagh! yaklaşıyor ve sen, seçilmiş Space Marine, bu tehdidi durdurmak için buradasın.",
                    "background": "/static/images/warhammer40k_battlefield.jpg",
                    "choices": [
                        {"id": "check_equipment", "text": "Ekipmanı Kontrol Et", "effect": "item:bolter, gain_xp:3", "next_scene": "mission_briefing"},
                        {"id": "pray_emperor", "text": "İmparator'a Dua Et", "effect": "buff:faith_bonus, gain_xp:2", "next_scene": "mission_briefing"},
                        {"id": "inspect_defenses", "text": "Savunmaları İncele", "effect": "item:defense_map, gain_xp:2", "next_scene": "mission_briefing"},
                        {"id": "find_commander", "text": "Komutanı Ara", "effect": "gain_xp:1", "next_scene": "mission_briefing"}
                    ]
                },
                {
                    "id": "mission_briefing",
                    "title": "Görev Brifingi",
                    "description": "Komutan seni çağırıyor. Ork Waaagh! başladı, görev açık. Warboss Gorkamorka'nın 100,000 Ork'u dünyaya doğru ilerliyor.",
                    "background": "/static/images/warhammer40k_space_marine.jpg",
                    "choices": [
                        {"id": "accept_mission", "text": "Görevi Kabul Et", "next_scene": "defense_preparation"},
                        {"id": "ask_details", "text": "Detayları Sor", "effect": "gain_xp:2", "next_scene": "defense_preparation"},
                        {"id": "request_backup", "text": "Takviye İste", "effect": "ally:imperial_guard", "next_scene": "defense_preparation"},
                        {"id": "strategic_planning", "text": "Stratejik Planlama", "effect": "buff:tactical_advantage", "next_scene": "defense_preparation"}
                    ]
                },
                {
                    "id": "defense_preparation",
                    "title": "Savunma Hazırlığı",
                    "description": "Dünyanın savunma hatlarını hazırlıyorsun. Ork ordusu yaklaşıyor, her dakika önemli. Imperial Guard birlikleri pozisyon alıyor.",
                    "background": "/static/images/warhammer40k_battlefield.jpg",
                    "choices": [
                        {"id": "fortify_position", "text": "Pozisyonu Güçlendir", "effect": "buff:defense_bonus", "next_scene": "ork_scout_patrol"},
                        {"id": "set_traps", "text": "Tuzaklar Kur", "effect": "buff:ambush_bonus", "next_scene": "ork_scout_patrol"},
                        {"id": "coordinate_artillery", "text": "Topçuyu Koordine Et", "effect": "buff:artillery_support", "next_scene": "ork_scout_patrol"},
                        {"id": "inspire_troops", "text": "Birlikleri Motive Et", "effect": "buff:morale_boost", "next_scene": "ork_scout_patrol"}
                    ]
                },
                {
                    "id": "ork_scout_patrol",
                    "title": "Ork Keşif Devriyesi",
                    "description": "İlk Ork keşif devriyesi geldi! Küçük bir grup Ork Boyz savunma hatlarını test ediyor. Bu sadece başlangıç...",
                    "background": "/static/images/warhammer40k_ork_horde.jpg",
                    "choices": [
                        {"id": "engage_scouts", "text": "Keşif Devriyesiyle Savaş", "combat": True, "enemy": "Ork Scouts", "next_scene": "main_ork_force"},
                        {"id": "let_them_pass", "text": "Geçmelerine İzin Ver", "effect": "gain_xp:1", "next_scene": "main_ork_force"},
                        {"id": "ambush_scouts", "text": "Pusu Kur", "effect": "buff:surprise_attack", "combat": True, "enemy": "Ork Scouts", "next_scene": "main_ork_force"},
                        {"id": "interrogate_captive", "text": "Esir Al ve Sorgula", "effect": "item:intel_data, gain_xp:3", "next_scene": "main_ork_force"}
                    ]
                },
                {
                    "id": "main_ork_force",
                    "title": "Ana Ork Gücü",
                    "description": "Ana Ork ordusu geldi! Gökyüzü yeşil bulutlarla kaplandı, Warboss Gorkamorka'nın savaş çığlıkları yankılanıyor. 100,000 Ork dünyaya saldırıyor!",
                    "background": "/static/images/warhammer40k_ork_horde.jpg",
                    "choices": [
                        {"id": "hold_defense_line", "text": "Savunma Hattını Tut", "combat": True, "enemy": "Ork Horde", "next_scene": "warboss_reveal"},
                        {"id": "counter_attack", "text": "Karşı Saldırı", "combat": True, "enemy": "Ork Elite", "next_scene": "warboss_reveal"},
                        {"id": "artillery_barrage", "text": "Topçu Saldırısı", "effect": "buff:artillery_support", "next_scene": "warboss_reveal"},
                        {"id": "tactical_retreat", "text": "Taktik Geri Çekilme", "next_scene": "regroup"}
                    ]
                },
                {
                    "id": "warboss_reveal",
                    "title": "Warboss Gorkamorka'nın Görünüşü",
                    "description": "Savaşın ortasında Warboss Gorkamorka göründü! 5 metre boyunda, yeşil derili, devasa silahlarla donanmış. Bu savaş senin için!",
                    "background": "/static/images/warhammer40k_ork_horde.jpg",
                    "choices": [
                        {"id": "challenge_warboss", "text": "Warboss'u Meydan Oku", "combat": True, "enemy": "Warboss Gorkamorka", "next_scene": "victory"},
                        {"id": "use_psychic", "text": "Psi Gücü Kullan", "effect": "buff:psychic_boost", "combat": True, "enemy": "Warboss Gorkamorka", "next_scene": "victory"},
                        {"id": "call_reinforcements", "text": "Takviye Çağır", "effect": "ally:space_marines", "next_scene": "victory"},
                        {"id": "tactical_retreat", "text": "Taktik Geri Çekilme", "next_scene": "regroup"}
                    ]
                },
                {
                    "id": "imperial_bunker",
                    "title": "İmparatorluk Sığınağı",
                    "description": "Cadia'nın gizli İmparatorluk sığınağına ulaştın. Burada yaralı askerler ve mühimmat var!",
                    "background": "/static/images/imperial_bunker.jpg",
                    "choices": [
                        {"id": "help_wounded", "text": "Yaralılara Yardım Et", "effect": "ally:wounded_soldiers, gain_xp:3", "next_scene": "imperial_armory"},
                        {"id": "get_supplies", "text": "Mühimmat Al", "effect": "item:imperial_supplies", "next_scene": "imperial_armory"},
                        {"id": "fight_bunker_orks", "text": "Sığınak Orklarıyla Savaş", "combat": True, "enemy": "Bunker Orks", "next_scene": "imperial_armory"},
                        {"id": "coordinate_defense", "text": "Savunmayı Koordine Et", "effect": "buff:defense_coordination", "next_scene": "imperial_armory"}
                    ]
                },
                {
                    "id": "imperial_armory",
                    "title": "İmparatorluk Cephaneliği",
                    "description": "Cadia'nın gizli İmparatorluk cephaneliğini keşfettin. Burada güçlü silahlar var!",
                    "background": "/static/images/imperial_armory.jpg",
                    "choices": [
                        {"id": "get_heavy_weapons", "text": "Ağır Silahlar Al", "effect": "item:heavy_weapons", "next_scene": "imperial_medical"},
                        {"id": "hack_armory_systems", "text": "Cephanelik Sistemlerini Hack Et", "effect": "buff:armory_control", "next_scene": "imperial_medical"},
                        {"id": "fight_armory_orks", "text": "Cephanelik Orklarıyla Savaş", "combat": True, "enemy": "Armory Orks", "next_scene": "imperial_medical"},
                        {"id": "secure_armory", "text": "Cephaneliği Güvenli Hale Getir", "effect": "ally:armory_team", "next_scene": "imperial_medical"}
                    ]
                },
                {
                    "id": "imperial_medical",
                    "title": "İmparatorluk Tıbbi Merkezi",
                    "description": "Cadia'nın gizli İmparatorluk tıbbi merkezini keşfettin. Burada yaralı askerler var!",
                    "background": "/static/images/imperial_medical.jpg",
                    "choices": [
                        {"id": "help_medics", "text": "Doktorlara Yardım Et", "effect": "ally:medical_team, gain_xp:4", "next_scene": "imperial_communications"},
                        {"id": "get_medical_supplies", "text": "Tıbbi Malzeme Al", "effect": "item:medical_supplies", "next_scene": "imperial_communications"},
                        {"id": "fight_medical_orks", "text": "Tıbbi Merkez Orklarıyla Savaş", "combat": True, "enemy": "Medical Orks", "next_scene": "imperial_communications"},
                        {"id": "secure_medical", "text": "Tıbbi Merkezi Güvenli Hale Getir", "effect": "buff:medical_control", "next_scene": "imperial_communications"}
                    ]
                },
                {
                    "id": "imperial_communications",
                    "title": "İmparatorluk İletişim Merkezi",
                    "description": "Cadia'nın gizli İmparatorluk iletişim merkezini keşfettin. Buradan tüm sistemi koordine edebilirsin!",
                    "background": "/static/images/imperial_communications.jpg",
                    "choices": [
                        {"id": "hack_communications", "text": "İletişim Sistemlerini Hack Et", "effect": "buff:communication_control", "next_scene": "imperial_artillery"},
                        {"id": "coordinate_forces", "text": "Güçleri Koordine Et", "effect": "ally:communication_team", "next_scene": "imperial_artillery"},
                        {"id": "fight_comm_orks", "text": "İletişim Orklarıyla Savaş", "combat": True, "enemy": "Communication Orks", "next_scene": "imperial_artillery"},
                        {"id": "secure_communications", "text": "İletişimi Güvenli Hale Getir", "effect": "buff:secure_communications", "next_scene": "imperial_artillery"}
                    ]
                },
                {
                    "id": "imperial_artillery",
                    "title": "İmparatorluk Topçu Birliği",
                    "description": "Cadia'nın gizli İmparatorluk topçu birliğini keşfettin. Burada güçlü toplar var!",
                    "background": "/static/images/imperial_artillery.jpg",
                    "choices": [
                        {"id": "coordinate_artillery", "text": "Topçuyu Koordine Et", "effect": "buff:artillery_support", "next_scene": "imperial_tanks"},
                        {"id": "get_artillery_support", "text": "Topçu Desteği Al", "effect": "ally:artillery_team", "next_scene": "imperial_tanks"},
                        {"id": "fight_artillery_orks", "text": "Topçu Orklarıyla Savaş", "combat": True, "enemy": "Artillery Orks", "next_scene": "imperial_tanks"},
                        {"id": "secure_artillery", "text": "Topçuyu Güvenli Hale Getir", "effect": "buff:artillery_control", "next_scene": "imperial_tanks"}
                    ]
                },
                {
                    "id": "imperial_tanks",
                    "title": "İmparatorluk Tank Birliği",
                    "description": "Cadia'nın gizli İmparatorluk tank birliğini keşfettin. Burada güçlü tanklar var!",
                    "background": "/static/images/imperial_tanks.jpg",
                    "choices": [
                        {"id": "command_tanks", "text": "Tankları Komuta Et", "effect": "buff:tank_support", "next_scene": "imperial_air_support"},
                        {"id": "get_tank_support", "text": "Tank Desteği Al", "effect": "ally:tank_team", "next_scene": "imperial_air_support"},
                        {"id": "fight_tank_orks", "text": "Tank Orklarıyla Savaş", "combat": True, "enemy": "Tank Orks", "next_scene": "imperial_air_support"},
                        {"id": "secure_tanks", "text": "Tankları Güvenli Hale Getir", "effect": "buff:tank_control", "next_scene": "imperial_air_support"}
                    ]
                },
                {
                    "id": "imperial_air_support",
                    "title": "İmparatorluk Hava Desteği",
                    "description": "Cadia'nın gizli İmparatorluk hava desteği birliğini keşfettin. Burada güçlü uçaklar var!",
                    "background": "/static/images/imperial_air_support.jpg",
                    "choices": [
                        {"id": "coordinate_air_support", "text": "Hava Desteğini Koordine Et", "effect": "buff:air_support", "next_scene": "imperial_special_forces"},
                        {"id": "get_air_support", "text": "Hava Desteği Al", "effect": "ally:air_support_team", "next_scene": "imperial_special_forces"},
                        {"id": "fight_air_orks", "text": "Hava Orklarıyla Savaş", "combat": True, "enemy": "Air Orks", "next_scene": "imperial_special_forces"},
                        {"id": "secure_air_support", "text": "Hava Desteğini Güvenli Hale Getir", "effect": "buff:air_control", "next_scene": "imperial_special_forces"}
                    ]
                },
                {
                    "id": "imperial_special_forces",
                    "title": "İmparatorluk Özel Kuvvetler",
                    "description": "Cadia'nın gizli İmparatorluk özel kuvvetlerini keşfettin. Burada elit askerler var!",
                    "background": "/static/images/imperial_special_forces.jpg",
                    "choices": [
                        {"id": "join_special_forces", "text": "Özel Kuvvetlere Katıl", "effect": "ally:special_forces, gain_xp:5", "next_scene": "imperial_psykers"},
                        {"id": "coordinate_special_forces", "text": "Özel Kuvvetleri Koordine Et", "effect": "buff:special_forces_support", "next_scene": "imperial_psykers"},
                        {"id": "fight_special_orks", "text": "Özel Kuvvet Orklarıyla Savaş", "combat": True, "enemy": "Special Orks", "next_scene": "imperial_psykers"},
                        {"id": "secure_special_forces", "text": "Özel Kuvvetleri Güvenli Hale Getir", "effect": "buff:special_forces_control", "next_scene": "imperial_psykers"}
                    ]
                },
                {
                    "id": "imperial_psykers",
                    "title": "İmparatorluk Psikerler",
                    "description": "Cadia'nın gizli İmparatorluk psikerlerini keşfettin. Burada güçlü psikerler var!",
                    "background": "/static/images/imperial_psykers.jpg",
                    "choices": [
                        {"id": "learn_psychic_powers", "text": "Psi Güçlerini Öğren", "effect": "buff:psychic_powers, gain_xp:4", "next_scene": "imperial_tech_priests"},
                        {"id": "coordinate_psykers", "text": "Psikerleri Koordine Et", "effect": "ally:psykers_team", "next_scene": "imperial_tech_priests"},
                        {"id": "fight_psychic_orks", "text": "Psi Orklarıyla Savaş", "combat": True, "enemy": "Psychic Orks", "next_scene": "imperial_tech_priests"},
                        {"id": "secure_psykers", "text": "Psikerleri Güvenli Hale Getir", "effect": "buff:psychic_control", "next_scene": "imperial_tech_priests"}
                    ]
                },
                {
                    "id": "imperial_tech_priests",
                    "title": "İmparatorluk Tek Rahipleri",
                    "description": "Cadia'nın gizli İmparatorluk tek rahiplerini keşfettin. Burada güçlü teknoloji var!",
                    "background": "/static/images/imperial_tech_priests.jpg",
                    "choices": [
                        {"id": "learn_tech_lore", "text": "Tek Lore'unu Öğren", "effect": "buff:tech_lore, gain_xp:4", "next_scene": "imperial_inquisition"},
                        {"id": "coordinate_tech_priests", "text": "Tek Rahipleri Koordine Et", "effect": "ally:tech_priests_team", "next_scene": "imperial_inquisition"},
                        {"id": "fight_tech_orks", "text": "Tek Orklarıyla Savaş", "combat": True, "enemy": "Tech Orks", "next_scene": "imperial_inquisition"},
                        {"id": "secure_tech_priests", "text": "Tek Rahipleri Güvenli Hale Getir", "effect": "buff:tech_control", "next_scene": "imperial_inquisition"}
                    ]
                },
                {
                    "id": "imperial_inquisition",
                    "title": "İmparatorluk Engizisyon",
                    "description": "Cadia'nın gizli İmparatorluk engizisyonunu keşfettin. Burada güçlü engizisyoncular var!",
                    "background": "/static/images/imperial_inquisition.jpg",
                    "choices": [
                        {"id": "join_inquisition", "text": "Engizisyona Katıl", "effect": "ally:inquisition_team, gain_xp:5", "next_scene": "imperial_assassins"},
                        {"id": "coordinate_inquisition", "text": "Engizisyonu Koordine Et", "effect": "buff:inquisition_support", "next_scene": "imperial_assassins"},
                        {"id": "fight_inquisition_orks", "text": "Engizisyon Orklarıyla Savaş", "combat": True, "enemy": "Inquisition Orks", "next_scene": "imperial_assassins"},
                        {"id": "secure_inquisition", "text": "Engizisyonu Güvenli Hale Getir", "effect": "buff:inquisition_control", "next_scene": "imperial_assassins"}
                    ]
                },
                {
                    "id": "imperial_assassins",
                    "title": "İmparatorluk Suikastçıları",
                    "description": "Cadia'nın gizli İmparatorluk suikastçılarını keşfettin. Burada güçlü suikastçılar var!",
                    "background": "/static/images/imperial_assassins.jpg",
                    "choices": [
                        {"id": "join_assassins", "text": "Suikastçılara Katıl", "effect": "ally:assassins_team, gain_xp:5", "next_scene": "imperial_knights"},
                        {"id": "coordinate_assassins", "text": "Suikastçıları Koordine Et", "effect": "buff:assassins_support", "next_scene": "imperial_knights"},
                        {"id": "fight_assassin_orks", "text": "Suikastçı Orklarıyla Savaş", "combat": True, "enemy": "Assassin Orks", "next_scene": "imperial_knights"},
                        {"id": "secure_assassins", "text": "Suikastçıları Güvenli Hale Getir", "effect": "buff:assassins_control", "next_scene": "imperial_knights"}
                    ]
                },
                {
                    "id": "imperial_knights",
                    "title": "İmparatorluk Şövalyeleri",
                    "description": "Cadia'nın gizli İmparatorluk şövalyelerini keşfettin. Burada güçlü şövalyeler var!",
                    "background": "/static/images/imperial_knights.jpg",
                    "choices": [
                        {"id": "join_knights", "text": "Şövalyelere Katıl", "effect": "ally:knights_team, gain_xp:5", "next_scene": "imperial_titans"},
                        {"id": "coordinate_knights", "text": "Şövalyeleri Koordine Et", "effect": "buff:knights_support", "next_scene": "imperial_titans"},
                        {"id": "fight_knight_orks", "text": "Şövalye Orklarıyla Savaş", "combat": True, "enemy": "Knight Orks", "next_scene": "imperial_titans"},
                        {"id": "secure_knights", "text": "Şövalyeleri Güvenli Hale Getir", "effect": "buff:knights_control", "next_scene": "imperial_titans"}
                    ]
                },
                {
                    "id": "imperial_titans",
                    "title": "İmparatorluk Titanları",
                    "description": "Cadia'nın gizli İmparatorluk titanlarını keşfettin. Burada devasa titanlar var!",
                    "background": "/static/images/imperial_titans.jpg",
                    "choices": [
                        {"id": "pilot_titan", "text": "Titan Pilot Et", "effect": "buff:titan_pilot, gain_xp:6", "next_scene": "imperial_final_battle"},
                        {"id": "coordinate_titans", "text": "Titanları Koordine Et", "effect": "ally:titans_team", "next_scene": "imperial_final_battle"},
                        {"id": "fight_titan_orks", "text": "Titan Orklarıyla Savaş", "combat": True, "enemy": "Titan Orks", "next_scene": "imperial_final_battle"},
                        {"id": "secure_titans", "text": "Titanları Güvenli Hale Getir", "effect": "buff:titans_control", "next_scene": "imperial_final_battle"}
                    ]
                },
                {
                    "id": "imperial_final_battle",
                    "title": "İmparatorluk Son Savaş",
                    "description": "Cadia'nın son savaşı başladı! Bu sıra tabanlı kombat senin için!",
                    "background": "/static/images/imperial_final_battle.jpg",
                    "choices": [
                        {"id": "fight_final_battle", "text": "Son Savaşta Savaş", "combat": True, "enemy": "Imperial Final Boss", "next_scene": "victory"},
                        {"id": "coordinate_final_forces", "text": "Son Güçleri Koordine Et", "effect": "buff:final_coordination", "combat": True, "enemy": "Imperial Final Boss", "next_scene": "victory"},
                        {"id": "call_final_allies", "text": "Son Müttefikleri Çağır", "effect": "ally:final_allies", "combat": True, "enemy": "Imperial Final Boss", "next_scene": "victory"},
                        {"id": "negotiate_final", "text": "Son Müzakere", "effect": "karma:+15", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "space_marine_chapter",
                    "title": "Space Marine Chapter",
                    "description": "Ultramarines Chapter'ının gizli üssüne ulaştın. Burada güçlü Space Marine'ler var!",
                    "background": "/static/images/space_marine_chapter.jpg",
                    "choices": [
                        {"id": "join_ultramarines", "text": "Ultramarines'e Katıl", "effect": "ally:ultramarines_chapter, gain_xp:5", "next_scene": "chaplain_meeting"},
                        {"id": "learn_marine_tactics", "text": "Marine Taktiklerini Öğren", "effect": "buff:marine_tactics", "next_scene": "chaplain_meeting"},
                        {"id": "fight_marine_training", "text": "Marine Eğitimiyle Savaş", "combat": True, "enemy": "Marine Trainers", "next_scene": "chaplain_meeting"},
                        {"id": "study_marine_lore", "text": "Marine Lore'unu Öğren", "effect": "item:marine_lore", "next_scene": "chaplain_meeting"}
                    ]
                },
                {
                    "id": "chaplain_meeting",
                    "title": "Chaplain ile Görüşme",
                    "description": "Chapter Chaplain ile karşılaştın. Bu güçlü ruhani lider sana rehberlik edebilir!",
                    "background": "/static/images/chaplain_meeting.jpg",
                    "choices": [
                        {"id": "receive_blessing", "text": "Chaplain'den Kutsama Al", "effect": "buff:chaplain_blessing, gain_xp:4", "next_scene": "librarian_study"},
                        {"id": "learn_faith", "text": "İmparator İnancını Öğren", "effect": "buff:faith_power", "next_scene": "librarian_study"},
                        {"id": "fight_chaplain", "text": "Chaplain ile Savaş", "combat": True, "enemy": "Chapter Chaplain", "next_scene": "librarian_study"},
                        {"id": "pray_with_chaplain", "text": "Chaplain ile Dua Et", "effect": "buff:divine_protection", "next_scene": "librarian_study"}
                    ]
                },
                {
                    "id": "librarian_study",
                    "title": "Librarian Çalışma Odası",
                    "description": "Chapter Librarian'ın çalışma odasına ulaştın. Burada güçlü psiker büyüleri var!",
                    "background": "/static/images/librarian_study.jpg",
                    "choices": [
                        {"id": "learn_psychic_powers", "text": "Psi Güçlerini Öğren", "effect": "buff:psychic_powers, gain_xp:5", "next_scene": "techmarine_workshop"},
                        {"id": "study_warp_lore", "text": "Warp Lore'unu Öğren", "effect": "item:warp_lore", "next_scene": "techmarine_workshop"},
                        {"id": "fight_librarian", "text": "Librarian ile Savaş", "combat": True, "enemy": "Chapter Librarian", "next_scene": "techmarine_workshop"},
                        {"id": "meditate_with_librarian", "text": "Librarian ile Meditasyon", "effect": "buff:psychic_control", "next_scene": "techmarine_workshop"}
                    ]
                },
                {
                    "id": "techmarine_workshop",
                    "title": "Techmarine Atölyesi",
                    "description": "Chapter Techmarine'in atölyesine ulaştın. Burada güçlü teknoloji var!",
                    "background": "/static/images/techmarine_workshop.jpg",
                    "choices": [
                        {"id": "learn_tech_lore", "text": "Tek Lore'unu Öğren", "effect": "buff:tech_lore, gain_xp:4", "next_scene": "apothecary_lab"},
                        {"id": "get_marine_equipment", "text": "Marine Ekipmanı Al", "effect": "item:marine_equipment", "next_scene": "apothecary_lab"},
                        {"id": "fight_techmarine", "text": "Techmarine ile Savaş", "combat": True, "enemy": "Chapter Techmarine", "next_scene": "apothecary_lab"},
                        {"id": "study_tech_priest_lore", "text": "Tek Rahip Lore'unu Öğren", "effect": "item:tech_priest_lore", "next_scene": "apothecary_lab"}
                    ]
                },
                {
                    "id": "apothecary_lab",
                    "title": "Apothecary Laboratuvarı",
                    "description": "Chapter Apothecary'nin laboratuvarına ulaştın. Burada güçlü tıbbi teknoloji var!",
                    "background": "/static/images/apothecary_lab.jpg",
                    "choices": [
                        {"id": "learn_medical_lore", "text": "Tıbbi Lore'u Öğren", "effect": "buff:medical_lore, gain_xp:4", "next_scene": "dreadnought_chamber"},
                        {"id": "get_medical_supplies", "text": "Tıbbi Malzeme Al", "effect": "item:medical_supplies", "next_scene": "dreadnought_chamber"},
                        {"id": "fight_apothecary", "text": "Apothecary ile Savaş", "combat": True, "enemy": "Chapter Apothecary", "next_scene": "dreadnought_chamber"},
                        {"id": "study_gene_seed", "text": "Gene Seed'i İncele", "effect": "item:gene_seed_knowledge", "next_scene": "dreadnought_chamber"}
                    ]
                },
                {
                    "id": "dreadnought_chamber",
                    "title": "Dreadnought Odası",
                    "description": "Chapter Dreadnought'larının odasına ulaştın. Burada güçlü Dreadnought'lar var!",
                    "background": "/static/images/dreadnought_chamber.jpg",
                    "choices": [
                        {"id": "pilot_dreadnought", "text": "Dreadnought Pilot Et", "effect": "buff:dreadnought_pilot, gain_xp:6", "next_scene": "terminator_armory"},
                        {"id": "learn_dreadnought_lore", "text": "Dreadnought Lore'unu Öğren", "effect": "item:dreadnought_lore", "next_scene": "terminator_armory"},
                        {"id": "fight_dreadnought", "text": "Dreadnought ile Savaş", "combat": True, "enemy": "Chapter Dreadnought", "next_scene": "terminator_armory"},
                        {"id": "honor_dreadnought", "text": "Dreadnought'u Onurlandır", "effect": "buff:honor_blessing", "next_scene": "terminator_armory"}
                    ]
                },
                {
                    "id": "terminator_armory",
                    "title": "Terminator Cephaneliği",
                    "description": "Chapter Terminator cephaneliğine ulaştın. Burada güçlü Terminator zırhları var!",
                    "background": "/static/images/terminator_armory.jpg",
                    "choices": [
                        {"id": "get_terminator_armor", "text": "Terminator Zırhı Al", "effect": "item:terminator_armor", "next_scene": "land_raider_bay"},
                        {"id": "learn_terminator_tactics", "text": "Terminator Taktiklerini Öğren", "effect": "buff:terminator_tactics", "next_scene": "land_raider_bay"},
                        {"id": "fight_terminator", "text": "Terminator ile Savaş", "combat": True, "enemy": "Chapter Terminator", "next_scene": "land_raider_bay"},
                        {"id": "study_terminator_lore", "text": "Terminator Lore'unu Öğren", "effect": "item:terminator_lore", "next_scene": "land_raider_bay"}
                    ]
                },
                {
                    "id": "land_raider_bay",
                    "title": "Land Raider Hangarı",
                    "description": "Chapter Land Raider hangarına ulaştın. Burada güçlü Land Raider'lar var!",
                    "background": "/static/images/land_raider_bay.jpg",
                    "choices": [
                        {"id": "pilot_land_raider", "text": "Land Raider Pilot Et", "effect": "buff:land_raider_pilot, gain_xp:5", "next_scene": "thunderhawk_hangar"},
                        {"id": "learn_vehicle_tactics", "text": "Araç Taktiklerini Öğren", "effect": "buff:vehicle_tactics", "next_scene": "thunderhawk_hangar"},
                        {"id": "fight_land_raider", "text": "Land Raider ile Savaş", "combat": True, "enemy": "Chapter Land Raider", "next_scene": "thunderhawk_hangar"},
                        {"id": "study_vehicle_lore", "text": "Araç Lore'unu Öğren", "effect": "item:vehicle_lore", "next_scene": "thunderhawk_hangar"}
                    ]
                },
                {
                    "id": "thunderhawk_hangar",
                    "title": "Thunderhawk Hangarı",
                    "description": "Chapter Thunderhawk hangarına ulaştın. Burada güçlü Thunderhawk'lar var!",
                    "background": "/static/images/thunderhawk_hangar.jpg",
                    "choices": [
                        {"id": "pilot_thunderhawk", "text": "Thunderhawk Pilot Et", "effect": "buff:thunderhawk_pilot, gain_xp:6", "next_scene": "battle_barge_bridge"},
                        {"id": "learn_air_tactics", "text": "Hava Taktiklerini Öğren", "effect": "buff:air_tactics", "next_scene": "battle_barge_bridge"},
                        {"id": "fight_thunderhawk", "text": "Thunderhawk ile Savaş", "combat": True, "enemy": "Chapter Thunderhawk", "next_scene": "battle_barge_bridge"},
                        {"id": "study_air_lore", "text": "Hava Lore'unu Öğren", "effect": "item:air_lore", "next_scene": "battle_barge_bridge"}
                    ]
                },
                {
                    "id": "battle_barge_bridge",
                    "title": "Battle Barge Köprüsü",
                    "description": "Chapter Battle Barge'ının köprüsüne ulaştın. Burada güçlü Battle Barge var!",
                    "background": "/static/images/battle_barge_bridge.jpg",
                    "choices": [
                        {"id": "command_battle_barge", "text": "Battle Barge'ı Komuta Et", "effect": "buff:battle_barge_command, gain_xp:7", "next_scene": "chapter_master_chamber"},
                        {"id": "learn_naval_tactics", "text": "Deniz Taktiklerini Öğren", "effect": "buff:naval_tactics", "next_scene": "chapter_master_chamber"},
                        {"id": "fight_battle_barge", "text": "Battle Barge ile Savaş", "combat": True, "enemy": "Chapter Battle Barge", "next_scene": "chapter_master_chamber"},
                        {"id": "study_naval_lore", "text": "Deniz Lore'unu Öğren", "effect": "item:naval_lore", "next_scene": "chapter_master_chamber"}
                    ]
                },
                {
                    "id": "chapter_master_chamber",
                    "title": "Chapter Master Odası",
                    "description": "Chapter Master'ın odasına ulaştın. Burada güçlü Chapter Master var!",
                    "background": "/static/images/chapter_master_chamber.jpg",
                    "choices": [
                        {"id": "meet_chapter_master", "text": "Chapter Master ile Görüş", "effect": "ally:chapter_master, gain_xp:8", "next_scene": "ork_warboss_final"},
                        {"id": "learn_master_tactics", "text": "Master Taktiklerini Öğren", "effect": "buff:master_tactics", "next_scene": "ork_warboss_final"},
                        {"id": "fight_chapter_master", "text": "Chapter Master ile Savaş", "combat": True, "enemy": "Chapter Master", "next_scene": "ork_warboss_final"},
                        {"id": "receive_master_blessing", "text": "Master Kutsaması Al", "effect": "buff:master_blessing", "next_scene": "ork_warboss_final"}
                    ]
                },
                {
                    "id": "ork_warboss_final",
                    "title": "Ork Warboss Final Savaşı",
                    "description": "Ork Warboss Gorkamorka ile son savaş! Bu sıra tabanlı kombat senin için!",
                    "background": "/static/images/ork_warboss_final.jpg",
                    "choices": [
                        {"id": "fight_warboss", "text": "Warboss ile Savaş", "combat": True, "enemy": "Ork Warboss Gorkamorka", "next_scene": "victory"},
                        {"id": "use_marine_tactics", "text": "Marine Taktiklerini Kullan", "effect": "buff:marine_power", "combat": True, "enemy": "Ork Warboss Gorkamorka", "next_scene": "victory"},
                        {"id": "call_marine_allies", "text": "Marine Müttefiklerini Çağır", "effect": "ally:marine_allies", "combat": True, "enemy": "Ork Warboss Gorkamorka", "next_scene": "victory"},
                        {"id": "negotiate_warboss", "text": "Warboss ile Müzakere", "effect": "karma:+15", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "imperial_guard_regiment",
                    "title": "İmparatorluk Muhafız Alayı",
                    "description": "Cadian Shock Troops alayına ulaştın. Burada güçlü İmparatorluk Muhafızları var!",
                    "background": "/static/images/imperial_guard_regiment.jpg",
                    "choices": [
                        {"id": "join_guard_regiment", "text": "Muhafız Alayına Katıl", "effect": "ally:guard_regiment, gain_xp:4", "next_scene": "imperial_guard_artillery"},
                        {"id": "learn_guard_tactics", "text": "Muhafız Taktiklerini Öğren", "effect": "buff:guard_tactics", "next_scene": "imperial_guard_artillery"},
                        {"id": "fight_guard_training", "text": "Muhafız Eğitimiyle Savaş", "combat": True, "enemy": "Guard Trainers", "next_scene": "imperial_guard_artillery"},
                        {"id": "study_guard_lore", "text": "Muhafız Lore'unu Öğren", "effect": "item:guard_lore", "next_scene": "imperial_guard_artillery"}
                    ]
                },
                {
                    "id": "imperial_guard_artillery",
                    "title": "İmparatorluk Muhafız Topçusu",
                    "description": "İmparatorluk Muhafız topçu birliğine ulaştın. Burada güçlü toplar var!",
                    "background": "/static/images/imperial_guard_artillery.jpg",
                    "choices": [
                        {"id": "command_artillery", "text": "Topçuyu Komuta Et", "effect": "buff:artillery_command, gain_xp:5", "next_scene": "imperial_guard_tanks"},
                        {"id": "learn_artillery_tactics", "text": "Topçu Taktiklerini Öğren", "effect": "buff:artillery_tactics", "next_scene": "imperial_guard_tanks"},
                        {"id": "fight_artillery_crew", "text": "Topçu Ekibiyle Savaş", "combat": True, "enemy": "Artillery Crew", "next_scene": "imperial_guard_tanks"},
                        {"id": "study_artillery_lore", "text": "Topçu Lore'unu Öğren", "effect": "item:artillery_lore", "next_scene": "imperial_guard_tanks"}
                    ]
                },
                {
                    "id": "imperial_guard_tanks",
                    "title": "İmparatorluk Muhafız Tankları",
                    "description": "İmparatorluk Muhafız tank birliğine ulaştın. Burada güçlü Leman Russ tankları var!",
                    "background": "/static/images/imperial_guard_tanks.jpg",
                    "choices": [
                        {"id": "pilot_leman_russ", "text": "Leman Russ Pilot Et", "effect": "buff:leman_russ_pilot, gain_xp:5", "next_scene": "imperial_guard_air_support"},
                        {"id": "learn_tank_tactics", "text": "Tank Taktiklerini Öğren", "effect": "buff:tank_tactics", "next_scene": "imperial_guard_air_support"},
                        {"id": "fight_tank_crew", "text": "Tank Ekibiyle Savaş", "combat": True, "enemy": "Tank Crew", "next_scene": "imperial_guard_air_support"},
                        {"id": "study_tank_lore", "text": "Tank Lore'unu Öğren", "effect": "item:tank_lore", "next_scene": "imperial_guard_air_support"}
                    ]
                },
                {
                    "id": "imperial_guard_air_support",
                    "title": "İmparatorluk Muhafız Hava Desteği",
                    "description": "İmparatorluk Muhafız hava desteği birliğine ulaştın. Burada güçlü Valkyrie'ler var!",
                    "background": "/static/images/imperial_guard_air_support.jpg",
                    "choices": [
                        {"id": "pilot_valkyrie", "text": "Valkyrie Pilot Et", "effect": "buff:valkyrie_pilot, gain_xp:6", "next_scene": "imperial_guard_commissar"},
                        {"id": "learn_air_tactics", "text": "Hava Taktiklerini Öğren", "effect": "buff:air_tactics", "next_scene": "imperial_guard_commissar"},
                        {"id": "fight_air_crew", "text": "Hava Ekibiyle Savaş", "combat": True, "enemy": "Air Crew", "next_scene": "imperial_guard_commissar"},
                        {"id": "study_air_lore", "text": "Hava Lore'unu Öğren", "effect": "item:air_lore", "next_scene": "imperial_guard_commissar"}
                    ]
                },
                {
                    "id": "imperial_guard_commissar",
                    "title": "İmparatorluk Muhafız Commissar",
                    "description": "İmparatorluk Muhafız Commissar'ına ulaştın. Burada güçlü Commissar var!",
                    "background": "/static/images/imperial_guard_commissar.jpg",
                    "choices": [
                        {"id": "meet_guard_commissar", "text": "Commissar ile Görüş", "effect": "ally:guard_commissar, gain_xp:4", "next_scene": "imperial_guard_priest"},
                        {"id": "learn_discipline", "text": "Disiplin Öğren", "effect": "buff:discipline_power", "next_scene": "imperial_guard_priest"},
                        {"id": "fight_commissar", "text": "Commissar ile Savaş", "combat": True, "enemy": "Guard Commissar", "next_scene": "imperial_guard_priest"},
                        {"id": "receive_commissar_blessing", "text": "Commissar Kutsaması Al", "effect": "buff:commissar_blessing", "next_scene": "imperial_guard_priest"}
                    ]
                },
                {
                    "id": "imperial_guard_priest",
                    "title": "İmparatorluk Muhafız Rahip",
                    "description": "İmparatorluk Muhafız rahibine ulaştın. Burada güçlü rahip var!",
                    "background": "/static/images/imperial_guard_priest.jpg",
                    "choices": [
                        {"id": "pray_with_guard_priest", "text": "Rahiple Dua Et", "effect": "buff:priest_blessing, gain_xp:4", "next_scene": "imperial_guard_psyker"},
                        {"id": "learn_faith", "text": "İmparator İnancını Öğren", "effect": "buff:faith_power", "next_scene": "imperial_guard_psyker"},
                        {"id": "fight_priest", "text": "Rahiple Savaş", "combat": True, "enemy": "Guard Priest", "next_scene": "imperial_guard_psyker"},
                        {"id": "receive_priest_blessing", "text": "Rahip Kutsaması Al", "effect": "buff:divine_protection", "next_scene": "imperial_guard_psyker"}
                    ]
                },
                {
                    "id": "imperial_guard_psyker",
                    "title": "İmparatorluk Muhafız Psiker",
                    "description": "İmparatorluk Muhafız psikerine ulaştın. Burada güçlü psiker var!",
                    "background": "/static/images/imperial_guard_psyker.jpg",
                    "choices": [
                        {"id": "learn_guard_psychic", "text": "Muhafız Psi Güçlerini Öğren", "effect": "buff:psychic_powers, gain_xp:5", "next_scene": "imperial_guard_tech_priest"},
                        {"id": "study_warp_lore", "text": "Warp Lore'unu Öğren", "effect": "item:warp_lore", "next_scene": "imperial_guard_tech_priest"},
                        {"id": "fight_psyker", "text": "Psiker ile Savaş", "combat": True, "enemy": "Guard Psyker", "next_scene": "imperial_guard_tech_priest"},
                        {"id": "meditate_with_psyker", "text": "Psiker ile Meditasyon", "effect": "buff:psychic_control", "next_scene": "imperial_guard_tech_priest"}
                    ]
                },
                {
                    "id": "imperial_guard_tech_priest",
                    "title": "İmparatorluk Muhafız Tek Rahip",
                    "description": "İmparatorluk Muhafız tek rahibine ulaştın. Burada güçlü teknoloji var!",
                    "background": "/static/images/imperial_guard_tech_priest.jpg",
                    "choices": [
                        {"id": "learn_guard_tech_lore", "text": "Muhafız Tek Lore'unu Öğren", "effect": "buff:tech_lore, gain_xp:4", "next_scene": "imperial_guard_final_battle"},
                        {"id": "get_guard_equipment", "text": "Muhafız Ekipmanı Al", "effect": "item:guard_equipment", "next_scene": "imperial_guard_final_battle"},
                        {"id": "fight_tech_priest", "text": "Tek Rahip ile Savaş", "combat": True, "enemy": "Guard Tech Priest", "next_scene": "imperial_guard_final_battle"},
                        {"id": "study_tech_priest_lore", "text": "Tek Rahip Lore'unu Öğren", "effect": "item:tech_priest_lore", "next_scene": "imperial_guard_final_battle"}
                    ]
                },
                {
                    "id": "imperial_guard_final_battle",
                    "title": "İmparatorluk Muhafız Son Savaş",
                    "description": "İmparatorluk Muhafız son savaşı başladı! Bu sıra tabanlı kombat senin için!",
                    "background": "/static/images/imperial_guard_final_battle.jpg",
                    "choices": [
                        {"id": "fight_final_battle", "text": "Son Savaşta Savaş", "combat": True, "enemy": "Imperial Guard Final Boss", "next_scene": "victory"},
                        {"id": "use_guard_tactics", "text": "Muhafız Taktiklerini Kullan", "effect": "buff:guard_power", "combat": True, "enemy": "Imperial Guard Final Boss", "next_scene": "victory"},
                        {"id": "call_guard_allies", "text": "Muhafız Müttefiklerini Çağır", "effect": "ally:guard_allies", "combat": True, "enemy": "Imperial Guard Final Boss", "next_scene": "victory"},
                        {"id": "negotiate_final", "text": "Son Müzakere", "effect": "karma:+15", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "imperial_fortress",
                    "title": "İmparatorluk Kalesi",
                    "description": "Cadia'nın İmparatorluk kalesine ulaştın. Burada güçlü savunma sistemleri var!",
                    "background": "/static/images/imperial_fortress.jpg",
                    "choices": [
                        {"id": "command_fortress", "text": "Kaleyi Komuta Et", "effect": "buff:fortress_command, gain_xp:5", "next_scene": "imperial_arsenal"},
                        {"id": "study_fortress_defenses", "text": "Kale Savunmalarını İncele", "effect": "buff:defense_knowledge", "next_scene": "imperial_arsenal"},
                        {"id": "fight_fortress_guards", "text": "Kale Muhafızları ile Savaş", "combat": True, "enemy": "Fortress Guards", "next_scene": "imperial_arsenal"},
                        {"id": "learn_fortress_lore", "text": "Kale Lore'unu Öğren", "effect": "item:fortress_lore", "next_scene": "imperial_arsenal"}
                    ]
                },
                {
                    "id": "imperial_arsenal",
                    "title": "İmparatorluk Cephaneliği",
                    "description": "Cadia'nın İmparatorluk cephaneliğine ulaştın. Burada güçlü silahlar var!",
                    "background": "/static/images/imperial_arsenal.jpg",
                    "choices": [
                        {"id": "get_imperial_weapons", "text": "İmparatorluk Silahları Al", "effect": "item:imperial_weapons", "next_scene": "imperial_barracks"},
                        {"id": "learn_weapon_crafting", "text": "Silah Yapımını Öğren", "effect": "buff:weapon_crafting", "next_scene": "imperial_barracks"},
                        {"id": "fight_arsenal_guards", "text": "Cephanelik Muhafızları ile Savaş", "combat": True, "enemy": "Arsenal Guards", "next_scene": "imperial_barracks"},
                        {"id": "study_arsenal_lore", "text": "Cephanelik Lore'unu Öğren", "effect": "item:arsenal_lore", "next_scene": "imperial_barracks"}
                    ]
                },
                {
                    "id": "imperial_barracks",
                    "title": "İmparatorluk Kışlası",
                    "description": "Cadia'nın İmparatorluk kışlasına ulaştın. Burada güçlü askerler var!",
                    "background": "/static/images/imperial_barracks.jpg",
                    "choices": [
                        {"id": "train_with_soldiers", "text": "Askerlerle Eğitim Al", "effect": "ally:imperial_soldiers, gain_xp:4", "next_scene": "imperial_medical"},
                        {"id": "learn_military_tactics", "text": "Askeri Taktikleri Öğren", "effect": "buff:military_tactics", "next_scene": "imperial_medical"},
                        {"id": "fight_training_officers", "text": "Eğitim Subayları ile Savaş", "combat": True, "enemy": "Training Officers", "next_scene": "imperial_medical"},
                        {"id": "study_military_lore", "text": "Askeri Lore'u Öğren", "effect": "item:military_lore", "next_scene": "imperial_medical"}
                    ]
                },
                {
                    "id": "imperial_medical",
                    "title": "İmparatorluk Tıbbi Merkezi",
                    "description": "Cadia'nın İmparatorluk tıbbi merkezine ulaştın. Burada güçlü doktorlar var!",
                    "background": "/static/images/imperial_medical.jpg",
                    "choices": [
                        {"id": "help_medical_staff", "text": "Tıbbi Personele Yardım Et", "effect": "ally:medical_staff, gain_xp:4", "next_scene": "imperial_communications"},
                        {"id": "learn_medical_skills", "text": "Tıbbi Becerileri Öğren", "effect": "buff:medical_skills", "next_scene": "imperial_communications"},
                        {"id": "fight_medical_security", "text": "Tıbbi Güvenlik ile Savaş", "combat": True, "enemy": "Medical Security", "next_scene": "imperial_communications"},
                        {"id": "study_medical_lore", "text": "Tıbbi Lore'u Öğren", "effect": "item:medical_lore", "next_scene": "imperial_communications"}
                    ]
                },
                {
                    "id": "imperial_communications",
                    "title": "İmparatorluk İletişim Merkezi",
                    "description": "Cadia'nın İmparatorluk iletişim merkezine ulaştın. Burada güçlü iletişim sistemleri var!",
                    "background": "/static/images/imperial_communications.jpg",
                    "choices": [
                        {"id": "hack_communication_systems", "text": "İletişim Sistemlerini Hack Et", "effect": "buff:communication_control, gain_xp:4", "next_scene": "imperial_intelligence"},
                        {"id": "coordinate_forces", "text": "Güçleri Koordine Et", "effect": "ally:communication_team", "next_scene": "imperial_intelligence"},
                        {"id": "fight_comm_guards", "text": "İletişim Muhafızları ile Savaş", "combat": True, "enemy": "Comm Guards", "next_scene": "imperial_intelligence"},
                        {"id": "study_comm_lore", "text": "İletişim Lore'unu Öğren", "effect": "item:comm_lore", "next_scene": "imperial_intelligence"}
                    ]
                },
                {
                    "id": "imperial_intelligence",
                    "title": "İmparatorluk İstihbarat Merkezi",
                    "description": "Cadia'nın İmparatorluk istihbarat merkezine ulaştın. Burada güçlü ajanlar var!",
                    "background": "/static/images/imperial_intelligence.jpg",
                    "choices": [
                        {"id": "join_intelligence", "text": "İstihbarata Katıl", "effect": "ally:intelligence_agents, gain_xp:5", "next_scene": "imperial_research"},
                        {"id": "learn_spy_skills", "text": "Casus Becerilerini Öğren", "effect": "buff:spy_skills", "next_scene": "imperial_research"},
                        {"id": "fight_intelligence_agents", "text": "İstihbarat Ajanları ile Savaş", "combat": True, "enemy": "Intelligence Agents", "next_scene": "imperial_research"},
                        {"id": "study_intelligence_lore", "text": "İstihbarat Lore'unu Öğren", "effect": "item:intelligence_lore", "next_scene": "imperial_research"}
                    ]
                },
                {
                    "id": "imperial_research",
                    "title": "İmparatorluk Araştırma Merkezi",
                    "description": "Cadia'nın İmparatorluk araştırma merkezine ulaştın. Burada güçlü bilim adamları var!",
                    "background": "/static/images/imperial_research.jpg",
                    "choices": [
                        {"id": "join_research_team", "text": "Araştırma Ekibine Katıl", "effect": "ally:research_team, gain_xp:5", "next_scene": "imperial_engineering"},
                        {"id": "learn_research_skills", "text": "Araştırma Becerilerini Öğren", "effect": "buff:research_skills", "next_scene": "imperial_engineering"},
                        {"id": "fight_research_security", "text": "Araştırma Güvenliği ile Savaş", "combat": True, "enemy": "Research Security", "next_scene": "imperial_engineering"},
                        {"id": "study_research_lore", "text": "Araştırma Lore'unu Öğren", "effect": "item:research_lore", "next_scene": "imperial_engineering"}
                    ]
                },
                {
                    "id": "imperial_engineering",
                    "title": "İmparatorluk Mühendislik Merkezi",
                    "description": "Cadia'nın İmparatorluk mühendislik merkezine ulaştın. Burada güçlü mühendisler var!",
                    "background": "/static/images/imperial_engineering.jpg",
                    "choices": [
                        {"id": "join_engineering_team", "text": "Mühendislik Ekibine Katıl", "effect": "ally:engineering_team, gain_xp:5", "next_scene": "imperial_artillery"},
                        {"id": "learn_engineering_skills", "text": "Mühendislik Becerilerini Öğren", "effect": "buff:engineering_skills", "next_scene": "imperial_artillery"},
                        {"id": "fight_engineering_guards", "text": "Mühendislik Muhafızları ile Savaş", "combat": True, "enemy": "Engineering Guards", "next_scene": "imperial_artillery"},
                        {"id": "study_engineering_lore", "text": "Mühendislik Lore'unu Öğren", "effect": "item:engineering_lore", "next_scene": "imperial_artillery"}
                    ]
                },
                {
                    "id": "imperial_artillery",
                    "title": "İmparatorluk Topçu Birliği",
                    "description": "Cadia'nın İmparatorluk topçu birliğine ulaştın. Burada güçlü toplar var!",
                    "background": "/static/images/imperial_artillery.jpg",
                    "choices": [
                        {"id": "command_artillery", "text": "Topçuyu Komuta Et", "effect": "buff:artillery_command, gain_xp:5", "next_scene": "imperial_tanks"},
                        {"id": "learn_artillery_tactics", "text": "Topçu Taktiklerini Öğren", "effect": "buff:artillery_tactics", "next_scene": "imperial_tanks"},
                        {"id": "fight_artillery_crew", "text": "Topçu Ekibi ile Savaş", "combat": True, "enemy": "Artillery Crew", "next_scene": "imperial_tanks"},
                        {"id": "study_artillery_lore", "text": "Topçu Lore'unu Öğren", "effect": "item:artillery_lore", "next_scene": "imperial_tanks"}
                    ]
                },
                {
                    "id": "imperial_tanks",
                    "title": "İmparatorluk Tank Birliği",
                    "description": "Cadia'nın İmparatorluk tank birliğine ulaştın. Burada güçlü tanklar var!",
                    "background": "/static/images/imperial_tanks.jpg",
                    "choices": [
                        {"id": "pilot_imperial_tank", "text": "İmparatorluk Tankı Pilot Et", "effect": "buff:tank_pilot, gain_xp:5", "next_scene": "imperial_air_support"},
                        {"id": "learn_tank_tactics", "text": "Tank Taktiklerini Öğren", "effect": "buff:tank_tactics", "next_scene": "imperial_air_support"},
                        {"id": "fight_tank_crew", "text": "Tank Ekibi ile Savaş", "combat": True, "enemy": "Tank Crew", "next_scene": "imperial_air_support"},
                        {"id": "study_tank_lore", "text": "Tank Lore'unu Öğren", "effect": "item:tank_lore", "next_scene": "imperial_air_support"}
                    ]
                },
                {
                    "id": "imperial_air_support",
                    "title": "İmparatorluk Hava Desteği",
                    "description": "Cadia'nın İmparatorluk hava desteği birliğine ulaştın. Burada güçlü uçaklar var!",
                    "background": "/static/images/imperial_air_support.jpg",
                    "choices": [
                        {"id": "pilot_imperial_aircraft", "text": "İmparatorluk Uçağı Pilot Et", "effect": "buff:aircraft_pilot, gain_xp:6", "next_scene": "imperial_special_forces"},
                        {"id": "learn_air_tactics", "text": "Hava Taktiklerini Öğren", "effect": "buff:air_tactics", "next_scene": "imperial_special_forces"},
                        {"id": "fight_air_crew", "text": "Hava Ekibi ile Savaş", "combat": True, "enemy": "Air Crew", "next_scene": "imperial_special_forces"},
                        {"id": "study_air_lore", "text": "Hava Lore'unu Öğren", "effect": "item:air_lore", "next_scene": "imperial_special_forces"}
                    ]
                },
                {
                    "id": "imperial_special_forces",
                    "title": "İmparatorluk Özel Kuvvetler",
                    "description": "Cadia'nın İmparatorluk özel kuvvetlerine ulaştın. Burada güçlü elit askerler var!",
                    "background": "/static/images/imperial_special_forces.jpg",
                    "choices": [
                        {"id": "join_special_forces", "text": "Özel Kuvvetlere Katıl", "effect": "ally:special_forces, gain_xp:6", "next_scene": "imperial_psykers"},
                        {"id": "learn_special_tactics", "text": "Özel Taktikleri Öğren", "effect": "buff:special_tactics", "next_scene": "imperial_psykers"},
                        {"id": "fight_special_forces", "text": "Özel Kuvvetler ile Savaş", "combat": True, "enemy": "Special Forces", "next_scene": "imperial_psykers"},
                        {"id": "study_special_lore", "text": "Özel Kuvvetler Lore'unu Öğren", "effect": "item:special_lore", "next_scene": "imperial_psykers"}
                    ]
                },
                {
                    "id": "imperial_psykers",
                    "title": "İmparatorluk Psikerler",
                    "description": "Cadia'nın İmparatorluk psikerlerine ulaştın. Burada güçlü psikerler var!",
                    "background": "/static/images/imperial_psykers.jpg",
                    "choices": [
                        {"id": "join_psykers", "text": "Psikerlere Katıl", "effect": "ally:psykers, gain_xp:5", "next_scene": "imperial_tech_priests"},
                        {"id": "learn_psychic_powers", "text": "Psi Güçlerini Öğren", "effect": "buff:psychic_powers", "next_scene": "imperial_tech_priests"},
                        {"id": "fight_psykers", "text": "Psikerler ile Savaş", "combat": True, "enemy": "Psykers", "next_scene": "imperial_tech_priests"},
                        {"id": "study_psychic_lore", "text": "Psi Lore'unu Öğren", "effect": "item:psychic_lore", "next_scene": "imperial_tech_priests"}
                    ]
                },
                {
                    "id": "imperial_tech_priests",
                    "title": "İmparatorluk Tek Rahipleri",
                    "description": "Cadia'nın İmparatorluk tek rahiplerine ulaştın. Burada güçlü teknoloji var!",
                    "background": "/static/images/imperial_tech_priests.jpg",
                    "choices": [
                        {"id": "join_tech_priests", "text": "Tek Rahiplere Katıl", "effect": "ally:tech_priests, gain_xp:5", "next_scene": "imperial_inquisition"},
                        {"id": "learn_tech_lore", "text": "Tek Lore'unu Öğren", "effect": "buff:tech_lore", "next_scene": "imperial_inquisition"},
                        {"id": "fight_tech_priests", "text": "Tek Rahipler ile Savaş", "combat": True, "enemy": "Tech Priests", "next_scene": "imperial_inquisition"},
                        {"id": "study_tech_lore", "text": "Tek Rahip Lore'unu Öğren", "effect": "item:tech_priest_lore", "next_scene": "imperial_inquisition"}
                    ]
                },
                {
                    "id": "imperial_inquisition",
                    "title": "İmparatorluk Engizisyon",
                    "description": "Cadia'nın İmparatorluk engizisyonuna ulaştın. Burada güçlü engizisyoncular var!",
                    "background": "/static/images/imperial_inquisition.jpg",
                    "choices": [
                        {"id": "join_inquisition", "text": "Engizisyona Katıl", "effect": "ally:inquisition, gain_xp:6", "next_scene": "imperial_assassins"},
                        {"id": "learn_inquisition_lore", "text": "Engizisyon Lore'unu Öğren", "effect": "buff:inquisition_power", "next_scene": "imperial_assassins"},
                        {"id": "fight_inquisitors", "text": "Engizisyoncular ile Savaş", "combat": True, "enemy": "Inquisitors", "next_scene": "imperial_assassins"},
                        {"id": "study_inquisition_lore", "text": "Engizisyon Lore'unu Öğren", "effect": "item:inquisition_lore", "next_scene": "imperial_assassins"}
                    ]
                },
                {
                    "id": "imperial_assassins",
                    "title": "İmparatorluk Suikastçıları",
                    "description": "Cadia'nın İmparatorluk suikastçılarına ulaştın. Burada güçlü suikastçılar var!",
                    "background": "/static/images/imperial_assassins.jpg",
                    "choices": [
                        {"id": "join_assassins", "text": "Suikastçılara Katıl", "effect": "ally:assassins, gain_xp:6", "next_scene": "imperial_knights"},
                        {"id": "learn_assassin_skills", "text": "Suikastçı Becerilerini Öğren", "effect": "buff:assassin_skills", "next_scene": "imperial_knights"},
                        {"id": "fight_assassins", "text": "Suikastçılar ile Savaş", "combat": True, "enemy": "Assassins", "next_scene": "imperial_knights"},
                        {"id": "study_assassin_lore", "text": "Suikastçı Lore'unu Öğren", "effect": "item:assassin_lore", "next_scene": "imperial_knights"}
                    ]
                },
                {
                    "id": "imperial_knights",
                    "title": "İmparatorluk Şövalyeleri",
                    "description": "Cadia'nın İmparatorluk şövalyelerine ulaştın. Burada güçlü şövalyeler var!",
                    "background": "/static/images/imperial_knights.jpg",
                    "choices": [
                        {"id": "join_knights", "text": "Şövalyelere Katıl", "effect": "ally:knights, gain_xp:6", "next_scene": "imperial_titans"},
                        {"id": "learn_knight_tactics", "text": "Şövalye Taktiklerini Öğren", "effect": "buff:knight_tactics", "next_scene": "imperial_titans"},
                        {"id": "fight_knights", "text": "Şövalyeler ile Savaş", "combat": True, "enemy": "Knights", "next_scene": "imperial_titans"},
                        {"id": "study_knight_lore", "text": "Şövalye Lore'unu Öğren", "effect": "item:knight_lore", "next_scene": "imperial_titans"}
                    ]
                },
                {
                    "id": "imperial_titans",
                    "title": "İmparatorluk Titanları",
                    "description": "Cadia'nın İmparatorluk titanlarına ulaştın. Burada devasa titanlar var!",
                    "background": "/static/images/imperial_titans.jpg",
                    "choices": [
                        {"id": "pilot_titan", "text": "Titan Pilot Et", "effect": "buff:titan_pilot, gain_xp:7", "next_scene": "imperial_final_battle"},
                        {"id": "learn_titan_tactics", "text": "Titan Taktiklerini Öğren", "effect": "buff:titan_tactics", "next_scene": "imperial_final_battle"},
                        {"id": "fight_titan", "text": "Titan ile Savaş", "combat": True, "enemy": "Titan", "next_scene": "imperial_final_battle"},
                        {"id": "study_titan_lore", "text": "Titan Lore'unu Öğren", "effect": "item:titan_lore", "next_scene": "imperial_final_battle"}
                    ]
                },
                {
                    "id": "imperial_final_battle",
                    "title": "İmparatorluk Son Savaş",
                    "description": "İmparatorluk son savaşı başladı! Bu sıra tabanlı kombat senin için!",
                    "background": "/static/images/imperial_final_battle.jpg",
                    "choices": [
                        {"id": "fight_imperial_final_boss", "text": "İmparatorluk Son Boss ile Savaş", "combat": True, "enemy": "Imperial Final Boss", "next_scene": "victory"},
                        {"id": "use_imperial_tactics", "text": "İmparatorluk Taktiklerini Kullan", "effect": "buff:imperial_power", "combat": True, "enemy": "Imperial Final Boss", "next_scene": "victory"},
                        {"id": "call_imperial_allies", "text": "İmparatorluk Müttefiklerini Çağır", "effect": "ally:imperial_allies", "combat": True, "enemy": "Imperial Final Boss", "next_scene": "victory"},
                        {"id": "negotiate_imperial_boss", "text": "İmparatorluk Boss ile Müzakere", "effect": "karma:+15", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "ork_scout_encounter",
                    "title": "Ork Keşif Karşılaşması",
                    "description": "Ork keşif birimiyle karşılaştın. Bu küçük grup büyük tehdidin habercisi!",
                    "background": "/static/images/ork_scout_encounter.jpg",
                    "choices": [
                        {"id": "fight_ork_scouts", "text": "Ork Keşif Birimiyle Savaş", "combat": True, "enemy": "Ork Scouts", "next_scene": "ork_camp_discovery"},
                        {"id": "interrogate_ork_scout", "text": "Ork Keşif Askerini Sorgula", "effect": "item:ork_intel, gain_xp:3", "next_scene": "ork_camp_discovery"},
                        {"id": "stealth_approach", "text": "Gizlice Yaklaş", "effect": "buff:stealth_bonus", "next_scene": "ork_camp_discovery"},
                        {"id": "let_them_pass", "text": "Geçmelerine İzin Ver", "effect": "gain_xp:1", "next_scene": "ork_camp_discovery"}
                    ]
                },
                {
                    "id": "ork_camp_discovery",
                    "title": "Ork Kampı Keşfi",
                    "description": "Ork kampını keşfettin. Burada güçlü Ork Boyz'lar var!",
                    "background": "/static/images/ork_camp_discovery.jpg",
                    "choices": [
                        {"id": "infiltrate_ork_camp", "text": "Ork Kampına Sız", "effect": "item:ork_weapons, gain_xp:4", "next_scene": "ork_nob_encounter"},
                        {"id": "attack_ork_camp", "text": "Ork Kampına Saldır", "combat": True, "enemy": "Ork Boyz", "next_scene": "ork_nob_encounter"},
                        {"id": "spy_on_ork_camp", "text": "Ork Kampını Gözetle", "effect": "item:camp_intel", "next_scene": "ork_nob_encounter"},
                        {"id": "call_artillery", "text": "Topçu Desteği Çağır", "effect": "buff:artillery_support", "next_scene": "ork_nob_encounter"}
                    ]
                },
                {
                    "id": "ork_nob_encounter",
                    "title": "Ork Nob Karşılaşması",
                    "description": "Ork Nob ile karşılaştın. Bu güçlü Ork lideri!",
                    "background": "/static/images/ork_nob_encounter.jpg",
                    "choices": [
                        {"id": "fight_ork_nob", "text": "Ork Nob ile Savaş", "combat": True, "enemy": "Ork Nob", "next_scene": "ork_mek_workshop"},
                        {"id": "challenge_ork_nob", "text": "Ork Nob'u Meydan Oku", "effect": "buff:challenge_bonus", "combat": True, "enemy": "Ork Nob", "next_scene": "ork_mek_workshop"},
                        {"id": "negotiate_with_nob", "text": "Ork Nob ile Müzakere", "effect": "karma:+5", "next_scene": "ork_mek_workshop"},
                        {"id": "use_psychic_powers", "text": "Psi Gücü Kullan", "effect": "buff:psychic_boost", "combat": True, "enemy": "Ork Nob", "next_scene": "ork_mek_workshop"}
                    ]
                },
                {
                    "id": "ork_mek_workshop",
                    "title": "Ork Mek Atölyesi",
                    "description": "Ork Mek'in atölyesini keşfettin. Burada güçlü Ork teknolojisi var!",
                    "background": "/static/images/ork_mek_workshop.jpg",
                    "choices": [
                        {"id": "fight_ork_mek", "text": "Ork Mek ile Savaş", "combat": True, "enemy": "Ork Mek", "next_scene": "ork_weirdboy_encounter"},
                        {"id": "steal_ork_tech", "text": "Ork Teknolojisini Çal", "effect": "item:ork_technology", "next_scene": "ork_weirdboy_encounter"},
                        {"id": "sabotage_ork_workshop", "text": "Ork Atölyesini Sabotaj Et", "effect": "buff:sabotage_bonus", "next_scene": "ork_weirdboy_encounter"},
                        {"id": "study_ork_tech", "text": "Ork Teknolojisini İncele", "effect": "item:tech_knowledge", "next_scene": "ork_weirdboy_encounter"}
                    ]
                },
                {
                    "id": "ork_weirdboy_encounter",
                    "title": "Ork Weirdboy Karşılaşması",
                    "description": "Ork Weirdboy ile karşılaştın. Bu güçlü Ork psiker!",
                    "background": "/static/images/ork_weirdboy_encounter.jpg",
                    "choices": [
                        {"id": "fight_ork_weirdboy", "text": "Ork Weirdboy ile Savaş", "combat": True, "enemy": "Ork Weirdboy", "next_scene": "ork_tank_encounter"},
                        {"id": "use_psychic_duel", "text": "Psi Düellosu Yap", "effect": "buff:psychic_duel", "combat": True, "enemy": "Ork Weirdboy", "next_scene": "ork_tank_encounter"},
                        {"id": "disrupt_weirdboy", "text": "Weirdboy'u Boz", "effect": "buff:disruption_bonus", "next_scene": "ork_tank_encounter"},
                        {"id": "study_ork_psychic", "text": "Ork Psi Gücünü İncele", "effect": "item:psychic_knowledge", "next_scene": "ork_tank_encounter"}
                    ]
                },
                {
                    "id": "ork_tank_encounter",
                    "title": "Ork Tank Karşılaşması",
                    "description": "Ork Tank ile karşılaştın. Bu güçlü Ork savaş aracı!",
                    "background": "/static/images/ork_tank_encounter.jpg",
                    "choices": [
                        {"id": "fight_ork_tank", "text": "Ork Tank ile Savaş", "combat": True, "enemy": "Ork Tank", "next_scene": "ork_artillery_encounter"},
                        {"id": "disable_ork_tank", "text": "Ork Tank'ı Devre Dışı Bırak", "effect": "buff:disable_bonus", "next_scene": "ork_artillery_encounter"},
                        {"id": "hijack_ork_tank", "text": "Ork Tank'ı Ele Geçir", "effect": "buff:tank_control", "next_scene": "ork_artillery_encounter"},
                        {"id": "call_air_support", "text": "Hava Desteği Çağır", "effect": "buff:air_support", "next_scene": "ork_artillery_encounter"}
                    ]
                },
                {
                    "id": "ork_artillery_encounter",
                    "title": "Ork Topçu Karşılaşması",
                    "description": "Ork Topçu birimiyle karşılaştın. Bu güçlü Ork topları!",
                    "background": "/static/images/ork_artillery_encounter.jpg",
                    "choices": [
                        {"id": "fight_ork_artillery", "text": "Ork Topçusu ile Savaş", "combat": True, "enemy": "Ork Artillery", "next_scene": "ork_elite_guard"},
                        {"id": "disable_ork_artillery", "text": "Ork Topçusunu Devre Dışı Bırak", "effect": "buff:disable_bonus", "next_scene": "ork_elite_guard"},
                        {"id": "counter_artillery", "text": "Karşı Topçu Saldırısı", "effect": "buff:counter_artillery", "next_scene": "ork_elite_guard"},
                        {"id": "call_imperial_artillery", "text": "İmparatorluk Topçusunu Çağır", "effect": "buff:imperial_artillery", "next_scene": "ork_elite_guard"}
                    ]
                },
                {
                    "id": "ork_elite_guard",
                    "title": "Ork Elit Muhafızları",
                    "description": "Ork Elit Muhafızlarıyla karşılaştın. Bu güçlü Ork savaşçıları!",
                    "background": "/static/images/ork_elite_guard.jpg",
                    "choices": [
                        {"id": "fight_ork_elite", "text": "Ork Elit Muhafızları ile Savaş", "combat": True, "enemy": "Ork Elite Guard", "next_scene": "ork_warboss_preparation"},
                        {"id": "use_tactical_advantage", "text": "Taktik Avantaj Kullan", "effect": "buff:tactical_advantage", "combat": True, "enemy": "Ork Elite Guard", "next_scene": "ork_warboss_preparation"},
                        {"id": "call_special_forces", "text": "Özel Kuvvetleri Çağır", "effect": "buff:special_forces", "next_scene": "ork_warboss_preparation"},
                        {"id": "use_psychic_powers", "text": "Psi Gücü Kullan", "effect": "buff:psychic_boost", "combat": True, "enemy": "Ork Elite Guard", "next_scene": "ork_warboss_preparation"}
                    ]
                },
                {
                    "id": "ork_warboss_preparation",
                    "title": "Warboss'a Hazırlık",
                    "description": "Warboss Gorkamorka'ya karşı son hazırlıkları yapıyorsun. Bu savaş senin için!",
                    "background": "/static/images/ork_warboss_preparation.jpg",
                    "choices": [
                        {"id": "final_equipment_check", "text": "Son Ekipman Kontrolü", "effect": "buff:final_preparation, gain_xp:6", "next_scene": "ork_warboss_final"},
                        {"id": "final_strategy_meeting", "text": "Son Strateji Toplantısı", "effect": "buff:strategy_bonus", "next_scene": "ork_warboss_final"},
                        {"id": "final_blessing", "text": "Son Kutsama", "effect": "buff:final_blessing", "next_scene": "ork_warboss_final"},
                        {"id": "final_ritual", "text": "Son Ritüel", "effect": "buff:final_ritual_power", "next_scene": "ork_warboss_final"}
                    ]
                },
                {
                    "id": "ork_warboss_final",
                    "title": "Ork Warboss Final Savaşı",
                    "description": "Warboss Gorkamorka ile son savaş! Bu sıra tabanlı kombat senin için!",
                    "background": "/static/images/ork_warboss_final.jpg",
                    "choices": [
                        {"id": "fight_warboss", "text": "Warboss ile Savaş", "combat": True, "enemy": "Warboss Gorkamorka", "next_scene": "victory"},
                        {"id": "use_marine_tactics", "text": "Marine Taktiklerini Kullan", "effect": "buff:marine_power", "combat": True, "enemy": "Warboss Gorkamorka", "next_scene": "victory"},
                        {"id": "call_marine_allies", "text": "Marine Müttefiklerini Çağır", "effect": "ally:marine_allies", "combat": True, "enemy": "Warboss Gorkamorka", "next_scene": "victory"},
                        {"id": "negotiate_warboss", "text": "Warboss ile Müzakere", "effect": "karma:+15", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "side_mission_imperial_guard",
                    "title": "Yan Görev: İmparatorluk Muhafızları",
                    "description": "İmparatorluk Muhafızlarına yardım et ve güçlü müttefikler kazan!",
                    "background": "/static/images/side_mission_imperial_guard.jpg",
                    "choices": [
                        {"id": "help_imperial_guard", "text": "İmparatorluk Muhafızlarına Yardım Et", "effect": "ally:imperial_guard, gain_xp:4", "next_scene": "side_mission_imperial_artillery"},
                        {"id": "learn_guard_tactics", "text": "Muhafız Taktiklerini Öğren", "effect": "buff:guard_tactics", "next_scene": "side_mission_imperial_artillery"},
                        {"id": "fight_guard_training", "text": "Muhafız Eğitimiyle Savaş", "combat": True, "enemy": "Guard Trainers", "next_scene": "side_mission_imperial_artillery"},
                        {"id": "study_guard_lore", "text": "Muhafız Lore'unu Öğren", "effect": "item:guard_lore", "next_scene": "side_mission_imperial_artillery"}
                    ]
                },
                {
                    "id": "side_mission_imperial_artillery",
                    "title": "Yan Görev: İmparatorluk Topçusu",
                    "description": "İmparatorluk Topçusuna yardım et ve güçlü destek kazan!",
                    "background": "/static/images/side_mission_imperial_artillery.jpg",
                    "choices": [
                        {"id": "help_imperial_artillery", "text": "İmparatorluk Topçusuna Yardım Et", "effect": "ally:imperial_artillery, gain_xp:4", "next_scene": "side_mission_imperial_tanks"},
                        {"id": "learn_artillery_tactics", "text": "Topçu Taktiklerini Öğren", "effect": "buff:artillery_tactics", "next_scene": "side_mission_imperial_tanks"},
                        {"id": "fight_artillery_crew", "text": "Topçu Ekibiyle Savaş", "combat": True, "enemy": "Artillery Crew", "next_scene": "side_mission_imperial_tanks"},
                        {"id": "study_artillery_lore", "text": "Topçu Lore'unu Öğren", "effect": "item:artillery_lore", "next_scene": "side_mission_imperial_tanks"}
                    ]
                },
                {
                    "id": "side_mission_imperial_tanks",
                    "title": "Yan Görev: İmparatorluk Tankları",
                    "description": "İmparatorluk Tanklarına yardım et ve güçlü destek kazan!",
                    "background": "/static/images/side_mission_imperial_tanks.jpg",
                    "choices": [
                        {"id": "help_imperial_tanks", "text": "İmparatorluk Tanklarına Yardım Et", "effect": "ally:imperial_tanks, gain_xp:4", "next_scene": "side_mission_imperial_air"},
                        {"id": "learn_tank_tactics", "text": "Tank Taktiklerini Öğren", "effect": "buff:tank_tactics", "next_scene": "side_mission_imperial_air"},
                        {"id": "fight_tank_crew", "text": "Tank Ekibiyle Savaş", "combat": True, "enemy": "Tank Crew", "next_scene": "side_mission_imperial_air"},
                        {"id": "study_tank_lore", "text": "Tank Lore'unu Öğren", "effect": "item:tank_lore", "next_scene": "side_mission_imperial_air"}
                    ]
                },
                {
                    "id": "side_mission_imperial_air",
                    "title": "Yan Görev: İmparatorluk Hava Desteği",
                    "description": "İmparatorluk Hava Desteğine yardım et ve güçlü destek kazan!",
                    "background": "/static/images/side_mission_imperial_air.jpg",
                    "choices": [
                        {"id": "help_imperial_air", "text": "İmparatorluk Hava Desteğine Yardım Et", "effect": "ally:imperial_air, gain_xp:4", "next_scene": "side_mission_final"},
                        {"id": "learn_air_tactics", "text": "Hava Taktiklerini Öğren", "effect": "buff:air_tactics", "next_scene": "side_mission_final"},
                        {"id": "fight_air_crew", "text": "Hava Ekibiyle Savaş", "combat": True, "enemy": "Air Crew", "next_scene": "side_mission_final"},
                        {"id": "study_air_lore", "text": "Hava Lore'unu Öğren", "effect": "item:air_lore", "next_scene": "side_mission_final"}
                    ]
                },
                {
                    "id": "side_mission_final",
                    "title": "Yan Görev: Son Direniş",
                    "description": "Yan görevlerin son direnişi! Bu sıra tabanlı kombat senin için!",
                    "background": "/static/images/side_mission_final.jpg",
                    "choices": [
                        {"id": "fight_side_mission_boss", "text": "Yan Görev Boss'u ile Savaş", "combat": True, "enemy": "Side Mission Boss", "next_scene": "victory"},
                        {"id": "use_side_tactics", "text": "Yan Görev Taktiklerini Kullan", "effect": "buff:side_power", "combat": True, "enemy": "Side Mission Boss", "next_scene": "victory"},
                        {"id": "call_side_allies", "text": "Yan Görev Müttefiklerini Çağır", "effect": "ally:side_allies", "combat": True, "enemy": "Side Mission Boss", "next_scene": "victory"},
                        {"id": "negotiate_side_boss", "text": "Yan Görev Boss'u ile Müzakere", "effect": "karma:+10", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "betrayal_scene",
                    "title": "İhanetin Ortaya Çıkışı",
                    "description": "Savaşın ortasında bir ihanet ortaya çıktı! Seni arkadan vuran bir müttefik var!",
                    "background": "/static/images/betrayal_scene.jpg",
                    "choices": [
                        {"id": "fight_traitor", "text": "Hainle Savaş", "combat": True, "enemy": "Traitor", "next_scene": "victory"},
                        {"id": "expose_traitor", "text": "Haini Açığa Çıkar", "effect": "buff:expose_bonus", "next_scene": "victory"},
                        {"id": "forgive_traitor", "text": "Haini Affet", "effect": "karma:+10", "next_scene": "victory"},
                        {"id": "use_psychic_truth", "text": "Psi Gücüyle Gerçeği Bul", "effect": "buff:truth_reveal", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "victory",
                    "title": "Zafer",
                    "description": "Orkları püskürttün ve dünyayı kurtardın. İmparator seni onurlandırıyor ve Chapter Master olarak terfi ettiriyor.",
                    "background": "/static/images/warhammer40k_victory.jpg",
                    "choices": []
                },
                {
                    "id": "regroup",
                    "title": "Yeniden Toplanma",
                    "description": "Taktik geri çekilme sonrası güçlerini topladın. Yeni bir plan yapman gerekiyor. Warboss Gorkamorka hala tehdit oluşturuyor.",
                    "background": "/static/images/warhammer40k_battlefield.jpg",
                    "choices": [
                        {"id": "plan_ambush", "text": "Pusu Planla", "effect": "buff:ambush_bonus", "next_scene": "warboss_confrontation"},
                        {"id": "call_reinforcements", "text": "Takviye Çağır", "effect": "ally:space_marines", "next_scene": "warboss_confrontation"},
                        {"id": "direct_assault", "text": "Doğrudan Saldır", "combat": True, "enemy": "Ork Elite", "next_scene": "warboss_confrontation"}
                    ]
                },
                {
                    "id": "warboss_confrontation",
                    "title": "Warboss ile Yüzleşme",
                    "description": "Warboss Gorkamorka karşında! Bu savaş senin için!",
                    "background": "/static/images/warhammer40k_ork_horde.jpg",
                    "choices": [
                        {"id": "fight_warboss", "text": "Warboss ile Savaş", "combat": True, "enemy": "Warboss Gorkamorka", "next_scene": "victory"},
                        {"id": "use_psychic", "text": "Psi Gücü Kullan", "effect": "buff:psychic_boost", "combat": True, "enemy": "Warboss Gorkamorka", "next_scene": "victory"},
                        {"id": "tactical_retreat", "text": "Taktik Geri Çekilme", "next_scene": "regroup"}
                    ]
                }
            ]
        }
        
        self.campaigns["hive_city_defense"] = hive_campaign
        self.campaigns["forest_mystery"] = forest_mystery_campaign
        # Ejderha Avcısının Yolu kampanyası ekle
        dragon_hunt_campaign = {
            "id": "dragon_hunt",
            "name": "🐉 Ejderha Avcısının Yolu",
            "type": "fantasy",
            "description": "Ejderhaların yaşadığı tehlikeli dünyada kapsamlı bir macera. Plot twist'ler, ihanetler ve rastgele olaylar seni bekliyor. Seçimlerinin sonuçlarını ancak sonunda öğreneceksin.",
            "scenes": [
                {
                    "id": "intro",
                    "title": "Ejderha Avcısı Başlangıcı",
                    "description": "Ejderha avcısı olarak görevlendirildin. Krallığı tehdit eden ejderhaları avlamak için yola çıkıyorsun.",
                    "background": "/static/images/fantasy_forest.jpg",
                    "choices": [
                        {"id": "check_equipment", "text": "Ekipmanı Kontrol Et", "effect": "item:heroic_weapon, gain_xp:3", "next_scene": "dragon_encounter"},
                        {"id": "pray_gods", "text": "Tanrılara Dua Et", "effect": "buff:divine_blessing, gain_xp:2", "next_scene": "dragon_encounter"},
                        {"id": "find_guide", "text": "Rehber Ara", "effect": "ally:experienced_hunter", "next_scene": "dragon_encounter"},
                        {"id": "study_dragons", "text": "Ejderhaları Araştır", "effect": "gain_xp:2", "next_scene": "dragon_encounter"}
                    ]
                },
                {
                    "id": "dragon_encounter",
                    "title": "İlk Ejderha Karşılaşması",
                    "description": "İlk ejderhayla karşılaştın. Bu savaş senin için!",
                    "background": "/static/images/fantasy_dragon.jpg",
                    "choices": [
                        {"id": "fight_dragon", "text": "Ejderhayla Savaş", "combat": True, "enemy": "Young Dragon", "next_scene": "ancient_temple"},
                        {"id": "use_magic", "text": "Sihir Kullan", "effect": "buff:magic_power", "combat": True, "enemy": "Young Dragon", "next_scene": "ancient_temple"},
                        {"id": "negotiate_dragon", "text": "Ejderhayla Konuş", "effect": "karma:+5", "next_scene": "ancient_temple"},
                        {"id": "escape_dragon", "text": "Kaç", "next_scene": "ancient_temple"}
                    ]
                },
                {
                    "id": "ancient_temple",
                    "title": "Antik Tapınak",
                    "description": "Antik tapınağa ulaştın. Burada ejderhaların sırrını öğrenebilirsin.",
                    "background": "/static/images/fantasy_temple.jpg",
                    "choices": [
                        {"id": "explore_temple", "text": "Tapınağı Keşfet", "effect": "item:ancient_knowledge, gain_xp:3", "next_scene": "betrayal_scene"},
                        {"id": "pray_temple", "text": "Tapınakta Dua Et", "effect": "buff:temple_blessing", "next_scene": "betrayal_scene"},
                        {"id": "find_artifact", "text": "Artefakt Ara", "effect": "item:dragon_artifact", "next_scene": "betrayal_scene"},
                        {"id": "study_inscriptions", "text": "Yazıtları Oku", "effect": "gain_xp:2", "next_scene": "betrayal_scene"}
                    ]
                },
                {
                    "id": "betrayal_scene",
                    "title": "Rehberin İhaneti",
                    "description": "Güvendiğin rehber aslında ejderhaların hizmetkârıydı! Seni tuzağa düşürmek istiyor.",
                    "background": "/static/images/fantasy_betrayal.jpg",
                    "choices": [
                        {"id": "fight_betrayer", "text": "Hainle Savaş", "combat": True, "enemy": "Traitor Guide", "next_scene": "final_battle"},
                        {"id": "use_artifact", "text": "Artefaktı Kullan", "effect": "buff:artifact_power", "combat": True, "enemy": "Traitor Guide", "next_scene": "final_battle"},
                        {"id": "call_allies", "text": "Müttefikleri Çağır", "effect": "ally:loyal_companions", "next_scene": "final_battle"},
                        {"id": "escape_betrayal", "text": "Kaç", "next_scene": "final_battle"}
                    ]
                },
                {
                    "id": "dragon_hunter_ancient_ruins",
                    "title": "Ejderha Avcısı Antik Harabeler",
                    "description": "Ejderha avcılarının antik harabelerine ulaştın. Burada kadim bilgiler var!",
                    "background": "/static/images/dragon_hunter_ancient_ruins.jpg",
                    "choices": [
                        {"id": "explore_ancient_ruins", "text": "Antik Harabeleri Keşfet", "effect": "item:ancient_knowledge, gain_xp:5", "next_scene": "dragon_hunter_crystal_cave"},
                        {"id": "fight_ruin_guardian", "text": "Harabe Bekçisi ile Savaş", "combat": True, "enemy": "Ruin Guardian", "next_scene": "dragon_hunter_crystal_cave"},
                        {"id": "study_ancient_lore", "text": "Antik Lore'u Öğren", "effect": "buff:ancient_lore", "next_scene": "dragon_hunter_crystal_cave"},
                        {"id": "collect_ancient_artifacts", "text": "Antik Artefaktları Topla", "effect": "item:ancient_artifacts", "next_scene": "dragon_hunter_crystal_cave"}
                    ]
                },
                {
                    "id": "dragon_hunter_crystal_cave",
                    "title": "Ejderha Avcısı Kristal Mağara",
                    "description": "Ejderha avcılarının kristal mağarasına ulaştın. Burada güçlü kristaller var!",
                    "background": "/static/images/dragon_hunter_crystal_cave.jpg",
                    "choices": [
                        {"id": "mine_crystals", "text": "Kristalleri Kaz", "effect": "item:dragon_crystals, gain_xp:4", "next_scene": "dragon_hunter_volcanic_forge"},
                        {"id": "fight_crystal_golem", "text": "Kristal Golem ile Savaş", "combat": True, "enemy": "Crystal Golem", "next_scene": "dragon_hunter_volcanic_forge"},
                        {"id": "study_crystal_lore", "text": "Kristal Lore'unu Öğren", "effect": "buff:crystal_lore", "next_scene": "dragon_hunter_volcanic_forge"},
                        {"id": "craft_crystal_weapon", "text": "Kristal Silah Yap", "effect": "item:crystal_weapon", "next_scene": "dragon_hunter_volcanic_forge"}
                    ]
                },
                {
                    "id": "dragon_hunter_volcanic_forge",
                    "title": "Ejderha Avcısı Volkanik Forge",
                    "description": "Ejderha avcılarının volkanik forge'una ulaştın. Burada güçlü silahlar dövülüyor!",
                    "background": "/static/images/dragon_hunter_volcanic_forge.jpg",
                    "choices": [
                        {"id": "forge_dragon_weapon", "text": "Ejderha Silahı Döv", "effect": "item:forged_dragon_weapon, gain_xp:5", "next_scene": "dragon_hunter_ice_citadel"},
                        {"id": "fight_forge_master", "text": "Forge Ustası ile Savaş", "combat": True, "enemy": "Forge Master", "next_scene": "dragon_hunter_ice_citadel"},
                        {"id": "learn_forge_lore", "text": "Forge Lore'unu Öğren", "effect": "buff:forge_lore", "next_scene": "dragon_hunter_ice_citadel"},
                        {"id": "study_forge_secrets", "text": "Forge Sırlarını İncele", "effect": "item:forge_secrets", "next_scene": "dragon_hunter_ice_citadel"}
                    ]
                },
                {
                    "id": "dragon_hunter_ice_citadel",
                    "title": "Ejderha Avcısı Buz Kalesi",
                    "description": "Ejderha avcılarının buz kalesine ulaştın. Burada buz ejderhaları var!",
                    "background": "/static/images/dragon_hunter_ice_citadel.jpg",
                    "choices": [
                        {"id": "fight_ice_dragon", "text": "Buz Ejderhası ile Savaş", "combat": True, "enemy": "Ice Dragon", "next_scene": "dragon_hunter_desert_oasis"},
                        {"id": "learn_ice_magic", "text": "Buz Büyüsünü Öğren", "effect": "buff:ice_magic, gain_xp:4", "next_scene": "dragon_hunter_desert_oasis"},
                        {"id": "study_ice_lore", "text": "Buz Lore'unu Öğren", "effect": "buff:ice_lore", "next_scene": "dragon_hunter_desert_oasis"},
                        {"id": "collect_ice_artifacts", "text": "Buz Artefaktlarını Topla", "effect": "item:ice_artifacts", "next_scene": "dragon_hunter_desert_oasis"}
                    ]
                },
                {
                    "id": "dragon_hunter_desert_oasis",
                    "title": "Ejderha Avcısı Çöl Vahası",
                    "description": "Ejderha avcılarının çöl vahasına ulaştın. Burada kum ejderhaları var!",
                    "background": "/static/images/dragon_hunter_desert_oasis.jpg",
                    "choices": [
                        {"id": "fight_sand_dragon", "text": "Kum Ejderhası ile Savaş", "combat": True, "enemy": "Sand Dragon", "next_scene": "dragon_hunter_underwater_city"},
                        {"id": "learn_sand_magic", "text": "Kum Büyüsünü Öğren", "effect": "buff:sand_magic, gain_xp:4", "next_scene": "dragon_hunter_underwater_city"},
                        {"id": "study_desert_lore", "text": "Çöl Lore'unu Öğren", "effect": "buff:desert_lore", "next_scene": "dragon_hunter_underwater_city"},
                        {"id": "collect_desert_artifacts", "text": "Çöl Artefaktlarını Topla", "effect": "item:desert_artifacts", "next_scene": "dragon_hunter_underwater_city"}
                    ]
                },
                {
                    "id": "dragon_hunter_underwater_city",
                    "title": "Ejderha Avcısı Sualtı Şehri",
                    "description": "Ejderha avcılarının sualtı şehrine ulaştın. Burada su ejderhaları var!",
                    "background": "/static/images/dragon_hunter_underwater_city.jpg",
                    "choices": [
                        {"id": "fight_water_dragon", "text": "Su Ejderhası ile Savaş", "combat": True, "enemy": "Water Dragon", "next_scene": "dragon_hunter_sky_fortress"},
                        {"id": "learn_water_magic", "text": "Su Büyüsünü Öğren", "effect": "buff:water_magic, gain_xp:4", "next_scene": "dragon_hunter_sky_fortress"},
                        {"id": "study_underwater_lore", "text": "Sualtı Lore'unu Öğren", "effect": "buff:underwater_lore", "next_scene": "dragon_hunter_sky_fortress"},
                        {"id": "collect_water_artifacts", "text": "Su Artefaktlarını Topla", "effect": "item:water_artifacts", "next_scene": "dragon_hunter_sky_fortress"}
                    ]
                },
                {
                    "id": "dragon_hunter_sky_fortress",
                    "title": "Ejderha Avcısı Gökyüzü Kalesi",
                    "description": "Ejderha avcılarının gökyüzü kalesine ulaştın. Burada rüzgar ejderhaları var!",
                    "background": "/static/images/dragon_hunter_sky_fortress.jpg",
                    "choices": [
                        {"id": "fight_wind_dragon", "text": "Rüzgar Ejderhası ile Savaş", "combat": True, "enemy": "Wind Dragon", "next_scene": "dragon_hunter_lightning_tower"},
                        {"id": "learn_wind_magic", "text": "Rüzgar Büyüsünü Öğren", "effect": "buff:wind_magic, gain_xp:4", "next_scene": "dragon_hunter_lightning_tower"},
                        {"id": "study_sky_lore", "text": "Gökyüzü Lore'unu Öğren", "effect": "buff:sky_lore", "next_scene": "dragon_hunter_lightning_tower"},
                        {"id": "collect_sky_artifacts", "text": "Gökyüzü Artefaktlarını Topla", "effect": "item:sky_artifacts", "next_scene": "dragon_hunter_lightning_tower"}
                    ]
                },
                {
                    "id": "dragon_hunter_lightning_tower",
                    "title": "Ejderha Avcısı Şimşek Kulesi",
                    "description": "Ejderha avcılarının şimşek kulesine ulaştın. Burada şimşek ejderhaları var!",
                    "background": "/static/images/dragon_hunter_lightning_tower.jpg",
                    "choices": [
                        {"id": "fight_lightning_dragon", "text": "Şimşek Ejderhası ile Savaş", "combat": True, "enemy": "Lightning Dragon", "next_scene": "dragon_hunter_poison_swamp"},
                        {"id": "learn_lightning_magic", "text": "Şimşek Büyüsünü Öğren", "effect": "buff:lightning_magic, gain_xp:4", "next_scene": "dragon_hunter_poison_swamp"},
                        {"id": "study_lightning_lore", "text": "Şimşek Lore'unu Öğren", "effect": "buff:lightning_lore", "next_scene": "dragon_hunter_poison_swamp"},
                        {"id": "collect_lightning_artifacts", "text": "Şimşek Artefaktlarını Topla", "effect": "item:lightning_artifacts", "next_scene": "dragon_hunter_poison_swamp"}
                    ]
                },
                {
                    "id": "dragon_hunter_poison_swamp",
                    "title": "Ejderha Avcısı Zehir Bataklığı",
                    "description": "Ejderha avcılarının zehir bataklığına ulaştın. Burada zehir ejderhaları var!",
                    "background": "/static/images/dragon_hunter_poison_swamp.jpg",
                    "choices": [
                        {"id": "fight_poison_dragon", "text": "Zehir Ejderhası ile Savaş", "combat": True, "enemy": "Poison Dragon", "next_scene": "dragon_hunter_ghost_manor"},
                        {"id": "learn_poison_magic", "text": "Zehir Büyüsünü Öğren", "effect": "buff:poison_magic, gain_xp:4", "next_scene": "dragon_hunter_ghost_manor"},
                        {"id": "study_poison_lore", "text": "Zehir Lore'unu Öğren", "effect": "buff:poison_lore", "next_scene": "dragon_hunter_ghost_manor"},
                        {"id": "collect_poison_artifacts", "text": "Zehir Artefaktlarını Topla", "effect": "item:poison_artifacts", "next_scene": "dragon_hunter_ghost_manor"}
                    ]
                },
                {
                    "id": "dragon_hunter_ghost_manor",
                    "title": "Ejderha Avcısı Hayalet Malikane",
                    "description": "Ejderha avcılarının hayalet malikanesine ulaştın. Burada hayalet ejderhaları var!",
                    "background": "/static/images/dragon_hunter_ghost_manor.jpg",
                    "choices": [
                        {"id": "fight_ghost_dragon", "text": "Hayalet Ejderhası ile Savaş", "combat": True, "enemy": "Ghost Dragon", "next_scene": "dragon_hunter_chaos_realm"},
                        {"id": "learn_ghost_magic", "text": "Hayalet Büyüsünü Öğren", "effect": "buff:ghost_magic, gain_xp:4", "next_scene": "dragon_hunter_chaos_realm"},
                        {"id": "study_ghost_lore", "text": "Hayalet Lore'unu Öğren", "effect": "buff:ghost_lore", "next_scene": "dragon_hunter_chaos_realm"},
                        {"id": "collect_ghost_artifacts", "text": "Hayalet Artefaktlarını Topla", "effect": "item:ghost_artifacts", "next_scene": "dragon_hunter_chaos_realm"}
                    ]
                },
                {
                    "id": "dragon_hunter_chaos_realm",
                    "title": "Ejderha Avcısı Kaos Alemi",
                    "description": "Ejderha avcılarının kaos alemine ulaştın. Burada kaos ejderhaları var!",
                    "background": "/static/images/dragon_hunter_chaos_realm.jpg",
                    "choices": [
                        {"id": "fight_chaos_dragon", "text": "Kaos Ejderhası ile Savaş", "combat": True, "enemy": "Chaos Dragon", "next_scene": "dragon_hunter_order_realm"},
                        {"id": "learn_chaos_magic", "text": "Kaos Büyüsünü Öğren", "effect": "buff:chaos_magic, gain_xp:4", "next_scene": "dragon_hunter_order_realm"},
                        {"id": "study_chaos_lore", "text": "Kaos Lore'unu Öğren", "effect": "buff:chaos_lore", "next_scene": "dragon_hunter_order_realm"},
                        {"id": "collect_chaos_artifacts", "text": "Kaos Artefaktlarını Topla", "effect": "item:chaos_artifacts", "next_scene": "dragon_hunter_order_realm"}
                    ]
                },
                {
                    "id": "dragon_hunter_order_realm",
                    "title": "Ejderha Avcısı Düzen Alemi",
                    "description": "Ejderha avcılarının düzen alemine ulaştın. Burada düzen ejderhaları var!",
                    "background": "/static/images/dragon_hunter_order_realm.jpg",
                    "choices": [
                        {"id": "fight_order_dragon", "text": "Düzen Ejderhası ile Savaş", "combat": True, "enemy": "Order Dragon", "next_scene": "dragon_hunter_time_temple"},
                        {"id": "learn_order_magic", "text": "Düzen Büyüsünü Öğren", "effect": "buff:order_magic, gain_xp:4", "next_scene": "dragon_hunter_time_temple"},
                        {"id": "study_order_lore", "text": "Düzen Lore'unu Öğren", "effect": "buff:order_lore", "next_scene": "dragon_hunter_time_temple"},
                        {"id": "collect_order_artifacts", "text": "Düzen Artefaktlarını Topla", "effect": "item:order_artifacts", "next_scene": "dragon_hunter_time_temple"}
                    ]
                },
                {
                    "id": "dragon_hunter_time_temple",
                    "title": "Ejderha Avcısı Zaman Tapınağı",
                    "description": "Ejderha avcılarının zaman tapınağına ulaştın. Burada zaman ejderhaları var!",
                    "background": "/static/images/dragon_hunter_time_temple.jpg",
                    "choices": [
                        {"id": "fight_time_dragon", "text": "Zaman Ejderhası ile Savaş", "combat": True, "enemy": "Time Dragon", "next_scene": "dragon_hunter_space_station"},
                        {"id": "learn_time_magic", "text": "Zaman Büyüsünü Öğren", "effect": "buff:time_magic, gain_xp:4", "next_scene": "dragon_hunter_space_station"},
                        {"id": "study_time_lore", "text": "Zaman Lore'unu Öğren", "effect": "buff:time_lore", "next_scene": "dragon_hunter_space_station"},
                        {"id": "collect_time_artifacts", "text": "Zaman Artefaktlarını Topla", "effect": "item:time_artifacts", "next_scene": "dragon_hunter_space_station"}
                    ]
                },
                {
                    "id": "dragon_hunter_space_station",
                    "title": "Ejderha Avcısı Uzay İstasyonu",
                    "description": "Ejderha avcılarının uzay istasyonuna ulaştın. Burada uzay ejderhaları var!",
                    "background": "/static/images/dragon_hunter_space_station.jpg",
                    "choices": [
                        {"id": "fight_space_dragon", "text": "Uzay Ejderhası ile Savaş", "combat": True, "enemy": "Space Dragon", "next_scene": "dragon_hunter_quantum_realm"},
                        {"id": "learn_space_magic", "text": "Uzay Büyüsünü Öğren", "effect": "buff:space_magic, gain_xp:4", "next_scene": "dragon_hunter_quantum_realm"},
                        {"id": "study_space_lore", "text": "Uzay Lore'unu Öğren", "effect": "buff:space_lore", "next_scene": "dragon_hunter_quantum_realm"},
                        {"id": "collect_space_artifacts", "text": "Uzay Artefaktlarını Topla", "effect": "item:space_artifacts", "next_scene": "dragon_hunter_quantum_realm"}
                    ]
                },
                {
                    "id": "dragon_hunter_quantum_realm",
                    "title": "Ejderha Avcısı Kuantum Alemi",
                    "description": "Ejderha avcılarının kuantum alemine ulaştın. Burada kuantum ejderhaları var!",
                    "background": "/static/images/dragon_hunter_quantum_realm.jpg",
                    "choices": [
                        {"id": "fight_quantum_dragon", "text": "Kuantum Ejderhası ile Savaş", "combat": True, "enemy": "Quantum Dragon", "next_scene": "final_battle"},
                        {"id": "learn_quantum_magic", "text": "Kuantum Büyüsünü Öğren", "effect": "buff:quantum_magic, gain_xp:4", "next_scene": "final_battle"},
                        {"id": "study_quantum_lore", "text": "Kuantum Lore'unu Öğren", "effect": "buff:quantum_lore", "next_scene": "final_battle"},
                        {"id": "collect_quantum_artifacts", "text": "Kuantum Artefaktlarını Topla", "effect": "item:quantum_artifacts", "next_scene": "final_battle"}
                    ]
                },
                {
                    "id": "final_battle",
                    "title": "Son Savaş",
                    "description": "Ejderha kralıyla son savaş! Krallığın kaderi senin ellerinde!",
                    "background": "/static/images/fantasy_battle.jpg",
                    "choices": [
                        {"id": "fight_king", "text": "Ejderha Kralıyla Savaş", "combat": True, "enemy": "Dragon King", "next_scene": "victory"},
                        {"id": "use_legendary_weapon", "text": "Efsanevi Silahı Kullan", "effect": "buff:legendary_power", "combat": True, "enemy": "Dragon King", "next_scene": "victory"},
                        {"id": "sacrifice_power", "text": "Gücünü Feda Et", "effect": "karma:+10", "next_scene": "victory"},
                        {"id": "call_divine", "text": "Tanrısal Gücü Çağır", "effect": "ally:divine_intervention", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "victory",
                    "title": "Zafer",
                    "description": "Ejderha kralını yendin ve krallığı kurtardın. Halk seni kahraman olarak görüyor.",
                    "background": "/static/images/fantasy_victory.jpg",
                    "choices": []
                }
            ]
        }
        
        # Cyberpunk Şehrinin Gizli Sırları kampanyası ekle
        cyberpunk_secrets_campaign = {
            "id": "cyberpunk_secrets",
            "name": "🌃 Cyberpunk Şehrinin Gizli Sırları",
            "type": "cyberpunk",
            "description": "Neon ışıkları altında, mega şirketlerin kontrol ettiği bir şehirde yaşıyorsun. Yapay zeka, sibernetik implantlar ve gizli komplolar her yerde. Seçimlerin şehrin kaderini belirleyecek.",
            "scenes": [
                {
                    "id": "intro",
                    "title": "Neon Şehrinde Uyanış",
                    "description": "Cyberpunk şehrinde uyandın. Mega şirketler şehri kontrol ediyor ve sen, seçilmiş hacker, bu sistemi değiştirmek için buradasın.",
                    "background": "/static/images/cyberpunk_city.jpg",
                    "choices": [
                        {"id": "check_implants", "text": "İmplantları Kontrol Et", "effect": "item:cyber_weapon, gain_xp:3", "next_scene": "ai_warning"},
                        {"id": "hack_system", "text": "Sistemi Hack Et", "effect": "buff:stealth_mode, gain_xp:2", "next_scene": "ai_warning"},
                        {"id": "find_hackers", "text": "Hacker'ları Ara", "effect": "ally:underground_hackers", "next_scene": "ai_warning"},
                        {"id": "study_corporations", "text": "Şirketleri Araştır", "effect": "gain_xp:2", "next_scene": "ai_warning"}
                    ]
                },
                {
                    "id": "ai_warning",
                    "title": "AI Uyarısı",
                    "description": "Yapay zeka seni uyarıyor. Mega şirketlerin gizli planlarını ortaya çıkarman gerekiyor.",
                    "background": "/static/images/cyberpunk_corporate.jpg",
                    "choices": [
                        {"id": "trust_ai", "text": "AI'ya Güven", "effect": "ally:ai_assistant", "next_scene": "corporate_tower"},
                        {"id": "question_ai", "text": "AI'yı Sorgula", "effect": "gain_xp:2", "next_scene": "corporate_tower"},
                        {"id": "ignore_ai", "text": "AI'yı Görmezden Gel", "next_scene": "corporate_tower"},
                        {"id": "hack_ai", "text": "AI'yı Hack Et", "effect": "buff:ai_control", "next_scene": "corporate_tower"}
                    ]
                },
                {
                    "id": "corporate_tower",
                    "title": "Şirket Kulesi",
                    "description": "Mega şirketin kulesine sızdın. CEO'nun gizli planlarını öğrenmek için buradayısın.",
                    "background": "/static/images/cyberpunk_corporate.jpg",
                    "choices": [
                        {"id": "hack_mainframe", "text": "Ana Bilgisayarı Hack Et", "effect": "item:corporate_data, gain_xp:3", "next_scene": "ai_lab"},
                        {"id": "stealth_approach", "text": "Gizlice Yaklaş", "effect": "buff:stealth_enhanced", "next_scene": "ai_lab"},
                        {"id": "fight_guards", "text": "Muhafızlarla Savaş", "combat": True, "enemy": "Corporate Guards", "next_scene": "ai_lab"},
                        {"id": "find_secrets", "text": "Gizli Bilgileri Ara", "effect": "item:secret_files", "next_scene": "ai_lab"}
                    ]
                },
                {
                    "id": "ai_lab",
                    "title": "AI Laboratuvarı",
                    "description": "Yapay zeka laboratuvarına ulaştın. AI'nın gerçek planını öğrenmek için buradayısın.",
                    "background": "/static/images/cyberpunk_ai_lab.jpg",
                    "choices": [
                        {"id": "confront_ai", "text": "AI ile Yüzleş", "effect": "gain_xp:3", "next_scene": "betrayal_scene"},
                        {"id": "hack_ai_system", "text": "AI Sistemini Hack Et", "effect": "buff:ai_control", "next_scene": "betrayal_scene"},
                        {"id": "negotiate_ai", "text": "AI ile Müzakere Et", "effect": "karma:+5", "next_scene": "betrayal_scene"},
                        {"id": "destroy_ai", "text": "AI'yı Yok Et", "effect": "karma:-5", "next_scene": "betrayal_scene"}
                    ]
                },
                {
                    "id": "betrayal_scene",
                    "title": "AI'nın İhaneti",
                    "description": "AI aslında mega şirketlerin hizmetkârıydı! Seni tuzağa düşürmek istiyor.",
                    "background": "/static/images/cyberpunk_betrayal.jpg",
                    "choices": [
                        {"id": "fight_ai", "text": "AI ile Savaş", "combat": True, "enemy": "Rogue AI", "next_scene": "final_battle"},
                        {"id": "use_cyber_weapon", "text": "Siber Silahı Kullan", "effect": "buff:cyber_power", "combat": True, "enemy": "Rogue AI", "next_scene": "final_battle"},
                        {"id": "call_hackers", "text": "Hacker'ları Çağır", "effect": "ally:hacker_network", "next_scene": "final_battle"},
                        {"id": "escape_betrayal", "text": "Kaç", "next_scene": "final_battle"}
                    ]
                },
                {
                    "id": "final_battle",
                    "title": "Son Savaş",
                    "description": "Mega şirketlerin kontrol sistemini yok etmek için son savaş! Şehrin kaderi senin ellerinde!",
                    "background": "/static/images/cyberpunk_battle.jpg",
                    "choices": [
                        {"id": "destroy_system", "text": "Sistemi Yok Et", "combat": True, "enemy": "Corporate AI", "next_scene": "victory"},
                        {"id": "hack_final_system", "text": "Son Sistemi Hack Et", "effect": "buff:ultimate_hack", "combat": True, "enemy": "Corporate AI", "next_scene": "victory"},
                        {"id": "sacrifice_cyber", "text": "Sibernetik Gücünü Feda Et", "effect": "karma:+10", "next_scene": "victory"},
                        {"id": "call_revolution", "text": "Devrimi Çağır", "effect": "ally:cyber_revolution", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "corporate_headquarters",
                    "title": "Şirket Merkezi",
                    "description": "Mega şirketin ana merkezine ulaştın. Burada CEO'nun gizli planlarını öğrenebilirsin!",
                    "background": "/static/images/corporate_hq.jpg",
                    "choices": [
                        {"id": "hack_headquarters", "text": "Merkezi Hack Et", "effect": "item:corporate_secrets, gain_xp:4", "next_scene": "corporate_ai_boss"},
                        {"id": "stealth_approach", "text": "Gizlice Yaklaş", "effect": "buff:stealth_bonus", "next_scene": "corporate_ai_boss"},
                        {"id": "fight_corporate_guards", "text": "Şirket Muhafızlarıyla Savaş", "combat": True, "enemy": "Corporate Guards", "next_scene": "corporate_ai_boss"},
                        {"id": "call_hacker_allies", "text": "Hacker Müttefiklerini Çağır", "effect": "ally:hacker_network", "next_scene": "corporate_ai_boss"}
                    ]
                },
                {
                    "id": "corporate_ai_boss",
                    "title": "Şirket AI Boss Savaşı",
                    "description": "Mega şirketin en güçlü AI sistemi karşında! Bu sıra tabanlı kombat senin için!",
                    "background": "/static/images/corporate_ai_boss.jpg",
                    "choices": [
                        {"id": "fight_corporate_ai", "text": "Şirket AI ile Savaş", "combat": True, "enemy": "Corporate AI Boss", "next_scene": "cyber_revolution"},
                        {"id": "hack_corporate_ai", "text": "Şirket AI'yı Hack Et", "effect": "buff:ai_control", "combat": True, "enemy": "Corporate AI Boss", "next_scene": "cyber_revolution"},
                        {"id": "negotiate_corporate_ai", "text": "Şirket AI ile Müzakere", "effect": "karma:+10", "next_scene": "cyber_revolution"},
                        {"id": "call_ai_revolution", "text": "AI Devrimini Çağır", "effect": "ally:ai_revolution", "next_scene": "cyber_revolution"}
                    ]
                },
                {
                    "id": "cyber_revolution",
                    "title": "Siber Devrim",
                    "description": "Şehirde siber devrim başladı! Halk ayaklanıyor ve sen bu devrimin lideri olabilirsin!",
                    "background": "/static/images/cyber_revolution.jpg",
                    "choices": [
                        {"id": "lead_revolution", "text": "Devrime Liderlik Et", "effect": "ally:revolution_army, gain_xp:5", "next_scene": "final_battle"},
                        {"id": "negotiate_peace", "text": "Barış Müzakere Et", "effect": "karma:+15", "next_scene": "final_battle"},
                        {"id": "fight_revolution", "text": "Devrimle Savaş", "combat": True, "enemy": "Revolution Forces", "next_scene": "final_battle"},
                        {"id": "call_mediators", "text": "Arabulucuları Çağır", "effect": "ally:peace_mediators", "next_scene": "final_battle"}
                    ]
                },
                {
                    "id": "side_mission_underground_network",
                    "title": "Yan Görev: Yeraltı Ağı",
                    "description": "Şehrin yeraltı hacker ağını keşfettin. Bu ağ çok güçlü!",
                    "background": "/static/images/underground_network.jpg",
                    "choices": [
                        {"id": "join_network", "text": "Ağa Katıl", "effect": "ally:underground_network, gain_xp:3", "next_scene": "side_mission_cyber_market"},
                        {"id": "hack_network", "text": "Ağı Hack Et", "effect": "buff:network_control", "next_scene": "side_mission_cyber_market"},
                        {"id": "fight_network_guards", "text": "Ağ Muhafızlarıyla Savaş", "combat": True, "enemy": "Network Guards", "next_scene": "side_mission_cyber_market"},
                        {"id": "negotiate_network", "text": "Ağla Müzakere", "effect": "karma:+5", "next_scene": "side_mission_cyber_market"}
                    ]
                },
                {
                    "id": "side_mission_cyber_market",
                    "title": "Yan Görev: Siber Pazar",
                    "description": "Şehrin gizli siber pazarını keşfettin. Burada her şey satılıyor!",
                    "background": "/static/images/cyber_market.jpg",
                    "choices": [
                        {"id": "buy_cyber_weapons", "text": "Siber Silahlar Satın Al", "effect": "item:cyber_weapons", "next_scene": "side_mission_cyber_lab"},
                        {"id": "sell_information", "text": "Bilgi Sat", "effect": "gain_xp:4", "next_scene": "side_mission_cyber_lab"},
                        {"id": "fight_market_guards", "text": "Pazar Muhafızlarıyla Savaş", "combat": True, "enemy": "Market Guards", "next_scene": "side_mission_cyber_lab"},
                        {"id": "negotiate_market", "text": "Pazarla Müzakere", "effect": "karma:+5", "next_scene": "side_mission_cyber_lab"}
                    ]
                },
                {
                    "id": "side_mission_cyber_lab",
                    "title": "Yan Görev: Siber Laboratuvar",
                    "description": "Şehrin gizli siber laboratuvarını keşfettin. Burada gelişmiş teknolojiler var!",
                    "background": "/static/images/cyber_lab.jpg",
                    "choices": [
                        {"id": "steal_technology", "text": "Teknolojileri Çal", "effect": "item:advanced_tech", "next_scene": "side_mission_cyber_prison"},
                        {"id": "study_technology", "text": "Teknolojileri İncele", "effect": "item:tech_knowledge", "next_scene": "side_mission_cyber_prison"},
                        {"id": "fight_lab_guards", "text": "Lab Muhafızlarıyla Savaş", "combat": True, "enemy": "Lab Guards", "next_scene": "side_mission_cyber_prison"},
                        {"id": "hack_lab_systems", "text": "Lab Sistemlerini Hack Et", "effect": "buff:lab_control", "next_scene": "side_mission_cyber_prison"}
                    ]
                },
                {
                    "id": "side_mission_cyber_prison",
                    "title": "Yan Görev: Siber Hapishane",
                    "description": "Şehrin gizli siber hapishanesini keşfettin. Burada mahkumlar var!",
                    "background": "/static/images/cyber_prison.jpg",
                    "choices": [
                        {"id": "free_prisoners", "text": "Mahkumları Serbest Bırak", "effect": "ally:freed_prisoners, gain_xp:4", "next_scene": "side_mission_final"},
                        {"id": "interrogate_prisoners", "text": "Mahkumları Sorgula", "effect": "item:prisoner_intel", "next_scene": "side_mission_final"},
                        {"id": "fight_prison_guards", "text": "Hapishane Muhafızlarıyla Savaş", "combat": True, "enemy": "Prison Guards", "next_scene": "side_mission_final"},
                        {"id": "negotiate_prisoners", "text": "Mahkumlarla Müzakere", "effect": "karma:+5", "next_scene": "side_mission_final"}
                    ]
                },
                {
                    "id": "side_mission_final",
                    "title": "Yan Görev: Son Direniş",
                    "description": "Şehrin son direniş noktası. Bu yeri ele geçirmek çok önemli!",
                    "background": "/static/images/final_resistance.jpg",
                    "choices": [
                        {"id": "attack_resistance", "text": "Direnişe Saldır", "combat": True, "enemy": "Final Resistance", "next_scene": "victory"},
                        {"id": "hack_resistance", "text": "Direnişi Hack Et", "effect": "buff:resistance_control", "next_scene": "victory"},
                        {"id": "negotiate_resistance", "text": "Direnişle Müzakere", "effect": "karma:+5", "next_scene": "victory"},
                        {"id": "call_allies", "text": "Müttefikleri Çağır", "effect": "ally:final_allies", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "cyber_netrunner_guild",
                    "title": "Siber Netrunner Loncası",
                    "description": "Siber Netrunner Loncası'nın merkezine ulaştın. Burada güçlü netrunner'lar var!",
                    "background": "/static/images/cyber_netrunner_guild.jpg",
                    "choices": [
                        {"id": "join_netrunner_guild", "text": "Loncaya Katıl", "effect": "ally:netrunner_guild, gain_xp:5", "next_scene": "cyber_hacker_meeting"},
                        {"id": "learn_guild_lore", "text": "Lonca Lore'unu Öğren", "effect": "buff:guild_lore", "next_scene": "cyber_hacker_meeting"},
                        {"id": "fight_guild_master", "text": "Lonca Ustası ile Savaş", "combat": True, "enemy": "Guild Master", "next_scene": "cyber_hacker_meeting"},
                        {"id": "receive_guild_blessing", "text": "Lonca Kutsaması Al", "effect": "buff:guild_blessing", "next_scene": "cyber_hacker_meeting"}
                    ]
                },
                {
                    "id": "cyber_hacker_meeting",
                    "title": "Siber Hacker Toplantısı",
                    "description": "Siber hacker'ların gizli toplantısına ulaştın. Burada güçlü hacker'lar var!",
                    "background": "/static/images/cyber_hacker_meeting.jpg",
                    "choices": [
                        {"id": "join_hacker_meeting", "text": "Toplantıya Katıl", "effect": "ally:hacker_group, gain_xp:4", "next_scene": "cyber_cyber_market"},
                        {"id": "learn_hacker_skills", "text": "Hacker Becerilerini Öğren", "effect": "buff:hacker_skills", "next_scene": "cyber_cyber_market"},
                        {"id": "fight_hacker_rival", "text": "Rakip Hacker ile Savaş", "combat": True, "enemy": "Hacker Rival", "next_scene": "cyber_cyber_market"},
                        {"id": "study_hacker_lore", "text": "Hacker Lore'unu Öğren", "effect": "item:hacker_lore", "next_scene": "cyber_cyber_market"}
                    ]
                },
                {
                    "id": "cyber_cyber_market",
                    "title": "Siber Siber Pazar",
                    "description": "Siber pazarında güçlü ekipmanlar satın al!",
                    "background": "/static/images/cyber_cyber_market.jpg",
                    "choices": [
                        {"id": "buy_cyber_equipment", "text": "Siber Ekipman Satın Al", "effect": "item:cyber_equipment", "next_scene": "cyber_cyber_clinic"},
                        {"id": "trade_with_merchants", "text": "Tüccarlarla Ticaret Yap", "effect": "ally:merchants", "next_scene": "cyber_cyber_clinic"},
                        {"id": "fight_market_thugs", "text": "Pazar Haydutları ile Savaş", "combat": True, "enemy": "Market Thugs", "next_scene": "cyber_cyber_clinic"},
                        {"id": "study_market_lore", "text": "Pazar Lore'unu Öğren", "effect": "item:market_lore", "next_scene": "cyber_cyber_clinic"}
                    ]
                },
                {
                    "id": "cyber_cyber_clinic",
                    "title": "Siber Siber Klinik",
                    "description": "Siber klinikte güçlü implantlar taktır!",
                    "background": "/static/images/cyber_cyber_clinic.jpg",
                    "choices": [
                        {"id": "get_cyber_implants", "text": "Siber İmplantlar Tak", "effect": "item:cyber_implants", "next_scene": "cyber_corporate_spy"},
                        {"id": "learn_medical_skills", "text": "Tıbbi Becerileri Öğren", "effect": "buff:medical_skills", "next_scene": "cyber_corporate_spy"},
                        {"id": "fight_clinic_security", "text": "Klinik Güvenliği ile Savaş", "combat": True, "enemy": "Clinic Security", "next_scene": "cyber_corporate_spy"},
                        {"id": "study_medical_lore", "text": "Tıbbi Lore'u Öğren", "effect": "item:medical_lore", "next_scene": "cyber_corporate_spy"}
                    ]
                },
                {
                    "id": "cyber_corporate_spy",
                    "title": "Siber Şirket Casusu",
                    "description": "Siber şirket casusu ile karşılaştın. Bu güçlü casus!",
                    "background": "/static/images/cyber_corporate_spy.jpg",
                    "choices": [
                        {"id": "recruit_corporate_spy", "text": "Casusu İşe Al", "effect": "ally:corporate_spy, gain_xp:5", "next_scene": "cyber_cyber_gang"},
                        {"id": "learn_spy_skills", "text": "Casus Becerilerini Öğren", "effect": "buff:spy_skills", "next_scene": "cyber_cyber_gang"},
                        {"id": "fight_corporate_spy", "text": "Casus ile Savaş", "combat": True, "enemy": "Corporate Spy", "next_scene": "cyber_cyber_gang"},
                        {"id": "study_spy_lore", "text": "Casus Lore'unu Öğren", "effect": "item:spy_lore", "next_scene": "cyber_cyber_gang"}
                    ]
                },
                {
                    "id": "cyber_cyber_gang",
                    "title": "Siber Siber Çete",
                    "description": "Siber çete ile karşılaştın. Bu güçlü çete!",
                    "background": "/static/images/cyber_cyber_gang.jpg",
                    "choices": [
                        {"id": "join_cyber_gang", "text": "Çeteye Katıl", "effect": "ally:cyber_gang, gain_xp:4", "next_scene": "cyber_cyber_arena"},
                        {"id": "learn_gang_skills", "text": "Çete Becerilerini Öğren", "effect": "buff:gang_skills", "next_scene": "cyber_cyber_arena"},
                        {"id": "fight_cyber_gang", "text": "Çete ile Savaş", "combat": True, "enemy": "Cyber Gang", "next_scene": "cyber_cyber_arena"},
                        {"id": "study_gang_lore", "text": "Çete Lore'unu Öğren", "effect": "item:gang_lore", "next_scene": "cyber_cyber_arena"}
                    ]
                },
                {
                    "id": "cyber_cyber_arena",
                    "title": "Siber Siber Arena",
                    "description": "Siber arena'da güçlü dövüşçülerle savaş!",
                    "background": "/static/images/cyber_cyber_arena.jpg",
                    "choices": [
                        {"id": "fight_in_arena", "text": "Arena'da Savaş", "combat": True, "enemy": "Arena Champion", "next_scene": "cyber_cyber_temple"},
                        {"id": "learn_arena_skills", "text": "Arena Becerilerini Öğren", "effect": "buff:arena_skills", "next_scene": "cyber_cyber_temple"},
                        {"id": "bet_on_fights", "text": "Dövüşlere Bahis Koy", "effect": "gain_gold:50", "next_scene": "cyber_cyber_temple"},
                        {"id": "study_arena_lore", "text": "Arena Lore'unu Öğren", "effect": "item:arena_lore", "next_scene": "cyber_cyber_temple"}
                    ]
                },
                {
                    "id": "cyber_cyber_temple",
                    "title": "Siber Siber Tapınak",
                    "description": "Siber tapınakta güçlü rahiplerle karşılaş!",
                    "background": "/static/images/cyber_cyber_temple.jpg",
                    "choices": [
                        {"id": "pray_at_temple", "text": "Tapınakta Dua Et", "effect": "buff:temple_blessing, gain_xp:4", "next_scene": "cyber_cyber_monastery"},
                        {"id": "learn_temple_lore", "text": "Tapınak Lore'unu Öğren", "effect": "buff:temple_lore", "next_scene": "cyber_cyber_monastery"},
                        {"id": "fight_temple_guards", "text": "Tapınak Muhafızları ile Savaş", "combat": True, "enemy": "Temple Guards", "next_scene": "cyber_cyber_monastery"},
                        {"id": "receive_temple_blessing", "text": "Tapınak Kutsaması Al", "effect": "buff:divine_protection", "next_scene": "cyber_cyber_monastery"}
                    ]
                },
                {
                    "id": "cyber_cyber_monastery",
                    "title": "Siber Siber Manastır",
                    "description": "Siber manastırda güçlü keşişlerle karşılaş!",
                    "background": "/static/images/cyber_cyber_monastery.jpg",
                    "choices": [
                        {"id": "meditate_at_monastery", "text": "Manastırda Meditasyon Yap", "effect": "buff:meditation_power, gain_xp:4", "next_scene": "cyber_cyber_library"},
                        {"id": "learn_monastery_lore", "text": "Manastır Lore'unu Öğren", "effect": "buff:monastery_lore", "next_scene": "cyber_cyber_library"},
                        {"id": "fight_monastery_guards", "text": "Manastır Muhafızları ile Savaş", "combat": True, "enemy": "Monastery Guards", "next_scene": "cyber_cyber_library"},
                        {"id": "receive_monastery_blessing", "text": "Manastır Kutsaması Al", "effect": "buff:spiritual_protection", "next_scene": "cyber_cyber_library"}
                    ]
                },
                {
                    "id": "cyber_cyber_library",
                    "title": "Siber Siber Kütüphane",
                    "description": "Siber kütüphanede gizli bilgileri keşfet!",
                    "background": "/static/images/cyber_cyber_library.jpg",
                    "choices": [
                        {"id": "study_cyber_lore", "text": "Siber Lore'u Öğren", "effect": "buff:cyber_lore, gain_xp:4", "next_scene": "cyber_cyber_laboratory"},
                        {"id": "find_secret_tomes", "text": "Gizli Tomarları Bul", "effect": "item:secret_tomes", "next_scene": "cyber_cyber_laboratory"},
                        {"id": "fight_library_guardian", "text": "Kütüphane Bekçisi ile Savaş", "combat": True, "enemy": "Library Guardian", "next_scene": "cyber_cyber_laboratory"},
                        {"id": "learn_library_lore", "text": "Kütüphane Lore'unu Öğren", "effect": "item:library_lore", "next_scene": "cyber_cyber_laboratory"}
                    ]
                },
                {
                    "id": "cyber_cyber_laboratory",
                    "title": "Siber Siber Laboratuvar",
                    "description": "Siber laboratuvarında gizli deneyleri keşfet!",
                    "background": "/static/images/cyber_cyber_laboratory.jpg",
                    "choices": [
                        {"id": "experiment_with_cybernetics", "text": "Sibernetik ile Deney Yap", "effect": "buff:cybernetics_knowledge, gain_xp:4", "next_scene": "cyber_cyber_prison"},
                        {"id": "steal_lab_data", "text": "Laboratuvar Verilerini Çal", "effect": "item:lab_data", "next_scene": "cyber_cyber_prison"},
                        {"id": "fight_lab_security", "text": "Laboratuvar Güvenliği ile Savaş", "combat": True, "enemy": "Lab Security", "next_scene": "cyber_cyber_prison"},
                        {"id": "study_lab_lore", "text": "Laboratuvar Lore'unu Öğren", "effect": "item:lab_lore", "next_scene": "cyber_cyber_prison"}
                    ]
                },
                {
                    "id": "cyber_cyber_prison",
                    "title": "Siber Siber Hapishane",
                    "description": "Siber hapishanede esir netrunner'ları kurtar!",
                    "background": "/static/images/cyber_cyber_prison.jpg",
                    "choices": [
                        {"id": "rescue_netrunners", "text": "Netrunner'ları Kurtar", "effect": "ally:rescued_netrunners, gain_xp:5", "next_scene": "cyber_cyber_factory"},
                        {"id": "hack_prison_systems", "text": "Hapishane Sistemlerini Hack Et", "effect": "buff:prison_access", "next_scene": "cyber_cyber_factory"},
                        {"id": "fight_prison_guards", "text": "Hapishane Muhafızları ile Savaş", "combat": True, "enemy": "Prison Guards", "next_scene": "cyber_cyber_factory"},
                        {"id": "study_prison_lore", "text": "Hapishane Lore'unu Öğren", "effect": "item:prison_lore", "next_scene": "cyber_cyber_factory"}
                    ]
                },
                {
                    "id": "cyber_cyber_factory",
                    "title": "Siber Siber Fabrika",
                    "description": "Siber fabrikada güçlü robotlarla savaş!",
                    "background": "/static/images/cyber_cyber_factory.jpg",
                    "choices": [
                        {"id": "fight_factory_robots", "text": "Fabrika Robotları ile Savaş", "combat": True, "enemy": "Factory Robots", "next_scene": "cyber_cyber_warehouse"},
                        {"id": "hack_factory_systems", "text": "Fabrika Sistemlerini Hack Et", "effect": "buff:factory_control", "next_scene": "cyber_cyber_warehouse"},
                        {"id": "steal_factory_parts", "text": "Fabrika Parçalarını Çal", "effect": "item:factory_parts", "next_scene": "cyber_cyber_warehouse"},
                        {"id": "study_factory_lore", "text": "Fabrika Lore'unu Öğren", "effect": "item:factory_lore", "next_scene": "cyber_cyber_warehouse"}
                    ]
                },
                {
                    "id": "cyber_cyber_warehouse",
                    "title": "Siber Siber Depo",
                    "description": "Siber depoda güçlü ekipmanlar bul!",
                    "background": "/static/images/cyber_cyber_warehouse.jpg",
                    "choices": [
                        {"id": "search_warehouse", "text": "Depoyu Ara", "effect": "item:warehouse_equipment", "next_scene": "cyber_cyber_bunker"},
                        {"id": "fight_warehouse_guards", "text": "Depo Muhafızları ile Savaş", "combat": True, "enemy": "Warehouse Guards", "next_scene": "cyber_cyber_bunker"},
                        {"id": "hack_warehouse_systems", "text": "Depo Sistemlerini Hack Et", "effect": "buff:warehouse_access", "next_scene": "cyber_cyber_bunker"},
                        {"id": "study_warehouse_lore", "text": "Depo Lore'unu Öğren", "effect": "item:warehouse_lore", "next_scene": "cyber_cyber_bunker"}
                    ]
                },
                {
                    "id": "cyber_cyber_bunker",
                    "title": "Siber Siber Sığınak",
                    "description": "Siber sığınakta güçlü savunma sistemleri var!",
                    "background": "/static/images/cyber_cyber_bunker.jpg",
                    "choices": [
                        {"id": "hack_bunker_systems", "text": "Sığınak Sistemlerini Hack Et", "effect": "buff:bunker_access, gain_xp:5", "next_scene": "cyber_cyber_control_center"},
                        {"id": "fight_bunker_defenses", "text": "Sığınak Savunmaları ile Savaş", "combat": True, "enemy": "Bunker Defenses", "next_scene": "cyber_cyber_control_center"},
                        {"id": "steal_bunker_data", "text": "Sığınak Verilerini Çal", "effect": "item:bunker_data", "next_scene": "cyber_cyber_control_center"},
                        {"id": "study_bunker_lore", "text": "Sığınak Lore'unu Öğren", "effect": "item:bunker_lore", "next_scene": "cyber_cyber_control_center"}
                    ]
                },
                {
                    "id": "cyber_cyber_control_center",
                    "title": "Siber Siber Kontrol Merkezi",
                    "description": "Siber kontrol merkezinde güçlü AI sistemleri var!",
                    "background": "/static/images/cyber_cyber_control_center.jpg",
                    "choices": [
                        {"id": "hack_control_systems", "text": "Kontrol Sistemlerini Hack Et", "effect": "buff:control_access, gain_xp:6", "next_scene": "cyber_cyber_final_battle"},
                        {"id": "fight_control_ai", "text": "Kontrol AI'sı ile Savaş", "combat": True, "enemy": "Control AI", "next_scene": "cyber_cyber_final_battle"},
                        {"id": "steal_control_data", "text": "Kontrol Verilerini Çal", "effect": "item:control_data", "next_scene": "cyber_cyber_final_battle"},
                        {"id": "study_control_lore", "text": "Kontrol Lore'unu Öğren", "effect": "item:control_lore", "next_scene": "cyber_cyber_final_battle"}
                    ]
                },
                {
                    "id": "cyber_cyber_final_battle",
                    "title": "Siber Siber Son Savaş",
                    "description": "Siber son savaş başladı! Bu sıra tabanlı kombat senin için!",
                    "background": "/static/images/cyber_cyber_final_battle.jpg",
                    "choices": [
                        {"id": "fight_cyber_final_boss", "text": "Siber Son Boss ile Savaş", "combat": True, "enemy": "Cyber Final Boss", "next_scene": "victory"},
                        {"id": "use_cyber_tactics", "text": "Siber Taktiklerini Kullan", "effect": "buff:cyber_power", "combat": True, "enemy": "Cyber Final Boss", "next_scene": "victory"},
                        {"id": "call_cyber_allies", "text": "Siber Müttefiklerini Çağır", "effect": "ally:cyber_allies", "combat": True, "enemy": "Cyber Final Boss", "next_scene": "victory"},
                        {"id": "negotiate_cyber_boss", "text": "Siber Boss ile Müzakere", "effect": "karma:+15", "next_scene": "victory"}
                    ]
                },
                {
                    "id": "victory",
                    "title": "Zafer",
                    "description": "Mega şirketleri yendin ve şehri kurtardın. Halk seni kahraman olarak görüyor.",
                    "background": "/static/images/cyberpunk_victory.jpg",
                    "choices": []
                }
            ]
        }
        
        self.campaigns["ork_invasion_defense"] = ork_invasion_campaign
        self.campaigns["dragon_hunt"] = dragon_hunt_campaign
        self.campaigns["cyberpunk_secrets"] = cyberpunk_secrets_campaign
        logger.info("Campaign manager initialized - Tüm kampanyalar yüklendi")
    
    def add_campaign(self, campaign_data: Dict):
        """Yeni kampanya ekle"""
        campaign_id = campaign_data.get("id")
        if campaign_id:
            self.campaigns[campaign_id] = campaign_data
            logger.info(f"Campaign added: {campaign_data.get('name', campaign_id)}")
            return True
        return False
    
    def remove_campaign(self, campaign_id: str):
        """Kampanya sil"""
        if campaign_id in self.campaigns:
            campaign_name = self.campaigns[campaign_id].get('name', campaign_id)
            del self.campaigns[campaign_id]
            logger.info(f"Campaign removed: {campaign_name}")
            return True
        return False
    
    def list_campaigns(self) -> List[Dict]:
        """Mevcut kampanyaları listele"""
        return [
            {
                "id": campaign["id"],
                "name": campaign["name"],
                "type": campaign.get("type", "unknown"),
                "description": campaign.get("description", "")
            }
            for campaign in self.campaigns.values()
        ]
    
    def get_campaign(self, campaign_id: str) -> Optional[Dict]:
        """Belirli bir kampanyayı getir"""
        return self.campaigns.get(campaign_id)
    
    def get_campaign_step(self, campaign_id: str, step_id: str) -> Optional[Dict]:
        """Kampanya adımını getir"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            return None
        
        # İlk adım için start scene'i döndür
        if step_id == "start":
            scenes = campaign.get("scenes", [])
            if scenes:
                first_scene = scenes[0]
                return {
                    "description": f"{first_scene['title']}\n\n{first_scene['description']}",
                    "choices": [
                        {
                            "id": choice["id"],
                            "text": choice["text"],
                            "nextSceneId": choice.get("next_scene")
                        }
                        for choice in first_scene.get("choices", [])
                    ],
                    "background": first_scene.get("background")
                }
        
        # Diğer adımlar için scene'i bul
        scenes = campaign.get("scenes", [])
        for scene in scenes:
            if scene["id"] == step_id:
                return {
                    "description": f"{scene['title']}\n\n{scene['description']}",
                    "choices": [
                        {
                            "id": choice["id"],
                            "text": choice["text"],
                            "nextSceneId": choice.get("next_scene")
                        }
                        for choice in scene.get("choices", [])
                    ],
                    "background": scene.get("background")
                }
        
        return None
    
    def get_choice_result(self, campaign_id: str, choice_id: str) -> Optional[Dict]:
        """Seçim sonucunu getir"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            return None
        
        scenes = campaign.get("scenes", [])
        for scene in scenes:
            for choice in scene.get("choices", []):
                if choice["id"] == choice_id:
                    return {
                        "result": choice.get("result", ""),
                        "next_scene": choice.get("next_scene"),
                        "combat": choice.get("combat", False)
                    }
        
        return None
    
    def get_boss(self, campaign_id: str) -> Optional[Dict]:
        """Kampanya boss'unu getir"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            return None
        
        return campaign.get("boss") 