#!/usr/bin/env python3
"""
Minimal Flask App for Render Deployment
"""

from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/game')
def game():
    return render_template('game_enhanced.html')

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "message": "AI Dungeon Master is running!"})

@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    return jsonify({
        'success': True,
        'token': 'guest_token_123',
        'user_id': 'guest_user',
        'username': 'Guest',
        'is_guest': True
    })

@app.route('/api/game/character/classes')
def character_classes():
    classes = [
        {"id": "warrior", "name": "Warrior", "description": "Strong fighter"},
        {"id": "mage", "name": "Mage", "description": "Powerful spellcaster"}
    ]
    return jsonify({"success": True, "classes": classes})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=False)
