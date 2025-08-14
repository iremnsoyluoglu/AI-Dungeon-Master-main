"""
Character Management Agent

This agent is responsible for managing character creation, progression,
NPC interactions, and character-related game mechanics.
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

class CharacterManagementAgent:
    """
    Agent responsible for character management and NPC interactions.
    
    Capabilities:
    - Generate character backstories and personalities
    - Manage character progression and leveling
    - Create and manage NPCs
    - Handle character relationships and interactions
    - Generate character-specific dialogue and responses
    """
    
    def __init__(self, api_key: str = None):
        """Initialize the Character Management Agent."""
        self.api_key = api_key
        self.llm = OpenAI(temperature=0.7, api_key=api_key) if api_key else None
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.characters = {}
        self.npcs = {}
        self.character_templates = self._load_character_templates()
        
        # Initialize tools
        self.tools = self._initialize_tools()
        
        # Initialize agent
        self.agent = self._initialize_agent()
    
    def _load_character_templates(self) -> Dict[str, Any]:
        """Load character generation templates."""
        return {
            "races": {
                "human": {
                    "description": "Versatile and adaptable",
                    "base_stats": {"str": 10, "dex": 10, "int": 10, "con": 10, "wis": 10, "cha": 10},
                    "traits": ["adaptable", "versatile", "ambitious"],
                    "names": ["Aiden", "Elena", "Marcus", "Sofia", "James", "Isabella"]
                },
                "elf": {
                    "description": "Graceful and magical",
                    "base_stats": {"str": 8, "dex": 12, "int": 12, "con": 8, "wis": 12, "cha": 10},
                    "traits": ["graceful", "magical", "ancient"],
                    "names": ["Thalindir", "Aeris", "Galadriel", "Legolas", "Arwen", "Elrond"]
                },
                "dwarf": {
                    "description": "Sturdy and skilled",
                    "base_stats": {"str": 12, "dex": 8, "int": 10, "con": 12, "wis": 10, "cha": 8},
                    "traits": ["sturdy", "skilled", "traditional"],
                    "names": ["Thorin", "Gimli", "Balin", "Dwalin", "Dís", "Fíli"]
                },
                "space_marine": {
                    "description": "Genetically enhanced super soldier",
                    "base_stats": {"str": 15, "dex": 12, "int": 10, "con": 15, "wis": 10, "cha": 8},
                    "traits": ["enhanced", "disciplined", "loyal"],
                    "names": ["Commander", "Captain", "Sergeant", "Brother", "Veteran", "Hero"]
                }
            },
            "classes": {
                "warrior": {
                    "description": "Master of combat",
                    "stat_bonuses": {"str": 2, "con": 1},
                    "abilities": ["weapon_mastery", "armor_training", "combat_tactics"],
                    "specializations": ["berserker", "knight", "ranger"]
                },
                "mage": {
                    "description": "Wielder of arcane magic",
                    "stat_bonuses": {"int": 2, "wis": 1},
                    "abilities": ["spellcasting", "magic_research", "elemental_control"],
                    "specializations": ["evoker", "illusionist", "necromancer"]
                },
                "rogue": {
                    "description": "Stealthy and agile",
                    "stat_bonuses": {"dex": 2, "int": 1},
                    "abilities": ["stealth", "lockpicking", "trap_detection"],
                    "specializations": ["assassin", "scout", "thief"]
                }
            }
        }
    
    def _initialize_tools(self) -> List[Tool]:
        """Initialize agent tools."""
        return [
            Tool(
                name="create_character",
                func=self._create_character,
                description="Create a new character with backstory and personality"
            ),
            Tool(
                name="generate_npc",
                func=self._generate_npc,
                description="Generate an NPC with personality and role"
            ),
            Tool(
                name="update_character_progression",
                func=self._update_character_progression,
                description="Update character stats and progression"
            ),
            Tool(
                name="generate_character_dialogue",
                func=self._generate_character_dialogue,
                description="Generate dialogue specific to a character"
            ),
            Tool(
                name="manage_character_relationships",
                func=self._manage_character_relationships,
                description="Manage relationships between characters"
            )
        ]
    
    def _initialize_agent(self) -> AgentExecutor:
        """Initialize the LangChain agent."""
        if not self.llm:
            logger.warning("No LLM configured - agent will use template-based generation")
            return None
            
        prompt = StringPromptTemplate(
            input_variables=["input", "chat_history", "agent_scratchpad"],
            template="""
            You are a Character Management Agent for an AI Dungeon Master game.
            Your role is to create and manage characters, NPCs, and their interactions.
            
            Chat History: {chat_history}
            Human: {input}
            Agent: {agent_scratchpad}
            
            Use the available tools to manage characters and create engaging NPCs.
            Always maintain character consistency and create believable personalities.
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
    
    def _create_character(self, race: str, class_name: str, theme: str = "fantasy") -> Dict[str, Any]:
        """Create a new character with backstory and personality."""
        logger.info(f"Creating character: {race} {class_name} for {theme} theme")
        
        if not self.llm:
            return self._create_character_template(race, class_name, theme)
        
        prompt = f"""
        Create a detailed character for a {theme} themed game.
        
        Race: {race}
        Class: {class_name}
        Theme: {theme}
        
        Generate a character with:
        - Detailed backstory
        - Personality traits
        - Motivations and goals
        - Character flaws and strengths
        - Relationships and connections
        
        Return as JSON with fields: name, backstory, personality, motivations, relationships
        """
        
        try:
            response = self.llm(prompt)
            character_data = json.loads(response)
            
            # Add game mechanics
            character_data.update(self._create_character_template(race, class_name, theme))
            
            character_id = f"{race}_{class_name}_{datetime.now().strftime('%H%M%S')}"
            character_data["id"] = character_id
            character_data["created_at"] = datetime.now().isoformat()
            
            self.characters[character_id] = character_data
            return character_data
            
        except Exception as e:
            logger.error(f"Error creating character: {e}")
            return self._create_character_template(race, class_name, theme)
    
    def _create_character_template(self, race: str, class_name: str, theme: str) -> Dict[str, Any]:
        """Create character using templates when LLM is not available."""
        race_data = self.character_templates["races"].get(race, self.character_templates["races"]["human"])
        class_data = self.character_templates["classes"].get(class_name, self.character_templates["classes"]["warrior"])
        
        import random
        
        # Generate name
        names = race_data.get("names", ["Adventurer"])
        name = random.choice(names)
        
        # Calculate stats
        base_stats = race_data["base_stats"].copy()
        stat_bonuses = class_data.get("stat_bonuses", {})
        
        for stat, bonus in stat_bonuses.items():
            base_stats[stat] = base_stats.get(stat, 10) + bonus
        
        return {
            "name": f"{name} the {class_name.title()}",
            "race": race,
            "class": class_name,
            "theme": theme,
            "stats": base_stats,
            "level": 1,
            "xp": 0,
            "backstory": f"A {race} {class_name} from the {theme} world, seeking adventure and glory.",
            "personality": f"Brave and determined, this {race} {class_name} is ready for any challenge.",
            "motivations": ["adventure", "glory", "knowledge"],
            "relationships": {},
            "inventory": [],
            "abilities": class_data.get("abilities", [])
        }
    
    def _generate_npc(self, npc_type: str, role: str, theme: str) -> Dict[str, Any]:
        """Generate an NPC with personality and role."""
        logger.info(f"Generating NPC: {npc_type} {role} for {theme} theme")
        
        npc_templates = {
            "mentor": {
                "personality": "wise and experienced",
                "motivations": ["teach", "guide", "protect"],
                "dialogue_style": "philosophical and patient"
            },
            "ally": {
                "personality": "loyal and supportive",
                "motivations": ["help", "friendship", "shared_goals"],
                "dialogue_style": "friendly and encouraging"
            },
            "antagonist": {
                "personality": "ambitious and ruthless",
                "motivations": ["power", "control", "revenge"],
                "dialogue_style": "threatening and manipulative"
            },
            "neutral": {
                "personality": "cautious and calculating",
                "motivations": ["survival", "profit", "information"],
                "dialogue_style": "careful and measured"
            }
        }
        
        template = npc_templates.get(npc_type, npc_templates["neutral"])
        
        npc_id = f"npc_{npc_type}_{role}_{datetime.now().strftime('%H%M%S')}"
        
        npc = {
            "id": npc_id,
            "type": npc_type,
            "role": role,
            "theme": theme,
            "personality": template["personality"],
            "motivations": template["motivations"],
            "dialogue_style": template["dialogue_style"],
            "created_at": datetime.now().isoformat(),
            "relationships": {},
            "knowledge": []
        }
        
        self.npcs[npc_id] = npc
        return npc
    
    def _update_character_progression(self, character_id: str, xp_gain: int = 0, level_up: bool = False) -> Dict[str, Any]:
        """Update character stats and progression."""
        logger.info(f"Updating character progression: {character_id}")
        
        if character_id not in self.characters:
            logger.error(f"Character not found: {character_id}")
            return None
        
        character = self.characters[character_id]
        
        # Update XP
        character["xp"] += xp_gain
        
        # Check for level up
        if level_up or character["xp"] >= character["level"] * 100:
            character["level"] += 1
            character["xp"] = 0
            
            # Improve stats
            for stat in character["stats"]:
                character["stats"][stat] += 1
            
            logger.info(f"Character {character_id} leveled up to level {character['level']}")
        
        return character
    
    def _generate_character_dialogue(self, character_id: str, situation: str) -> str:
        """Generate dialogue specific to a character."""
        logger.info(f"Generating dialogue for character {character_id} in {situation}")
        
        if character_id not in self.characters:
            return "Hello there, traveler."
        
        character = self.characters[character_id]
        race = character.get("race", "human")
        class_name = character.get("class", "adventurer")
        
        dialogue_templates = {
            "combat": f"As a {race} {class_name}, I'm ready for battle!",
            "exploration": f"Let's explore this area carefully, my {race} instincts tell me there's more here.",
            "social": f"Greetings! I am {character['name']}, a {race} {class_name} seeking adventure.",
            "danger": f"Stay alert! My {class_name} training warns me of danger ahead.",
            "victory": f"Another victory for {character['name']}! My {race} heritage serves me well."
        }
        
        return dialogue_templates.get(situation, f"Hello, I am {character['name']}.")
    
    def _manage_character_relationships(self, character_id: str, target_id: str, relationship_type: str) -> Dict[str, Any]:
        """Manage relationships between characters."""
        logger.info(f"Managing relationship: {character_id} -> {target_id} ({relationship_type})")
        
        if character_id not in self.characters:
            logger.error(f"Character not found: {character_id}")
            return None
        
        character = self.characters[character_id]
        
        if "relationships" not in character:
            character["relationships"] = {}
        
        character["relationships"][target_id] = {
            "type": relationship_type,
            "strength": 1.0,
            "updated_at": datetime.now().isoformat()
        }
        
        return character["relationships"]
    
    def get_character(self, character_id: str) -> Optional[Dict[str, Any]]:
        """Get a character by ID."""
        return self.characters.get(character_id)
    
    def get_all_characters(self) -> List[Dict[str, Any]]:
        """Get all characters."""
        return list(self.characters.values())
    
    def get_npc(self, npc_id: str) -> Optional[Dict[str, Any]]:
        """Get an NPC by ID."""
        return self.npcs.get(npc_id)
    
    def get_all_npcs(self) -> List[Dict[str, Any]]:
        """Get all NPCs."""
        return list(self.npcs.values())
    
    def save_characters_to_file(self, filename: str = "characters.json"):
        """Save all characters to a JSON file."""
        try:
            data = {
                "characters": self.characters,
                "npcs": self.npcs,
                "exported_at": datetime.now().isoformat()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Characters saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving characters: {e}")
    
    def load_characters_from_file(self, filename: str = "characters.json"):
        """Load characters from a JSON file."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.characters = data.get("characters", {})
            self.npcs = data.get("npcs", {})
            
            logger.info(f"Characters loaded from {filename}")
        except Exception as e:
            logger.error(f"Error loading characters: {e}")

# Example usage
if __name__ == "__main__":
    # Initialize the agent
    agent = CharacterManagementAgent()
    
    # Create a character
    character = agent._create_character("elf", "mage", "fantasy")
    print(f"Created character: {character['name']}")
    
    # Generate an NPC
    npc = agent._generate_npc("mentor", "wizard", "fantasy")
    print(f"Generated NPC: {npc['role']} {npc['type']}")
    
    # Save characters
    agent.save_characters_to_file()
