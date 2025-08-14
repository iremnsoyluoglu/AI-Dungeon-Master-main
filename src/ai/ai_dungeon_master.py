#!/usr/bin/env python3
"""
AI Dungeon Master - Türkçe Hikaye Anlatıcısı
=============================================

AI destekli Dungeon Master ki:
- Sürekli hikaye anlatır
- Oyuncu aksiyonlarına tepki verir
- Dinamik senaryo üretir
- Türkçe iletişim kurar
"""

import logging
import random
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.inventory_system import InventorySystem
from core.skill_system import SkillSystem
from multiplayer.session_manager import MultiplayerSessionManager
from ai.ai_learning_system import AILearningSystem

logger = logging.getLogger(__name__)

class AIDungeonMaster:
    """AI Dungeon Master - Türkçe hikaye anlatıcısı"""
    
    def __init__(self):
        self.current_scenario = None
        self.player_actions = []
        self.narrative_history = []
        self.scenario_templates = self._load_scenario_templates()
        self.narrative_styles = self._load_narrative_styles()
        
        # Kalıcı depolama için dosya yolları
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.sessions_file = os.path.join(self.data_dir, "game_sessions.json")
        self.actions_file = os.path.join(self.data_dir, "player_actions.json")
        self.scenarios_file = os.path.join(self.data_dir, "generated_scenarios.json")
        
        # Data dizinini oluştur
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Mevcut verileri yükle
        self._load_persistent_data()
        
        # Initialize new systems
        self.inventory_system = InventorySystem()
        self.skill_system = SkillSystem()
        self.multiplayer_manager = MultiplayerSessionManager()
        self.ai_learning = AILearningSystem()
    
    def _load_persistent_data(self):
        """Kalıcı verileri yükle"""
        try:
            # Oyuncu aksiyonları
            if os.path.exists(self.actions_file):
                with open(self.actions_file, 'r', encoding='utf-8') as f:
                    self.player_actions = json.load(f)
                logger.info(f"Loaded {len(self.player_actions)} player actions")
            
            # Oyun oturumları
            if os.path.exists(self.sessions_file):
                with open(self.sessions_file, 'r', encoding='utf-8') as f:
                    self.game_sessions = json.load(f)
                logger.info(f"Loaded {len(self.game_sessions)} game sessions")
            else:
                self.game_sessions = {}
            
            # Üretilen senaryolar
            if os.path.exists(self.scenarios_file):
                with open(self.scenarios_file, 'r', encoding='utf-8') as f:
                    self.generated_scenarios = json.load(f)
                logger.info(f"Loaded {len(self.generated_scenarios)} generated scenarios")
            else:
                self.generated_scenarios = []
                
        except Exception as e:
            logger.error(f"Error loading persistent data: {e}")
            self.player_actions = []
            self.game_sessions = {}
            self.generated_scenarios = []
    
    def _save_persistent_data(self):
        """Kalıcı verileri kaydet"""
        try:
            # Oyuncu aksiyonları
            with open(self.actions_file, 'w', encoding='utf-8') as f:
                json.dump(self.player_actions, f, ensure_ascii=False, indent=2)
            
            # Oyun oturumları
            with open(self.sessions_file, 'w', encoding='utf-8') as f:
                json.dump(self.game_sessions, f, ensure_ascii=False, indent=2)
            
            # Üretilen senaryolar
            with open(self.scenarios_file, 'w', encoding='utf-8') as f:
                json.dump(self.generated_scenarios, f, ensure_ascii=False, indent=2)
                
            logger.info("Persistent data saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving persistent data: {e}")
    
    def _load_scenario_templates(self) -> Dict[str, Any]:
        """Senaryo şablonlarını yükle"""
        return {
            "fantasy_dragon": {
                "title": "🐉 Ejderha Mağarası",
                "setting": "Kasvetli bir mağara sistemi, derinliklerinde eski bir ejderha yaşıyor",
                "npcs": ["Bilge Keşiş", "Mağara Bekçisi", "Kayıp Şövalye"],
                "locations": ["Mağara Girişi", "Hazine Odası", "Ejderha Yuvası"],
                "enemies": ["Goblin", "Ork", "Kırmızı Ejderha"],
                "quests": ["Hazine Bul", "Ejderhayı Yen", "Kayıp Şövalyeyi Kurtar"]
            },
            "warhammer_mission": {
                "title": "🛡️ Space Marine Görevi", 
                "setting": "Ork istilası tehdidi altındaki bir dünya, İmperium'u korumak gerekiyor",
                "npcs": ["Imperial Komutan", "Tech-Priest", "Inquisitor"],
                "locations": ["Imperial Üs", "Ork Kampı", "Antik Harabeler"],
                "enemies": ["Ork Boy", "Ork Nob", "Ork Warboss"],
                "quests": ["Üssü Savun", "Warboss'u Yok Et", "Artefakt Bul"]
            },
            "pyraxis_legend": {
                "title": "🔥 Pyraxis Efsanesi",
                "setting": "Kızıl Alevin Efendisi Pyraxis'in krallığı tehdit ettiği epik bir macera. Ejderha Avcısı olmak için hazır mısın?",
                "npcs": ["Orman Perisi", "Demirci Ustası", "Bilge Keşiş", "Flame Oracle Vynn"],
                "locations": ["Orman Girişi", "Kuzey Dağları", "Pyraxis Mağarası", "Krallık Şehri"],
                "enemies": ["Ork Lideri Grug", "Alev Ruhu", "Kırmızı Ejderha Pyraxis"],
                "quests": ["Ormanı Keşfet", "Ork Liderini Yen", "Pyraxis ile Yüzleş", "Krallığı Kurtar"]
            }
        }
    
    def _load_narrative_styles(self) -> Dict[str, List[str]]:
        """Anlatım stilleri"""
        return {
            "descriptive": [
                "Hava ağır bir kükürt kokusuyla doluyor ve uzaktan garip sesler geliyor.",
                "Mağaranın duvarları eski runik yazılarla kaplı ve gizemli bir ışık huzmesi içeriden sızıyor.",
                "Rüzgar eski kemiklerin arasından geçerken ürkütücü bir melodi çıkarıyor.",
                "Gölgeler duvarlarda dans ediyor ve her adımınızda yankı yapıyor."
            ],
            "action": [
                "Aniden bir gürültü duyuyorsunuz!",
                "Gölgeler arasından bir şey hareket ediyor!",
                "Zemin titremeye başlıyor!",
                "Uzaktan savaş çığlıkları geliyor!"
            ],
            "mysterious": [
                "Burada bir şeyler var... ama ne olduğunu anlayamıyorsunuz.",
                "Garip bir enerji hissi alıyorsunuz.",
                "Bu yerin bir geçmişi var, eski ve unutulmuş.",
                "Bir şey sizi izliyor gibi hissediyorsunuz."
            ]
        }
    
    def start_scenario(self, scenario_id: str, players: List[Dict]) -> Dict[str, Any]:
        """Senaryo başlat ve ilk hikayeyi anlat"""
        try:
            self.current_scenario = scenario_id
            template = self.scenario_templates.get(scenario_id, self.scenario_templates["fantasy_dragon"])
            
            # Oyuncuları tanıt
            player_intro = self._generate_player_introduction(players)
            
            # Başlangıç hikayesi
            opening_narrative = self._generate_opening_narrative(template)
            
            # İlk sahne
            first_scene = self._generate_first_scene(template)
            
            narrative = f"""
{opening_narrative}

{player_intro}

{first_scene}
            """.strip()
            
            # Hikayeyi kaydet
            self.narrative_history.append({
                "timestamp": datetime.now().isoformat(),
                "narrative": narrative,
                "type": "opening"
            })
            
            # Oyun oturumunu kaydet
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
            session_data = {
                "session_id": session_id,
                "scenario_id": scenario_id,
                "players": players,
                "start_time": datetime.now().isoformat(),
                "status": "active",
                "narrative_history": self.narrative_history.copy()
            }
            self.game_sessions[session_id] = session_data
            self._save_persistent_data()
            
            # Generate contextual actions
            contextual_actions = self._generate_initial_actions(template)
            
            return {
                "scenario_id": scenario_id,
                "session_id": session_id,
                "narrative": narrative,
                "available_actions": contextual_actions,
                "current_scene": "opening",
                "players": players,
                "story_context": {
                    "scenario_type": scenario_id,
                    "location": "starting_area",
                    "situation": "exploration",
                    "npcs": template.get("npcs", []),
                    "enemies": template.get("enemies", []),
                    "locations": template.get("locations", [])
                },
                "game_state": {
                    "status": "active",
                    "turn": 1,
                    "round": 1,
                    "combat_active": False
                }
            }
        except Exception as e:
            logger.error(f"Error starting scenario: {e}")
            # Return a safe default response
            return {
                "scenario_id": scenario_id,
                "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}",
                "narrative": "🌲 Büyülü ormanın derinliklerinde... Ağaçlar konuşuyor, yaratıklar her yerde. Sen kimsin ve neden buradasın? Ormanın sırları seni bekliyor, ama her sır bir bedel gerektirir... 🎭 Bu ormanda hiçbir şey göründüğü gibi değil. Büyü ve gerçeklik iç içe geçmiş durumda...",
                "available_actions": [
                    {
                        "type": "explore",
                        "description": "🌳 Çevreyi araştır",
                        "context": "exploration",
                        "dice": "1d20",
                        "skill": "perception"
                    },
                    {
                        "type": "social",
                        "description": "💬 NPC ile konuş",
                        "context": "communication",
                        "dice": "1d20",
                        "skill": "persuasion"
                    },
                    {
                        "type": "investigate",
                        "description": "🔍 Gizli şeyleri araştır",
                        "context": "investigation",
                        "dice": "1d20",
                        "skill": "investigation"
                    }
                ],
                "current_scene": "opening",
                "players": players,
                "story_context": {
                    "scenario_type": scenario_id,
                    "location": "starting_area",
                    "situation": "exploration",
                    "npcs": [],
                    "enemies": [],
                    "locations": []
                },
                "game_state": {
                    "status": "active",
                    "turn": 1,
                    "round": 1,
                    "combat_active": False
                }
            }
    
    def _generate_player_introduction(self, players: List[Dict]) -> str:
        """Oyuncuları tanıtan metin"""
        if len(players) == 1:
            player = players[0]
            character_name = player.get('character_name') or player.get('name', 'Kahraman')
            character_class = player.get('character_class') or player.get('class', 'Savaşçı')
            return f"{character_name} ({character_class}), bu tehlikeli yolculuğa tek başına çıkmış."
        else:
            player_names = []
            for p in players:
                character_name = p.get('character_name') or p.get('name', 'Kahraman')
                character_class = p.get('character_class') or p.get('class', 'Savaşçı')
                player_names.append(f"{character_name} ({character_class})")
            
            if len(player_names) == 2:
                return f"Grup: {player_names[0]} ve {player_names[1]} bu tehlikeli yolculuğa birlikte çıkmış."
            else:
                return f"Grup: {', '.join(player_names[:-1])} ve {player_names[-1]} bu tehlikeli yolculuğa birlikte çıkmış."
    
    def _generate_opening_narrative(self, template: Dict) -> str:
        """Açılış hikayesi üret - Enhanced with more detail and atmosphere"""
        try:
            setting = template.get("setting", "")
            title = template.get("title", "")
            scenario_id = getattr(self, 'current_scenario', '').lower()
            
            # Pyraxis senaryosu için özel hikaye
            if "pyraxis" in title.lower() or "pyraxis" in scenario_id:
                return f"""🔥 {title} - Epik Macera Başlıyor!

Kuzey Dağları'nın karla kaplı zirvelerinden gelen duman, krallığın son günlerini işaret ediyor. 
Kızıl Alevin Efendisi Pyraxis, yüzyıllar sonra uyanmış ve krallığı tehdit ediyor.

Gökyüzü kızıl alevlerle yanıyor, dağlar titriyor. Krallık korku içinde, 
ama bir umut var: Sen ve senin gibi seçilmiş birkaç kahraman...

Bu, Ejderha Avcısı olma yolculuğunun başlangıcı. Pyraxis ile yüzleşmek için hazır mısın?

🎭 **Destanın Başlangıcı**
Kuzey Dağları'nın eteklerinde, Pyraxis'in uyanışının ilk işaretleri görülmeye başladı. 
Köylüler geceleri kızıl ışıklar gördüklerini, dağlardan gelen gürültüleri duyduklarını anlatıyor.
Krallık şehri panik içinde, çünkü Pyraxis'in son uyanışında yüzlerce köy yanmış, binlerce insan ölmüştü.

⚔️ **Kahramanların Çağrısı**
Şimdi sen, seçilmiş kahraman, bu tehlikeli yolculuğa çıkmaya hazırsın. 
Pyraxis'in mağarasına ulaşmak, onu yenmek ve krallığı kurtarmak senin görevin.
Ama dikkatli ol - bu yolculukta sadece Pyraxis değil, onun hizmetkarları da seni bekliyor."""
            
            # Büyülü orman senaryosu için özel hikaye
            elif "büyülü" in title.lower() or "magical" in title.lower() or "forest" in scenario_id or "orman" in scenario_id:
                return f"""🌲 {title} - Büyülü Orman Macerası

Büyülü ormanın derinliklerinde... Ağaçlar konuşuyor, yaratıklar her yerde. Sen kimsin ve neden buradasın? 
Ormanın sırları seni bekliyor, ama her sır bir bedel gerektirir...

🎭 Bu ormanda hiçbir şey göründüğü gibi değil. Büyü ve gerçeklik iç içe geçmiş durumda. 
Her adımında yeni bir gizem, her dönüşte yeni bir tehlike seni bekliyor.

✨ **Ormanın Sırları**
Eski efsanelere göre, bu orman bir zamanlar güçlü bir büyücünün eviymiş. 
Büyücü öldükten sonra, büyüsü ormana sinmiş ve ağaçlar canlanmış. 
Şimdi orman kendi zihnine sahip ve sadece layık olanları içeri alıyor.

🌳 **Konuşan Ağaçlar**
Ormanın derinliklerinde yürürken, ağaçların konuştuğunu duyacaksın. 
Bazıları dostça, bazıları ise tehlikeli. Hangi seslere güveneceğini bilmek önemli.

👁️ **Gizli Tehlikeler**
Ormanın gölgelerinde eski tuzaklar, yanıltıcı yollar ve aç ağızlar bekliyor. 
Her adımında dikkatli olmalısın, çünkü bu orman affetmiyor.

💫 **Karakterlerinizin Hikayesi**
Bu ormanda karşılaşacağınız her karakter kendi hikayesine sahip. 
**Eldrin the Wise** size rehberlik edebilir, **Lyra the Ranger** tehlikeli yolları gösterebilir,
**Mystra the Enchantress** büyülü sırları paylaşabilir. Her biri kendi motivasyonları,
kendi geçmişleri ve kendi hedefleri olan gerçek karakterler.

🎯 **Sizin Seçimleriniz**
Bu hikayede sadece sizin seçimleriniz önemli. Her kararınız hikayeyi şekillendirecek,
her eyleminiz sonuçları değiştirecek. Karakterlerinizle gerçek bağlar kurun,
çünkü bu ormanda dostluk ve ihanet aynı anda var olabilir.

Hazır mısın bu büyülü yolculuğa çıkmaya?"""
            
            # Warhammer senaryosu için özel hikaye
            elif "warhammer" in scenario_id or "mission" in scenario_id:
                return f"""🛡️ {title} - Imperial Görevi

Ork istilası tehdidi altındaki bir dünyadayız. İmperium'un gücü burada test edilecek ve 
sadece en cesur askerler hayatta kalabilecek.

⚔️ Bu, sadece bir görev değil, İmparator'a olan sadakatimizin sınandığı bir an. 
Orkların barbarlığına karşı Imperial disiplini ve teknolojisi galip gelecek.

🚨 **Ork Tehdidi**
Ork Waaagh'ı sistemin dış kolonilerini ele geçirmiş durumda. 
Milyonlarca sivil tehdit altında ve İmperium'un bu bölgedeki varlığı tehlikeye giriyor.
Ork Warboss Gorgutz, kendi teknolojisini geliştirmiş ve geleneksel Imperial taktiklerini etkisiz hale getiriyor.

🛡️ **Imperial Savunma**
Imperial Guard birlikleri son savunma hattında. Space Marine desteği gelene kadar 
savunmayı tutmak senin görevin. Tech-Priest'ler ork teknolojisini analiz etmeye çalışıyor,
ama zaman daralıyor.

⚙️ **Teknolojik Üstünlük**
Orkların bu kadar gelişmiş teknolojiye sahip olması şüpheli. 
Arkalarında başka bir güç olabilir - belki de Chaos'un parmağı var bu işte.

💫 **Karakterlerinizin Hikayesi**
Bu savaşta karşılaşacağınız her karakter kendi görevine sahip. 
**Commissar Valen** size liderlik edebilir, **Tech-Priest Zeta-7** teknolojik destek sağlayabilir,
**Medicae Sister Helena** yaralarınızı iyileştirebilir. Her biri İmparator'a olan sadakatleri,
kendi uzmanlıkları ve kendi motivasyonları olan gerçek askerler.

🎯 **Sizin Seçimleriniz**
Bu savaşta her kararınız hayati önem taşıyor. Her taktik seçiminiz sonucu değiştirecek,
her stratejik hamleniz savaşın gidişatını etkileyecek. Birlikte çalışın,
çünkü bu savaşta birlik güçtür ve İmparator bizi izliyor.

Hazır mısın İmperium'u korumaya?"""
            
            # Cyberpunk senaryosu için özel hikaye
            elif "cyberpunk" in scenario_id:
                return f"""🌃 {title} - Cyberpunk Macerası

Neon ışıkları altında, mega şirketlerin gölgesinde bir dünyada yaşıyoruz. 
Teknoloji ve insanlık arasındaki çizgi bulanıklaşmış, her köşe başında yeni bir tehdit var.

💻 Bu şehirde bilgi en değerli silah, network en güçlü kalkan. 
Hack'lemek, kaçmak, hayatta kalmak... Bu cyberpunk dünyasında sen nerede duruyorsun?

🌆 **Mega Şehir Yaşamı**
Night City'nin sokaklarında neon ışıkları yanıp sönüyor. 
Megacorps'un gökdelenleri bulutları deliyor, sokak seviyesinde ise hayatta kalma mücadelesi sürüyor.
Burada para konuşuyor, güç yönetiyor ve bilgi satılıyor.

💾 **Dijital Tuzaklar**
Şehrin network'ü her yerde. Her kamera, her terminal, her implant potansiyel bir tehdit.
Hack'lemek ya da hack'lenmek - bu senaryoda her ikisi de mümkün.
Şehir sürekli izliyor ve kayıt tutuyor.

💫 **Karakterlerinizin Hikayesi**
Bu şehirde karşılaşacağınız her karakter kendi ajandasına sahip. 
**Netrunner Shadow** size dijital dünyada rehberlik edebilir, **Street Samurai Blade** fiziksel koruma sağlayabilir,
**Fixer Silver** değerli bilgiler verebilir. Her biri kendi motivasyonları,
kendi geçmişleri ve kendi hedefleri olan gerçek karakterler.

🎯 **Sizin Seçimleriniz**
Bu şehirde her kararınız sonuçları değiştirecek. Her hack'leme işleminiz sistemleri etkileyecek,
her sosyal etkileşiminiz ilişkileri şekillendirecek. Güvenilir dostlar bulun,
çünkü bu şehirde herkes kendi çıkarı için çalışıyor ve ihanet her köşede bekliyor.

Hazır mısın bu cyberpunk dünyasında hayatta kalmaya?"""
            
            else:
                # Genel açılış hikayeleri - Enhanced
                return f"""🎭 {title} - Epik Macera Başlıyor!

{setting}

🌟 **Yeni Bir Yolculuk**
Bu senaryo, senin karakterini ve becerilerini test edecek. 
Her kararın sonuçları olacak, her seçimin bedeli var.
Dostlarını seç, düşmanlarını tanı, ama asla geri dönme - çünkü bu yolculuk sadece ileri gidiyor.

⚔️ **Hazırlık Zamanı**
Senaryonun başında, karakterin ve ekibin hazırlanmalı. 
Ekipman kontrol et, strateji geliştir, dostlarınla konuş.
Çünkü bu macerada her detay önemli, her hazırlık hayat kurtarabilir."""
                
        except Exception as e:
            logger.error(f"Error generating opening narrative: {e}")
            return f"""🌲 Büyülü ormanın derinliklerinde... Ağaçlar konuşuyor, yaratıklar her yerde. Sen kimsin ve neden buradasın? 
Ormanın sırları seni bekliyor, ama her sır bir bedel gerektirir... 

🎭 Bu ormanda hiçbir şey göründüğü gibi değil. Büyü ve gerçeklik iç içe geçmiş durumda. 
Her adımında yeni bir gizem, her dönüşte yeni bir tehlike seni bekliyor.

✨ **Ormanın Sırları**
Eski efsanelere göre, bu orman bir zamanlar güçlü bir büyücünün eviymiş. 
Büyücü öldükten sonra, büyüsü ormana sinmiş ve ağaçlar canlanmış. 
Şimdi orman kendi zihnine sahip ve sadece layık olanları içeri alıyor.

Hazır mısın bu büyülü yolculuğa çıkmaya?"""
    
    def _generate_first_scene(self, template: Dict) -> str:
        """İlk sahne hikayesi - Enhanced with more detail and context"""
        try:
            locations = template.get("locations", ["Bilinmeyen Bölge"])
            location = random.choice(locations)
            title = template.get("title", "")
            scenario_id = getattr(self, 'current_scenario', '').lower()
            
            # Scenario-specific first scenes
            if "büyülü" in title.lower() or "magical" in title.lower() or "forest" in scenario_id or "orman" in scenario_id:
                scene_templates = [
                    f"""🌲 **{location}** - Büyülü Ormanın Girişi

Ormanın girişinde duruyorsunuz. Ağaçların arasından gelen hafif bir rüzgar, 
eski büyülerin kokusunu taşıyor. Yapraklar fısıldıyor gibi, sanki size bir şeyler anlatmaya çalışıyorlar.

Uzaktan, ormanın derinliklerinden garip sesler geliyor. 
Bazıları dostça, bazıları ise tehlikeli. Orman sizi içeri davet ediyor, 
ama her adımınızı dikkatli atmanız gerekiyor.""",
                    
                    f"""🌳 **{location}** - Ormanın Sırları

{location} bölgesine ulaştınız. Burada, ormanın en eski ağaçlarından biri duruyor. 
Gövdesinde eski runik yazılar var, sanki size bir mesaj vermeye çalışıyor gibi.

Ağacın etrafında küçük büyülü ışık huzmeleri dans ediyor. 
Bu yerin gücü sizi çekiyor, ama aynı zamanda tehlikeli olduğunu da hissettiriyor."""
                ]
            elif "warhammer" in scenario_id or "mission" in scenario_id:
                scene_templates = [
                    f"""🛡️ **{location}** - Imperial Savunma Hattı

{location} bölgesinde, Imperial Guard'ın son savunma pozisyonlarından birindesiniz. 
Uzaktan ork savaş çığlıkları geliyor, hava savaşın kokusuyla dolu.

Sistemleriniz ork teknolojisinin yaklaştığını gösteriyor. 
Tech-Priest'ler son hazırlıkları yapıyor, askerler pozisyon alıyor.
Bu, İmperium'un bu bölgedeki son savunma hattı.""",
                    
                    f"""⚔️ **{location}** - Savaş Alanı

{location} önündesiniz. Bu bölge, ork istilasının ilk dalgasının geldiği yer. 
Yerde hala savaşın izleri var - yanmış araçlar, kırık silahlar, savaş alanının kalıntıları.

Hava ağır ve tehlikeli. Orkların yaklaştığını hissedebiliyorsunuz. 
Bu, sadece bir savaş değil, İmparator'a olan sadakatimizin sınandığı bir an."""
                ]
            elif "cyberpunk" in scenario_id:
                scene_templates = [
                    f"""🌃 **{location}** - Neon Sokakları

{location} bölgesinde, Night City'nin en tehlikeli sokaklarından birindesiniz. 
Neon ışıkları yanıp sönüyor, uzaktan siren sesleri geliyor.

Her köşe başında potansiyel bir tehdit, her terminal potansiyel bir fırsat. 
Şehrin network'ü sizi izliyor, her adımınız kaydediliyor.
Bu cyberpunk dünyasında, bilgi en değerli silahınız.""",
                    
                    f"""💻 **{location}** - Dijital Sınırlar

{location} önündesiniz. Bu, şehrin en gelişmiş teknoloji merkezlerinden biri. 
Her yerde hologramlar, her köşede interaktif ekranlar.

Ama dikkatli olun - bu teknoloji hem dost hem düşman olabilir. 
Hack'lemek ya da hack'lenmek... Bu senaryoda her ikisi de mümkün.
Şehrin dijital ağları sizi bekliyor."""
                ]
            elif "ejderha" in title.lower() or "dragon" in title.lower() or "fantasy_dragon" in scenario_id:
                scene_templates = [
                    f"""🐉 **{location}** - Ejderha İzleri

{location} bölgesinde, ejderhanın geçtiği izler net bir şekilde görünüyor. 
Yerde yanmış toprak, ağaçlarda tırmık izleri, havada kükürt kokusu.

Bu izler taze - ejderha yakınlarda. Köylülerin anlattığı korku hikayeleri 
şimdi gerçek gibi görünüyor. Her adımınızı dikkatli atın, çünkü ejderha da sizi izliyor.""",
                    
                    f"""🔥 **{location}** - Ejderha Yuvası Yakınları

{location} bölgesindesiniz. Bu, ejderhanın yuvasına giden yolda önemli bir nokta. 
Hava sıcak ve ağır, uzaktan ejderhanın kükremesini duyabiliyorsunuz.

Yerde yanmış kalıntılar, ejderhanın geçmiş saldırılarının izleri var. 
Bu, sadece bir keşif görevi değil - bu, ejderha ile yüzleşmenin başlangıcı."""
                ]
            else:
                # General scene templates
                scene_templates = [
                    f"""🎭 **{location}** - Maceranın Başlangıcı

{location} bölgesine ulaştınız. Bu yer, senaryonuzun başlangıç noktası. 
Etrafınızı saran atmosfer, bu yolculuğun tehlikeli olacağını söylüyor.

Her köşe başında yeni bir gizem, her adımda yeni bir sınav sizi bekliyor. 
Hazır olun - çünkü bu macera sadece başlıyor.""",
                    
                    f"""⚔️ **{location}** - Tehlike Dolu Bölge

{location} önündesiniz. Bu bölge, tehlike ve fırsatların iç içe geçtiği bir yer. 
Hava gergin, atmosfer yoğun - bir şeyler olmak üzere.

Burada ne olduğunu keşfetmek ve hayatta kalmak zorundasınız. 
Her kararınız önemli, her seçiminiz sonuçları olacak."""
                ]
            
            return random.choice(scene_templates)
            
        except Exception as e:
            logger.error(f"Error generating first scene: {e}")
            return f"🌲 {location} bölgesindesiniz. Etrafınızı saran atmosfer size bu yerin tehlikeli olduğunu söylüyor."
    
    def _generate_initial_actions(self, template: Dict) -> List[Dict]:
        """Başlangıç aksiyonları - senaryoya özel ve bağlamsal"""
        try:
            scenario_type = template.get("title", "").lower()
            scenario_id = getattr(self, 'current_scenario', '').lower()
            
            # Senaryo tipine göre özel aksiyonlar
            if "ejderha" in scenario_type or "dragon" in scenario_type or "fantasy_dragon" in scenario_id:
                return [
                    {
                        "type": "explore",
                        "description": "🌳 Ejderha izlerini takip et",
                        "dice": "1d20",
                        "skill": "survival",
                        "narrative": "Ejderhanın geçtiği yolları bulabilirsiniz."
                    },
                    {
                        "type": "investigate", 
                        "description": "🔍 Yakılmış köyü araştır",
                        "dice": "1d20",
                        "skill": "investigation",
                        "narrative": "Ejderhanın saldırısı hakkında ipuçları bulabilirsiniz."
                    },
                    {
                        "type": "talk",
                        "description": "💬 Köylülerden bilgi topla",
                        "dice": "1d20", 
                        "skill": "persuasion",
                        "narrative": "Ejderha hakkında bilgi alabilirsiniz."
                    },
                    {
                        "type": "prepare",
                        "description": "⚔️ Av ekipmanını hazırla",
                        "dice": "1d20",
                        "skill": "survival", 
                        "narrative": "Ejderha avı için hazırlık yapabilirsiniz."
                    }
                ]
            elif "büyülü" in scenario_type or "magical" in scenario_type or "forest" in scenario_type or "orman" in scenario_type:
                return [
                    {
                        "type": "explore",
                        "description": "🌲 Büyülü ormanı keşfet",
                        "dice": "1d20",
                        "skill": "nature",
                        "narrative": "Ormanın gizemlerini keşfedebilirsiniz."
                    },
                    {
                        "type": "communicate",
                        "description": "🌳 Konuşan ağaçlarla iletişim kur",
                        "dice": "1d20",
                        "skill": "nature",
                        "narrative": "Ağaçlardan bilgi alabilirsiniz."
                    },
                    {
                        "type": "investigate",
                        "description": "✨ Büyülü enerjiyi hisset",
                        "dice": "1d20",
                        "skill": "arcana",
                        "narrative": "Büyülü enerji kaynaklarını bulabilirsiniz."
                    },
                    {
                        "type": "stealth",
                        "description": "👁️ Gizlice ormanda ilerle",
                        "dice": "1d20",
                        "skill": "stealth",
                        "narrative": "Tehlikelerden kaçınarak ilerleyebilirsiniz."
                    }
                ]
            elif "hive" in scenario_type or "warhammer" in scenario_type or "mission" in scenario_id:
                return [
                    {
                        "type": "defend",
                        "description": "🛡️ Savunma pozisyonlarını kontrol et",
                        "dice": "1d20",
                        "skill": "military",
                        "narrative": "Savunma sistemlerini inceleyebilirsiniz."
                    },
                    {
                        "type": "scout",
                        "description": "🔍 Düşman güçlerini keşfet",
                        "dice": "1d20",
                        "skill": "reconnaissance",
                        "narrative": "Düşman hakkında bilgi toplayabilirsiniz."
                    },
                    {
                        "type": "evacuate",
                        "description": "🚨 Sivilleri güvenli bölgeye taşı",
                        "dice": "1d20",
                        "skill": "leadership",
                        "narrative": "Sivilleri kurtarabilirsiniz."
                    },
                    {
                        "type": "prepare",
                        "description": "⚔️ Savaş ekipmanını hazırla",
                        "dice": "1d20",
                        "skill": "military",
                        "narrative": "Savaş için hazırlık yapabilirsiniz."
                    }
                ]
            elif "cyberpunk" in scenario_type or "cyberpunk" in scenario_id:
                return [
                    {
                        "type": "hack",
                        "description": "💻 Şehir ağlarına bağlan",
                        "dice": "1d20",
                        "skill": "hacking",
                        "narrative": "Dijital bilgi toplayabilirsiniz."
                    },
                    {
                        "type": "negotiate",
                        "description": "💬 Yerel ganglerle konuş",
                        "dice": "1d20",
                        "skill": "street_cred",
                        "narrative": "Ganglerden bilgi alabilirsiniz."
                    },
                    {
                        "type": "investigate",
                        "description": "🔍 Şirket faaliyetlerini araştır",
                        "dice": "1d20",
                        "skill": "investigation",
                        "narrative": "Şirket sırlarını keşfedebilirsiniz."
                    },
                    {
                        "type": "stealth",
                        "description": "👁️ Gizlice şehirde ilerle",
                        "dice": "1d20",
                        "skill": "stealth",
                        "narrative": "Tehlikelerden kaçınarak ilerleyebilirsiniz."
                    }
                ]
            else:
                # Varsayılan genel aksiyonlar
                return [
                    {
                        "type": "explore",
                        "description": "🔍 Çevreyi keşfet",
                        "dice": "1d20",
                        "skill": "perception",
                        "narrative": "Gizli geçitler veya tehlikeler bulabilirsiniz."
                    },
                    {
                        "type": "investigate", 
                        "description": "🔎 Eski izleri takip et",
                        "dice": "1d20",
                        "skill": "investigation",
                        "narrative": "Daha derin bilgiler elde edebilirsiniz."
                    },
                    {
                        "type": "talk",
                        "description": "💬 Yerel halkla konuş",
                        "dice": "1d20",
                        "skill": "persuasion",
                        "narrative": "Yerel halktan bilgi alabilirsiniz."
                    },
                    {
                        "type": "prepare",
                        "description": "⚔️ Hazırlık yap",
                        "dice": "1d20",
                        "skill": "survival",
                        "narrative": "Gelecek tehlikeler için hazırlık yapabilirsiniz."
                    }
                ]
        except Exception as e:
            logger.error(f"Error generating initial actions: {e}")
            # Return safe default actions
            return [
                {
                    "type": "explore",
                    "description": "🔍 Çevreyi keşfet",
                    "dice": "1d20",
                    "skill": "perception",
                    "narrative": "Çevrenizi keşfetmeye başlayın."
                },
                {
                    "type": "talk",
                    "description": "💬 NPC ile konuş",
                    "dice": "1d20",
                    "skill": "persuasion",
                    "narrative": "Yerel halkla konuşun."
                },
                {
                    "type": "investigate",
                    "description": "🔎 Araştır",
                    "dice": "1d20",
                    "skill": "investigation",
                    "narrative": "Daha fazla bilgi toplayın."
                }
            ]
    
    def _generate_new_actions(self, previous_action: str, dice_result: Optional[int]) -> List[Dict]:
        """Yeni aksiyonlar üret - önceki aksiyona ve senaryoya bağlı"""
        success = dice_result and dice_result >= 12
        
        # Önceki aksiyona göre bağlamsal aksiyonlar
        if "ejderha" in previous_action.lower() or "dragon" in previous_action.lower():
            return [
                {
                    "type": "track",
                    "description": "Ejderha izlerini takip et",
                    "dice": "1d20",
                    "skill": "survival",
                    "narrative": "Ejderhanın geçtiği yolları takip edebilirsiniz."
                },
                {
                    "type": "prepare_weapons",
                    "description": "Ejderha avı silahlarını hazırla",
                    "dice": "1d20",
                    "skill": "survival",
                    "narrative": "Ejderhaya karşı etkili silahlar hazırlayabilirsiniz."
                },
                {
                    "type": "seek_help",
                    "description": "Diğer avcılardan yardım iste",
                    "dice": "1d20",
                    "skill": "persuasion",
                    "narrative": "Deneyimli avcılardan bilgi alabilirsiniz."
                }
            ]
        elif "büyülü" in previous_action.lower() or "magical" in previous_action.lower():
            return [
                {
                    "type": "cast_spell",
                    "description": "Büyülü keşif büyüsü kullan",
                    "dice": "1d20",
                    "skill": "arcana",
                    "narrative": "Büyü ile çevreyi keşfedebilirsiniz."
                },
                {
                    "type": "communicate_nature",
                    "description": "Doğa ruhlarıyla iletişim kur",
                    "dice": "1d20",
                    "skill": "nature",
                    "narrative": "Doğa ruhlarından bilgi alabilirsiniz."
                },
                {
                    "type": "find_magical_items",
                    "description": "Büyülü eşyaları ara",
                    "dice": "1d20",
                    "skill": "investigation",
                    "narrative": "Büyülü eşyalar bulabilirsiniz."
                }
            ]
        elif "hive" in previous_action.lower() or "warhammer" in previous_action.lower():
            return [
                {
                    "type": "coordinate_defense",
                    "description": "Savunma koordinasyonu yap",
                    "dice": "1d20",
                    "skill": "leadership",
                    "narrative": "Savunma sistemlerini koordine edebilirsiniz."
                },
                {
                    "type": "call_reinforcements",
                    "description": "Takviye kuvvet çağır",
                    "dice": "1d20",
                    "skill": "leadership",
                    "narrative": "Ek kuvvetler getirebilirsiniz."
                },
                {
                    "type": "fortify_position",
                    "description": "Pozisyonu güçlendir",
                    "dice": "1d20",
                    "skill": "military",
                    "narrative": "Savunma pozisyonlarını güçlendirebilirsiniz."
                }
            ]
        elif "cyberpunk" in previous_action.lower():
            return [
                {
                    "type": "hack_systems",
                    "description": "Güvenlik sistemlerini hackle",
                    "dice": "1d20",
                    "skill": "hacking",
                    "narrative": "Güvenlik sistemlerini atlatabilirsiniz."
                },
                {
                    "type": "negotiate_deals",
                    "description": "Gang liderleriyle anlaşma yap",
                    "dice": "1d20",
                    "skill": "persuasion",
                    "narrative": "Ganglerle işbirliği yapabilirsiniz."
                },
                {
                    "type": "gather_intel",
                    "description": "İstihbarat topla",
                    "dice": "1d20",
                    "skill": "investigation",
                    "narrative": "Önemli bilgiler toplayabilirsiniz."
                }
            ]
        else:
            # Genel bağlamsal aksiyonlar
            return [
                {
                    "type": "explore",
                    "description": "Çevreyi daha detaylı keşfet",
                    "dice": "1d20",
                    "skill": "perception",
                    "narrative": "Gizli geçitler veya tehlikeler bulabilirsiniz."
                },
                {
                    "type": "investigate",
                    "description": "Daha derin araştırma yap",
                    "dice": "1d20", 
                    "skill": "investigation",
                    "narrative": "Daha derin bilgiler elde edebilirsiniz."
                },
                {
                    "type": "interact",
                    "description": "NPC'lerle etkileşim kur",
                    "dice": "1d20",
                    "skill": "persuasion", 
                    "narrative": "Yerel halktan bilgi alabilirsiniz."
                },
                {
                    "type": "prepare",
                    "description": "Hazırlık yap",
                    "dice": "1d20",
                    "skill": "survival",
                    "narrative": "Gelecek tehlikeler için hazırlanabilirsiniz."
                }
            ]
    
    def _generate_action_result(self, player: Dict, action: Dict, dice_result: Optional[int]) -> str:
        """Aksiyon sonucu hikayesi üret - belirsiz sonuçlar"""
        player_name = player["character_name"]
        action_type = action.get("type")
        success = dice_result and dice_result >= 12
        
        # Başarı ve başarısızlık sonuçları karışık - bazen "başarı" kötü, "başarısızlık" iyi olabilir
        if action_type == "explore":
            if success:
                results = [
                    f"🔍 {player_name} çevreyi dikkatlice keşfetti ve gizli bir geçit buldu! Bu geçit sizi daha derinlere götürebilir.",
                    f"🔍 {player_name} çevreyi keşfetti ve bir hazine sandığı buldu! Ama sandık tuzaklı olabilir...",
                    f"🔍 {player_name} keşif sırasında bir ses duydu. Bu ses dost mu düşman mı?"
                ]
            else:
                results = [
                    f"🔍 {player_name} çevreyi keşfetti ama hiçbir şey bulamadı. Belki de daha dikkatli bakmak gerekiyor.",
                    f"🔍 {player_name} keşif sırasında bir tuzaktan kaçtı! Bazen hiçbir şey bulmamak daha iyidir.",
                    f"🔍 {player_name} hiçbir şey bulamadı ama bu da bir tür şans sayılabilir."
                ]
        
        elif action_type == "investigate":
            if success:
                results = [
                    f"🔎 {player_name} detaylı araştırma yaptı ve önemli bir ipucu buldu! Bu bilgi yolculuğunuzda işe yarayabilir.",
                    f"🔎 {player_name} araştırma sırasında eski bir kitap buldu. Bu kitap sırlar içeriyor olabilir.",
                    f"🔎 {player_name} önemli bir bilgi keşfetti ama bu bilgi tehlikeli olabilir."
                ]
            else:
                results = [
                    f"🔎 {player_name} araştırma yaptı ama hiçbir şey bulamadı. Belki de başka bir yerde aramak gerekiyor.",
                    f"🔎 {player_name} araştırma sırasında bir tuzaktan kaçtı! Bazen hiçbir şey bulmamak daha iyidir.",
                    f"🔎 {player_name} hiçbir şey bulamadı ama bu da bir tür şans sayılabilir."
                ]
        
        elif action_type == "talk":
            if success:
                results = [
                    f"💬 {player_name} başarıyla iletişim kurdu ve değerli bilgi aldı! Yerel halk size yardım etmeye hazır.",
                    f"💬 {player_name} konuşma sırasında bir müttefik buldu! Ama bu müttefik güvenilir mi?",
                    f"💬 {player_name} önemli bir bilgi aldı ama bu bilgi yanıltıcı olabilir."
                ]
            else:
                results = [
                    f"💬 {player_name} konuşmaya çalıştı ama kimse güvenmedi. Belki de farklı bir yaklaşım gerekiyor.",
                    f"💬 {player_name} konuşma sırasında bir düşmanla karşılaştı! Bazen susmak daha iyidir.",
                    f"💬 {player_name} hiçbir şey öğrenemedi ama bu da bir tür şans sayılabilir."
                ]
        
        elif action_type == "stealth":
            if success:
                results = [
                    f"👤 {player_name} gizlice ilerledi ve düşmanları fark etmedi! Bu avantaj sağlayabilir.",
                    f"👤 {player_name} sessizce hareket etti ve gizli bir geçit buldu!",
                    f"👤 {player_name} gizlice ilerledi ama bu yol tehlikeli olabilir."
                ]
            else:
                results = [
                    f"👤 {player_name} gizlice ilerlemeye çalıştı ama ses çıkardı! Düşmanlar uyandı.",
                    f"👤 {player_name} sessizce hareket edemedi ama bu da bir tür avantaj olabilir.",
                    f"👤 {player_name} gizlice ilerleyemedi ama bu da bir tür şans sayılabilir."
                ]
        
        elif action_type == "attack":
            if success:
                damage = random.randint(5, 15)
                results = [
                    f"⚔️ {player_name} saldırdı ve {damage} hasar verdi! Düşman geri çekiliyor.",
                    f"⚔️ {player_name} saldırısı başarılı oldu! Ama düşman daha güçlü olabilir.",
                    f"⚔️ {player_name} saldırdı ve {damage} hasar verdi! Ama bu saldırı düşmanı daha da öfkelendirdi."
                ]
            else:
                results = [
                    f"⚔️ {player_name} saldırdı ama ıskaladı! Düşman hala ayakta.",
                    f"⚔️ {player_name} saldırısı başarısız oldu! Ama bu düşmanı şaşırttı.",
                    f"⚔️ {player_name} ıskaladı ama bu da bir tür avantaj olabilir."
                ]
        
        elif action_type == "cast_spell":
            if success:
                results = [
                    f"🔮 {player_name} büyü yaptı ve etkili oldu! Büyü düşmanı etkiledi.",
                    f"🔮 {player_name} büyü başarılı oldu! Ama büyü beklenmedik sonuçlar doğurabilir.",
                    f"🔮 {player_name} büyü yaptı ve etkili oldu! Ama bu büyü tehlikeli olabilir."
                ]
            else:
                results = [
                    f"🔮 {player_name} büyü yapmaya çalıştı ama başarısız oldu! Mana kaybetti.",
                    f"🔮 {player_name} büyü başarısız oldu! Ama bu da bir tür avantaj olabilir.",
                    f"🔮 {player_name} büyü yapamadı ama bu da bir tür şans sayılabilir."
                ]
        
        else:
            results = [f"🎯 {player_name} bir aksiyon yaptı."]
        
        return random.choice(results)
    
    def process_player_action(self, player: Dict, action: Dict, dice_result: Optional[int] = None) -> Dict[str, Any]:
        """Oyuncu aksiyonunu işle ve sonucu döndür"""
        try:
            action_type = action.get("type", "general")
            action_description = action.get("description", "Bilinmeyen aksiyon")
            
            # Check if this is a combat action
            if action_type == "combat" or "combat" in action_description.lower():
                return self._process_combat_action(player, action, dice_result)
            
            # Regular action processing
            result = self._generate_action_result(player, action, dice_result)
            
            # Generate new actions based on the result
            new_actions = self._generate_new_actions(action_description, dice_result)
            
            # Handle story progression
            current_context = {
                "scenario_type": self.current_scenario,
                "location": result.get("location", "unknown"),
                "situation": result.get("situation", "exploration"),
                "npcs": result.get("npcs", [])
            }
            
            story_progression = self._handle_story_progression(action, current_context)
            
            return {
                "success": True,
                "narrative": result.get("narrative", "Aksiyon tamamlandı."),
                "new_actions": new_actions,
                "story_updates": story_progression.get("narrative_updates", []),
                "context_changes": story_progression.get("context_changes", {}),
                "dice_result": dice_result
            }
            
        except Exception as e:
            logger.error(f"Error processing player action: {e}")
            return {
                "success": False,
                "error": f"Aksiyon işlenirken hata oluştu: {str(e)}"
            }

    def _process_combat_action(self, player: Dict, action: Dict, dice_result: Optional[int] = None) -> Dict[str, Any]:
        """Process combat-specific actions with contextual narrative"""
        try:
            scenario_type = self.current_scenario or "fantasy"
            action_context = action.get("context", "")
            action_description = action.get("description", "")
            
            # Generate contextual combat narrative
            combat_data = {
                "enemies": action.get("enemies", ["Bilinmeyen Düşman"]),
                "players": [player],
                "scenario_type": scenario_type,
                "location": action.get("location", "unknown"),
                "situation": "combat"
            }
            
            combat_narrative = self.generate_combat_narrative(combat_data)
            
            # Generate contextual combat actions
            contextual_combat_actions = self._generate_contextual_combat_actions(
                scenario_type, 
                {"location": action.get("location", "unknown"), "situation": "combat"}, 
                combat_data
            )
            
            # Handle combat story progression
            story_progression = self._handle_combat_story_progression(action, combat_data, {
                "scenario_type": scenario_type,
                "location": action.get("location", "unknown"),
                "situation": "combat"
            })
            
            # Process the combat action result
            action_result = self._process_combat_action_result(player, action, dice_result)
            
            return {
                "success": True,
                "narrative": f"{combat_narrative}\n\n{action_result.get('narrative', '')}",
                "combat_actions": contextual_combat_actions,
                "story_updates": story_progression.get("narrative_updates", []),
                "combat_data": combat_data,
                "action_result": action_result,
                "dice_result": dice_result,
                "is_combat": True
            }
            
        except Exception as e:
            logger.error(f"Error processing combat action: {e}")
            return {
                "success": False,
                "error": f"Savaş aksiyonu işlenirken hata oluştu: {str(e)}",
                "is_combat": True
            }

    def _process_combat_action_result(self, player: Dict, action: Dict, dice_result: Optional[int] = None) -> Dict[str, Any]:
        """Process the result of a combat action"""
        action_type = action.get("type", "combat")
        action_context = action.get("context", "")
        
        # Default combat result
        result = {
            "narrative": "Savaş devam ediyor...",
            "damage_dealt": 0,
            "damage_taken": 0,
            "status_effects": [],
            "combat_advantage": False
        }
        
        # Process based on action context
        if action_context == "target_weak_points":
            if dice_result and dice_result >= 15:
                result.update({
                    "narrative": "Ejderhanın zayıf noktalarını başarıyla hedeflediniz! Kritik hasar verdiniz!",
                    "damage_dealt": 25,
                    "combat_advantage": True,
                    "status_effects": ["exposed_weak_points"]
                })
            else:
                result.update({
                    "narrative": "Ejderhanın zayıf noktalarını bulamadınız, ancak normal hasar verdiniz.",
                    "damage_dealt": 10
                })
                
        elif action_context == "hack_systems":
            if dice_result and dice_result >= 15:
                result.update({
                    "narrative": "Düşmanın sistemlerini başarıyla hack ettiniz! Düşman geçici olarak devre dışı!",
                    "damage_dealt": 15,
                    "status_effects": ["systems_disabled"],
                    "combat_advantage": True
                })
            else:
                result.update({
                    "narrative": "Hack girişimi başarısız oldu, ancak düşmanı rahatsız ettiniz.",
                    "damage_dealt": 5
                })
                
        elif action_context == "power_attack":
            if dice_result and dice_result >= 12:
                result.update({
                    "narrative": "Güçlü saldırınız düşmana ağır hasar verdi!",
                    "damage_dealt": 20
                })
            else:
                result.update({
                    "narrative": "Saldırınız düşmana hasar verdi.",
                    "damage_dealt": 8
                })
                
        elif action_context == "defensive_stance":
            result.update({
                "narrative": "Savunma pozisyonu aldınız. Gelecek saldırıya karşı korunmalısınız.",
                "damage_reduction": 0.5,
                "status_effects": ["defensive_stance"]
            })
            
        else:
            # Generic combat action
            if dice_result and dice_result >= 10:
                result.update({
                    "narrative": "Saldırınız başarılı! Düşmana hasar verdiniz.",
                    "damage_dealt": 12
                })
            else:
                result.update({
                    "narrative": "Saldırınız düşmana ulaşamadı.",
                    "damage_dealt": 0
                })
        
        return result
    
    def _generate_new_scene(self, action_type: str, dice_result: Optional[int]) -> str:
        """Yeni sahne hikayesi üret"""
        success = dice_result and dice_result >= 12
        
        if action_type == "explore" and success:
            scene_templates = [
                "Gizli geçit sizi yeni bir bölgeye götürüyor. Burada daha fazla tehlike ve ödül var.",
                "Keşif sonucu yeni bir alan açıldı. Bu bölge daha önce hiç keşfedilmemiş.",
                "Gizli geçit sizi mağaranın derinliklerine götürüyor. Burada eski sırlar gizli."
            ]
        elif action_type == "investigate" and success:
            scene_templates = [
                "Araştırma sonucu önemli bir bilgi elde ettiniz. Bu bilgi size yol gösterecek.",
                "Detaylı araştırma yeni ipuçları verdi. Bu ipuçları sizi hedefe götürecek.",
                "Araştırma sonucu gizli bir sır ortaya çıktı. Bu sır size güç verecek."
            ]
        elif action_type == "talk" and success:
            scene_templates = [
                "NPC size yardım etmeye hazır. Bu ittifak yolculuğunuzda işe yarayacak.",
                "Yerel halk size güveniyor. Bu güven yeni fırsatlar açacak.",
                "İletişim başarılı oldu. Artık daha fazla bilgiye erişiminiz var."
            ]
        else:
            scene_templates = [
                "Durum değişmedi. Belki de farklı bir yaklaşım denemek gerekiyor.",
                "Hiçbir şey olmadı. Yolculuğunuza devam etmek zorundasınız.",
                "Sonuç beklenenden farklı. Yeni stratejiler düşünmek gerekiyor."
            ]
        
        return random.choice(scene_templates)
    
    def generate_combat_narrative(self, combat_data: Dict) -> str:
        """Savaş hikayesi üret - Contextual ve story-driven combat"""
        enemies = combat_data.get("enemies", [])
        players = combat_data.get("players", [])
        scenario_type = combat_data.get("scenario_type", "fantasy")
        location = combat_data.get("location", "unknown")
        situation = combat_data.get("situation", "combat")
        
        if not enemies:
            return "Savaş bitti! Kahramanlarınız zafer kazandı."
        
        enemy = random.choice(enemies)
        player = random.choice(players) if players else {"character_name": "Kahraman"}
        
        # Contextual combat narratives based on scenario type and location
        contextual_combat_templates = {
            "fantasy": {
                "dragon_hunt": [
                    f"🐉 {enemy} mağaranın derinliklerinden çıkıyor! Kızıl alevler nefesinden süzülüyor ve {player['character_name']} kendini ejderhanın gölgesi altında buluyor.",
                    f"🔥 {enemy} kanatlarını açıp havaya yükseliyor! {player['character_name']} ejderhanın altında kalıyor ve sıcak hava akımları etrafını sarıyor.",
                    f"⚔️ {enemy} kuyruğunu savuruyor! {player['character_name']} ejderhanın öfkesini hissediyor ve savaş başlıyor!"
                ],
                "forest_ambush": [
                    f"🌲 Gölgelerden {enemy} ortaya çıkıyor! {player['character_name']} ormanın gizli tehlikeleriyle karşı karşıya.",
                    f"🗡️ {enemy} gizlice yaklaştı ve saldırıya geçti! {player['character_name']} kendini ani bir savaşın ortasında buluyor.",
                    f"👁️ {enemy} ağaçların arasından gözetliyor ve saldırıya hazırlanıyor! {player['character_name']} tehlikenin farkına varıyor."
                ],
                "ancient_ruins": [
                    f"🏛️ Antik harabelerin gölgelerinden {enemy} beliriyor! {player['character_name']} tarihin unutulmuş tehlikeleriyle karşılaşıyor.",
                    f"🗿 {enemy} antik tuzakların arasından çıkıyor! {player['character_name']} hem düşmanla hem de harabenin tehlikeleriyle savaşmalı.",
                    f"⚡ {enemy} antik büyülerle güçlendirilmiş görünüyor! {player['character_name']} büyülü bir savaşa hazırlanmalı."
                ]
            },
            "cyberpunk": {
                "urban_streets": [
                    f"🌃 Neon ışıklarının altında {enemy} beliriyor! {player['character_name']} şehrin karanlık sokaklarında tehlikeli bir savaşa girişiyor.",
                    f"💻 {enemy} cybernetik implantlarıyla güçlendirilmiş! {player['character_name']} teknolojinin tehlikeleriyle karşı karşıya.",
                    f"🚗 {enemy} hızla yaklaşıyor, cybernetic güçleriyle! {player['character_name']} modern bir savaşın ortasında kalıyor."
                ],
                "corporate_tower": [
                    f"🏢 {enemy} corporate güvenlik sistemi olarak devreye giriyor! {player['character_name']} yüksek teknoloji savaşına hazırlanmalı.",
                    f"🔒 {enemy} şirketin son savunma hattı! {player['character_name']} corporate dünyasının tehlikeleriyle yüzleşmeli.",
                    f"⚡ {enemy} elektrik sistemlerini kontrol ediyor! {player['character_name']} teknolojik bir savaşın ortasında."
                ]
            },
            "warhammer": {
                "hive_city": [
                    f"🏭 {enemy} hive şehrinin derinliklerinden çıkıyor! {player['character_name']} İmperium'un en tehlikeli düşmanlarıyla karşı karşıya.",
                    f"🛡️ {enemy} ork teknolojisiyle donatılmış! {player['character_name']} xenos tehdidiyle savaşmalı.",
                    f"⚔️ {enemy} warboss'un emriyle saldırıya geçiyor! {player['character_name']} İmperium'u korumak için savaşmalı."
                ],
                "space_marine": [
                    f"🛡️ {enemy} Space Marine power armor'ı ile yaklaşıyor! {player['character_name']} Astartes savaş taktikleriyle yüzleşmeli.",
                    f"⚔️ {enemy} bolter'ını doğrultuyor! {player['character_name']} İmperium'un en güçlü savaşçılarıyla karşı karşıya.",
                    f"🔱 {enemy} chainsword'unu çekiyor! {player['character_name']} yakın dövüş savaşına hazırlanmalı."
                ]
            }
        }
        
        # Get contextual templates based on scenario type
        scenario_templates = contextual_combat_templates.get(scenario_type, contextual_combat_templates["fantasy"])
        
        # Get location-specific templates
        location_templates = scenario_templates.get(location, scenario_templates.get("dragon_hunt", [
            f"⚔️ {enemy} ile karşı karşıya! {player['character_name']} savaşa hazırlanmalı!",
            f"🗡️ {enemy} saldırıya geçti! {player['character_name']} savunmaya geçiyor!",
            f"🔥 {enemy} özel bir saldırı hazırlıyor! {player['character_name']} dikkatli olmalı!",
            f"🛡️ {player['character_name']} saldırıya geçiyor! {enemy} savunmaya çekiliyor!"
        ]))
        
        return random.choice(location_templates)

    def _generate_contextual_combat_actions(self, scenario_type: str, current_context: Dict, combat_data: Dict) -> List[Dict]:
        """Generate contextual combat actions based on scenario, location, and situation"""
        contextual_combat_actions = []
        
        enemies = combat_data.get("enemies", [])
        location = current_context.get("location", "unknown")
        situation = current_context.get("situation", "combat")
        
        # Scenario-specific combat actions
        if scenario_type == "fantasy":
            if "dragon" in str(enemies).lower() or "ejderha" in str(enemies).lower():
                contextual_combat_actions.extend([
                    {
                        "type": "combat",
                        "description": "Ejderhanın zayıf noktalarını hedefle",
                        "dice": "1d20",
                        "skill": "perception",
                        "narrative": "Ejderhanın pulları arasındaki zayıf noktaları arıyorsunuz.",
                        "context": "target_weak_points",
                        "damage_multiplier": 1.5,
                        "requirements": {"perception": 15}
                    },
                    {
                        "type": "combat",
                        "description": "Alev nefesinden kaçın",
                        "dice": "1d20",
                        "skill": "dexterity",
                        "narrative": "Ejderhanın alev nefesinden kaçınmaya çalışıyorsunuz.",
                        "context": "dodge_breath",
                        "damage_reduction": 0.5,
                        "requirements": {"dexterity": 14}
                    },
                    {
                        "type": "combat",
                        "description": "Mağara çökmesini tetikle",
                        "dice": "1d20",
                        "skill": "strength",
                        "narrative": "Mağaranın tavanındaki zayıf noktaları hedefliyorsunuz.",
                        "context": "cave_collapse",
                        "area_effect": True,
                        "requirements": {"strength": 16}
                    }
                ])
            elif "forest" in location.lower():
                contextual_combat_actions.extend([
                    {
                        "type": "combat",
                        "description": "Ağaçlardan avantaj elde et",
                        "dice": "1d20",
                        "skill": "acrobatics",
                        "narrative": "Ağaçlara tırmanarak yüksek pozisyondan saldırı yapıyorsunuz.",
                        "context": "high_ground",
                        "damage_multiplier": 1.2,
                        "requirements": {"acrobatics": 12}
                    },
                    {
                        "type": "combat",
                        "description": "Ormanın gizliliğini kullan",
                        "dice": "1d20",
                        "skill": "stealth",
                        "narrative": "Ormanın gölgelerini kullanarak gizlice yaklaşıyorsunuz.",
                        "context": "forest_stealth",
                        "critical_chance": 0.3,
                        "requirements": {"stealth": 13}
                    }
                ])
                
        elif scenario_type == "cyberpunk":
            if "corporate" in location.lower():
                contextual_combat_actions.extend([
                    {
                        "type": "combat",
                        "description": "Sistemleri hack et",
                        "dice": "1d20",
                        "skill": "technology",
                        "narrative": "Düşmanın cybernetic sistemlerini hack etmeye çalışıyorsunuz.",
                        "context": "hack_systems",
                        "status_effect": "disabled",
                        "requirements": {"technology": 15}
                    },
                    {
                        "type": "combat",
                        "description": "Elektrik sistemlerini devre dışı bırak",
                        "dice": "1d20",
                        "skill": "engineering",
                        "narrative": "Bina elektrik sistemlerini devre dışı bırakıyorsunuz.",
                        "context": "disable_power",
                        "area_effect": True,
                        "requirements": {"engineering": 14}
                    }
                ])
            elif "streets" in location.lower():
                contextual_combat_actions.extend([
                    {
                        "type": "combat",
                        "description": "Araçları kalkan olarak kullan",
                        "dice": "1d20",
                        "skill": "tactics",
                        "narrative": "Park etmiş araçları kalkan olarak kullanıyorsunuz.",
                        "context": "vehicle_cover",
                        "defense_bonus": 2,
                        "requirements": {"tactics": 12}
                    },
                    {
                        "type": "combat",
                        "description": "Neon ışıklarını karışıklık yarat",
                        "dice": "1d20",
                        "skill": "stealth",
                        "narrative": "Neon ışıklarını kullanarak düşmanın görüşünü karıştırıyorsunuz.",
                        "context": "neon_distraction",
                        "accuracy_penalty": -2,
                        "requirements": {"stealth": 13}
                    }
                ])
                
        elif scenario_type == "warhammer":
            if "hive" in location.lower():
                contextual_combat_actions.extend([
                    {
                        "type": "combat",
                        "description": "Imperial pozisyonunu kullan",
                        "dice": "1d20",
                        "skill": "tactics",
                        "narrative": "Imperial savunma pozisyonlarını stratejik olarak kullanıyorsunuz.",
                        "context": "imperial_position",
                        "defense_bonus": 3,
                        "requirements": {"tactics": 14}
                    },
                    {
                        "type": "combat",
                        "description": "Ork teknolojisini istismar et",
                        "dice": "1d20",
                        "skill": "technology",
                        "narrative": "Ork teknolojisindeki zayıflıkları istismar ediyorsunuz.",
                        "context": "exploit_ork_tech",
                        "damage_multiplier": 1.3,
                        "requirements": {"technology": 15}
                    }
                ])
        
        # Universal combat actions
        contextual_combat_actions.extend([
            {
                "type": "combat",
                "description": "Güçlü saldırı",
                "dice": "1d20",
                "skill": "strength",
                "narrative": "Tüm gücünüzle saldırıya geçiyorsunuz.",
                "context": "power_attack",
                "damage_multiplier": 1.2,
                "requirements": {"strength": 12}
            },
            {
                "type": "combat",
                "description": "Savunma pozisyonu al",
                "dice": "1d20",
                "skill": "defense",
                "narrative": "Savunma pozisyonu alıyorsunuz.",
                "context": "defensive_stance",
                "defense_bonus": 2,
                "requirements": {"defense": 10}
            },
            {
                "type": "combat",
                "description": "Çeviklikle kaç",
                "dice": "1d20",
                "skill": "dexterity",
                "narrative": "Çevik hareketlerle kaçmaya çalışıyorsunuz.",
                "context": "agile_escape",
                "escape_chance": 0.7,
                "requirements": {"dexterity": 13}
            }
        ])
        
        return contextual_combat_actions

    def _handle_combat_story_progression(self, combat_action: Dict, combat_data: Dict, current_context: Dict) -> Dict:
        """Handle story progression during combat"""
        action_context = combat_action.get("context", "")
        scenario_type = current_context.get("scenario_type", "fantasy")
        
        narrative_updates = []
        story_changes = {}
        
        # Combat-specific story progression
        if action_context == "target_weak_points":
            if scenario_type == "fantasy":
                narrative_updates.append("Ejderhanın zayıf noktalarını başarıyla hedeflediniz! Canavar acı içinde kıvranıyor.")
                story_changes["dragon_wounded"] = True
                story_changes["combat_advantage"] = "weak_points_exposed"
                
        elif action_context == "hack_systems":
            if scenario_type == "cyberpunk":
                narrative_updates.append("Düşmanın cybernetic sistemleri başarıyla hack edildi! Teknolojik avantaj elde ettiniz.")
                story_changes["systems_hacked"] = True
                story_changes["enemy_disabled"] = True
                
        elif action_context == "imperial_position":
            if scenario_type == "warhammer":
                narrative_updates.append("Imperial savunma pozisyonlarını stratejik olarak kullandınız! İmperium'un gücü sizinle!")
                story_changes["imperial_advantage"] = True
                story_changes["combat_bonus"] = "imperial_tactics"
        
        # Update combat data with story changes
        combat_data.update(story_changes)
        
        return {
            "narrative_updates": narrative_updates,
            "story_changes": story_changes,
            "combat_data": combat_data
        }
    
    def generate_quest_narrative(self, quest_data: Dict) -> str:
        """Quest hikayesi üret"""
        quest_name = quest_data.get("name", "Bilinmeyen Görev")
        quest_type = quest_data.get("type", "explore")
        
        quest_templates = {
            "explore": f"🗺️ Yeni bir görev: {quest_name}. Bu görev sizi bilinmeyen bölgelere götürecek.",
            "combat": f"⚔️ Tehlikeli görev: {quest_name}. Bu görev savaş gerektiriyor.",
            "social": f"💬 Sosyal görev: {quest_name}. Bu görev iletişim becerileri gerektiriyor.",
            "magic": f"🔮 Büyü görevi: {quest_name}. Bu görev büyü becerileri gerektiriyor."
        }
        
        return quest_templates.get(quest_type, quest_templates["explore"])
    
    def get_narrative_history(self, limit: int = 10) -> List[Dict]:
        """Hikaye geçmişini getir"""
        return self.narrative_history[-limit:] if limit else self.narrative_history
    
    def get_current_narrative(self) -> str:
        """Mevcut hikayeyi getir"""
        if self.narrative_history:
            return self.narrative_history[-1]["narrative"]
        return "Hikaye henüz başlamadı."
    
    def generate_scenario(self, theme: str, difficulty: str = "medium") -> Dict[str, Any]:
        """LLM ile senaryo üret"""
        logger.info(f"Generating scenario: theme={theme}, difficulty={difficulty}")
        
        # Tema bazlı senaryo şablonları
        scenario_templates = {
            "fantasy": {
                "title": f"🐉 {theme.title()} Macerası",
                "description": f"{theme} temasında epik bir fantazi macerası",
                "type": "fantasy",
                "difficulty": difficulty,
                "locations": ["Orman", "Mağara", "Şehir", "Kale"],
                "enemies": ["Goblin", "Ork", "Ejderha"],
                "npcs": ["Bilge Keşiş", "Demirci", "Kral"],
                "quests": ["Hazine Bul", "Ejderhayı Yen", "Krallığı Kurtar"]
            },
            "warhammer": {
                "title": f"🛡️ {theme.title()} Görevi",
                "description": f"{theme} temasında Warhammer 40K görevi",
                "type": "warhammer", 
                "difficulty": difficulty,
                "locations": ["Imperial Üs", "Ork Kampı", "Antik Harabeler"],
                "enemies": ["Ork Boy", "Ork Nob", "Ork Warboss"],
                "npcs": ["Imperial Komutan", "Tech-Priest", "Inquisitor"],
                "quests": ["Üssü Savun", "Warboss'u Yok Et", "Artefakt Bul"]
            },
            "pyraxis": {
                "title": f"🔥 {theme.title()} Efsanesi",
                "description": f"{theme} temasında Pyraxis efsanesi",
                "type": "fantasy",
                "difficulty": difficulty,
                "locations": ["Orman Girişi", "Kuzey Dağları", "Pyraxis Mağarası"],
                "enemies": ["Ork Lideri", "Alev Ruhu", "Kırmızı Ejderha Pyraxis"],
                "npcs": ["Orman Perisi", "Demirci Ustası", "Flame Oracle Vynn"],
                "quests": ["Ormanı Keşfet", "Ork Liderini Yen", "Pyraxis ile Yüzleş"]
            }
        }
        
        # Tema seçimi
        if "warhammer" in theme.lower() or "40k" in theme.lower():
            template = scenario_templates["warhammer"]
        elif "pyraxis" in theme.lower() or "ejderha" in theme.lower():
            template = scenario_templates["pyraxis"]
        else:
            template = scenario_templates["fantasy"]
        
        # Zorluk seviyesine göre ayarlamalar
        difficulty_multipliers = {
            "easy": 0.7,
            "medium": 1.0,
            "hard": 1.3,
            "epic": 1.6
        }
        
        multiplier = difficulty_multipliers.get(difficulty, 1.0)
        
        # Senaryo oluştur
        scenario = {
            "id": f"{theme.lower()}_{difficulty}_{random.randint(1000, 9999)}",
            "name": template["title"],
            "description": template["description"],
            "type": template["type"],
            "difficulty": difficulty,
            "locations": template["locations"],
            "enemies": template["enemies"],
            "npcs": template["npcs"],
            "quests": template["quests"],
            "created_at": datetime.now().isoformat(),
            "ai_generated": True
        }
        
        logger.info(f"Generated scenario: {scenario['name']}")
        
        # Üretilen senaryoyu kaydet
        self.generated_scenarios.append(scenario)
        self._save_persistent_data()
        
        return scenario 

    def _generate_contextual_actions(self, scenario_type: str, current_context: Dict) -> List[Dict]:
        """Generate contextual actions based on current scenario and context"""
        
        # Base contextual actions
        contextual_actions = []
        
        # Get current location and situation
        location = current_context.get('location', 'unknown')
        situation = current_context.get('situation', 'exploration')
        npcs_present = current_context.get('npcs', [])
        
        # Scenario-specific contextual actions
        if "ejderha" in scenario_type.lower() or "dragon" in scenario_type.lower():
            contextual_actions.extend([
                {
                    "type": "investigate",
                    "description": "Ejderha izlerini takip et",
                    "dice": "1d20",
                    "skill": "survival",
                    "narrative": "Ejderhanın geçtiği yolları bulabilirsiniz.",
                    "context": "dragon_hunting"
                },
                {
                    "type": "explore",
                    "description": "Yakılmış köyü araştır",
                    "dice": "1d20", 
                    "skill": "investigation",
                    "narrative": "Köydeki hasarı inceleyerek ejderha hakkında ipuçları bulabilirsiniz.",
                    "context": "village_investigation"
                },
                {
                    "type": "stealth",
                    "description": "Gizlice yaklaş",
                    "dice": "1d20",
                    "skill": "stealth", 
                    "narrative": "Ejderhaya fark ettirmeden yaklaşmaya çalışırsınız.",
                    "context": "stealth_approach"
                }
            ])
            
        elif "büyülü orman" in scenario_type.lower() or "magical forest" in scenario_type.lower():
            contextual_actions.extend([
                {
                    "type": "nature",
                    "description": "Ağaçlarla konuş",
                    "dice": "1d20",
                    "skill": "nature",
                    "narrative": "Büyülü ağaçlardan bilgi almaya çalışırsınız.",
                    "context": "tree_communication"
                },
                {
                    "type": "explore", 
                    "description": "Gizli patikaları araştır",
                    "dice": "1d20",
                    "skill": "perception",
                    "narrative": "Ormanın gizli patikalarını bulmaya çalışırsınız.",
                    "context": "hidden_paths"
                },
                {
                    "type": "magic",
                    "description": "Büyülü enerjiyi hissed",
                    "dice": "1d20",
                    "skill": "arcana",
                    "narrative": "Çevredeki büyülü enerjiyi algılamaya çalışırsınız.",
                    "context": "magical_sensing"
                }
            ])
            
        elif "cyberpunk" in scenario_type.lower():
            contextual_actions.extend([
                {
                    "type": "hack",
                    "description": "Sistemi hack et",
                    "dice": "1d20",
                    "skill": "technology",
                    "narrative": "Bilgisayar sistemlerine sızma girişiminde bulunursunuz.",
                    "context": "system_hack"
                },
                {
                    "type": "stealth",
                    "description": "Gölgelerde gizlen",
                    "dice": "1d20", 
                    "skill": "stealth",
                    "narrative": "Şehrin gölgelerinde gizlice hareket edersiniz.",
                    "context": "urban_stealth"
                },
                {
                    "type": "social",
                    "description": "Yerel bilgi topla",
                    "dice": "1d20",
                    "skill": "persuasion", 
                    "narrative": "Yerel halktan bilgi toplamaya çalışırsınız.",
                    "context": "information_gathering"
                }
            ])
            
        elif "warhammer" in scenario_type.lower() or "hive" in scenario_type.lower():
            contextual_actions.extend([
                {
                    "type": "combat",
                    "description": "Savunma pozisyonu al",
                    "dice": "1d20",
                    "skill": "tactics",
                    "narrative": "Stratejik bir savunma pozisyonu alırsınız.",
                    "context": "defensive_position"
                },
                {
                    "type": "explore",
                    "description": "Tehlikeli bölgeleri keşfet",
                    "dice": "1d20",
                    "skill": "survival",
                    "narrative": "Hive şehrinin tehlikeli bölgelerini keşfedersiniz.",
                    "context": "dangerous_exploration"
                },
                {
                    "type": "leadership", 
                    "description": "Korumaları organize et",
                    "dice": "1d20",
                    "skill": "leadership",
                    "narrative": "Mevcut korumaları organize edersiniz.",
                    "context": "guard_organization"
                }
            ])
        
        # Location-specific actions
        if location == "forest":
            contextual_actions.extend([
                {
                    "type": "survival",
                    "description": "Yiyecek topla",
                    "dice": "1d20",
                    "skill": "survival",
                    "narrative": "Ormanın doğal kaynaklarından yiyecek toplarsınız.",
                    "context": "food_gathering"
                }
            ])
        elif location == "city":
            contextual_actions.extend([
                {
                    "type": "social",
                    "description": "Pazar yeri araştır",
                    "dice": "1d20",
                    "skill": "investigation",
                    "narrative": "Pazar yerinde bilgi ve malzeme ararsınız.",
                    "context": "market_research"
                }
            ])
        
        # Situation-specific actions
        if situation == "combat":
            contextual_actions.extend([
                {
                    "type": "combat",
                    "description": "Saldırı pozisyonu al",
                    "dice": "1d20",
                    "skill": "tactics",
                    "narrative": "Saldırı için stratejik pozisyon alırsınız.",
                    "context": "attack_position"
                },
                {
                    "type": "defense",
                    "description": "Savunma pozisyonu al", 
                    "dice": "1d20",
                    "skill": "tactics",
                    "narrative": "Savunma için stratejik pozisyon alırsınız.",
                    "context": "defense_position"
                }
            ])
        elif situation == "negotiation":
            contextual_actions.extend([
                {
                    "type": "social",
                    "description": "Diplomatik yaklaş",
                    "dice": "1d20",
                    "skill": "persuasion",
                    "narrative": "Diplomatik bir yaklaşım benimsersiniz.",
                    "context": "diplomatic_approach"
                },
                {
                    "type": "intimidation",
                    "description": "Tehdit et",
                    "dice": "1d20",
                    "skill": "intimidation", 
                    "narrative": "Tehditkar bir tavır benimsersiniz.",
                    "context": "threatening_approach"
                }
            ])
        
        # NPC interaction actions
        if npcs_present:
            contextual_actions.extend([
                {
                    "type": "social",
                    "description": "NPC ile konuş",
                    "dice": "1d20",
                    "skill": "persuasion",
                    "narrative": "Mevcut NPC ile konuşmaya çalışırsınız.",
                    "context": "npc_conversation"
                },
                {
                    "type": "investigate",
                    "description": "NPC'yi gözlemle",
                    "dice": "1d20",
                    "skill": "insight",
                    "narrative": "NPC'nin davranışlarını ve niyetlerini analiz edersiniz.",
                    "context": "npc_observation"
                }
            ])
        
        return contextual_actions 

    def _handle_story_progression(self, player_action: Dict, current_context: Dict) -> Dict:
        """Handle story progression based on player actions and current context"""
        
        # Extract action details
        action_type = player_action.get('type', 'explore')
        action_context = player_action.get('context', 'general')
        
        # Get current story state
        story_progress = current_context.get('story_progress', 0)
        completed_events = current_context.get('completed_events', [])
        
        # Generate story progression based on action
        progression_result = {
            'new_scene': None,
            'narrative_update': '',
            'context_changes': {},
            'unlocked_events': [],
            'story_milestones': []
        }
        
        # Action-specific story progression
        if action_type == 'investigate':
            if action_context == 'dragon_hunting':
                progression_result.update({
                    'narrative_update': 'Ejderha izlerini takip ederken, yerde büyük pençe izleri buldunuz. İzler sizi dağın eteklerine doğru yönlendiriyor.',
                    'context_changes': {
                        'location': 'mountain_foot',
                        'clues_found': current_context.get('clues_found', 0) + 1,
                        'dragon_distance': 'near'
                    },
                    'unlocked_events': ['dragon_lair_discovery']
                })
            elif action_context == 'village_investigation':
                progression_result.update({
                    'narrative_update': 'Köydeki hasarı incelerken, ejderhanın saldırı şeklinden bu yaratığın yaşlı ve deneyimli olduğunu anlıyorsunuz.',
                    'context_changes': {
                        'dragon_age': 'elder',
                        'village_state': 'destroyed',
                        'survivors_found': True
                    }
                })
                
        elif action_type == 'explore':
            if action_context == 'hidden_paths':
                progression_result.update({
                    'narrative_update': 'Gizli patikaları araştırırken, ağaçların arasından parlayan bir ışık gördünüz. Büyülü bir glade\'e çıktınız.',
                    'context_changes': {
                        'location': 'magical_glade',
                        'magical_energy': 'high',
                        'discovered_areas': current_context.get('discovered_areas', []) + ['magical_glade']
                    },
                    'unlocked_events': ['ancient_tree_encounter']
                })
            elif action_context == 'dangerous_exploration':
                progression_result.update({
                    'narrative_update': 'Hive şehrinin tehlikeli bölgelerini keşfederken, ork istilasının izlerini buldunuz. Savaş yakın.',
                    'context_changes': {
                        'ork_threat_level': 'high',
                        'battle_imminent': True,
                        'defense_preparation_time': 'limited'
                    }
                })
                
        elif action_type == 'combat':
            if action_context == 'defensive_position':
                progression_result.update({
                    'narrative_update': 'Savunma pozisyonu alırken, düşmanın yaklaştığını görüyorsunuz. Savaş başlamak üzere.',
                    'context_changes': {
                        'combat_phase': 'preparation',
                        'enemy_position': 'approaching',
                        'defense_bonus': 5
                    }
                })
                
        elif action_type == 'social':
            if action_context == 'npc_conversation':
                # Generate dynamic NPC conversation
                npc_response = self._generate_npc_response(current_context)
                progression_result.update({
                    'narrative_update': f'NPC ile konuşurken: "{npc_response}"',
                    'context_changes': {
                        'npc_trust': current_context.get('npc_trust', 0) + 1,
                        'information_gained': True
                    }
                })
                
        elif action_type == 'magic':
            if action_context == 'magical_sensing':
                progression_result.update({
                    'narrative_update': 'Büyülü enerjiyi algılarken, çevredeki büyünün güçlü bir varlık tarafından kontrol edildiğini hissediyorsunuz.',
                    'context_changes': {
                        'magical_presence': 'powerful',
                        'magical_entity_detected': True,
                        'magical_energy_level': 'intense'
                    },
                    'unlocked_events': ['magical_entity_encounter']
                })
        
        # Update story progress
        new_progress = story_progress + 10
        progression_result['story_milestones'] = self._check_story_milestones(new_progress, completed_events)
        
        return progression_result
    
    def _generate_npc_response(self, current_context: Dict) -> str:
        """Generate rich, character-driven responses with personality and depth"""
        
        scenario_type = current_context.get('scenario_type', 'fantasy')
        npc_type = current_context.get('npc_type', 'villager')
        current_mood = current_context.get('npc_mood', 'neutral')
        
        # Rich character responses with personality, appearance, and dialogue
        character_responses = {
            'fantasy': {
                'villager': {
                    'friendly': "**Eldrin the Wise** gözlerini kısarak size bakıyor. Uzun beyaz sakalı rüzgarda dalgalanıyor, büyülü asası hafifçe parlıyor. 'Yolcu, bu ormanın sırları tehlikeli. Ama cesaretiniz varsa, size rehberlik edebilirim.'",
                    'neutral': "**Lyra the Ranger** ağaçların arasından çıkıyor. Yeşil pelerini ve uzun yayıyla, ormanın en deneyimli avcısı olduğu belli. 'Bu bölgede tehlikeli yaratıklar var. Dikkatli olmalısınız.'",
                    'suspicious': "**Thorin the Blacksmith** demirci dükkanının önünde duruyor. Güçlü kolları ve yanmış yüzü, yılların deneyimini taşıyor. 'Silahlarınızı kontrol ettiniz mi? Bu yolculukta güvenilir ekipman hayat kurtarır.'"
                },
                'merchant': {
                    'friendly': "**Mystra the Enchantress** büyülü ışıklar arasında beliriyor. Mor elbiseleri ve parlayan gözleri, güçlü bir büyücü olduğunu gösteriyor. 'Büyü bu ormanın her yerinde. Ama kontrol edilmezse tehlikeli olabilir.'",
                    'neutral': "**Grimwald the Trader** pahalı kıyafetleri ve altın dişleriyle gülümsüyor. Karavanından çeşitli eşyalar sergiliyor. 'En kaliteli malzemeler burada. Fiyatlar uygun, kalite garantili.'",
                    'suspicious': "**Shadow the Rogue** gölgeler arasından çıkıyor. Siyah kıyafetleri ve keskin bakışları, tehlikeli bir karakter olduğunu gösteriyor. 'Bilgi değerli bir meta. Önce ödeme, sonra bilgi.'"
                },
                'wizard': {
                    'friendly': "**Archmage Zephyr** büyülü enerji halesiyle çevrili. Mavi cübbesi ve parlayan gözleri, güçlü bir büyücü olduğunu gösteriyor. 'Büyülü güçleriniz varsa, size öğretebilirim. Ama önce sınavdan geçmelisiniz.'",
                    'neutral': "**Sage Elara** eski kitaplar arasında oturuyor. Bilgelik dolu gözleri ve sakin tavrı, uzun yılların deneyimini taşıyor. 'Büyü ile ilgili sorularınız mı var? Bilgi paylaşmak için hazırım.'",
                    'suspicious': "**Dark Sorcerer Malakar** karanlık enerjiyle çevrili. Kırmızı gözleri ve tehlikeli aura'sı, güçlü ama tehlikeli bir büyücü olduğunu gösteriyor. 'Büyü gücünüzü kanıtlamadan size hiçbir şey söyleyemem.'"
                }
            },
            'warhammer': {
                'villager': {
                    'friendly': "**Commissar Valen** sert bakışlarıyla size yaklaşıyor. Imperial Guard üniforması ve güçlü duruşu, İmparator'a olan sadakatini gösteriyor. 'Soldier, bu savaşta her adım önemli. İmparator bizi izliyor.'",
                    'neutral': "**Tech-Priest Zeta-7** mekanik sesiyle konuşuyor. Kırmızı cübbesi ve mekanik uzuvları, Adeptus Mechanicus'un teknolojik gücünü yansıtıyor. 'Machine Spirit bu bölgede güçlü. Sistemleri kontrol etmeliyiz.'",
                    'suspicious': "**Sergeant Marcus** yaralı ama kararlı. Battle-worn armor'ı ve yorgun gözleri, uzun savaş deneyimini anlatıyor. 'Bu pozisyonu korumalıyız. Orklar yaklaşıyor.'"
                },
                'merchant': {
                    'friendly': "**Medicae Sister Helena** beyaz cübbesiyle yaralıları tedavi ediyor. Şefkatli ama kararlı bakışları, İmparator'un şifa veren elini temsil ediyor. 'Yaralarınızı kontrol edelim. Savaş henüz bitmedi.'",
                    'neutral': "**Arms Dealer Viktor** ağır silahlar sergiliyor. Güçlü kolları ve profesyonel tavrı, güvenilir bir tüccar olduğunu gösteriyor. 'En kaliteli Imperial silahları. Her savaş için uygun.'",
                    'suspicious': "**Rogue Trader Darius** pahalı kıyafetleri ve soğuk bakışlarıyla duruyor. Şüpheli işler yaptığı belli, ama gerekli malzemeleri sağlıyor. 'Fiyatlar yüksek, ama kalite garantili.'"
                },
                'wizard': {
                    'friendly': "**Librarian Astor** psykik güçleriyle çevrili. Mavi cübbesi ve parlayan gözleri, güçlü bir psiker olduğunu gösteriyor. 'Warp'ın güçlerini kontrol etmek tehlikeli. Size öğretebilirim.'",
                    'neutral': "**Sanctioned Psyker Kira** psykik enerji halesiyle duruyor. Kontrollü güçleri ve dikkatli tavrı, eğitimli bir psiker olduğunu gösteriyor. 'Psykik güçlerle ilgili sorularınız mı var?'",
                    'suspicious': "**Rogue Psyker Malice** kontrolsüz psykik güçleriyle tehlikeli görünüyor. Karanlık aura'sı ve tehlikeli bakışları, tehlikeli bir karakter olduğunu gösteriyor. 'Gücünüzü kanıtlamadan size hiçbir şey söyleyemem.'"
                }
            },
            'cyberpunk': {
                'villager': {
                    'friendly': "**Netrunner Shadow** hologramik görüntüsü yanıp sönüyor. Siyah kıyafetleri ve dijital gözleri, matrix'in en tehlikeli hacker'ı olduğunu gösteriyor. 'Network'te tehlikeli oyunlar oynanıyor. Dikkatli olun.'",
                    'neutral': "**Street Samurai Blade** neon ışıkları altında duruyor. Cybernetic uzuvları ve keskin kılıcı, sokağın en ölümcül savaşçısı olduğunu anlatıyor. 'Bu sokaklar kanla yazılmış. Her köşe bir savaş alanı.'",
                    'suspicious': "**Gang Leader Viper** tehlikeli bakışlarıyla size yaklaşıyor. Dövmeleri ve silahları, sokağın en güçlü gang lideri olduğunu gösteriyor. 'Bu mahalle bizim. Ne istiyorsunuz?'"
                },
                'merchant': {
                    'friendly': "**Fixer Silver** pahalı takım elbisesi ve altın dişleriyle gülümsüyor. Şehrin en güvenilir bilgi kaynağı, herkesin sırrını biliyor. 'Bilgi bu şehirde en değerli para birimi. Ne arıyorsunuz?'",
                    'neutral': "**Corpo Agent Nova** şirket üniforması ve soğuk bakışlarıyla yaklaşıyor. Yüksek teknoloji ekipmanları ve profesyonel duruşu, güçlü bir şirket temsilcisi olduğunu gösteriyor. 'Şirket çıkarları her şeyden önce gelir. Anlaşma yapalım.'",
                    'suspicious': "**Black Market Dealer Ghost** gölgeler arasından çıkıyor. Kontrolsüz cyberware'leri ve tehlikeli bakışları, yasadışı işler yaptığını gösteriyor. 'Özel malzemeler. Fiyatlar yüksek, ama kalite garantili.'"
                },
                'wizard': {
                    'friendly': "**AI Programmer Nexus** hologramik arayüzüyle konuşuyor. Dijital gözleri ve teknolojik ekipmanları, yapay zeka uzmanı olduğunu gösteriyor. 'AI'lar bu şehirde her yerde. Kontrol etmek tehlikeli.'",
                    'neutral': "**Tech Guru Matrix** dijital cihazlarla çevrili. Bilgisayar terminali ve hologramik ekranları, teknoloji uzmanı olduğunu gösteriyor. 'Teknoloji ile ilgili sorularınız mı var? Sistemleri kontrol edebilirim.'",
                    'suspicious': "**Rogue AI Controller** tehlikeli dijital aura'sıyla beliriyor. Kontrolsüz yapay zeka güçleri ve tehlikeli bakışları, tehlikeli bir karakter olduğunu gösteriyor. 'Gücünüzü kanıtlamadan size hiçbir şey söyleyemem.'"
                }
            }
        }
        
        # Get scenario-specific responses
        scenario_responses = character_responses.get(scenario_type, character_responses['fantasy'])
        npc_responses = scenario_responses.get(npc_type, scenario_responses['villager'])
        
        return npc_responses.get(current_mood, "**Mysterious Character** size yaklaşıyor. Gözlerinde hem tecrübe hem de gizem var. 'Bu yolculukta size yardım edebilirim.'")
    
    def _check_story_milestones(self, progress: int, completed_events: List) -> List:
        """Check for story milestones based on progress"""
        
        milestones = []
        
        if progress >= 25 and 'first_encounter' not in completed_events:
            milestones.append({
                'name': 'first_encounter',
                'description': 'İlk büyük karşılaşma',
                'unlocked': True
            })
            
        if progress >= 50 and 'midpoint_revelation' not in completed_events:
            milestones.append({
                'name': 'midpoint_revelation',
                'description': 'Hikayenin ortasında önemli keşif',
                'unlocked': True
            })
            
        if progress >= 75 and 'final_preparation' not in completed_events:
            milestones.append({
                'name': 'final_preparation',
                'description': 'Final savaşı için hazırlık',
                'unlocked': True
            })
            
        return milestones 

    def get_contextual_actions_with_systems(self, scenario_type: str, current_context: Dict, player_id: str = None) -> List[Dict]:
        """Get contextual actions integrating all systems"""
        contextual_actions = []
        
        # Get base contextual actions
        base_actions = self._generate_contextual_actions(scenario_type, current_context)
        contextual_actions.extend(base_actions)
        
        if player_id:
            # Get inventory-based actions
            inventory_actions = self.inventory_system.get_contextual_actions(
                player_id, scenario_type, current_context
            )
            contextual_actions.extend(inventory_actions)
            
            # Get skill-based actions
            skill_actions = self.skill_system.get_contextual_skill_actions(
                player_id, scenario_type, current_context
            )
            contextual_actions.extend(skill_actions)
            
            # Get personalized actions from AI learning
            personalized_actions = self.ai_learning.get_personalized_actions(
                player_id, scenario_type, current_context
            )
            contextual_actions.extend(personalized_actions)
        
        return contextual_actions

    def process_player_action_with_systems(self, player: Dict, action: Dict, dice_result: Optional[int] = None, player_id: str = None) -> Dict[str, Any]:
        """Process player action integrating all systems"""
        try:
            # Process base action
            result = self.process_player_action(player, action, dice_result)
            
            if player_id:
                # Learn from action
                learning_result = self.ai_learning.learn_from_action(
                    player_id, action, result, {
                        "scenario_type": self.current_scenario,
                        "location": action.get("location", "unknown"),
                        "situation": action.get("situation", "general")
                    }
                )
                
                # Apply inventory effects if applicable
                if action.get("type") == "inventory":
                    inventory_result = self.inventory_system.use_item(
                        player_id, action.get("item_id"), action.get("target")
                    )
                    if inventory_result["success"]:
                        result["inventory_effects"] = inventory_result.get("effects", {})
                
                # Apply skill effects if applicable
                if action.get("type") == "skill":
                    skill_result = self.skill_system.gain_skill_xp(
                        player_id, action.get("skill_id"), action.get("xp_gain", 10)
                    )
                    if skill_result["success"]:
                        result["skill_effects"] = skill_result
                
                # Add system information to result
                result["systems_integrated"] = True
                result["learning_applied"] = learning_result.get("success", False)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing action with systems: {e}")
            return {
                "success": False,
                "error": f"Action processing error: {str(e)}"
            }

    def get_player_status_with_systems(self, player_id: str) -> Dict[str, Any]:
        """Get comprehensive player status including all systems"""
        try:
            status = {
                "player_id": player_id,
                "basic_info": {},
                "inventory": {},
                "skills": {},
                "learning_insights": {},
                "multiplayer_sessions": []
            }
            
            # Get inventory status
            inventory = self.inventory_system.get_player_inventory(player_id)
            status["inventory"] = {
                "items": inventory["items"],
                "equipped": inventory["equipped"],
                "gold": inventory["gold"],
                "capacity": inventory["capacity"],
                "max_capacity": inventory["max_capacity"]
            }
            
            # Get skill status
            player_skills = self.skill_system.get_player_skills(player_id)
            status["skills"] = {
                "skill_points": player_skills["skill_points"],
                "skills": player_skills["skills"],
                "total_xp": player_skills["total_xp"]
            }
            
            # Get learning insights
            insights = self.ai_learning.get_player_insights(player_id)
            status["learning_insights"] = insights
            
            # Get multiplayer sessions
            session_manager = self.multiplayer_manager
            available_sessions = session_manager.get_available_sessions()
            status["multiplayer_sessions"] = available_sessions
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting player status: {e}")
            return {"error": f"Status retrieval error: {str(e)}"}

    def create_multiplayer_session(self, creator_id: str, session_name: str, scenario_id: str, max_players: int = 6) -> Dict[str, Any]:
        """Create a new multiplayer session"""
        return self.multiplayer_manager.create_session(creator_id, session_name, scenario_id, max_players)

    def join_multiplayer_session(self, session_id: str, player_id: str, username: str, character_id: Optional[str] = None) -> Dict[str, Any]:
        """Join a multiplayer session"""
        return self.multiplayer_manager.join_session(session_id, player_id, username, character_id)

    def perform_team_action(self, session_id: str, team_id: str, action: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a collaborative team action"""
        return self.multiplayer_manager.perform_team_action(session_id, team_id, action)

    def get_personalized_experience(self, player_id: str, scenario_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get personalized experience based on AI learning"""
        try:
            # Get personalized actions
            personalized_actions = self.ai_learning.get_personalized_actions(player_id, scenario_type, context)
            
            # Get behavior prediction
            behavior_prediction = self.ai_learning.predict_player_behavior(player_id, context)
            
            # Get difficulty adaptation
            difficulty_adaptation = self.ai_learning.learning_data["difficulty_adaptations"].get(player_id, {})
            
            # Get narrative preferences
            narrative_preferences = self.ai_learning.learning_data["narrative_styles"].get(player_id, {})
            
            return {
                "success": True,
                "personalized_actions": personalized_actions,
                "behavior_prediction": behavior_prediction,
                "difficulty_adaptation": difficulty_adaptation,
                "narrative_preferences": narrative_preferences,
                "recommendations": self.ai_learning.get_player_insights(player_id).get("recommendations", [])
            }
            
        except Exception as e:
            logger.error(f"Error getting personalized experience: {e}")
            return {"success": False, "error": f"Personalization error: {str(e)}"}

    def upgrade_character_skill(self, player_id: str, skill_id: str) -> Dict[str, Any]:
        """Upgrade a character skill"""
        return self.skill_system.learn_skill(player_id, skill_id)

    def add_item_to_inventory(self, player_id: str, item_id: str, quantity: int = 1) -> Dict[str, Any]:
        """Add item to player's inventory"""
        return self.inventory_system.add_item(player_id, item_id, quantity)

    def equip_item(self, player_id: str, item_id: str) -> Dict[str, Any]:
        """Equip an item"""
        return self.inventory_system.equip_item(player_id, item_id)

    def get_available_skills(self, player_id: str) -> List[Dict[str, Any]]:
        """Get available skills for player"""
        return self.skill_system.get_available_skills(player_id)