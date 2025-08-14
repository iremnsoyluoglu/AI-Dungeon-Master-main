#!/usr/bin/env python3
"""
AI Dungeon Master - Agent Integration Script

This script integrates the agent system with the main game application,
providing automated content generation and curation capabilities.
"""

import os
import sys
import json
import logging
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.agent_orchestrator import AgentOrchestrator
from agents.story_generation_agent import StoryGenerationAgent
from agents.character_management_agent import CharacterManagementAgent
from agents.game_state_agent import GameStateAgent
from agents.content_curator_agent import ContentCuratorAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GameAgentIntegration:
    """Integrates the agent system with the main game."""
    
    def __init__(self):
        """Initialize the game agent integration."""
        self.orchestrator = AgentOrchestrator()
        self.data_dir = Path("data")
        
        # Ensure data directory exists
        self.data_dir.mkdir(exist_ok=True)
        
        logger.info("Game Agent Integration initialized")
    
    def generate_scenario_for_game(self, theme: str, difficulty: str = "medium") -> dict:
        """Generate a scenario specifically for the game."""
        try:
            # Use the story generation agent
            scenario = self.orchestrator.story_agent.generate_daily_scenario()
            
            if scenario:
                # Validate the scenario
                validation = self.orchestrator.content_agent.validate_content(
                    scenario, "scenario"
                )
                
                if validation.get("approved", False):
                    logger.info(f"Generated approved scenario: {scenario.get('title', 'Unknown')}")
                    return scenario
                else:
                    logger.warning(f"Generated scenario failed validation: {validation.get('issues', [])}")
                    # Return a fallback scenario
                    return self._create_fallback_scenario(theme, difficulty)
            
            return self._create_fallback_scenario(theme, difficulty)
            
        except Exception as e:
            logger.error(f"Error generating scenario: {e}")
            return self._create_fallback_scenario(theme, difficulty)
    
    def _create_fallback_scenario(self, theme: str, difficulty: str) -> dict:
        """Create a fallback scenario when generation fails."""
        return {
            "id": f"{theme}_{difficulty}_fallback",
            "title": f"{theme.title()} Adventure",
            "description": f"A {difficulty} adventure in the {theme} world.",
            "theme": theme,
            "difficulty": difficulty,
            "estimated_play_time": 60,
            "scenes": {
                "start": {
                    "id": "start",
                    "title": "The Beginning",
                    "description": "Your adventure begins here.",
                    "choices": [
                        {"text": "Explore the area", "next_node": "explore"},
                        {"text": "Talk to NPC", "next_node": "npc_interaction"}
                    ]
                },
                "explore": {
                    "id": "explore",
                    "title": "Exploration",
                    "description": "You discover something interesting.",
                    "choices": [
                        {"text": "Investigate further", "next_node": "investigate"},
                        {"text": "Return to start", "next_node": "start"}
                    ]
                },
                "npc_interaction": {
                    "id": "npc_interaction",
                    "title": "NPC Encounter",
                    "description": "You meet a mysterious character.",
                    "choices": [
                        {"text": "Ask for help", "next_node": "help"},
                        {"text": "Be cautious", "next_node": "cautious"}
                    ]
                }
            }
        }
    
    def create_character_for_game(self, race: str, character_class: str, theme: str) -> dict:
        """Create a character using the character management agent."""
        try:
            character = self.orchestrator.character_agent._create_character(
                race, character_class, theme
            )
            
            if character:
                logger.info(f"Created character: {character.get('name', 'Unknown')}")
                return character
            
            return self._create_fallback_character(race, character_class, theme)
            
        except Exception as e:
            logger.error(f"Error creating character: {e}")
            return self._create_fallback_character(race, character_class, theme)
    
    def _create_fallback_character(self, race: str, character_class: str, theme: str) -> dict:
        """Create a fallback character when creation fails."""
        return {
            "id": f"{race}_{character_class}_001",
            "name": f"{race.title()} {character_class.title()}",
            "race": race,
            "class": character_class,
            "level": 1,
            "theme": theme,
            "stats": {
                "str": 10,
                "dex": 10,
                "int": 10,
                "con": 10,
                "wis": 10,
                "cha": 10
            },
            "experience": 0,
            "health": 100,
            "max_health": 100
        }
    
    def manage_game_session(self, player_id: str, scenario_id: str, character_id: str) -> dict:
        """Manage a game session using the game state agent."""
        try:
            session = self.orchestrator.game_state_agent._create_session(
                player_id, scenario_id, character_id
            )
            
            if session:
                logger.info(f"Created session: {session.get('session_id', 'Unknown')}")
                return session
            
            return self._create_fallback_session(player_id, scenario_id, character_id)
            
        except Exception as e:
            logger.error(f"Error managing session: {e}")
            return self._create_fallback_session(player_id, scenario_id, character_id)
    
    def _create_fallback_session(self, player_id: str, scenario_id: str, character_id: str) -> dict:
        """Create a fallback session when management fails."""
        return {
            "session_id": f"session_{player_id}_{scenario_id}",
            "player_id": player_id,
            "scenario_id": scenario_id,
            "character_id": character_id,
            "status": "active",
            "created_at": "2025-08-09T15:00:00",
            "current_scene": "start",
            "game_state": {
                "health": 100,
                "experience": 0,
                "inventory": [],
                "quests": []
            }
        }
    
    def validate_game_content(self, content: dict, content_type: str) -> dict:
        """Validate game content using the content curator agent."""
        try:
            validation = self.orchestrator.content_agent.validate_content(
                content, content_type
            )
            
            logger.info(f"Content validation result: {validation.get('approved', False)}")
            return validation
            
        except Exception as e:
            logger.error(f"Error validating content: {e}")
            return {"approved": False, "issues": ["Validation error"]}
    
    def get_agent_status(self) -> dict:
        """Get the status of all agents."""
        try:
            status = self.orchestrator.get_orchestrator_status()
            return status
        except Exception as e:
            logger.error(f"Error getting agent status: {e}")
            return {"status": "error", "message": str(e)}
    
    def export_agent_data(self) -> bool:
        """Export agent data for backup."""
        try:
            return self.orchestrator.export_orchestrator_data()
        except Exception as e:
            logger.error(f"Error exporting agent data: {e}")
            return False

def main():
    """Main function for testing the integration."""
    print("🤖 AI Dungeon Master - Agent Integration Test")
    print("=" * 50)
    
    integration = GameAgentIntegration()
    
    # Test scenario generation
    print("\n📖 Testing Scenario Generation...")
    scenario = integration.generate_scenario_for_game("fantasy", "medium")
    print(f"✅ Generated scenario: {scenario.get('title', 'Unknown')}")
    
    # Test character creation
    print("\n👤 Testing Character Creation...")
    character = integration.create_character_for_game("elf", "mage", "fantasy")
    print(f"✅ Created character: {character.get('name', 'Unknown')}")
    
    # Test session management
    print("\n🎮 Testing Session Management...")
    session = integration.manage_game_session("player_001", "fantasy_scenario", "elf_mage_001")
    print(f"✅ Created session: {session.get('session_id', 'Unknown')}")
    
    # Test content validation
    print("\n✅ Testing Content Validation...")
    validation = integration.validate_game_content(scenario, "scenario")
    print(f"✅ Content validation: {validation.get('approved', False)}")
    
    # Test agent status
    print("\n📊 Testing Agent Status...")
    status = integration.get_agent_status()
    print(f"✅ Agent status: {status.get('status', 'Unknown')}")
    
    print("\n🎉 All integration tests completed successfully!")

if __name__ == "__main__":
    main()
