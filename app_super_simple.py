#!/usr/bin/env python3
"""
Super Simple Flask App for Render - GUARANTEED TO WORK
"""

from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Dungeon Master</title>
        <style>
            body { 
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                color: white; 
                font-family: Arial, sans-serif; 
                text-align: center; 
                padding: 50px;
            }
            .container { 
                background: rgba(0,0,0,0.3); 
                padding: 30px; 
                border-radius: 10px; 
                border: 2px solid #ffd700;
            }
            h1 { color: #ffd700; }
            .btn { 
                background: #ffd700; 
                color: #000; 
                padding: 15px 30px; 
                border: none; 
                border-radius: 5px; 
                font-size: 18px; 
                cursor: pointer; 
                margin: 10px;
                text-decoration: none;
                display: inline-block;
            }
            .btn:hover { background: #ffed4e; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 AI Dungeon Master</h1>
            <p>Your game is LIVE and working!</p>
            <a href="/game" class="btn">🎲 Start Game</a>
            <a href="/api/health" class="btn">🔍 Health Check</a>
        </div>
    </body>
    </html>
    '''

@app.route('/game')
def game():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Dungeon Master - Game</title>
        <style>
            body { 
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                color: white; 
                font-family: Arial, sans-serif; 
                padding: 20px;
            }
            .game-container { 
                background: rgba(0,0,0,0.3); 
                padding: 30px; 
                border-radius: 10px; 
                border: 2px solid #ffd700;
                max-width: 800px;
                margin: 0 auto;
            }
            h1 { color: #ffd700; text-align: center; }
            .character-section { margin: 20px 0; }
            .btn { 
                background: #ffd700; 
                color: #000; 
                padding: 10px 20px; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer; 
                margin: 5px;
            }
            .btn:hover { background: #ffed4e; }
        </style>
    </head>
    <body>
        <div class="game-container">
            <h1>🎮 AI Dungeon Master - Game Interface</h1>
            
            <div class="character-section">
                <h2>👤 Character Creation</h2>
                <button class="btn" onclick="alert('Warrior selected!')">⚔️ Warrior</button>
                <button class="btn" onclick="alert('Mage selected!')">🔮 Mage</button>
                <button class="btn" onclick="alert('Rogue selected!')">🗡️ Rogue</button>
            </div>
            
            <div class="character-section">
                <h2>🌍 Choose Your World</h2>
                <button class="btn" onclick="alert('Fantasy world selected!')">🏰 Fantasy</button>
                <button class="btn" onclick="alert('Warhammer 40K selected!')">⚡ Warhammer 40K</button>
                <button class="btn" onclick="alert('Cyberpunk selected!')">🌃 Cyberpunk</button>
            </div>
            
            <div class="character-section">
                <h2>🎲 Start Adventure</h2>
                <button class="btn" onclick="alert('Adventure started! Your character embarks on an epic journey...')">🚀 Begin Adventure</button>
            </div>
            
            <p style="text-align: center; margin-top: 30px;">
                <a href="/" style="color: #ffd700;">← Back to Main</a>
            </p>
        </div>
    </body>
    </html>
    '''

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy", 
        "message": "AI Dungeon Master is running successfully!",
        "version": "1.0.0",
        "deployment": "SUCCESS"
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    return jsonify({
        'success': True,
        'token': 'guest_token_123',
        'user_id': 'guest_user',
        'username': 'Guest',
        'is_guest': True,
        'message': 'Login successful!'
    })

@app.route('/api/game/character/classes')
def character_classes():
    classes = [
        {"id": "warrior", "name": "Warrior", "description": "Strong fighter"},
        {"id": "mage", "name": "Mage", "description": "Powerful spellcaster"},
        {"id": "rogue", "name": "Rogue", "description": "Stealthy assassin"}
    ]
    return jsonify({"success": True, "classes": classes})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    print(f"🎮 AI Dungeon Master starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
