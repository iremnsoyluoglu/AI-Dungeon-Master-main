#!/usr/bin/env python3
"""
Advanced Save/Load System
Handles game state persistence, character saves, and campaign progress
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class SaveGameData:
    """Complete save game data structure"""
    save_id: str
    timestamp: datetime
    game_version: str
    character_data: Dict[str, Any]
    game_state: Dict[str, Any]
    campaign_progress: Dict[str, Any]
    npc_relationships: Dict[str, Any]
    skill_progress: Dict[str, Any]
    moral_alignment: Dict[str, Any]
    inventory: List[str]
    quest_progress: Dict[str, Any]
    combat_state: Optional[Dict[str, Any]] = None
    session_data: Optional[Dict[str, Any]] = None

class SaveSystem:
    """Advanced save/load system for the game"""
    
    def __init__(self, save_directory: str = "saves"):
        self.save_directory = Path(save_directory)
        self.save_directory.mkdir(exist_ok=True)
        self.game_version = "1.0.0"
        
    def save_game(self, 
                  character_id: str,
                  game_engine: Any,
                  campaign_manager: Any,
                  session_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Save complete game state"""
        try:
            # Get character data
            character = game_engine.get_character(character_id)
            if not character:
                return {"success": False, "error": "Character not found"}
            
            # Create save data
            save_data = SaveGameData(
                save_id=f"save_{character_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                timestamp=datetime.now(),
                game_version=self.game_version,
                character_data=character,
                game_state=self._get_game_state(game_engine, character_id),
                campaign_progress=self._get_campaign_progress(campaign_manager, character_id),
                npc_relationships=self._get_npc_relationships(game_engine, character_id),
                skill_progress=self._get_skill_progress(game_engine, character_id),
                moral_alignment=self._get_moral_alignment(game_engine, character_id),
                inventory=character.get("inventory", []),
                quest_progress=self._get_quest_progress(campaign_manager, character_id),
                combat_state=self._get_combat_state(game_engine, character_id),
                session_data=session_data
            )
            
            # Save to file
            save_file = self.save_directory / f"{save_data.save_id}.json"
            with open(save_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(save_data), f, indent=2, default=str)
            
            logger.info(f"Game saved successfully: {save_data.save_id}")
            return {
                "success": True,
                "save_id": save_data.save_id,
                "timestamp": save_data.timestamp.isoformat(),
                "character_name": character.name
            }
            
        except Exception as e:
            logger.error(f"Error saving game: {e}")
            return {"success": False, "error": str(e)}
    
    def load_game(self, save_id: str, game_engine: Any, campaign_manager: Any) -> Dict[str, Any]:
        """Load complete game state"""
        try:
            # Load save file
            save_file = self.save_directory / f"{save_id}.json"
            if not save_file.exists():
                return {"success": False, "error": "Save file not found"}
            
            with open(save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # Restore character
            character_data = save_data["character_data"]
            character = game_engine.get_character(character_data["id"])
            if character:
                # Update character with saved data
                character.hp = character_data["hp"]
                character.mana = character_data["mana"]
                character.xp = character_data["xp"]
                character.level = character_data["level"]
                character.skill_points = character_data["skill_points"]
                character.inventory = character_data["inventory"]
                character.skills = character_data["skills"]
                character.equipment = character_data["equipment"]
                
                # Restore stats
                character.stats.strength = character_data["stats"]["strength"]
                character.stats.dexterity = character_data["stats"]["dexterity"]
                character.stats.constitution = character_data["stats"]["constitution"]
                character.stats.intelligence = character_data["stats"]["intelligence"]
                character.stats.wisdom = character_data["stats"]["wisdom"]
                character.stats.charisma = character_data["stats"]["charisma"]
            
            # Restore NPC relationships
            if "npc_relationships" in save_data:
                self._restore_npc_relationships(game_engine, character_data["id"], save_data["npc_relationships"])
            
            # Restore moral alignment
            if "moral_alignment" in save_data:
                self._restore_moral_alignment(game_engine, character_data["id"], save_data["moral_alignment"])
            
            logger.info(f"Game loaded successfully: {save_id}")
            return {
                "success": True,
                "save_id": save_id,
                "character_name": character_data["name"],
                "timestamp": save_data["timestamp"]
            }
            
        except Exception as e:
            logger.error(f"Error loading game: {e}")
            return {"success": False, "error": str(e)}
    
    def get_save_files(self, character_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of available save files"""
        saves = []
        
        for save_file in self.save_directory.glob("*.json"):
            try:
                with open(save_file, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)
                
                # Filter by character if specified
                if character_id and save_data["character_data"]["id"] != character_id:
                    continue
                
                saves.append({
                    "save_id": save_data["save_id"],
                    "timestamp": save_data["timestamp"],
                    "character_name": save_data["character_data"]["name"],
                    "character_level": save_data["character_data"]["level"],
                    "character_class": save_data["character_data"]["character_class"],
                    "file_size": save_file.stat().st_size
                })
                
            except Exception as e:
                logger.warning(f"Error reading save file {save_file}: {e}")
        
        # Sort by timestamp (newest first)
        saves.sort(key=lambda x: x["timestamp"], reverse=True)
        return saves
    
    def delete_save(self, save_id: str) -> Dict[str, Any]:
        """Delete a save file"""
        try:
            save_file = self.save_directory / f"{save_id}.json"
            if save_file.exists():
                save_file.unlink()
                logger.info(f"Save file deleted: {save_id}")
                return {"success": True, "message": "Save file deleted"}
            else:
                return {"success": False, "error": "Save file not found"}
                
        except Exception as e:
            logger.error(f"Error deleting save file: {e}")
            return {"success": False, "error": str(e)}
    
    def auto_save(self, character_id: str, game_engine: Any, campaign_manager: Any) -> Dict[str, Any]:
        """Create an auto-save"""
        try:
            # Create auto-save with special ID
            auto_save_id = f"autosave_{character_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Save game with auto-save ID
            result = self.save_game(character_id, game_engine, campaign_manager)
            if result["success"]:
                # Rename to auto-save
                old_file = self.save_directory / f"{result['save_id']}.json"
                new_file = self.save_directory / f"{auto_save_id}.json"
                old_file.rename(new_file)
                
                logger.info(f"Auto-save created: {auto_save_id}")
                return {"success": True, "auto_save_id": auto_save_id}
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error creating auto-save: {e}")
            return {"success": False, "error": str(e)}
    
    def _get_game_state(self, game_engine: Any, character_id: str) -> Dict[str, Any]:
        """Get current game state"""
        return {
            "active_sessions": game_engine.active_sessions(),
            "combat_sessions": list(game_engine.combat_systems.keys()) if hasattr(game_engine, 'combat_systems') else [],
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_campaign_progress(self, campaign_manager: Any, character_id: str) -> Dict[str, Any]:
        """Get campaign progress"""
        # This would be implemented based on campaign manager
        return {
            "current_campaign": "default",
            "completed_scenes": [],
            "current_scene": 0,
            "total_scenes": 10
        }
    
    def _get_npc_relationships(self, game_engine: Any, character_id: str) -> Dict[str, Any]:
        """Get NPC relationship data"""
        try:
            relationships = game_engine.get_all_npc_relationships(character_id)
            return relationships
        except:
            return {}
    
    def _get_skill_progress(self, game_engine: Any, character_id: str) -> Dict[str, Any]:
        """Get skill progression data"""
        try:
            progression = game_engine.get_skill_progression(character_id)
            return progression
        except:
            return {}
    
    def _get_moral_alignment(self, game_engine: Any, character_id: str) -> Dict[str, Any]:
        """Get moral alignment data"""
        try:
            moral_status = game_engine.get_player_moral_status(character_id)
            return moral_status
        except:
            return {}
    
    def _get_quest_progress(self, campaign_manager: Any, character_id: str) -> Dict[str, Any]:
        """Get quest progress"""
        return {
            "active_quests": [],
            "completed_quests": [],
            "quest_points": 0
        }
    
    def _get_combat_state(self, game_engine: Any, character_id: str) -> Optional[Dict[str, Any]]:
        """Get current combat state"""
        # Check if character is in combat
        for session_id, combat_system in game_engine.combat_systems.items():
            for participant in combat_system.participants:
                if participant["character"].id == character_id:
                    return {
                        "session_id": session_id,
                        "current_turn": combat_system.current_turn,
                        "round": combat_system.round,
                        "participants": len(combat_system.participants)
                    }
        return None
    
    def _restore_npc_relationships(self, game_engine: Any, character_id: str, relationships: Dict[str, Any]):
        """Restore NPC relationships"""
        try:
            # This would restore NPC relationship data
            # Implementation depends on NPC system structure
            pass
        except Exception as e:
            logger.warning(f"Could not restore NPC relationships: {e}")
    
    def _restore_moral_alignment(self, game_engine: Any, character_id: str, moral_data: Dict[str, Any]):
        """Restore moral alignment"""
        try:
            # This would restore moral alignment data
            # Implementation depends on moral system structure
            pass
        except Exception as e:
            logger.warning(f"Could not restore moral alignment: {e}")
    
    def export_save(self, save_id: str, export_path: str) -> Dict[str, Any]:
        """Export save file to external location"""
        try:
            save_file = self.save_directory / f"{save_id}.json"
            if not save_file.exists():
                return {"success": False, "error": "Save file not found"}
            
            import shutil
            shutil.copy2(save_file, export_path)
            
            logger.info(f"Save exported to: {export_path}")
            return {"success": True, "export_path": export_path}
            
        except Exception as e:
            logger.error(f"Error exporting save: {e}")
            return {"success": False, "error": str(e)}
    
    def import_save(self, import_path: str) -> Dict[str, Any]:
        """Import save file from external location"""
        try:
            import shutil
            import pathlib
            
            # Validate file
            import_file = pathlib.Path(import_path)
            if not import_file.exists():
                return {"success": False, "error": "Import file not found"}
            
            # Read and validate save data
            with open(import_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # Validate save data structure
            required_fields = ["save_id", "character_data", "game_state"]
            for field in required_fields:
                if field not in save_data:
                    return {"success": False, "error": f"Invalid save file: missing {field}"}
            
            # Copy to save directory
            save_id = save_data["save_id"]
            target_file = self.save_directory / f"{save_id}.json"
            shutil.copy2(import_file, target_file)
            
            logger.info(f"Save imported: {save_id}")
            return {"success": True, "save_id": save_id}
            
        except Exception as e:
            logger.error(f"Error importing save: {e}")
            return {"success": False, "error": str(e)} 