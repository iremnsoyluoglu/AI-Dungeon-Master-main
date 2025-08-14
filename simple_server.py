#!/usr/bin/env python3
"""
Simple Test Server
==================

Basic Flask server to test if the web interface works
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "AI Dungeon Master Server is running!"})

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "message": "Server is running",
        "version": "1.0.0"
    })

@app.route('/api/test')
def test():
    return jsonify({
        "success": True,
        "message": "Test endpoint working"
    })

if __name__ == '__main__':
    print("🚀 Starting simple test server...")
    print("Access at: http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True) 