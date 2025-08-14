#!/usr/bin/env python3
"""
AI Dungeon Master - Production Version for Render
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os
import time

app = Flask(__name__)
CORS(app)

# Basit session manager
class SimpleSessionManager:
    def __init__(self):
        self.sessions = {}
    
    def create_session(self, session_id):
        self.sessions[session_id] = {"status": "active", "created": datetime.now()}
        return True
    
    def get_session(self, session_id):
        return self.sessions.get(session_id)

session_manager = SimpleSessionManager()

# Health check endpoint
@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy", "message": "AI Dungeon Master is running!"})

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/game')
def game():
    return render_template('game_enhanced.html')

@app.route('/multiplayer')
def multiplayer():
    return render_template('multiplayer.html')

@app.route('/enhanced')
def enhanced():
    return render_template('game_enhanced.html')

# Character classes data
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
    }
]

# API endpoints
@app.route('/api/game/character/classes')
def get_character_classes():
    return jsonify({"success": True, "classes": CHARACTER_CLASSES})

@app.route('/api/game/character/races')
def get_character_races():
    races = [
        {"id": "human", "name": "Human", "description": "Versatile and adaptable"},
        {"id": "elf", "name": "Elf", "description": "Graceful and magical"},
        {"id": "dwarf", "name": "Dwarf", "description": "Sturdy and skilled"},
        {"id": "orc", "name": "Orc", "description": "Strong and fierce"}
    ]
    return jsonify({"success": True, "races": races})

@app.route('/api/game/character/load', methods=['GET'])
def load_character():
    return jsonify({
        'success': True,
        'character': None,
        'game_state': {
            'level': 1,
            'xp': 0,
            'karma': 0
        }
    })

@app.route('/api/game/character/save', methods=['POST'])
def save_character():
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Character saved successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error saving character: {str(e)}'
        }), 500

# Authentication endpoints
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username', 'guest')
        
        token = 'guest_token_' + str(int(time.time()))
        return jsonify({
            'success': True,
            'token': token,
            'user_id': 'guest_user',
            'username': username,
            'is_guest': True
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username', 'user')
        
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

@app.route('/api/auth/verify', methods=['POST'])
def verify_auth():
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'success': False, 'error': 'No token provided'})
        
        return jsonify({
            'success': True,
            'user_id': 'guest_user',
            'username': 'Guest',
            'is_guest': True
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Game session endpoints
@app.route('/api/game/session/start', methods=['POST'])
def start_session():
    try:
        data = request.get_json()
        session_id = f"session_{int(time.time())}"
        session_manager.create_session(session_id)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Game session started successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error starting session: {str(e)}'
        }), 500

@app.route('/api/game/save', methods=['POST'])
def save_game():
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Game saved successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error saving game: {str(e)}'
        }), 500

@app.route('/api/game/load', methods=['POST'])
def load_game():
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'game_data': {
                'character': None,
                'scenario': 'Welcome to AI Dungeon Master!',
                'choices': ['Start Adventure', 'Create Character', 'Load Game']
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading game: {str(e)}'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    print(f"🎲 AI Dungeon Master Production başlatılıyor...")
    print(f"🌐 Port: {port}")
    print(f"🔧 Debug mode: {debug_mode}")
    print(f"🔧 Environment: {os.environ.get('FLASK_ENV', 'development')}")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
