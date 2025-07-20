import os
import openai
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class AIDungeonMaster:
    def __init__(self):
        self.ready = True
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = "gpt-3.5-turbo"
        self.conversation_history = []
        
        if self.api_key:
            openai.api_key = self.api_key
            logger.info("OpenAI API key loaded")
        else:
            logger.warning("OpenAI API key not found, using fallback responses")
    
    def run_campaign(self, prompt: str, context: Dict = None) -> str:
        """AI ile kampanya çalıştır"""
        if not self.api_key:
            return self._get_fallback_response(prompt)
        
        try:
            messages = self._build_messages(prompt, context)
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.8
            )
            
            ai_response = response.choices[0].message.content
            self.conversation_history.append({
                "prompt": prompt,
                "response": ai_response,
                "context": context
            })
            
            logger.info(f"AI response generated for prompt: {prompt[:50]}...")
            return ai_response
            
        except Exception as e:
            logger.error(f"AI API error: {e}")
            return self._get_fallback_response(prompt)
    
    def generate_npc(self, npc_type: str, context: Dict = None) -> Dict:
        """NPC oluştur"""
        prompt = f"Create a detailed NPC of type {npc_type} for a fantasy RPG campaign."
        
        if not self.api_key:
            return self._get_fallback_npc(npc_type)
        
        try:
            response = self.run_campaign(prompt, context)
            return {
                "name": f"{npc_type.title()} NPC",
                "description": response,
                "type": npc_type,
                "stats": self._generate_npc_stats(npc_type)
            }
        except Exception as e:
            logger.error(f"NPC generation error: {e}")
            return self._get_fallback_npc(npc_type)
    
    def generate_location(self, location_type: str, context: Dict = None) -> Dict:
        """Konum oluştur"""
        prompt = f"Describe a detailed {location_type} location for a fantasy RPG campaign."
        
        if not self.api_key:
            return self._get_fallback_location(location_type)
        
        try:
            response = self.run_campaign(prompt, context)
            return {
                "name": f"{location_type.title()} Location",
                "description": response,
                "type": location_type,
                "features": self._generate_location_features(location_type)
            }
        except Exception as e:
            logger.error(f"Location generation error: {e}")
            return self._get_fallback_location(location_type)
    
    def generate_quest(self, quest_type: str, context: Dict = None) -> Dict:
        """Görev oluştur"""
        prompt = f"Create a detailed {quest_type} quest for a fantasy RPG campaign."
        
        if not self.api_key:
            return self._get_fallback_quest(quest_type)
        
        try:
            response = self.run_campaign(prompt, context)
            return {
                "title": f"{quest_type.title()} Quest",
                "description": response,
                "type": quest_type,
                "objectives": self._generate_quest_objectives(quest_type)
            }
        except Exception as e:
            logger.error(f"Quest generation error: {e}")
            return self._get_fallback_quest(quest_type)
    
    def _build_messages(self, prompt: str, context: Dict = None) -> List[Dict]:
        """AI mesajlarını oluştur"""
        system_message = """You are an expert Dungeon Master for a fantasy RPG campaign. 
        Create immersive, engaging content that fits the fantasy genre. 
        Respond in Turkish and keep responses concise but descriptive."""
        
        messages = [{"role": "system", "content": system_message}]
        
        if context:
            context_str = f"Context: {context}"
            messages.append({"role": "user", "content": context_str})
        
        messages.append({"role": "user", "content": prompt})
        return messages
    
    def _get_fallback_response(self, prompt: str) -> str:
        """API olmadığında fallback cevap"""
        fallback_responses = {
            "combat": "Savaş başlıyor! Düşmanlar size doğru geliyor.",
            "exploration": "Yeni bir alan keşfediyorsunuz. Garip sesler duyuyorsunuz.",
            "dialogue": "NPC ile konuşuyorsunuz. Size yardım etmeye hazır görünüyor.",
            "puzzle": "Karmaşık bir bulmaca ile karşılaştınız. Çözümü bulmaya çalışın."
        }
        
        for key, response in fallback_responses.items():
            if key in prompt.lower():
                return response
        
        return "AI Dungeon Master aktif. Maceranız devam ediyor!"
    
    def _get_fallback_npc(self, npc_type: str) -> Dict:
        """Fallback NPC"""
        npc_templates = {
            "merchant": {"name": "Tüccar Ahmet", "description": "Deneyimli bir tüccar"},
            "guard": {"name": "Muhafız Mehmet", "description": "Güçlü bir muhafız"},
            "wizard": {"name": "Büyücü Zeynep", "description": "Bilge bir büyücü"},
            "rogue": {"name": "Hırsız Ali", "description": "Gizemli bir hırsız"}
        }
        
        return npc_templates.get(npc_type, {
            "name": f"{npc_type.title()} NPC",
            "description": f"Bir {npc_type} karakteri"
        })
    
    def _get_fallback_location(self, location_type: str) -> Dict:
        """Fallback konum"""
        return {
            "name": f"{location_type.title()} Konumu",
            "description": f"Gizemli bir {location_type} konumu",
            "type": location_type
        }
    
    def _get_fallback_quest(self, quest_type: str) -> Dict:
        """Fallback görev"""
        return {
            "title": f"{quest_type.title()} Görevi",
            "description": f"Önemli bir {quest_type} görevi",
            "type": quest_type
        }
    
    def _generate_npc_stats(self, npc_type: str) -> Dict:
        """NPC istatistikleri oluştur"""
        base_stats = {"HP": 50, "Attack": 10, "Defense": 10}
        
        if npc_type == "merchant":
            base_stats.update({"HP": 30, "Attack": 5, "Defense": 5})
        elif npc_type == "guard":
            base_stats.update({"HP": 80, "Attack": 15, "Defense": 20})
        elif npc_type == "wizard":
            base_stats.update({"HP": 40, "Attack": 20, "Defense": 5, "Mana": 100})
        
        return base_stats
    
    def _generate_location_features(self, location_type: str) -> List[str]:
        """Konum özellikleri oluştur"""
        features = {
            "cave": ["Karanlık geçitler", "Damlayan su", "Gizli odalar"],
            "forest": ["Yoğun ağaçlar", "Gizli patikalar", "Vahşi hayvanlar"],
            "castle": ["Yüksek duvarlar", "Kuleler", "Gizli geçitler"],
            "town": ["Pazar yeri", "Han", "Tapınak"]
        }
        
        return features.get(location_type, ["Gizemli özellikler"])
    
    def _generate_quest_objectives(self, quest_type: str) -> List[str]:
        """Görev hedefleri oluştur"""
        objectives = {
            "rescue": ["Rehineyi bul", "Güvenli yere götür"],
            "explore": ["Alanı keşfet", "Hazine bul"],
            "defeat": ["Düşmanı yen", "Kanıt getir"],
            "deliver": ["Eşyayı al", "Hedefi bul", "Teslim et"]
        }
        
        return objectives.get(quest_type, ["Görevi tamamla"])
    
    def get_conversation_history(self) -> List[Dict]:
        """Konuşma geçmişini getir"""
        return self.conversation_history
    
    def clear_history(self):
        """Geçmişi temizle"""
        self.conversation_history = []
        logger.info("Conversation history cleared") 