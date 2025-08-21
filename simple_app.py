#!/usr/bin/env python3
"""
Simple Flask App for Testing
============================
A basic Flask application to test backend functionality
"""

from flask import Flask, render_template, request, jsonify
import os
import sys

app = Flask(__name__)

# Add debugging information
@app.before_request
def log_request_info():
    app.logger.info('Headers: %s', dict(request.headers))
    app.logger.info('Body: %s', request.get_data())

@app.route('/')
def index():
    try:
        return render_template('login.html')
    except Exception as e:
        app.logger.error(f"Error rendering login.html: {e}")
        return f"Error: {str(e)}", 500

@app.route('/login')
def login_page():
    try:
        return render_template('login.html')
    except Exception as e:
        app.logger.error(f"Error rendering login.html: {e}")
        return f"Error: {str(e)}", 500

@app.route('/game')
def game_page():
    try:
        return render_template('game_enhanced.html')
    except Exception as e:
        app.logger.error(f"Error rendering game_enhanced.html: {e}")
        return f"Error: {str(e)}", 500

@app.route('/api/health')
def health():
    try:
        import flask
        flask_version = flask.__version__
    except:
        flask_version = "Unknown"
    
    return jsonify({
        "status": "healthy", 
        "message": "AI Dungeon Master is running!",
        "python_version": sys.version,
        "flask_version": flask_version
    })

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

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found", "path": request.path}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=False) 