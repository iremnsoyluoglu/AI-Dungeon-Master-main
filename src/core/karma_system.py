#!/usr/bin/env python3
"""
Karma System for AI Dungeon Master
Handles moral choices, karma points, and NPC relationship tracking
"""

import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class KarmaAction:
    action_id: str
    action_name: str
    karma_value: int
    description: str
    category: str  # "combat", "social", "exploration", "quest"

@dataclass
class NPCRelationship:
    npc_id: str
    npc_name: str
    relationship_level: int  # -10 to 10
    trust_level: int  # 0 to 100
    last_interaction: str
    interaction_history: List[Dict[str, Any]]
    special_events: List[str]

@dataclass
class KarmaState:
    karma_points: int
    moral_alignment: str  # "good", "neutral", "evil"
    reputation: Dict[str, int]  # faction reputations
    npc_relationships: Dict[str, NPCRelationship]
    choice_history: List[Dict[str, Any]]

class KarmaSystem:
    """Manages karma, moral choices, and NPC relationships"""
    
    def __init__(self):
        self.karma_file = "data/karma_data.json"
        self.npc_relationships_file = "data/npc_relationships.json"
        self._ensure_data_directory()
        self._load_karma_actions()
        self._load_npc_relationships()
        self._initialize_default_actions()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        import os
        os.makedirs("data", exist_ok=True)
    
    def _load_karma_actions(self):
        """Load karma actions from file"""
        try:
            import os
            if os.path.exists(self.karma_file):
                with open(self.karma_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.karma_actions = {}
                    for action_id, action_data in data.items():
                        self.karma_actions[action_id] = KarmaAction(**action_data)
            else:
                self.karma_actions = {}
        except Exception as e:
            print(f"Error loading karma actions: {e}")
            self.karma_actions = {}
    
    def _save_karma_actions(self):
        """Save karma actions to file"""
        try:
            with open(self.karma_file, 'w', encoding='utf-8') as f:
                data = {action_id: asdict(action) for action_id, action in self.karma_actions.items()}
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving karma actions: {e}")
    
    def _load_npc_relationships(self):
        """Load NPC relationships from file"""
        try:
            import os
            if os.path.exists(self.npc_relationships_file):
                with open(self.npc_relationships_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.npc_relationships = {}
                    for npc_id, npc_data in data.items():
                        self.npc_relationships[npc_id] = NPCRelationship(**npc_data)
            else:
                self.npc_relationships = {}
        except Exception as e:
            print(f"Error loading NPC relationships: {e}")
            self.npc_relationships = {}
    
    def _save_npc_relationships(self):
        """Save NPC relationships to file"""
        try:
            with open(self.npc_relationships_file, 'w', encoding='utf-8') as f:
                data = {npc_id: asdict(relationship) for npc_id, relationship in self.npc_relationships.items()}
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving NPC relationships: {e}")
    
    def _initialize_default_actions(self):
        """Initialize default karma actions if none exist"""
        if not self.karma_actions:
            self.karma_actions = {
                # Combat actions
                "kill_innocent": KarmaAction("kill_innocent", "Kill Innocent", -20, "Killing innocent people", "combat"),
                "spare_enemy": KarmaAction("spare_enemy", "Spare Enemy", 10, "Showing mercy to enemies", "combat"),
                "defend_weak": KarmaAction("defend_weak", "Defend Weak", 15, "Protecting the weak", "combat"),
                "attack_unprovoked": KarmaAction("attack_unprovoked", "Attack Unprovoked", -15, "Attacking without reason", "combat"),
                
                # Social actions
                "help_npc": KarmaAction("help_npc", "Help NPC", 5, "Helping NPCs", "social"),
                "ignore_help_request": KarmaAction("ignore_help_request", "Ignore Help Request", -5, "Ignoring those in need", "social"),
                "give_charity": KarmaAction("give_charity", "Give Charity", 8, "Giving to the poor", "social"),
                "steal_from_poor": KarmaAction("steal_from_poor", "Steal from Poor", -12, "Stealing from the poor", "social"),
                "tell_truth": KarmaAction("tell_truth", "Tell Truth", 3, "Being honest", "social"),
                "lie_to_npc": KarmaAction("lie_to_npc", "Lie to NPC", -3, "Lying to NPCs", "social"),
                "steal_item": KarmaAction("steal_item", "Steal Item", -8, "Stealing items from NPCs", "social"),
                "save_npc": KarmaAction("save_npc", "Save NPC", 12, "Saving NPCs from danger", "social"),
                "betray_ally": KarmaAction("betray_ally", "Betray Ally", -15, "Betraying trusted allies", "social"),
                
                # Exploration actions
                "respect_graves": KarmaAction("respect_graves", "Respect Graves", 5, "Respecting burial sites", "exploration"),
                "loot_graves": KarmaAction("loot_graves", "Loot Graves", -10, "Desecrating graves", "exploration"),
                "preserve_artifacts": KarmaAction("preserve_artifacts", "Preserve Artifacts", 7, "Preserving historical artifacts", "exploration"),
                "destroy_artifacts": KarmaAction("destroy_artifacts", "Destroy Artifacts", -8, "Destroying historical artifacts", "exploration"),
                
                # Quest actions
                "complete_quest": KarmaAction("complete_quest", "Complete Quest", 10, "Completing quests", "quest"),
                "abandon_quest": KarmaAction("abandon_quest", "Abandon Quest", -5, "Abandoning quests", "quest"),
                "help_quest_giver": KarmaAction("help_quest_giver", "Help Quest Giver", 8, "Helping quest givers", "quest"),
                "betray_quest_giver": KarmaAction("betray_quest_giver", "Betray Quest Giver", -15, "Betraying quest givers", "quest")
            }
            self._save_karma_actions()
    
    def record_action(self, character_id: str, action_id: str, npc_id: str = None, 
                     additional_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Record a karma action and update relationships"""
        if action_id not in self.karma_actions:
            return {"success": False, "error": "Unknown action"}
        
        action = self.karma_actions[action_id]
        now = datetime.now().isoformat()
        
        # Record choice history
        choice_record = {
            "action_id": action_id,
            "action_name": action.action_name,
            "karma_value": action.karma_value,
            "timestamp": now,
            "npc_id": npc_id,
            "additional_data": additional_data or {}
        }
        
        # Update NPC relationship if applicable
        if npc_id:
            self._update_npc_relationship(npc_id, action_id, action.karma_value, additional_data)
        
        return {
            "success": True,
            "action": action.action_name,
            "karma_change": action.karma_value,
            "description": action.description,
            "timestamp": now
        }
    
    def _update_npc_relationship(self, npc_id: str, action_id: str, karma_value: int, 
                                additional_data: Dict[str, Any] = None):
        """Update NPC relationship based on action"""
        if npc_id not in self.npc_relationships:
            # Create new NPC relationship
            self.npc_relationships[npc_id] = NPCRelationship(
                npc_id=npc_id,
                npc_name=additional_data.get("npc_name", f"NPC_{npc_id}") if additional_data else f"NPC_{npc_id}",
                relationship_level=0,
                trust_level=50,
                last_interaction=datetime.now().isoformat(),
                interaction_history=[],
                special_events=[]
            )
        
        npc = self.npc_relationships[npc_id]
        now = datetime.now().isoformat()
        
        # Update relationship level based on karma value
        if karma_value > 0:
            npc.relationship_level = min(10, npc.relationship_level + 1)
            npc.trust_level = min(100, npc.trust_level + 10)
        elif karma_value < 0:
            npc.relationship_level = max(-10, npc.relationship_level - 1)
            npc.trust_level = max(0, npc.trust_level - 10)
        
        # Record interaction
        interaction = {
            "action_id": action_id,
            "karma_value": karma_value,
            "timestamp": now,
            "relationship_change": 1 if karma_value > 0 else -1 if karma_value < 0 else 0,
            "trust_change": 10 if karma_value > 0 else -10 if karma_value < 0 else 0
        }
        
        npc.interaction_history.append(interaction)
        npc.last_interaction = now
        
        # Check for special events based on relationship level
        if npc.relationship_level >= 8 and "trusted_friend" not in npc.special_events:
            npc.special_events.append("trusted_friend")
        elif npc.relationship_level <= -8 and "sworn_enemy" not in npc.special_events:
            npc.special_events.append("sworn_enemy")
        
        self._save_npc_relationships()
    
    def get_npc_relationship(self, npc_id: str) -> Optional[NPCRelationship]:
        """Get NPC relationship data"""
        return self.npc_relationships.get(npc_id)
    
    def get_all_npc_relationships(self) -> Dict[str, NPCRelationship]:
        """Get all NPC relationships"""
        return self.npc_relationships
    
    def get_npc_reaction(self, npc_id: str, action_type: str) -> Dict[str, Any]:
        """Get NPC reaction based on relationship level"""
        npc = self.npc_relationships.get(npc_id)
        if not npc:
            return {"reaction": "neutral", "message": "Unknown NPC"}
        
        relationship_level = npc.relationship_level
        trust_level = npc.trust_level
        
        if relationship_level >= 8:
            return {
                "reaction": "very_friendly",
                "message": f"{npc.npc_name} is very friendly and helpful",
                "bonus": "extra_help",
                "relationship_level": relationship_level,
                "trust_level": trust_level
            }
        elif relationship_level >= 5:
            return {
                "reaction": "friendly",
                "message": f"{npc.npc_name} is friendly towards you",
                "bonus": "discount",
                "relationship_level": relationship_level,
                "trust_level": trust_level
            }
        elif relationship_level >= 2:
            return {
                "reaction": "neutral_positive",
                "message": f"{npc.npc_name} is somewhat friendly",
                "bonus": "small_favor",
                "relationship_level": relationship_level,
                "trust_level": trust_level
            }
        elif relationship_level >= -1:
            return {
                "reaction": "neutral",
                "message": f"{npc.npc_name} is neutral towards you",
                "bonus": "none",
                "relationship_level": relationship_level,
                "trust_level": trust_level
            }
        elif relationship_level >= -4:
            return {
                "reaction": "neutral_negative",
                "message": f"{npc.npc_name} is somewhat unfriendly",
                "penalty": "higher_prices",
                "relationship_level": relationship_level,
                "trust_level": trust_level
            }
        elif relationship_level >= -7:
            return {
                "reaction": "unfriendly",
                "message": f"{npc.npc_name} is unfriendly towards you",
                "penalty": "refuse_service",
                "relationship_level": relationship_level,
                "trust_level": trust_level
            }
        else:
            return {
                "reaction": "hostile",
                "message": f"{npc.npc_name} is hostile towards you",
                "penalty": "attack",
                "relationship_level": relationship_level,
                "trust_level": trust_level
            }
    
    def get_karma_summary(self, character_id: str) -> Dict[str, Any]:
        """Get karma summary for character"""
        # Calculate total karma from recorded actions
        total_karma = 0
        npc_relationships = {}
        
        # Calculate karma from NPC relationships
        for npc_id, relationship in self.npc_relationships.items():
            npc_relationships[npc_id] = {
                "relationship_level": relationship.relationship_level,
                "trust_level": relationship.trust_level,
                "special_events": relationship.special_events
            }
            # Estimate karma from relationship level
            total_karma += relationship.relationship_level * 2
        
        return {
            "total_karma": total_karma,
            "moral_alignment": self.get_moral_alignment(total_karma),
            "npc_relationships": npc_relationships,
            "total_actions": len(self.karma_actions),
            "action_categories": {
                "combat": len([a for a in self.karma_actions.values() if a.category == "combat"]),
                "social": len([a for a in self.karma_actions.values() if a.category == "social"]),
                "exploration": len([a for a in self.karma_actions.values() if a.category == "exploration"]),
                "quest": len([a for a in self.karma_actions.values() if a.category == "quest"])
            },
            "npc_relationships_count": len(self.npc_relationships),
            "available_actions": list(self.karma_actions.keys())
        }
    
    def get_moral_alignment(self, karma_points: int) -> str:
        """Determine moral alignment based on karma points"""
        if karma_points >= 50:
            return "good"
        elif karma_points <= -50:
            return "evil"
        else:
            return "neutral"
    
    def get_karma_effects(self, karma_points: int) -> Dict[str, Any]:
        """Get effects based on karma level"""
        alignment = self.get_moral_alignment(karma_points)
        
        effects = {
            "good": {
                "npc_reactions": "friendly",
                "shop_discounts": True,
                "quest_rewards": "bonus",
                "combat_bonus": "defensive",
                "special_dialogue": "trusted"
            },
            "neutral": {
                "npc_reactions": "neutral",
                "shop_discounts": False,
                "quest_rewards": "normal",
                "combat_bonus": "none",
                "special_dialogue": "standard"
            },
            "evil": {
                "npc_reactions": "hostile",
                "shop_discounts": False,
                "quest_rewards": "penalty",
                "combat_bonus": "aggressive",
                "special_dialogue": "feared"
            }
        }
        
        return effects.get(alignment, effects["neutral"]) 