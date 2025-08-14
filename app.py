#!/usr/bin/env python3
"""
AI Dungeon Master - Basit Flask Uygulaması
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import sys
import os
import time

app = Flask(__name__)
CORS(app)

# Multiplayer modüllerini import et
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from multiplayer.session_manager import MultiplayerSessionManager, SessionStatus

# Multiplayer session manager
session_manager = MultiplayerSessionManager()

# Warhammer ve Fantasy karakter sınıfları
CHARACTER_CLASSES = [
    {
        "id": "space_marine",
        "name": "Space Marine",
        "description": "İmperium'un seçkin savaşçısı, genetik olarak geliştirilmiş süper asker",
        "stats": {"hp": 150, "attack": 25, "defense": 20, "strength": 18, "toughness": 16},
        "skills": [
            {"name": "Bolter Mastery", "description": "Bolter silahlarında uzmanlık", "effect": "+3 attack"},
            {"name": "Power Armor", "description": "Gelişmiş zırh koruması", "effect": "+5 defense"},
            {"name": "Chainsword", "description": "Zincirli kılıç kullanımı", "effect": "+2 damage"},
            {"name": "Tactical Awareness", "description": "Savaş alanı farkındalığı", "effect": "+1 initiative"}
        ],
        "special_abilities": ["Astartes Physiology", "Combat Doctrine", "Chapter Tactics"]
    },
    {
        "id": "imperial_guard",
        "name": "Imperial Guard",
        "description": "İmperium'un ana askeri gücü, disiplinli ve cesur",
        "stats": {"hp": 80, "attack": 15, "defense": 12, "strength": 12, "toughness": 10},
        "skills": [
            {"name": "Lasgun Training", "description": "Lasgun silah eğitimi", "effect": "+2 attack"},
            {"name": "Commissar Leadership", "description": "Komiser liderliği", "effect": "+1 morale"},
            {"name": "Trench Warfare", "description": "Siper savaşı deneyimi", "effect": "+3 defense"},
            {"name": "Regimental Standard", "description": "Alay standardı", "effect": "+2 leadership"}
        ],
        "special_abilities": ["First Rank Fire", "Second Rank Fire", "Fix Bayonets"]
    },
    {
        "id": "psyker",
        "name": "Psyker",
        "description": "Psişik güçlere sahip, Warp enerjisini kullanan büyücü",
        "stats": {"hp": 70, "attack": 30, "defense": 8, "willpower": 20, "psychic": 18},
        "skills": [
            {"name": "Warp Manipulation", "description": "Warp enerjisi kontrolü", "effect": "+5 psychic"},
            {"name": "Mind Control", "description": "Zihin kontrolü", "effect": "enemy confusion"},
            {"name": "Psychic Barrier", "description": "Psişik koruma kalkanı", "effect": "+4 defense"},
            {"name": "Warp Lightning", "description": "Warp şimşeği", "effect": "+8 damage"}
        ],
        "special_abilities": ["Psychic Powers", "Warp Resistance", "Sanctioned Psyker"]
    },
    {
        "id": "ork_nob",
        "name": "Ork Nob",
        "description": "Ork boyunun lideri, güçlü ve savaşçı",
        "stats": {"hp": 120, "attack": 22, "defense": 15, "strength": 20, "toughness": 14},
        "skills": [
            {"name": "Waaagh!", "description": "Ork savaş çığlığı", "effect": "+3 attack, +2 morale"},
            {"name": "Choppa Mastery", "description": "Ork baltası ustalığı", "effect": "+4 damage"},
            {"name": "Tough as Nails", "description": "Çelik gibi dayanıklılık", "effect": "+3 toughness"},
            {"name": "Mob Rule", "description": "Çete yönetimi", "effect": "+2 leadership"}
        ],
        "special_abilities": ["Waaagh Energy", "Ork Physiology", "Mob Mentality"]
    },
    {
        "id": "eldar_farseer",
        "name": "Eldar Farseer",
        "description": "Eldar'ın psişik lideri, geleceği gören bilge",
        "stats": {"hp": 90, "attack": 18, "defense": 14, "willpower": 22, "psychic": 20},
        "skills": [
            {"name": "Foresight", "description": "Geleceği görme", "effect": "+2 initiative"},
            {"name": "Rune Reading", "description": "Rün okuma", "effect": "+3 psychic"},
            {"name": "Wraithbone Crafting", "description": "Wraithbone işleme", "effect": "+2 crafting"},
            {"name": "Spirit Stone", "description": "Ruh taşı bağlantısı", "effect": "+4 willpower"}
        ],
        "special_abilities": ["Farseer Powers", "Eldar Technology", "Spirit Guidance"]
    },
    {
        "id": "chaos_sorcerer",
        "name": "Chaos Sorcerer",
        "description": "Kaos tanrılarının gücünü kullanan karanlık büyücü",
        "stats": {"hp": 85, "attack": 25, "defense": 10, "willpower": 18, "chaos": 20},
        "skills": [
            {"name": "Chaos Magic", "description": "Kaos büyüsü", "effect": "+6 chaos damage"},
            {"name": "Warp Corruption", "description": "Warp bozulması", "effect": "enemy corruption"},
            {"name": "Daemon Summoning", "description": "Şeytan çağırma", "effect": "summon daemon"},
            {"name": "Dark Pact", "description": "Karanlık anlaşma", "effect": "+3 chaos power"}
        ],
        "special_abilities": ["Chaos Powers", "Warp Corruption", "Daemon Binding"]
    },
    {
        "id": "necron_lord",
        "name": "Necron Lord",
        "description": "Necron hanedanının lideri, ölümsüz metal savaşçı",
        "stats": {"hp": 140, "attack": 20, "defense": 25, "strength": 16, "technology": 22},
        "skills": [
            {"name": "Gauss Technology", "description": "Gauss silah teknolojisi", "effect": "+5 damage"},
            {"name": "Living Metal", "description": "Canlı metal yapısı", "effect": "+3 regeneration"},
            {"name": "Phase Shifter", "description": "Faz değiştirici", "effect": "+4 defense"},
            {"name": "Necron Protocols", "description": "Necron protokolleri", "effect": "+2 leadership"}
        ],
        "special_abilities": ["Necron Technology", "Living Metal", "Phase Shifting"]
    },
    {
        "id": "tau_fire_caste",
        "name": "Tau Fire Caste",
        "description": "Tau İmparatorluğu'nun savaşçı kastı, gelişmiş teknoloji kullanır",
        "stats": {"hp": 95, "attack": 18, "defense": 16, "strength": 12, "technology": 18},
        "skills": [
            {"name": "Pulse Rifle", "description": "Pulse tüfeği eğitimi", "effect": "+3 attack"},
            {"name": "Battlesuit Training", "description": "Savaş giysisi eğitimi", "effect": "+4 defense"},
            {"name": "Greater Good", "description": "Büyük İyi ideali", "effect": "+2 morale"},
            {"name": "Advanced Targeting", "description": "Gelişmiş hedefleme", "effect": "+2 accuracy"}
        ],
        "special_abilities": ["Tau Technology", "Greater Good", "Battlesuit Systems"]
    }
]

# Warhammer ve Fantasy karakter ırkları
CHARACTER_RACES = [
    {
        "id": "human",
        "name": "Human (İnsan)",
        "description": "İmperium'un temel ırkı, çok yönlü ve uyumlu",
        "traits": ["Adaptable", "Versatile", "Ambitious"],
        "bonuses": {"hp": 0, "attack": 0, "defense": 0, "experience": 1}
    },
    {
        "id": "space_marine",
        "name": "Astartes (Space Marine)",
        "description": "Genetik olarak geliştirilmiş süper asker",
        "traits": ["Enhanced Physiology", "Combat Implants", "Chapter Gene-Seed"],
        "bonuses": {"hp": 50, "attack": 5, "defense": 5, "strength": 3, "toughness": 3}
    },
    {
        "id": "ork",
        "name": "Ork",
        "description": "Savaşçı ve teknoloji odaklı yeşil ırk",
        "traits": ["Waaagh Energy", "Tough as Nails", "Mob Mentality"],
        "bonuses": {"hp": 30, "attack": 3, "defense": 2, "strength": 4, "toughness": 3}
    },
    {
        "id": "eldar",
        "name": "Eldar",
        "description": "Eski ve gelişmiş uzay elfleri",
        "traits": ["Ancient Knowledge", "Psychic Potential", "Advanced Technology"],
        "bonuses": {"hp": -10, "attack": 2, "defense": 1, "willpower": 4, "psychic": 3}
    },
    {
        "id": "necron",
        "name": "Necron",
        "description": "Ölümsüz metal yapılı eski ırk",
        "traits": ["Living Metal", "Ancient Technology", "Immortal"],
        "bonuses": {"hp": 40, "attack": 1, "defense": 4, "technology": 5, "regeneration": 2}
    },
    {
        "id": "tau",
        "name": "Tau",
        "description": "Genç ve teknolojik olarak gelişmiş ırk",
        "traits": ["Greater Good", "Advanced Technology", "Caste System"],
        "bonuses": {"hp": -5, "attack": 1, "defense": 2, "technology": 3, "morale": 2}
    },
    {
        "id": "chaos_cultist",
        "name": "Chaos Cultist",
        "description": "Kaos tanrılarına tapan bozulmuş insan",
        "traits": ["Warp Corruption", "Chaos Devotion", "Dark Powers"],
        "bonuses": {"hp": 10, "attack": 2, "defense": -1, "chaos": 4, "willpower": 2}
    },
    {
        "id": "tyranid",
        "name": "Tyranid",
        "description": "Biyolojik olarak gelişmiş uzay yaratığı",
        "traits": ["Hive Mind", "Biological Adaptation", "Synapse Creature"],
        "bonuses": {"hp": 25, "attack": 3, "defense": 1, "strength": 3, "regeneration": 1}
    }
]

# Tüm Senaryolar - Fantasy, Warhammer 40K, ve Cyberpunk
SCENARIOS = [
    # Fantasy Senaryoları
    {
        "id": "forest_scenario",
        "title": "Büyülü Ormanın Gizemleri",
        "description": "Büyülü bir ormanda gizlenen sırları keşfet. Antik büyüler ve gizemli yaratıklarla dolu bir macera.",
        "genre": "fantasy",
        "difficulty": "Hard",
        "objectives": ["Explore Forest", "Discover Ancient Magic", "Find Artifacts"],
        "rewards": {"experience": 1000, "reputation": 500, "equipment": "Magical Staff"}
    },
    {
        "id": "dragon_hunter_scenario",
        "title": "Ejderha Avcısının Yolu",
        "description": "Ejderhaların yaşadığı tehlikeli dünyada bir ejderha avcısının yolculuğu. Antik sırlar ve güçlü düşmanlarla dolu bir macera.",
        "genre": "fantasy",
        "difficulty": "Hard",
        "objectives": ["Hunt Dragons", "Gain Experience", "Become Legend"],
        "rewards": {"experience": 1200, "reputation": 600, "equipment": "Dragon Slayer Sword"}
    },
    {
        "id": "dragon_hunt_scenario",
        "title": "Ejderha Avı: Kızıl Alev",
        "description": "Kızıl Alev adlı efsanevi ejderhayı avlamak için tehlikeli bir yolculuk. Bu ejderha yüzyıllardır bölgeyi terörize ediyor.",
        "genre": "fantasy",
        "difficulty": "Hard",
        "objectives": ["Track Red Flame", "Defeat Legendary Dragon", "Claim Reward"],
        "rewards": {"experience": 1500, "reputation": 800, "equipment": "Legendary Weapon"}
    },
    {
        "id": "ancient_ruins_scenario",
        "title": "Antik Harabelerin Sırrı",
        "description": "Antik bir uygarlığın harabelerinde gizlenen sırları keşfet. Tehlikeli tuzaklar ve güçlü artefaktlar.",
        "genre": "fantasy",
        "difficulty": "Hard",
        "objectives": ["Explore Ruins", "Activate Ancient Power", "Control Artifacts"],
        "rewards": {"experience": 1300, "reputation": 700, "equipment": "Ancient Artifact"}
    },
    {
        "id": "crystal_cave_scenario",
        "title": "Kristal Mağarasının Laneti",
        "description": "Kristal mağarasında gizlenen laneti keşfet. Büyülü kristaller ve tehlikeli yaratıklar.",
        "genre": "fantasy",
        "difficulty": "Medium",
        "objectives": ["Explore Cave", "Touch Crystal", "Use Power Wisely"],
        "rewards": {"experience": 900, "reputation": 400, "equipment": "Crystal Staff"}
    },
    # Warhammer 40K Senaryoları
    {
        "id": "hive_city_scenario",
        "title": "Hive Şehrinin Komutanlığı - Imperium'un Son Savunması",
        "description": "Hive şehrinde cyberpunk atmosferinde geçen, AI manipülasyonu ve corporate espionage ile dolu bir macera.",
        "genre": "warhammer40k",
        "difficulty": "Hard",
        "objectives": ["Defend Hive City", "Fight AI Corruption", "Survive Corporate War"],
        "rewards": {"experience": 1200, "reputation": 600, "equipment": "Power Armor"}
    },
    {
        "id": "hive_defense_scenario",
        "title": "Hive Şehrinin Savunması",
        "description": "Hive şehrini dış tehditlerden korumak için savaş. Imperium'un son savunması.",
        "genre": "warhammer40k",
        "difficulty": "Hard",
        "objectives": ["Deploy Defenses", "Defend Gates", "Victory"],
        "rewards": {"experience": 1100, "reputation": 550, "equipment": "Imperial Guard"}
    },
    {
        "id": "ork_invasion_scenario",
        "title": "Ork İstilası: Son Savunma",
        "description": "Ork istilasına karşı son savunma. Waaagh! enerjisi ile dolu bir savaş.",
        "genre": "warhammer40k",
        "difficulty": "Hard",
        "objectives": ["Prepare Defense", "Fight Orks", "Victory"],
        "rewards": {"experience": 1300, "reputation": 700, "equipment": "Waaagh Banner"}
    },
    # Cyberpunk Senaryoları
    {
        "id": "cyberpunk_city_scenario",
        "title": "Cyberpunk Şehrinin Gizli Sırları",
        "description": "Cyberpunk şehrinin gizli sırlarını keşfet. Teknoloji ve insanlık arasındaki sınır bulanıklaşıyor.",
        "genre": "cyberpunk",
        "difficulty": "Hard",
        "objectives": ["Explore Districts", "Hack Systems", "Control City"],
        "rewards": {"experience": 1400, "reputation": 800, "equipment": "Cyber Implants"}
    }
]

# Hikaye sistemi verileri
STORY_DATA = {
    "current_scenario": None,
    "story_progress": {},
    "npc_interactions": {},
    "story_branches": {},
    "story_combats": {}  # Hikaye savaşları için yeni alan
}

# NPC verileri
NPC_DATA = {
    "dragon": {
        "name": "Ejderha",
        "type": "quest_giver",
        "personality": "Bilge ve güçlü",
        "dialogue": {
            "greeting": "Hoş geldin, cesur savaşçı!",
            "quest_offer": "Bana yardım eder misin?",
            "farewell": "Yolun açık olsun!"
        },
        "combat_stats": {
            "hp": 100,
            "attack": 15,
            "defense": 10,
            "special_abilities": ["Ateş Nefesi", "Kanat Çırpışı"]
        }
    },
    "merchant": {
        "name": "Tüccar",
        "type": "trader",
        "personality": "Açgözlü ama güvenilir",
        "dialogue": {
            "greeting": "Alışveriş yapmak ister misin?",
            "quest_offer": "Bir işim var senin için...",
            "farewell": "Tekrar gel!"
        },
        "combat_stats": {
            "hp": 30,
            "attack": 5,
            "defense": 3,
            "special_abilities": ["Kaçış"]
        }
    },
    "ork_warboss": {
        "name": "Ork Warboss",
        "type": "enemy",
        "personality": "Vahşi ve saldırgan",
        "dialogue": {
            "greeting": "WAAAGH! Sen kimsin?",
            "challenge": "Savaşmak ister misin?",
            "defeat": "Sen güçlüsün..."
        },
        "combat_stats": {
            "hp": 80,
            "attack": 12,
            "defense": 8,
            "special_abilities": ["Waaagh!", "Choppa Strike"]
        }
    },
    "eldar_farseer": {
        "name": "Eldar Farseer",
        "type": "ally",
        "personality": "Bilge ve gizemli",
        "dialogue": {
            "greeting": "Geleceği görüyorum...",
            "warning": "Tehlike yaklaşıyor",
            "help": "Yardım edebilirim"
        },
        "combat_stats": {
            "hp": 60,
            "attack": 10,
            "defense": 6,
            "special_abilities": ["Foresight", "Psychic Blast"]
        }
    }
}

# Oyun kayıtları (gerçek uygulamada veritabanı kullanılır)
GAME_SAVES = {}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/multiplayer')
def multiplayer():
    return render_template('multiplayer.html')

@app.route('/simple_test.html')
def simple_test():
    return render_template('simple_test.html')

@app.route('/test_buttons')
def test_buttons():
    return render_template('test_button_functionality.html')

@app.route('/simple_button_test')
def simple_button_test():
    return render_template('simple_button_test.html')

@app.route('/enhanced')
def enhanced():
    return render_template('game_enhanced.html')

@app.route('/demo')
def deep_story_demo():
    return render_template('test_deep_story_demo.html')

@app.route('/minimal_test')
def minimal_test():
    return render_template('minimal_test.html')



@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "systems": {
            "character_system": "active",
            "combat_system": "active",
            "dice_system": "active",
            "game_engine": "active"
        }
    })

@app.route('/api/game/character/classes')
def get_character_classes():
    try:
        with open('data/character_classes.json', 'r', encoding='utf-8') as f:
            classes_data = json.load(f)
        return jsonify({"success": True, "classes": list(classes_data.values())})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/game/character/races')
def get_character_races():
    try:
        with open('data/character_races.json', 'r', encoding='utf-8') as f:
            races_data = json.load(f)
        return jsonify({"success": True, "races": list(races_data.values())})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/game/character/load', methods=['GET'])
def load_character():
    try:
        # For now, return empty character data to prevent hardcoded display
        # This will be updated when user creates a character
        return jsonify({
            'success': True,
            'character': None,
            'game_state': {
                'level': 1,
                'xp': 0,
                'karma': 0
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Karakter yüklenemedi: {str(e)}'
        }), 500

@app.route('/api/game/character/save', methods=['POST'])
def save_character():
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'guest')
        character_data = {
            'id': f"char_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'name': data.get('name'),
            'class': data.get('class'),
            'race': data.get('race'),
            'created_at': datetime.now().isoformat(),
            'user_id': user_id
        }
        
        # Karakteri kaydet
        characters_file = 'data/characters.json'
        characters = []
        
        try:
            with open(characters_file, 'r', encoding='utf-8') as f:
                file_content = f.read().strip()
                if file_content:
                    characters_dict = json.loads(file_content)
                    # Dictionary'yi list'e çevir
                    if isinstance(characters_dict, dict):
                        characters = list(characters_dict.values())
                    elif isinstance(characters_dict, list):
                        characters = characters_dict
                    else:
                        characters = []
                else:
                    characters = []
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            characters = []
        
        characters.append(character_data)
        
        # List'i tekrar dictionary formatına çevir ve kaydet
        characters_dict = {char['id']: char for char in characters}
        
        with open(characters_file, 'w', encoding='utf-8') as f:
            json.dump(characters_dict, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'success': True,
            'message': 'Karakter başarıyla kaydedildi',
            'character': character_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Karakter kaydedilemedi: {str(e)}'
        }), 500

# RAG System Integration - Real Implementation
@app.route('/api/rag/upload', methods=['POST'])
def upload_document():
    """RAG sistemine dosya yükleme endpoint'i - Gerçek RAG entegrasyonu"""
    try:
        from rag.main import RAGSystem
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'Dosya bulunamadı'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Dosya seçilmedi'}), 400
        
        # Dosya türü kontrolü
        allowed_extensions = {'.pdf', '.txt'}
        file_ext = '.' + file.filename.rsplit('.', 1)[1].lower()
        if file_ext not in allowed_extensions:
            return jsonify({'success': False, 'error': 'Desteklenmeyen dosya türü. Sadece PDF ve TXT dosyaları kabul edilir.'}), 400
        
        # Dosya boyutu kontrolü (50MB)
        file_content = file.read()
        if len(file_content) > 50 * 1024 * 1024:
            return jsonify({'success': False, 'error': 'Dosya boyutu çok büyük. Maksimum 50MB.'}), 400
        
        file.seek(0)  # Dosya pointer'ını başa al
        
        # Dosyayı kaydet
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join('rag', 'uploads', 'user_documents', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)
        
        # RAG sistemine gönder ve işle
        try:
            rag_system = RAGSystem()
            result = rag_system.upload_document(filepath)
            
            if result.get('success', False):
                return jsonify({
                    'success': True,
                    'message': f'Dosya başarıyla yüklendi ve RAG sistemine işlendi. {result.get("chunks_created", 0)} parça oluşturuldu.',
                    'filename': filename,
                    'filepath': filepath,
                    'rag_result': result
                })
            else:
                # Check if it's an API key error
                if "OpenAI API key required" in result.get('error', ''):
                    return jsonify({
                        'success': False,
                        'error': 'OpenAI API anahtarı gerekli. Lütfen OPENAI_API_KEY ortam değişkenini ayarlayın.',
                        'filename': filename,
                        'api_key_required': True
                    }), 400
                else:
                    return jsonify({
                        'success': False,
                        'error': f'RAG işleme hatası: {result.get("error", "Bilinmeyen hata")}',
                        'filename': filename
                    }), 500
                
        except Exception as rag_error:
            return jsonify({
                'success': False,
                'error': f'RAG sistem hatası: {str(rag_error)}',
                'filename': filename
            }), 500
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/rag/generate-scenario', methods=['POST'])
def generate_ai_scenario():
    """AI destekli senaryo üretimi endpoint'i - Gerçek RAG entegrasyonu"""
    try:
        from rag.main import RAGSystem
        
        data = request.get_json()
        theme = data.get('theme', 'fantasy')
        difficulty = data.get('difficulty', 'medium')
        level = data.get('level', 5)
        custom_prompt = data.get('custom_prompt', '')
        
        # RAG sistemini kullanarak senaryo üret
        try:
            rag_system = RAGSystem()
            result = rag_system.generate_scenario(theme, level)
            
            if result.get('success', False):
                scenario = result.get('scenario', {})
                
                # Eğer custom prompt varsa, senaryoya ekle
                if custom_prompt:
                    scenario['custom_prompt'] = custom_prompt
                    scenario['description'] += f"\n\nÖzel İstek: {custom_prompt}"
                
                return jsonify({
                    'success': True,
                    'scenario': scenario,
                    'rag_result': result
                })
            else:
                # Check if it's an API key error and use fallback
                if "OpenAI API key required" in result.get('error', ''):
                    fallback_scenario = result.get('fallback_scenario', {})
                    
                    # Eğer custom prompt varsa, fallback senaryoya ekle
                    if custom_prompt:
                        fallback_scenario['custom_prompt'] = custom_prompt
                        fallback_scenario['description'] += f"\n\nÖzel İstek: {custom_prompt}"
                    
                    return jsonify({
                        'success': True,
                        'scenario': fallback_scenario,
                        'warning': 'OpenAI API anahtarı olmadığı için fallback senaryo kullanıldı.',
                        'api_key_required': True
                    })
                else:
                    # Other RAG error - use basic fallback
                    fallback_scenario = {
                        'title': f'AI Üretilen {theme.title()} Senaryosu',
                        'description': f'Seviye {level} için özel olarak üretilen {difficulty} zorlukta senaryo.',
                        'difficulty': difficulty,
                        'theme': theme,
                        'story': f'AI tarafından üretilen özel bir hikaye. {theme.title()} temasında, seviye {level} için tasarlandı.',
                        'choices': [
                            "AI önerisi: İleri git",
                            "AI önerisi: Keşfet", 
                            "AI önerisi: Savaş",
                            "AI önerisi: Diplomasi"
                        ],
                        'note': 'RAG sistemi geçici olarak kullanılamıyor, fallback senaryo üretildi.'
                    }
                    
                    return jsonify({
                        'success': True,
                        'scenario': fallback_scenario,
                        'warning': 'RAG sistemi geçici olarak kullanılamıyor'
                    })
                
        except Exception as rag_error:
            # RAG hatası durumunda fallback
            fallback_scenario = {
                'title': f'AI Üretilen {theme.title()} Senaryosu',
                'description': f'Seviye {level} için özel olarak üretilen {difficulty} zorlukta senaryo.',
                'difficulty': difficulty,
                'theme': theme,
                'story': f'AI tarafından üretilen özel bir hikaye. {theme.title()} temasında, seviye {level} için tasarlandı.',
                'choices': [
                    "AI önerisi: İleri git",
                    "AI önerisi: Keşfet", 
                    "AI önerisi: Savaş",
                    "AI önerisi: Diplomasi"
                ],
                'note': 'RAG sistemi geçici olarak kullanılamıyor, fallback senaryo üretildi.'
            }
            
            return jsonify({
                'success': True,
                'scenario': fallback_scenario,
                'warning': f'RAG sistemi hatası: {str(rag_error)}'
            })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500



