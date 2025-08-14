#!/usr/bin/env python3
"""
Skill System
============

Comprehensive skill system with skill-based action requirements, progression,
and learning mechanics.
"""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum

class SkillType(Enum):
    COMBAT = "combat"
    SOCIAL = "social"
    STEALTH = "stealth"
    MAGIC = "magic"
    CRAFTING = "crafting"
    EXPLORATION = "exploration"
    KNOWLEDGE = "knowledge"

class SkillDifficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"
    MASTER = "master"

class SkillSystem:
    """Comprehensive skill system with progression and learning"""
    
    def __init__(self):
        self.skills_file = "data/skills.json"
        self.player_skills_file = "data/player_skills.json"
        self._ensure_data_directory()
        self._load_skills()
        self._load_player_skills()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs("data", exist_ok=True)
    
    def _load_skills(self):
        """Load skill definitions"""
        try:
            if os.path.exists(self.skills_file):
                with open(self.skills_file, 'r', encoding='utf-8') as f:
                    self.skills = json.load(f)
            else:
                self.skills = self._create_default_skills()
                self._save_skills()
        except Exception as e:
            print(f"Error loading skills: {e}")
            self.skills = self._create_default_skills()
    
    def _save_skills(self):
        """Save skill definitions"""
        try:
            with open(self.skills_file, 'w', encoding='utf-8') as f:
                json.dump(self.skills, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving skills: {e}")
    
    def _load_player_skills(self):
        """Load player skill data"""
        try:
            if os.path.exists(self.player_skills_file):
                with open(self.player_skills_file, 'r', encoding='utf-8') as f:
                    self.player_skills = json.load(f)
            else:
                self.player_skills = {}
        except Exception as e:
            print(f"Error loading player skills: {e}")
            self.player_skills = {}
    
    def _save_player_skills(self):
        """Save player skill data"""
        try:
            with open(self.player_skills_file, 'w', encoding='utf-8') as f:
                json.dump(self.player_skills, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving player skills: {e}")
    
    def _create_default_skills(self) -> Dict[str, Any]:
        """Create default skill definitions"""
        return {
            "weapon_mastery": {
                "id": "weapon_mastery",
                "name": "Silah Ustalığı",
                "type": SkillType.COMBAT.value,
                "description": "Silahları etkili kullanma becerisi",
                "difficulty": SkillDifficulty.EASY.value,
                "max_level": 5,
                "prerequisites": [],
                "requirements": {
                    "level": 1,
                    "skill_points": 1
                },
                "effects": {
                    "attack_bonus": 2,
                    "critical_chance": 0.02
                },
                "progression": {
                    "xp_per_level": [100, 200, 400, 800, 1600],
                    "bonus_per_level": [1, 2, 3, 4, 5]
                }
            },
            "battle_rage": {
                "id": "battle_rage",
                "name": "Savaş Öfkesi",
                "type": SkillType.COMBAT.value,
                "description": "Savaş sırasında güçlü bir öfke durumu",
                "difficulty": SkillDifficulty.MEDIUM.value,
                "max_level": 3,
                "prerequisites": ["weapon_mastery"],
                "requirements": {
                    "level": 3,
                    "skill_points": 2,
                    "strength": 14
                },
                "effects": {
                    "damage_bonus": 3,
                    "temporary_hp": 10
                },
                "progression": {
                    "xp_per_level": [300, 600, 1200],
                    "bonus_per_level": [3, 6, 10]
                }
            },
            "stealth": {
                "id": "stealth",
                "name": "Gizlilik",
                "type": SkillType.STEALTH.value,
                "description": "Gizlice hareket etme ve gizlenme becerisi",
                "difficulty": SkillDifficulty.EASY.value,
                "max_level": 5,
                "prerequisites": [],
                "requirements": {
                    "level": 1,
                    "skill_points": 1,
                    "dexterity": 12
                },
                "effects": {
                    "stealth_bonus": 2,
                    "sneak_attack_damage": 1.5
                },
                "progression": {
                    "xp_per_level": [100, 200, 400, 800, 1600],
                    "bonus_per_level": [1, 2, 3, 4, 5]
                }
            },
            "persuasion": {
                "id": "persuasion",
                "name": "İkna",
                "type": SkillType.SOCIAL.value,
                "description": "İnsanları ikna etme ve etkileme becerisi",
                "difficulty": SkillDifficulty.MEDIUM.value,
                "max_level": 5,
                "prerequisites": [],
                "requirements": {
                    "level": 1,
                    "skill_points": 1,
                    "charisma": 12
                },
                "effects": {
                    "persuasion_bonus": 2,
                    "discount_chance": 0.1
                },
                "progression": {
                    "xp_per_level": [150, 300, 600, 1200, 2400],
                    "bonus_per_level": [2, 3, 4, 5, 6]
                }
            },
            "fire_magic": {
                "id": "fire_magic",
                "name": "Ateş Büyüsü",
                "type": SkillType.MAGIC.value,
                "description": "Ateş elementini kontrol etme becerisi",
                "difficulty": SkillDifficulty.HARD.value,
                "max_level": 5,
                "prerequisites": [],
                "requirements": {
                    "level": 2,
                    "skill_points": 2,
                    "intelligence": 14,
                    "mana": 50
                },
                "effects": {
                    "fire_damage_bonus": 2,
                    "fire_resistance": 0.1
                },
                "progression": {
                    "xp_per_level": [200, 400, 800, 1600, 3200],
                    "bonus_per_level": [2, 4, 6, 8, 10]
                }
            },
            "blacksmithing": {
                "id": "blacksmithing",
                "name": "Demircilik",
                "type": SkillType.CRAFTING.value,
                "description": "Silah ve zırh yapma becerisi",
                "difficulty": SkillDifficulty.MEDIUM.value,
                "max_level": 5,
                "prerequisites": [],
                "requirements": {
                    "level": 1,
                    "skill_points": 1,
                    "strength": 12
                },
                "effects": {
                    "crafting_quality": 1.1,
                    "repair_efficiency": 1.2
                },
                "progression": {
                    "xp_per_level": [150, 300, 600, 1200, 2400],
                    "bonus_per_level": [1, 2, 3, 4, 5]
                }
            },
            "survival": {
                "id": "survival",
                "name": "Hayatta Kalma",
                "type": SkillType.EXPLORATION.value,
                "description": "Vahşi doğada hayatta kalma becerisi",
                "difficulty": SkillDifficulty.EASY.value,
                "max_level": 5,
                "prerequisites": [],
                "requirements": {
                    "level": 1,
                    "skill_points": 1
                },
                "effects": {
                    "healing_rate": 1.2,
                    "food_efficiency": 1.3
                },
                "progression": {
                    "xp_per_level": [100, 200, 400, 800, 1600],
                    "bonus_per_level": [1, 2, 3, 4, 5]
                }
            },
            "lore": {
                "id": "lore",
                "name": "Bilgelik",
                "type": SkillType.KNOWLEDGE.value,
                "description": "Antik bilgileri ve sırları anlama becerisi",
                "difficulty": SkillDifficulty.HARD.value,
                "max_level": 5,
                "prerequisites": [],
                "requirements": {
                    "level": 1,
                    "skill_points": 1,
                    "intelligence": 12
                },
                "effects": {
                    "lore_bonus": 2,
                    "quest_reward_bonus": 0.1
                },
                "progression": {
                    "xp_per_level": [200, 400, 800, 1600, 3200],
                    "bonus_per_level": [2, 3, 4, 5, 6]
                }
            }
        }
    
    def get_skill(self, skill_id: str) -> Optional[Dict[str, Any]]:
        """Get skill definition by ID"""
        return self.skills.get(skill_id)
    
    def get_player_skills(self, player_id: str) -> Dict[str, Any]:
        """Get player's skills"""
        if player_id not in self.player_skills:
            self.player_skills[player_id] = {
                "skills": {},
                "skill_points": 5,
                "total_xp": 0,
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
        return self.player_skills[player_id]
    
    def can_learn_skill(self, player_id: str, skill_id: str) -> Dict[str, Any]:
        """Check if player can learn a skill"""
        try:
            skill_def = self.get_skill(skill_id)
            if not skill_def:
                return {"success": False, "error": f"Skill {skill_id} not found"}
            
            player_data = self.get_player_skills(player_id)
            
            # Check prerequisites
            for prerequisite in skill_def.get("prerequisites", []):
                if prerequisite not in player_data["skills"]:
                    return {
                        "success": False,
                        "error": f"Requires {prerequisite} skill"
                    }
            
            # Check requirements
            requirements = skill_def.get("requirements", {})
            
            # Check level requirement
            if "level" in requirements:
                player_level = self._calculate_player_level(player_id)
                if player_level < requirements["level"]:
                    return {
                        "success": False,
                        "error": f"Requires level {requirements['level']}"
                    }
            
            # Check skill points
            if player_data["skill_points"] < requirements.get("skill_points", 1):
                return {
                    "success": False,
                    "error": f"Not enough skill points"
                }
            
            # Check if already learned
            if skill_id in player_data["skills"]:
                return {
                    "success": False,
                    "error": f"Skill already learned"
                }
            
            return {
                "success": True,
                "skill_id": skill_id,
                "requirements_met": True,
                "message": "Can learn skill"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error checking skill requirements: {str(e)}"}
    
    def learn_skill(self, player_id: str, skill_id: str) -> Dict[str, Any]:
        """Learn a skill"""
        try:
            can_learn = self.can_learn_skill(player_id, skill_id)
            if not can_learn["success"]:
                return can_learn
            
            skill_def = self.get_skill(skill_id)
            player_data = self.get_player_skills(player_id)
            
            # Deduct skill points
            requirements = skill_def.get("requirements", {})
            skill_points_cost = requirements.get("skill_points", 1)
            player_data["skill_points"] -= skill_points_cost
            
            # Add skill to player
            player_data["skills"][skill_id] = {
                "level": 1,
                "xp": 0,
                "max_xp": skill_def["progression"]["xp_per_level"][0],
                "learned_at": datetime.now().isoformat(),
                "last_used": None
            }
            
            player_data["last_updated"] = datetime.now().isoformat()
            self._save_player_skills()
            
            return {
                "success": True,
                "skill_id": skill_id,
                "level": 1,
                "message": f"Learned {skill_def['name']}"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error learning skill: {str(e)}"}
    
    def gain_skill_xp(self, player_id: str, skill_id: str, xp_amount: int) -> Dict[str, Any]:
        """Gain experience points for a skill"""
        try:
            player_data = self.get_player_skills(player_id)
            
            if skill_id not in player_data["skills"]:
                return {"success": False, "error": f"Skill {skill_id} not learned"}
            
            skill_def = self.get_skill(skill_id)
            skill_data = player_data["skills"][skill_id]
            
            current_level = skill_data["level"]
            current_xp = skill_data["xp"]
            max_xp = skill_data["max_xp"]
            
            # Add XP
            new_xp = current_xp + xp_amount
            skill_data["xp"] = new_xp
            
            # Check for level up
            level_ups = 0
            while new_xp >= max_xp and current_level < skill_def["max_level"]:
                level_ups += 1
                current_level += 1
                new_xp -= max_xp
                
                # Update max XP for next level
                if current_level <= len(skill_def["progression"]["xp_per_level"]):
                    max_xp = skill_def["progression"]["xp_per_level"][current_level - 1]
                else:
                    max_xp = float('inf')  # Max level reached
            
            # Update skill data
            skill_data["level"] = current_level
            skill_data["xp"] = new_xp
            skill_data["max_xp"] = max_xp
            skill_data["last_used"] = datetime.now().isoformat()
            
            player_data["total_xp"] += xp_amount
            player_data["last_updated"] = datetime.now().isoformat()
            
            self._save_player_skills()
            
            return {
                "success": True,
                "skill_id": skill_id,
                "xp_gained": xp_amount,
                "new_level": current_level,
                "level_ups": level_ups,
                "message": f"Gained {xp_amount} XP in {skill_def['name']}"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error gaining skill XP: {str(e)}"}
    
    def get_skill_bonus(self, player_id: str, skill_id: str) -> Dict[str, Any]:
        """Get skill bonus for a player"""
        try:
            player_data = self.get_player_skills(player_id)
            
            if skill_id not in player_data["skills"]:
                return {"success": False, "error": f"Skill {skill_id} not learned"}
            
            skill_def = self.get_skill(skill_id)
            skill_data = player_data["skills"][skill_id]
            level = skill_data["level"]
            
            # Calculate bonuses
            bonuses = {}
            effects = skill_def.get("effects", {})
            
            for effect, base_value in effects.items():
                if effect.endswith("_bonus"):
                    progression = skill_def["progression"]["bonus_per_level"]
                    if level <= len(progression):
                        bonuses[effect] = base_value + progression[level - 1]
                    else:
                        bonuses[effect] = base_value + progression[-1]
                else:
                    bonuses[effect] = base_value
            
            return {
                "success": True,
                "skill_id": skill_id,
                "level": level,
                "bonuses": bonuses
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error getting skill bonus: {str(e)}"}
    
    def get_contextual_skill_actions(self, player_id: str, scenario_type: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get contextual skill actions based on scenario and context"""
        player_data = self.get_player_skills(player_id)
        contextual_actions = []
        
        # Check combat skills in combat
        if context.get("situation") == "combat":
            for skill_id in player_data["skills"]:
                skill_def = self.get_skill(skill_id)
                if skill_def and skill_def["type"] == SkillType.COMBAT.value:
                    skill_bonus = self.get_skill_bonus(player_id, skill_id)
                    if skill_bonus["success"]:
                        contextual_actions.append({
                            "type": "skill",
                            "description": f"⚔️ {skill_def['name']} kullan",
                            "action": "use_skill",
                            "skill_id": skill_id,
                            "context": "combat",
                            "dice": "1d20",
                            "bonus": skill_bonus["bonuses"].get("attack_bonus", 0)
                        })
        
        # Check social skills in social situations
        if context.get("situation") == "social":
            for skill_id in player_data["skills"]:
                skill_def = self.get_skill(skill_id)
                if skill_def and skill_def["type"] == SkillType.SOCIAL.value:
                    skill_bonus = self.get_skill_bonus(player_id, skill_id)
                    if skill_bonus["success"]:
                        contextual_actions.append({
                            "type": "skill",
                            "description": f"💬 {skill_def['name']} kullan",
                            "action": "use_skill",
                            "skill_id": skill_id,
                            "context": "social",
                            "dice": "1d20",
                            "bonus": skill_bonus["bonuses"].get("persuasion_bonus", 0)
                        })
        
        # Check stealth skills in stealth situations
        if context.get("situation") == "stealth":
            for skill_id in player_data["skills"]:
                skill_def = self.get_skill(skill_id)
                if skill_def and skill_def["type"] == SkillType.STEALTH.value:
                    skill_bonus = self.get_skill_bonus(player_id, skill_id)
                    if skill_bonus["success"]:
                        contextual_actions.append({
                            "type": "skill",
                            "description": f"👁️ {skill_def['name']} kullan",
                            "action": "use_skill",
                            "skill_id": skill_id,
                            "context": "stealth",
                            "dice": "1d20",
                            "bonus": skill_bonus["bonuses"].get("stealth_bonus", 0)
                        })
        
        return contextual_actions
    
    def _calculate_player_level(self, player_id: str) -> int:
        """Calculate player level based on total XP"""
        player_data = self.get_player_skills(player_id)
        total_xp = player_data.get("total_xp", 0)
        
        # Simple level calculation (1000 XP per level)
        level = 1 + (total_xp // 1000)
        return min(level, 20)  # Cap at level 20
    
    def get_available_skills(self, player_id: str) -> List[Dict[str, Any]]:
        """Get all skills available to the player"""
        available_skills = []
        player_data = self.get_player_skills(player_id)
        
        for skill_id, skill_def in self.skills.items():
            can_learn = self.can_learn_skill(player_id, skill_id)
            
            available_skills.append({
                "id": skill_id,
                "name": skill_def["name"],
                "type": skill_def["type"],
                "description": skill_def["description"],
                "difficulty": skill_def["difficulty"],
                "max_level": skill_def["max_level"],
                "requirements": skill_def.get("requirements", {}),
                "can_learn": can_learn["success"],
                "error": can_learn.get("error", ""),
                "learned": skill_id in player_data["skills"],
                "current_level": player_data["skills"].get(skill_id, {}).get("level", 0) if skill_id in player_data["skills"] else 0
            })
        
        return available_skills

    def get_skill_tree(self, character_class: str) -> Dict[str, Any]:
        """Get skill tree for a specific character class"""
        try:
            # Define skill trees for different character classes
            skill_trees = {
                "warrior": {
                    "class_name": "Savaşçı",
                    "description": "Savaş odaklı beceri ağacı",
                    "skills": [
                        {
                            "id": "weapon_mastery",
                            "name": "Silah Ustalığı",
                            "type": "combat",
                            "description": "Silahları etkili kullanma",
                            "max_level": 5,
                            "prerequisites": []
                        },
                        {
                            "id": "armor_training",
                            "name": "Zırh Eğitimi",
                            "type": "combat",
                            "description": "Zırh kullanma becerisi",
                            "max_level": 3,
                            "prerequisites": []
                        },
                        {
                            "id": "battle_tactics",
                            "name": "Savaş Taktikleri",
                            "type": "combat",
                            "description": "Savaş stratejileri",
                            "max_level": 4,
                            "prerequisites": ["weapon_mastery"]
                        }
                    ],
                    "current_skill_points": 5,
                    "max_skill_points": 20
                },
                "mage": {
                    "class_name": "Büyücü",
                    "description": "Büyü odaklı beceri ağacı",
                    "skills": [
                        {
                            "id": "spellcasting",
                            "name": "Büyü Yapma",
                            "type": "magic",
                            "description": "Büyü yapma becerisi",
                            "max_level": 5,
                            "prerequisites": []
                        },
                        {
                            "id": "magic_knowledge",
                            "name": "Büyü Bilgisi",
                            "type": "knowledge",
                            "description": "Büyü teorisi",
                            "max_level": 4,
                            "prerequisites": []
                        },
                        {
                            "id": "elemental_magic",
                            "name": "Elemental Büyü",
                            "type": "magic",
                            "description": "Elemental büyüler",
                            "max_level": 5,
                            "prerequisites": ["spellcasting"]
                        }
                    ],
                    "current_skill_points": 5,
                    "max_skill_points": 20
                },
                "rogue": {
                    "class_name": "Hırsız",
                    "description": "Gizlilik odaklı beceri ağacı",
                    "skills": [
                        {
                            "id": "stealth",
                            "name": "Gizlilik",
                            "type": "stealth",
                            "description": "Gizli hareket etme",
                            "max_level": 5,
                            "prerequisites": []
                        },
                        {
                            "id": "lockpicking",
                            "name": "Kilit Açma",
                            "type": "stealth",
                            "description": "Kilit açma becerisi",
                            "max_level": 4,
                            "prerequisites": []
                        },
                        {
                            "id": "trap_disarming",
                            "name": "Tuzak Etkisizleştirme",
                            "type": "stealth",
                            "description": "Tuzakları etkisizleştirme",
                            "max_level": 4,
                            "prerequisites": ["lockpicking"]
                        }
                    ],
                    "current_skill_points": 5,
                    "max_skill_points": 20
                },
                "cleric": {
                    "class_name": "Rahip",
                    "description": "İyileştirme odaklı beceri ağacı",
                    "skills": [
                        {
                            "id": "healing",
                            "name": "İyileştirme",
                            "type": "magic",
                            "description": "Yaraları iyileştirme",
                            "max_level": 5,
                            "prerequisites": []
                        },
                        {
                            "id": "divine_magic",
                            "name": "İlahi Büyü",
                            "type": "magic",
                            "description": "İlahi büyüler",
                            "max_level": 5,
                            "prerequisites": []
                        },
                        {
                            "id": "protection_magic",
                            "name": "Koruma Büyüsü",
                            "type": "magic",
                            "description": "Koruyucu büyüler",
                            "max_level": 4,
                            "prerequisites": ["divine_magic"]
                        }
                    ],
                    "current_skill_points": 5,
                    "max_skill_points": 20
                }
            }
            
            # Return the skill tree for the specified class
            if character_class in skill_trees:
                return skill_trees[character_class]
            else:
                # Return a default skill tree if class not found
                return {
                    "class_name": "Genel",
                    "description": "Genel beceri ağacı",
                    "skills": [
                        {
                            "id": "basic_combat",
                            "name": "Temel Savaş",
                            "type": "combat",
                            "description": "Temel savaş becerileri",
                            "max_level": 3,
                            "prerequisites": []
                        }
                    ],
                    "current_skill_points": 3,
                    "max_skill_points": 15
                }
                
        except Exception as e:
            print(f"Error getting skill tree: {e}")
            return None
