#!/usr/bin/env python3
"""
Level System for AI Dungeon Master
Handles character progression, experience points, and level-based unlocks
"""

import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class LevelRequirement:
    level: int
    experience_required: int
    skill_points_gained: int
    stat_bonuses: Dict[str, int]
    unlocks: List[str]

@dataclass
class CharacterProgression:
    level: int
    experience: int
    experience_to_next: int
    skill_points: int
    total_skill_points: int
    stat_bonuses: Dict[str, int]
    unlocked_features: List[str]

class LevelSystem:
    """Manages character level progression and experience"""
    
    def __init__(self):
        self.level_requirements_file = "data/level_requirements.json"
        self._ensure_data_directory()
        self._load_level_requirements()
        self._initialize_default_requirements()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        import os
        os.makedirs("data", exist_ok=True)
    
    def _load_level_requirements(self):
        """Load level requirements from file"""
        try:
            import os
            if os.path.exists(self.level_requirements_file):
                with open(self.level_requirements_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.level_requirements = {}
                    for level, req_data in data.items():
                        self.level_requirements[int(level)] = LevelRequirement(**req_data)
            else:
                self.level_requirements = {}
        except Exception as e:
            print(f"Error loading level requirements: {e}")
            self.level_requirements = {}
    
    def _save_level_requirements(self):
        """Save level requirements to file"""
        try:
            with open(self.level_requirements_file, 'w', encoding='utf-8') as f:
                data = {str(level): asdict(req) for level, req in self.level_requirements.items()}
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving level requirements: {e}")
    
    def _initialize_default_requirements(self):
        """Initialize default level requirements if none exist"""
        if not self.level_requirements:
            self.level_requirements = {
                1: LevelRequirement(1, 0, 0, {}, []),
                2: LevelRequirement(2, 100, 2, {"hp": 10, "attack": 2}, ["basic_skills"]),
                3: LevelRequirement(3, 250, 2, {"hp": 15, "defense": 2}, ["combat_skills"]),
                4: LevelRequirement(4, 450, 3, {"hp": 20, "attack": 3}, ["magic_skills"]),
                5: LevelRequirement(5, 700, 3, {"hp": 25, "defense": 3}, ["advanced_skills"]),
                6: LevelRequirement(6, 1000, 4, {"hp": 30, "attack": 4}, ["ultimate_skills"]),
                7: LevelRequirement(7, 1350, 4, {"hp": 35, "defense": 4}, ["specialization"]),
                8: LevelRequirement(8, 1750, 5, {"hp": 40, "attack": 5}, ["mastery"]),
                9: LevelRequirement(9, 2200, 5, {"hp": 45, "defense": 5}, ["legendary_skills"]),
                10: LevelRequirement(10, 2700, 6, {"hp": 50, "attack": 6, "defense": 6}, ["epic_skills"])
            }
            self._save_level_requirements()
    
    def calculate_experience_gain(self, action_type: str, difficulty: str, 
                                success: bool, bonus_multiplier: float = 1.0) -> int:
        """Calculate experience gain for an action"""
        base_xp = {
            "combat": {"easy": 10, "medium": 25, "hard": 50, "epic": 100},
            "exploration": {"easy": 5, "medium": 15, "hard": 30, "epic": 60},
            "social": {"easy": 3, "medium": 10, "hard": 20, "epic": 40},
            "quest": {"easy": 20, "medium": 50, "hard": 100, "epic": 200},
            "skill_check": {"easy": 2, "medium": 5, "hard": 10, "epic": 20}
        }
        
        base = base_xp.get(action_type, {}).get(difficulty, 10)
        
        # Success bonus
        if success:
            base = int(base * 1.5)
        else:
            base = int(base * 0.3)  # Partial XP for failure
        
        # Apply bonus multiplier
        final_xp = int(base * bonus_multiplier)
        
        return max(1, final_xp)  # Minimum 1 XP
    
    def add_experience(self, character_data: Dict[str, Any], xp_gained: int) -> Dict[str, Any]:
        """Add experience to character and check for level up"""
        current_level = character_data.get("level", 1)
        current_xp = character_data.get("experience", 0)
        
        new_xp = current_xp + xp_gained
        new_level = current_level
        
        # Check for level ups
        while new_level < 10 and new_xp >= self.level_requirements[new_level + 1].experience_required:
            new_level += 1
        
        # Calculate experience to next level
        if new_level < 10:
            xp_to_next = self.level_requirements[new_level + 1].experience_required - new_xp
        else:
            xp_to_next = 0
        
        # Calculate skill points gained
        skill_points_gained = 0
        for level in range(current_level + 1, new_level + 1):
            if level in self.level_requirements:
                skill_points_gained += self.level_requirements[level].skill_points_gained
        
        # Update character data
        character_data["level"] = new_level
        character_data["experience"] = new_xp
        character_data["experience_to_next"] = xp_to_next
        character_data["skill_points"] = character_data.get("skill_points", 0) + skill_points_gained
        character_data["total_skill_points"] = character_data.get("total_skill_points", 0) + skill_points_gained
        
        # Add stat bonuses for new levels
        for level in range(current_level + 1, new_level + 1):
            if level in self.level_requirements:
                req = self.level_requirements[level]
                for stat, bonus in req.stat_bonuses.items():
                    if stat == "hp":
                        character_data["max_health"] = character_data.get("max_health", 100) + bonus
                        character_data["health"] = character_data.get("health", 100) + bonus
                    elif stat == "attack":
                        character_data["attack"] = character_data.get("attack", 10) + bonus
                    elif stat == "defense":
                        character_data["defense"] = character_data.get("defense", 5) + bonus
        
        return {
            "success": True,
            "character_data": character_data,
            "level_up": new_level > current_level,
            "levels_gained": new_level - current_level,
            "skill_points_gained": skill_points_gained,
            "xp_gained": xp_gained,
            "message": f"Gained {xp_gained} XP. Level: {current_level} → {new_level}"
        }
    
    def get_level_progression(self, character_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed level progression information"""
        level = character_data.get("level", 1)
        experience = character_data.get("experience", 0)
        
        if level >= 10:
            return {
                "level": level,
                "experience": experience,
                "experience_to_next": 0,
                "progress_percentage": 100,
                "max_level": True,
                "skill_points": character_data.get("skill_points", 0),
                "total_skill_points": character_data.get("total_skill_points", 0)
            }
        
        next_level_req = self.level_requirements.get(level + 1)
        if not next_level_req:
            return {"error": "Level requirements not found"}
        
        current_level_req = self.level_requirements.get(level, LevelRequirement(level, 0, 0, {}, []))
        
        xp_in_current_level = experience - current_level_req.experience_required
        xp_needed_for_next = next_level_req.experience_required - current_level_req.experience_required
        progress_percentage = min(100, (xp_in_current_level / xp_needed_for_next) * 100) if xp_needed_for_next > 0 else 100
        
        return {
            "level": level,
            "experience": experience,
            "experience_to_next": next_level_req.experience_required - experience,
            "progress_percentage": progress_percentage,
            "max_level": False,
            "skill_points": character_data.get("skill_points", 0),
            "total_skill_points": character_data.get("total_skill_points", 0),
            "next_level_bonuses": next_level_req.stat_bonuses,
            "next_level_unlocks": next_level_req.unlocks
        }
    
    def get_level_requirements(self) -> Dict[str, Any]:
        """Get all level requirements"""
        return {
            str(level): asdict(req) for level, req in self.level_requirements.items()
        }
    
    def can_unlock_feature(self, character_data: Dict[str, Any], feature: str) -> bool:
        """Check if character can unlock a feature based on level"""
        level = character_data.get("level", 1)
        
        for req_level, req in self.level_requirements.items():
            if req_level <= level and feature in req.unlocks:
                return True
        
        return False
    
    def get_available_unlocks(self, character_data: Dict[str, Any]) -> List[str]:
        """Get all available unlocks for character level"""
        level = character_data.get("level", 1)
        unlocks = []
        
        for req_level, req in self.level_requirements.items():
            if req_level <= level:
                unlocks.extend(req.unlocks)
        
        return list(set(unlocks))  # Remove duplicates
    
    def get_level_bonuses(self, character_data: Dict[str, Any]) -> Dict[str, int]:
        """Get total stat bonuses from all levels"""
        level = character_data.get("level", 1)
        total_bonuses = {"hp": 0, "attack": 0, "defense": 0}
        
        for req_level, req in self.level_requirements.items():
            if req_level <= level:
                for stat, bonus in req.stat_bonuses.items():
                    if stat in total_bonuses:
                        total_bonuses[stat] += bonus
        
        return total_bonuses 