@app.route('/api/game/character/skills/<class_id>')
def get_character_skills(class_id):
    """Get skills for a specific character class"""
    try:
        character_class = next((cls for cls in CHARACTER_CLASSES if cls['id'] == class_id), None)
        if character_class:
            return jsonify({
                "success": True,
                "class_name": character_class['name'],
                "skills": character_class.get('skills', []),
                "special_abilities": character_class.get('special_abilities', [])
            })
        else:
            return jsonify({"success": False, "error": "Character class not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/scenarios')
def get_scenarios():
    try:
        with open('data/enhanced_scenarios.json', 'r', encoding='utf-8') as f:
            scenarios_data = json.load(f)
        
        # Senaryoları frontend formatına çevir
        scenarios_list = []
        enhanced_scenarios = scenarios_data.get('enhanced_scenarios', {})
        for scenario_id, scenario in enhanced_scenarios.items():
            scenarios_list.append({
                "id": scenario.get('id', scenario_id),
                "title": scenario.get('title', 'Bilinmeyen Senaryo'),
                "theme": scenario.get('theme', 'fantasy'),
                "difficulty": scenario.get('difficulty', 'medium'),
                "description": scenario.get('description', ''),
                "isFavorite": False,
                "createdAt": scenario.get('created_at', ''),
                "tags": [scenario.get('genre', 'fantasy')]
            })
        
        return jsonify({"success": True, "scenarios": scenarios_list})
    except Exception as e:
        print(f"Senaryo yükleme hatası: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

# Detaylı senaryo endpoint'i
@app.route('/api/scenario/<scenario_id>', methods=['GET'])
def get_detailed_scenario(scenario_id):
    try:
        # Senaryo verilerini yükle
        with open('data/enhanced_scenarios.json', 'r', encoding='utf-8') as f:
            scenarios_data = json.load(f)
        
        scenario = scenarios_data.get('enhanced_scenarios', {}).get(scenario_id)
        if not scenario:
            return jsonify({"success": False, "error": "Senaryo bulunamadı"}), 404
        
        # Kullanıcı bilgilerini al
        username = request.args.get('username', 'guest')
        
        # Kullanıcının bu senaryo için ilerleme durumunu kontrol et
        if username in STORY_DATA['story_progress'] and scenario_id in STORY_DATA['story_progress'][username]:
            progress = STORY_DATA['story_progress'][username][scenario_id]
            scenario['user_progress'] = progress
        else:
            # Yeni kullanıcı için başlangıç durumu
            scenario['user_progress'] = {
                'current_node': 'start',
                'visited_nodes': [],
                'choices_made': [],
                'karma': 0
            }
        
        # Kullanıcının karakter bilgilerini ekle
        if username in CHARACTER_DATA:
            scenario['character'] = CHARACTER_DATA[username]
        else:
            scenario['character'] = {
                'name': 'Yeni Kahraman',
                'race': 'İnsan',
                'class': 'Savaşçı',
                'level': 1,
                'xp': 0,
                'stats': {
                    'strength': 15,
                    'dexterity': 12,
                    'constitution': 14,
                    'intelligence': 10,
                    'wisdom': 8,
                    'charisma': 13
                }
            }
        
        # Kullanıcının NPC etkileşimlerini ekle
        if username in STORY_DATA['npc_interactions']:
            scenario['npc_interactions'] = STORY_DATA['npc_interactions'][username]
        else:
            scenario['npc_interactions'] = {}
        
        # Kullanıcının savaş geçmişini ekle
        if username in STORY_DATA['combat_history']:
            scenario['combat_history'] = STORY_DATA['combat_history'][username]
        else:
            scenario['combat_history'] = []
        
        # Kullanıcının ekipman ve envanter bilgilerini ekle
        if username in STORY_DATA['inventory']:
            scenario['inventory'] = STORY_DATA['inventory'][username]
        else:
            scenario['inventory'] = {
                'equipment': {
                    'weapon': 'Çelik Kılıç',
                    'armor': 'Deri Zırh',
                    'shield': '-',
                    'gloves': 'Büyülü Yüzük',
                    'boots': '-'
                },
                'items': ['⚔️', '🛡️', '🧪', '🍖', '💎', '📜', '🗝️', '🏹', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+']
            }
        
        # Kullanıcının aktif içeriklerini ekle
        if username in STORY_DATA['active_content']:
            scenario['active_content'] = STORY_DATA['active_content'][username]
        else:
            scenario['active_content'] = {
                'active': True,
                'unlocked_skills': [],
                'completed_nodes': []
            }
        
        return jsonify({"success": True, "scenario": scenario})
    except Exception as e:
        print(f"Detaylı senaryo yükleme hatası: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

# Hikaye sistemi endpoint'leri
@app.route('/api/story/scenario/<scenario_id>', methods=['GET'])
def get_scenario_details(scenario_id):
    try:
        # Senaryo detaylarını JSON dosyasından yükle
        with open('data/enhanced_scenarios.json', 'r', encoding='utf-8') as f:
            scenarios_data = json.load(f)
        
        scenario = scenarios_data.get('enhanced_scenarios', {}).get(scenario_id)
        if not scenario:
            return jsonify({"success": False, "error": "Senaryo bulunamadı"}), 404
        
        # Gelişmiş hikaye anlatımı özelliklerini ekle
        if 'advanced_storytelling' in scenario:
            # Contextual triggers'ları işle
            contextual_events = {}
            for trigger_name, trigger_data in scenario['advanced_storytelling'].get('contextual_triggers', {}).items():
                contextual_events[trigger_name] = {
                    "betrayal_chance": trigger_data.get('betrayal_chance', 0.3),
                    "plot_twist_chance": trigger_data.get('plot_twist_chance', 0.5),
                    "triggers": trigger_data.get('triggers', []),
                    "active": True
                }
            
            # Emotional arcs'ları ekle
            emotional_arcs = {}
            for arc_name, arc_data in scenario['advanced_storytelling'].get('emotional_arcs', {}).items():
                emotional_arcs[arc_name] = {
                    "stages": arc_data.get('stages', []),
                    "current_stage": 0,
                    "betrayal_impact": arc_data.get('betrayal_impact', 'moderate'),
                    "plot_twist_impact": arc_data.get('plot_twist_impact', 'moderate')
                }
            
            scenario['advanced_storytelling']['contextual_events'] = contextual_events
            scenario['advanced_storytelling']['emotional_arcs'] = emotional_arcs
        
        # Faction-specific content'ı işle
        if 'faction_specific_content' in scenario:
            for faction, content in scenario['faction_specific_content'].items():
                content['active'] = True
                content['unlocked_skills'] = []
                content['completed_nodes'] = []
        
        # Nodes yapısını koru, branches yapısını kaldır
        # Senaryo zaten nodes yapısına sahip, onu kullan
        if 'nodes' in scenario:
            # Nodes yapısını olduğu gibi bırak
            pass
        else:
            # Eğer nodes yapısı yoksa, basit bir branches yapısı oluştur
            scenario['branches'] = [
            {
                    "id": "main_story",
                "title": "Ana Hikaye",
                "description": "Senaryonun ana hikaye dalı",
                "choices": [
                    {"text": "Konuş", "next": "dialogue_1", "type": "dialogue"},
                        {"text": "Saldır", "next": "combat_1", "type": "combat", "npc_id": "enemy"},
                    {"text": "Kaç", "next": "escape_1", "type": "escape"}
                ]
            }
        ]
        
        return jsonify({"success": True, "scenario": scenario})
    except Exception as e:
        print(f"Senaryo detay yükleme hatası: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/story/progress', methods=['POST'])
def update_story_progress():
    try:
        data = request.get_json()
        username = data.get('username')
        scenario_id = data.get('scenario_id')
        current_node = data.get('current_node')
        choice = data.get('choice')
        
        if not username or not scenario_id:
            return jsonify({"success": False, "error": "Kullanıcı adı ve senaryo ID gerekli"}), 400
        
        # Hikaye ilerlemesini güncelle
        if username not in STORY_DATA['story_progress']:
            STORY_DATA['story_progress'][username] = {}
        
        if scenario_id not in STORY_DATA['story_progress'][username]:
            STORY_DATA['story_progress'][username][scenario_id] = {
                'current_node': 'start',
                'visited_nodes': [],
                'choices_made': [],
                'karma': 0
            }
        
        progress = STORY_DATA['story_progress'][username][scenario_id]
        progress['current_node'] = current_node
        progress['visited_nodes'].append(current_node)
        progress['choices_made'].append(choice)
        
        # Karma sistemi
        if choice == 'Konuş':
            progress['karma'] += 5
        elif choice == 'Saldır':
            progress['karma'] -= 10
        elif choice == 'Kaç':
            progress['karma'] -= 5
        
        return jsonify({
            "success": True,
            "progress": progress,
            "message": "Hikaye ilerlemesi güncellendi"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/story/npc/<npc_id>', methods=['GET'])
def get_npc_details(npc_id):
    try:
        npc = NPC_DATA.get(npc_id)
        if not npc:
            return jsonify({"success": False, "error": "NPC bulunamadı"}), 404
        
        return jsonify({"success": True, "npc": npc})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/story/npc/<npc_id>/interact', methods=['POST'])
def interact_with_npc(npc_id):
    try:
        data = request.get_json()
        interaction_type = data.get('interaction_type', 'greeting')
        username = data.get('username')
        
        npc = NPC_DATA.get(npc_id)
        if not npc:
            return jsonify({"success": False, "error": "NPC bulunamadı"}), 404
        
        # Etkileşim geçmişini kaydet
        if username not in STORY_DATA['npc_interactions']:
            STORY_DATA['npc_interactions'][username] = {}
        
        if npc_id not in STORY_DATA['npc_interactions'][username]:
            STORY_DATA['npc_interactions'][username][npc_id] = []
        
        STORY_DATA['npc_interactions'][username][npc_id].append({
            'type': interaction_type,
            'timestamp': datetime.now().isoformat()
        })
        
        # NPC yanıtını getir
        response = npc['dialogue'].get(interaction_type, "Merhaba!")
        
        return jsonify({
            "success": True,
            "npc_name": npc['name'],
            "response": response,
            "personality": npc['personality']
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/story/branches/<username>', methods=['GET'])
def get_user_story_branches(username):
    try:
        user_branches = STORY_DATA['story_branches'].get(username, [])
        return jsonify({
            "success": True,
            "branches": user_branches
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/story/branches', methods=['POST'])
def create_story_branch():
    try:
        data = request.get_json()
        username = data.get('username')
        title = data.get('title')
        description = data.get('description')
        
        if not username or not title:
            return jsonify({"success": False, "error": "Kullanıcı adı ve başlık gerekli"}), 400
        
        branch_id = f"branch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if username not in STORY_DATA['story_branches']:
            STORY_DATA['story_branches'][username] = []
        
        new_branch = {
            "id": branch_id,
            "title": title,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        STORY_DATA['story_branches'][username].append(new_branch)
        
        return jsonify({
            "success": True,
            "branch": new_branch,
            "message": "Hikaye dalı oluşturuldu"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Hikaye savaş sistemi endpoint'leri
@app.route('/api/story/combat/start', methods=['POST'])
def start_story_combat():
    """Hikaye içinde savaş başlat"""
    try:
        data = request.get_json()
        username = data.get('username')
        scenario_id = data.get('scenario_id')
        npc_id = data.get('npc_id')
        player_stats = data.get('player_stats', {})
        
        if not username or not scenario_id or not npc_id:
            return jsonify({"success": False, "error": "Kullanıcı adı, senaryo ID ve NPC ID gerekli"}), 400
        
        # NPC'yi kontrol et
        npc = NPC_DATA.get(npc_id)
        if not npc:
            return jsonify({"success": False, "error": "NPC bulunamadı"}), 404
        
        # Savaş ID'si oluştur
        combat_id = f"story_combat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Savaş durumunu kaydet
        if username not in STORY_DATA['story_combats']:
            STORY_DATA['story_combats'][username] = {}
        
        STORY_DATA['story_combats'][username][combat_id] = {
            "scenario_id": scenario_id,
            "npc_id": npc_id,
            "npc_name": npc['name'],
            "player_stats": player_stats,
            "npc_stats": npc['combat_stats'].copy(),
            "current_round": 1,
            "combat_log": [],
            "status": "active",
            "created_at": datetime.now().isoformat()
        }
        
        # İlk savaş mesajını ekle
        combat_data = STORY_DATA['story_combats'][username][combat_id]
        combat_data['combat_log'].append({
            "round": 1,
            "message": f"⚔️ {npc['name']} ile savaş başladı!",
            "type": "combat_start"
        })
        
        return jsonify({
            "success": True,
            "combat_id": combat_id,
            "npc_name": npc['name'],
            "npc_stats": npc['combat_stats'],
            "message": f"{npc['name']} ile savaş başladı!"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/story/combat/<combat_id>/action', methods=['POST'])
def perform_story_combat_action(combat_id):
    """Hikaye savaşında aksiyon yap"""
    try:
        data = request.get_json()
        username = data.get('username')
        action_type = data.get('action_type')  # 'attack', 'defend', 'special'
        special_ability = data.get('special_ability')
        
        if not username or not action_type:
            return jsonify({"success": False, "error": "Kullanıcı adı ve aksiyon türü gerekli"}), 400
        
        # Savaş durumunu kontrol et
        if username not in STORY_DATA['story_combats'] or combat_id not in STORY_DATA['story_combats'][username]:
            return jsonify({"success": False, "error": "Savaş bulunamadı"}), 404
        
        combat_data = STORY_DATA['story_combats'][username][combat_id]
        if combat_data['status'] != 'active':
            return jsonify({"success": False, "error": "Savaş zaten sona erdi"}), 400
        
        # NPC'yi al
        npc = NPC_DATA.get(combat_data['npc_id'])
        if not npc:
            return jsonify({"success": False, "error": "NPC bulunamadı"}), 404
        
        # Savaş turunu işle
        round_result = process_story_combat_round(combat_data, action_type, special_ability, npc)
        
        # Savaş durumunu güncelle
        combat_data['current_round'] += 1
        combat_data['combat_log'].extend(round_result['log'])
        
        # Savaş sonu kontrolü
        if round_result['combat_ended']:
            combat_data['status'] = 'ended'
            combat_data['winner'] = round_result['winner']
            
            # Hikaye ilerlemesini güncelle
            if username not in STORY_DATA['story_progress']:
                STORY_DATA['story_progress'][username] = {}
            
            if combat_data['scenario_id'] not in STORY_DATA['story_progress'][username]:
                STORY_DATA['story_progress'][username][combat_data['scenario_id']] = {
                    'current_node': 'combat_result',
                    'visited_nodes': [],
                    'choices_made': [],
                    'karma': 0
                }
            
            progress = STORY_DATA['story_progress'][username][combat_data['scenario_id']]
            if round_result['winner'] == 'player':
                progress['karma'] += 10
                progress['choices_made'].append(f"Defeated {npc['name']}")
            else:
                progress['karma'] -= 5
                progress['choices_made'].append(f"Lost to {npc['name']}")
        
        return jsonify({
            "success": True,
            "combat_status": combat_data['status'],
            "round_result": round_result,
            "combat_data": combat_data,
            "message": "Savaş aksiyonu tamamlandı"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/story/combat/<combat_id>/status', methods=['GET'])
def get_story_combat_status(combat_id):
    """Hikaye savaş durumunu getir"""
    try:
        username = request.args.get('username')
        
        if not username:
            return jsonify({"success": False, "error": "Kullanıcı adı gerekli"}), 400
        
        if username not in STORY_DATA['story_combats'] or combat_id not in STORY_DATA['story_combats'][username]:
            return jsonify({"success": False, "error": "Savaş bulunamadı"}), 404
        
        combat_data = STORY_DATA['story_combats'][username][combat_id]
        
        return jsonify({
            "success": True,
            "combat_data": combat_data
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

def process_story_combat_round(combat_data, player_action, special_ability, npc):
    """Hikaye savaş turunu işle"""
    log = []
    combat_ended = False
    winner = None
    
    # Oyuncu aksiyonu
    if player_action == 'attack':
        damage = max(1, combat_data['player_stats'].get('attack', 5) - combat_data['npc_stats']['defense'])
        combat_data['npc_stats']['hp'] -= damage
        log.append({
            "round": combat_data['current_round'],
            "message": f"⚔️ Saldırı yaptınız! {damage} hasar verdiniz.",
            "type": "player_attack"
        })
    elif player_action == 'defend':
        log.append({
            "round": combat_data['current_round'],
            "message": "🛡️ Savunma pozisyonu aldınız.",
            "type": "player_defend"
        })
    elif player_action == 'special' and special_ability:
        # Özel yetenek kullanımı
        damage = max(2, combat_data['player_stats'].get('attack', 5) * 1.5 - combat_data['npc_stats']['defense'])
        combat_data['npc_stats']['hp'] -= damage
        log.append({
            "round": combat_data['current_round'],
            "message": f"✨ {special_ability} kullandınız! {damage} hasar verdiniz.",
            "type": "player_special"
        })
    
    # NPC ölüm kontrolü
    if combat_data['npc_stats']['hp'] <= 0:
        combat_ended = True
        winner = 'player'
        log.append({
            "round": combat_data['current_round'],
            "message": f"🏆 {npc['name']} yenildi! Zafer kazandınız!",
            "type": "combat_end"
        })
        return {"log": log, "combat_ended": combat_ended, "winner": winner}
    
    # NPC aksiyonu
    npc_action = 'attack'  # Basit AI
    if npc_action == 'attack':
        damage = max(1, combat_data['npc_stats']['attack'] - combat_data['player_stats'].get('defense', 3))
        combat_data['player_stats']['hp'] -= damage
        log.append({
            "round": combat_data['current_round'],
            "message": f"⚔️ {npc['name']} saldırdı! {damage} hasar aldınız.",
            "type": "npc_attack"
        })
    
    # Oyuncu ölüm kontrolü
    if combat_data['player_stats']['hp'] <= 0:
        combat_ended = True
        winner = 'npc'
        log.append({
            "round": combat_data['current_round'],
            "message": f"💀 {npc['name']} sizi yendi! Yenildiniz!",
            "type": "combat_end"
        })
    
    return {"log": log, "combat_ended": combat_ended, "winner": winner}

# Auth endpoints
@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    try:
        data = request.get_json()
        username = data.get('username', '')
        password = data.get('password', '')
        
        # Basit doğrulama (gerçek uygulamada veritabanı kullanılır)
        if username and password:
            return jsonify({
                "success": True,
                "token": f"token_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "username": username,
                "message": "Giriş başarılı!"
            })
        else:
            return jsonify({"success": False, "error": "Kullanıcı adı ve şifre gerekli"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/auth/register', methods=['POST'])
def auth_register():
    try:
        data = request.get_json()
        username = data.get('username', '')
        email = data.get('email', '')
        password = data.get('password', '')
        
        if username and email and password:
            return jsonify({
                "success": True,
                "message": "Kayıt başarılı!"
            })
        else:
            return jsonify({"success": False, "error": "Tüm alanlar gerekli"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/auth/guest', methods=['POST'])
def auth_guest_login():
    try:
        guest_username = f"Misafir_{datetime.now().strftime('%H%M%S')}"
        return jsonify({
            "success": True,
            "token": f"guest_token_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "username": guest_username,
            "message": "Misafir girişi başarılı!"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/game/session/start', methods=['POST'])
def start_game_session():
    try:
        data = request.get_json()
        player_name = data.get('player_name', 'Unknown')
        scenario_id = data.get('scenario_id', '1')
        
        return jsonify({
            "success": True,
            "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "player_name": player_name,
            "scenario_id": scenario_id,
            "message": "Oyun başlatıldı!"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Combat endpoints
@app.route('/api/combat/start', methods=['POST'])
def start_combat():
    try:
        data = request.get_json()
        player_character = data.get('player_character', {})
        enemies = data.get('enemies', [])
        
        session_id = f"combat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "message": "Savaş başlatıldı!",
            "player": player_character,
            "enemies": enemies
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Dice endpoints
@app.route('/api/dice/roll', methods=['POST'])
def roll_dice():
    try:
        data = request.get_json()
        dice = data.get('dice', '1d20')
        
        # Basit zar atma simülasyonu
        import random
        if 'd' in dice:
            num, sides = dice.split('d')
            num = int(num) if num else 1
            sides = int(sides)
            result = sum(random.randint(1, sides) for _ in range(num))
        else:
            result = random.randint(1, 20)
        
        return jsonify({
            "success": True,
            "dice": dice,
            "result": result,
            "message": f"Zar atıldı: {result}"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Save/Load endpoints
@app.route('/api/game/save', methods=['POST'])
def save_game():
    try:
        data = request.get_json()
        username = data.get('username', 'Unknown')
        save_name = data.get('save_name', f'Save_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        game_data = data.get('game_data', {})
        
        if username not in GAME_SAVES:
            GAME_SAVES[username] = {}
        
        GAME_SAVES[username][save_name] = {
            'save_name': save_name,
            'username': username,
            'game_data': game_data,
            'save_date': datetime.now().isoformat(),
            'character': game_data.get('character', {}),
            'scenario': game_data.get('scenario', {}),
            'progress': game_data.get('progress', {}),
            'inventory': game_data.get('inventory', []),
            'quests': game_data.get('quests', []),
            'stats': game_data.get('stats', {})
        }
        
        return jsonify({
            "success": True,
            "save_name": save_name,
            "message": f"Oyun kaydedildi: {save_name}"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/game/load', methods=['POST'])
def load_game():
    try:
        data = request.get_json()
        username = data.get('username', 'Unknown')
        save_name = data.get('save_name', '')
        
        if username in GAME_SAVES and save_name in GAME_SAVES[username]:
            save_data = GAME_SAVES[username][save_name]
            return jsonify({
                "success": True,
                "save_data": save_data,
                "message": f"Oyun yüklendi: {save_name}"
            })
        else:
            return jsonify({"success": False, "error": "Kayıt bulunamadı"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/game/saves/<username>')
def get_saves(username):
    try:
        if username in GAME_SAVES:
            saves = []
            for save_name, save_data in GAME_SAVES[username].items():
                saves.append({
                    'save_name': save_name,
                    'save_date': save_data['save_date'],
                    'character_name': save_data.get('character', {}).get('name', 'Bilinmeyen'),
                    'level': save_data.get('stats', {}).get('level', 1),
                    'scenario': save_data.get('scenario', {}).get('title', 'Bilinmeyen')
                })
            return jsonify({"success": True, "saves": saves})
        else:
            return jsonify({"success": True, "saves": []})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/game/delete_save', methods=['DELETE'])
def delete_save():
    try:
        data = request.get_json()
        username = data.get('username', 'Unknown')
        save_name = data.get('save_name', '')
        
        if username in GAME_SAVES and save_name in GAME_SAVES[username]:
            del GAME_SAVES[username][save_name]
            return jsonify({
                "success": True,
                "message": f"Kayıt silindi: {save_name}"
            })
        else:
            return jsonify({"success": False, "error": "Kayıt bulunamadı"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Multiplayer endpoints
@app.route('/api/multiplayer/sessions', methods=['GET'])
def get_sessions():
    """Get all available multiplayer sessions"""
    try:
        sessions = []
        for session_id, session in session_manager.active_sessions.items():
            if session.status == SessionStatus.LOBBY:
                sessions.append({
                    'id': session_id,
                    'name': session.name,
                    'scenario_id': session.scenario_id,
                    'current_players': len(session.current_players),
                    'max_players': session.max_players,
                    'created_at': session.created_at.isoformat()
                })
        return jsonify({"success": True, "sessions": sessions})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/multiplayer/create_session', methods=['POST'])
def create_session():
    """Create a new multiplayer session"""
    try:
        data = request.get_json()
        name = data.get('name', 'Yeni Oyun')
        scenario_id = data.get('scenario_id', '1')
        max_players = data.get('max_players', 4)
        creator_id = data.get('creator_id', 'unknown')
        
        session = session_manager.create_session(name, scenario_id, max_players, creator_id)
        
        return jsonify({
            "success": True,
            "session_id": session.id,
            "message": f"Oyun oluşturuldu: {name}"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/multiplayer/join_session', methods=['POST'])
def join_session():
    """Join a multiplayer session"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        username = data.get('username', 'Misafir')
        
        # Generate player_id from username if not provided
        player_id = data.get('player_id', f"player_{username}")
        
        result = session_manager.join_session(session_id, player_id, username)
        
        if result['success']:
            session_name = result.get('session', {}).get('name', 'Bilinmeyen Oyun')
            return jsonify({
                "success": True,
                "message": f"Oyuna katıldınız: {session_name}",
                "player_id": player_id
            })
        else:
            return jsonify({"success": False, "error": result['error']}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/multiplayer/leave_session', methods=['POST'])
def leave_session():
    """Leave a multiplayer session"""
    try:
        data = request.get_json()
        player_id = data.get('player_id')
        
        result = session_manager.leave_session(player_id)
        
        if result['success']:
            return jsonify({
                "success": True,
                "message": "Oyundan ayrıldınız"
            })
        else:
            return jsonify({"success": False, "error": result['error']}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/multiplayer/start_session', methods=['POST'])
def start_session():
    """Start a multiplayer session"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        creator_id = data.get('creator_id')
        
        result = session_manager.start_session(session_id, creator_id)
        
        if result['success']:
            return jsonify({
                "success": True,
                "message": "Oyun başlatıldı!"
            })
        else:
            return jsonify({"success": False, "error": result['error']}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/multiplayer/session/<session_id>')
def get_session_info(session_id):
    """Get session information"""
    try:
        session_info = session_manager.get_session_info(session_id)
        if session_info:
            return jsonify({"success": True, "session": session_info})
        else:
            return jsonify({"success": False, "error": "Oyun bulunamadı"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/multiplayer/create_room', methods=['POST'])
def create_room():
    """Create a new multiplayer room for turn-based gameplay"""
    try:
        data = request.get_json()
        room_name = data.get('room_name', 'Yeni Oda')
        room_id = data.get('room_id', f"room_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        scenario_id = data.get('scenario_id', 'fantasy_forest')
        max_players = data.get('max_players', 4)
        creator_username = data.get('creator_username', 'Misafir')
        
        # Create a unique room ID if not provided
        if not room_id:
            room_id = f"room_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{creator_username}"
        
        # Create session with room-specific data
        session = session_manager.create_session(
            name=room_name,
            scenario_id=scenario_id,
            max_players=max_players,
            creator_id=creator_username
        )
        
        # Add room-specific game state
        session.game_state = {
            'room_id': room_id,
            'current_turn': 0,
            'turn_order': [],
            'current_player': None,
            'game_phase': 'lobby',  # lobby, character_creation, in_game, combat
            'scenario_progress': 0,
            'shared_inventory': [],
            'group_decisions': [],
            'players': []
        }
        
        return jsonify({
            "success": True,
            "room_id": room_id,
            "room_name": room_name,
            "message": f"Oda oluşturuldu: {room_name}",
            "creator": creator_username
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/multiplayer/join_room', methods=['POST'])
def join_room():
    """Join an existing multiplayer room"""
    try:
        data = request.get_json()
        room_id = data.get('room_id')
        player_name = data.get('player_name', 'Oyuncu')
        player_id = data.get('player_id', f"player_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        if not room_id:
            return jsonify({"success": False, "error": "Oda ID gerekli"}), 400
        
        # Find the session by room_id
        session = None
        for s in session_manager.sessions.values():
            if s.game_state and s.game_state.get('room_id') == room_id:
                session = s
                break
        
        if not session:
            return jsonify({"success": False, "error": "Oda bulunamadı"}), 404
        
        # Check if room is full
        if len(session.players) >= session.max_players:
            return jsonify({"success": False, "error": "Oda dolu"}), 400
        
        # Add player to session
        result = session_manager.join_session(session.id, player_id, player_name)
        
        if result['success']:
            return jsonify({
                "success": True,
                "room_id": room_id,
                "player_id": player_id,
                "player_name": player_name,
                "message": f"Odaya katıldınız: {session.name}"
            })
        else:
            return jsonify({"success": False, "error": result['error']}), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/multiplayer/room/<room_id>/status', methods=['GET'])
def get_room_status(room_id):
    """Get the current status of a multiplayer room"""
    try:
        # Find the session by room_id
        session = None
        for s in session_manager.sessions.values():
            if s.game_state and s.game_state.get('room_id') == room_id:
                session = s
                break
        
        if not session:
            return jsonify({"success": False, "error": "Oda bulunamadı"}), 404
        
        return jsonify({
            "success": True,
            "room_id": room_id,
            "room_name": session.name,
            "players": session.players,
            "game_state": session.game_state,
            "status": session.status.value
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

def process_turn(session, username, action, action_data):
    """Process a player's turn"""
    # This is where you'd implement the actual game logic
    # For now, we'll just return a simple response
    return {
        "player": username,
        "action": action,
        "result": f"{username} {action} aksiyonunu gerçekleştirdi",
        "timestamp": datetime.now().isoformat()
    }

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"Client connected: {request.sid}")
    emit('connected', {'message': 'Bağlantı kuruldu!'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f"Client disconnected: {request.sid}")
    # Player cleanup logic here

@socketio.on('join_session')
def handle_join_session(data):
    """Handle joining a session via WebSocket"""
    try:
        session_id = data.get('session_id')
        player_id = data.get('player_id')
        username = data.get('username')
        
        join_room(session_id)
        
        # Update session manager
        result = session_manager.join_session(session_id, player_id, username)
        
        if result['success']:
            session_name = result.get('session', {}).get('name', 'Bilinmeyen Oyun')
            emit('session_joined', {
                'success': True,
                'session_id': session_id,
                'message': f'Oyuna katıldınız: {session_name}'
            }, room=session_id)
            
            # Broadcast to other players
            emit('player_joined', {
                'player_id': player_id,
                'username': username,
                'message': f'{username} oyuna katıldı!'
            }, room=session_id, include_self=False)
        else:
            emit('session_joined', {
                'success': False,
                'error': result['error']
            })
    except Exception as e:
        emit('session_joined', {
            'success': False,
            'error': str(e)
        })

@socketio.on('leave_session')
def handle_leave_session(data):
    """Handle leaving a session via WebSocket"""
    try:
        session_id = data.get('session_id')
        player_id = data.get('player_id')
        username = data.get('username')
        
        leave_room(session_id)
        
        result = session_manager.leave_session(player_id)
        
        if result['success']:
            emit('session_left', {
                'success': True,
                'message': 'Oyundan ayrıldınız'
            })
            
            # Broadcast to other players
            emit('player_left', {
                'player_id': player_id,
                'username': username,
                'message': f'{username} oyundan ayrıldı!'
            }, room=session_id)
    except Exception as e:
        emit('session_left', {
            'success': False,
            'error': str(e)
        })

@socketio.on('chat_message')
def handle_chat_message(data):
    """Handle chat messages"""
    try:
        session_id = data.get('session_id')
        player_id = data.get('player_id')
        username = data.get('username')
        message = data.get('message')
        
        # Add to session chat history
        result = session_manager.send_chat_message(session_id, player_id, message)
        
        if result['success']:
            emit('chat_message', {
                'player_id': player_id,
                'username': username,
                'message': message,
                'timestamp': result['timestamp']
            }, room=session_id)
        else:
            emit('chat_error', {
                'error': result['error']
            })
    except Exception as e:
        emit('chat_error', {
            'error': str(e)
        })

@socketio.on('game_action')
def handle_game_action(data):
    """Handle game actions (combat, dice, etc.)"""
    try:
        session_id = data.get('session_id')
        player_id = data.get('player_id')
        action_type = data.get('action_type')
        action_data = data.get('action_data', {})
        
        # Broadcast action to all players in session
        emit('game_action', {
            'player_id': player_id,
            'action_type': action_type,
            'action_data': action_data,
            'timestamp': datetime.now().isoformat()
        }, room=session_id)
        
    except Exception as e:
        emit('game_error', {
            'error': str(e)
        })

# Room-specific WebSocket handlers
@socketio.on('join_room')
def handle_join_room(data):
    """Handle joining a room via WebSocket"""
    try:
        room_id = data.get('room_id')
        player_id = data.get('player_id')
        player_name = data.get('player_name')
        
        if not room_id or not player_id:
            emit('room_joined', {
                'success': False,
                'error': 'Oda ID ve Oyuncu ID gerekli'
            })
            return
        
        # Find the session by room_id
        session = None
        for s in session_manager.sessions.values():
            if s.game_state and s.game_state.get('room_id') == room_id:
                session = s
                break
        
        if not session:
            emit('room_joined', {
                'success': False,
                'error': 'Oda bulunamadı'
            })
            return
        
        # Join the room
        join_room(room_id)
        
        # Add player to session
        result = session_manager.join_session(session.id, player_id, player_name)
        
        if result['success']:
            # Update session game state
            if 'players' not in session.game_state:
                session.game_state['players'] = []
            
            session.game_state['players'].append({
                'id': player_id,
                'name': player_name,
                'status': 'online'
            })
            
            emit('room_joined', {
                'success': True,
                'room_id': room_id,
                'players': session.game_state['players'],
                'message': f'Odaya katıldınız: {session.name}'
            }, room=room_id)
            
            # Broadcast to other players
            emit('player_joined', {
                'player_id': player_id,
                'player_name': player_name,
                'players': session.game_state['players'],
                'message': f'{player_name} oyuna katıldı!'
            }, room=room_id, include_self=False)
        else:
            emit('room_joined', {
                'success': False,
                'error': result['error']
            })
    except Exception as e:
        emit('room_joined', {
            'success': False,
            'error': str(e)
        })

@socketio.on('leave_room')
def handle_leave_room(data):
    """Handle leaving a room via WebSocket"""
    try:
        room_id = data.get('room_id')
        player_id = data.get('player_id')
        
        # Find the session by room_id
        session = None
        for s in session_manager.sessions.values():
            if s.game_state and s.game_state.get('room_id') == room_id:
                session = s
                break
        
        if session and 'players' in session.game_state:
            # Remove player from session
            session.game_state['players'] = [
                p for p in session.game_state['players'] 
                if p['id'] != player_id
            ]
            
            # Broadcast to other players
            emit('player_left', {
                'player_id': player_id,
                'players': session.game_state['players'],
                'message': f'Oyuncu oyundan ayrıldı'
            }, room=room_id)
        
        leave_room(room_id)
        
    except Exception as e:
        print(f"Error leaving room: {e}")

@socketio.on('start_game')
def handle_start_game(data):
    """Handle starting a multiplayer game"""
    try:
        room_id = data.get('room_id')
        
        # Find the session by room_id
        session = None
        for s in session_manager.sessions.values():
            if s.game_state and s.game_state.get('room_id') == room_id:
                session = s
                break
        
        if not session:
            emit('game_started', {
                'success': False,
                'error': 'Oda bulunamadı'
            })
            return
        
        # Update game state
        session.game_state['game_phase'] = 'in_game'
        session.game_state['scenario_progress'] = 0
        
        # Get initial scenario content
        from templates.game import advancedScenarios
        scenario = advancedScenarios.get('forest', {})
        initial_node = scenario.get('nodes', {}).get('start', {})
        
        emit('game_started', {
            'success': True,
            'room_id': room_id,
            'scenario': {
                'title': initial_node.get('title', 'Hikaye Başlıyor'),
                'description': initial_node.get('description', 'Hikaye başlıyor...'),
                'choices': initial_node.get('choices', [])
            }
        }, room=room_id)
        
    except Exception as e:
        emit('game_started', {
            'success': False,
            'error': str(e)
        })

@socketio.on('make_choice')
def handle_make_choice(data):
    """Handle player making a choice in the story"""
    try:
        room_id = data.get('room_id')
        player_id = data.get('player_id')
        choice_id = data.get('choice_id')
        
        # Find the session by room_id
        session = None
        for s in session_manager.sessions.values():
            if s.game_state and s.game_state.get('room_id') == room_id:
                session = s
                break
        
        if not session:
            return
        
        # Update story progress (simplified for now)
        session.game_state['scenario_progress'] += 1
        
        # Get next story content (simplified)
        from templates.game import advancedScenarios
        scenario = advancedScenarios.get('forest', {})
        nodes = scenario.get('nodes', {})
        
        # Simple story progression
        story_nodes = ['start', 'explore_area', 'village_path', 'village_dialogue']
        current_progress = session.game_state['scenario_progress']
        
        if current_progress < len(story_nodes):
            current_node = story_nodes[current_progress]
            node_data = nodes.get(current_node, {})
            
            emit('story_update', {
                'room_id': room_id,
                'scenario': {
                    'title': node_data.get('title', 'Hikaye Devam Ediyor'),
                    'description': node_data.get('description', 'Hikaye devam ediyor...'),
                    'choices': node_data.get('choices', [])
                }
            }, room=room_id)
        
    except Exception as e:
        print(f"Error making choice: {e}")

@socketio.on('chat_message')
def handle_chat_message(data):
    """Handle chat messages in room"""
    try:
        room_id = data.get('room_id')
        player_name = data.get('player_name')
        message = data.get('message')
        
        if room_id and player_name and message:
            emit('chat_message', {
                'player_name': player_name,
                'message': message
            }, room=room_id)
            
    except Exception as e:
        print(f"Error handling chat message: {e}")

@app.route('/api/game/campaign/<campaign_id>/scene/<scene_id>', methods=['GET'])
def get_campaign_scene(campaign_id, scene_id):
    """Kampanya sahnesini getir"""
    try:
        from src.core.campaign_manager import CampaignManager
        campaign_manager = CampaignManager()
        
        # Kampanya sahnesini al
        scene = campaign_manager.get_campaign_step(campaign_id, scene_id)
        
        if scene:
            return jsonify({
                "success": True,
                "scene": scene
            })
        else:
            return jsonify({
                "success": False,
                "error": "Sahne bulunamadı"
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/api/game/campaign/<campaign_id>/choice/<choice_id>', methods=['POST'])
def make_campaign_choice(campaign_id, choice_id):
    """Kampanya seçimi yap"""
    try:
        from src.core.campaign_manager import CampaignManager
        campaign_manager = CampaignManager()
        
        # Seçim sonucunu al
        result = campaign_manager.get_choice_result(campaign_id, choice_id)
        
        if result:
            return jsonify({
                "success": True,
                "result": result
            })
        else:
            return jsonify({
                "success": False,
                "error": "Seçim sonucu bulunamadı"
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/api/game/campaigns', methods=['GET'])
def get_campaigns():
    """Tüm kampanyaları getir"""
    try:
        from src.core.campaign_manager import CampaignManager
        campaign_manager = CampaignManager()
        
        campaigns = campaign_manager.list_campaigns()
        
        return jsonify({
            "success": True,
            "campaigns": campaigns
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/api/game/progress/save', methods=['POST'])
def save_game_progress():
    """Save game progress for advanced storytelling system"""
    try:
        data = request.get_json()
        game_progress = data.get('game_progress', {})
        character = data.get('character', {})
        
        # Save to file
        progress_data = {
            'game_progress': game_progress,
            'character': character,
            'timestamp': datetime.now().isoformat()
        }
        
        # Create saves directory if it doesn't exist
        os.makedirs('saves', exist_ok=True)
        
        # Save to file
        filename = f"saves/game_progress_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            "success": True,
            "message": "Oyun ilerlemesi kaydedildi",
            "filename": filename
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/game/progress/load/<filename>', methods=['GET'])
def load_game_progress(filename):
    """Load game progress from file"""
    try:
        filepath = f"saves/{filename}"
        if not os.path.exists(filepath):
            return jsonify({"success": False, "error": "Dosya bulunamadı"}), 404
        
        with open(filepath, 'r', encoding='utf-8') as f:
            progress_data = json.load(f)
        
        return jsonify({
            "success": True,
            "game_progress": progress_data.get('game_progress', {}),
            "character": progress_data.get('character', {})
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/story/advanced/<scenario_id>', methods=['GET'])
def get_advanced_storytelling(scenario_id):
    try:
        # Load scenario with advanced storytelling features
        with open('data/enhanced_scenarios.json', 'r', encoding='utf-8') as f:
            scenarios_data = json.load(f)
        
        scenario = scenarios_data.get('enhanced_scenarios', {}).get(scenario_id)
        if not scenario:
            return jsonify({"success": False, "error": "Senaryo bulunamadı"}), 404
        
        # Process advanced storytelling features
        if 'advanced_storytelling' in scenario:
            # Generate contextual events based on triggers
            contextual_events = {}
            for trigger_name, trigger_data in scenario['advanced_storytelling'].get('contextual_triggers', {}).items():
                # Randomly determine if events should trigger
                import random
                should_trigger = random.random() < 0.3  # 30% chance
                
                contextual_events[trigger_name] = {
                    "active": should_trigger,
                    "betrayal_chance": trigger_data.get('betrayal_chance', 0.3),
                    "plot_twist_chance": trigger_data.get('plot_twist_chance', 0.5),
                    "triggers": trigger_data.get('triggers', []),
                    "current_event": random.choice(trigger_data.get('triggers', ['default_event'])) if should_trigger else None
                }
            
            # Process emotional arcs
            emotional_arcs = {}
            for arc_name, arc_data in scenario['advanced_storytelling'].get('emotional_arcs', {}).items():
                emotional_arcs[arc_name] = {
                    "stages": arc_data.get('stages', []),
                    "current_stage": 0,
                    "betrayal_impact": arc_data.get('betrayal_impact', 'moderate'),
                    "plot_twist_impact": arc_data.get('plot_twist_impact', 'moderate'),
                    "progress": 0.0
                }
            
            scenario['advanced_storytelling']['contextual_events'] = contextual_events
            scenario['advanced_storytelling']['emotional_arcs'] = emotional_arcs
        
        return jsonify({
            "success": True, 
            "advanced_storytelling": scenario.get('advanced_storytelling', {}),
            "faction_content": scenario.get('faction_specific_content', {}),
            "nodes": scenario.get('nodes', {})
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/data/enhanced_scenarios.json')
def get_enhanced_scenarios():
    """Serve enhanced scenarios JSON file"""
    try:
        with open('data/enhanced_scenarios.json', 'r', encoding='utf-8') as f:
            scenarios_data = json.load(f)
        
        return jsonify(scenarios_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Additional RAG endpoints for advanced functionality
@app.route('/api/rag/ask', methods=['POST'])
def rag_ask_question():
    """Ask question using RAG system"""
    try:
        from rag.main import RAGSystem
        rag_system = RAGSystem()
        
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({"error": "No question provided"}), 400
        
        result = rag_system.ask_question(question)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Question failed: {str(e)}"}), 500

# AI Agent Endpoints
@app.route('/api/agents/status', methods=['GET'])
def get_agents_status():
    """Get status of all AI agents"""
    try:
        from agents.agent_orchestrator import AgentOrchestrator
        orchestrator = AgentOrchestrator()
        status = orchestrator.get_orchestrator_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": f"Failed to get agent status: {str(e)}"}), 500

@app.route('/api/agents/story/create', methods=['POST'])
def agent_create_story():
    """Create story using AI agent"""
    try:
        from agents.story_generation_agent import StoryGenerationAgent
        
        data = request.get_json()
        theme = data.get('theme', 'fantasy')
        complexity = data.get('complexity', 'medium')
        length = data.get('length', 'medium')
        custom_elements = data.get('custom_elements', {})
        
        agent = StoryGenerationAgent()
        result = agent.create_story(
            theme=theme,
            complexity=complexity,
            length=length,
            custom_elements=custom_elements
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Story creation failed: {str(e)}"}), 500

@app.route('/api/agents/character/generate', methods=['POST'])
def agent_generate_character():
    """Generate character using AI agent"""
    try:
        from agents.character_management_agent import CharacterManagementAgent
        
        data = request.get_json()
        theme = data.get('theme', 'fantasy')
        character_type = data.get('character_type', 'player')
        level = data.get('level', 1)
        
        agent = CharacterManagementAgent()
        result = agent.generate_character(
            theme=theme,
            character_type=character_type,
            level=level
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Character generation failed: {str(e)}"}), 500

@app.route('/api/agents/content/curate', methods=['POST'])
def agent_curate_content():
    """Curate content using AI agent"""
    try:
        from agents.content_curator_agent import ContentCuratorAgent
        
        data = request.get_json()
        content_type = data.get('content_type', 'scenario')
        theme = data.get('theme', 'fantasy')
        quality_level = data.get('quality_level', 'high')
        
        agent = ContentCuratorAgent()
        result = agent.curate_content(
            content_type=content_type,
            theme=theme,
            quality_level=quality_level
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Content curation failed: {str(e)}"}), 500

@app.route('/api/agents/workflow/create', methods=['POST'])
def agent_create_workflow():
    """Create automated workflow using AI agents"""
    try:
        from agents.agent_orchestrator import AgentOrchestrator
        
        data = request.get_json()
        workflow_name = data.get('workflow_name', 'Custom Workflow')
        steps = data.get('steps', [])
        
        orchestrator = AgentOrchestrator()
        workflow_id = orchestrator.create_workflow(workflow_name, steps)
        
        return jsonify({
            "success": True,
            "workflow_id": workflow_id,
            "message": "Workflow created successfully"
        })
        
    except Exception as e:
        return jsonify({"error": f"Workflow creation failed: {str(e)}"}), 500

@app.route('/api/agents/workflow/execute/<workflow_id>', methods=['POST'])
def agent_execute_workflow(workflow_id):
    """Execute automated workflow"""
    try:
        from agents.agent_orchestrator import AgentOrchestrator
        
        orchestrator = AgentOrchestrator()
        result = orchestrator.execute_workflow(workflow_id)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Workflow execution failed: {str(e)}"}), 500

# Advanced Storytelling Endpoints
@app.route('/api/story/advanced/generate', methods=['POST'])
def generate_advanced_story():
    """Generate advanced book-like story"""
    try:
        data = request.get_json()
        theme = data.get('theme', 'fantasy')
        story_type = data.get('story_type', 'adventure')
        complexity = data.get('complexity', 'medium')
        length = data.get('length', 'medium')
        
        # Generate immersive story introduction
        story_intro = generate_story_introduction(theme, story_type, complexity)
        
        # Generate story nodes with advanced features
        story_nodes = generate_story_nodes(theme, story_type, complexity, length)
        
        # Generate emotional arcs
        emotional_arcs = generate_emotional_arcs(theme, story_type)
        
        # Generate contextual events
        contextual_events = generate_contextual_events(theme, story_type)
        
        return jsonify({
            "success": True,
            "story": {
                "introduction": story_intro,
                "nodes": story_nodes,
                "emotional_arcs": emotional_arcs,
                "contextual_events": contextual_events,
                "theme": theme,
                "story_type": story_type,
                "complexity": complexity,
                "length": length
            }
        })
        
    except Exception as e:
        return jsonify({"error": f"Story generation failed: {str(e)}"}), 500

def generate_story_introduction(theme, story_type, complexity):
    """Generate immersive story introduction"""
    introductions = {
        "fantasy": {
            "adventure": [
                "Güneşin ilk ışıkları antik ormanın yaprakları arasından süzülürken, sen kendini efsanevi bir yolculuğun başlangıcında buldun. Büyülü dünyanın derinliklerinde, her adımın yeni bir sır keşfettiği, her kararın kaderini değiştirdiği bir macera seni bekliyor.",
                "Antik harabelerin gölgesinde duruyorsun. Kayıp uygarlığın sırları seni çağırıyor. Büyülü enerjiler etrafında dans ediyor ve sen bu gizemli dünyanın merkezinde, her kararın yeni bir kapı açtığı bir yolculuğa çıkıyorsun.",
                "Ejderhaların uçtuğu gökyüzünde, büyülü krallıkların sınırlarında, sen kendini efsanevi bir destanın kahramanı olarak buldun. Her nefes alışında, her adımında, büyülü dünyanın sırları seni daha derinlere çekiyor."
            ],
            "mystery": [
                "Gizemli bir cinayet seni büyülü dünyanın karanlık sokaklarına sürükledi. Her ipucu yeni bir sır perdesini aralıyor ve sen bu karmaşık labirentin merkezinde, gerçeği bulmak için her şeyi riske atıyorsun.",
                "Antik bir lanet şehri sardı. Büyülü enerjiler bozulmuş ve sen bu karanlık gizemin çözümü için tek umut olarak ortaya çıktın. Her adımın yeni bir tehlike, her kararın yeni bir sır açtığı bir yolculuk başlıyor."
            ]
        },
        "warhammer": {
            "battle": [
                "Hive şehrinin savunma pozisyonlarındasın. Ork istilası yaklaşıyor ve sen İmperium'un son savunma hattındasın. Her karar şehrin kaderini belirleyecek, her savaş yeni bir kahramanlık destanı yazacak.",
                "Warp fırtınası yaklaşıyor ve sen Kaos'un karanlık güçlerine karşı savaşmaya hazırlanıyorsun. İmperium'un geleceği senin ellerinde ve her kararın galaksiyi değiştireceği bir savaş başlıyor."
            ],
            "investigation": [
                "Hive şehrinin derinliklerinde gizli bir kaos kültü faaliyet gösteriyor. Sen İmperium'un seçilmiş dedektifi olarak bu karanlık komployu çözmek için her şeyi riske atıyorsun.",
                "Şehirde gizli bir ihanet ağı keşfettin. Her ipucu yeni bir tehlike, her karar yeni bir sır açıyor. İmperium'un güvenliği senin ellerinde."
            ]
        },
        "cyberpunk": {
            "corporate": [
                "Neon ışıkların altında, mega şirketlerin gölgesinde, sen kendini tehlikeli bir komplonun merkezinde buldun. Teknoloji ve insanlık arasındaki çatışmada, her kararın yeni bir tehlike, her adımın yeni bir sır açtığı bir dünyada yaşıyorsun.",
                "Cyberpunk şehrinin yeraltı dünyasında, gang savaşlarının ortasında, sen kendini büyük bir komplonun merkezinde buldun. Her karar şehrin kaderini değiştirecek, her savaş yeni bir efsane yazacak."
            ],
            "hacking": [
                "Şehir ağlarının derinliklerinde, dijital dünyanın karanlık sokaklarında, sen kendini tehlikeli bir hack operasyonunun merkezinde buldun. Her kod satırı yeni bir tehlike, her hack yeni bir sır açıyor.",
                "Mega şirketlerin güvenlik sistemlerini aşmaya çalışırken, sen kendini büyük bir dijital komplonun merkezinde buldun. Her hack yeni bir tehlike, her karar yeni bir sır açıyor."
            ]
        }
    }
    
    theme_intros = introductions.get(theme, introductions["fantasy"])
    story_intros = theme_intros.get(story_type, theme_intros.get("adventure", theme_intros["adventure"]))
    
    import random
    return random.choice(story_intros)

def generate_story_nodes(theme, story_type, complexity, length):
    """Generate story nodes with advanced features"""
    nodes = {
        "start": {
            "id": "start",
            "title": "Hikayenin Başlangıcı",
            "description": generate_story_introduction(theme, story_type, complexity),
            "choices": [
                {
                    "text": "⚔️ Hemen harekete geç",
                    "next_node": "action_sequence",
                    "diceRoll": {"type": "d20", "target": 15, "skill": "Initiative"},
                    "effect": {"karma": 5},
                    "hidden_consequence": "immediate_action"
                },
                {
                    "text": "💬 Durumu analiz et",
                    "next_node": "analysis_sequence",
                    "diceRoll": {"type": "d20", "target": 12, "skill": "Investigation"},
                    "effect": {"karma": 3},
                    "hidden_consequence": "careful_analysis"
                },
                {
                    "text": "🎒 Hazırlık yap",
                    "next_node": "preparation_sequence",
                    "diceRoll": {"type": "d20", "target": 10, "skill": "Preparation"},
                    "effect": {"karma": 2},
                    "hidden_consequence": "proper_preparation"
                }
            ]
        }
    }
    
    # Add more nodes based on length and complexity
    if length == "long":
        nodes.update(generate_additional_nodes(theme, story_type, complexity))
    
    return nodes

def generate_additional_nodes(theme, story_type, complexity):
    """Generate additional story nodes"""
    additional_nodes = {
        "action_sequence": {
            "id": "action_sequence",
            "title": "Aksiyon Sırası",
            "description": "Hızlı kararın seni doğrudan aksiyonun merkezine sürükledi. Tehlikeler her yerde ve sen hızlı düşünmek zorundasın.",
            "choices": [
                {
                    "text": "⚔️ Saldırıya geç",
                    "next_node": "combat_sequence",
                    "diceRoll": {"type": "d20", "target": 16, "skill": "Combat"},
                    "effect": {"karma": 6},
                    "hidden_consequence": "aggressive_approach"
                },
                {
                    "text": "🛡️ Savunmaya geç",
                    "next_node": "defense_sequence",
                    "diceRoll": {"type": "d20", "target": 14, "skill": "Defense"},
                    "effect": {"karma": 4},
                    "hidden_consequence": "defensive_approach"
                }
            ]
        }
    }
    
    return additional_nodes

def generate_emotional_arcs(theme, story_type):
    """Generate emotional arcs for the story"""
    arcs = {
        "hero_journey": {
            "stages": ["call_to_adventure", "crossing_threshold", "ordeal", "return"],
            "current_stage": 0,
            "progress": 0.0,
            "impact": "transformative"
        },
        "character_growth": {
            "stages": ["innocence", "experience", "wisdom", "mastery"],
            "current_stage": 0,
            "progress": 0.0,
            "impact": "enlightening"
        }
    }
    
    return arcs

def generate_contextual_events(theme, story_type):
    """Generate contextual events for the story"""
    events = {
        "plot_twist": {
            "active": True,
            "chance": 0.4,
            "triggers": ["unexpected_revelation", "betrayal", "hidden_truth"],
            "impact": "transformative"
        },
        "character_development": {
            "active": True,
            "chance": 0.6,
            "triggers": ["personal_growth", "relationship_change", "skill_improvement"],
            "impact": "enlightening"
        }
    }
    
    return events

# ===== AUTHENTICATION ENDPOINTS =====

@app.route('/api/auth/verify', methods=['POST'])
def verify_auth():
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'success': False, 'error': 'No token provided'})
        
        # For now, accept any token (simple guest system)
        # In a real app, you'd verify the token properly
        return jsonify({
            'success': True,
            'user_id': 'guest_user',
            'username': 'Guest',
            'is_guest': True
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Simple guest login system
        if username == 'guest' or not username:
            token = 'guest_token_' + str(int(time.time()))
            return jsonify({
                'success': True,
                'token': token,
                'user_id': 'guest_user',
                'username': 'Guest',
                'is_guest': True
            })
        
        return jsonify({'success': False, 'error': 'Invalid credentials'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Simple registration (in real app, you'd save to database)
        token = 'user_token_' + str(int(time.time()))
        return jsonify({
            'success': True,
            'token': token,
            'user_id': 'user_' + username,
            'username': username,
            'is_guest': False
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    print(f"🎲 AI Dungeon Master başlatılıyor...")
    print(f"🌐 Port: {port}")
    print("🔗 WebSocket desteği aktif")
    print(f"🔧 Debug mode: {debug_mode}")
    print(f"🔧 Environment: {os.environ.get('FLASK_ENV', 'development')}")
    
    # Simple Flask run for production
    app.run(host='0.0.0.0', port=port, debug=debug_mode) 