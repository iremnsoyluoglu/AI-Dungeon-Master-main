#!/usr/bin/env python3
"""
AI Dungeon Master - Main Application
===================================

An intelligent AI-powered Fantasy Role-Playing Game Master that creates 
immersive, dynamic adventures using advanced language models.
"""

import os
import sys

# Proje kök dizinini bul
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "ai_dm.log")

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import logging

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from project root
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

# Initialize SocketIO for real-time communication
socketio = SocketIO(app, cors_allowed_origins="*")

# Import core modules
try:
    from core.game_engine import GameEngine
    from core.campaign_manager import CampaignManager
    from ai.ai_dungeon_master import AIDungeonMaster
    from web.routes import register_routes
except ImportError as e:
    logger.warning(f"Some modules not yet implemented: {e}")
    # Placeholder classes removed, real modules are now present

# Global application state
game_engine = GameEngine()
campaign_manager = CampaignManager()
ai_dm = AIDungeonMaster()
campaign_sessions = {}

@app.route('/')
def index():
    """Main game interface"""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'services': {
            'game_engine': hasattr(game_engine, 'active'),
            'ai_dm': hasattr(ai_dm, 'ready'),
            'campaign_manager': hasattr(campaign_manager, 'campaigns')
        }
    })

@app.route('/api/start-campaign', methods=['POST'])
def start_campaign():
    """Start a new campaign"""
    data = request.get_json()
    campaign_name = data.get('campaign', 'New Campaign')
    game_system = data.get('system', 'dnd5e')
    player_count = data.get('player_count', 1)
    player_class = data.get('player_class', 'warrior')
    characters = data.get('characters', [])
    session_id = f"{campaign_name}_{player_class}_{player_count}"
    campaign_sessions[session_id] = {
        'campaign': campaign_name,
        'player_class': player_class,
        'player_count': player_count,
        'characters': characters,
        'history': []
    }
    logger.info(f"Starting new campaign: {campaign_name} ({player_class}, {player_count} players) with characters: {characters}")
    return jsonify({
        'success': True,
        'campaign_id': session_id,
        'message': f'Campaign "{campaign_name}" ({player_class}, {player_count} players) started.'
    })

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info('Client connected')
    emit('connected', {'message': 'Welcome to AI Dungeon Master!'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info('Client disconnected')

@socketio.on('player_action')
def handle_player_action(data):
    """Handle player actions in the game"""
    action = data.get('action', '')
    player_id = data.get('player_id', 'unknown')
    campaign = data.get('campaign', 'default')
    player_class = data.get('player_class', 'warrior')
    session_id = f"{campaign}_{player_class}_{campaign_sessions.get('player_count', 1)}"
    logger.info(f"Player {player_id} action: {action} (Campaign: {campaign}, Class: {player_class})")
    # Save to session history
    if session_id in campaign_sessions:
        campaign_sessions[session_id]['history'].append({'player_id': player_id, 'action': action})
    # Call the real AI Dungeon Master
    ai_response = ai_dm.run_campaign(action)
    emit('dm_response', {
        'message': ai_response,
        'timestamp': 'now'
    }, broadcast=True)

@socketio.on('dice_roll')
def handle_dice_roll(data):
    """Handle dice rolling"""
    dice_notation = data.get('dice', '1d20')
    player_id = data.get('player_id', 'unknown')
    
    # Simple dice rolling logic (would be expanded)
    import random
    if 'd' in dice_notation:
        try:
            count, sides = map(int, dice_notation.split('d'))
            results = [random.randint(1, sides) for _ in range(count)]
            total = sum(results)
            
            emit('dice_result', {
                'player_id': player_id,
                'dice': dice_notation,
                'results': results,
                'total': total
            }, broadcast=True)
        except ValueError:
            emit('error', {'message': 'Invalid dice notation'})

def create_initial_files():
    """Create initial template files if they don't exist"""
    
    # Create basic index.html if it doesn't exist
    if not os.path.exists('templates/index.html'):
        os.makedirs('templates', exist_ok=True)
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>AI Dungeon Master</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #1a1a1a; color: #fff; }
        .container { max-width: 800px; margin: 0 auto; }
        .welcome { text-align: center; margin-bottom: 40px; }
        .status { background: #2a2a2a; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .actions { display: flex; gap: 10px; margin-top: 20px; }
        button { padding: 10px 20px; background: #0066cc; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0052a3; }
    </style>
</head>
<body>
    <div class=\"container\">
        <div class=\"welcome\">
            <h1>🧙‍♂️ AI Dungeon Master</h1>
            <p>Your intelligent RPG companion</p>
        </div>
        
        <div class=\"status\">
            <h3>System Status</h3>
            <p id=\"status\">Initializing...</p>
        </div>
        
        <div class=\"actions\">
            <button onclick=\"startCampaign()\">Start New Campaign</button>
            <button onclick=\"loadCampaign()\">Load Campaign</button>
            <button onclick=\"rollDice()\">Roll Dice</button>
        </div>
        
        <div id=\"game-area\" style=\"margin-top: 40px; min-height: 200px; background: #2a2a2a; padding: 20px; border-radius: 8px;\">
            <h3>Game Area</h3>
            <p>Welcome! Start a campaign to begin your adventure.</p>
        </div>
    </div>
    
    <script>
        // Basic JavaScript for demo functionality
        function startCampaign() {
            document.getElementById('game-area').innerHTML = '<h3>New Campaign Started!</h3><p>The AI Dungeon Master is preparing your adventure...</p>';
        }
        
        function loadCampaign() {
            alert('Load campaign functionality will be implemented');
        }
        
        function rollDice() {
            const result = Math.floor(Math.random() * 20) + 1;
            const gameArea = document.getElementById('game-area');
            gameArea.innerHTML += `<p><strong>Dice Roll:</strong> d20 = ${result}</p>`;
        }
        
        // Check system status
        fetch('/api/health')
            .then(response => response.json())
            .then(data => {
                document.getElementById('status').textContent = `Status: ${data.status} | Version: ${data.version}`;
            })
            .catch(error => {
                document.getElementById('status').textContent = 'Status: Error connecting to server';
            });
    </script>
</body>
</html>""")

if __name__ == '__main__':
    logger.info("Starting AI Dungeon Master application...")
    
    # Create initial files and directories
    create_initial_files()
    
    # Check for API keys
    if not os.getenv('OPENAI_API_KEY') and not os.getenv('ANTHROPIC_API_KEY'):
        logger.warning("No AI API keys found in environment. Please configure your .env file.")
    
    # Start the application
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    logger.info(f"Server starting on port {port}")
    logger.info("Access the application at: http://localhost:5000")
    
    socketio.run(app, host='0.0.0.0', port=port, debug=debug) 