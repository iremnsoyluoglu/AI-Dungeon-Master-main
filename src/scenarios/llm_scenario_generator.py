#!/usr/bin/env python3
"""
LLM Scenario Generator
=====================

Generates dynamic scenarios using AI language models.
"""

import json
import random
from typing import Dict, List, Any, Optional

class LLMScenarioGenerator:
    """Generates scenarios using AI language models"""
    
    def __init__(self):
        self.scenarios_file = "data/scenarios.json"
        self._ensure_data_directory()
        self._load_scenarios()
        self._initialize_default_scenarios()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        import os
        os.makedirs("data", exist_ok=True)
    
    def _load_scenarios(self):
        """Load scenarios from file"""
        try:
            import os
            if os.path.exists(self.scenarios_file):
                with open(self.scenarios_file, 'r', encoding='utf-8') as f:
                    self.scenarios = json.load(f)
            else:
                self.scenarios = {}
        except Exception as e:
            print(f"Error loading scenarios: {e}")
            self.scenarios = {}
    
    def _save_scenarios(self):
        """Save scenarios to file"""
        try:
            with open(self.scenarios_file, 'w', encoding='utf-8') as f:
                json.dump(self.scenarios, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving scenarios: {e}")
    
    def _initialize_default_scenarios(self):
        """Initialize default scenarios if none exist"""
        if not self.scenarios:
            self._create_default_scenarios()
    
    def _create_default_scenarios(self):
        """Create default scenarios"""
        default_scenarios = {
            "fantasy_adventure": {
                "id": "fantasy_adventure",
                "title": "Fantastik Macera",
                "description": "Orta Dünya'da geçen epik bir macera",
                "genre": "fantasy",
                "difficulty": "medium",
                "scenes": [
                    {
                        "id": "start",
                        "title": "Köy Meydanı",
                        "description": "Küçük bir köyün meydanında duruyorsunuz. Etrafta tüccarlar ve köylüler var.",
                        "choices": [
                            {"id": "explore", "text": "Köyü keşfet", "next_scene": "village_explore"},
                            {"id": "tavern", "text": "Meyhaneye git", "next_scene": "tavern"},
                            {"id": "quest", "text": "Görev ara", "next_scene": "quest_board"}
                        ]
                    },
                    {
                        "id": "village_explore",
                        "title": "Köy Keşfi",
                        "description": "Köyün sokaklarında dolaşıyorsunuz. Birkaç ilginç yer görüyorsunuz.",
                        "choices": [
                            {"id": "shop", "text": "Dükkana git", "next_scene": "shop"},
                            {"id": "church", "text": "Kiliseyi ziyaret et", "next_scene": "church"},
                            {"id": "return", "text": "Meydana dön", "next_scene": "start"}
                        ]
                    }
                ]
            },
            "sci_fi_mystery": {
                "id": "sci_fi_mystery",
                "title": "Bilim Kurgu Gizemi",
                "description": "Uzay istasyonunda geçen gizemli bir hikaye",
                "genre": "sci_fi",
                "difficulty": "hard",
                "scenes": [
                    {
                        "id": "start",
                        "title": "Uzay İstasyonu",
                        "description": "Uzay istasyonunun ana koridorunda duruyorsunuz. Etrafta garip sesler var.",
                        "choices": [
                            {"id": "investigate", "text": "Sesleri araştır", "next_scene": "investigation"},
                            {"id": "bridge", "text": "Köprüye git", "next_scene": "bridge"},
                            {"id": "quarters", "text": "Mürettebat odalarına git", "next_scene": "quarters"}
                        ]
                    }
                ]
            }
        }
        
        self.scenarios.update(default_scenarios)
        self._save_scenarios()
    
    def generate_scenario(self, genre: str = None, difficulty: str = None) -> Dict[str, Any]:
        """Generate a new scenario"""
        try:
            # For now, return a random existing scenario
            # In a full implementation, this would use AI to generate content
            available_scenarios = [
                scenario for scenario in self.scenarios.values()
                if (not genre or scenario.get("genre") == genre) and
                   (not difficulty or scenario.get("difficulty") == difficulty)
            ]
            
            if not available_scenarios:
                return {"success": False, "error": "No scenarios available"}
            
            selected_scenario = random.choice(available_scenarios)
            
            return {
                "success": True,
                "scenario": selected_scenario,
                "message": "Scenario generated successfully"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_scenarios(self, genre: str = None) -> List[Dict[str, Any]]:
        """Get all available scenarios"""
        scenarios = list(self.scenarios.values())
        if genre:
            scenarios = [s for s in scenarios if s.get("genre") == genre]
        return scenarios
    
    def get_scenario(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific scenario"""
        return self.scenarios.get(scenario_id) 