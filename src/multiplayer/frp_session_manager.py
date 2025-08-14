#!/usr/bin/env python3
"""
FRP Session Manager - Real FRP Gameplay
=======================================

Handles real FRP gameplay where:
- AI acts as Dungeon Master
- Players take turns making decisions
- Group combat with initiative
- Collaborative storytelling
- Real-time narrative updates
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import random

logger = logging.getLogger(__name__)

class PlayerRole(Enum):
    PLAYER = "player"
    DM = "dm"  # AI acts as DM

class TurnPhase(Enum):
    NARRATIVE = "narrative"      # DM describes situation
    PLAYER_DECISION = "player_decision"  # Players make choices
    COMBAT = "combat"           # Combat phase
    RESOLUTION = "resolution"   # Resolve actions

class PlayerAction(Enum):
    EXPLORE = "explore"
    TALK = "talk"
    ATTACK = "attack"
    CAST_SPELL = "cast_spell"
    USE_ITEM = "use_item"
    STEALTH = "stealth"
    INVESTIGATE = "investigate"
    PERSUADE = "persuade"
    INTIMIDATE = "intimidate"

@dataclass
class FRPPlayer:
    id: str
    username: str
    character_id: Optional[str]
    character_name: str
    character_class: str
    hp: int
    max_hp: int
    mana: int
    max_mana: int
    level: int
    xp: int
    initiative: int
    is_current_turn: bool
    is_alive: bool
    status_effects: List[str]
    position: Tuple[int, int] = (0, 0)

@dataclass
class GameState:
    session_id: str
    scenario_id: str
    current_phase: TurnPhase
    current_narrative: str
    available_actions: List[Dict]
    current_player_turn: Optional[str]
    round_number: int
    combat_active: bool
    enemies: List[Dict]
    environment: Dict
    quest_progress: Dict
    group_inventory: List[str]

class FRPSessionManager:
    """Manages real FRP gameplay sessions with AI DM"""
    
    def __init__(self):
        self.active_sessions: Dict[str, 'FRPSession'] = {}
        self.ai_dm = None  # Will be initialized with AI DM
        self.scenario_templates = self._load_scenario_templates()
    
    def create_frp_session(self, session_id: str, scenario_id: str, 
                          max_players: int = 6) -> 'FRPSession':
        """Create a new FRP session with AI DM"""
        session = FRPSession(
            session_id=session_id,
            scenario_id=scenario_id,
            max_players=max_players,
            ai_dm=self.ai_dm
        )
        self.active_sessions[session_id] = session
        logger.info(f"Created FRP session: {session_id}")
        return session
    
    def join_frp_session(self, session_id: str, player_data: Dict) -> Dict[str, Any]:
        """Join an FRP session as a player"""
        if session_id not in self.active_sessions:
            return {"success": False, "error": "Session not found"}
        
        session = self.active_sessions[session_id]
        return session.add_player(player_data)
    
    def get_session_state(self, session_id: str) -> Optional[GameState]:
        """Get current game state for a session"""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        return session.get_game_state()
    
    def process_player_action(self, session_id: str, player_id: str, 
                            action: Dict) -> Dict[str, Any]:
        """Process a player action in the FRP session"""
        if session_id not in self.active_sessions:
            return {"success": False, "error": "Session not found"}
        
        session = self.active_sessions[session_id]
        return session.process_player_action(player_id, action)
    
    def _load_scenario_templates(self) -> Dict[str, Any]:
        """Load scenario templates for AI DM"""
        return {
            "fantasy_dragon": {
                "title": "🐉 Ejderha Mağarası",
                "description": "Bir ejderha mağarasında gizli hazine arayışı",
                "starting_narrative": "Kasvetli bir mağaranın girişindesiniz. İçeriden garip sesler geliyor...",
                "enemies": ["goblin", "orc", "dragon"],
                "npcs": ["wise_old_man", "merchant", "captive_princess"],
                "locations": ["cave_entrance", "treasure_room", "dragon_lair"],
                "quests": ["find_treasure", "rescue_princess", "slay_dragon"]
            },
            "warhammer_mission": {
                "title": "🛡️ Space Marine Görevi",
                "description": "Ork istilasını durdurmak için Space Marine görevi",
                "starting_narrative": "Ork istilası tehdidi altındaki bir dünyadasınız. İmperium'u korumak sizin elinizde...",
                "enemies": ["ork_boy", "ork_nob", "ork_warboss"],
                "npcs": ["imperial_commander", "tech_priest", "inquisitor"],
                "locations": ["imperial_base", "ork_camp", "ancient_ruins"],
                "quests": ["defend_base", "eliminate_warboss", "recover_artifact"]
            }
        }

class FRPSession:
    """Individual FRP session with AI DM and players"""
    
    def __init__(self, session_id: str, scenario_id: str, max_players: int, ai_dm):
        self.session_id = session_id
        self.scenario_id = scenario_id
        self.max_players = max_players
        self.ai_dm = ai_dm
        
        # Players
        self.players: Dict[str, FRPPlayer] = {}
        self.player_order: List[str] = []
        self.current_player_index = 0
        
        # Game state
        self.game_state = GameState(
            session_id=session_id,
            scenario_id=scenario_id,
            current_phase=TurnPhase.NARRATIVE,
            current_narrative="",
            available_actions=[],
            current_player_turn=None,
            round_number=1,
            combat_active=False,
            enemies=[],
            environment={},
            quest_progress={},
            group_inventory=[]
        )
        
        # Combat state
        self.combat_round = 1
        self.initiative_order = []
        self.combat_log = []
        
        # Session state
        self.is_active = True
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        
        # Initialize scenario
        self._initialize_scenario()
    
    def _initialize_scenario(self):
        """Initialize the scenario with AI DM"""
        # Load scenario template
        scenario_templates = {
            "fantasy_dragon": {
                "title": "🐉 Ejderha Mağarası",
                "starting_narrative": "Kasvetli bir mağaranın girişindesiniz. İçeriden garip sesler geliyor ve hava ağır bir kükürt kokusuyla dolu. Mağaranın derinliklerinden gelen bir ışık huzmesi, hazine odasına işaret ediyor gibi görünüyor.",
                "available_actions": [
                    {"type": "explore", "description": "Mağarayı keşfet", "dice": "1d20", "skill": "perception"},
                    {"type": "talk", "description": "Sesleri dinle", "dice": "1d20", "skill": "investigation"},
                    {"type": "stealth", "description": "Gizlice ilerle", "dice": "1d20", "skill": "stealth"}
                ]
            },
            "warhammer_mission": {
                "title": "🛡️ Space Marine Görevi", 
                "starting_narrative": "Ork istilası tehdidi altındaki bir dünyadasınız. İmperium'u korumak sizin elinizde. Uzaktan ork savaş çığlıkları duyuluyor ve gökyüzü dumanla kaplı.",
                "available_actions": [
                    {"type": "investigate", "description": "Çevreyi araştır", "dice": "1d20", "skill": "investigation"},
                    {"type": "attack", "description": "Ork'lara saldır", "dice": "1d20", "skill": "combat"},
                    {"type": "persuade", "description": "Yerel halkla konuş", "dice": "1d20", "skill": "persuasion"}
                ]
            }
        }
        
        scenario = scenario_templates.get(self.scenario_id, scenario_templates["fantasy_dragon"])
        
        self.game_state.current_narrative = scenario["starting_narrative"]
        self.game_state.available_actions = scenario["available_actions"]
        
        logger.info(f"Initialized scenario: {scenario['title']}")
    
    def add_player(self, player_data: Dict) -> Dict[str, Any]:
        """Add a player to the FRP session"""
        if len(self.players) >= self.max_players:
            return {"success": False, "error": "Session is full"}
        
        player_id = player_data["id"]
        username = player_data["username"]
        
        # Create FRP player
        frp_player = FRPPlayer(
            id=player_id,
            username=username,
            character_id=player_data.get("character_id"),
            character_name=player_data.get("character_name", username),
            character_class=player_data.get("character_class", "warrior"),
            hp=player_data.get("hp", 100),
            max_hp=player_data.get("max_hp", 100),
            mana=player_data.get("mana", 50),
            max_mana=player_data.get("max_mana", 50),
            level=player_data.get("level", 1),
            xp=player_data.get("xp", 0),
            initiative=0,
            is_current_turn=False,
            is_alive=True,
            status_effects=[]
        )
        
        self.players[player_id] = frp_player
        self.player_order.append(player_id)
        
        # Set first player as current turn
        if len(self.players) == 1:
            self.current_player_index = 0
            frp_player.is_current_turn = True
            self.game_state.current_player_turn = player_id
        
        logger.info(f"Player {username} joined session {self.session_id}")
        
        return {
            "success": True,
            "player_id": player_id,
            "game_state": self.get_game_state()
        }
    
    def process_player_action(self, player_id: str, action: Dict) -> Dict[str, Any]:
        """Process a player action and advance the game"""
        if player_id not in self.players:
            return {"success": False, "error": "Player not in session"}
        
        player = self.players[player_id]
        
        # Check if it's player's turn
        if not player.is_current_turn:
            return {"success": False, "error": "Not your turn"}
        
        action_type = action.get("type")
        action_description = action.get("description", "")
        dice_result = action.get("dice_result")
        
        # Process the action
        result = self._process_action(player, action_type, action_description, dice_result)
        
        # Advance to next player
        self._advance_turn()
        
        # Update game state
        self._update_game_state()
        
        return {
            "success": True,
            "action_result": result,
            "game_state": self.get_game_state(),
            "next_player": self._get_current_player().username if self._get_current_player() else None
        }
    
    def _process_action(self, player: FRPPlayer, action_type: str, 
                       description: str, dice_result: Optional[int]) -> Dict[str, Any]:
        """Process a specific action"""
        
        # Determine action outcome based on dice result
        success = dice_result and dice_result >= 12  # DC 12 for most actions
        
        if action_type == "explore":
            if success:
                narrative = f"{player.character_name} mağarayı dikkatlice keşfetti ve gizli bir geçit buldu!"
                self.game_state.group_inventory.append("Ancient Map")
            else:
                narrative = f"{player.character_name} mağarayı keşfetti ama hiçbir şey bulamadı."
        
        elif action_type == "talk":
            if success:
                narrative = f"{player.character_name} başarıyla iletişim kurdu ve değerli bilgi aldı!"
                self.game_state.quest_progress["information_gathered"] = True
            else:
                narrative = f"{player.character_name} konuşmaya çalıştı ama kimse güvenmedi."
        
        elif action_type == "attack":
            if success:
                damage = random.randint(5, 15)
                narrative = f"{player.character_name} saldırdı ve {damage} hasar verdi!"
                # Update enemy HP or defeat enemy
            else:
                narrative = f"{player.character_name} saldırdı ama ıskaladı!"
        
        elif action_type == "cast_spell":
            if success:
                narrative = f"{player.character_name} büyü yaptı ve etkili oldu!"
                player.mana = max(0, player.mana - 10)
            else:
                narrative = f"{player.character_name} büyü yapmaya çalıştı ama başarısız oldu!"
        
        else:
            narrative = f"{player.character_name} {description} yaptı."
        
        # Update narrative
        self.game_state.current_narrative = narrative
        
        # Generate new available actions based on the action
        self._generate_new_actions(action_type, success)
        
        return {
            "action_type": action_type,
            "description": description,
            "dice_result": dice_result,
            "success": success,
            "narrative": narrative,
            "player": player.character_name
        }
    
    def _generate_new_actions(self, previous_action: str, was_successful: bool):
        """Generate new available actions based on previous action"""
        if previous_action == "explore" and was_successful:
            self.game_state.available_actions = [
                {"type": "investigate", "description": "Gizli geçidi araştır", "dice": "1d20", "skill": "investigation"},
                {"type": "stealth", "description": "Gizlice geçitten geç", "dice": "1d20", "skill": "stealth"},
                {"type": "talk", "description": "Yardım için seslen", "dice": "1d20", "skill": "persuasion"}
            ]
        elif previous_action == "talk" and was_successful:
            self.game_state.available_actions = [
                {"type": "explore", "description": "Verilen bilgiye göre ara", "dice": "1d20", "skill": "perception"},
                {"type": "attack", "description": "Hazırlıklı saldır", "dice": "1d20", "skill": "combat"},
                {"type": "cast_spell", "description": "Büyü hazırla", "dice": "1d20", "skill": "magic"}
            ]
        else:
            # Default actions
            self.game_state.available_actions = [
                {"type": "explore", "description": "Çevreyi keşfet", "dice": "1d20", "skill": "perception"},
                {"type": "talk", "description": "NPC ile konuş", "dice": "1d20", "skill": "persuasion"},
                {"type": "attack", "description": "Saldır", "dice": "1d20", "skill": "combat"}
            ]
    
    def _advance_turn(self):
        """Advance to the next player's turn"""
        # Clear current player's turn
        if self._get_current_player():
            self._get_current_player().is_current_turn = False
        
        # Move to next player
        self.current_player_index = (self.current_player_index + 1) % len(self.player_order)
        
        # Set new current player
        current_player = self._get_current_player()
        if current_player:
            current_player.is_current_turn = True
            self.game_state.current_player_turn = current_player.id
        
        # Update round if we've gone through all players
        if self.current_player_index == 0:
            self.game_state.round_number += 1
    
    def _get_current_player(self) -> Optional[FRPPlayer]:
        """Get the current player"""
        if not self.player_order or self.current_player_index >= len(self.player_order):
            return None
        
        player_id = self.player_order[self.current_player_index]
        return self.players.get(player_id)
    
    def _update_game_state(self):
        """Update the overall game state"""
        self.last_activity = datetime.now()
        
        # Check for combat conditions
        if self.game_state.combat_active:
            self._update_combat_state()
        
        # Update quest progress
        self._update_quest_progress()
    
    def _update_combat_state(self):
        """Update combat state if active"""
        # Combat logic would go here
        pass
    
    def _update_quest_progress(self):
        """Update quest progress based on actions"""
        # Quest logic would go here
        pass
    
    def get_game_state(self) -> GameState:
        """Get the current game state"""
        return self.game_state
    
    def get_players_info(self) -> List[Dict]:
        """Get information about all players"""
        return [
            {
                "id": player.id,
                "username": player.username,
                "character_name": player.character_name,
                "character_class": player.character_class,
                "hp": player.hp,
                "max_hp": player.max_hp,
                "mana": player.mana,
                "max_mana": player.max_mana,
                "level": player.level,
                "xp": player.xp,
                "is_current_turn": player.is_current_turn,
                "is_alive": player.is_alive,
                "status_effects": player.status_effects
            }
            for player in self.players.values()
        ]
    
    def start_combat(self, enemies: List[Dict]) -> Dict[str, Any]:
        """Start a combat encounter"""
        self.game_state.combat_active = True
        self.game_state.enemies = enemies
        
        # Roll initiative for all participants
        all_participants = list(self.players.values()) + enemies
        
        for participant in all_participants:
            if hasattr(participant, 'initiative'):
                participant.initiative = random.randint(1, 20) + getattr(participant, 'dexterity', 0)
        
        # Sort by initiative
        all_participants.sort(key=lambda x: x.initiative, reverse=True)
        self.initiative_order = [p.id for p in all_participants if hasattr(p, 'id')]
        
        return {
            "success": True,
            "combat_started": True,
            "initiative_order": self.initiative_order,
            "enemies": enemies
        }
    
    def end_session(self):
        """End the FRP session"""
        self.is_active = False
        logger.info(f"FRP session {self.session_id} ended") 