#!/usr/bin/env python3
"""
Betrayal System
==============

Handles betrayal mechanics and plot twists.
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional

class BetrayalSystem:
    """Manages betrayal mechanics and plot twists"""
    
    def __init__(self):
        self.betrayals_file = "data/betrayals.json"
        self.plot_twists_file = "data/plot_twists.json"
        self._ensure_data_directory()
        self._load_betrayals()
        self._load_plot_twists()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        import os
        os.makedirs("data", exist_ok=True)
    
    def _load_betrayals(self):
        """Load betrayals from file"""
        try:
            import os
            if os.path.exists(self.betrayals_file):
                with open(self.betrayals_file, 'r', encoding='utf-8') as f:
                    self.betrayals = json.load(f)
            else:
                self.betrayals = {}
        except Exception as e:
            print(f"Error loading betrayals: {e}")
            self.betrayals = {}
    
    def _save_betrayals(self):
        """Save betrayals to file"""
        try:
            with open(self.betrayals_file, 'w', encoding='utf-8') as f:
                json.dump(self.betrayals, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving betrayals: {e}")
    
    def _load_plot_twists(self):
        """Load plot twists from file"""
        try:
            import os
            if os.path.exists(self.plot_twists_file):
                with open(self.plot_twists_file, 'r', encoding='utf-8') as f:
                    self.plot_twists = json.load(f)
            else:
                self.plot_twists = {}
        except Exception as e:
            print(f"Error loading plot twists: {e}")
            self.plot_twists = {}
    
    def _save_plot_twists(self):
        """Save plot twists to file"""
        try:
            with open(self.plot_twists_file, 'w', encoding='utf-8') as f:
                json.dump(self.plot_twists, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving plot twists: {e}")
    
    def record_player_decision(self, session_id: str, decision: str, 
                             moral_alignment: str = "neutral") -> Dict[str, Any]:
        """Record a player decision for betrayal analysis"""
        try:
            decision_id = f"decision_{len(self.betrayals) + 1}"
            now = datetime.now().isoformat()
            
            decision_data = {
                "id": decision_id,
                "session_id": session_id,
                "decision": decision,
                "moral_alignment": moral_alignment,
                "timestamp": now,
                "betrayal_potential": self._calculate_betrayal_potential(decision, moral_alignment)
            }
            
            self.betrayals[decision_id] = decision_data
            self._save_betrayals()
            
            return {
                "success": True,
                "decision_id": decision_id,
                "betrayal_potential": decision_data["betrayal_potential"],
                "message": "Decision recorded successfully"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _calculate_betrayal_potential(self, decision: str, moral_alignment: str) -> int:
        """Calculate betrayal potential based on decision and alignment"""
        potential = 0
        
        # Decision-based analysis
        decision_lower = decision.lower()
        
        if any(word in decision_lower for word in ["kill", "murder", "assassinate"]):
            potential += 30
        elif any(word in decision_lower for word in ["steal", "rob", "thief"]):
            potential += 20
        elif any(word in decision_lower for word in ["betray", "deceive", "lie"]):
            potential += 40
        elif any(word in decision_lower for word in ["help", "save", "protect"]):
            potential -= 10
        
        # Alignment-based modifiers
        if moral_alignment == "evil":
            potential += 20
        elif moral_alignment == "good":
            potential -= 15
        elif moral_alignment == "chaotic":
            potential += 10
        
        return max(0, min(100, potential))
    
    def check_plot_twist_triggers(self, session_id: str) -> Dict[str, Any]:
        """Check if any plot twists should be triggered"""
        try:
            # Get all decisions for this session
            session_decisions = [
                decision for decision in self.betrayals.values()
                if decision.get("session_id") == session_id
            ]
            
            if not session_decisions:
                return {"success": True, "plot_twists": []}
            
            # Calculate total betrayal potential
            total_potential = sum(d.get("betrayal_potential", 0) for d in session_decisions)
            average_potential = total_potential / len(session_decisions)
            
            # Check for plot twist triggers
            triggered_twists = []
            
            if average_potential >= 70:
                triggered_twists.append(self._create_major_betrayal(session_id))
            elif average_potential >= 50:
                triggered_twists.append(self._create_minor_betrayal(session_id))
            elif average_potential >= 30:
                triggered_twists.append(self._create_suspicion(session_id))
            
            return {
                "success": True,
                "average_betrayal_potential": average_potential,
                "plot_twists": triggered_twists,
                "total_decisions": len(session_decisions)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _create_major_betrayal(self, session_id: str) -> Dict[str, Any]:
        """Create a major betrayal plot twist"""
        twist_id = f"twist_{len(self.plot_twists) + 1}"
        now = datetime.now().isoformat()
        
        betrayal_options = [
            {
                "type": "ally_betrayal",
                "title": "Ally Betrayal",
                "description": "A trusted ally reveals they were working against you all along",
                "impact": "major",
                "consequences": ["Loss of ally", "Combat encounter", "Story shift"]
            },
            {
                "type": "quest_betrayal",
                "title": "Quest Betrayal",
                "description": "The quest you were given was a trap all along",
                "impact": "major",
                "consequences": ["Quest failure", "Enemy ambush", "Reputation loss"]
            },
            {
                "type": "world_betrayal",
                "title": "World Betrayal",
                "description": "The world itself is not what it seems",
                "impact": "major",
                "consequences": ["Reality shift", "New enemies", "Story revelation"]
            }
        ]
        
        selected_betrayal = random.choice(betrayal_options)
        
        twist_data = {
            "id": twist_id,
            "session_id": session_id,
            "type": "major_betrayal",
            "title": selected_betrayal["title"],
            "description": selected_betrayal["description"],
            "impact": selected_betrayal["impact"],
            "consequences": selected_betrayal["consequences"],
            "triggered_at": now
        }
        
        self.plot_twists[twist_id] = twist_data
        self._save_plot_twists()
        
        return twist_data
    
    def _create_minor_betrayal(self, session_id: str) -> Dict[str, Any]:
        """Create a minor betrayal plot twist"""
        twist_id = f"twist_{len(self.plot_twists) + 1}"
        now = datetime.now().isoformat()
        
        betrayal_options = [
            {
                "type": "information_betrayal",
                "title": "Information Betrayal",
                "description": "Someone you trusted gave you false information",
                "impact": "minor",
                "consequences": ["Quest complication", "Time loss", "Mistrust"]
            },
            {
                "type": "resource_betrayal",
                "title": "Resource Betrayal",
                "description": "Your resources have been compromised",
                "impact": "minor",
                "consequences": ["Item loss", "Gold loss", "Equipment damage"]
            }
        ]
        
        selected_betrayal = random.choice(betrayal_options)
        
        twist_data = {
            "id": twist_id,
            "session_id": session_id,
            "type": "minor_betrayal",
            "title": selected_betrayal["title"],
            "description": selected_betrayal["description"],
            "impact": selected_betrayal["impact"],
            "consequences": selected_betrayal["consequences"],
            "triggered_at": now
        }
        
        self.plot_twists[twist_id] = twist_data
        self._save_plot_twists()
        
        return twist_data
    
    def _create_suspicion(self, session_id: str) -> Dict[str, Any]:
        """Create a suspicion plot twist"""
        twist_id = f"twist_{len(self.plot_twists) + 1}"
        now = datetime.now().isoformat()
        
        suspicion_options = [
            {
                "type": "npc_suspicion",
                "title": "NPC Suspicion",
                "description": "An NPC seems to be hiding something from you",
                "impact": "minor",
                "consequences": ["Dialogue options", "Investigation quest", "Trust issues"]
            },
            {
                "type": "environment_suspicion",
                "title": "Environment Suspicion",
                "description": "Something about your surroundings seems wrong",
                "impact": "minor",
                "consequences": ["Exploration", "Puzzle elements", "Atmosphere change"]
            }
        ]
        
        selected_suspicion = random.choice(suspicion_options)
        
        twist_data = {
            "id": twist_id,
            "session_id": session_id,
            "type": "suspicion",
            "title": selected_suspicion["title"],
            "description": selected_suspicion["description"],
            "impact": selected_suspicion["impact"],
            "consequences": selected_suspicion["consequences"],
            "triggered_at": now
        }
        
        self.plot_twists[twist_id] = twist_data
        self._save_plot_twists()
        
        return twist_data
    
    def get_betrayal_summary(self, session_id: str) -> Dict[str, Any]:
        """Get a summary of betrayals for a session"""
        try:
            session_decisions = [
                decision for decision in self.betrayals.values()
                if decision.get("session_id") == session_id
            ]
            
            session_twists = [
                twist for twist in self.plot_twists.values()
                if twist.get("session_id") == session_id
            ]
            
            total_potential = sum(d.get("betrayal_potential", 0) for d in session_decisions)
            average_potential = total_potential / len(session_decisions) if session_decisions else 0
            
            return {
                "success": True,
                "session_id": session_id,
                "total_decisions": len(session_decisions),
                "total_plot_twists": len(session_twists),
                "average_betrayal_potential": average_potential,
                "decisions": session_decisions,
                "plot_twists": session_twists
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_manual_betrayal(self, session_id: str, betrayal_type: str, 
                              description: str) -> Dict[str, Any]:
        """Manually create a betrayal plot twist"""
        try:
            twist_id = f"twist_{len(self.plot_twists) + 1}"
            now = datetime.now().isoformat()
            
            twist_data = {
                "id": twist_id,
                "session_id": session_id,
                "type": betrayal_type,
                "title": f"Manual {betrayal_type.title()}",
                "description": description,
                "impact": "manual",
                "consequences": ["Custom consequences"],
                "triggered_at": now,
                "manual": True
            }
            
            self.plot_twists[twist_id] = twist_data
            self._save_plot_twists()
            
            return {
                "success": True,
                "twist_id": twist_id,
                "twist": twist_data,
                "message": "Manual betrayal created successfully"
            }
        except Exception as e:
            return {"success": False, "error": str(e)} 