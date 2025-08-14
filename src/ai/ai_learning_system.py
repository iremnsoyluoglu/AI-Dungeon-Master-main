#!/usr/bin/env python3
"""
AI Learning System
==================

Comprehensive AI learning system with action preference learning, adaptation,
and personalized experiences.
"""

import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import numpy as np
from collections import defaultdict, Counter

class LearningType(Enum):
    ACTION_PREFERENCE = "action_preference"
    DIFFICULTY_ADAPTATION = "difficulty_adaptation"
    NARRATIVE_STYLE = "narrative_style"
    COMBAT_PATTERN = "combat_pattern"
    SOCIAL_PATTERN = "social_pattern"

class LearningAlgorithm(Enum):
    REINFORCEMENT = "reinforcement"
    SUPERVISED = "supervised"
    UNSUPERVISED = "unsupervised"
    DEEP_LEARNING = "deep_learning"

class AILearningSystem:
    """Comprehensive AI learning system with adaptive behavior"""
    
    def __init__(self):
        self.learning_data_file = "data/ai_learning_data.json"
        self.player_preferences_file = "data/player_preferences.json"
        self.model_weights_file = "data/ai_model_weights.json"
        self._ensure_data_directory()
        self._load_learning_data()
        self._load_player_preferences()
        self._load_model_weights()
        
        # Learning parameters
        self.learning_rate = 0.1
        self.exploration_rate = 0.2
        self.memory_size = 1000
        self.decay_factor = 0.95
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs("data", exist_ok=True)
    
    def _load_learning_data(self):
        """Load AI learning data"""
        try:
            if os.path.exists(self.learning_data_file):
                with open(self.learning_data_file, 'r', encoding='utf-8') as f:
                    self.learning_data = json.load(f)
            else:
                self.learning_data = self._initialize_learning_data()
                self._save_learning_data()
        except Exception as e:
            print(f"Error loading learning data: {e}")
            self.learning_data = self._initialize_learning_data()
    
    def _save_learning_data(self):
        """Save AI learning data"""
        try:
            with open(self.learning_data_file, 'w', encoding='utf-8') as f:
                json.dump(self.learning_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving learning data: {e}")
    
    def _load_player_preferences(self):
        """Load player preferences"""
        try:
            if os.path.exists(self.player_preferences_file):
                with open(self.player_preferences_file, 'r', encoding='utf-8') as f:
                    self.player_preferences = json.load(f)
            else:
                self.player_preferences = {}
        except Exception as e:
            print(f"Error loading player preferences: {e}")
            self.player_preferences = {}
    
    def _save_player_preferences(self):
        """Save player preferences"""
        try:
            with open(self.player_preferences_file, 'w', encoding='utf-8') as f:
                json.dump(self.player_preferences, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving player preferences: {e}")
    
    def _load_model_weights(self):
        """Load AI model weights"""
        try:
            if os.path.exists(self.model_weights_file):
                with open(self.model_weights_file, 'r', encoding='utf-8') as f:
                    self.model_weights = json.load(f)
            else:
                self.model_weights = self._initialize_model_weights()
                self._save_model_weights()
        except Exception as e:
            print(f"Error loading model weights: {e}")
            self.model_weights = self._initialize_model_weights()
    
    def _save_model_weights(self):
        """Save AI model weights"""
        try:
            with open(self.model_weights_file, 'w', encoding='utf-8') as f:
                json.dump(self.model_weights, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving model weights: {e}")
    
    def _initialize_learning_data(self) -> Dict[str, Any]:
        """Initialize learning data structure"""
        return {
            "action_preferences": {},
            "difficulty_adaptations": {},
            "narrative_styles": {},
            "combat_patterns": {},
            "social_patterns": {},
            "global_statistics": {
                "total_actions": 0,
                "total_sessions": 0,
                "average_session_duration": 0,
                "most_popular_actions": [],
                "difficulty_distribution": {}
            },
            "learning_history": [],
            "model_performance": {
                "accuracy": 0.0,
                "prediction_success_rate": 0.0,
                "adaptation_success_rate": 0.0
            }
        }
    
    def _initialize_model_weights(self) -> Dict[str, Any]:
        """Initialize AI model weights"""
        return {
            "action_preference_weights": {
                "combat": 1.0,
                "social": 1.0,
                "exploration": 1.0,
                "stealth": 1.0,
                "magic": 1.0
            },
            "difficulty_weights": {
                "easy": 1.0,
                "medium": 1.0,
                "hard": 1.0
            },
            "narrative_weights": {
                "descriptive": 1.0,
                "action_oriented": 1.0,
                "character_focused": 1.0,
                "plot_driven": 1.0
            },
            "combat_weights": {
                "aggressive": 1.0,
                "defensive": 1.0,
                "tactical": 1.0,
                "supportive": 1.0
            },
            "social_weights": {
                "friendly": 1.0,
                "intimidating": 1.0,
                "persuasive": 1.0,
                "deceptive": 1.0
            }
        }
    
    def learn_from_action(self, player_id: str, action: Dict[str, Any], outcome: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Learn from player action and outcome"""
        try:
            now = datetime.now().isoformat()
            
            # Record action data
            action_data = {
                "id": str(uuid.uuid4()),
                "player_id": player_id,
                "action": action,
                "outcome": outcome,
                "context": context,
                "timestamp": now,
                "success": outcome.get("success", False),
                "satisfaction_score": outcome.get("satisfaction_score", 0.5)
            }
            
            # Update learning data
            self.learning_data["learning_history"].append(action_data)
            
            # Limit history size
            if len(self.learning_data["learning_history"]) > self.memory_size:
                self.learning_data["learning_history"].pop(0)
            
            # Update action preferences
            self._update_action_preferences(player_id, action, outcome)
            
            # Update difficulty adaptation
            self._update_difficulty_adaptation(player_id, action, outcome, context)
            
            # Update narrative style preferences
            self._update_narrative_preferences(player_id, action, outcome, context)
            
            # Update combat patterns
            if action.get("type") == "combat":
                self._update_combat_patterns(player_id, action, outcome, context)
            
            # Update social patterns
            if action.get("type") == "social":
                self._update_social_patterns(player_id, action, outcome, context)
            
            # Update global statistics
            self._update_global_statistics(action_data)
            
            # Retrain models
            self._retrain_models()
            
            self._save_learning_data()
            self._save_player_preferences()
            self._save_model_weights()
            
            return {
                "success": True,
                "action_id": action_data["id"],
                "learning_applied": True,
                "message": "Learning data recorded and applied"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error learning from action: {str(e)}"}
    
    def _update_action_preferences(self, player_id: str, action: Dict[str, Any], outcome: Dict[str, Any]):
        """Update player's action preferences"""
        if player_id not in self.learning_data["action_preferences"]:
            self.learning_data["action_preferences"][player_id] = defaultdict(float)
        
        action_type = action.get("type", "unknown")
        satisfaction_score = outcome.get("satisfaction_score", 0.5)
        
        # Update preference weight using reinforcement learning
        current_weight = self.learning_data["action_preferences"][player_id][action_type]
        reward = satisfaction_score - 0.5  # Normalize to [-0.5, 0.5]
        new_weight = current_weight + (self.learning_rate * reward)
        self.learning_data["action_preferences"][player_id][action_type] = new_weight
    
    def _update_difficulty_adaptation(self, player_id: str, action: Dict[str, Any], outcome: Dict[str, Any], context: Dict[str, Any]):
        """Update difficulty adaptation for player"""
        if player_id not in self.learning_data["difficulty_adaptations"]:
            self.learning_data["difficulty_adaptations"][player_id] = {
                "current_difficulty": "medium",
                "success_rate": 0.5,
                "preferred_difficulty": "medium",
                "adaptation_history": []
            }
        
        difficulty_data = self.learning_data["difficulty_adaptations"][player_id]
        success = outcome.get("success", False)
        
        # Update success rate
        current_rate = difficulty_data["success_rate"]
        difficulty_data["success_rate"] = (current_rate * 0.9) + (1.0 if success else 0.0) * 0.1
        
        # Adapt difficulty
        if difficulty_data["success_rate"] > 0.7:
            # Player is doing well, increase difficulty
            difficulty_levels = ["easy", "medium", "hard"]
            current_index = difficulty_levels.index(difficulty_data["current_difficulty"])
            if current_index < len(difficulty_levels) - 1:
                difficulty_data["current_difficulty"] = difficulty_levels[current_index + 1]
        elif difficulty_data["success_rate"] < 0.3:
            # Player is struggling, decrease difficulty
            difficulty_levels = ["easy", "medium", "hard"]
            current_index = difficulty_levels.index(difficulty_data["current_difficulty"])
            if current_index > 0:
                difficulty_data["current_difficulty"] = difficulty_levels[current_index - 1]
        
        # Record adaptation
        difficulty_data["adaptation_history"].append({
            "timestamp": datetime.now().isoformat(),
            "success_rate": difficulty_data["success_rate"],
            "difficulty": difficulty_data["current_difficulty"],
            "action_type": action.get("type")
        })
    
    def _update_narrative_preferences(self, player_id: str, action: Dict[str, Any], outcome: Dict[str, Any], context: Dict[str, Any]):
        """Update narrative style preferences"""
        if player_id not in self.learning_data["narrative_styles"]:
            self.learning_data["narrative_styles"][player_id] = defaultdict(float)
        
        # Analyze narrative context
        narrative_elements = context.get("narrative_elements", {})
        satisfaction_score = outcome.get("satisfaction_score", 0.5)
        
        for element, value in narrative_elements.items():
            if isinstance(value, (int, float)):
                current_weight = self.learning_data["narrative_styles"][player_id][element]
                reward = satisfaction_score - 0.5
                new_weight = current_weight + (self.learning_rate * reward * value)
                self.learning_data["narrative_styles"][player_id][element] = new_weight
    
    def _update_combat_patterns(self, player_id: str, action: Dict[str, Any], outcome: Dict[str, Any], context: Dict[str, Any]):
        """Update combat patterns"""
        if player_id not in self.learning_data["combat_patterns"]:
            self.learning_data["combat_patterns"][player_id] = {
                "preferred_style": "balanced",
                "attack_frequency": 0.5,
                "defense_frequency": 0.5,
                "tactical_frequency": 0.5,
                "pattern_history": []
            }
        
        combat_data = self.learning_data["combat_patterns"][player_id]
        action_style = action.get("style", "balanced")
        
        # Update pattern frequency
        if action_style in combat_data:
            current_freq = combat_data[f"{action_style}_frequency"]
            combat_data[f"{action_style}_frequency"] = current_freq * 0.9 + 0.1
        
        # Record pattern
        combat_data["pattern_history"].append({
            "timestamp": datetime.now().isoformat(),
            "style": action_style,
            "success": outcome.get("success", False),
            "context": context.get("combat_context", {})
        })
    
    def _update_social_patterns(self, player_id: str, action: Dict[str, Any], outcome: Dict[str, Any], context: Dict[str, Any]):
        """Update social patterns"""
        if player_id not in self.learning_data["social_patterns"]:
            self.learning_data["social_patterns"][player_id] = {
                "preferred_approach": "friendly",
                "persuasion_frequency": 0.5,
                "intimidation_frequency": 0.5,
                "deception_frequency": 0.5,
                "pattern_history": []
            }
        
        social_data = self.learning_data["social_patterns"][player_id]
        action_approach = action.get("approach", "friendly")
        
        # Update pattern frequency
        if action_approach in social_data:
            current_freq = social_data[f"{action_approach}_frequency"]
            social_data[f"{action_approach}_frequency"] = current_freq * 0.9 + 0.1
        
        # Record pattern
        social_data["pattern_history"].append({
            "timestamp": datetime.now().isoformat(),
            "approach": action_approach,
            "success": outcome.get("success", False),
            "context": context.get("social_context", {})
        })
    
    def _update_global_statistics(self, action_data: Dict[str, Any]):
        """Update global statistics"""
        stats = self.learning_data["global_statistics"]
        
        stats["total_actions"] += 1
        
        # Update most popular actions
        action_type = action_data["action"].get("type", "unknown")
        if "action_counts" not in stats:
            stats["action_counts"] = Counter()
        stats["action_counts"][action_type] += 1
        
        # Update difficulty distribution
        difficulty = action_data["context"].get("difficulty", "medium")
        if "difficulty_distribution" not in stats:
            stats["difficulty_distribution"] = Counter()
        stats["difficulty_distribution"][difficulty] += 1
    
    def get_personalized_actions(self, player_id: str, scenario_type: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get personalized actions based on player preferences"""
        try:
            personalized_actions = []
            
            # Get player preferences
            action_preferences = self.learning_data["action_preferences"].get(player_id, {})
            difficulty_adaptation = self.learning_data["difficulty_adaptations"].get(player_id, {})
            narrative_preferences = self.learning_data["narrative_styles"].get(player_id, {})
            
            # Calculate action weights based on preferences
            action_weights = {}
            for action_type in ["combat", "social", "exploration", "stealth", "magic"]:
                base_weight = 1.0
                preference_weight = action_preferences.get(action_type, 0.0)
                action_weights[action_type] = base_weight + preference_weight
            
            # Generate personalized actions
            for action_type, weight in action_weights.items():
                if weight > 1.2:  # High preference
                    personalized_actions.append({
                        "type": action_type,
                        "description": f"🎯 Kişiselleştirilmiş {action_type} aksiyonu",
                        "personalized": True,
                        "preference_score": weight,
                        "difficulty": difficulty_adaptation.get("current_difficulty", "medium"),
                        "narrative_style": self._get_preferred_narrative_style(player_id)
                    })
            
            return personalized_actions
            
        except Exception as e:
            return []
    
    def _get_preferred_narrative_style(self, player_id: str) -> str:
        """Get player's preferred narrative style"""
        narrative_preferences = self.learning_data["narrative_styles"].get(player_id, {})
        
        if not narrative_preferences:
            return "descriptive"
        
        # Find the highest preference
        max_preference = max(narrative_preferences.items(), key=lambda x: x[1])
        return max_preference[0] if max_preference[1] > 0 else "descriptive"
    
    def _retrain_models(self):
        """Retrain AI models based on collected data"""
        try:
            # Simple retraining logic - update weights based on recent data
            recent_data = self.learning_data["learning_history"][-100:]  # Last 100 actions
            
            if not recent_data:
                return
            
            # Calculate success rates for different action types
            action_success_rates = defaultdict(list)
            
            for data_point in recent_data:
                action_type = data_point["action"].get("type", "unknown")
                success = data_point["success"]
                satisfaction = data_point["satisfaction_score"]
                
                action_success_rates[action_type].append(success and satisfaction > 0.5)
            
            # Update model weights
            for action_type, success_list in action_success_rates.items():
                if success_list:
                    success_rate = sum(success_list) / len(success_list)
                    if action_type in self.model_weights["action_preference_weights"]:
                        current_weight = self.model_weights["action_preference_weights"][action_type]
                        new_weight = current_weight * self.decay_factor + success_rate * (1 - self.decay_factor)
                        self.model_weights["action_preference_weights"][action_type] = new_weight
            
            # Update model performance metrics
            recent_success = sum(1 for d in recent_data if d["success"]) / len(recent_data)
            self.learning_data["model_performance"]["accuracy"] = recent_success
            
        except Exception as e:
            print(f"Error retraining models: {e}")
    
    def get_player_insights(self, player_id: str) -> Dict[str, Any]:
        """Get insights about player's behavior and preferences"""
        try:
            insights = {
                "player_id": player_id,
                "preferences": {},
                "patterns": {},
                "recommendations": []
            }
            
            # Action preferences
            action_preferences = self.learning_data["action_preferences"].get(player_id, {})
            if action_preferences:
                insights["preferences"]["favorite_actions"] = sorted(
                    action_preferences.items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:3]
            
            # Difficulty adaptation
            difficulty_data = self.learning_data["difficulty_adaptations"].get(player_id, {})
            if difficulty_data:
                insights["preferences"]["preferred_difficulty"] = difficulty_data.get("preferred_difficulty", "medium")
                insights["preferences"]["success_rate"] = difficulty_data.get("success_rate", 0.5)
            
            # Combat patterns
            combat_data = self.learning_data["combat_patterns"].get(player_id, {})
            if combat_data:
                insights["patterns"]["combat_style"] = combat_data.get("preferred_style", "balanced")
                insights["patterns"]["attack_frequency"] = combat_data.get("attack_frequency", 0.5)
            
            # Social patterns
            social_data = self.learning_data["social_patterns"].get(player_id, {})
            if social_data:
                insights["patterns"]["social_approach"] = social_data.get("preferred_approach", "friendly")
            
            # Generate recommendations
            recommendations = []
            
            if difficulty_data.get("success_rate", 0.5) > 0.7:
                recommendations.append("Daha zorlu görevler deneyebilirsiniz.")
            
            if combat_data.get("defense_frequency", 0.5) < 0.3:
                recommendations.append("Savunma stratejilerini geliştirmeyi düşünebilirsiniz.")
            
            if social_data.get("persuasion_frequency", 0.5) < 0.3:
                recommendations.append("İkna becerilerinizi geliştirmeyi deneyebilirsiniz.")
            
            insights["recommendations"] = recommendations
            
            return insights
            
        except Exception as e:
            return {"error": f"Error getting player insights: {str(e)}"}
    
    def predict_player_behavior(self, player_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Predict player behavior in given context"""
        try:
            predictions = {
                "likely_actions": [],
                "preferred_approach": "balanced",
                "confidence": 0.5
            }
            
            # Get player patterns
            action_preferences = self.learning_data["action_preferences"].get(player_id, {})
            combat_patterns = self.learning_data["combat_patterns"].get(player_id, {})
            social_patterns = self.learning_data["social_patterns"].get(player_id, {})
            
            # Predict likely actions
            if context.get("situation") == "combat":
                if combat_patterns.get("attack_frequency", 0.5) > 0.7:
                    predictions["likely_actions"].append("aggressive_attack")
                elif combat_patterns.get("defense_frequency", 0.5) > 0.7:
                    predictions["likely_actions"].append("defensive_stance")
                else:
                    predictions["likely_actions"].append("tactical_approach")
            
            elif context.get("situation") == "social":
                if social_patterns.get("persuasion_frequency", 0.5) > 0.7:
                    predictions["preferred_approach"] = "persuasive"
                elif social_patterns.get("intimidation_frequency", 0.5) > 0.7:
                    predictions["preferred_approach"] = "intimidating"
                else:
                    predictions["preferred_approach"] = "friendly"
            
            # Calculate confidence based on data availability
            data_points = len(self.learning_data["learning_history"])
            if data_points > 100:
                predictions["confidence"] = 0.8
            elif data_points > 50:
                predictions["confidence"] = 0.6
            else:
                predictions["confidence"] = 0.3
            
            return predictions
            
        except Exception as e:
            return {"error": f"Error predicting behavior: {str(e)}"}
