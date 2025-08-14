#!/usr/bin/env python3
"""
Comic Vine API Integration
==========================

Integrates with Comic Vine API to fetch scenarios, characters, and story content.
Uses LLM to process and enhance the fetched content.
"""

import requests
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ComicVineCharacter:
    id: str
    name: str
    description: str
    powers: List[str]
    origin: str
    publisher: str

@dataclass
class ComicVineScenario:
    id: str
    title: str
    description: str
    characters: List[ComicVineCharacter]
    locations: List[str]
    plot_points: List[str]
    genre: str
    difficulty: str

class ComicVineAPI:
    """Comic Vine API integration for scenario generation"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("COMIC_VINE_API_KEY")
        self.base_url = "https://comicvine.gamespot.com/api"
        self.headers = {
            "User-Agent": "AI-Dungeon-Master/1.0"
        }
        
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
    
    def search_characters(self, query: str, limit: int = 10) -> List[ComicVineCharacter]:
        """Search for characters in Comic Vine"""
        try:
            if not self.api_key:
                # Return mock data if no API key
                return self._get_mock_characters(query)
            
            url = f"{self.base_url}/search"
            params = {
                "api_key": self.api_key,
                "format": "json",
                "query": query,
                "resources": "character",
                "limit": limit
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            characters = []
            
            for result in data.get("results", []):
                character = ComicVineCharacter(
                    id=result.get("id", ""),
                    name=result.get("name", ""),
                    description=result.get("deck", ""),
                    powers=result.get("powers", []),
                    origin=result.get("origin", {}).get("name", ""),
                    publisher=result.get("publisher", {}).get("name", "")
                )
                characters.append(character)
            
            return characters
            
        except Exception as e:
            logger.error(f"Error searching characters: {e}")
            return self._get_mock_characters(query)
    
    def get_character_details(self, character_id: str) -> Optional[ComicVineCharacter]:
        """Get detailed character information"""
        try:
            if not self.api_key:
                return self._get_mock_character_details(character_id)
            
            url = f"{self.base_url}/character/{character_id}"
            params = {
                "api_key": self.api_key,
                "format": "json"
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            result = data.get("results", {})
            
            character = ComicVineCharacter(
                id=result.get("id", ""),
                name=result.get("name", ""),
                description=result.get("deck", ""),
                powers=result.get("powers", []),
                origin=result.get("origin", {}).get("name", ""),
                publisher=result.get("publisher", {}).get("name", "")
            )
            
            return character
            
        except Exception as e:
            logger.error(f"Error getting character details: {e}")
            return self._get_mock_character_details(character_id)
    
    def search_scenarios(self, theme: str, genre: str = "fantasy") -> List[ComicVineScenario]:
        """Search for scenarios based on theme and genre"""
        try:
            if not self.api_key:
                return self._get_mock_scenarios(theme, genre)
            
            # Search for story arcs or issues that match the theme
            url = f"{self.base_url}/search"
            params = {
                "api_key": self.api_key,
                "format": "json",
                "query": f"{theme} {genre}",
                "resources": "story_arc",
                "limit": 5
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            scenarios = []
            
            for result in data.get("results", []):
                scenario = ComicVineScenario(
                    id=result.get("id", ""),
                    title=result.get("name", ""),
                    description=result.get("deck", ""),
                    characters=[],  # Would need additional API calls
                    locations=[],   # Would need additional API calls
                    plot_points=[], # Would need additional API calls
                    genre=genre,
                    difficulty="medium"
                )
                scenarios.append(scenario)
            
            return scenarios
            
        except Exception as e:
            logger.error(f"Error searching scenarios: {e}")
            return self._get_mock_scenarios(theme, genre)
    
    def generate_scenario_with_llm(self, theme: str, genre: str = "fantasy") -> ComicVineScenario:
        """Generate a scenario using LLM based on Comic Vine data"""
        try:
            # Get base scenario from Comic Vine
            base_scenarios = self.search_scenarios(theme, genre)
            
            if base_scenarios:
                base_scenario = base_scenarios[0]
            else:
                base_scenario = self._get_mock_scenarios(theme, genre)[0]
            
            # Enhance scenario with LLM
            enhanced_scenario = self._enhance_scenario_with_llm(base_scenario, theme, genre)
            
            return enhanced_scenario
            
        except Exception as e:
            logger.error(f"Error generating scenario with LLM: {e}")
            return self._get_mock_scenarios(theme, genre)[0]
    
    def generate_dynamic_scenario(self, theme: str, genre: str = "fantasy", difficulty: str = "medium") -> Dict[str, Any]:
        """Generate dynamic scenario from Comic Vine data using LLM"""
        try:
            # Get Comic Vine data
            comic_vine_data = self._get_comic_vine_data_for_theme(theme, genre)
            
            # Import LLM integration
            from .llm_integration import LLMIntegration
            llm = LLMIntegration()
            
            # Generate scenario using LLM
            scenario = llm.generate_scenario_from_comic_vine(comic_vine_data, theme, genre)
            
            # Add metadata
            scenario["source"] = "comic_vine_llm"
            scenario["difficulty"] = difficulty
            scenario["generated_at"] = str(datetime.now())
            
            return scenario
            
        except Exception as e:
            logger.error(f"Error generating dynamic scenario: {e}")
            return self._get_fallback_scenario(theme, genre)
    
    def _get_comic_vine_data_for_theme(self, theme: str, genre: str) -> Dict[str, Any]:
        """Get Comic Vine data for specific theme"""
        try:
            # Search for characters related to theme
            characters = self.search_characters(theme, limit=5)
            
            # Get locations and plot points
            locations = self._get_locations_for_theme(theme)
            plot_points = self._get_plot_points_for_theme(theme)
            
            return {
                "characters": [{"name": c.name, "description": c.description, "powers": c.powers} 
                              for c in characters],
                "locations": locations,
                "plot_points": plot_points,
                "theme": theme,
                "genre": genre
            }
            
        except Exception as e:
            logger.error(f"Error getting Comic Vine data: {e}")
            return self._get_mock_comic_vine_data(theme, genre)
    
    def _get_locations_for_theme(self, theme: str) -> List[str]:
        """Get locations for theme"""
        location_map = {
            "dragon_lords": ["Ejderha Krallığı", "Antik Tapınak", "Gizli Mağara", "Orman Köyü"],
            "space_marine_mission": ["Uzay Gemisi", "Xenos Üssü", "İmparator Tapınağı", "Savaş Alanı"],
            "pyraxis_legend": ["Ateş Tapınağı", "Lav Dağı", "Büyücü Köyü", "Antik Harabeler"],
            "cyberpunk_heist": ["Mega Corporation", "Hacker Deni", "Siber Şehir", "Gizli Üs"],
            "western_outlaw": ["Vahşi Batı Kasabası", "Saloon", "Tren İstasyonu", "Çöl"],
            "steampunk_invention": ["Buhar Laboratuvarı", "Hava Gemisi", "Mekanik Şehir", "Büyü Akademisi"],
            "post_apocalyptic_survival": ["Radyasyon Sığınağı", "Harap Şehir", "Mutant Kampı", "Güvenli Bölge"],
            "superhero_origin": ["Süper Kahraman Üssü", "Şehir Merkezi", "Gizli Laboratuvar", "Uzay İstasyonu"]
        }
        
        return location_map.get(theme, ["Bilinmeyen Lokasyon"])
    
    def _get_plot_points_for_theme(self, theme: str) -> List[str]:
        """Get plot points for theme"""
        plot_map = {
            "dragon_lords": ["Ejderha lordları ile savaş", "Antik büyüyü keşfet", "Krallığı kurtar"],
            "space_marine_mission": ["Xenos tehdidini yok et", "İmparator için savaş", "Zafer kazan"],
            "pyraxis_legend": ["Ateş tanrısının gücünü al", "Büyücülerle ittifak kur", "Efsaneyi tamamla"],
            "cyberpunk_heist": ["Corporation'ı soyguna gir", "Hacker ekibi kur", "Özgürlük için savaş"],
            "western_outlaw": ["Tren soygunu yap", "Şerif ile yüzleş", "Kefaret bul"],
            "steampunk_invention": ["Büyük buluşu tamamla", "Mekanik dünyayı keşfet", "Geleceği şekillendir"],
            "post_apocalyptic_survival": ["Hayatta kal", "Topluluk kur", "Yeni dünya yarat"],
            "superhero_origin": ["Güçlerini keşfet", "Kahraman ol", "Şehri koru"]
        }
        
        return plot_map.get(theme, ["Bilinmeyen görev"])
    
    def _get_mock_comic_vine_data(self, theme: str, genre: str) -> Dict[str, Any]:
        """Get mock Comic Vine data for testing"""
        return {
            "characters": [
                {"name": "Test Karakteri", "description": "Test açıklaması", "powers": ["Test gücü"]}
            ],
            "locations": ["Test Lokasyonu"],
            "plot_points": ["Test görevi"],
            "theme": theme,
            "genre": genre
        }
    
    def _get_fallback_scenario(self, theme: str, genre: str) -> Dict[str, Any]:
        """Get fallback scenario when LLM fails"""
        return {
            "title": f"{theme.title()} Macerası",
            "description": f"{theme} temalı bir macera",
            "characters": ["Ana Karakter"],
            "locations": ["Ana Lokasyon"],
            "story_nodes": [
                {
                    "id": "start",
                    "title": "Başlangıç",
                    "description": "Maceraya başlıyorsunuz",
                    "choices": [
                        {
                            "text": "Devam Et",
                            "next_node": "end",
                            "consequence": "Macerayı tamamladınız"
                        }
                    ]
                }
            ],
            "difficulty": "medium",
            "genre": genre,
            "theme": theme,
            "source": "fallback"
        }
    
    def _enhance_scenario_with_llm(self, base_scenario: ComicVineScenario, theme: str, genre: str) -> ComicVineScenario:
        """Enhance scenario using LLM processing"""
        # This would integrate with an actual LLM service
        # For now, we'll use template-based enhancement
        
        enhanced_plot_points = [
            f"Giriş: {theme} temalı bir maceraya başla",
            f"Keşif: {genre} dünyasını keşfet",
            f"Çatışma: Ana düşmanla yüzleş",
            f"Çözüm: Sorunu çöz ve ödülü al",
            f"Sonuç: Macerayı tamamla"
        ]
        
        enhanced_characters = [
            ComicVineCharacter(
                id="hero_1",
                name="Kahraman",
                description="Ana karakter, maceranın kahramanı",
                powers=["Savaş becerisi", "Liderlik"],
                origin="Kahramanlık",
                publisher="AI Dungeon Master"
            ),
            ComicVineCharacter(
                id="villain_1",
                name="Düşman",
                description="Ana antagonist, kahramanın karşısındaki güç",
                powers=["Karanlık güçler", "Strateji"],
                origin="Kötülük",
                publisher="AI Dungeon Master"
            ),
            ComicVineCharacter(
                id="helper_1",
                name="Yardımcı",
                description="Kahramana yardım eden karakter",
                powers=["Bilgelik", "İyileştirme"],
                origin="İyilik",
                publisher="AI Dungeon Master"
            )
        ]
        
        enhanced_locations = [
            "Başlangıç noktası",
            "Ana mekan",
            "Düşmanın yeri",
            "Güvenli bölge",
            "Final savaş alanı"
        ]
        
        return ComicVineScenario(
            id=base_scenario.id,
            title=f"AI Enhanced: {base_scenario.title}",
            description=f"LLM ile geliştirilmiş {theme} temalı {genre} macerası. {base_scenario.description}",
            characters=enhanced_characters,
            locations=enhanced_locations,
            plot_points=enhanced_plot_points,
            genre=genre,
            difficulty="medium"
        )
    
    def _get_mock_characters(self, query: str) -> List[ComicVineCharacter]:
        """Get mock character data"""
        mock_characters = {
            "dragon": [
                ComicVineCharacter(
                    id="dragon_1",
                    name="Kırmızı Ejderha",
                    description="Güçlü ve tehlikeli bir ejderha",
                    powers=["Ateş nefesi", "Uçma", "Güçlü savunma"],
                    origin="Ejderha Krallığı",
                    publisher="Fantasy World"
                ),
                ComicVineCharacter(
                    id="dragon_2",
                    name="Mavi Ejderha",
                    description="Bilge ve eski bir ejderha",
                    powers=["Buz nefesi", "Büyü", "Bilgelik"],
                    origin="Buz Dağları",
                    publisher="Fantasy World"
                )
            ],
            "warrior": [
                ComicVineCharacter(
                    id="warrior_1",
                    name="Savaşçı",
                    description="Cesur ve güçlü bir savaşçı",
                    powers=["Kılıç ustalığı", "Dayanıklılık", "Liderlik"],
                    origin="Savaşçılar Birliği",
                    publisher="Fantasy World"
                )
            ],
            "wizard": [
                ComicVineCharacter(
                    id="wizard_1",
                    name="Büyücü",
                    description="Güçlü büyüleri olan bir büyücü",
                    powers=["Ateş büyüsü", "Buz büyüsü", "Işınlanma"],
                    origin="Büyücüler Akademisi",
                    publisher="Fantasy World"
                )
            ]
        }
        
        # Find matching characters
        matching_characters = []
        for category, characters in mock_characters.items():
            if category.lower() in query.lower():
                matching_characters.extend(characters)
        
        return matching_characters[:5]  # Limit to 5 results
    
    def _get_mock_character_details(self, character_id: str) -> Optional[ComicVineCharacter]:
        """Get mock character details"""
        all_characters = []
        for characters in self._get_mock_characters("").values():
            all_characters.extend(characters)
        
        for character in all_characters:
            if character.id == character_id:
                return character
        
        return None
    
    def _get_mock_scenarios(self, theme: str, genre: str) -> List[ComicVineScenario]:
        """Get mock scenario data"""
        mock_scenarios = {
            "fantasy": [
                ComicVineScenario(
                    id="scenario_1",
                    title="Ejderha Mağarası Macerası",
                    description="Karanlık bir mağarada gizli hazine arayışı",
                    characters=[],
                    locations=["Mağara girişi", "İç oda", "Hazine odası"],
                    plot_points=["Mağaraya gir", "Engelleri aş", "Hazineyi bul", "Güvenli çık"],
                    genre="fantasy",
                    difficulty="medium"
                ),
                ComicVineScenario(
                    id="scenario_2",
                    title="Orman Perisi Efsanesi",
                    description="Ormanın derinliklerinde gizli bir periyi bulma macerası",
                    characters=[],
                    locations=["Orman", "Gizli bahçe", "Peri sarayı"],
                    plot_points=["Ormana gir", "İzleri takip et", "Periyi bul", "Yardım et"],
                    genre="fantasy",
                    difficulty="easy"
                )
            ],
            "sci-fi": [
                ComicVineScenario(
                    id="scenario_3",
                    title="Uzay İstasyonu Görevi",
                    description="Uzay istasyonunda tehlikeli bir görev",
                    characters=[],
                    locations=["İstasyon", "Kontrol odası", "Motor bölümü"],
                    plot_points=["İstasyona gir", "Sorunu tespit et", "Düzelt", "Güvenli çık"],
                    genre="sci-fi",
                    difficulty="hard"
                )
            ]
        }
        
        return mock_scenarios.get(genre, mock_scenarios["fantasy"])
    
    def get_scenario_for_game(self, theme: str, difficulty: str = "medium") -> Dict[str, Any]:
        """Get a complete scenario ready for game use"""
        try:
            # Generate scenario with LLM
            scenario = self.generate_scenario_with_llm(theme, "fantasy")
            
            # Convert to game format
            game_scenario = {
                "id": scenario.id,
                "title": scenario.title,
                "description": scenario.description,
                "difficulty": difficulty,
                "genre": scenario.genre,
                "characters": [
                    {
                        "id": char.id,
                        "name": char.name,
                        "description": char.description,
                        "powers": char.powers,
                        "origin": char.origin
                    }
                    for char in scenario.characters
                ],
                "locations": scenario.locations,
                "plot_points": scenario.plot_points,
                "game_elements": {
                    "starting_location": scenario.locations[0] if scenario.locations else "Başlangıç",
                    "final_goal": scenario.plot_points[-1] if scenario.plot_points else "Macera tamamla",
                    "key_items": ["Anahtar", "Harita", "İksir"],
                    "enemies": ["Goblin", "Ork", "Ejderha"],
                    "allies": ["Köylü", "Tüccar", "Bilge"]
                }
            }
            
            return game_scenario
            
        except Exception as e:
            logger.error(f"Error getting scenario for game: {e}")
            return {
                "id": "default_scenario",
                "title": "Varsayılan Macera",
                "description": "Bir macera bekliyor...",
                "difficulty": difficulty,
                "genre": "fantasy",
                "characters": [],
                "locations": ["Başlangıç", "Orta", "Son"],
                "plot_points": ["Başla", "Keşfet", "Bitir"],
                "game_elements": {
                    "starting_location": "Başlangıç",
                    "final_goal": "Macera tamamla",
                    "key_items": ["Anahtar"],
                    "enemies": ["Düşman"],
                    "allies": ["Yardımcı"]
                }
            } 