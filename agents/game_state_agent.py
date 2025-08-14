"""
Game State Agent

This agent is responsible for managing game state, session data,
progression tracking, and game mechanics coordination.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import StringPromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GameStateAgent:
    """
    Agent responsible for game state management and session coordination.
    
    Capabilities:
    - Track game sessions and player progress
    - Manage save/load functionality
    - Coordinate game mechanics and rules
    - Handle multiplayer session management
    - Monitor game performance and analytics
    """
    
    def __init__(self, api_key: str = None):
        """Initialize the Game State Agent."""
        self.api_key = api_key
        self.llm = OpenAI(temperature=0.5, api_key=api_key) if api_key else None
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.active_sessions = {}
        self.game_rules = self._load_game_rules()
        self.analytics = {
            "sessions_created": 0,
            "total_play_time": 0,
            "scenarios_completed": 0,
            "characters_created": 0
        }
        
        # Initialize tools
        self.tools = self._initialize_tools()
        
        # Initialize agent
        self.agent = self._initialize_agent()
    
    def _load_game_rules(self) -> Dict[str, Any]:
        """Load game rules and mechanics."""
        return {
            "leveling": {
                "xp_per_level": 100,
                "stat_points_per_level": 1,
                "max_level": 20
            },
            "combat": {
                "dice_type": "d20",
                "critical_success": 20,
                "critical_failure": 1,
                "advantage_threshold": 15
            },
            "storytelling": {
                "betrayal_chance": 0.1,
                "plot_twist_chance": 0.15,
                "random_event_chance": 0.2
            },
            "saving": {
                "auto_save_interval": 300,  # 5 minutes
                "max_save_slots": 10,
                "save_retention_days": 30
            }
        }
    
    def _initialize_tools(self) -> List[Tool]:
        """Initialize agent tools."""
        return [
            Tool(
                name="create_session",
                func=self._create_session,
                description="Create a new game session"
            ),
            Tool(
                name="save_game_state",
                func=self._save_game_state,
                description="Save current game state"
            ),
            Tool(
                name="load_game_state",
                func=self._load_game_state,
                description="Load game state from save"
            ),
            Tool(
                name="update_session_progress",
                func=self._update_session_progress,
                description="Update session progress and analytics"
            ),
            Tool(
                name="validate_game_rules",
                func=self._validate_game_rules,
                description="Validate game actions against rules"
            )
        ]
    
    def _initialize_agent(self) -> AgentExecutor:
        """Initialize the LangChain agent."""
        if not self.llm:
            logger.warning("No LLM configured - agent will use rule-based management")
            return None
            
        prompt = StringPromptTemplate(
            input_variables=["input", "chat_history", "agent_scratchpad"],
            template="""
            You are a Game State Agent for an AI Dungeon Master game.
            Your role is to manage game sessions, state, and progression.
            
            Chat History: {chat_history}
            Human: {input}
            Agent: {agent_scratchpad}
            
            Use the available tools to manage game state and ensure proper
            game mechanics and session coordination.
            """
        )
        
        agent = LLMSingleActionAgent(
            llm_chain=LLMChain(llm=self.llm, prompt=prompt),
            allowed_tools=[tool.name for tool in self.tools],
            stop=["\nHuman:"],
            memory=self.memory
        )
        
        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            verbose=True
        )
    
    def _create_session(self, player_id: str, scenario_id: str, character_id: str) -> Dict[str, Any]:
        """Create a new game session."""
        logger.info(f"Creating session for player {player_id} with scenario {scenario_id}")
        
        session_id = f"session_{player_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session = {
            "session_id": session_id,
            "player_id": player_id,
            "scenario_id": scenario_id,
            "character_id": character_id,
            "created_at": datetime.now().isoformat(),
            "current_scene": "start",
            "game_state": {
                "level": 1,
                "xp": 0,
                "karma": 0,
                "current_scene": "start",
                "emotional_arcs": {
                    "trust_building": "suspicion",
                    "power_progression": "weakness"
                },
                "relationships": {},
                "hidden_flags": [],
                "ending_path": None,
                "betrayal_count": 0,
                "plot_twist_count": 0
            },
            "session_data": {
                "play_time": 0,
                "choices_made": [],
                "events_triggered": [],
                "last_save": datetime.now().isoformat()
            },
            "status": "active"
        }
        
        self.active_sessions[session_id] = session
        self.analytics["sessions_created"] += 1
        
        logger.info(f"Session created: {session_id}")
        return session
    
    def _save_game_state(self, session_id: str, save_slot: str = "auto") -> bool:
        """Save current game state."""
        logger.info(f"Saving game state for session {session_id}")
        
        if session_id not in self.active_sessions:
            logger.error(f"Session not found: {session_id}")
            return False
        
        session = self.active_sessions[session_id]
        
        # Update last save time
        session["session_data"]["last_save"] = datetime.now().isoformat()
        
        # Create save data
        save_data = {
            "session_id": session_id,
            "save_slot": save_slot,
            "saved_at": datetime.now().isoformat(),
            "game_state": session["game_state"],
            "session_data": session["session_data"]
        }
        
        # Save to file
        filename = f"saves/save_{session_id}_{save_slot}.json"
        try:
            import os
            os.makedirs("saves", exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Game state saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving game state: {e}")
            return False
    
    def _load_game_state(self, session_id: str, save_slot: str = "auto") -> Optional[Dict[str, Any]]:
        """Load game state from save."""
        logger.info(f"Loading game state for session {session_id}")
        
        filename = f"saves/save_{session_id}_{save_slot}.json"
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # Update active session
            if session_id in self.active_sessions:
                self.active_sessions[session_id]["game_state"] = save_data["game_state"]
                self.active_sessions[session_id]["session_data"] = save_data["session_data"]
            
            logger.info(f"Game state loaded from {filename}")
            return save_data
        except Exception as e:
            logger.error(f"Error loading game state: {e}")
            return None
    
    def _update_session_progress(self, session_id: str, action: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Update session progress and analytics."""
        logger.info(f"Updating session progress: {session_id} - {action}")
        
        if session_id not in self.active_sessions:
            logger.error(f"Session not found: {session_id}")
            return None
        
        session = self.active_sessions[session_id]
        
        # Update session data
        if data:
            session["session_data"].update(data)
        
        # Track choice
        if action == "choice_made":
            session["session_data"]["choices_made"].append({
                "timestamp": datetime.now().isoformat(),
                "choice": data.get("choice", "unknown")
            })
        
        # Track event
        elif action == "event_triggered":
            session["session_data"]["events_triggered"].append({
                "timestamp": datetime.now().isoformat(),
                "event": data.get("event", "unknown")
            })
        
        # Update play time
        elif action == "play_time_update":
            play_time = data.get("play_time", 0)
            session["session_data"]["play_time"] += play_time
            self.analytics["total_play_time"] += play_time
        
        # Update game state
        elif action == "game_state_update":
            session["game_state"].update(data.get("game_state", {}))
        
        return session
    
    def _validate_game_rules(self, action: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate game actions against rules."""
        logger.info(f"Validating game rules for action: {action}")
        
        validation_result = {
            "valid": True,
            "message": "Action is valid",
            "modifications": {}
        }
        
        if action == "level_up":
            current_level = data.get("current_level", 1)
            current_xp = data.get("current_xp", 0)
            required_xp = current_level * self.game_rules["leveling"]["xp_per_level"]
            
            if current_xp < required_xp:
                validation_result["valid"] = False
                validation_result["message"] = f"Insufficient XP for level up. Need {required_xp}, have {current_xp}"
        
        elif action == "dice_roll":
            dice_result = data.get("result", 0)
            if dice_result < 1 or dice_result > 20:
                validation_result["valid"] = False
                validation_result["message"] = "Invalid dice result"
        
        elif action == "save_game":
            session_id = data.get("session_id")
            if session_id and session_id not in self.active_sessions:
                validation_result["valid"] = False
                validation_result["message"] = "Invalid session ID"
        
        return validation_result
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get a session by ID."""
        return self.active_sessions.get(session_id)
    
    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """Get all active sessions."""
        return list(self.active_sessions.values())
    
    def end_session(self, session_id: str) -> bool:
        """End a game session."""
        logger.info(f"Ending session: {session_id}")
        
        if session_id not in self.active_sessions:
            logger.error(f"Session not found: {session_id}")
            return False
        
        session = self.active_sessions[session_id]
        session["status"] = "ended"
        session["ended_at"] = datetime.now().isoformat()
        
        # Save final state
        self._save_game_state(session_id, "final")
        
        # Remove from active sessions
        del self.active_sessions[session_id]
        
        return True
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get game analytics."""
        return {
            **self.analytics,
            "active_sessions": len(self.active_sessions),
            "last_updated": datetime.now().isoformat()
        }
    
    def export_session_data(self, session_id: str, filename: str = None) -> bool:
        """Export session data to file."""
        if session_id not in self.active_sessions:
            logger.error(f"Session not found: {session_id}")
            return False
        
        if not filename:
            filename = f"session_export_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            session_data = {
                "session": self.active_sessions[session_id],
                "analytics": self.get_analytics(),
                "exported_at": datetime.now().isoformat()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Session data exported to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error exporting session data: {e}")
            return False

# Example usage
if __name__ == "__main__":
    # Initialize the agent
    agent = GameStateAgent()
    
    # Create a session
    session = agent._create_session("player_001", "fantasy_scenario_1", "elf_mage_001")
    print(f"Created session: {session['session_id']}")
    
    # Update progress
    agent._update_session_progress(session['session_id'], "choice_made", {"choice": "explore"})
    
    # Save game state
    agent._save_game_state(session['session_id'])
    
    # Get analytics
    analytics = agent.get_analytics()
    print(f"Analytics: {analytics}")
