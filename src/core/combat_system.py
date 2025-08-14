#!/usr/bin/env python3
"""
Combat System
============

Handles turn-based combat mechanics.
"""

import json
import random
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional

class CombatSystem:
    """Manages turn-based combat mechanics"""
    
    def __init__(self):
        self.combats_file = "data/combat_sessions.json"
        self._ensure_data_directory()
        self._load_combats()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        import os
        os.makedirs("data", exist_ok=True)
    
    def _load_combats(self):
        """Load combat sessions from file"""
        try:
            import os
            if os.path.exists(self.combats_file):
                with open(self.combats_file, 'r', encoding='utf-8') as f:
                    self.combats = json.load(f)
            else:
                self.combats = {}
        except Exception as e:
            print(f"Error loading combat sessions: {e}")
            self.combats = {}
    
    def _save_combats(self):
        """Save combat sessions to file"""
        try:
            with open(self.combats_file, 'w', encoding='utf-8') as f:
                json.dump(self.combats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving combat sessions: {e}")
    
    def add_participant(self, combat_id: str, participant: Dict[str, Any]) -> Dict[str, Any]:
        """Add a participant to an existing combat"""
        combat = self.combats.get(combat_id)
        if not combat:
            return {"success": False, "error": "Combat session not found"}
        
        try:
            # Calculate initiative for the new participant
            initiative_roll = self.roll_dice("1d20")
            participant["initiative"] = initiative_roll + participant.get("dexterity", 10)
            
            # Add to participants list
            combat["participants"].append(participant)
            
            # Recalculate turn order
            combat["participants"].sort(key=lambda x: x["initiative"], reverse=True)
            combat["turn_order"] = [p["id"] for p in combat["participants"]]
            
            combat["last_updated"] = datetime.now().isoformat()
            self._save_combats()
            
            return {
                "success": True,
                "combat_id": combat_id,
                "participant": participant,
                "message": "Participant added successfully"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def start_combat(self, participants: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Start a new combat session"""
        try:
            combat_id = str(uuid.uuid4())
            now = datetime.now().isoformat()
            
            # Calculate initiative for each participant
            for participant in participants:
                initiative_roll = self.roll_dice("1d20")
                participant["initiative"] = initiative_roll + participant.get("dexterity", 10)
            
            # Sort by initiative (highest first)
            participants.sort(key=lambda x: x["initiative"], reverse=True)
            turn_order = [p["id"] for p in participants]
            
            combat_data = {
                "id": combat_id,
                "participants": participants,
                "turn_order": turn_order,
                "current_turn": 0,
                "round": 1,
                "status": "active",
                "combat_log": [],
                "created_at": now,
                "last_updated": now
            }
            
            self.combats[combat_id] = combat_data
            self._save_combats()
            
            return {
                "success": True,
                "combat_id": combat_id,
                "combat": combat_data,
                "message": "Combat started successfully"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_combat_state(self, combat_id: str) -> Optional[Dict[str, Any]]:
        """Get combat state by ID"""
        return self.combats.get(combat_id)
    
    def perform_combat_action(self, combat_id: str, character_id: str, 
                            action_type: str, target_id: str = None) -> Dict[str, Any]:
        """Perform a combat action"""
        combat = self.combats.get(combat_id)
        if not combat:
            return {"success": False, "error": "Combat session not found"}
        
        # Check if it's the character's turn
        current_turn = combat["turn_order"][combat["current_turn"]]
        if current_turn != character_id:
            return {"success": False, "error": "Not your turn"}
        
        # Find the acting character
        character = None
        for participant in combat["participants"]:
            if participant["id"] == character_id:
                character = participant
                break
        
        if not character:
            return {"success": False, "error": "Character not found in combat"}
        
        # Process the action
        result = self._process_combat_action(character, action_type, target_id, combat)
        
        # Log the action
        combat["combat_log"].append({
            "round": combat["round"],
            "turn": combat["current_turn"],
            "character": character["name"],
            "action": action_type,
            "target": target_id,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
        # Move to next turn
        combat["current_turn"] += 1
        if combat["current_turn"] >= len(combat["turn_order"]):
            combat["current_turn"] = 0
            combat["round"] += 1
        
        combat["last_updated"] = datetime.now().isoformat()
        self._save_combats()
        
        return {
            "success": True,
            "action_result": result,
            "next_turn": combat["turn_order"][combat["current_turn"]],
            "round": combat["round"],
            "combat_state": combat
        }
    
    def _process_combat_action(self, character: Dict[str, Any], action_type: str, 
                              target_id: str, combat: Dict[str, Any]) -> Dict[str, Any]:
        """Process a combat action"""
        if action_type == "attack":
            return self._process_attack(character, target_id, combat)
        elif action_type == "defend":
            return self._process_defend(character)
        elif action_type == "cast_spell":
            return self._process_spell(character, target_id, combat)
        else:
            return {"success": False, "error": "Unknown action type"}
    
    def _process_attack(self, attacker: Dict[str, Any], target_id: str, 
                       combat: Dict[str, Any]) -> Dict[str, Any]:
        """Process an attack action"""
        # Find target
        target = None
        for participant in combat["participants"]:
            if participant["id"] == target_id:
                target = participant
                break
        
        if not target:
            return {"success": False, "error": "Target not found"}
        
        # Attack roll
        attack_roll = self.roll_dice("1d20")
        attack_bonus = attacker.get("strength", 10)
        total_attack = attack_roll + attack_bonus
        
        # Target's armor class
        target_ac = target.get("armor_class", 10)
        
        if total_attack >= target_ac:
            # Hit! Calculate damage
            weapon_damage = attacker.get("weapon_damage", "1d6")
            damage = self.roll_dice(weapon_damage)
            
            # Apply damage
            target["current_health"] = max(0, target["current_health"] - damage)
            
            return {
                "success": True,
                "hit": True,
                "attack_roll": attack_roll,
                "total_attack": total_attack,
                "target_ac": target_ac,
                "damage": damage,
                "target_health": target["current_health"],
                "target_dead": target["current_health"] <= 0
            }
        else:
            return {
                "success": True,
                "hit": False,
                "attack_roll": attack_roll,
                "total_attack": total_attack,
                "target_ac": target_ac,
                "damage": 0
            }
    
    def _process_defend(self, character: Dict[str, Any]) -> Dict[str, Any]:
        """Process a defend action"""
        # Temporary armor bonus
        character["armor_class"] = character.get("armor_class", 10) + 2
        
        return {
            "success": True,
            "action": "defend",
            "armor_bonus": 2,
            "new_armor_class": character["armor_class"]
        }
    
    def _process_spell(self, caster: Dict[str, Any], target_id: str, 
                      combat: Dict[str, Any]) -> Dict[str, Any]:
        """Process a spell casting action"""
        if caster.get("character_class") != "mage":
            return {"success": False, "error": "Only mages can cast spells"}
        
        # Spell check
        spell_roll = self.roll_dice("1d20")
        spell_bonus = caster.get("intelligence", 10)
        total_spell = spell_roll + spell_bonus
        
        spell_dc = 15
        
        if total_spell >= spell_dc:
            # Spell success
            damage = self.roll_dice("2d6")
            
            if target_id:
                # Find target and apply damage
                for participant in combat["participants"]:
                    if participant["id"] == target_id:
                        participant["current_health"] = max(0, participant["current_health"] - damage)
                        break
            
            return {
                "success": True,
                "spell_success": True,
                "spell_roll": spell_roll,
                "total_spell": total_spell,
                "spell_dc": spell_dc,
                "damage": damage
            }
        else:
            return {
                "success": True,
                "spell_success": False,
                "spell_roll": spell_roll,
                "total_spell": total_spell,
                "spell_dc": spell_dc,
                "damage": 0
            }
    
    def roll_dice(self, dice_notation: str) -> int:
        """Roll dice using notation like '2d6', '1d20', etc."""
        try:
            if "d" not in dice_notation:
                return int(dice_notation)
            
            parts = dice_notation.split("d")
            if len(parts) != 2:
                return 0
            
            num_dice = int(parts[0])
            dice_size = int(parts[1])
            
            total = 0
            for _ in range(num_dice):
                total += random.randint(1, dice_size)
            
            return total
        except:
            return 0
    
    def end_combat(self, combat_id: str) -> bool:
        """End a combat session"""
        combat = self.combats.get(combat_id)
        if not combat:
            return False
        
        combat["status"] = "finished"
        combat["ended_at"] = datetime.now().isoformat()
        self._save_combats()
        return True 