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
    return render_template('index.html')

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=False) 