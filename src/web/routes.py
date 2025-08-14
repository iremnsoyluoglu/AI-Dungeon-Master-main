#!/usr/bin/env python3
"""
Web Routes for FRP Game
=======================

Handles all HTTP routes for:
- Game sessions
- Character management
- Combat system
- Multiplayer functionality
- Scenario management
"""

from flask import request, jsonify, session
from flask_socketio import emit, join_room, leave_room
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def register_routes(app, game_engine, campaign_manager, ai_dm):
    """Register all web routes"""
    
    # Socket.IO event handlers
    def handle_connect(sid, environ):
        """Handle client connection"""
        logger.info(f"Client connected: {sid}")
        emit('connected', {'message': 'Connected to AI Dungeon Master'})
    
    def handle_disconnect(sid):
        """Handle client disconnection"""
        logger.info(f"Client disconnected: {sid}")
    
    def handle_join_session(sid, data):
        """Handle joining a game session"""
        try:
            scenario_id = data.get('scenario_id')
            players = data.get('players', [])
            
            logger.info(f"Join session: {scenario_id} with {len(players)} players")
            
            # Start scenario with AI DM
            game_data = ai_dm.start_scenario(scenario_id, players)
            
            # Join room for this session
            join_room(sid)
            
            # Emit game state
            emit('game_state_update', game_data)
            
        except Exception as e:
            logger.error(f"Error joining session: {e}")
            emit('error', {'message': 'Failed to join session'})
    
    def handle_leave_session(sid, data):
        """Handle leaving a game session"""
        try:
            leave_room(sid)
            emit('left_session', {'message': 'Left session'})
        except Exception as e:
            logger.error(f"Error leaving session: {e}")
    
    def handle_chat_message(sid, data):
        """Handle chat messages"""
        try:
            message = data.get('message')
            player = data.get('player')
            
            logger.info(f"Chat message from {player}: {message}")
            
            # Process message with AI DM
            response = ai_dm.process_chat_message(player, message)
            
            # Broadcast to all players in session
            emit('chat_message', {
                'player': player,
                'message': message,
                'response': response
            }, room=sid)
            
        except Exception as e:
            logger.error(f"Error processing chat message: {e}")
    
    # Register Socket.IO handlers
    app.socketio.on('connect')(handle_connect)
    app.socketio.on('disconnect')(handle_disconnect)
    app.socketio.on('join_frp_session')(handle_join_session)
    app.socketio.on('leave_session')(handle_leave_session)
    app.socketio.on('chat_message')(handle_chat_message)
    
    # Multiplayer Session Routes
    @app.route('/api/multiplayer/sessions', methods=['POST'])
    def create_session():
        """Create a new multiplayer session"""
        try:
            data = request.get_json()
            name = data.get('name')
            scenario_id = data.get('scenario_id')
            max_players = data.get('max_players', 4)
            creator_id = data.get('creator_id')
            
            if not all([name, scenario_id, creator_id]):
                return jsonify({"error": "Missing required fields"}), 400
            
            # Create session using session manager
            from multiplayer.session_manager import MultiplayerSessionManager
            session_manager = MultiplayerSessionManager()
            
            new_session = session_manager.create_session(
                name=name,
                scenario_id=scenario_id,
                max_players=max_players,
                creator_id=creator_id
            )
            
            return jsonify(session_manager._session_to_dict(new_session)), 201
            
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            return jsonify({"error": "Failed to create session"}), 500
    
    @app.route('/api/multiplayer/sessions/<session_id>/join', methods=['POST'])
    def join_session(session_id):
        """Join a multiplayer session"""
        try:
            data = request.get_json()
            player_id = data.get('player_id')
            username = data.get('username')
            
            if not all([player_id, username]):
                return jsonify({"error": "Missing required fields"}), 400
            
            from multiplayer.session_manager import MultiplayerSessionManager
            session_manager = MultiplayerSessionManager()
            
            result = session_manager.join_session(session_id, player_id, username)
            
            if result["success"]:
                return jsonify(result), 200
            else:
                return jsonify({"error": result["error"]}), 400
                
        except Exception as e:
            logger.error(f"Error joining session: {e}")
            return jsonify({"error": "Failed to join session"}), 500
    
    @app.route('/api/multiplayer/sessions/<session_id>/leave', methods=['POST'])
    def leave_session(session_id):
        """Leave a multiplayer session"""
        try:
            data = request.get_json()
            player_id = data.get('player_id')
            
            if not player_id:
                return jsonify({"error": "Missing player_id"}), 400
            
            from multiplayer.session_manager import MultiplayerSessionManager
            session_manager = MultiplayerSessionManager()
            
            result = session_manager.leave_session(player_id)
            
            if result["success"]:
                return jsonify(result), 200
            else:
                return jsonify({"error": result["error"]}), 400
                
        except Exception as e:
            logger.error(f"Error leaving session: {e}")
            return jsonify({"error": "Failed to leave session"}), 500
    
    @app.route('/api/multiplayer/sessions/<session_id>/start', methods=['POST'])
    def start_session(session_id):
        """Start a multiplayer session"""
        try:
            data = request.get_json()
            creator_id = data.get('creator_id')
            
            if not creator_id:
                return jsonify({"error": "Missing creator_id"}), 400
            
            from multiplayer.session_manager import MultiplayerSessionManager
            session_manager = MultiplayerSessionManager()
            
            result = session_manager.start_session(session_id, creator_id)
            
            if result["success"]:
                return jsonify(result), 200
            else:
                return jsonify({"error": result["error"]}), 400
                
        except Exception as e:
            logger.error(f"Error starting session: {e}")
            return jsonify({"error": "Failed to start session"}), 500
    
    @app.route('/api/multiplayer/lobby/<scenario_id>', methods=['GET'])
    def get_lobby_sessions(scenario_id):
        """Get all lobby sessions for a scenario"""
        try:
            from multiplayer.session_manager import MultiplayerSessionManager
            session_manager = MultiplayerSessionManager()
            
            sessions = session_manager.get_lobby_sessions(scenario_id)
            return jsonify(sessions), 200
            
        except Exception as e:
            logger.error(f"Error getting lobby sessions: {e}")
            return jsonify({"error": "Failed to get lobby sessions"}), 500
    
    @app.route('/api/multiplayer/sessions/<session_id>', methods=['GET'])
    def get_session_info(session_id):
        """Get session information"""
        try:
            from multiplayer.session_manager import MultiplayerSessionManager
            session_manager = MultiplayerSessionManager()
            
            session_info = session_manager.get_session_info(session_id)
            if session_info:
                return jsonify(session_info), 200
            else:
                return jsonify({"error": "Session not found"}), 404
                
        except Exception as e:
            logger.error(f"Error getting session info: {e}")
            return jsonify({"error": "Failed to get session info"}), 500
    
    # Character Management Routes
    @app.route('/api/characters', methods=['POST'])
    def create_character():
        """Create a new character"""
        try:
            data = request.get_json()
            name = data.get('name')
            character_class = data.get('character_class')
            user_id = data.get('user_id')
            
            if not all([name, character_class, user_id]):
                return jsonify({"error": "Missing required fields"}), 400
            
            from core.game_engine import CharacterClass
            char_class = CharacterClass(character_class)
            
            character = game_engine.create_character(name, char_class, user_id)
            
            return jsonify(character.to_dict()), 201
            
        except Exception as e:
            logger.error(f"Error creating character: {e}")
            return jsonify({"error": "Failed to create character"}), 500
    
    @app.route('/api/characters/<character_id>', methods=['GET'])
    def get_character(character_id):
        """Get character information"""
        try:
            character = game_engine.get_character(character_id)
            if character:
                return jsonify(character.to_dict()), 200
            else:
                return jsonify({"error": "Character not found"}), 404
                
        except Exception as e:
            logger.error(f"Error getting character: {e}")
            return jsonify({"error": "Failed to get character"}), 500
    
    @app.route('/api/characters/<character_id>', methods=['PUT'])
    def update_character(character_id):
        """Update character information"""
        try:
            data = request.get_json()
            character = game_engine.get_character(character_id)
            
            if not character:
                return jsonify({"error": "Character not found"}), 404
            
            # Update character fields
            if 'hp' in data:
                character.hp = data['hp']
            if 'mana' in data:
                character.mana = data['mana']
            if 'xp' in data:
                character.gain_xp(data['xp'])
            if 'inventory' in data:
                character.inventory = data['inventory']
            
            # Save character
            game_engine.save_character(character)
            
            return jsonify(character.to_dict()), 200
            
        except Exception as e:
            logger.error(f"Error updating character: {e}")
            return jsonify({"error": "Failed to update character"}), 500

    @app.route('/api/characters/classes', methods=['GET'])
    def get_character_classes():
        """Get all character classes"""
        try:
            # Import character system
            from characters.character_system import CharacterSystem
            char_system = CharacterSystem()
            
            classes = char_system.get_character_classes()
            return jsonify(classes)
            
        except Exception as e:
            logger.error(f"Error getting character classes: {e}")
            return jsonify({'error': 'Failed to get character classes'}), 500

    @app.route('/api/characters/races', methods=['GET'])
    def get_character_races():
        """Get all character races"""
        try:
            # Import character system
            from characters.character_system import CharacterSystem
            char_system = CharacterSystem()
            
            races = char_system.get_character_races()
            return jsonify(races)
            
        except Exception as e:
            logger.error(f"Error getting character races: {e}")
            return jsonify({'error': 'Failed to get character races'}), 500

    @app.route('/api/characters/classes/<theme>', methods=['GET'])
    def get_classes_by_theme(theme):
        """Get character classes by theme (fantasy or warhammer40k)"""
        try:
            from characters.character_system import CharacterSystem
            char_system = CharacterSystem()
            
            classes = char_system.get_classes_by_theme(theme)
            return jsonify(classes)
            
        except Exception as e:
            logger.error(f"Error getting classes by theme: {e}")
            return jsonify({'error': 'Failed to get classes by theme'}), 500

    @app.route('/api/characters/classes/role/<role>', methods=['GET'])
    def get_classes_by_role(role):
        """Get character classes by role (tank, damage_dealer, support, balanced)"""
        try:
            from characters.character_system import CharacterSystem
            char_system = CharacterSystem()
            
            classes = char_system.get_classes_by_role(role)
            return jsonify(classes)
            
        except Exception as e:
            logger.error(f"Error getting classes by role: {e}")
            return jsonify({'error': 'Failed to get classes by role'}), 500

    @app.route('/api/characters/<character_id>/level', methods=['GET'])
    def get_character_level(character_id):
        """Get character level information"""
        try:
            from characters.character_system import CharacterSystem
            char_system = CharacterSystem()
            character = char_system.get_character(character_id)
            if character:
                return jsonify({
                    'level': character.get('level', 1),
                    'xp': character.get('xp', 0),
                    'xp_to_next': character.get('xp_to_next', 100),
                    'skill_points': character.get('skill_points', 0)
                })
            return jsonify({'error': 'Character not found'}), 404
        except Exception as e:
            logger.error(f"Error getting character level: {e}")
            return jsonify({'error': 'Failed to get character level'}), 500

    @app.route('/api/characters/<character_id>/skills', methods=['GET'])
    def get_character_skills(character_id):
        """Get character skills and available skills"""
        try:
            from characters.character_system import CharacterSystem
            char_system = CharacterSystem()
            character = char_system.get_character(character_id)
            if character:
                character_class = character.get('character_class')
                level = character.get('level', 1)
                
                # Load level requirements
                with open('data/level_requirements.json', 'r', encoding='utf-8') as f:
                    level_data = json.load(f)
                
                class_skills = level_data['class_specific_skills'].get(character_class, {})
                available_skills = []
                
                # Add basic skills
                if level >= 2:
                    available_skills.extend(class_skills.get('basic_skills', []))
                
                # Add intermediate skills
                if level >= 4:
                    available_skills.extend(class_skills.get('intermediate_skills', []))
                
                # Add ultimate skills
                if level >= 5:
                    available_skills.extend(class_skills.get('ultimate_skills', []))
                
                return jsonify({
                    'character_class': character_class,
                    'level': level,
                    'available_skills': available_skills,
                    'unlocked_skills': character.get('unlocked_skills', [])
                })
            return jsonify({'error': 'Character not found'}), 404
        except Exception as e:
            logger.error(f"Error getting character skills: {e}")
            return jsonify({'error': 'Failed to get character skills'}), 500

    @app.route('/api/characters/<character_id>/gain_xp', methods=['POST'])
    def gain_character_xp(character_id):
        """Gain XP and check for level up"""
        try:
            data = request.get_json()
            xp_gain = data.get('xp_gain', 0)
            
            from characters.character_system import CharacterSystem
            char_system = CharacterSystem()
            character = char_system.get_character(character_id)
            if character:
                current_xp = character.get('xp', 0)
                current_level = character.get('level', 1)
                
                new_xp = current_xp + xp_gain
                
                # Check for level up
                with open('data/level_requirements.json', 'r', encoding='utf-8') as f:
                    level_data = json.load(f)
                
                level_progression = level_data['level_progression']
                new_level = current_level
                
                for level, requirements in level_progression.items():
                    level_num = int(level)
                    if new_xp >= requirements['xp_required'] and level_num > current_level:
                        new_level = level_num
                
                # Update character
                character['xp'] = new_xp
                character['level'] = new_level
                
                if new_level > current_level:
                    # Level up bonuses
                    level_bonuses = level_progression[str(new_level)]
                    character['hp'] = character.get('hp', 0) + level_bonuses['hp_bonus']
                    character['attack'] = character.get('attack', 0) + level_bonuses['attack_bonus']
                    character['defense'] = character.get('defense', 0) + level_bonuses['defense_bonus']
                    character['special'] = character.get('special', 0) + level_bonuses['special_bonus']
                    character['skill_points'] = character.get('skill_points', 0) + level_bonuses['skill_points']
                
                char_system.save_characters()
                
                return jsonify({
                    'xp_gained': xp_gain,
                    'new_xp': new_xp,
                    'level_up': new_level > current_level,
                    'new_level': new_level,
                    'skill_points': character.get('skill_points', 0)
                })
            return jsonify({'error': 'Character not found'}), 404
        except Exception as e:
            logger.error(f"Error gaining XP: {e}")
            return jsonify({'error': 'Failed to gain XP'}), 500

    @app.route('/api/characters/<character_id>/unlock_skill', methods=['POST'])
    def unlock_character_skill(character_id):
        """Unlock a skill using skill points"""
        try:
            data = request.get_json()
            skill_name = data.get('skill_name')
            
            from characters.character_system import CharacterSystem
            char_system = CharacterSystem()
            character = char_system.get_character(character_id)
            if character:
                skill_points = character.get('skill_points', 0)
                if skill_points > 0:
                    unlocked_skills = character.get('unlocked_skills', [])
                    if skill_name not in unlocked_skills:
                        unlocked_skills.append(skill_name)
                        character['unlocked_skills'] = unlocked_skills
                        character['skill_points'] = skill_points - 1
                        char_system.save_characters()
                        
                        return jsonify({
                            'skill_unlocked': skill_name,
                            'remaining_skill_points': character['skill_points']
                        })
                    else:
                        return jsonify({'error': 'Skill already unlocked'}), 400
                else:
                    return jsonify({'error': 'Not enough skill points'}), 400
            return jsonify({'error': 'Character not found'}), 404
        except Exception as e:
            logger.error(f"Error unlocking skill: {e}")
            return jsonify({'error': 'Failed to unlock skill'}), 500
    
    # Combat System Routes
    @app.route('/api/combat/sessions', methods=['POST'])
    def create_combat_session():
        """Create a new combat session"""
        try:
            data = request.get_json()
            session_id = data.get('session_id')
            participants = data.get('participants', [])
            
            if not session_id:
                return jsonify({"error": "Missing session_id"}), 400
            
            from core.combat_system import AdvancedCombatSystem
            combat_system = AdvancedCombatSystem(session_id)
            
            # Add participants
            for participant_data in participants:
                combat_system.add_participant(participant_data)
            
            # Roll initiative
            initiative_result = combat_system.roll_initiative()
            
            return jsonify({
                "session_id": session_id,
                "initiative": initiative_result,
                "combat_state": combat_system.get_combat_state()
            }), 201
            
        except Exception as e:
            logger.error(f"Error creating combat session: {e}")
            return jsonify({"error": "Failed to create combat session"}), 500
    
    @app.route('/api/combat/sessions/<session_id>/actions', methods=['POST'])
    def process_combat_action(session_id):
        """Process a combat action"""
        try:
            data = request.get_json()
            action = data.get('action')
            
            if not action:
                return jsonify({"error": "Missing action"}), 400
            
            # In real implementation, get combat system from session manager
            from core.combat_system import AdvancedCombatSystem
            combat_system = AdvancedCombatSystem(session_id)
            
            result = combat_system.process_action(action)
            
            return jsonify(result), 200
            
        except Exception as e:
            logger.error(f"Error processing combat action: {e}")
            return jsonify({"error": "Failed to process combat action"}), 500
    
    # Dice Rolling Routes
    @app.route('/api/dice/roll', methods=['POST'])
    def roll_dice():
        """Roll dice"""
        try:
            data = request.get_json()
            dice_notation = data.get('dice_notation', '1d20')
            advantage = data.get('advantage', False)
            disadvantage = data.get('disadvantage', False)
            
            result = game_engine.roll_dice(dice_notation, advantage, disadvantage)
            
            return jsonify(result), 200
            
        except Exception as e:
            logger.error(f"Error rolling dice: {e}")
            return jsonify({"error": "Failed to roll dice"}), 500
    
    # Game State Routes
    @app.route('/api/game/start', methods=['POST'])
    def start_game():
        """Start a new game"""
        try:
            data = request.get_json()
            scenario_id = data.get('scenario_id')
            scenario = data.get('scenario')
            
            if not scenario_id:
                return jsonify({"error": "Missing scenario_id"}), 400
            
            # Initialize game state
            game_state = {
                "scenario_id": scenario_id,
                "scenario": scenario,
                "current_scene": "start",
                "narrative": f"{scenario['title']} oyunu başladı!",
                "available_actions": [
                    {
                        "type": "explore",
                        "description": "Çevreyi keşfet",
                        "diceRoll": {"diceType": "d20", "targetNumber": 15, "skill": "perception"},
                        "consequences": {
                            "success": "Gizli bir geçit buldun!",
                            "failure": "Hiçbir şey bulamadın."
                        }
                    },
                    {
                        "type": "talk",
                        "description": "NPC ile konuş",
                        "diceRoll": {"diceType": "d20", "targetNumber": 12, "skill": "persuasion"},
                        "consequences": {
                            "success": "NPC seninle işbirliği yapmaya hazır!",
                            "failure": "NPC güvenmiyor."
                        }
                    }
                ],
                "player_hp": 100,
                "player_mana": 50,
                "player_xp": 0,
                "player_level": 1
            }
            
            return jsonify(game_state), 200
            
        except Exception as e:
            logger.error(f"Error starting game: {e}")
            return jsonify({"error": "Failed to start game"}), 500
    
    @app.route('/api/game/action', methods=['POST'])
    def process_game_action():
        """Process a game action"""
        try:
            data = request.get_json()
            action = data.get('action')
            dice_result = data.get('dice_result')
            
            if not action:
                return jsonify({"error": "Missing action"}), 400
            
            # Process action and return new game state
            # This would integrate with the AI dungeon master
            response = ai_dm.process_action(action, dice_result)
            
            return jsonify(response), 200
            
        except Exception as e:
            logger.error(f"Error processing game action: {e}")
            return jsonify({"error": "Failed to process action"}), 500
    
    # Scenario Management Routes
    @app.route('/api/scenarios', methods=['GET'])
    def get_scenarios():
        """Get all available scenarios"""
        try:
            # Mock scenarios for now
            scenarios = [
                {
                    "id": "1",
                    "title": "🐉 Ejderha Mağarası",
                    "theme": "fantasy",
                    "difficulty": "medium",
                    "description": "Bir ejderha mağarasında gizli hazine arayışı",
                    "isFavorite": False,
                    "createdAt": "2024-01-01T00:00:00Z",
                    "tags": ["fantasy", "dragon", "treasure"]
                },
                {
                    "id": "2",
                    "title": "🛡️ Space Marine Görevi",
                    "theme": "warhammer",
                    "difficulty": "hard",
                    "description": "Ork istilasını durdurmak için Space Marine görevi",
                    "isFavorite": True,
                    "createdAt": "2024-01-01T00:00:00Z",
                    "tags": ["warhammer", "space-marine", "ork"]
                }
            ]
            
            return jsonify(scenarios), 200
            
        except Exception as e:
            logger.error(f"Error getting scenarios: {e}")
            return jsonify({"error": "Failed to get scenarios"}), 500
    
    @app.route('/api/scenarios/<scenario_id>/favorite', methods=['POST'])
    def toggle_favorite(scenario_id):
        """Toggle favorite status for a scenario"""
        try:
            # Mock implementation
            is_favorite = True  # This would be stored in database
            
            return jsonify({"isFavorite": is_favorite}), 200
            
        except Exception as e:
            logger.error(f"Error toggling favorite: {e}")
            return jsonify({"error": "Failed to toggle favorite"}), 500
    
    # Scenario generation removed - only predefined scenarios are available
    
    # WebSocket event handlers
    def handle_connect(sid, environ):
        """Handle WebSocket connection"""
        logger.info(f"Client connected: {sid}")
        emit('connected', {'sid': sid})
    
    def handle_disconnect(sid):
        """Handle WebSocket disconnection"""
        logger.info(f"Client disconnected: {sid}")
    
    def handle_join_session(sid, data):
        """Handle join session WebSocket event"""
        try:
            session_id = data.get('session_id')
            player_id = data.get('player_id')
            username = data.get('username')
            
            if not all([session_id, player_id, username]):
                emit('error', {'message': 'Missing required fields'})
                return
            
            # Join room for session
            join_room(session_id)
            
            # Notify other players in session
            emit('player_joined', {
                'player_id': player_id,
                'username': username
            }, room=session_id, include_self=False)
            
            emit('success', {'message': 'Joined session successfully'})
            
        except Exception as e:
            logger.error(f"Error handling join session: {e}")
            emit('error', {'message': 'Failed to join session'})
    
    def handle_leave_session(sid, data):
        """Handle leave session WebSocket event"""
        try:
            session_id = data.get('session_id')
            player_id = data.get('player_id')
            
            if not all([session_id, player_id]):
                emit('error', {'message': 'Missing required fields'})
                return
            
            # Leave room
            leave_room(session_id)
            
            # Notify other players
            emit('player_left', {
                'player_id': player_id
            }, room=session_id, include_self=False)
            
            emit('success', {'message': 'Left session successfully'})
            
        except Exception as e:
            logger.error(f"Error handling leave session: {e}")
            emit('error', {'message': 'Failed to leave session'})
    
    def handle_chat_message(sid, data):
        """Handle chat message WebSocket event"""
        try:
            session_id = data.get('session_id')
            player_id = data.get('player_id')
            message = data.get('message')
            
            if not all([session_id, player_id, message]):
                emit('error', {'message': 'Missing required fields'})
                return
            
            # Broadcast message to session
            emit('chat_message', {
                'player_id': player_id,
                'message': message,
                'timestamp': '2024-01-01T00:00:00Z'
            }, room=session_id)
            
        except Exception as e:
            logger.error(f"Error handling chat message: {e}")
            emit('error', {'message': 'Failed to send chat message'})
    
    # Register WebSocket events
    app.socketio.on('connect', handle_connect)
    app.socketio.on('disconnect', handle_disconnect)
    app.socketio.on('join_session', handle_join_session)
    app.socketio.on('leave_session', handle_leave_session)
    app.socketio.on('chat_message', handle_chat_message)
    
    # Save/Load System Routes
    @app.route('/api/save/game', methods=['POST'])
    def save_game():
        """Save game state"""
        try:
            data = request.get_json()
            character_id = data.get('character_id')
            save_name = data.get('save_name', 'Manual Save')
            
            if not character_id:
                return jsonify({"error": "Missing character_id"}), 400
            
            from core.save_system import SaveSystem
            save_system = SaveSystem()
            
            result = save_system.save_game(
                character_id=character_id,
                game_engine=game_engine,
                campaign_manager=campaign_manager
            )
            
            return jsonify(result), 200 if result["success"] else 400
            
        except Exception as e:
            logger.error(f"Error saving game: {e}")
            return jsonify({"error": "Failed to save game"}), 500
    
    @app.route('/api/save/load', methods=['POST'])
    def load_game():
        """Load game state"""
        try:
            data = request.get_json()
            save_id = data.get('save_id')
            
            if not save_id:
                return jsonify({"error": "Missing save_id"}), 400
            
            from core.save_system import SaveSystem
            save_system = SaveSystem()
            
            result = save_system.load_game(
                save_id=save_id,
                game_engine=game_engine,
                campaign_manager=campaign_manager
            )
            
            return jsonify(result), 200 if result["success"] else 400
            
        except Exception as e:
            logger.error(f"Error loading game: {e}")
            return jsonify({"error": "Failed to load game"}), 500
    
    @app.route('/api/save/files', methods=['GET'])
    def get_save_files():
        """Get list of save files"""
        try:
            character_id = request.args.get('character_id')
            
            from core.save_system import SaveSystem
            save_system = SaveSystem()
            
            save_files = save_system.get_save_files(character_id)
            
            return jsonify(save_files), 200
            
        except Exception as e:
            logger.error(f"Error getting save files: {e}")
            return jsonify({"error": "Failed to get save files"}), 500
    
    @app.route('/api/save/delete', methods=['DELETE'])
    def delete_save():
        """Delete a save file"""
        try:
            data = request.get_json()
            save_id = data.get('save_id')
            
            if not save_id:
                return jsonify({"error": "Missing save_id"}), 400
            
            from core.save_system import SaveSystem
            save_system = SaveSystem()
            
            result = save_system.delete_save(save_id)
            
            return jsonify(result), 200 if result["success"] else 400
            
        except Exception as e:
            logger.error(f"Error deleting save: {e}")
            return jsonify({"error": "Failed to delete save"}), 500
    
    @app.route('/api/save/auto', methods=['POST'])
    def auto_save():
        """Create auto-save"""
        try:
            data = request.get_json()
            character_id = data.get('character_id')
            
            if not character_id:
                return jsonify({"error": "Missing character_id"}), 400
            
            from core.save_system import SaveSystem
            save_system = SaveSystem()
            
            result = save_system.auto_save(
                character_id=character_id,
                game_engine=game_engine,
                campaign_manager=campaign_manager
            )
            
            return jsonify(result), 200 if result["success"] else 400
            
        except Exception as e:
            logger.error(f"Error creating auto-save: {e}")
            return jsonify({"error": "Failed to create auto-save"}), 500
    
    logger.info("All routes registered successfully") 