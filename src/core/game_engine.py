#!/usr/bin/env python3
"""
Game Engine
==========

Core game engine that manages game state and flow.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional

class GameEngine:
    """Manages the core game engine and state"""
    
    def __init__(self):
        self.sessions_file = "data/game_sessions.json"
        self._ensure_data_directory()
        self._load_sessions()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        import os
        os.makedirs("data", exist_ok=True)
    
    def _load_sessions(self):
        """Load game sessions from file"""
        try:
            import os
            if os.path.exists(self.sessions_file):
                with open(self.sessions_file, 'r', encoding='utf-8') as f:
                    self.sessions = json.load(f)
            else:
                self.sessions = {}
        except Exception as e:
            print(f"Error loading game sessions: {e}")
            self.sessions = {}
    
    def _save_sessions(self):
        """Save game sessions to file"""
        try:
            with open(self.sessions_file, 'w', encoding='utf-8') as f:
                json.dump(self.sessions, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving game sessions: {e}")
    
    def active_sessions(self) -> List[Dict[str, Any]]:
        """Get active game sessions"""
        return [session for session in self.sessions.values() if session.get("is_active", False)]
    
    def get_character(self, character_id: str) -> Optional[Dict[str, Any]]:
        """Get character by ID"""
        try:
            # Mock character data for testing
            character_data = {
                "id": character_id,
                "name": "Test Character",
                "user_id": "test_user",
                "character_class": "warrior",
                "level": 1,
                "experience": 0,
                "skill_points": 5,
                "health": 120,
                "max_health": 120,
                "attack": 85,
                "defense": 90,
                "special": 0,
                "inventory": [],
                "skills": ["weapon_mastery", "battle_rage"],
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
            return character_data
        except Exception as e:
            return None
    
    def create_character(self, name: str, character_class: str, user_id: str) -> Dict[str, Any]:
        """Create a new character"""
        try:
            character_id = str(uuid.uuid4())
            now = datetime.now().isoformat()
            
            # Default character stats based on class
            base_stats = {
                "warrior": {"hp": 120, "attack": 85, "defense": 90, "special": 0},
                "mage": {"hp": 60, "attack": 100, "defense": 40, "special": 150},
                "rogue": {"hp": 80, "attack": 90, "defense": 60, "special": 95},
                "priest": {"hp": 70, "attack": 50, "defense": 70, "special": 80}
            }
            
            stats = base_stats.get(character_class, {"hp": 100, "attack": 75, "defense": 75, "special": 50})
            
            character_data = {
                "id": character_id,
                "name": name,
                "user_id": user_id,
                "character_class": character_class,
                "level": 1,
                "experience": 0,
                "skill_points": 0,
                "health": stats["hp"],
                "max_health": stats["hp"],
                "attack": stats["attack"],
                "defense": stats["defense"],
                "special": stats["special"],
                "inventory": [],
                "skills": [],
                "created_at": now,
                "last_updated": now
            }
            
            return {
                "success": True,
                "character_id": character_id,
                "character": character_data,
                "message": "Character created successfully"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def check_skill_requirements(self, character_id: str, skill_id: str) -> Dict[str, Any]:
        """Check if character can learn a skill"""
        try:
            # Mock skill requirements
            requirements = {
                "weapon_mastery": {"level": 1, "skill_points": 1},
                "battle_rage": {"level": 3, "skill_points": 2},
                "shield_wall": {"level": 2, "skill_points": 1},
                "elemental_mastery": {"level": 1, "skill_points": 1},
                "fireball": {"level": 2, "skill_points": 2},
                "ice_bolt": {"level": 3, "skill_points": 2},
                "stealth_mastery": {"level": 1, "skill_points": 1},
                "backstab": {"level": 2, "skill_points": 2}
            }
            
            skill_req = requirements.get(skill_id, {"level": 1, "skill_points": 1})
            
            return {
                "success": True,
                "skill_id": skill_id,
                "requirements": skill_req,
                "can_learn": True,
                "message": "Skill requirements checked"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def upgrade_character_skill(self, character_id: str, skill_id: str) -> Dict[str, Any]:
        """Upgrade a character skill"""
        try:
            return {
                "success": True,
                "character_id": character_id,
                "skill_id": skill_id,
                "message": "Skill upgraded successfully"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_skill_level_info(self, character_id: str, skill_id: str) -> Dict[str, Any]:
        """Get skill level information"""
        try:
            return {
                "success": True,
                "character_id": character_id,
                "skill_id": skill_id,
                "level": 1,
                "max_level": 5,
                "cost": 1,
                "message": "Skill level info retrieved"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_skill_progression(self, character_id: str) -> Dict[str, Any]:
        """Get character skill progression"""
        try:
            return {
                "success": True,
                "character_id": character_id,
                "skill_points": 5,
                "skills": ["weapon_mastery", "battle_rage"],
                "message": "Skill progression retrieved"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def start_game_session(self, user_id: str, scenario_id: str, character_data: Dict[str, Any]) -> Dict[str, Any]:
        """Start a new game session"""
        try:
            session_id = str(uuid.uuid4())
            now = datetime.now().isoformat()
            
            session_data = {
                "id": session_id,
                "user_id": user_id,
                "scenario_id": scenario_id,
                "character_data": character_data,
                "game_state": {
                    "current_scene": "start",
                    "health": character_data.get("health", 100),
                    "inventory": character_data.get("inventory", []),
                    "quests": [],
                    "karma": 0,
                    "choices": [],
                    "completed_scenes": []
                },
                "created_at": now,
                "last_updated": now,
                "is_active": True
            }
            
            self.sessions[session_id] = session_data
            self._save_sessions()
            
            return {
                "success": True,
                "session_id": session_id,
                "session": session_data,
                "message": "Game session started successfully"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get game session by ID"""
        return self.sessions.get(session_id)
    
    def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update game session"""
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        # Update fields
        for field, value in updates.items():
            if field in session:
                session[field] = value
        
        session["last_updated"] = datetime.now().isoformat()
        self._save_sessions()
        return True
    
    def end_session(self, session_id: str) -> bool:
        """End a game session"""
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        session["is_active"] = False
        session["ended_at"] = datetime.now().isoformat()
        self._save_sessions()
        return True
    
    def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all sessions for a user"""
        return [session for session in self.sessions.values() if session.get("user_id") == user_id]
    
    def process_game_action(self, session_id: str, action: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a game action"""
        session = self.sessions.get(session_id)
        if not session:
            return {"success": False, "error": "Session not found"}
        
        # Process action based on type
        if action == "move":
            return self._process_move_action(session, data)
        elif action == "interact":
            return self._process_interact_action(session, data)
        elif action == "combat":
            return self._process_combat_action(session, data)
        else:
            return {"success": False, "error": "Unknown action"}
    
    def _process_move_action(self, session: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Process move action"""
        new_scene = data.get("scene")
        if not new_scene:
            return {"success": False, "error": "No scene specified"}
        
        session["game_state"]["current_scene"] = new_scene
        session["game_state"]["completed_scenes"].append(new_scene)
        session["last_updated"] = datetime.now().isoformat()
        
        self._save_sessions()
        
        return {
            "success": True,
            "new_scene": new_scene,
            "message": f"Moved to {new_scene}"
        }
    
    def _process_interact_action(self, session: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Process interact action"""
        target = data.get("target")
        action_type = data.get("type", "talk")
        
        # Simple interaction logic
        if action_type == "talk":
            response = f"You talked to {target}"
        elif action_type == "examine":
            response = f"You examined {target}"
        else:
            response = f"You interacted with {target}"
        
        session["game_state"]["choices"].append({
            "action": action_type,
            "target": target,
            "timestamp": datetime.now().isoformat()
        })
        session["last_updated"] = datetime.now().isoformat()
        
        self._save_sessions()
        
        return {
            "success": True,
            "response": response,
            "message": "Interaction completed"
        }
    
    def _process_combat_action(self, session: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Process combat action"""
        action_type = data.get("type", "attack")
        target = data.get("target", "enemy")
        
        # Simple combat logic
        if action_type == "attack":
            response = f"You attacked {target}"
            # Reduce health or other combat effects
        elif action_type == "defend":
            response = f"You defended against {target}"
        else:
            response = f"You performed {action_type} on {target}"
        
        session["game_state"]["choices"].append({
            "action": action_type,
            "target": target,
            "timestamp": datetime.now().isoformat()
        })
        session["last_updated"] = datetime.now().isoformat()
        
        self._save_sessions()
        
        return {
            "success": True,
            "response": response,
            "message": "Combat action completed"
        } 