#!/usr/bin/env python3
"""
Simple Flask App for Testing
============================
A basic Flask application to test backend functionality
"""

from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/game')
def game_page():
    return render_template('game_enhanced.html')

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "message": "AI Dungeon Master is running!"})

@app.route('/api/game')
def game():
    return jsonify({
        "title": "AI Dungeon Master",
        "status": "Deployed Successfully!",
        "features": [
            "AI-Powered Story Generation",
            "Character System",
            "Multiple Themes",
            "Interactive Gameplay"
        ]
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    return jsonify({
        'success': True,
        'token': 'guest_token_123',
        'user_id': 'guest_user',
        'username': 'Guest',
        'is_guest': True
    })

@app.route('/api/game/character/classes')
def get_character_classes():
    classes = [
        {"id": "warrior", "name": "Warrior", "description": "Strong fighter"},
        {"id": "mage", "name": "Mage", "description": "Powerful spellcaster"}
    ]
    return jsonify({"success": True, "classes": classes})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=False) 