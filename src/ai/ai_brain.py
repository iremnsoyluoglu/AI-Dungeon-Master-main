#!/usr/bin/env python3
"""
AI Brain System
==============

Handles AI character thinking and decision making.
"""

import json
import random
from typing import Dict, List, Any, Optional

class AIBrainSystem:
    """Manages AI character thinking and decision making"""
    
    def __init__(self):
        self.brains_file = "data/ai_brains.json"
        self._ensure_data_directory()
        self._load_brains()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        import os
        os.makedirs("data", exist_ok=True)
    
    def _load_brains(self):
        """Load AI brains from file"""
        try:
            import os
            if os.path.exists(self.brains_file):
                with open(self.brains_file, 'r', encoding='utf-8') as f:
                    self.brains = json.load(f)
            else:
                self.brains = {}
        except Exception as e:
            print(f"Error loading AI brains: {e}")
            self.brains = {}
    
    def _save_brains(self):
        """Save AI brains to file"""
        try:
            with open(self.brains_file, 'w', encoding='utf-8') as f:
                json.dump(self.brains, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving AI brains: {e}")
    
    def create_ai_brain(self, brain_type: str, personality: str = "neutral") -> Dict[str, Any]:
        """Create a new AI brain"""
        try:
            brain_id = f"brain_{len(self.brains) + 1}"
            
            brain_data = {
                "id": brain_id,
                "type": brain_type,
                "personality": personality,
                "knowledge": [],
                "memories": [],
                "created_at": "2025-07-29T20:00:00"
            }
            
            self.brains[brain_id] = brain_data
            self._save_brains()
            
            return {
                "success": True,
                "brain_id": brain_id,
                "brain": brain_data,
                "message": "AI brain created successfully"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def think(self, brain_id: str, context: str, situation: Dict[str, Any]) -> Dict[str, Any]:
        """Make AI think about a situation"""
        try:
            brain = self.brains.get(brain_id)
            if not brain:
                return {"success": False, "error": "Brain not found"}
            
            # Simple AI thinking logic
            thoughts = self._generate_thoughts(brain, context, situation)
            decision = self._make_decision(brain, thoughts, situation)
            
            # Update brain with new knowledge
            brain["memories"].append({
                "context": context,
                "thoughts": thoughts,
                "decision": decision,
                "timestamp": "2025-07-29T20:00:00"
            })
            
            self._save_brains()
            
            return {
                "success": True,
                "thoughts": thoughts,
                "decision": decision,
                "message": "AI thinking completed"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _generate_thoughts(self, brain: Dict[str, Any], context: str, situation: Dict[str, Any]) -> List[str]:
        """Generate thoughts based on context and situation"""
        thoughts = []
        
        # Simple thought generation based on personality
        personality = brain.get("personality", "neutral")
        
        if personality == "aggressive":
            thoughts.extend([
                "Bu durumda saldırgan olmalıyım",
                "Güç göstermek önemli",
                "Düşmanları korkutmalıyım"
            ])
        elif personality == "cautious":
            thoughts.extend([
                "Dikkatli olmalıyım",
                "Risk almamalıyım",
                "Güvenli yolu seçmeliyim"
            ])
        else:  # neutral
            thoughts.extend([
                "Durumu değerlendirmeliyim",
                "En iyi çözümü bulmalıyım",
                "Dengeli bir yaklaşım benimsemeliyim"
            ])
        
        return thoughts
    
    def _make_decision(self, brain: Dict[str, Any], thoughts: List[str], situation: Dict[str, Any]) -> Dict[str, Any]:
        """Make a decision based on thoughts and situation"""
        # Simple decision making
        decision = {
            "action": "wait",
            "reasoning": "Durumu gözlemliyorum",
            "confidence": random.randint(50, 90)
        }
        
        # Adjust decision based on thoughts
        if any("saldırgan" in thought for thought in thoughts):
            decision["action"] = "attack"
            decision["reasoning"] = "Saldırgan bir yaklaşım benimsiyorum"
        elif any("dikkatli" in thought for thought in thoughts):
            decision["action"] = "defend"
            decision["reasoning"] = "Savunmada kalıyorum"
        
        return decision
    
    def get_brain(self, brain_id: str) -> Optional[Dict[str, Any]]:
        """Get AI brain by ID"""
        return self.brains.get(brain_id)
    
    def get_all_brains(self) -> Dict[str, Dict[str, Any]]:
        """Get all AI brains"""
        return self.brains 