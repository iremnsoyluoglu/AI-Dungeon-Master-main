#!/usr/bin/env python3
"""
Vercel-Optimized Flask App
==========================
A simplified Flask application specifically designed for Vercel deployment
"""

from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    """Main landing page"""
    return '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Dungeon Master</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #2a2a2a 100%);
                color: white;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .container {
                text-align: center;
                background: rgba(26, 26, 26, 0.8);
                padding: 40px;
                border-radius: 12px;
                border: 2px solid #FFD700;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }
            .game-icon {
                font-size: 60px;
                margin-bottom: 20px;
                color: #FFD700;
            }
            .game-title {
                font-size: 32px;
                font-weight: bold;
                color: #FFD700;
                margin-bottom: 8px;
                text-transform: uppercase;
                letter-spacing: 2px;
            }
            .game-subtitle {
                color: rgba(255, 255, 255, 0.8);
                margin-bottom: 30px;
            }
            .button {
                background: linear-gradient(45deg, #FFD700, #FFA500);
                color: #000;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                margin: 5px;
                text-decoration: none;
                display: inline-block;
                transition: all 0.3s ease;
            }
            .button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
            }
            .button-container {
                display: flex;
                flex-direction: column;
                gap: 10px;
                align-items: center;
            }
            .button-row {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                justify-content: center;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="game-icon">🎮</div>
            <h1 class="game-title">AI DUNGEON MASTER</h1>
            <p class="game-subtitle">Fantastik Dünyalara Açılan Kapı</p>
            <div class="button-container">
                <div class="button-row">
                    <button class="button" onclick="navigateTo('/login')">GİRİŞ</button>
                    <button class="button" onclick="navigateTo('/register')">KAYIT</button>
                </div>
                <div class="button-row">
                    <button class="button" onclick="navigateTo('/enhanced')">MİSAFİR</button>
                    <button class="button" onclick="navigateTo('/multiplayer')">MULTIPLAYER</button>
                </div>
                <div class="button-row">
                    <button class="button" onclick="navigateTo('/api/health')">DURUM KONTROLÜ</button>
                </div>
            </div>
        </div>
        
        <script>
            function navigateTo(path) {
                try {
                    window.location.href = path;
                } catch (error) {
                    console.error('Navigation error:', error);
                    alert('Sayfa yüklenirken bir hata oluştu. Lütfen tekrar deneyin.');
                }
            }
        </script>
    </body>
    </html>
    '''

@app.route('/login')
def login():
    """Login page"""
    return '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Giriş - AI Dungeon Master</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #2a2a2a 100%);
                color: white;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .login-container {
                background: rgba(26, 26, 26, 0.8);
                padding: 40px;
                border-radius: 12px;
                border: 2px solid #FFD700;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                width: 400px;
            }
            .game-icon {
                font-size: 60px;
                text-align: center;
                color: #FFD700;
                margin-bottom: 20px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                color: #FFD700;
            }
            input {
                width: 100%;
                padding: 10px;
                border: 1px solid #FFD700;
                border-radius: 4px;
                background: rgba(255, 255, 255, 0.1);
                color: white;
                box-sizing: border-box;
            }
            .button {
                background: linear-gradient(45deg, #FFD700, #FFA500);
                color: #000;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                width: 100%;
                margin-top: 10px;
            }
            .button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="game-icon">🎮</div>
            <h2 style="text-align: center; color: #FFD700; margin-bottom: 30px;">GİRİŞ YAP</h2>
            <form onsubmit="handleLogin(event)">
                <div class="form-group">
                    <label>Kullanıcı Adı</label>
                    <input type="text" id="username" placeholder="Kullanıcı adınızı girin" required>
                </div>
                <div class="form-group">
                    <label>Şifre</label>
                    <input type="password" id="password" placeholder="Şifrenizi girin" required>
                </div>
                <button type="submit" class="button">GİRİŞ YAP</button>
            </form>
            <p style="text-align: center; margin-top: 20px;">
                <a href="/game" style="color: #FFD700;">Misafir olarak oyuna başla</a>
            </p>
            <script>
                function handleLogin(event) {
                    event.preventDefault();
                    const username = document.getElementById('username').value;
                    const password = document.getElementById('password').value;
                    
                    if (username && password) {
                        // Başarılı giriş - oyuna yönlendir
                        window.location.href = '/enhanced';
                    } else {
                        alert('Lütfen kullanıcı adı ve şifre girin!');
                    }
                }
            </script>
        </div>
    </body>
    </html>
    '''

@app.route('/game')
def game():
    """Game page"""
    return '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Oyun - AI Dungeon Master</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #2a2a2a 100%);
                color: white;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }
            .game-container {
                max-width: 1200px;
                margin: 0 auto;
                background: rgba(26, 26, 26, 0.8);
                padding: 20px;
                border-radius: 12px;
                border: 2px solid #FFD700;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }
            .game-header {
                text-align: center;
                margin-bottom: 30px;
            }
            .game-icon {
                font-size: 60px;
                color: #FFD700;
                margin-bottom: 10px;
            }
            .game-title {
                font-size: 32px;
                font-weight: bold;
                color: #FFD700;
                margin-bottom: 10px;
            }
            .game-area {
                background: rgba(0, 0, 0, 0.3);
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 20px;
                min-height: 300px;
            }
            .button {
                background: linear-gradient(45deg, #FFD700, #FFA500);
                color: #000;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                cursor: pointer;
                margin: 5px;
            }
            .button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
            }
        </style>
    </head>
    <body>
        <div class="game-container">
            <div class="game-header">
                <div class="game-icon">🎮</div>
                <h1 class="game-title">AI DUNGEON MASTER</h1>
                <p>Oyun başlatılıyor...</p>
            </div>
            <div class="game-area">
                <h3>Hoş geldiniz, maceracı!</h3>
                <p>AI Dungeon Master oyununa hoş geldiniz. Burada fantastik dünyalarda maceraya atılabilir, karakterlerinizi geliştirebilir ve eşsiz hikayeler yaşayabilirsiniz.</p>
                <br>
                <p><strong>Özellikler:</strong></p>
                <ul>
                    <li>AI destekli hikaye üretimi</li>
                    <li>Karakter sistemi</li>
                    <li>Çoklu tema desteği</li>
                    <li>Etkileşimli oyun deneyimi</li>
                </ul>
            </div>
            <div style="text-align: center;">
                <a href="/enhanced" class="button">TAM OYUNA GEÇ</a>
                <button class="button" onclick="alert('Karakter oluşturuluyor...')">KARAKTER OLUŞTUR</button>
                <button class="button" onclick="alert('Ayarlar açılıyor...')">AYARLAR</button>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/enhanced')
def enhanced():
    """Enhanced game page with full RPG functionality, plot twists, NPC interactions, and multiple endings"""
    return render_template('game.html')

@app.route('/multiplayer')
def multiplayer():
    """Multiplayer page"""
    return '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Multiplayer - AI Dungeon Master</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #2a2a2a 100%);
                color: white;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .multiplayer-container {
                background: rgba(26, 26, 26, 0.8);
                padding: 40px;
                border-radius: 12px;
                border: 2px solid #FFD700;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                width: 500px;
                text-align: center;
            }
            .game-icon {
                font-size: 60px;
                color: #FFD700;
                margin-bottom: 20px;
            }
            .button {
                background: linear-gradient(45deg, #FFD700, #FFA500);
                color: #000;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                margin: 10px;
                text-decoration: none;
                display: inline-block;
                transition: all 0.3s ease;
            }
            .button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
            }
            .room-list {
                background: rgba(0, 0, 0, 0.3);
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                text-align: left;
            }
            .room-item {
                padding: 10px;
                border: 1px solid rgba(255, 215, 0, 0.3);
                border-radius: 4px;
                margin-bottom: 10px;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .room-item:hover {
                background: rgba(255, 215, 0, 0.1);
            }
        </style>
    </head>
    <body>
        <div class="multiplayer-container">
            <div class="game-icon">🎮</div>
            <h2 style="color: #FFD700; margin-bottom: 20px;">MULTIPLAYER OYUN</h2>
            <p>Arkadaşlarınızla birlikte oynayın!</p>
            
            <div class="room-list">
                <h3 style="color: #FFD700; margin-bottom: 15px;">Aktif Odalar</h3>
                <div class="room-item" onclick="joinRoom('Fantasy Adventure')">
                    <strong>Fantasy Adventure</strong> - 2/4 Oyuncu
                </div>
                <div class="room-item" onclick="joinRoom('Warhammer Battle')">
                    <strong>Warhammer Battle</strong> - 1/4 Oyuncu
                </div>
                <div class="room-item" onclick="joinRoom('Cyberpunk Heist')">
                    <strong>Cyberpunk Heist</strong> - 3/4 Oyuncu
                </div>
            </div>
            
            <div style="margin-top: 20px;">
                <button class="button" onclick="createRoom()">ODA OLUŞTUR</button>
                <button class="button" onclick="window.location.href='/'">GERİ DÖN</button>
            </div>
        </div>
        
        <script>
            function joinRoom(roomName) {
                alert(`${roomName} odasına katılıyorsunuz...`);
                // Burada WebSocket bağlantısı kurulacak
            }
            
            function createRoom() {
                const roomName = prompt('Oda adını girin:');
                if (roomName) {
                    alert(`${roomName} odası oluşturuldu!`);
                }
            }
        </script>
    </body>
    </html>
    '''

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "AI Dungeon Master is running successfully on Vercel!",
        "version": "1.0.0",
        "deployment": "vercel"
    })

@app.route('/api/scenarios/enhanced/<scenario_id>')
def get_enhanced_scenario(scenario_id):
    """Get enhanced scenario data"""
    try:
        # Load enhanced scenarios from data file
        with open('data/enhanced_scenarios.json', 'r', encoding='utf-8') as f:
            scenarios_data = json.load(f)
        
        if 'enhanced_scenarios' in scenarios_data and scenario_id in scenarios_data['enhanced_scenarios']:
            scenario = scenarios_data['enhanced_scenarios'][scenario_id]
            return jsonify({
                "success": True,
                "scenario": scenario
            })
        else:
            return jsonify({
                "success": False,
                "error": "Scenario not found"
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/scenarios/enhanced/<scenario_id>/ending')
def get_scenario_endings(scenario_id):
    """Get possible endings for a scenario"""
    try:
        # Load enhanced scenarios from data file
        with open('data/enhanced_scenarios.json', 'r', encoding='utf-8') as f:
            scenarios_data = json.load(f)
        
        if 'enhanced_scenarios' in scenarios_data and scenario_id in scenarios_data['enhanced_scenarios']:
            scenario = scenarios_data['enhanced_scenarios'][scenario_id]
            endings = scenario.get('ending_variations', {})
            
            possible_endings = []
            for ending_id, ending_data in endings.items():
                possible_endings.append({
                    "id": ending_id,
                    "name": ending_id.replace('_', ' ').title(),
                    "description": ending_data.get('description', ''),
                    "requirements": ending_data.get('requirements', {})
                })
            
            return jsonify({
                "success": True,
                "possible_endings": possible_endings
            })
        else:
            return jsonify({
                "success": False,
                "error": "Scenario not found"
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/game')
def game_api():
    """Game API endpoint"""
    return jsonify({
        "title": "AI Dungeon Master",
        "status": "Deployed Successfully on Vercel!",
        "features": [
            "AI-Powered Story Generation",
            "Character System",
            "Multiple Themes",
            "Interactive Gameplay"
        ]
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found", "path": request.path}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=False)
