#!/usr/bin/env python3
"""
AI Dungeon Master - Main Application
===================================

An intelligent AI-powered Fantasy Role-Playing Game Master that creates 
immersive, dynamic adventures using advanced language models.
"""

import os
import sys
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import logging
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(os.path.dirname(BASE_DIR), "templates")
STATIC_DIR = os.path.join(os.path.dirname(BASE_DIR), "static")
LOG_DIR = os.path.join(os.path.dirname(BASE_DIR), "logs")
LOG_FILE = os.path.join(LOG_DIR, "ai_dm.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['DEBUG'] = True
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

try:
    from core.game_engine import GameEngine
    from core.campaign_manager import CampaignManager
    from ai.ai_dungeon_master import AIDungeonMaster
    from web.routes import register_routes
except ImportError as e:
    logger.warning(f"Some modules not yet implemented: {e}")

game_engine = GameEngine()
campaign_manager = CampaignManager()
ai_dm = AIDungeonMaster()
campaign_sessions = {}

# Register web routes
try:
    register_routes(app, game_engine, campaign_manager, ai_dm)
    logger.info("Web routes registered successfully")
except Exception as e:
    logger.error(f"Error registering routes: {e}")

# Fantasy Classes
FANTASY_CLASSES = {
    "warrior": {
        "name": "Warrior", 
        "hp": 120, 
        "attack": 85, 
        "defense": 90, 
        "special": 0, 
        "abilities": ["Shield Wall", "Sword Strike"],
        "description": "Güçlü savaşçı, yüksek savunma ve HP"
    },
    "mage": {
        "name": "Mage", 
        "hp": 60, 
        "attack": 100, 
        "defense": 40, 
        "special": 150, 
        "abilities": ["Fireball", "Ice Bolt"],
        "description": "Güçlü büyücü, yüksek saldırı ve mana"
    },
    "rogue": {
        "name": "Rogue", 
        "hp": 80, 
        "attack": 90, 
        "defense": 60, 
        "special": 95, 
        "abilities": ["Stealth", "Backstab"],
        "description": "Hızlı ve gizli, yüksek saldırı ve stealth"
    },
    "priest": {
        "name": "Priest", 
        "hp": 70, 
        "attack": 50, 
        "defense": 70, 
        "special": 80, 
        "abilities": ["Heal", "Bless"],
        "description": "İyileştirici, yüksek heal ve savunma"
    }
}

# Warhammer 40K Classes
WARHAMMER_CLASSES = {
    "space_marine": {
        "name": "Space Marine", 
        "hp": 150, 
        "attack": 95, 
        "defense": 100, 
        "special": 120, 
        "abilities": ["Bolter Fire", "Power Armor"],
        "description": "Süper asker, yüksek HP ve savunma"
    },
    "tech_priest": {
        "name": "Tech-Priest", 
        "hp": 90, 
        "attack": 60, 
        "defense": 80, 
        "special": 100, 
        "abilities": ["Repair", "Tech Scan"],
        "description": "Teknoloji uzmanı, yüksek tech ve savunma"
    },
    "inquisitor": {
        "name": "Inquisitor", 
        "hp": 100, 
        "attack": 85, 
        "defense": 75, 
        "special": 95, 
        "abilities": ["Purge", "Investigate"],
        "description": "Araştırmacı, dengeli istatistikler"
    },
    "imperial_guard": {
        "name": "Imperial Guard", 
        "hp": 80, 
        "attack": 70, 
        "defense": 60, 
        "special": 90, 
        "abilities": ["Teamwork", "Suppression"],
        "description": "Asker, takım çalışması odaklı"
    }
}

# Combined character classes for easy access
CHARACTER_CLASSES = {**FANTASY_CLASSES, **WARHAMMER_CLASSES}

campaign_flows = {
    "dragon_quest": {
        "start": {
            "description": "Bir ejderha mağarasının girişindesiniz. Ne yapmak istersiniz?",
            "choices": [
                {"id": "enter_cave", "text": "Mağaraya gir"},
                {"id": "look_around", "text": "Etrafı gözlemle"}
            ]
        },
        "enter_cave": {
            "description": "Mağaraya girdiniz ve bir goblin ile karşılaştınız!",
            "choices": [
                {"id": "attack_goblin", "text": "Saldır"},
                {"id": "sneak_past", "text": "Gizlice geçmeye çalış"}
            ],
            "encounter": "goblin"
        },
        "look_around": {
            "description": "Etrafı incelediniz, bir iksir buldunuz! Şimdi ne yapmak istersiniz?",
            "choices": [
                {"id": "enter_cave", "text": "Mağaraya gir"}
            ]
        },
        "attack_goblin": {
            "description": "Gobline saldırıyorsunuz! Saldırı zarı atın.",
            "choices": [],
            "dice": "attack"
        },
        "sneak_past": {
            "description": "Gizlice geçmeye çalışıyorsunuz. Gözlem zarı atın.",
            "choices": [],
            "dice": "stealth"
        },
        "attack_success": {
            "description": "Goblin'i yendiniz! Mağaranın derinliklerine ilerliyorsunuz.",
            "choices": [
                {"id": "end", "text": "Devam et"}
            ]
        },
        "attack_fail": {
            "description": "Goblin saldırınızı savuşturdu ve sizi yaraladı!",
            "choices": [
                {"id": "end", "text": "Devam et"}
            ]
        },
        "stealth_success": {
            "description": "Goblin sizi fark etmedi, gizlice geçtiniz!",
            "choices": [
                {"id": "end", "text": "Devam et"}
            ]
        },
        "stealth_fail": {
            "description": "Goblin sizi fark etti! Savaşmak zorundasınız.",
            "choices": [
                {"id": "attack_goblin", "text": "Saldır"}
            ]
        },
        "end": {
            "description": "Macera burada sona erdi!",
            "choices": []
        }
    },
    "dragon_lords": {
        "start": {
            "description": "Yanık bir köyde uyanıyorsunuz. Köylüler panik halinde. Ne yapmak istersiniz?",
            "choices": [
                {"id": "calm_villagers", "text": "Köylüleri sakinleştirip bilgi topla"},
                {"id": "run_forest", "text": "Hemen yakındaki ormana kaç"},
                {"id": "search_ruins", "text": "Köydeki enkaza dalıp hayatta kalan ara"},
                {"id": "go_smoke", "text": "Köyün üzerindeki dumana doğru git"}
            ]
        },
        "calm_villagers": {
            "description": "Köylüler ejderha saldırısından bahseder, 50 gold verir.",
            "choices": [
                {"id": "forest_path", "text": "Orman yoluna devam et"}
            ]
        },
        "run_forest": {
            "description": "Ormanda gizli ejderha yuvası keşfedersiniz.",
            "choices": [
                {"id": "forest_path", "text": "Orman yoluna devam et"}
            ]
        },
        "search_ruins": {
            "description": "Yaralı bir savaşçı bulursunuz (NPC ally).",
            "choices": [
                {"id": "forest_path", "text": "Orman yoluna devam et"}
            ]
        },
        "go_smoke": {
            "description": "Ejderha ile erken karşılaşma (zor savaş)",
            "choices": [
                {"id": "dragon_battle", "text": "Ejderha ile savaş"}
            ]
        },
        "forest_path": {
            "description": "Antik orman yolunda ilerlerken garip sesler duyarsınız.",
            "choices": [
                {"id": "follow_sounds", "text": "Sesleri takip et"},
                {"id": "hide", "text": "Sessizce saklan"},
                {"id": "challenge", "text": "Yüksek sesle meydan oku"},
                {"id": "find_other_way", "text": "Geri dön ve başka yol ara"}
            ]
        },
        "follow_sounds": {
            "description": "Orman sprite'larıyla karşılaşır, büyü öğrenebilirsiniz.",
            "choices": [
                {"id": "city_ruins", "text": "Terk edilmiş şehre git"}
            ]
        },
        "hide": {
            "description": "Ejderha kültistlerini fark edersiniz, sürpriz saldırı avantajı.",
            "choices": [
                {"id": "city_ruins", "text": "Terk edilmiş şehre git"}
            ]
        },
        "challenge": {
            "description": "Orc grubuyla savaş (HP: 60 her biri, 4 tane)",
            "choices": [
                {"id": "city_ruins", "text": "Terk edilmiş şehre git"}
            ]
        },
        "find_other_way": {
            "description": "Güvenli ama daha uzun yol.",
            "choices": [
                {"id": "city_ruins", "text": "Terk edilmiş şehre git"}
            ]
        },
        "city_ruins": {
            "description": "Başkentin harabeleri önünüzde. Üç farklı bölgeye gidebilirsiniz.",
            "choices": [
                {"id": "palace", "text": "Kral Sarayı'nın kalıntılarına git"},
                {"id": "wizard_tower", "text": "Büyücü Kulesi'ni araştır"},
                {"id": "sewers", "text": "Yeraltı Kanalizasyonu'na in"},
                {"id": "market", "text": "Pazar Alanı'nda malzeme ara"}
            ]
        },
        "palace": {
            "description": "Kral Aldric ile karşılaşır, görev alırsınız.",
            "choices": [
                {"id": "dragon_battle", "text": "Ejderha ile savaş"}
            ]
        },
        "wizard_tower": {
            "description": "İlk ejderha mührü parçasını bulursunuz.",
            "choices": [
                {"id": "dragon_battle", "text": "Ejderha ile savaş"}
            ]
        },
        "sewers": {
            "description": "Dracolich'in minyonlarıyla savaş.",
            "choices": [
                {"id": "dragon_battle", "text": "Ejderha ile savaş"}
            ]
        },
        "market": {
            "description": "Ekipman ve iksir bulursunuz.",
            "choices": [
                {"id": "dragon_battle", "text": "Ejderha ile savaş"}
            ]
        },
        "dragon_battle": {
            "description": "Kırmızı Ejderha Pyraxis ile karşı karşıyasınız! (HP: 300, Attack: 120, Defense: 80, Fire Immunity) Savaş başlıyor! Fiziksel Saldırı, Büyü Kullan, Savunma veya Özel Yetenek seçebilirsiniz.",
            "choices": [
                {"id": "attack", "text": "Fiziksel Saldırı"},
                {"id": "cast_spell", "text": "Büyü Kullan"},
                {"id": "defend", "text": "Savunma"},
                {"id": "special", "text": "Özel Yetenek"}
            ]
        },
        "attack": {
            "description": "Ejderhaya fiziksel saldırı yapıyorsunuz. Zar atılıyor...",
            "dice": "attack",
            "choices": []
        },
        "cast_spell": {
            "description": "Büyü kullanıyorsunuz. Zar atılıyor...",
            "dice": "magic",
            "choices": []
        },
        "defend": {
            "description": "Savunma pozisyonu alıyorsunuz. Zar atılıyor...",
            "dice": "defense",
            "choices": []
        },
        "special": {
            "description": "Sınıfa özel yetenek kullanıyorsunuz. Zar atılıyor...",
            "dice": "special",
            "choices": []
        }
    }
}

# Legacy route handlers removed - now handled by web/routes.py

if __name__ == '__main__':
    port = 5050
    logger.info(f"Server starting on port {port}")
    logger.info("Access the application at: http://localhost:5050")
    socketio.run(app, host='0.0.0.0', port=port, debug=False, use_reloader=False) 