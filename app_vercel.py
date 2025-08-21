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
                    <div class="stat-item">
                        <div class="stat-label">Çeviklik</div>
                        <div class="stat-value" id="stat-dexterity">12</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Zeka</div>
                        <div class="stat-value" id="stat-intelligence">14</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Dayanıklılık</div>
                        <div class="stat-value" id="stat-constitution">16</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Bilgelik</div>
                        <div class="stat-value" id="stat-wisdom">13</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Karizma</div>
                        <div class="stat-value" id="stat-charisma">11</div>
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
            // Game State Variables
            let currentTheme = 'fantasy';
            let selectedRace = '';
            let selectedClass = '';
            let characterName = '';
            let playerLevel = 1;
            let playerXP = 0;
            let currentQuest = null;
            let questsCompleted = [];
            let currentScenario = null;
            let storyProgress = 0;
            let plotTwistsUnlocked = [];
            let gameState = 'character_creation';
            
            // NPC Relationship System
            let npcRelationships = {
                aldric: { trust: 0, quests: 0, status: 'neutral', betrayalRevealed: false },
                lydia: { trust: 0, quests: 0, status: 'neutral', dragonIdentityRevealed: false },
                marcus: { trust: 0, quests: 0, status: 'neutral' },
                zara: { trust: 0, quests: 0, status: 'neutral' },
                rexSteel: { trust: 0, quests: 0, status: 'enemy' }
            };

            // Combat System Variables
            let inCombat = false;
            let combatRound = 0;
            let enemyHP = 100;
            let playerHP = 100;

            // Scenario Data
            let scenarios = {
                dragon_hunter: {
                    title: "🐉 Ejderha Avcısının Yolu",
                    theme: "fantasy",
                    description: "Kızıl ejderha köyleri yakıyor. Sen ejderha avcısısın. Bu tehlikeli görevde ejderhayı durdurmak için her şeyi riske atacaksın.",
                    plotTwists: ['aldric_betrayal', 'lydia_dragon_identity', 'mother_dragon_twist'],
                    endings: ['good_ending', 'betrayal_ending', 'dragon_alliance', 'sacrifice_ending', 'dark_lord_ending']
                },
                neon_city: {
                    title: "🌃 Neon Şehir Koşucuları", 
                    theme: "cyberpunk",
                    description: "MegaCorp şehri kontrol ediyor. Gizli AI'ların insanlığı ele geçirdiğini keşfediyorsun. Dijital devrim başlıyor!",
                    plotTwists: ['ai_ceo_shock', 'digital_consciousness', 'corporate_conspiracy'],
                    endings: ['revolution_ending', 'corporate_ending', 'ai_merge_ending', 'underground_king', 'lone_wolf']
                }
            };

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
                // Sadece aynı tema içindeki seçimleri temizle
                const parentContent = element.closest('.theme-content');
                parentContent.querySelectorAll('.list-item').forEach(item => {
                    item.classList.remove('selected');
                });
                element.classList.add('selected');
                updateCharacterDisplay();
            }

            function selectClass(element, classType) {
                selectedClass = classType;
                // Sadece aynı tema içindeki seçimleri temizle
                const parentContent = element.closest('.theme-content');
                parentContent.querySelectorAll('.list-item').forEach(item => {
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
                
                // Oyun durumunu güncelle
                gameState = 'playing';
                updateCharacterStats();
                
                // Senaryoyu belirle
                if (currentTheme === 'fantasy') {
                    currentScenario = 'dragon_hunter';
                    startDragonHunterScenario();
                } else if (currentTheme === 'cyberpunk') {
                    currentScenario = 'neon_city';
                    startNeonCityScenario();
                } else {
                    startGenericScenario();
                }
            }

            function startDragonHunterScenario() {
                storyProgress = 1;
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h2>🐉 Ejderha Avcısının Yolu Başlıyor!</h2>
                    <p><strong>Karakter:</strong> ${characterName} - ${selectedRace} ${selectedClass}</p>
                    <p><strong>Level:</strong> ${playerLevel} | <strong>XP:</strong> ${playerXP}</p>
                    <hr>
                    <h3>📖 Hikaye:</h3>
                    <p>Kızıl ejderha Pyraxis köyleri yakıyor. Köy büyükleri seni ejderha avcısı olarak seçti. 
                    Aldric adındaki deneyimli savaşçı senin rehberin olacak. Lydia ise köyün şifacısı - yolculukta sana yardım edecek.</p>
                    <br>
                    <p><strong>Aldric</strong> yaklaşıyor: "Genç avcı, ejderha çok güçlü. Önce kendini geliştirmen gerek!"</p>
                    <p><strong>Güven Sistemi:</strong> Aldric ile olan ilişkin hikayeyi etkileyecek.</p>
                `;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="interactWithNPC('aldric', 'agree')">✅ "Haklısın Aldric, eğitim almaya hazırım!"</button>
                    <button class="choice-btn" onclick="interactWithNPC('aldric', 'stubborn')">⚔️ "Doğrudan ejderhaya saldıralım!"</button>
                    <button class="choice-btn" onclick="exploreVillage()">🏘️ "Önce köyü keşfetmek istiyorum"</button>
                `;
            }

            function startNeonCityScenario() {
                storyProgress = 1;
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h2>🌃 Neon Şehir Koşucuları Başlıyor!</h2>
                    <p><strong>Karakter:</strong> ${characterName} - ${selectedRace} ${selectedClass}</p>
                    <p><strong>Level:</strong> ${playerLevel} | <strong>XP:</strong> ${playerXP}</p>
                    <hr>
                    <h3>📖 Hikaye:</h3>
                    <p>2087 yılı, Neo Tokyo. MegaCorp şehri kontrol ediyor. Sen bir hacker olarak şehrin karanlık sırlarını keşfediyorsun. 
                    Zara adında devrimci bir hacker senin yanında. Rex Steel ise MegaCorp'un güvenlik şefi - düşmanın.</p>
                    <br>
                    <p><strong>Zara</strong> ekranda beliriyor: "Taze kan! MegaCorp'un gizli AI projesi var. Araştırmaya hazır mısın?"</p>
                    <p><strong>Güven Sistemi:</strong> Zara ile olan ilişkin devrimin sonucunu belirleyecek.</p>
                `;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="interactWithNPC('zara', 'agree')">💻 "Elbette! AI projesini araştıralım"</button>
                    <button class="choice-btn" onclick="interactWithNPC('zara', 'cautious')">🔍 "Önce daha fazla bilgi toplamamız gerek"</button>
                    <button class="choice-btn" onclick="soloMission()">🚶 "Tek başıma çalışmayı tercih ederim"</button>
                `;
            }

            function startGenericScenario() {
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h2>🎮 ${characterName} olarak maceraya başlıyorsunuz!</h2>
                    <p><strong>Karakteriniz:</strong> ${selectedRace} ${selectedClass}</p>
                    <p><strong>Tema:</strong> ${currentTheme.charAt(0).toUpperCase() + currentTheme.slice(1)}</p>
                    <br>
                    <p>Karanlık bir ormanda yürüyorsunuz. Önünüzde iki yol var:</p>
                    <ul>
                        <li>Sol yol: Eski bir kaleye gidiyor</li>
                        <li>Sağ yol: Gizemli bir mağaraya açılıyor</li>
                    </ul>
                `;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="choosePath('castle')">🏰 KALEYE GİT</button>
                    <button class="choice-btn" onclick="choosePath('cave')">🕳️ MAĞARAYA GİR</button>
                    <button class="choice-btn" onclick="exploreArea()">🔍 ETRAFI KEŞFET</button>
                `;
            }

            function generateStory() {
                const stories = [
                    "Gizemli bir ses size yaklaşıyor...",
                    "Uzakta bir ışık görüyorsunuz...",
                    "Rüzgar yaprakları savuruyor...",
                    "Bir kuş ötüyor ve dikkatinizi çekiyor...",
                    "Yerde eski bir harita buldunuz..."
                ];
                
                const randomStory = stories[Math.floor(Math.random() * stories.length)];
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h2>📖 Hikaye Üretildi</h2>
                    <p>${randomStory}</p>
                    <br>
                    <p>Ne yapmak istiyorsunuz?</p>
                `;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="investigate()">🔍 ARAŞTIR</button>
                    <button class="choice-btn" onclick="moveForward()">➡️ İLERLE</button>
                    <button class="choice-btn" onclick="rest()">😴 DİNLEN</button>
                `;
            }

            function showCharacter() {
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h2>👤 Karakter Bilgileri</h2>
                    <p><strong>İsim:</strong> ${characterName || 'Belirtilmemiş'}</p>
                    <p><strong>Irk:</strong> ${selectedRace || 'Seçilmemiş'}</p>
                    <p><strong>Sınıf:</strong> ${selectedClass || 'Seçilmemiş'}</p>
                    <p><strong>Tema:</strong> ${currentTheme.charAt(0).toUpperCase() + currentTheme.slice(1)}</p>
                    <br>
                    <h3>İstatistikler:</h3>
                    <p>HP: ${document.getElementById('stat-hp').textContent}</p>
                    <p>Saldırı: ${document.getElementById('stat-attack').textContent}</p>
                    <p>Savunma: ${document.getElementById('stat-defense').textContent}</p>
                    <p>Güç: ${document.getElementById('stat-strength').textContent}</p>
                `;
            }

            function updateCharacterStats() {
                // Temel özellikler (ırk ve sınıfa göre dinamik)
                let strength = 12, dexterity = 12, intelligence = 14, constitution = 16, wisdom = 13, charisma = 11;
                let hp = 100, attack = 15, defense = 10;
                
                // IRK BONUSLARI
                if (selectedRace === 'human') {
                    strength += 1; dexterity += 1; intelligence += 1; constitution += 1; wisdom += 1; charisma += 1;
                } else if (selectedRace === 'elf') {
                    dexterity += 3; intelligence += 2; wisdom += 1; constitution -= 1;
                } else if (selectedRace === 'dwarf') {
                    strength += 2; constitution += 3; wisdom += 1; charisma -= 1;
                } else if (selectedRace === 'orc') {
                    strength += 3; constitution += 2; intelligence -= 1; charisma -= 1;
                } else if (selectedRace === 'halfling') {
                    dexterity += 3; charisma += 2; strength -= 1;
                } else if (selectedRace === 'tiefling') {
                    intelligence += 2; charisma += 2; constitution -= 1;
                }
                
                // SINIF BONUSLARI
                if (currentTheme === 'fantasy') {
                    if (selectedClass === 'warrior') {
                        strength += 3; constitution += 2; hp = 120; attack = 18; defense = 12;
                    } else if (selectedClass === 'mage') {
                        intelligence += 3; wisdom += 2; hp = 80; attack = 20; defense = 8;
                    } else if (selectedClass === 'rogue') {
                        dexterity += 3; intelligence += 1; hp = 90; attack = 16; defense = 11;
                    } else if (selectedClass === 'cleric') {
                        wisdom += 3; constitution += 1; hp = 100; attack = 14; defense = 13;
                    }
                } else if (currentTheme === 'warhammer') {
                    if (selectedClass === 'spacemarine') {
                        strength += 4; constitution += 3; hp = 150; attack = 25; defense = 20;
                    } else if (selectedClass === 'imperialguard') {
                        strength += 1; constitution += 1; hp = 80; attack = 15; defense = 12;
                    } else if (selectedClass === 'psyker') {
                        intelligence += 4; wisdom += 2; hp = 70; attack = 30; defense = 8;
                    } else if (selectedClass === 'orknob') {
                        strength += 3; constitution += 2; hp = 120; attack = 22; defense = 15;
                    }
                } else if (currentTheme === 'cyberpunk') {
                    if (selectedClass === 'netrunner') {
                        intelligence += 3; dexterity += 2; hp = 85; attack = 18; defense = 9;
                    } else if (selectedClass === 'solo') {
                        strength += 2; constitution += 2; hp = 110; attack = 20; defense = 14;
                    } else if (selectedClass === 'techie') {
                        intelligence += 2; dexterity += 2; hp = 90; attack = 16; defense = 12;
                    } else if (selectedClass === 'fixer') {
                        charisma += 3; intelligence += 1; hp = 95; attack = 17; defense = 11;
                    }
                }
                
                // Özellikleri güncelle
                document.getElementById('stat-hp').textContent = hp;
                document.getElementById('stat-attack').textContent = attack;
                document.getElementById('stat-defense').textContent = defense;
                document.getElementById('stat-strength').textContent = strength;
                document.getElementById('stat-dexterity').textContent = dexterity;
                document.getElementById('stat-intelligence').textContent = intelligence;
                document.getElementById('stat-constitution').textContent = constitution;
                document.getElementById('stat-wisdom').textContent = wisdom;
                document.getElementById('stat-charisma').textContent = charisma;
            }

            function choosePath(path) {
                const storyArea = document.querySelector('.story-text');
                if (path === 'castle') {
                    storyArea.innerHTML = `
                        <h2>🏰 Kaleye Ulaştınız</h2>
                        <p>Eski kale kapısının önündesiniz. Kapı kilitli görünüyor.</p>
                        <p>Etrafta bir anahtar arayabilir veya kapıyı kırmaya çalışabilirsiniz.</p>
                    `;
                } else if (path === 'cave') {
                    storyArea.innerHTML = `
                        <h2>🕳️ Mağaraya Girdiniz</h2>
                        <p>Karanlık mağaranın içindesiniz. Sadece uzaktan bir ışık görüyorsunuz.</p>
                        <p>Işığa doğru ilerleyebilir veya etrafı keşfedebilirsiniz.</p>
                    `;
                }
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="exploreArea()">🔍 ETRAFI KEŞFET</button>
                    <button class="choice-btn" onclick="moveForward()">➡️ İLERLE</button>
                    <button class="choice-btn" onclick="goBack()">⬅️ GERİ DÖN</button>
                `;
            }

            function exploreArea() {
                const storyArea = document.querySelector('.story-text');
                const discoveries = [
                    "Eski bir anahtar buldunuz!",
                    "Bir el feneri buldunuz.",
                    "Yerde altın paralar buldunuz!",
                    "Bir yara bandı buldunuz.",
                    "Eski bir kitap buldunuz."
                ];
                const discovery = discoveries[Math.floor(Math.random() * discoveries.length)];
                
                storyArea.innerHTML = `
                    <h2>🔍 Keşif Sonucu</h2>
                    <p>${discovery}</p>
                    <p>Ne yapmak istiyorsunuz?</p>
                `;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="moveForward()">➡️ İLERLE</button>
                    <button class="choice-btn" onclick="rest()">😴 DİNLEN</button>
                    <button class="choice-btn" onclick="goBack()">⬅️ GERİ DÖN</button>
                `;
            }

            function moveForward() {
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h2>➡️ İlerliyorsunuz</h2>
                    <p>Yeni bir alana ulaştınız. Etrafta ne olduğunu görmek için dikkatli olun.</p>
                    <p>Bir sonraki adımınızı seçin:</p>
                `;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="exploreArea()">🔍 ETRAFI KEŞFET</button>
                    <button class="choice-btn" onclick="rest()">😴 DİNLEN</button>
                    <button class="choice-btn" onclick="goBack()">⬅️ GERİ DÖN</button>
                `;
            }

            function rest() {
                const storyArea = document.querySelector('.story-text');
                const currentHP = parseInt(document.getElementById('stat-hp').textContent);
                const maxHP = 100;
                const healAmount = Math.min(20, maxHP - currentHP);
                
                document.getElementById('stat-hp').textContent = currentHP + healAmount;
                
                storyArea.innerHTML = `
                    <h2>😴 Dinlendiniz</h2>
                    <p>Dinlenerek ${healAmount} HP kazandınız.</p>
                    <p>Şimdi ${document.getElementById('stat-hp').textContent} HP'niz var.</p>
                    <p>Ne yapmak istiyorsunuz?</p>
                `;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="moveForward()">➡️ İLERLE</button>
                    <button class="choice-btn" onclick="exploreArea()">🔍 ETRAFI KEŞFET</button>
                    <button class="choice-btn" onclick="goBack()">⬅️ GERİ DÖN</button>
                `;
            }

            function goBack() {
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h2>⬅️ Geri Döndünüz</h2>
                    <p>Önceki konumunuza geri döndünüz.</p>
                    <p>Ne yapmak istiyorsunuz?</p>
                `;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="startGame()">🎮 OYUNA BAŞLA</button>
                    <button class="choice-btn" onclick="generateStory()">📖 HİKAYE ÜRET</button>
                    <button class="choice-btn" onclick="showCharacter()">👤 KARAKTER GÖSTER</button>
                `;
            }

            function investigate() {
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h2>🔍 Araştırma Sonucu</h2>
                    <p>Dikkatli bir şekilde etrafı incelediniz.</p>
                    <p>Bir ipucu buldunuz! Bu size yardımcı olabilir.</p>
                    <p>Ne yapmak istiyorsunuz?</p>
                `;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="moveForward()">➡️ İLERLE</button>
                    <button class="choice-btn" onclick="rest()">😴 DİNLEN</button>
                    <button class="choice-btn" onclick="goBack()">⬅️ GERİ DÖN</button>
                `;
            }

            function exploreArea() {
                const storyArea = document.querySelector('.story-text');
                const discoveries = [
                    "Eski bir anahtar buldunuz!",
                    "Bir el feneri buldunuz.",
                    "Yerde altın paralar buldunuz!",
                    "Bir yara bandı buldunuz.",
                    "Eski bir kitap buldunuz."
                ];
                const discovery = discoveries[Math.floor(Math.random() * discoveries.length)];
                
                storyArea.innerHTML = `
                    <h2>🔍 Keşif Sonucu</h2>
                    <p>${discovery}</p>
                    <p>Ne yapmak istiyorsunuz?</p>
                `;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="moveForward()">➡️ İLERLE</button>
                    <button class="choice-btn" onclick="rest()">😴 DİNLEN</button>
                    <button class="choice-btn" onclick="goBack()">⬅️ GERİ DÖN</button>
                `;
            }

            function moveForward() {
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h2>➡️ İlerliyorsunuz</h2>
                    <p>Yeni bir alana ulaştınız. Etrafta ne olduğunu görmek için dikkatli olun.</p>
                    <p>Bir sonraki adımınızı seçin:</p>
                `;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="exploreArea()">🔍 ETRAFI KEŞFET</button>
                    <button class="choice-btn" onclick="rest()">😴 DİNLEN</button>
                    <button class="choice-btn" onclick="goBack()">⬅️ GERİ DÖN</button>
                `;
            }

            function rest() {
                const storyArea = document.querySelector('.story-text');
                const currentHP = parseInt(document.getElementById('stat-hp').textContent);
                const maxHP = 100;
                const healAmount = Math.min(20, maxHP - currentHP);
                
                document.getElementById('stat-hp').textContent = currentHP + healAmount;
                
                storyArea.innerHTML = `
                    <h2>😴 Dinlendiniz</h2>
                    <p>Dinlenerek ${healAmount} HP kazandınız.</p>
                    <p>Şimdi ${document.getElementById('stat-hp').textContent} HP'niz var.</p>
                    <p>Ne yapmak istiyorsunuz?</p>
                `;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="moveForward()">➡️ İLERLE</button>
                    <button class="choice-btn" onclick="exploreArea()">🔍 ETRAFI KEŞFET</button>
                    <button class="choice-btn" onclick="goBack()">⬅️ GERİ DÖN</button>
                `;
            }

            function goBack() {
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h2>⬅️ Geri Döndünüz</h2>
                    <p>Önceki konumunuza geri döndünüz.</p>
                    <p>Ne yapmak istiyorsunuz?</p>
                `;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="startGame()">🎮 OYUNA BAŞLA</button>
                    <button class="choice-btn" onclick="generateStory()">📖 HİKAYE ÜRET</button>
                    <button class="choice-btn" onclick="showCharacter()">👤 KARAKTER GÖSTER</button>
                `;
            }

            function investigate() {
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h2>🔍 Araştırma Sonucu</h2>
                    <p>Dikkatli bir şekilde etrafı incelediniz.</p>
                    <p>Bir ipucu buldunuz! Bu size yardımcı olabilir.</p>
                    <p>Ne yapmak istiyorsunuz?</p>
                `;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="moveForward()">➡️ İLERLE</button>
                    <button class="choice-btn" onclick="rest()">😴 DİNLEN</button>
                    <button class="choice-btn" onclick="goBack()">⬅️ GERİ DÖN</button>
                `;
            }

            function saveGame() {
                const gameData = {
                    characterName: characterName,
                    selectedRace: selectedRace,
                    selectedClass: selectedClass,
                    currentTheme: currentTheme,
                    stats: {
                        hp: document.getElementById('stat-hp').textContent,
                        attack: document.getElementById('stat-attack').textContent,
                        defense: document.getElementById('stat-defense').textContent,
                        strength: document.getElementById('stat-strength').textContent
                    }
                };
                
                localStorage.setItem('aiDungeonMasterSave', JSON.stringify(gameData));
                alert('Oyun başarıyla kaydedildi!');
            }

            function loadGame() {
                const savedData = localStorage.getItem('aiDungeonMasterSave');
                if (savedData) {
                    const gameData = JSON.parse(savedData);
                    characterName = gameData.characterName;
                    selectedRace = gameData.selectedRace;
                    selectedClass = gameData.selectedClass;
                    currentTheme = gameData.currentTheme;
                    
                    document.getElementById('character-name-input').value = characterName;
                    document.getElementById('stat-hp').textContent = gameData.stats.hp;
                    document.getElementById('stat-attack').textContent = gameData.stats.attack;
                    document.getElementById('stat-defense').textContent = gameData.stats.defense;
                    document.getElementById('stat-strength').textContent = gameData.stats.strength;
                    
                    updateCharacterDisplay();
                    alert('Oyun başarıyla yüklendi!');
                } else {
                    alert('Kaydedilmiş oyun bulunamadı!');
                }
            }

            function inventory() {
                alert('Envanter sistemi yakında eklenecek!');
            }

            function skills() {
                alert('Yetenek sistemi yakında eklenecek!');
            }

            function combat() {
                alert('Savaş sistemi yakında eklenecek!');
            }

            // NPC Interaction System
            function interactWithNPC(npc, response) {
                let npcData = npcRelationships[npc];
                const storyArea = document.querySelector('.story-text');
                
                if (npc === 'aldric') {
                    if (response === 'agree') {
                        npcData.trust += 20;
                        addXP(50);
                        storyArea.innerHTML = `
                            <h3>✅ Aldric ile Güven Artışı!</h3>
                            <p><strong>Aldric Güven Seviyesi:</strong> ${npcData.trust}/100</p>
                            <p><strong>XP Kazandınız:</strong> +50 | <strong>Toplam XP:</strong> ${playerXP}</p>
                            <hr>
                            <p><strong>Aldric</strong> gülümsüyor: "Akıllı seçim! Önce köydeki görevleri tamamlayalım. 
                            Şifalı otlar topla, köylüleri koru, sonra ejderha için hazır olacaksın."</p>
                            <p>Aldric sana ilk görevi veriyor...</p>
                        `;
                        
                        const choiceButtons = document.querySelector('.choice-buttons');
                        choiceButtons.innerHTML = `
                            <button class="choice-btn" onclick="startQuest('healing_herbs')">🌿 "Şifalı ot toplama görevini kabul ediyorum"</button>
                            <button class="choice-btn" onclick="interactWithNPC('lydia', 'first_meet')">💊 "Önce Lydia ile konuşayım"</button>
                            <button class="choice-btn" onclick="exploreVillage()">🏘️ "Köyü keşfetmek istiyorum"</button>
                        `;
                    } else if (response === 'stubborn') {
                        npcData.trust -= 10;
                        storyArea.innerHTML = `
                            <h3>⚠️ Aldric'in Güveni Azaldı!</h3>
                            <p><strong>Aldric Güven Seviyesi:</strong> ${npcData.trust}/100</p>
                            <hr>
                            <p><strong>Aldric</strong> kaşlarını çatıyor: "Tecrübesizlik! Ejderha seni bir nefeste öldürür. 
                            Ama madem kararını verdin... Kendi yolunu çiz."</p>
                            <p>Aldric senden uzaklaşıyor. Bu, ileride ona olan güvenini etkileyebilir...</p>
                        `;
                        
                        const choiceButtons = document.querySelector('.choice-buttons');
                        choiceButtons.innerHTML = `
                            <button class="choice-btn" onclick="directToDragon()">🐉 "Ejderha mağarasına doğrudan git"</button>
                            <button class="choice-btn" onclick="apologizeToAldric()">🙏 "Aldric'ten özür dile"</button>
                            <button class="choice-btn" onclick="findOtherAllies()">👥 "Başka müttefikler bul"</button>
                        `;
                    }
                } else if (npc === 'zara') {
                    if (response === 'agree') {
                        npcData.trust += 30;
                        addXP(75);
                        storyArea.innerHTML = `
                            <h3>💻 Zara ile Devrimci İttifak!</h3>
                            <p><strong>Zara Güven Seviyesi:</strong> ${npcData.trust}/100</p>
                            <p><strong>XP Kazandınız:</strong> +75 | <strong>Toplam XP:</strong> ${playerXP}</p>
                            <hr>
                            <p><strong>Zara</strong> heyecanla: "Harika! İlk hedefimiz MegaCorp'un veri merkezine sızmak. 
                            Ama dikkatli olmamız gerek - Rex Steel'in güvenlik sistemleri çok güçlü."</p>
                            <p>Zara size gelişmiş bir hacking aracı veriyor...</p>
                        `;
                        
                        const choiceButtons = document.querySelector('.choice-buttons');
                        choiceButtons.innerHTML = `
                            <button class="choice-btn" onclick="startQuest('data_infiltration')">🔓 "Veri merkezine sızma görevini başlat"</button>
                            <button class="choice-btn" onclick="gatherIntel()">🔍 "Önce istihbarat toplayalım"</button>
                            <button class="choice-btn" onclick="meetOtherHackers()">👥 "Diğer hackerlarla tanışmak istiyorum"</button>
                        `;
                    }
                } else if (npc === 'lydia' && response === 'first_meet') {
                    npcData.trust += 15;
                    storyArea.innerHTML = `
                        <h3>💊 Şifacı Lydia ile Tanışma</h3>
                        <p><strong>Lydia Güven Seviyesi:</strong> ${npcData.trust}/100</p>
                        <hr>
                        <p><strong>Lydia</strong> yumuşak bir sesle: "Merhaba cesur avcı. Ben köyün şifacısıyım. 
                        Yolculuğun için sana şifalı iksirler hazırlayabilirim... Ama bir şey var..."</p>
                        <p>Lydia'nın gözlerinde gizemli bir ışık parlıyor.</p>
                        <p><em>Not: Lydia'nın sırrı hikayenin ilerleyen bölümlerinde ortaya çıkacak...</em></p>
                    `;
                    
                    const choiceButtons = document.querySelector('.choice-buttons');
                    choiceButtons.innerHTML = `
                        <button class="choice-btn" onclick="askLydiaSecret()">❓ "Ne tür bir şey? Bana anlatabilir misin?"</button>
                        <button class="choice-btn" onclick="acceptPotions()">💊 "İksirler için teşekkürler"</button>
                        <button class="choice-btn" onclick="observeLydia()">👁️ "Lydia'yı dikkatlice gözlemle"</button>
                    `;
                }
                
                updateNPCDisplay();
            }

            // Plot Twist System
            function triggerPlotTwist(twistType) {
                const storyArea = document.querySelector('.story-text');
                
                if (twistType === 'aldric_betrayal' && !plotTwistsUnlocked.includes('aldric_betrayal')) {
                    plotTwistsUnlocked.push('aldric_betrayal');
                    npcRelationships.aldric.betrayalRevealed = true;
                    
                    storyArea.innerHTML = `
                        <h2>💥 ŞOK! ALDRIC'IN İHANETİ!</h2>
                        <p><strong>Plot Twist Açıldı:</strong> Aldric'in Gerçek Yüzü</p>
                        <hr>
                        <p>Ejderha mağarasının önünde korkunç gerçek ortaya çıkıyor...</p>
                        <p><strong>Aldric</strong> aniden sana sırtını dönüyor: "Özür dilerim genç avcı... 
                        Ama Pyraxis benim efendim! Seni buraya getirmem için bana altın dağları vaat etti!"</p>
                        <p><strong>Ejderha Pyraxis</strong> gülerek: "Mükemmel plan değil mi? En güvendiğin kişi seni ele verdi!"</p>
                        <p>Şimdi hem Aldric hem de ejderhayla savaşman gerekiyor!</p>
                    `;
                    
                    const choiceButtons = document.querySelector('.choice-buttons');
                    choiceButtons.innerHTML = `
                        <button class="choice-btn" onclick="fightBoth()">⚔️ "İkisiyle de savaş!"</button>
                        <button class="choice-btn" onclick="tryToConvinceAldric()">💬 "Aldric'i ikna etmeye çalış"</button>
                        <button class="choice-btn" onclick="makeAllianceWithDragon()">🤝 "Ejderhayla ittifak yap"</button>
                    `;
                    
                } else if (twistType === 'lydia_dragon_identity' && !plotTwistsUnlocked.includes('lydia_dragon_identity')) {
                    plotTwistsUnlocked.push('lydia_dragon_identity');
                    npcRelationships.lydia.dragonIdentityRevealed = true;
                    
                    storyArea.innerHTML = `
                        <h2>🐲 İNANILMAZ SÜRPRIZ! LYDIA'NIN GERÇEĞİ!</h2>
                        <p><strong>Plot Twist Açıldı:</strong> Lydia'nın Gerçek Kimliği</p>
                        <hr>
                        <p>Kritik anda Lydia aniden parıldıyor ve altın pullu ejderha formuna dönüşüyor!</p>
                        <p><strong>Lydia (Ejderha formu)</strong>: "Özür dilerim sevgili dostum... Ben Pyraxis'in kardeşiyim. 
                        Ama artık insanları sevdim. Kardeşimi durdurmana yardım edeceğim!"</p>
                        <p>Bu ihanet mi, yoksa yeni bir ittifak mı? Karar senin!</p>
                    `;
                    
                    const choiceButtons = document.querySelector('.choice-buttons');
                    choiceButtons.innerHTML = `
                        <button class="choice-btn" onclick="acceptDragonAlliance()">🤝 "Lydia'ya güven ve ittifak yap"</button>
                        <button class="choice-btn" onclick="feelBetrayed()">💔 "İhanete uğradığını hisset"</button>
                        <button class="choice-btn" onclick="askForProof()">❓ "Sadakatinin kanıtını iste"</button>
                    `;
                }
            }

            // Quest System
            function startQuest(questType) {
                currentQuest = questType;
                const storyArea = document.querySelector('.story-text');
                
                if (questType === 'healing_herbs') {
                    storyArea.innerHTML = `
                        <h3>🌿 Görev: Şifalı Ot Toplama</h3>
                        <p><strong>Görev Vereni:</strong> Aldric</p>
                        <p><strong>Açıklama:</strong> Ormandan 5 adet şifalı ot topla</p>
                        <hr>
                        <p>Ormana giriyorsun. Şifalı otlar burada bir yerde olmalı...</p>
                        <p>Ama dikkat et! Orman tehlikeli yaratıklarla dolu.</p>
                    `;
                    
                    const choiceButtons = document.querySelector('.choice-buttons');
                    choiceButtons.innerHTML = `
                        <button class="choice-btn" onclick="searchHerbs('carefully')">🔍 "Dikkatli şekilde ara"</button>
                        <button class="choice-btn" onclick="searchHerbs('quickly')">⏰ "Hızlıca topla"</button>
                        <button class="choice-btn" onclick="searchHerbs('magical')">✨ "Büyü kullanarak ara"</button>
                    `;
                }
            }

            // Combat System
            function startCombat(enemy, enemyStats) {
                inCombat = true;
                combatRound = 1;
                enemyHP = enemyStats.hp;
                
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h3>⚔️ SAVAŞ BAŞLADI!</h3>
                    <p><strong>Düşman:</strong> ${enemy}</p>
                    <p><strong>Düşman HP:</strong> ${enemyHP}/${enemyStats.hp}</p>
                    <p><strong>Sizin HP:</strong> ${playerHP}/100</p>
                    <p><strong>Round:</strong> ${combatRound}</p>
                    <hr>
                    <p>${enemy} ile epic bir savaş başlıyor!</p>
                `;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="combatAction('attack')">⚔️ SALDI</button>
                    <button class="choice-btn" onclick="combatAction('defend')">🛡️ SAVUN</button>
                    <button class="choice-btn" onclick="combatAction('special')">✨ ÖZEL SALDIRI</button>
                    <button class="choice-btn" onclick="combatAction('flee')">🏃 KAÇMAYA ÇALIŞ</button>
                `;
            }

            // XP and Level System
            function addXP(amount) {
                playerXP += amount;
                checkLevelUp();
                updateStatsDisplay();
            }

            function checkLevelUp() {
                const xpNeeded = playerLevel * 100;
                if (playerXP >= xpNeeded) {
                    playerLevel++;
                    playerXP -= xpNeeded;
                    levelUp();
                }
            }

            function levelUp() {
                alert(`🎉 LEVEL UP! Şimdi ${playerLevel}. seviyesiniz!`);
                updateCharacterStats();
            }

            function updateStatsDisplay() {
                // HP, XP ve level güncelleme
                document.getElementById('stat-hp').textContent = playerHP;
                // Level ve XP gösterimi için yeni alanlar eklenebilir
            }

            function updateNPCDisplay() {
                // NPC ilişkilerini gösteren UI güncellemesi
                // Bu kısım daha sonra genişletilebilir
            }

            // Missing Functions Implementation
            function exploreVillage() {
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h3>🏘️ Köy Keşfi</h3>
                    <p>Köyde dolaşıyorsun. Farklı yerler ve insanlar görüyorsun...</p>
                    <ul>
                        <li>🏠 Aldric'in evi - Eğitim alabilirsin</li>
                        <li>💊 Lydia'nın şifahanesi - İksir alabilirsin</li>
                        <li>🏛️ Köy meydanı - Büyüklerle konuşabilirsin</li>
                        <li>🗡️ Silah ustası - Ekipman geliştirebilirsin</li>
                    </ul>
                `;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="visitAldric()">🏠 "Aldric'i ziyaret et"</button>
                    <button class="choice-btn" onclick="visitLydia()">💊 "Lydia'nın şifahanesine git"</button>
                    <button class="choice-btn" onclick="visitWeaponsmith()">🗡️ "Silah ustasını görmeye git"</button>
                    <button class="choice-btn" onclick="startGame()">🎮 "Maceraya başla"</button>
                `;
            }

            function searchHerbs(method) {
                const storyArea = document.querySelector('.story-text');
                let herbsFound = 0;
                let xpGained = 0;
                let danger = false;
                
                if (method === 'carefully') {
                    herbsFound = 5;
                    xpGained = 100;
                    storyArea.innerHTML = `
                        <h3>🌿 Başarılı Ot Toplama!</h3>
                        <p>Dikkatli araman sonuç verdi! 5/5 şifalı ot topladın.</p>
                        <p><strong>XP Kazandın:</strong> +${xpGained}</p>
                    `;
                } else if (method === 'quickly') {
                    herbsFound = 3;
                    xpGained = 50;
                    danger = true;
                    storyArea.innerHTML = `
                        <h3>⚠️ Kısmi Başarı!</h3>
                        <p>Acele ettin! Sadece 3/5 şifalı ot topladın.</p>
                        <p>Ama dikkat! Bir orman canavarı yaklaşıyor!</p>
                    `;
                } else if (method === 'magical') {
                    herbsFound = 7;
                    xpGained = 150;
                    storyArea.innerHTML = `
                        <h3>✨ Büyülü Başarı!</h3>
                        <p>Büyün sayesinde ekstra şifalı otlar buldun! 7/5 şifalı ot topladın.</p>
                        <p>Bonus ödül: Nadir şifalı ot!</p>
                    `;
                }
                
                addXP(xpGained);
                
                const choiceButtons = document.querySelector('.choice-buttons');
                if (danger) {
                    choiceButtons.innerHTML = `
                        <button class="choice-btn" onclick="startCombat('Orman Canavarı', {hp: 80, attack: 20})">⚔️ "Canavarla savaş!"</button>
                        <button class="choice-btn" onclick="fleeFromDanger()">🏃 "Kaçmaya çalış!"</button>
                        <button class="choice-btn" onclick="hideFromMonster()">🌿 "Saklanmaya çalış!"</button>
                    `;
                } else {
                    choiceButtons.innerHTML = `
                        <button class="choice-btn" onclick="returnToAldric()">🏠 "Aldric'e dön"</button>
                        <button class="choice-btn" onclick="continueExploring()">🔍 "Keşfe devam et"</button>
                        <button class="choice-btn" onclick="visitLydia()">💊 "Lydia'yı ziyaret et"</button>
                    `;
                }
            }

            function combatAction(action) {
                if (!inCombat) return;
                
                const storyArea = document.querySelector('.story-text');
                combatRound++;
                
                let playerDamage = 0;
                let enemyDamage = 0;
                let actionText = '';
                
                if (action === 'attack') {
                    playerDamage = Math.floor(Math.random() * 30) + 20;
                    enemyDamage = Math.floor(Math.random() * 20) + 10;
                    actionText = `Saldırın ${playerDamage} hasar verdi!`;
                } else if (action === 'defend') {
                    playerDamage = Math.floor(Math.random() * 15) + 10;
                    enemyDamage = Math.floor(Math.random() * 10) + 5;
                    actionText = `Savunduğunuz için daha az hasar aldınız!`;
                } else if (action === 'special') {
                    playerDamage = Math.floor(Math.random() * 50) + 30;
                    enemyDamage = Math.floor(Math.random() * 25) + 15;
                    actionText = `Özel saldırınız ${playerDamage} hasar verdi!`;
                } else if (action === 'flee') {
                    if (Math.random() > 0.5) {
                        inCombat = false;
                        storyArea.innerHTML = `
                            <h3>🏃 Kaçış Başarılı!</h3>
                            <p>Savaştan başarıyla kaçtınız!</p>
                        `;
                        const choiceButtons = document.querySelector('.choice-buttons');
                        choiceButtons.innerHTML = `
                            <button class="choice-btn" onclick="exploreArea()">🔍 "Güvenli bir yer ara"</button>
                            <button class="choice-btn" onclick="rest()">😴 "Dinlen"</button>
                        `;
                        return;
                    } else {
                        actionText = `Kaçış başarısız! Düşman saldırdı!`;
                        enemyDamage = Math.floor(Math.random() * 30) + 20;
                    }
                }
                
                enemyHP -= playerDamage;
                playerHP -= enemyDamage;
                
                if (enemyHP <= 0) {
                    inCombat = false;
                    addXP(200);
                    storyArea.innerHTML = `
                        <h3>🎉 ZAFER!</h3>
                        <p>Düşmanı yendiniz!</p>
                        <p><strong>XP Kazandınız:</strong> +200</p>
                        <p>Level: ${playerLevel} | XP: ${playerXP}</p>
                    `;
                    
                    const choiceButtons = document.querySelector('.choice-buttons');
                    choiceButtons.innerHTML = `
                        <button class="choice-btn" onclick="collectLoot()">💰 "Ganimet topla"</button>
                        <button class="choice-btn" onclick="continueQuest()">➡️ "Göreve devam et"</button>
                        <button class="choice-btn" onclick="rest()">😴 "Dinlen"</button>
                    `;
                    return;
                }
                
                if (playerHP <= 0) {
                    inCombat = false;
                    storyArea.innerHTML = `
                        <h3>💀 YENİLGİ!</h3>
                        <p>Düşman sizi yendi... Ama hikaye burada bitmiyor!</p>
                        <p>Bir şekilde kurtuldunuz ama HP'niz düşük.</p>
                    `;
                    playerHP = 10;
                    
                    const choiceButtons = document.querySelector('.choice-buttons');
                    choiceButtons.innerHTML = `
                        <button class="choice-btn" onclick="seekHealing()">💊 "Şifacı ara"</button>
                        <button class="choice-btn" onclick="rest()">😴 "Dinlenmeye çalış"</button>
                        <button class="choice-btn" onclick="retreatToVillage()">🏠 "Köye geri dön"</button>
                    `;
                    return;
                }
                
                storyArea.innerHTML = `
                    <h3>⚔️ SAVAŞ DEVAM EDİYOR!</h3>
                    <p><strong>Round ${combatRound}</strong></p>
                    <p>${actionText}</p>
                    <p><strong>Düşman HP:</strong> ${enemyHP > 0 ? enemyHP : 0}</p>
                    <p><strong>Sizin HP:</strong> ${playerHP > 0 ? playerHP : 0}</p>
                    <hr>
                    <p>Savaş devam ediyor! Bir sonraki hamlenizi seçin:</p>
                `;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="combatAction('attack')">⚔️ SALDI</button>
                    <button class="choice-btn" onclick="combatAction('defend')">🛡️ SAVUN</button>
                    <button class="choice-btn" onclick="combatAction('special')">✨ ÖZEL SALDIRI</button>
                    <button class="choice-btn" onclick="combatAction('flee')">🏃 KAÇMAYA ÇALIŞ</button>
                `;
            }

            function directToDragon() {
                storyProgress = 5; // İleri atlıyoruz
                if (Math.random() > 0.3) { // %70 ihtimalle plot twist
                    triggerPlotTwist('aldric_betrayal');
                } else {
                    const storyArea = document.querySelector('.story-text');
                    storyArea.innerHTML = `
                        <h2>🐉 Ejderha Mağarası</h2>
                        <p>Doğrudan ejderha mağarasına geldiniz ama çok zayıfsınız!</p>
                        <p>Pyraxis sizi görünce gülerek: "Başka bir cesur fool! Seni yakacağım!"</p>
                    `;
                    
                    startCombat('Kızıl Ejderha Pyraxis', {hp: 300, attack: 50});
                }
            }

            function fightBoth() {
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h2>⚔️ İKİLİ SAVAŞ!</h2>
                    <p>Hem Aldric hem de Pyraxis'e karşı epic bir savaş başlıyor!</p>
                    <p>Bu çok zor olacak ama imkansız değil...</p>
                `;
                
                startCombat('Aldric & Pyraxis', {hp: 400, attack: 60});
            }

            function makeAllianceWithDragon() {
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h2>🤝 DARK LORD ENDING!</h2>
                    <p><strong>Sonlardan Biri: Karanlık Lord</strong></p>
                    <hr>
                    <p>Pyraxis ile ittifak yaptınız! Birlikte köyü yöneteceksiniz.</p>
                    <p>İnsanlar sizi korkar ama siz güçlüsünüz. Bu bir son...</p>
                    <p><strong>🏆 Başarım Açıldı:</strong> Dark Lord Ending</p>
                `;
                
                endGame('dark_lord');
            }

            function acceptDragonAlliance() {
                npcRelationships.lydia.trust = 100;
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h2>🐲 DRAGON ALLIANCE ENDING!</h2>
                    <p><strong>Sonlardan Biri: Ejderha İttifakı</strong></p>
                    <hr>
                    <p>Lydia ile birlikte kardeşi Pyraxis'i ikna ettiniz!</p>
                    <p>Artık ejderhalar ve insanlar barış içinde yaşıyor.</p>
                    <p><strong>🏆 Başarım Açıldı:</strong> Dragon Alliance Ending</p>
                `;
                
                endGame('dragon_alliance');
            }

            function endGame(endingType) {
                gameState = 'ended';
                questsCompleted.push(endingType);
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="showAllEndings()">📜 "Tüm sonları gör"</button>
                    <button class="choice-btn" onclick="playAgain()">🔄 "Tekrar oyna"</button>
                    <button class="choice-btn" onclick="resetGame()">🆕 "Yeni oyun"</button>
                `;
            }

            function showAllEndings() {
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h2>📜 TÜM SONLAR</h2>
                    <h3>🐉 Dragon Hunter Sonları:</h3>
                    <ul>
                        <li>✅ Good Ending - Ejderhayı yen, köyü kurtar</li>
                        <li>💔 Betrayal Ending - Aldric'in ihanetini keşfet</li>
                        <li>🤝 Dragon Alliance - Ejderhalarla barış</li>
                        <li>🕯️ Sacrifice Ending - Kendini feda et</li>
                        <li>👑 Dark Lord Ending - Karanlık güçlerle ittifak</li>
                    </ul>
                    <h3>🌃 Cyberpunk Sonları:</h3>
                    <ul>
                        <li>🔥 Revolution Ending - Sistemi çökert</li>
                        <li>💼 Corporate Ending - Şirketlere katıl</li>
                        <li>🤖 AI Merge Ending - AI ile birleş</li>
                        <li>👤 Underground King - Gölgeden yönet</li>
                        <li>🐺 Lone Wolf - Herkesi aldat</li>
                    </ul>
                `;
            }

            function playAgain() {
                // Aynı karakterle yeni macera
                storyProgress = 0;
                plotTwistsUnlocked = [];
                currentQuest = null;
                startGame();
            }

            // Missing Critical Functions
            function visitWeaponsmith() {
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h3>🗡️ Silah Ustası Dükkanı</h3>
                    <p>Yaşlı silah ustası Gareth seni karşılıyor: "Merhaba genç savaşçı! Senin için ne yapabilirim?"</p>
                    <ul>
                        <li>🗡️ Kılıç geliştirme - 100 altın</li>
                        <li>🛡️ Zırh tamir - 50 altın</li>
                        <li>🏹 Yay ve ok - 75 altın</li>
                    </ul>
                `;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="buyWeapon('sword')">🗡️ "Kılıç satın al"</button>
                    <button class="choice-btn" onclick="buyWeapon('armor')">🛡️ "Zırh tamir ettir"</button>
                    <button class="choice-btn" onclick="buyWeapon('bow')">🏹 "Yay satın al"</button>
                    <button class="choice-btn" onclick="exploreVillage()">🏘️ "Köye geri dön"</button>
                `;
            }

            function buyWeapon(weaponType) {
                const storyArea = document.querySelector('.story-text');
                if (weaponType === 'sword') {
                    storyArea.innerHTML = `
                        <h3>🗡️ Kılıç Satın Alındı!</h3>
                        <p>Saldırı gücünüz +10 arttı!</p>
                    `;
                    let currentAttack = parseInt(document.getElementById('stat-attack').textContent);
                    document.getElementById('stat-attack').textContent = currentAttack + 10;
                } else if (weaponType === 'armor') {
                    storyArea.innerHTML = `
                        <h3>🛡️ Zırh Tamir Edildi!</h3>
                        <p>Savunma gücünüz +5 arttı!</p>
                    `;
                    let currentDefense = parseInt(document.getElementById('stat-defense').textContent);
                    document.getElementById('stat-defense').textContent = currentDefense + 5;
                } else if (weaponType === 'bow') {
                    storyArea.innerHTML = `
                        <h3>🏹 Yay Satın Alındı!</h3>
                        <p>Uzaktan saldırı yeteneği kazandınız!</p>
                    `;
                }
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="visitWeaponsmith()">🗡️ "Başka bir şey al"</button>
                    <button class="choice-btn" onclick="exploreVillage()">🏘️ "Köye geri dön"</button>
                    <button class="choice-btn" onclick="startGame()">🎮 "Maceraya başla"</button>
                `;
            }

            function fleeFromDanger() {
                const storyArea = document.querySelector('.story-text');
                if (Math.random() > 0.4) {
                    storyArea.innerHTML = `
                        <h3>🏃 Başarılı Kaçış!</h3>
                        <p>Hızla koşarak tehlikeden uzaklaştınız!</p>
                        <p>Güvenli bir yere ulaştınız.</p>
                    `;
                    
                    const choiceButtons = document.querySelector('.choice-buttons');
                    choiceButtons.innerHTML = `
                        <button class="choice-btn" onclick="rest()">😴 "Nefes al ve dinlen"</button>
                        <button class="choice-btn" onclick="exploreArea()">🔍 "Etrafı keşfet"</button>
                        <button class="choice-btn" onclick="returnToAldric()">🏠 "Aldric'e geri dön"</button>
                    `;
                } else {
                    storyArea.innerHTML = `
                        <h3>⚠️ Kaçış Başarısız!</h3>
                        <p>Canavar sizi yakaladı! Savaşmak zorundasınız!</p>
                    `;
                    
                    startCombat('Orman Canavarı', {hp: 80, attack: 20});
                }
            }

            function hideFromMonster() {
                const storyArea = document.querySelector('.story-text');
                if (Math.random() > 0.3) {
                    storyArea.innerHTML = `
                        <h3>🌿 Başarılı Saklanma!</h3>
                        <p>Ağaçların arkasına saklandınız. Canavar sizi görmedi ve uzaklaştı.</p>
                        <p>Artık güvendesiniz.</p>
                    `;
                    
                    const choiceButtons = document.querySelector('.choice-buttons');
                    choiceButtons.innerHTML = `
                        <button class="choice-btn" onclick="continueExploring()">🔍 "Aramaya devam et"</button>
                        <button class="choice-btn" onclick="returnToAldric()">🏠 "Aldric'e geri dön"</button>
                        <button class="choice-btn" onclick="rest()">😴 "Dinlen"</button>
                    `;
                } else {
                    storyArea.innerHTML = `
                        <h3>👁️ Fark Edildin!</h3>
                        <p>Canavar sizi gördü! Artık savaş kaçınılmaz!</p>
                    `;
                    
                    startCombat('Orman Canavarı', {hp: 80, attack: 20});
                }
            }

            function retreatToVillage() {
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h3>🏠 Köye Geri Dönüş</h3>
                    <p>Yaralı olarak köye geri döndünüz. Köylüler size yardım ediyor.</p>
                    <p>Lydia sizi iyileştirdi. HP'niz restore edildi!</p>
                `;
                
                playerHP = 50; // Kısmen iyileştir
                document.getElementById('stat-hp').textContent = playerHP;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="visitLydia()">💊 "Lydia ile konuş"</button>
                    <button class="choice-btn" onclick="visitAldric()">🏠 "Aldric'i ziyaret et"</button>
                    <button class="choice-btn" onclick="rest()">😴 "Tam dinlen"</button>
                `;
            }

            function meetOtherHackers() {
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h3>👥 Underground Hacker Topluluğu</h3>
                    <p>Zara sizi gizli hacker topluluğuna götürüyor...</p>
                    <p>Burada Rex Steel'e karşı savaşan diğer devrimcilerle tanışıyorsunuz.</p>
                    <p><strong>Nova:</strong> "Yeni üye! MegaCorp'a karşı birlikte savaşacağız!"</p>
                `;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="planRevolution()">🔥 "Devrim planla"</button>
                    <button class="choice-btn" onclick="gatherIntel()">🔍 "İstihbarat topla"</button>
                    <button class="choice-btn" onclick="hackTraining()">💻 "Hacking eğitimi al"</button>
                `;
            }

            function planRevolution() {
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h3>🔥 Devrim Planı</h3>
                    <p>Hacker grubu ile birlikte MegaCorp'un ana sistemlerine saldırı planı yapıyorsunuz!</p>
                    <p>Bu epik bir son olabilir...</p>
                `;
                
                addXP(300);
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="executeRevolution()">⚡ "Devrimi başlat!"</button>
                    <button class="choice-btn" onclick="soloMission()">🚶 "Tek başına git"</button>
                    <button class="choice-btn" onclick="gatherIntel()">📊 "Daha fazla bilgi topla"</button>
                `;
            }

            function executeRevolution() {
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h2>🔥 REVOLUTION ENDING!</h2>
                    <p><strong>Sonlardan Biri: Devrim</strong></p>
                    <hr>
                    <p>Hacker topluluğu ile birlikte MegaCorp'u çökerttiniz!</p>
                    <p>Şehir artık özgür! İnsanlar AI kontrolünden kurtuldu!</p>
                    <p><strong>🏆 Başarım Açıldı:</strong> Revolution Ending</p>
                `;
                
                endGame('revolution');
            }

            function hackTraining() {
                const storyArea = document.querySelector('.story-text');
                storyArea.innerHTML = `
                    <h3>💻 Hacking Eğitimi</h3>
                    <p>Gelişmiş hacking teknikleri öğreniyorsunuz...</p>
                    <p>Saldırı gücünüz arttı!</p>
                `;
                
                addXP(150);
                let currentAttack = parseInt(document.getElementById('stat-attack').textContent);
                document.getElementById('stat-attack').textContent = currentAttack + 15;
                
                const choiceButtons = document.querySelector('.choice-buttons');
                choiceButtons.innerHTML = `
                    <button class="choice-btn" onclick="planRevolution()">🔥 "Devrim planla"</button>
                    <button class="choice-btn" onclick="soloMission()">🚶 "Tek operasyon yap"</button>
                    <button class="choice-btn" onclick="meetOtherHackers()">👥 "Grup ile kal"</button>
                `;
            }

            // Helper functions
            function visitAldric() { interactWithNPC('aldric', 'visit'); }
            function visitLydia() { interactWithNPC('lydia', 'first_meet'); }
            function apologizeToAldric() { interactWithNPC('aldric', 'apologize'); }
            function returnToAldric() { interactWithNPC('aldric', 'return_quest'); }
            function soloMission() { startQuest('solo_hack'); }
            function gatherIntel() { startQuest('intel_gathering'); }
            function askLydiaSecret() { triggerPlotTwist('lydia_dragon_identity'); }
            function feelBetrayed() { npcRelationships.lydia.trust -= 30; }
            function seekHealing() { visitLydia(); }
            function collectLoot() { addXP(50); exploreArea(); }
            function continueQuest() { startGame(); }
            function continueExploring() { exploreArea(); }

            function resetGame() {
                if (confirm('Oyunu sıfırlamak istediğinizden emin misiniz?')) {
                    // Tüm oyun değişkenlerini sıfırla
                    characterName = '';
                    selectedRace = '';
                    selectedClass = '';
                    playerLevel = 1;
                    playerXP = 0;
                    currentQuest = null;
                    questsCompleted = [];
                    currentScenario = null;
                    storyProgress = 0;
                    plotTwistsUnlocked = [];
                    gameState = 'character_creation';
                    inCombat = false;
                    combatRound = 0;
                    enemyHP = 100;
                    playerHP = 100;
                    
                    // NPC ilişkilerini sıfırla
                    npcRelationships = {
                        aldric: { trust: 0, quests: 0, status: 'neutral', betrayalRevealed: false },
                        lydia: { trust: 0, quests: 0, status: 'neutral', dragonIdentityRevealed: false },
                        marcus: { trust: 0, quests: 0, status: 'neutral' },
                        zara: { trust: 0, quests: 0, status: 'neutral' },
                        rexSteel: { trust: 0, quests: 0, status: 'enemy' }
                    };
                    
                    document.getElementById('character-name-input').value = '';
                    document.querySelectorAll('.list-item').forEach(item => {
                        item.classList.remove('selected');
                    });
                    updateCharacterDisplay();
                    
                    // İstatistikleri sıfırla
                    document.getElementById('stat-hp').textContent = '100';
                    document.getElementById('stat-attack').textContent = '15';
                    document.getElementById('stat-defense').textContent = '10';
                    document.getElementById('stat-strength').textContent = '12';
                    
                    // Hikaye alanını sıfırla
                    const storyArea = document.querySelector('.story-text');
                    storyArea.innerHTML = `
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
                    `;
                    
                    const choiceButtons = document.querySelector('.choice-buttons');
                    choiceButtons.innerHTML = `
                        <button class="choice-btn" onclick="startGame()">🎮 OYUNA BAŞLA</button>
                        <button class="choice-btn" onclick="generateStory()">📖 HİKAYE ÜRET</button>
                        <button class="choice-btn" onclick="showCharacter()">👤 KARAKTER GÖSTER</button>
                    `;
                    
                    alert('Oyun tamamen sıfırlandı! Yeni bir macera başlayabilirsiniz.');
                }
            }
        </script>
    </body>
    </html>
    '''

@app.route('/register')
def register():
    """Register page"""
    return '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Kayıt - AI Dungeon Master</title>
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
            .register-container {
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
        <div class="register-container">
            <div class="game-icon">🎮</div>
            <h2 style="text-align: center; color: #FFD700; margin-bottom: 30px;">KAYIT OL</h2>
            <form onsubmit="handleRegister(event)">
                <div class="form-group">
                    <label>Kullanıcı Adı</label>
                    <input type="text" id="username" placeholder="Kullanıcı adınızı girin" required>
                </div>
                <div class="form-group">
                    <label>E-posta</label>
                    <input type="email" id="email" placeholder="E-posta adresinizi girin" required>
                </div>
                <div class="form-group">
                    <label>Şifre</label>
                    <input type="password" id="password" placeholder="Şifrenizi girin" required>
                </div>
                <div class="form-group">
                    <label>Şifre Tekrar</label>
                    <input type="password" id="password2" placeholder="Şifrenizi tekrar girin" required>
                </div>
                <button type="submit" class="button">KAYIT OL</button>
            </form>
            <p style="text-align: center; margin-top: 20px;">
                <a href="/login" style="color: #FFD700;">Zaten hesabınız var mı? Giriş yapın</a>
            </p>
            <script>
                function handleRegister(event) {
                    event.preventDefault();
                    const username = document.getElementById('username').value;
                    const email = document.getElementById('email').value;
                    const password = document.getElementById('password').value;
                    const password2 = document.getElementById('password2').value;
                    
                    if (password !== password2) {
                        alert('Şifreler eşleşmiyor!');
                        return;
                    }
                    
                    if (username && email && password) {
                        alert('Kayıt başarılı! Giriş sayfasına yönlendiriliyorsunuz...');
                        window.location.href = '/login';
                    } else {
                        alert('Lütfen tüm alanları doldurun!');
                    }
                }
            </script>
        </div>
    </body>
    </html>
    '''

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
                <div class="room-item" onclick="joinRoom('Cyberpunk Mission')">
                    <strong>Cyberpunk Mission</strong> - 3/4 Oyuncu
                </div>
            </div>
            
            <div>
                <button class="button" onclick="createRoom()">YENİ ODA OLUŞTUR</button>
                <button class="button" onclick="refreshRooms()">ODALARI YENİLE</button>
                <button class="button" onclick="window.location.href='/'">ANA SAYFA</button>
            </div>
        </div>
        
        <script>
            function joinRoom(roomName) {
                alert(`${roomName} odasına katılıyorsunuz...`);
                // Burada multiplayer oyun başlatılacak
                window.location.href = '/enhanced';
            }
            
            function createRoom() {
                const roomName = prompt('Oda adını girin:');
                if (roomName) {
                    alert(`${roomName} odası oluşturuldu!`);
                    window.location.href = '/enhanced';
                }
            }
            
            function refreshRooms() {
                alert('Odalar yenileniyor...');
                location.reload();
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
