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
            "description": "Caldrith şehrinde uyanıyorsun. Sınıfını seçtin, macera başlıyor! İlk hedefin: Bataklıklara ulaşmak.",
            "choices": [
                {"id": "swamp_entry", "text": "Kasvetli Bataklıklara git"}
            ]
        },
        # Bölge 1: Kasvetli Bataklıklar
        "swamp_entry": {
            "description": "Bataklıkta zehirli yaratıklar ve Eloria ile karşılaşıyorsun.",
            "choices": [
                {"id": "fight_swamp_beast", "text": "Yaratıkla savaş"},
                {"id": "talk_eloria", "text": "Eloria ile konuş"}
            ]
        },
        "fight_swamp_beast": {
            "description": "Zehirli yaratığı yendin! 10 XP kazandın. Eloria sana yardım teklif ediyor.",
            "choices": [
                {"id": "good_help_eloria", "text": "Yardım et (İyi)"},
                {"id": "evil_ignore_eloria", "text": "Yok say (Kötü)"}
            ],
            "xp": 10
        },
        "talk_eloria": {
            "description": "Eloria: 'Yardımına ihtiyacım var.' Ne yapacaksın?",
            "choices": [
                {"id": "good_help_eloria", "text": "Yardım et (İyi)"},
                {"id": "evil_ignore_eloria", "text": "Yok say (Kötü)"}
            ]
        },
        "good_help_eloria": {
            "description": "Eloria özel bilgi verdi, HP bonusu ve İyileştirme İksiri aldın. Dağlara geçiyorsun.",
            "choices": [
                {"id": "mountain_entry", "text": "Gölge Dağlarına git"}
            ],
            "reward": {"item": {"name": "İyileştirme İksiri", "type": "potion", "heal": 30, "usable": True}, "buff": "hp_bonus"}
        },
        "evil_ignore_eloria": {
            "description": "Eloria seni lanetledi, HP kaybettin. Dağlara geçiyorsun.",
            "choices": [
                {"id": "mountain_entry", "text": "Gölge Dağlarına git"}
            ],
            "penalty": "hp_loss"
        },
        # Bölge 2: Gölge Dağları
        "mountain_entry": {
            "description": "Dağlarda Brakk the Cruel ve bandit boss ile karşılaşıyorsun.",
            "choices": [
                {"id": "fight_bandit_boss", "text": "Bandit Boss ile savaş"},
                {"id": "talk_brakk", "text": "Brakk ile konuş"}
            ]
        },
        "fight_bandit_boss": {
            "description": "Bandit Boss'u yendin! 15 XP ve rare item kazandın.",
            "choices": [
                {"id": "vault_entry", "text": "Forgotten Vaults'a git"}
            ],
            "xp": 15,
            "reward": "rare_item"
        },
        "talk_brakk": {
            "description": "Brakk: 'Bana yardım et, sana dagger veririm.'",
            "choices": [
                {"id": "good_help_brakk", "text": "Yardım et (İyi)"},
                {"id": "evil_betray_brakk", "text": "İhanet et (Kötü)"}
            ]
        },
        "good_help_brakk": {
            "description": "Brakk sadık oldu, rare dagger verdi. Vaults'a geçiyorsun.",
            "choices": [
                {"id": "vault_entry", "text": "Forgotten Vaults'a git"}
            ],
            "reward": "rare_dagger"
        },
        "evil_betray_brakk": {
            "description": "Brakk pusu kurdu, can kaybettin. Vaults'a geçiyorsun.",
            "choices": [
                {"id": "vault_entry", "text": "Forgotten Vaults'a git"}
            ],
            "penalty": "hp_loss",
            "evil_ally": True
        },
        # Bölge 3: Forgotten Vaults
        "vault_entry": {
            "description": "Vaults'ta Tech-Priest Maldrin ile karşılaşıyorsun. Antik canavarlar var.",
            "choices": [
                {"id": "fight_vault_monster", "text": "Canavarla savaş"},
                {"id": "talk_maldrin", "text": "Maldrin ile konuş"}
            ]
        },
        "fight_vault_monster": {
            "description": "Canavarı yendin! 20 XP ve skill açıldı.",
            "choices": [
                {"id": "graveyard_entry", "text": "Stellaris Mezarlığı'na git"}
            ],
            "xp": 20,
            "reward": "skill_unlock"
        },
        "talk_maldrin": {
            "description": "Maldrin: 'Tech yeteneklerini açabilirim.'",
            "choices": [
                {"id": "good_ask_maldrin", "text": "Soru sor (İyi)"},
                {"id": "evil_ignore_maldrin", "text": "Yok say (Kötü)"}
            ]
        },
        "good_ask_maldrin": {
            "description": "Yeni skill açıldı! Maldrin sana Tech Relic verdi. Mezarlığa geçiyorsun.",
            "choices": [
                {"id": "graveyard_entry", "text": "Stellaris Mezarlığı'na git"}
            ],
            "reward": {"item": {"name": "Tech Relic", "type": "artifact", "effect": "tech_buff", "usable": False}, "skill": "skill_unlock"}
        },
        "evil_ignore_maldrin": {
            "description": "Maldrin seni lanetledi, XP kaybettin. Mezarlığa geçiyorsun.",
            "choices": [
                {"id": "graveyard_entry", "text": "Stellaris Mezarlığı'na git"}
            ],
            "penalty": "xp_loss"
        },
        # Bölge 4: Stellaris Mezarlığı
        "graveyard_entry": {
            "description": "Mezarlıkta kaybolmuş ruhlar ve Guard Captain Drex ile karşılaşıyorsun.",
            "choices": [
                {"id": "fight_ghosts", "text": "Ruhlarla savaş"},
                {"id": "talk_drex", "text": "Drex ile konuş"}
            ]
        },
        "fight_ghosts": {
            "description": "Ruhları yendin! 25 XP ve bonus gold kazandın.",
            "choices": [
                {"id": "pyraxis_entry", "text": "Pyraxis'e git"}
            ],
            "xp": 25,
            "reward": "bonus_gold"
        },
        "talk_drex": {
            "description": "Drex: 'Şehri kurtar ya da beni öldür.'",
            "choices": [
                {"id": "good_help_drex", "text": "Yardım et (İyi)"},
                {"id": "evil_kill_drex", "text": "Öldür (Kötü)"}
            ]
        },
        "good_help_drex": {
            "description": "Şehri kurtardın, XP ve gold kazandın. Drex sana Zafer Madalyası verdi. Pyraxis'e geçiyorsun.",
            "choices": [
                {"id": "pyraxis_entry", "text": "Pyraxis'e git"}
            ],
            "xp": 20,
            "reward": {"item": {"name": "Zafer Madalyası", "type": "medal", "effect": "defense_up", "usable": False}, "gold": 100}
        },
        "evil_kill_drex": {
            "description": "Drex'i öldürdün, evil path açıldı. Pyraxis'e geçiyorsun.",
            "choices": [
                {"id": "pyraxis_entry", "text": "Pyraxis'e git"}
            ],
            "reward": "evil_path"
        },
        # Bölge 5: Pyraxis
        "pyraxis_entry": {
            "description": "Pyraxis'in önündesin. Flame Oracle Vynn ile karşılaşıyorsun. Son seçim!",
            "choices": [
                {"id": "talk_vynn", "text": "Vynn ile konuş"},
                {"id": "final_battle", "text": "Ejderha ile savaş"}
            ],
            "background": "/static/images/pyraxisfam.jpg",
            "evil_ally": True
        },
        "talk_vynn": {
            "description": "Vynn: 'Geleceğin yolunu seç.' Skill cost düşer.",
            "choices": [
                {"id": "final_battle", "text": "Ejderha ile savaş"}
            ],
            "reward": "skill_cost_reduction"
        },
        "final_battle": {
            "description": "Pyraxis ile final savaşı! Saldırı, savunma, skill veya ultimate kullanabilirsin. (Eğer kötü yolu seçtiysen Brakk yanında!)",
            "choices": [
                {"id": "good_ending", "text": "İyi Son (Pyraxis'i kurtar)"},
                {"id": "evil_ending", "text": "Kötü Son (Pyraxis'i yok et)"}
            ],
            "evil_ally": True
        },
        "good_ending": {
            "description": "Pyraxis'i kurtardın, kahraman oldun! Oyun bitti.",
            "choices": []
        },
        "evil_ending": {
            "description": "Pyraxis'i yok ettin, karanlık lord oldun! Oyun bitti.",
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