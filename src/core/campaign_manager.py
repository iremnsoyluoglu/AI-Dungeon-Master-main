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
                            "result": "Dumanın geldiği yere doğru cesaretle ilerledin. Pyraxis ile erken karşılaşma başladı!",
                            "next_scene": "early_fight"
                        }
                    ]
                },
                {
                    "id": "forest_path",
                    "title": "Orman Yolu",
                    "description": "Yolun seni getirdiği orman, sessizliğin içinde bir uğultu taşıyor. Kuşlar susmuş, rüzgâr bile fısıldıyor gibi. Bu doğa değil... büyü. Belki antik, belki lanetli. Ya da seni bir seçim yapmaya zorluyor.",
                    "choices": [
                        {
                            "id": "follow_sounds",
                            "text": "Sesleri Takip Et",
                            "result": "Ağaçların arasında bir ışık hüzmesi gördün. Yarım-elf bir büyücü seni bekliyordu. Yeni bir büyü öğrendin: Buz Zırhı.",
                            "next_scene": "boss_fight"
                        },
                        {
                            "id": "hide",
                            "text": "Saklan",
                            "result": "Bir gölge üzerinden geçti, seni fark etmedi. Bir sonraki savaşta sürpriz saldırı bonusu kazandın.",
                            "next_scene": "boss_fight"
                        },
                        {
                            "id": "challenge",
                            "text": "Meydan Oku",
                            "result": "Kılıcını çekip karanlığa bağırdın. Ork Savaşı başladı!",
                            "next_scene": "orc_fight"
                        },
                        {
                            "id": "find_other_way",
                            "text": "Geri Dön",
                            "result": "Gece çok karanlık, sesler tuzak olabilir diye geri döndün. Güvendesin ama zaman kaybettin.",
                            "next_scene": "safe_route"
                        }
                    ]
                },
                {
                    "id": "new_ally",
                    "title": "Yeni Müttefik",
                    "description": "Cüce savaşçı Borin sana katıldı. Güçlü, cesur ve deneyimli bir dost.",
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
                    "description": "Dumanın kaynağına yaklaştın. Devasa kanatlarıyla Pyraxis seni bekliyor. Dövüş kaçınılmaz.",
                    "choices": [
                        {
                            "id": "fight_early",
                            "text": "Savaş",
                            "result": "Pyraxis ile erken savaş başladı!",
                            "next_scene": "boss_fight",
                            "combat": True
                        },
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
                    "choices": [
                        {
                            "id": "attack_ork",
                            "text": "Saldır",
                            "result": "Grug yenildi, yolun Pyraxis'e açıldı.",
                            "next_scene": "boss_fight",
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
                    "description": "Zorlu bir geceyi atlattın. Hayattasın ancak yolun uzadı.",
                    "choices": [
                        {
                            "id": "return_to_forest",
                            "text": "Orman Yoluna Geri Dön",
                            "result": "Güvenli rotadan orman yoluna geri döndün.",
                            "next_scene": "forest_path"
                        }
                    ]
                },
                {
                    "id": "boss_fight",
                    "title": "BOSS DÖVÜŞÜ: Pyraxis – Alevin Efendisi",
                    "description": "Kuzey Dağları'nın karla kaplı zirvesinde Pyraxis seni bekliyor. Gözleri alev, nefesi ölüm. Uçuyor, ateş nefesi ile saldırıyor!",
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
                    "description": "Hayatta kaldın, ancak Pyraxis geri döndü. Savaş başka bir gün için ertelendi. Suçluluk duygusu seni bırakmıyor...",
                    "choices": []
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
                    ]
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
                    ]
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