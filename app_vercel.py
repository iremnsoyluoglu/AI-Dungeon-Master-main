#!/usr/bin/env python3
"""
Vercel-Optimized Flask App
==========================
A simplified Flask application specifically designed for Vercel deployment
"""

from flask import Flask, render_template, request, jsonify
import os

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
        </style>
    </head>
    <body>
        <div class="container">
            <div class="game-icon">🎮</div>
            <h1 class="game-title">AI DUNGEON MASTER</h1>
            <p class="game-subtitle">Fantastik Dünyalara Açılan Kapı</p>
            <div>
                <a href="/login" class="button">GİRİŞ</a>
                <a href="/game" class="button">OYUNA BAŞLA</a>
                <a href="/api/health" class="button">DURUM KONTROLÜ</a>
            </div>
        </div>
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
    """Enhanced game page with full functionality"""
    return '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Dungeon Master - Enhanced</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                color: white;
                height: 100vh;
                overflow: hidden;
            }

            .dashboard {
                display: grid;
                grid-template-columns: 280px 1fr 320px;
                height: 100vh;
                gap: 2px;
                background: #000;
            }

            .left-panel {
                background: linear-gradient(180deg, #2c1810 0%, #4a1f1f 100%);
                padding: 15px;
                overflow-y: auto;
                border: 1px solid rgba(255, 215, 0, 0.3);
            }

            .left-panel h3 {
                color: #ffd700;
                font-size: 16px;
                margin-bottom: 15px;
                text-align: center;
            }

            .theme-tabs {
                display: flex;
                margin-bottom: 20px;
                background: rgba(0, 0, 0, 0.3);
                border-radius: 8px;
                overflow: hidden;
            }

            .theme-tab {
                flex: 1;
                padding: 10px;
                text-align: center;
                cursor: pointer;
                background: rgba(255, 255, 255, 0.1);
                transition: all 0.3s ease;
                font-size: 12px;
            }

            .theme-tab.active {
                background: #ffd700;
                color: #000;
                font-weight: bold;
            }

            .theme-tab:hover {
                background: rgba(255, 215, 0, 0.3);
            }

            .character-name-section {
                margin-bottom: 20px;
            }

            .character-name-section h4 {
                color: #ffd700;
                margin-bottom: 10px;
                font-size: 14px;
            }

            .name-input-container input {
                width: 100%;
                padding: 8px;
                border: 1px solid #ffd700;
                border-radius: 4px;
                background: rgba(0, 0, 0, 0.3);
                color: white;
                font-size: 12px;
            }

            .theme-content {
                margin-bottom: 20px;
            }

            .race-class-list {
                margin-bottom: 20px;
            }

            .race-class-list h4 {
                color: #ffd700;
                margin-bottom: 10px;
                font-size: 14px;
            }

            .list-items {
                display: flex;
                flex-direction: column;
                gap: 5px;
            }

            .list-item {
                padding: 8px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 12px;
                text-align: center;
            }

            .list-item:hover {
                background: rgba(255, 215, 0, 0.3);
            }

            .list-item.selected {
                background: #ffd700;
                color: #000;
                font-weight: bold;
            }

            .center-panel {
                background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
                padding: 20px;
                overflow-y: auto;
                border: 1px solid rgba(255, 215, 0, 0.3);
            }

            .story-area {
                background: rgba(0, 0, 0, 0.4);
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 20px;
                border: 1px solid rgba(255, 215, 0, 0.3);
                min-height: 300px;
            }

            .story-text {
                line-height: 1.6;
                margin-bottom: 15px;
                font-size: 14px;
            }

            .choice-buttons {
                display: flex;
                flex-direction: column;
                gap: 10px;
                margin-top: 20px;
            }

            .choice-btn {
                padding: 12px;
                background: linear-gradient(45deg, #ffd700, #ffa500);
                color: #000;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s ease;
            }

            .choice-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
            }

            .right-panel {
                background: linear-gradient(180deg, #4a148c 0%, #6a1b9a 100%);
                padding: 15px;
                overflow-y: auto;
                border: 1px solid rgba(255, 215, 0, 0.3);
            }

            .right-panel h3 {
                color: #ffd700;
                font-size: 16px;
                margin-bottom: 15px;
                text-align: center;
            }

            .character-info {
                background: rgba(0, 0, 0, 0.3);
                padding: 12px;
                border-radius: 8px;
                margin-bottom: 15px;
                border: 1px solid rgba(255, 215, 0, 0.3);
                text-align: center;
            }

            .character-name {
                color: #ffd700;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 5px;
            }

            .character-details {
                color: rgba(255, 255, 255, 0.8);
                font-size: 12px;
            }

            .stats-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 8px;
                margin-bottom: 15px;
            }

            .stat-item {
                background: rgba(0, 0, 0, 0.3);
                padding: 8px;
                border-radius: 4px;
                text-align: center;
                border: 1px solid rgba(255, 215, 0, 0.3);
            }

            .stat-label {
                color: #ffd700;
                font-size: 11px;
                margin-bottom: 2px;
            }

            .stat-value {
                color: white;
                font-size: 14px;
                font-weight: bold;
            }

            .action-buttons {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }

            .action-btn {
                padding: 8px;
                background: linear-gradient(45deg, #ffd700, #ffa500);
                color: #000;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-weight: bold;
                font-size: 12px;
                transition: all 0.3s ease;
            }

            .action-btn:hover {
                transform: translateY(-1px);
                box-shadow: 0 2px 8px rgba(255, 215, 0, 0.4);
            }

            .action-btn.secondary {
                background: linear-gradient(45deg, #4CAF50, #45a049);
                color: white;
            }

            .action-btn.danger {
                background: linear-gradient(45deg, #f44336, #d32f2f);
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="dashboard">
            <!-- Sol Panel -->
            <div class="left-panel">
                <h3>🎮 Temalar & Karakterler</h3>
                <div class="theme-tabs">
                    <div class="theme-tab active" onclick="switchTheme('fantasy')">Fantasy</div>
                    <div class="theme-tab" onclick="switchTheme('warhammer')">Warhammer 40K</div>
                    <div class="theme-tab" onclick="switchTheme('cyberpunk')">Cyberpunk</div>
                </div>

                <div class="character-name-section">
                    <h4>👤 Karakter Adı</h4>
                    <div class="name-input-container">
                        <input type="text" id="character-name-input" placeholder="Karakter adınızı girin..." maxlength="20" oninput="updateCharacterName(this.value)">
                    </div>
                </div>

                <div id="fantasy-content" class="theme-content">
                    <div class="race-class-list">
                        <h4>🏹 Irklar</h4>
                        <div class="list-items">
                            <div class="list-item" onclick="selectRace(this, 'elf')">Elf</div>
                            <div class="list-item" onclick="selectRace(this, 'human')">İnsan</div>
                            <div class="list-item" onclick="selectRace(this, 'dwarf')">Cüce</div>
                            <div class="list-item" onclick="selectRace(this, 'orc')">Ork</div>
                        </div>
                    </div>
                    <div class="race-class-list">
                        <h4>🗡️ Sınıflar</h4>
                        <div class="list-items">
                            <div class="list-item" onclick="selectClass(this, 'warrior')">Savaşçı</div>
                            <div class="list-item" onclick="selectClass(this, 'mage')">Büyücü</div>
                            <div class="list-item" onclick="selectClass(this, 'rogue')">Hırsız</div>
                            <div class="list-item" onclick="selectClass(this, 'cleric')">Rahip</div>
                        </div>
                    </div>
                </div>

                <div id="warhammer-content" class="theme-content" style="display: none">
                    <div class="race-class-list">
                        <h4>👥 Irklar</h4>
                        <div class="list-items">
                            <div class="list-item" onclick="selectRace(this, 'imperial')">İmparatorluk</div>
                            <div class="list-item" onclick="selectRace(this, 'spacemarine')">Space Marine</div>
                            <div class="list-item" onclick="selectRace(this, 'ork')">Ork</div>
                            <div class="list-item" onclick="selectRace(this, 'eldar')">Eldar</div>
                        </div>
                    </div>
                    <div class="race-class-list">
                        <h4>⚔️ Sınıflar</h4>
                        <div class="list-items">
                            <div class="list-item" onclick="selectClass(this, 'spacemarine')">Space Marine</div>
                            <div class="list-item" onclick="selectClass(this, 'imperialguard')">Imperial Guard</div>
                            <div class="list-item" onclick="selectClass(this, 'psyker')">Psyker</div>
                            <div class="list-item" onclick="selectClass(this, 'orknob')">Ork Nob</div>
                        </div>
                    </div>
                </div>

                <div id="cyberpunk-content" class="theme-content" style="display: none">
                    <div class="race-class-list">
                        <h4>🤖 Karakterler</h4>
                        <div class="list-items">
                            <div class="list-item" onclick="selectRace(this, 'human')">İnsan</div>
                            <div class="list-item" onclick="selectRace(this, 'cyborg')">Cyborg</div>
                            <div class="list-item" onclick="selectRace(this, 'ai')">AI</div>
                        </div>
                    </div>
                    <div class="race-class-list">
                        <h4>💻 Sınıflar</h4>
                        <div class="list-items">
                            <div class="list-item" onclick="selectClass(this, 'netrunner')">Netrunner</div>
                            <div class="list-item" onclick="selectClass(this, 'solo')">Solo</div>
                            <div class="list-item" onclick="selectClass(this, 'techie')">Techie</div>
                            <div class="list-item" onclick="selectClass(this, 'fixer')">Fixer</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Orta Panel -->
            <div class="center-panel">
                <div class="story-area">
                    <div class="story-text">
                        <h2>🎮 AI Dungeon Master'a Hoş Geldiniz!</h2>
                        <p>Fantastik dünyalarda maceraya atılmaya hazır mısınız? Sol panelden karakterinizi oluşturun ve hikayenizi başlatın.</p>
                        <br>
                        <p><strong>Nasıl Oynanır:</strong></p>
                        <ul>
                            <li>Sol panelden bir tema seçin (Fantasy, Warhammer 40K, Cyberpunk)</li>
                            <li>Karakter adınızı girin</li>
                            <li>Irk ve sınıf seçin</li>
                            <li>Sağ panelden oyunu başlatın</li>
                        </ul>
                    </div>
                    <div class="choice-buttons">
                        <button class="choice-btn" onclick="startGame()">OYUNA BAŞLA</button>
                        <button class="choice-btn" onclick="generateStory()">HİKAYE ÜRET</button>
                        <button class="choice-btn" onclick="showCharacter()">KARAKTER GÖSTER</button>
                    </div>
                </div>
            </div>

            <!-- Sağ Panel -->
            <div class="right-panel">
                <h3>👤 Karakter Bilgileri</h3>
                <div class="character-info">
                    <div class="character-name" id="char-name">Karakter Adı</div>
                    <div class="character-details" id="char-details">Tema: Fantasy | Irk: - | Sınıf: -</div>
                </div>

                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-label">HP</div>
                        <div class="stat-value" id="stat-hp">100</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Saldırı</div>
                        <div class="stat-value" id="stat-attack">15</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Savunma</div>
                        <div class="stat-value" id="stat-defense">10</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Güç</div>
                        <div class="stat-value" id="stat-strength">12</div>
                    </div>
                </div>

                <div class="action-buttons">
                    <button class="action-btn" onclick="saveGame()">💾 KAYDET</button>
                    <button class="action-btn secondary" onclick="loadGame()">📂 YÜKLE</button>
                    <button class="action-btn" onclick="inventory()">🎒 ENVANTER</button>
                    <button class="action-btn" onclick="skills()">⚡ YETENEKLER</button>
                    <button class="action-btn" onclick="combat()">⚔️ SAVAŞ</button>
                    <button class="action-btn danger" onclick="resetGame()">🔄 SIFIRLA</button>
                </div>
            </div>
        </div>

        <script>
            let currentTheme = 'fantasy';
            let selectedRace = '';
            let selectedClass = '';
            let characterName = '';

            function switchTheme(theme) {
                currentTheme = theme;
                
                // Tema tablarını güncelle
                document.querySelectorAll('.theme-tab').forEach(tab => {
                    tab.classList.remove('active');
                });
                event.target.classList.add('active');
                
                // İçerikleri gizle/göster
                document.querySelectorAll('.theme-content').forEach(content => {
                    content.style.display = 'none';
                });
                document.getElementById(theme + '-content').style.display = 'block';
                
                // Seçimleri sıfırla
                selectedRace = '';
                selectedClass = '';
                updateCharacterDisplay();
            }

            function selectRace(element, race) {
                selectedRace = race;
                document.querySelectorAll('.list-item').forEach(item => {
                    item.classList.remove('selected');
                });
                element.classList.add('selected');
                updateCharacterDisplay();
            }

            function selectClass(element, classType) {
                selectedClass = classType;
                document.querySelectorAll('.list-item').forEach(item => {
                    item.classList.remove('selected');
                });
                element.classList.add('selected');
                updateCharacterDisplay();
            }

            function updateCharacterName(name) {
                characterName = name;
                document.getElementById('char-name').textContent = name || 'Karakter Adı';
                updateCharacterDisplay();
            }

            function updateCharacterDisplay() {
                const details = `Tema: ${currentTheme.charAt(0).toUpperCase() + currentTheme.slice(1)} | Irk: ${selectedRace || '-'} | Sınıf: ${selectedClass || '-'}`;
                document.getElementById('char-details').textContent = details;
            }

            function startGame() {
                if (!characterName || !selectedRace || !selectedClass) {
                    alert('Lütfen karakter adı, ırk ve sınıf seçin!');
                    return;
                }
                alert('Oyun başlatılıyor... ' + characterName + ' olarak ' + selectedRace + ' ' + selectedClass + ' karakteri ile!');
            }

            function generateStory() {
                alert('AI destekli hikaye üretiliyor...');
            }

            function showCharacter() {
                alert('Karakter bilgileri gösteriliyor...');
            }

            function saveGame() {
                alert('Oyun kaydediliyor...');
            }

            function loadGame() {
                alert('Oyun yükleniyor...');
            }

            function inventory() {
                alert('Envanter açılıyor...');
            }

            function skills() {
                alert('Yetenekler açılıyor...');
            }

            function combat() {
                alert('Savaş modu başlatılıyor...');
            }

            function resetGame() {
                if (confirm('Oyunu sıfırlamak istediğinizden emin misiniz?')) {
                    characterName = '';
                    selectedRace = '';
                    selectedClass = '';
                    document.getElementById('character-name-input').value = '';
                    document.querySelectorAll('.list-item').forEach(item => {
                        item.classList.remove('selected');
                    });
                    updateCharacterDisplay();
                    alert('Oyun sıfırlandı!');
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
