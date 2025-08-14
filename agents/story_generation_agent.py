"""
Story Generation Agent

This agent is responsible for automatically generating new scenarios,
story content, and branching narratives using LangChain and LLM integration.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.schema import AgentAction, AgentFinish
from langchain.memory import ConversationBufferMemory
from langchain.prompts import StringPromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain
import openai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StoryGenerationAgent:
    """
    Agent responsible for generating new scenarios and story content.
    
    Capabilities:
    - Generate new scenarios for different themes
    - Create branching story narratives
    - Generate contextual events and plot twists
    - Create character dialogue and descriptions
    - Maintain story continuity and coherence
    """
    
    def __init__(self, api_key: str = None):
        """Initialize the Story Generation Agent."""
        self.api_key = api_key
        self.llm = OpenAI(temperature=0.7, api_key=api_key) if api_key else None
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.scenario_templates = self._load_scenario_templates()
        self.generated_scenarios = []
        
        # Initialize tools
        self.tools = self._initialize_tools()
        
        # Initialize agent
        self.agent = self._initialize_agent()
        
    def _load_scenario_templates(self) -> Dict[str, Any]:
        """Load scenario generation templates."""
        return {
            "fantasy": {
                "setting": "medieval fantasy world with magic and mythical creatures",
                "themes": ["heroic quest", "magical discovery", "ancient prophecy", "dragon hunting"],
                "locations": ["enchanted forest", "ancient temple", "dragon lair", "wizard tower"],
                "conflicts": ["good vs evil", "order vs chaos", "magic vs technology"]
            },
            "warhammer_40k": {
                "setting": "grimdark future with space marines and chaos",
                "themes": ["imperial duty", "chaos corruption", "xenos threat", "hive city survival"],
                "locations": ["hive city", "space ship", "chaos realm", "imperial fortress"],
                "conflicts": ["imperium vs chaos", "humanity vs xenos", "order vs corruption"]
            },
            "cyberpunk": {
                "setting": "dystopian future with advanced technology and corporate control",
                "themes": ["corporate espionage", "hacker rebellion", "AI consciousness", "street survival"],
                "locations": ["corporate tower", "underground network", "AI facility", "street market"],
                "conflicts": ["corporations vs rebels", "humanity vs AI", "order vs anarchy"]
            }
        }
    
    def _initialize_tools(self) -> List[Tool]:
        """Initialize agent tools."""
        return [
            Tool(
                name="generate_scenario",
                func=self._generate_scenario,
                description="Generate a new scenario for a specific theme"
            ),
            Tool(
                name="create_story_branch",
                func=self._create_story_branch,
                description="Create a branching story path from an existing scenario"
            ),
            Tool(
                name="generate_plot_twist",
                func=self._generate_plot_twist,
                description="Generate a plot twist for a story"
            ),
            Tool(
                name="create_character_dialogue",
                func=self._create_character_dialogue,
                description="Generate dialogue for NPCs in the story"
            ),
            Tool(
                name="validate_story_continuity",
                func=self._validate_story_continuity,
                description="Validate that story elements maintain continuity"
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
            You are a Story Generation Agent for an AI Dungeon Master game.
            Your role is to create engaging, coherent, and immersive story content.
            
            Chat History: {chat_history}
            Human: {input}
            Agent: {agent_scratchpad}
            
            Use the available tools to generate story content. Always maintain
            story coherence and create engaging narratives.
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
    
    def _generate_scenario(self, theme: str, difficulty: str = "medium") -> Dict[str, Any]:
        """Generate a new scenario for the specified theme."""
        logger.info(f"Generating scenario for theme: {theme}, difficulty: {difficulty}")
        
        if not self.llm:
            # Fallback to template-based generation
            return self._generate_scenario_template(theme, difficulty)
        
        prompt = f"""
        Generate a new scenario for a {theme} themed game with {difficulty} difficulty.
        
        Requirements:
        - Create an engaging story with clear objectives
        - Include multiple branching paths
        - Add contextual events and plot twists
        - Ensure logical story progression
        - Include character interactions and dialogue
        
        Theme: {theme}
        Difficulty: {difficulty}
        
        Generate a complete scenario structure in JSON format.
        """
        
        try:
            response = self.llm(prompt)
            scenario = json.loads(response)
            self.generated_scenarios.append(scenario)
            return scenario
        except Exception as e:
            logger.error(f"Error generating scenario: {e}")
            return self._generate_scenario_template(theme, difficulty)
    
    def _generate_scenario_template(self, theme: str, difficulty: str) -> Dict[str, Any]:
        """Generate scenario using templates when LLM is not available."""
        template = self.scenario_templates.get(theme, self.scenario_templates["fantasy"])
        
        scenario_id = f"{theme}_{difficulty}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Enhanced scenario templates with proper structure
        scenario_templates = {
            "fantasy": {
                "title": "The Crystal Caverns of Eldoria",
                "description": "Deep within the mystical realm of Eldoria lies the Crystal Caverns, a place of ancient magic and forgotten secrets. Legends speak of a powerful artifact hidden within its depths, but the caverns are guarded by both magical creatures and treacherous traps. Your quest to retrieve the Crystal of Eternal Light will test your courage, wisdom, and magical abilities. The fate of the kingdom rests upon your shoulders as you navigate through enchanted chambers, solve ancient puzzles, and face the guardians of the caverns.",
                "scenes": {
                    "start": {
                        "id": "start",
                        "title": "The Cave Entrance",
                        "description": "You stand before the imposing entrance to the Crystal Caverns. The stone archway is carved with ancient runes that glow with a faint blue light. A cool breeze carries the scent of magic from within. Two paths lie before you - one leads to a well-lit chamber, the other to a dark tunnel that seems to whisper secrets.",
                        "choices": [
                            {
                                "text": "Enter the well-lit chamber to explore safely",
                                "next_node": "light_chamber",
                                "effect": {"karma": 5, "xp": 10}
                            },
                            {
                                "text": "Venture into the dark tunnel for hidden secrets",
                                "next_node": "dark_tunnel",
                                "effect": {"karma": 2, "xp": 15}
                            },
                            {
                                "text": "Study the ancient runes for magical insights",
                                "next_node": "study_runes",
                                "effect": {"karma": 8, "xp": 12}
                            }
                        ]
                    },
                    "light_chamber": {
                        "id": "light_chamber",
                        "title": "The Crystal Chamber",
                        "description": "The chamber is bathed in the soft glow of countless crystals embedded in the walls. In the center stands a pedestal with a crystal orb that pulses with magical energy. Ancient guardians, their forms made of pure light, circle the pedestal protectively.",
                        "choices": [
                            {
                                "text": "Attempt to communicate with the guardians",
                                "next_node": "guardian_dialogue",
                                "effect": {"karma": 10, "xp": 15}
                            },
                            {
                                "text": "Use stealth to approach the pedestal",
                                "next_node": "stealth_approach",
                                "effect": {"karma": 3, "xp": 20}
                            },
                            {
                                "text": "Cast a spell to reveal hidden dangers",
                                "next_node": "magic_reveal",
                                "effect": {"karma": 5, "xp": 18}
                            }
                        ]
                    },
                    "dark_tunnel": {
                        "id": "dark_tunnel",
                        "title": "The Shadow Path",
                        "description": "The tunnel is pitch black except for occasional glints of crystal light. Strange sounds echo from the depths, and you can feel the presence of ancient magic. The air is thick with mystery and potential danger.",
                        "choices": [
                            {
                                "text": "Light a magical torch to illuminate the path",
                                "next_node": "light_path",
                                "effect": {"karma": 4, "xp": 12}
                            },
                            {
                                "text": "Use your senses to navigate in darkness",
                                "next_node": "dark_navigation",
                                "effect": {"karma": 6, "xp": 15}
                            },
                            {
                                "text": "Follow the mysterious sounds deeper",
                                "next_node": "follow_sounds",
                                "effect": {"karma": 2, "xp": 18}
                            }
                        ]
                    }
                }
            },
            "warhammer_40k": {
                "title": "Hive City Infiltration",
                "description": "The sprawling hive city of Necromunda stretches endlessly into the toxic clouds above. In the depths of the underhive, a Chaos cult has been discovered plotting against the Imperium. Your mission is to infiltrate their lair, gather intelligence, and eliminate the threat before it spreads. The underhive is a maze of rusted corridors, inhabited by mutants, gangers, and worse. Your Space Marine training will be tested as you navigate through the dangerous depths, facing both physical and spiritual corruption.",
                "scenes": {
                    "start": {
                        "id": "start",
                        "title": "Hive City Entrance",
                        "description": "You stand at the entrance to the massive hive city, its towering spires reaching into the toxic clouds. The air is thick with industrial pollution and the distant sounds of machinery. Your mission briefing indicated the Chaos cult operates in the lower levels. Three possible entry points present themselves.",
                        "choices": [
                            {
                                "text": "Enter through the main industrial sector",
                                "next_node": "industrial_sector",
                                "effect": {"karma": 5, "xp": 10}
                            },
                            {
                                "text": "Descend through the maintenance tunnels",
                                "next_node": "maintenance_tunnels",
                                "effect": {"karma": 3, "xp": 15}
                            },
                            {
                                "text": "Use your authority to access restricted areas",
                                "next_node": "restricted_access",
                                "effect": {"karma": 8, "xp": 12}
                            }
                        ]
                    },
                    "industrial_sector": {
                        "id": "industrial_sector",
                        "title": "The Industrial Heart",
                        "description": "The industrial sector is a maze of massive machinery, conveyor belts, and worker hab-blocks. The air is thick with smoke and the constant noise of production. Workers in tattered clothing move about their tasks, and you can sense the presence of the cult's influence among them.",
                        "choices": [
                            {
                                "text": "Interrogate workers for information",
                                "next_node": "worker_interrogation",
                                "effect": {"karma": 2, "xp": 15}
                            },
                            {
                                "text": "Follow suspicious activity patterns",
                                "next_node": "suspicious_activity",
                                "effect": {"karma": 5, "xp": 18}
                            },
                            {
                                "text": "Use your Space Marine authority to command respect",
                                "next_node": "marine_authority",
                                "effect": {"karma": 10, "xp": 12}
                            }
                        ]
                    },
                    "maintenance_tunnels": {
                        "id": "maintenance_tunnels",
                        "title": "The Maintenance Depths",
                        "description": "The maintenance tunnels are dark and cramped, filled with the constant hum of machinery and the occasional drip of toxic fluids. Strange markings on the walls suggest cult activity, and you can hear distant chanting echoing through the metal corridors.",
                        "choices": [
                            {
                                "text": "Investigate the strange markings",
                                "next_node": "marking_investigation",
                                "effect": {"karma": 4, "xp": 15}
                            },
                            {
                                "text": "Follow the chanting sounds",
                                "next_node": "chanting_source",
                                "effect": {"karma": 3, "xp": 18}
                            },
                            {
                                "text": "Use your auspex to scan for life signs",
                                "next_node": "auspex_scan",
                                "effect": {"karma": 6, "xp": 12}
                            }
                        ]
                    }
                }
            },
            "cyberpunk": {
                "title": "Corporate Data Heist",
                "description": "Night City's corporate district gleams with neon lights and chrome towers. Arasaka Corporation has developed a revolutionary AI system that could change the balance of power in the city. Your mission is to infiltrate their headquarters, steal the AI core, and deliver it to your fixer. The building is protected by advanced security systems, corporate guards, and rival netrunners. Your skills as a street samurai or netrunner will be tested as you navigate through the high-tech fortress, avoiding detection while racing against time.",
                "scenes": {
                    "start": {
                        "id": "start",
                        "title": "Arasaka Tower Perimeter",
                        "description": "Arasaka Tower rises like a chrome monolith into the neon-lit sky. Security drones patrol the perimeter, and corporate guards stand watch at every entrance. The building's security systems are legendary, but you have your own advantages - street smarts, cybernetics, and desperation. Three infiltration methods present themselves.",
                        "choices": [
                            {
                                "text": "Hack the security systems to create a distraction",
                                "next_node": "security_hack",
                                "effect": {"karma": 3, "xp": 15}
                            },
                            {
                                "text": "Use stealth to infiltrate through maintenance areas",
                                "next_node": "stealth_infiltration",
                                "effect": {"karma": 5, "xp": 12}
                            },
                            {
                                "text": "Create a diversion with street-level chaos",
                                "next_node": "street_diversion",
                                "effect": {"karma": 2, "xp": 18}
                            }
                        ]
                    },
                    "security_hack": {
                        "id": "security_hack",
                        "title": "Digital Infiltration",
                        "description": "You jack into the building's network through a nearby access point. The digital landscape is a maze of firewalls, security protocols, and corporate data streams. You can see the AI core's location deep within the system, but getting there will require navigating through layers of digital security.",
                        "choices": [
                            {
                                "text": "Use brute force to break through firewalls",
                                "next_node": "brute_force",
                                "effect": {"karma": 2, "xp": 20}
                            },
                            {
                                "text": "Social engineer your way through the system",
                                "next_node": "social_engineering",
                                "effect": {"karma": 6, "xp": 15}
                            },
                            {
                                "text": "Find a backdoor in the security architecture",
                                "next_node": "backdoor_search",
                                "effect": {"karma": 4, "xp": 18}
                            }
                        ]
                    },
                    "stealth_infiltration": {
                        "id": "stealth_infiltration",
                        "title": "Shadow Movement",
                        "description": "You move through the building's maintenance areas, using your cybernetic enhancements to avoid detection. The corridors are dimly lit and filled with the hum of machinery. Corporate employees move about their business, unaware of your presence.",
                        "choices": [
                            {
                                "text": "Use your stealth skills to avoid all contact",
                                "next_node": "pure_stealth",
                                "effect": {"karma": 8, "xp": 12}
                            },
                            {
                                "text": "Infiltrate by posing as a maintenance worker",
                                "next_node": "maintenance_disguise",
                                "effect": {"karma": 5, "xp": 15}
                            },
                            {
                                "text": "Create controlled chaos to mask your movement",
                                "next_node": "controlled_chaos",
                                "effect": {"karma": 3, "xp": 18}
                            }
                        ]
                    }
                }
            }
        }
        
        template = scenario_templates.get(theme, scenario_templates["fantasy"])
        
        return {
            "id": scenario_id,
            "theme": theme,
            "difficulty": difficulty,
            "title": template["title"],
            "description": template["description"],
            "estimated_play_time": 60 if difficulty == "easy" else 90 if difficulty == "medium" else 120,
            "scenes": template["scenes"],
            "advanced_storytelling": {
                "contextual_events": {
                    "exploration": {
                        "betrayal_chance": 0.2,
                        "plot_twist_chance": 0.3,
                        "random_event_chance": 0.1
                    }
                }
            }
        }
    
    def _create_story_branch(self, scenario_id: str, branch_point: str) -> Dict[str, Any]:
        """Create a new story branch from an existing scenario."""
        logger.info(f"Creating story branch for scenario: {scenario_id}")
        
        return {
            "branch_id": f"{scenario_id}_branch_{datetime.now().strftime('%H%M%S')}",
            "parent_scenario": scenario_id,
            "branch_point": branch_point,
            "new_scenes": {
                "branch_start": {
                    "id": "branch_start",
                    "title": "New Path",
                    "description": "You discover a new path in your journey.",
                    "choices": [
                        {
                            "text": "Follow the new path",
                            "next_node": "branch_explore",
                            "effect": {"karma": 7}
                        }
                    ]
                }
            }
        }
    
    def _generate_plot_twist(self, context: str) -> Dict[str, Any]:
        """Generate a plot twist for the given context."""
        logger.info(f"Generating plot twist for context: {context}")
        
        plot_twists = {
            "betrayal": "A trusted ally reveals their true nature",
            "revelation": "A hidden truth about the world is discovered",
            "transformation": "The protagonist undergoes a significant change",
            "reversal": "The situation completely changes direction"
        }
        
        return {
            "type": "plot_twist",
            "context": context,
            "description": plot_twists.get(context, "An unexpected event occurs"),
            "impact": "major",
            "timestamp": datetime.now().isoformat()
        }
    
    def _create_character_dialogue(self, character_type: str, situation: str) -> str:
        """Generate dialogue for NPCs."""
        logger.info(f"Generating dialogue for {character_type} in {situation}")
        
        dialogue_templates = {
            "mentor": "I have much to teach you, young one. But first, you must prove yourself.",
            "ally": "We're in this together. I'll help you however I can.",
            "antagonist": "You think you can stop me? You're nothing but a fool.",
            "neutral": "I have information that might interest you... for a price."
        }
        
        return dialogue_templates.get(character_type, "Hello there, traveler.")
    
    def _validate_story_continuity(self, scenario: Dict[str, Any]) -> bool:
        """Validate that story elements maintain continuity."""
        logger.info("Validating story continuity")
        
        # Check for required elements
        required_elements = ["id", "theme", "scenes", "title"]
        for element in required_elements:
            if element not in scenario:
                logger.error(f"Missing required element: {element}")
                return False
        
        # Check scene connectivity
        scenes = scenario.get("scenes", {})
        for scene_id, scene in scenes.items():
            if "choices" in scene:
                for choice in scene["choices"]:
                    if "next_node" in choice:
                        next_node = choice["next_node"]
                        if next_node not in scenes and next_node != "end":
                            logger.warning(f"Choice points to non-existent scene: {next_node}")
        
        return True
    
    def generate_daily_scenario(self) -> Dict[str, Any]:
        """Generate a new scenario for daily content."""
        logger.info("Generating daily scenario")
        
        themes = ["fantasy", "warhammer_40k", "cyberpunk"]
        difficulties = ["easy", "medium", "hard"]
        
        import random
        theme = random.choice(themes)
        difficulty = random.choice(difficulties)
        
        scenario = self._generate_scenario(theme, difficulty)
        
        # Validate the generated scenario
        if self._validate_story_continuity(scenario):
            logger.info(f"Successfully generated daily scenario: {scenario['id']}")
            return scenario
        else:
            logger.error("Generated scenario failed continuity validation")
            return None
    
    def get_generated_scenarios(self) -> List[Dict[str, Any]]:
        """Get all generated scenarios."""
        return self.generated_scenarios
    
    def save_scenario_to_file(self, scenario: Dict[str, Any], filename: str = None):
        """Save a generated scenario to a JSON file."""
        if not filename:
            filename = f"generated_scenario_{scenario['id']}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(scenario, f, indent=2, ensure_ascii=False)
            logger.info(f"Scenario saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving scenario: {e}")

# Example usage
if __name__ == "__main__":
    # Initialize the agent (without API key for template-based generation)
    agent = StoryGenerationAgent()
    
    # Generate a daily scenario
    scenario = agent.generate_daily_scenario()
    if scenario:
        print(f"Generated scenario: {scenario['title']}")
        agent.save_scenario_to_file(scenario)
