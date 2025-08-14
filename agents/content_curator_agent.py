"""
Content Curator Agent

This agent is responsible for content quality control, validation,
curation, and ensuring content meets game standards.
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

class ContentCuratorAgent:
    """
    Agent responsible for content curation and quality control.
    
    Capabilities:
    - Validate content quality and appropriateness
    - Curate and organize game content
    - Monitor content consistency and coherence
    - Filter and moderate user-generated content
    - Maintain content standards and guidelines
    """
    
    def __init__(self, api_key: str = None):
        """Initialize the Content Curator Agent."""
        self.api_key = api_key
        self.llm = OpenAI(temperature=0.3, api_key=api_key) if api_key else None
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.content_guidelines = self._load_content_guidelines()
        self.curated_content = {}
        self.content_metrics = {
            "scenarios_reviewed": 0,
            "characters_curated": 0,
            "content_approved": 0,
            "content_rejected": 0
        }
        
        # Initialize tools
        self.tools = self._initialize_tools()
        
        # Initialize agent
        self.agent = self._initialize_agent()
    
    def _load_content_guidelines(self) -> Dict[str, Any]:
        """Load content quality guidelines."""
        return {
            "age_rating": "T",  # Teen
            "content_standards": {
                "violence": "moderate",
                "language": "mild",
                "themes": "fantasy",
                "complexity": "medium"
            },
            "quality_metrics": {
                "min_scenario_length": 200,  # Increased from 100
                "max_scenario_length": 5000,
                "min_description_length": 150,  # New requirement
                "min_choices_per_scene": 2,  # New requirement
                "min_scenes_per_scenario": 3,  # New requirement
                "required_elements": ["title", "description", "scenes", "choices"],
                "forbidden_content": ["explicit_violence", "adult_themes", "discrimination"]
            },
            "themes": {
                "fantasy": {
                    "appropriate": ["magic", "adventure", "heroism", "quests", "dragons", "wizards", "enchanted"],
                    "avoid": ["explicit_gore", "sexual_content", "real_world_politics"]
                },
                "warhammer_40k": {
                    "appropriate": ["grimdark", "war", "imperial_duty", "chaos", "space_marines", "xenos"],
                    "avoid": ["explicit_torture", "real_world_religion", "excessive_gore"]
                },
                "cyberpunk": {
                    "appropriate": ["technology", "corporate_espionage", "hacking", "street_life", "neon", "cybernetics"],
                    "avoid": ["explicit_violence", "drug_glorification", "real_world_crimes"]
                }
            }
        }
    
    def _initialize_tools(self) -> List[Tool]:
        """Initialize agent tools."""
        return [
            Tool(
                name="validate_content",
                func=self._validate_content,
                description="Validate content against quality guidelines"
            ),
            Tool(
                name="curate_scenario",
                func=self._curate_scenario,
                description="Curate and improve a scenario"
            ),
            Tool(
                name="filter_content",
                func=self._filter_content,
                description="Filter inappropriate content"
            ),
            Tool(
                name="check_consistency",
                func=self._check_consistency,
                description="Check content consistency and coherence"
            ),
            Tool(
                name="generate_content_report",
                func=self._generate_content_report,
                description="Generate content quality report"
            )
        ]
    
    def _initialize_agent(self) -> AgentExecutor:
        """Initialize the LangChain agent."""
        if not self.llm:
            logger.warning("No LLM configured - agent will use rule-based curation")
            return None
            
        prompt = StringPromptTemplate(
            input_variables=["input", "chat_history", "agent_scratchpad"],
            template="""
            You are a Content Curator Agent for an AI Dungeon Master game.
            Your role is to ensure content quality, appropriateness, and consistency.
            
            Chat History: {chat_history}
            Human: {input}
            Agent: {agent_scratchpad}
            
            Use the available tools to validate and curate content according to
            established guidelines and quality standards.
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
    
    def _validate_content(self, content: Dict[str, Any], content_type: str) -> Dict[str, Any]:
        """Validate content against quality guidelines."""
        logger.info(f"Validating {content_type} content")
        
        validation_result = {
            "valid": True,
            "issues": [],
            "suggestions": [],
            "rating": "approved"
        }
        
        # Check required elements
        required_elements = self.content_guidelines["quality_metrics"]["required_elements"]
        for element in required_elements:
            if element not in content:
                # Special handling for "choices" - they should be in scenes, not at top level
                if element == "choices":
                    # Check if choices exist in any scene
                    has_choices = False
                    if "scenes" in content:
                        for scene in content["scenes"].values():
                            if "choices" in scene and len(scene["choices"]) > 0:
                                has_choices = True
                                break
                    if not has_choices:
                        validation_result["valid"] = False
                        validation_result["issues"].append(f"Missing required element: {element} in scenes")
                else:
                    validation_result["valid"] = False
                    validation_result["issues"].append(f"Missing required element: {element}")
        
        # Check content length
        if "description" in content:
            description_length = len(content["description"])
            min_length = self.content_guidelines["quality_metrics"]["min_description_length"]
            
            if description_length < min_length:
                validation_result["issues"].append(f"Description too short: {description_length} chars (min: {min_length})")
                validation_result["valid"] = False
        
        # Check scenario structure
        if "scenes" in content:
            scenes = content["scenes"]
            min_scenes = self.content_guidelines["quality_metrics"]["min_scenes_per_scenario"]
            min_choices = self.content_guidelines["quality_metrics"]["min_choices_per_scene"]
            
            if len(scenes) < min_scenes:
                validation_result["issues"].append(f"Too few scenes: {len(scenes)} (min: {min_scenes})")
                validation_result["valid"] = False
            
            # Check choices in each scene
            for scene_id, scene in scenes.items():
                if "choices" in scene:
                    choices = scene["choices"]
                    if len(choices) < min_choices:
                        validation_result["issues"].append(f"Scene '{scene_id}' has too few choices: {len(choices)} (min: {min_choices})")
                        validation_result["valid"] = False
                    
                    # Check choice quality
                    for i, choice in enumerate(choices):
                        if "text" not in choice or len(choice["text"]) < 10:
                            validation_result["issues"].append(f"Choice {i+1} in scene '{scene_id}' is too short or missing")
                            validation_result["valid"] = False
                        if "next_node" not in choice:
                            validation_result["issues"].append(f"Choice {i+1} in scene '{scene_id}' missing next_node")
                            validation_result["valid"] = False
                else:
                    validation_result["issues"].append(f"Scene '{scene_id}' has no choices")
                    validation_result["valid"] = False
        
        # Check for forbidden content
        forbidden_content = self.content_guidelines["quality_metrics"]["forbidden_content"]
        content_text = str(content).lower()
        for forbidden in forbidden_content:
            if forbidden in content_text:
                validation_result["valid"] = False
                validation_result["issues"].append(f"Forbidden content detected: {forbidden}")
                validation_result["rating"] = "rejected"
        
        # Theme-specific validation
        if "theme" in content:
            theme = content["theme"]
            theme_guidelines = self.content_guidelines["themes"].get(theme, {})
            
            if theme_guidelines:
                # Check for appropriate content
                appropriate_content = theme_guidelines.get("appropriate", [])
                content_has_appropriate = any(appropriate in content_text for appropriate in appropriate_content)
                
                if not content_has_appropriate:
                    validation_result["suggestions"].append(f"Consider adding more {theme}-appropriate content")
                
                # Check for avoided content
                avoid_content = theme_guidelines.get("avoid", [])
                for avoid in avoid_content:
                    if avoid in content_text:
                        validation_result["issues"].append(f"Avoided content for {theme}: {avoid}")
        
        # Update metrics
        if validation_result["rating"] == "approved":
            self.content_metrics["content_approved"] += 1
        else:
            self.content_metrics["content_rejected"] += 1
        
        return validation_result
    
    def _curate_scenario(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Curate and improve a scenario."""
        logger.info("Curating scenario content")
        
        curated_scenario = scenario.copy()
        
        # Improve title if needed
        if "title" in curated_scenario:
            title = curated_scenario["title"]
            if len(title) < 5:
                curated_scenario["title"] = f"Enhanced {title}"
        
        # Improve description if needed
        if "description" in curated_scenario:
            description = curated_scenario["description"]
            min_length = self.content_guidelines["quality_metrics"]["min_description_length"]
            if len(description) < min_length:
                # Enhance description with theme-appropriate content
                theme = curated_scenario.get("theme", "fantasy")
                enhanced_description = self._enhance_description(description, theme, min_length)
                curated_scenario["description"] = enhanced_description
        
        # Ensure proper scene structure
        if "scenes" in curated_scenario:
            scenes = curated_scenario["scenes"]
            min_scenes = self.content_guidelines["quality_metrics"]["min_scenes_per_scenario"]
            
            # Add more scenes if needed
            while len(scenes) < min_scenes:
                new_scene_id = f"scene_{len(scenes)}"
                scenes[new_scene_id] = self._create_enhanced_scene(new_scene_id, curated_scenario.get("theme", "fantasy"))
            
            # Improve existing scenes
            for scene_id, scene in scenes.items():
                scene = self._enhance_scene(scene, scene_id, curated_scenario.get("theme", "fantasy"))
                scenes[scene_id] = scene
        
        # Add metadata
        curated_scenario["curated_at"] = datetime.now().isoformat()
        curated_scenario["curated_by"] = "ContentCuratorAgent"
        curated_scenario["quality_improved"] = True
        
        self.content_metrics["scenarios_reviewed"] += 1
        return curated_scenario
    
    def _enhance_description(self, description: str, theme: str, min_length: int) -> str:
        """Enhance scenario description to meet minimum length requirements."""
        theme_enhancements = {
            "fantasy": [
                "The air crackles with ancient magic as you step into this mystical realm. ",
                "Legends speak of powerful artifacts hidden within these enchanted lands. ",
                "Your destiny awaits in this world of wonder and danger. ",
                "The fate of kingdoms rests upon your shoulders in this epic quest. "
            ],
            "warhammer_40k": [
                "The grim darkness of the far future surrounds you as you navigate this hostile world. ",
                "The Emperor's light guides your path through the endless war. ",
                "Chaos threatens to consume all in this brutal conflict. ",
                "Your duty to the Imperium drives you forward in this desperate struggle. "
            ],
            "cyberpunk": [
                "Neon lights flicker in the perpetual darkness of the corporate dystopia. ",
                "Technology and humanity clash in this high-tech, low-life world. ",
                "Corporate greed and street-level rebellion define this cybernetic society. ",
                "Your skills as a netrunner or street samurai will be tested in this urban jungle. "
            ]
        }
        
        enhancements = theme_enhancements.get(theme, theme_enhancements["fantasy"])
        enhanced_description = description
        
        while len(enhanced_description) < min_length and enhancements:
            enhancement = enhancements.pop(0)
            enhanced_description += enhancement
        
        return enhanced_description
    
    def _create_enhanced_scene(self, scene_id: str, theme: str) -> Dict[str, Any]:
        """Create an enhanced scene with proper structure."""
        scene_templates = {
            "fantasy": {
                "title": "Mystical Encounter",
                "description": "You encounter a mysterious figure who offers guidance or challenges your path. The ancient magic of this place seems to respond to your presence.",
                "choices": [
                    {
                        "text": "Accept the figure's guidance and learn ancient secrets",
                        "next_node": f"{scene_id}_guidance",
                        "effect": {"karma": 5, "xp": 10}
                    },
                    {
                        "text": "Challenge the figure to prove your worth",
                        "next_node": f"{scene_id}_challenge",
                        "effect": {"karma": -2, "xp": 15}
                    },
                    {
                        "text": "Attempt to negotiate for information",
                        "next_node": f"{scene_id}_negotiate",
                        "effect": {"karma": 3, "xp": 8}
                    }
                ]
            },
            "warhammer_40k": {
                "title": "Imperial Duty",
                "description": "Your mission brings you face-to-face with the harsh realities of the 41st millennium. The Emperor's will guides your actions.",
                "choices": [
                    {
                        "text": "Follow Imperial protocol and maintain discipline",
                        "next_node": f"{scene_id}_protocol",
                        "effect": {"karma": 5, "xp": 10}
                    },
                    {
                        "text": "Take aggressive action against the threat",
                        "next_node": f"{scene_id}_aggressive",
                        "effect": {"karma": -1, "xp": 15}
                    },
                    {
                        "text": "Investigate the situation thoroughly",
                        "next_node": f"{scene_id}_investigate",
                        "effect": {"karma": 3, "xp": 12}
                    }
                ]
            },
            "cyberpunk": {
                "title": "Corporate Intrigue",
                "description": "The neon-lit streets hide secrets that could make or break your reputation. Corporate interests and street gangs vie for control.",
                "choices": [
                    {
                        "text": "Hack into corporate systems for information",
                        "next_node": f"{scene_id}_hack",
                        "effect": {"karma": 2, "xp": 15}
                    },
                    {
                        "text": "Negotiate with street contacts for intel",
                        "next_node": f"{scene_id}_negotiate",
                        "effect": {"karma": 4, "xp": 10}
                    },
                    {
                        "text": "Use your combat skills to force answers",
                        "next_node": f"{scene_id}_combat",
                        "effect": {"karma": -2, "xp": 18}
                    }
                ]
            }
        }
        
        template = scene_templates.get(theme, scene_templates["fantasy"])
        return {
            "id": scene_id,
            "title": template["title"],
            "description": template["description"],
            "choices": template["choices"]
        }
    
    def _enhance_scene(self, scene: Dict[str, Any], scene_id: str, theme: str) -> Dict[str, Any]:
        """Enhance an existing scene to meet quality standards."""
        enhanced_scene = scene.copy()
        
        # Ensure minimum description length
        if "description" in enhanced_scene:
            description = enhanced_scene["description"]
            if len(description) < 100:
                enhanced_scene["description"] = self._enhance_description(description, theme, 100)
        
        # Ensure minimum choices
        if "choices" in enhanced_scene:
            choices = enhanced_scene["choices"]
            min_choices = self.content_guidelines["quality_metrics"]["min_choices_per_scene"]
            
            while len(choices) < min_choices:
                new_choice = self._create_enhanced_choice(theme, f"{scene_id}_choice_{len(choices)}")
                choices.append(new_choice)
            
            # Enhance existing choices
            for i, choice in enumerate(choices):
                if "text" not in choice or len(choice["text"]) < 10:
                    choice["text"] = f"Continue your journey through the {theme} world"
                if "next_node" not in choice:
                    choice["next_node"] = f"{scene_id}_continue_{i}"
                if "effect" not in choice:
                    choice["effect"] = {"karma": 1, "xp": 5}
        else:
            # Create choices if none exist
            enhanced_scene["choices"] = [
                self._create_enhanced_choice(theme, f"{scene_id}_choice_0"),
                self._create_enhanced_choice(theme, f"{scene_id}_choice_1")
            ]
        
        return enhanced_scene
    
    def _create_enhanced_choice(self, theme: str, choice_id: str) -> Dict[str, Any]:
        """Create an enhanced choice with proper structure."""
        choice_templates = {
            "fantasy": [
                {"text": "Explore the magical surroundings", "effect": {"karma": 3, "xp": 8}},
                {"text": "Seek guidance from mystical beings", "effect": {"karma": 5, "xp": 10}},
                {"text": "Use your magical abilities", "effect": {"karma": 2, "xp": 12}},
                {"text": "Search for ancient artifacts", "effect": {"karma": 4, "xp": 15}}
            ],
            "warhammer_40k": [
                {"text": "Follow Imperial doctrine", "effect": {"karma": 5, "xp": 10}},
                {"text": "Engage in tactical combat", "effect": {"karma": 2, "xp": 15}},
                {"text": "Investigate the situation", "effect": {"karma": 3, "xp": 12}},
                {"text": "Maintain squad discipline", "effect": {"karma": 4, "xp": 8}}
            ],
            "cyberpunk": [
                {"text": "Hack into systems for information", "effect": {"karma": 2, "xp": 15}},
                {"text": "Negotiate with street contacts", "effect": {"karma": 4, "xp": 10}},
                {"text": "Use your combat skills", "effect": {"karma": -1, "xp": 18}},
                {"text": "Analyze the situation", "effect": {"karma": 3, "xp": 12}}
            ]
        }
        
        import random
        templates = choice_templates.get(theme, choice_templates["fantasy"])
        choice_template = random.choice(templates)
        
        return {
            "text": choice_template["text"],
            "next_node": choice_id,
            "effect": choice_template["effect"]
        }
    
    def _filter_content(self, content: str, content_type: str = "text") -> Dict[str, Any]:
        """Filter inappropriate content."""
        logger.info(f"Filtering {content_type} content")
        
        filter_result = {
            "filtered": False,
            "filtered_content": content,
            "issues_found": [],
            "replacement_suggestions": []
        }
        
        # Check for inappropriate words/phrases
        inappropriate_patterns = [
            "explicit", "adult", "inappropriate", "offensive",
            "discriminatory", "hate", "violence", "gore"
        ]
        
        content_lower = content.lower()
        for pattern in inappropriate_patterns:
            if pattern in content_lower:
                filter_result["filtered"] = True
                filter_result["issues_found"].append(f"Inappropriate content: {pattern}")
                filter_result["replacement_suggestions"].append(f"Replace '{pattern}' with appropriate alternative")
        
        # Check content length
        if len(content) < 10:
            filter_result["issues_found"].append("Content too short")
            filter_result["replacement_suggestions"].append("Add more descriptive content")
        
        return filter_result
    
    def _check_consistency(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Check content consistency and coherence."""
        logger.info("Checking content consistency")
        
        consistency_result = {
            "consistent": True,
            "inconsistencies": [],
            "suggestions": []
        }
        
        # Check for logical inconsistencies
        if "scenes" in content:
            scenes = content["scenes"]
            scene_ids = set(scenes.keys())
            
            for scene_id, scene in scenes.items():
                if "choices" in scene:
                    for choice in scene["choices"]:
                        if "next_node" in choice:
                            next_node = choice["next_node"]
                            if next_node not in scene_ids and next_node != "end":
                                consistency_result["inconsistencies"].append(
                                    f"Choice in {scene_id} points to non-existent scene: {next_node}"
                                )
                                consistency_result["consistent"] = False
        
        # Check theme consistency
        if "theme" in content:
            theme = content["theme"]
            theme_keywords = {
                "fantasy": ["magic", "sword", "dragon", "elf", "dwarf"],
                "warhammer_40k": ["space", "marine", "imperium", "chaos", "xenos"],
                "cyberpunk": ["cyber", "hack", "corporate", "neon", "tech"]
            }
            
            content_text = str(content).lower()
            theme_words = theme_keywords.get(theme, [])
            
            theme_consistency = any(word in content_text for word in theme_words)
            if not theme_consistency:
                consistency_result["suggestions"].append(f"Add more {theme}-themed content")
        
        return consistency_result
    
    def _generate_content_report(self, content_id: str = None) -> Dict[str, Any]:
        """Generate content quality report."""
        logger.info("Generating content quality report")
        
        report = {
            "report_id": f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "generated_at": datetime.now().isoformat(),
            "metrics": self.content_metrics.copy(),
            "summary": {
                "total_content_reviewed": self.content_metrics["content_approved"] + self.content_metrics["content_rejected"],
                "approval_rate": 0.0,
                "quality_score": 0.0
            },
            "recommendations": []
        }
        
        # Calculate approval rate
        total_reviewed = report["summary"]["total_content_reviewed"]
        if total_reviewed > 0:
            report["summary"]["approval_rate"] = self.content_metrics["content_approved"] / total_reviewed
        
        # Generate recommendations
        if report["summary"]["approval_rate"] < 0.8:
            report["recommendations"].append("Improve content quality guidelines")
        
        if self.content_metrics["scenarios_reviewed"] < 10:
            report["recommendations"].append("Increase content review frequency")
        
        return report
    
    def validate_content(self, content: Dict[str, Any], content_type: str) -> Dict[str, Any]:
        """Public method to validate content."""
        return self._validate_content(content, content_type)
    
    def curate_content(self, content: Dict[str, Any], content_type: str) -> Dict[str, Any]:
        """Public method to curate content."""
        if content_type == "scenario":
            return self._curate_scenario(content)
        else:
            return self._filter_content(content, content_type)
    
    def approve_content(self, content_id: str, content: Dict[str, Any]) -> bool:
        """Approve content for use in the game."""
        logger.info(f"Approving content: {content_id}")
        
        validation = self._validate_content(content, "scenario")
        if validation["valid"]:
            self.curated_content[content_id] = {
                "content": content,
                "approved_at": datetime.now().isoformat(),
                "validation_result": validation
            }
            return True
        else:
            logger.warning(f"Content {content_id} failed validation: {validation['issues']}")
            return False
    
    def get_curated_content(self, content_id: str = None) -> Dict[str, Any]:
        """Get curated content."""
        if content_id:
            return self.curated_content.get(content_id)
        return self.curated_content
    
    def export_content_report(self, filename: str = None) -> bool:
        """Export content curation report."""
        if not filename:
            filename = f"content_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            report = self._generate_content_report()
            report["curated_content"] = self.curated_content
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Content report exported to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error exporting content report: {e}")
            return False

# Example usage
if __name__ == "__main__":
    # Initialize the agent
    agent = ContentCuratorAgent()
    
    # Test scenario
    test_scenario = {
        "id": "test_scenario",
        "title": "Test Adventure",
        "description": "A simple test scenario for validation.",
        "theme": "fantasy",
        "scenes": {
            "start": {
                "id": "start",
                "title": "Beginning",
                "description": "Your adventure begins.",
                "choices": [
                    {"text": "Explore", "next_node": "explore"},
                    {"text": "Rest", "next_node": "rest"}
                ]
            }
        }
    }
    
    # Validate content
    validation = agent._validate_content(test_scenario, "scenario")
    print(f"Validation result: {validation}")
    
    # Curate scenario
    curated = agent._curate_scenario(test_scenario)
    print(f"Curated scenario: {curated['title']}")
    
    # Generate report
    report = agent._generate_content_report()
    print(f"Content report: {report['summary']}")
