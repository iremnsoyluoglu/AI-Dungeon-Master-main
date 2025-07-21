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
                            "next_scene": "spirit_guardian_boss"
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
                    "id": "victory",
                    "title": "Zafer",
                    "description": "Pyraxis yere çakılıyor. Gökyüzü aydınlanıyor. Krallık seni kahraman ilan ediyor. Ejderha Avcısı unvanını kazandın!",
                    "choices": []
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
                    "id": "pyraxis_confrontation",
                    "title": "Pyraxis ile Yüzleşme",
                    "description": "Pyraxis mağarasının derinliklerinde seni bekliyor. Gözleri alev, sesi gök gürültüsü gibi yankılanıyor.\n\nPyraxis: 'Cesaretin varmış, ölümlü. Son sözlerini söylemeden önce bana ne teklif edebilirsin? Yoksa doğrudan alevlerime mi teslim olacaksın?'",
                    "background": "/static/images/pyraxisfam.jpg",
                    "choices": [
                        {"id": "pyraxis_persuade", "text": "İkna etmeye çalış: 'Bu savaşa gerek yok, birlikte barış getirebiliriz.'", "result": "Pyraxis seni küçümsedi ama bir an duraksadı. Sözlerin onu etkilemedi.", "effect": "reputation:+5", "next_scene": "pyraxis_boss_fight"},
                        {"id": "pyraxis_intimidate", "text": "Korkut: 'Gücüm sandığından fazla, pişman olabilirsin.'", "result": "Pyraxis güldü: 'Küçük tehditlerin bana işlemez.'", "effect": "reputation:-2", "next_scene": "pyraxis_boss_fight"},
                        {"id": "pyraxis_bluff", "text": "Blöf yap: 'Arkadaşlarım ve müttefiklerim mağaranı sardı.'", "result": "Pyraxis bir an şüphelendi ama blöfünü anladı.", "effect": "reputation:-1", "next_scene": "pyraxis_boss_fight"},
                        {"id": "pyraxis_bargain", "text": "Pazarlık yap: 'Sana krallığın hazinesini teklif ediyorum.'", "result": "Pyraxis: 'Hazineniz umrumda değil. Sadece güç ilgimi çeker.'", "effect": "lose_gold:100", "next_scene": "pyraxis_boss_fight"},
                        {"id": "pyraxis_flee", "text": "Kaçmaya çalış", "result": "Kaçmaya çalıştın ama Pyraxis seni engelledi. Savaş kaçınılmaz!", "effect": "lose_hp:10", "next_scene": "pyraxis_boss_fight"},
                        {"id": "pyraxis_attack", "text": "Doğrudan saldır!", "result": "Kılıcını çekip Pyraxis'e saldırdın. Savaş başlıyor!", "effect": "", "next_scene": "pyraxis_boss_fight"}
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
                        {"id": "spider_gift", "text": "Örümceğin Hediyesi (İlişki > 2)", "result": "Örümcek sana nadir bir ipek verdi!", "effect": "item:rare_silk, gain_xp:7", "condition": "relationship:Spider:>2", "next_scene": "trap_chest"},
                        {"id": "spider_neutral", "text": "Örümcekle Sohbet Et (İlişki -2 ile 2 arası)", "result": "Örümcekle iletişim kurdun, küçük bir bilgi aldın.", "effect": "gain_xp:2", "condition": "relationship:Spider:>=-2,<=2", "next_scene": "trap_chest"},
                        {"id": "spider_hostile", "text": "Örümceğin Saldırısı (İlişki < -2)", "result": "Örümcek seni zehirledi, HP kaybettin.", "effect": "lose_hp:10, debuff:poisoned", "condition": "relationship:Spider:<-2", "next_scene": "trap_chest"}
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
        
        self.campaigns["dragon_lords"] = dragon_campaign
        logger.info("Campaign manager initialized - Ejderha Efendilerinin Dönüşü kampanyası yüklendi")
    
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