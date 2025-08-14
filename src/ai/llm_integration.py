#!/usr/bin/env python3
"""
LLM Integration System
======================

Integrates with various LLM APIs for dynamic content generation.
Supports OpenAI, Anthropic, and local LLM models.
"""

import json
import logging
import os
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class LLMResponse:
    content: str
    model: str
    tokens_used: int
    cost: float

class LLMIntegration:
    """LLM Integration for dynamic content generation"""
    
    def __init__(self, provider: str = "openai"):
        self.provider = provider
        self.api_key = os.getenv(f"{provider.upper()}_API_KEY")
        self.base_url = self._get_base_url(provider)
        
    def _get_base_url(self, provider: str) -> str:
        """Get base URL for LLM provider"""
        urls = {
            "openai": "https://api.openai.com/v1",
            "anthropic": "https://api.anthropic.com/v1",
            "local": "http://localhost:11434"  # Ollama
        }
        return urls.get(provider, urls["openai"])
    
    def generate_scenario(self, theme: str, genre: str, difficulty: str) -> Dict[str, Any]:
        """Generate a complete scenario using LLM"""
        try:
            prompt = self._create_scenario_prompt(theme, genre, difficulty)
            response = self._call_llm(prompt)
            
            # Parse LLM response
            scenario = self._parse_scenario_response(response.content, theme, genre)
            
            return scenario
            
        except Exception as e:
            logger.error(f"Error generating scenario with LLM: {e}")
            return self._get_fallback_scenario(theme, genre)
    
    def generate_character_dialogue(self, character_name: str, personality: str, situation: str) -> str:
        """Generate character dialogue using LLM"""
        try:
            prompt = f"""
            Karakter: {character_name}
            Kişilik: {personality}
            Durum: {situation}
            
            Bu karakterin bu durumda ne söyleyeceğini yaz. Doğal ve karakteristik olsun.
            """
            
            response = self._call_llm(prompt)
            return response.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating dialogue: {e}")
            return f"{character_name}: 'Bu durumda ne yapacağımı düşünüyorum...'"
    
    def generate_ai_brain_thoughts(self, character_id: str, personality: str, situation: Dict[str, Any]) -> List[str]:
        """Generate AI brain thoughts using LLM"""
        try:
            situation_text = json.dumps(situation, ensure_ascii=False)
            
            prompt = f"""
            Karakter ID: {character_id}
            Kişilik: {personality}
            Durum: {situation_text}
            
            Bu karakterin bu durumda ne düşüneceğini 3-5 cümle olarak yaz.
            Her düşünce ayrı satırda olsun.
            """
            
            response = self._call_llm(prompt)
            thoughts = [thought.strip() for thought in response.content.split('\n') if thought.strip()]
            
            return thoughts
            
        except Exception as e:
            logger.error(f"Error generating AI brain thoughts: {e}")
            return [
                "Bu durum hakkında düşünüyorum...",
                "En iyi yaklaşım nedir?",
                "Dikkatli olmalıyım."
            ]
    
    def enhance_comic_vine_content(self, comic_vine_data: Dict[str, Any], theme: str) -> Dict[str, Any]:
        """Enhance Comic Vine content with LLM"""
        try:
            comic_data = json.dumps(comic_vine_data, ensure_ascii=False)
            
            prompt = f"""
            Comic Vine verisi: {comic_data}
            Tema: {theme}
            
            Bu Comic Vine verisini kullanarak {theme} temalı bir oyun senaryosu oluştur.
            Şunları ekle:
            - Detaylı hikaye
            - Karakterler
            - Lokasyonlar
            - Görevler
            - Engeller
            """
            
            response = self._call_llm(prompt)
            enhanced_data = self._parse_enhanced_content(response.content, comic_vine_data)
            
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Error enhancing Comic Vine content: {e}")
            return comic_vine_data
    
    def generate_scenario_from_comic_vine(self, comic_vine_data: Dict[str, Any], theme: str, genre: str) -> Dict[str, Any]:
        """Generate complete scenario from Comic Vine data using LLM"""
        try:
            # Create prompt for scenario generation from Comic Vine data
            prompt = self._create_comic_vine_scenario_prompt(comic_vine_data, theme, genre)
            response = self._call_llm(prompt)
            
            # Parse the generated scenario
            scenario = self._parse_comic_vine_scenario(response.content, comic_vine_data, theme, genre)
            
            return scenario
            
        except Exception as e:
            logger.error(f"Error generating scenario from Comic Vine: {e}")
            return self._get_fallback_scenario(theme, genre)
    
    def _create_comic_vine_scenario_prompt(self, comic_vine_data: Dict[str, Any], theme: str, genre: str) -> str:
        """Create prompt for generating scenario from Comic Vine data"""
        characters = comic_vine_data.get("characters", [])
        locations = comic_vine_data.get("locations", [])
        plot_points = comic_vine_data.get("plot_points", [])
        
        character_text = "\n".join([f"- {char.get('name', 'Unknown')}: {char.get('description', 'No description')}" 
                                   for char in characters[:5]])
        
        location_text = "\n".join([f"- {loc}" for loc in locations[:3]])
        
        plot_text = "\n".join([f"- {point}" for point in plot_points[:5]])
        
        return f"""
        Comic Vine verilerinden bir oyun senaryosu oluştur:
        
        Tema: {theme}
        Tür: {genre}
        
        Karakterler:
        {character_text}
        
        Lokasyonlar:
        {location_text}
        
        Plot Noktaları:
        {plot_text}
        
        Bu verileri kullanarak şu formatta bir senaryo oluştur:
        {{
            "title": "Senaryo Başlığı",
            "description": "Senaryo açıklaması",
            "characters": ["Karakter1", "Karakter2"],
            "locations": ["Lokasyon1", "Lokasyon2"],
            "story_nodes": [
                {{
                    "id": "node_1",
                    "title": "İlk Sahne",
                    "description": "Sahne açıklaması",
                    "choices": [
                        {{
                            "text": "Seçenek 1",
                            "next_node": "node_2",
                            "consequence": "Sonuç açıklaması"
                        }}
                    ]
                }}
            ],
            "difficulty": "medium",
            "genre": "{genre}",
            "theme": "{theme}"
        }}
        
        Senaryo Türkçe olmalı ve {theme} temasına uygun olmalı.
        """
    
    def _parse_comic_vine_scenario(self, content: str, original_data: Dict[str, Any], theme: str, genre: str) -> Dict[str, Any]:
        """Parse LLM-generated scenario from Comic Vine data"""
        try:
            # Try to parse JSON response
            if "{" in content and "}" in content:
                start = content.find("{")
                end = content.rfind("}") + 1
                json_str = content[start:end]
                
                scenario = json.loads(json_str)
                
                # Add original Comic Vine data
                scenario["comic_vine_source"] = original_data
                scenario["llm_enhanced"] = True
                
                return scenario
                
        except Exception as e:
            logger.error(f"Error parsing Comic Vine scenario: {e}")
        
        # Fallback to text parsing
        return self._parse_text_scenario(content)
    
    def _create_scenario_prompt(self, theme: str, genre: str, difficulty: str) -> str:
        """Create prompt for scenario generation"""
        return f"""
        {genre} temalı {theme} senaryosu oluştur.
        Zorluk: {difficulty}
        
        Şunları içermeli:
        1. Senaryo başlığı
        2. Kısa açıklama
        3. Ana karakterler (4-6 tane)
        4. Lokasyonlar (3-5 tane)
        5. Ana görevler (5-8 tane)
        6. Engeller ve düşmanlar
        7. Ödüller
        
        JSON formatında döndür.
        """
    
    def _call_llm(self, prompt: str) -> LLMResponse:
        """Call LLM API"""
        if self.provider == "openai":
            return self._call_openai(prompt)
        elif self.provider == "anthropic":
            return self._call_anthropic(prompt)
        elif self.provider == "local":
            return self._call_local_llm(prompt)
        else:
            return self._call_mock_llm(prompt)
    
    def _call_openai(self, prompt: str) -> LLMResponse:
        """Call OpenAI API"""
        if not self.api_key:
            return self._call_mock_llm(prompt)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            return LLMResponse(
                content=content,
                model="gpt-3.5-turbo",
                tokens_used=result["usage"]["total_tokens"],
                cost=0.0  # Calculate based on token usage
            )
        else:
            logger.error(f"OpenAI API error: {response.status_code}")
            return self._call_mock_llm(prompt)
    
    def _call_anthropic(self, prompt: str) -> LLMResponse:
        """Call Anthropic Claude API"""
        if not self.api_key:
            return self._call_mock_llm(prompt)
        
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(
            f"{self.base_url}/messages",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result["content"][0]["text"]
            return LLMResponse(
                content=content,
                model="claude-3-sonnet",
                tokens_used=result["usage"]["input_tokens"] + result["usage"]["output_tokens"],
                cost=0.0
            )
        else:
            logger.error(f"Anthropic API error: {response.status_code}")
            return self._call_mock_llm(prompt)
    
    def _call_local_llm(self, prompt: str) -> LLMResponse:
        """Call local LLM (Ollama)"""
        data = {
            "model": "llama2",
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            return LLMResponse(
                content=result["response"],
                model="llama2",
                tokens_used=0,
                cost=0.0
            )
        else:
            logger.error(f"Local LLM error: {response.status_code}")
            return self._call_mock_llm(prompt)
    
    def _call_mock_llm(self, prompt: str) -> LLMResponse:
        """Mock LLM response for testing"""
        # Generate mock response based on prompt
        if "senaryo" in prompt.lower():
            mock_response = {
                "title": "Mock Scenario",
                "description": "Bu bir test senaryosudur.",
                "characters": ["Kahraman", "Yardımcı", "Düşman"],
                "locations": ["Başlangıç", "Orta", "Son"],
                "quests": ["Görev 1", "Görev 2", "Görev 3"],
                "obstacles": ["Engel 1", "Engel 2"],
                "rewards": ["Ödül 1", "Ödül 2"]
            }
            content = json.dumps(mock_response, ensure_ascii=False, indent=2)
        else:
            content = "Mock LLM response: " + prompt[:100] + "..."
        
        return LLMResponse(
            content=content,
            model="mock-llm",
            tokens_used=0,
            cost=0.0
        )
    
    def _parse_scenario_response(self, content: str, theme: str, genre: str) -> Dict[str, Any]:
        """Parse LLM scenario response"""
        try:
            # Try to parse as JSON
            if content.strip().startswith('{'):
                scenario = json.loads(content)
            else:
                # Parse as text
                scenario = self._parse_text_scenario(content)
            
            # Add metadata
            scenario.update({
                "theme": theme,
                "genre": genre,
                "ai_generated": True,
                "source": "llm"
            })
            
            return scenario
            
        except Exception as e:
            logger.error(f"Error parsing scenario response: {e}")
            return self._get_fallback_scenario(theme, genre)
    
    def _parse_text_scenario(self, content: str) -> Dict[str, Any]:
        """Parse text-based scenario response"""
        lines = content.split('\n')
        scenario = {
            "title": "LLM Generated Scenario",
            "description": "",
            "characters": [],
            "locations": [],
            "quests": [],
            "obstacles": [],
            "rewards": []
        }
        
        current_section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if "başlık" in line.lower() or "title" in line.lower():
                scenario["title"] = line.split(':')[-1].strip()
            elif "açıklama" in line.lower() or "description" in line.lower():
                scenario["description"] = line.split(':')[-1].strip()
            elif "karakter" in line.lower() or "character" in line.lower():
                current_section = "characters"
            elif "lokasyon" in line.lower() or "location" in line.lower():
                current_section = "locations"
            elif "görev" in line.lower() or "quest" in line.lower():
                current_section = "quests"
            elif "engel" in line.lower() or "obstacle" in line.lower():
                current_section = "obstacles"
            elif "ödül" in line.lower() or "reward" in line.lower():
                current_section = "rewards"
            elif line.startswith('-') or line.startswith('*'):
                item = line[1:].strip()
                if current_section and item:
                    scenario[current_section].append(item)
        
        return scenario
    
    def _parse_enhanced_content(self, content: str, original_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse enhanced Comic Vine content"""
        try:
            if content.strip().startswith('{'):
                enhanced = json.loads(content)
            else:
                enhanced = original_data.copy()
                enhanced["llm_enhancement"] = content
            
            return enhanced
            
        except Exception as e:
            logger.error(f"Error parsing enhanced content: {e}")
            return original_data
    
    def _get_fallback_scenario(self, theme: str, genre: str) -> Dict[str, Any]:
        """Get fallback scenario when LLM fails"""
        return {
            "title": f"{theme.title()} Macerası",
            "description": f"{genre} temalı bir macera.",
            "characters": ["Kahraman", "Yardımcı", "Düşman"],
            "locations": ["Başlangıç", "Orta", "Son"],
            "quests": ["Ana görev", "Yan görev"],
            "obstacles": ["Engel"],
            "rewards": ["Ödül"],
            "theme": theme,
            "genre": genre,
            "ai_generated": True,
            "source": "fallback"
        } 