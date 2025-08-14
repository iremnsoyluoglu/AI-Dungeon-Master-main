#!/usr/bin/env python3
"""
Multiplayer Session Manager
==========================

Comprehensive multiplayer system with collaborative actions, team mechanics,
and real-time session management.
"""

import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from enum import Enum
from dataclasses import dataclass, asdict

class SessionStatus(Enum):
    LOBBY = "lobby"
    IN_GAME = "in_game"
    COMBAT = "combat"
    PAUSED = "paused"
    ENDED = "ended"

class PlayerRole(Enum):
    PLAYER = "player"
    GAME_MASTER = "game_master"
    SPECTATOR = "spectator"

@dataclass
class Player:
    id: str
    username: str
    role: PlayerRole
    character_id: Optional[str] = None
    joined_at: Optional[str] = None
    last_activity: Optional[str] = None
    is_ready: bool = False
    is_online: bool = True

@dataclass
class Team:
    id: str
    name: str
    players: List[str]
    leader_id: Optional[str] = None
    created_at: str = None
    color: str = "#4CAF50"

class MultiplayerSessionManager:
    """Comprehensive multiplayer session management system"""
    
    def __init__(self):
        self.sessions_file = "data/multiplayer_sessions.json"
        self._ensure_data_directory()
        self._load_sessions()
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs("data", exist_ok=True)
    
    def _load_sessions(self):
        """Load multiplayer sessions"""
        try:
            if os.path.exists(self.sessions_file):
                with open(self.sessions_file, 'r', encoding='utf-8') as f:
                    self.sessions = json.load(f)
            else:
                self.sessions = {}
        except Exception as e:
            print(f"Error loading multiplayer sessions: {e}")
            self.sessions = {}
    
    def _save_sessions(self):
        """Save multiplayer sessions"""
        try:
            with open(self.sessions_file, 'w', encoding='utf-8') as f:
                json.dump(self.sessions, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving multiplayer sessions: {e}")
    
    def create_session(self, creator_id: str, session_name: str, scenario_id: str, max_players: int = 6) -> Dict[str, Any]:
        """Create a new multiplayer session"""
        try:
            session_id = str(uuid.uuid4())
            now = datetime.now().isoformat()
            
            session_data = {
                "id": session_id,
                "name": session_name,
                "scenario_id": scenario_id,
                "creator_id": creator_id,
                "max_players": max_players,
                "status": SessionStatus.LOBBY.value,
                "players": [],
                "teams": [],
                "game_state": {
                    "current_scene": "lobby",
                    "combat_state": None,
                    "shared_inventory": [],
                    "team_actions": [],
                    "collaborative_quests": []
                },
                "settings": {
                    "allow_pvp": False,
                    "shared_exp": True,
                    "team_based": True,
                    "voice_chat": False
                },
                "created_at": now,
                "last_updated": now,
                "started_at": None,
                "ended_at": None
            }
            
            # Add creator as game master
            creator_player = Player(
                id=creator_id,
                username=f"GM_{creator_id[:8]}",
                role=PlayerRole.GAME_MASTER,
                joined_at=now,
                last_activity=now,
                is_ready=True
            )
            
            session_data["players"].append(asdict(creator_player))
            self.sessions[session_id] = session_data
            self._save_sessions()
            
            return {
                "success": True,
                "session_id": session_id,
                "session": session_data,
                "message": f"Created multiplayer session: {session_name}"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error creating session: {str(e)}"}
    
    def join_session(self, session_id: str, player_id: str, username: str, character_id: Optional[str] = None) -> Dict[str, Any]:
        """Join a multiplayer session"""
        try:
            if session_id not in self.sessions:
                return {"success": False, "error": "Session not found"}
            
            session = self.sessions[session_id]
            
            # Check if session is full
            if len(session["players"]) >= session["max_players"]:
                return {"success": False, "error": "Session is full"}
            
            # Check if player is already in session
            for player in session["players"]:
                if player["id"] == player_id:
                    return {"success": False, "error": "Already in session"}
            
            # Check if session is joinable
            if session["status"] != SessionStatus.LOBBY.value:
                return {"success": False, "error": "Session is not accepting new players"}
            
            now = datetime.now().isoformat()
            
            # Create new player
            new_player = Player(
                id=player_id,
                username=username,
                role=PlayerRole.PLAYER,
                character_id=character_id,
                joined_at=now,
                last_activity=now,
                is_ready=False
            )
            
            session["players"].append(asdict(new_player))
            session["last_updated"] = now
            self._save_sessions()
            
            return {
                "success": True,
                "session_id": session_id,
                "player_id": player_id,
                "message": f"Joined session: {session['name']}"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error joining session: {str(e)}"}
    
    def leave_session(self, session_id: str, player_id: str) -> Dict[str, Any]:
        """Leave a multiplayer session"""
        try:
            if session_id not in self.sessions:
                return {"success": False, "error": "Session not found"}
            
            session = self.sessions[session_id]
            
            # Find and remove player
            player_removed = False
            for i, player in enumerate(session["players"]):
                if player["id"] == player_id:
                    session["players"].pop(i)
                    player_removed = True
                    break
            
            if not player_removed:
                return {"success": False, "error": "Player not found in session"}
            
            # Remove player from teams
            for team in session["teams"]:
                if player_id in team["players"]:
                    team["players"].remove(player_id)
                    if team["leader_id"] == player_id:
                        team["leader_id"] = team["players"][0] if team["players"] else None
            
            session["last_updated"] = datetime.now().isoformat()
            
            # If no players left, end session
            if len(session["players"]) == 0:
                session["status"] = SessionStatus.ENDED.value
                session["ended_at"] = datetime.now().isoformat()
            
            self._save_sessions()
            
            return {
                "success": True,
                "session_id": session_id,
                "player_id": player_id,
                "message": "Left session"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error leaving session: {str(e)}"}
    
    def create_team(self, session_id: str, team_name: str, leader_id: str, player_ids: List[str]) -> Dict[str, Any]:
        """Create a team within a session"""
        try:
            if session_id not in self.sessions:
                return {"success": False, "error": "Session not found"}
            
            session = self.sessions[session_id]
            
            # Check if players are in session
            session_player_ids = [p["id"] for p in session["players"]]
            for player_id in player_ids:
                if player_id not in session_player_ids:
                    return {"success": False, "error": f"Player {player_id} not in session"}
            
            # Check if players are already in teams
            for team in session["teams"]:
                for player_id in player_ids:
                    if player_id in team["players"]:
                        return {"success": False, "error": f"Player {player_id} already in team"}
            
            team_id = str(uuid.uuid4())
            now = datetime.now().isoformat()
            
            new_team = Team(
                id=team_id,
                name=team_name,
                players=player_ids,
                leader_id=leader_id,
                created_at=now,
                color="#4CAF50"
            )
            
            session["teams"].append(asdict(new_team))
            session["last_updated"] = now
            self._save_sessions()
            
            return {
                "success": True,
                "team_id": team_id,
                "team": asdict(new_team),
                "message": f"Created team: {team_name}"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error creating team: {str(e)}"}
    
    def perform_team_action(self, session_id: str, team_id: str, action: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a collaborative team action"""
        try:
            if session_id not in self.sessions:
                return {"success": False, "error": "Session not found"}
            
            session = self.sessions[session_id]
            
            # Find team
            team = None
            for t in session["teams"]:
                if t["id"] == team_id:
                    team = t
                    break
            
            if not team:
                return {"success": False, "error": "Team not found"}
            
            # Validate action
            action_type = action.get("type")
            if not action_type:
                return {"success": False, "error": "Invalid action"}
            
            # Process team action
            action_result = self._process_team_action(session, team, action)
            
            # Add to team actions history
            team_action_record = {
                "id": str(uuid.uuid4()),
                "team_id": team_id,
                "action": action,
                "result": action_result,
                "timestamp": datetime.now().isoformat(),
                "participants": team["players"]
            }
            
            session["game_state"]["team_actions"].append(team_action_record)
            session["last_updated"] = datetime.now().isoformat()
            self._save_sessions()
            
            return {
                "success": True,
                "team_id": team_id,
                "action": action,
                "result": action_result,
                "message": f"Team action performed: {action_type}"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error performing team action: {str(e)}"}
    
    def _process_team_action(self, session: Dict[str, Any], team: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
        """Process a team action and return results"""
        action_type = action.get("type")
        participants = action.get("participants", team["players"])
        
        # Calculate team bonuses based on team size and coordination
        team_size = len(participants)
        coordination_bonus = min(team_size * 0.2, 1.0)  # Max 100% bonus for 5+ players
        
        if action_type == "combat":
            # Collaborative combat action
            total_damage = 0
            for player_id in participants:
                # Get player stats (simplified)
                player_stats = {"attack": 10, "defense": 5}
                damage = player_stats["attack"] * (1 + coordination_bonus)
                total_damage += damage
            
            return {
                "type": "combat",
                "damage_dealt": total_damage,
                "team_bonus": coordination_bonus,
                "participants": participants
            }
        
        elif action_type == "exploration":
            # Collaborative exploration
            discovery_chance = 0.3 + (coordination_bonus * 0.3)
            items_found = []
            
            # Simulate exploration results
            import random
            if random.random() < discovery_chance:
                items_found = ["treasure_chest", "ancient_relic"]
            
            return {
                "type": "exploration",
                "discovery_chance": discovery_chance,
                "items_found": items_found,
                "participants": participants
            }
        
        elif action_type == "social":
            # Collaborative social interaction
            persuasion_bonus = coordination_bonus * 2
            return {
                "type": "social",
                "persuasion_bonus": persuasion_bonus,
                "success_rate": 0.5 + persuasion_bonus,
                "participants": participants
            }
        
        else:
            return {
                "type": "generic",
                "success": True,
                "team_bonus": coordination_bonus,
                "participants": participants
            }
    
    def get_session_state(self, session_id: str) -> Dict[str, Any]:
        """Get current session state"""
        if session_id not in self.sessions:
            return {"success": False, "error": "Session not found"}
        
        session = self.sessions[session_id]
        
        # Calculate session statistics
        player_count = len(session["players"])
        team_count = len(session["teams"])
        online_players = sum(1 for p in session["players"] if p.get("is_online", True))
        
        return {
            "success": True,
            "session_id": session_id,
            "session": session,
            "statistics": {
                "player_count": player_count,
                "team_count": team_count,
                "online_players": online_players,
                "max_players": session["max_players"]
            }
        }
    
    def get_available_sessions(self) -> List[Dict[str, Any]]:
        """Get list of available multiplayer sessions"""
        available_sessions = []
        
        for session_id, session in self.sessions.items():
            if session["status"] == SessionStatus.LOBBY.value:
                player_count = len(session["players"])
                
                available_sessions.append({
                    "id": session_id,
                    "name": session["name"],
                    "scenario_id": session["scenario_id"],
                    "player_count": player_count,
                    "max_players": session["max_players"],
                    "created_at": session["created_at"],
                    "settings": session["settings"]
                })
        
        return available_sessions
    
    def update_player_activity(self, session_id: str, player_id: str) -> bool:
        """Update player's last activity time"""
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        now = datetime.now().isoformat()
        
        for player in session["players"]:
            if player["id"] == player_id:
                player["last_activity"] = now
                break
        
        session["last_updated"] = now
        self._save_sessions()
        return True
    
    def cleanup_inactive_sessions(self, max_inactive_hours: int = 24) -> int:
        """Clean up inactive sessions"""
        now = datetime.now()
        cleanup_count = 0
        
        sessions_to_remove = []
        
        for session_id, session in self.sessions.items():
            last_updated = datetime.fromisoformat(session["last_updated"])
            if now - last_updated > timedelta(hours=max_inactive_hours):
                sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            del self.sessions[session_id]
            cleanup_count += 1
        
        if cleanup_count > 0:
            self._save_sessions()
        
        return cleanup_count 