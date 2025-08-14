#!/usr/bin/env python3
"""
Dice System
==========

Handles dice rolling mechanics for the game.
"""

import random
from typing import Dict, List, Any, Optional

class DiceSystem:
    """Manages dice rolling mechanics"""
    
    def __init__(self):
        self.dice_history = []
    
    def roll_dice(self, dice_notation: str) -> Dict[str, Any]:
        """Roll dice using notation like '2d6', '1d20', '3d8+5', etc."""
        try:
            # Handle modifiers (e.g., "3d8+5")
            modifier = 0
            base_notation = dice_notation
            
            if "+" in dice_notation:
                parts = dice_notation.split("+")
                base_notation = parts[0]
                modifier = int(parts[1])
            elif "-" in dice_notation:
                parts = dice_notation.split("-")
                base_notation = parts[0]
                modifier = -int(parts[1])
            
            if "d" not in base_notation:
                value = int(base_notation)
                result = {
                    "notation": dice_notation,
                    "rolls": [value],
                    "total": value + modifier,
                    "modifier": modifier,
                    "success": True
                }
                self.dice_history.append(result)
                return result
            
            parts = base_notation.split("d")
            if len(parts) != 2:
                return {"success": False, "error": "Invalid dice notation"}
            
            num_dice = int(parts[0])
            dice_size = int(parts[1])
            
            rolls = []
            total = 0
            
            for _ in range(num_dice):
                roll = random.randint(1, dice_size)
                rolls.append(roll)
                total += roll
            
            total += modifier
            
            result = {
                "notation": dice_notation,
                "rolls": rolls,
                "total": total,
                "modifier": modifier,
                "success": True
            }
            
            self.dice_history.append(result)
            return result
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def roll_attack(self, attack_bonus: int = 0, target_ac: int = 10) -> Dict[str, Any]:
        """Roll an attack with bonus against target AC"""
        attack_roll = self.roll_dice("1d20")
        if not attack_roll["success"]:
            return attack_roll
        
        total_attack = attack_roll["total"] + attack_bonus
        hit = total_attack >= target_ac
        critical_hit = attack_roll["total"] == 20
        critical_miss = attack_roll["total"] == 1
        
        return {
            "success": True,
            "attack_roll": attack_roll,
            "attack_bonus": attack_bonus,
            "total_attack": total_attack,
            "target_ac": target_ac,
            "hit": hit,
            "critical_hit": critical_hit,
            "critical_miss": critical_miss
        }
    
    def roll_damage(self, damage_dice: str, damage_bonus: int = 0) -> Dict[str, Any]:
        """Roll damage dice with bonus"""
        damage_roll = self.roll_dice(damage_dice)
        if not damage_roll["success"]:
            return damage_roll
        
        total_damage = damage_roll["total"] + damage_bonus
        
        return {
            "success": True,
            "damage_roll": damage_roll,
            "damage_bonus": damage_bonus,
            "total_damage": total_damage
        }
    
    def roll_saving_throw(self, save_bonus: int = 0, save_dc: int = 15) -> Dict[str, Any]:
        """Roll a saving throw"""
        save_roll = self.roll_dice("1d20")
        if not save_roll["success"]:
            return save_roll
        
        total_save = save_roll["total"] + save_bonus
        success = total_save >= save_dc
        critical_success = save_roll["total"] == 20
        critical_failure = save_roll["total"] == 1
        
        return {
            "success": True,
            "save_roll": save_roll,
            "save_bonus": save_bonus,
            "total_save": total_save,
            "save_dc": save_dc,
            "success": success,
            "critical_success": critical_success,
            "critical_failure": critical_failure
        }
    
    def roll_initiative(self, dexterity_modifier: int = 0) -> Dict[str, Any]:
        """Roll initiative with dexterity modifier"""
        initiative_roll = self.roll_dice("1d20")
        if not initiative_roll["success"]:
            return initiative_roll
        
        total_initiative = initiative_roll["total"] + dexterity_modifier
        
        return {
            "success": True,
            "initiative_roll": initiative_roll,
            "dexterity_modifier": dexterity_modifier,
            "total_initiative": total_initiative
        }
    
    def roll_skill_check(self, skill_bonus: int = 0, difficulty_class: int = 15) -> Dict[str, Any]:
        """Roll a skill check"""
        skill_roll = self.roll_dice("1d20")
        if not skill_roll["success"]:
            return skill_roll
        
        total_skill = skill_roll["total"] + skill_bonus
        success = total_skill >= difficulty_class
        critical_success = skill_roll["total"] == 20
        critical_failure = skill_roll["total"] == 1
        
        return {
            "success": True,
            "skill_roll": skill_roll,
            "skill_bonus": skill_bonus,
            "total_skill": total_skill,
            "difficulty_class": difficulty_class,
            "success": success,
            "critical_success": critical_success,
            "critical_failure": critical_failure
        }
    
    def get_dice_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent dice roll history"""
        return self.dice_history[-limit:] if self.dice_history else []
    
    def clear_history(self):
        """Clear dice roll history"""
        self.dice_history.clear() 