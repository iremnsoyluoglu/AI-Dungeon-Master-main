#!/usr/bin/env python3
"""
Advanced Story Branching System with Contextual Plot Twists and Betrayal Mechanics
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

@dataclass
class StoryContext:
    """Represents the current story context and state"""
    location: str
    context_type: str
    emotional_state: str
    trust_level: float
    power_level: float
    relationships: Dict[str, float]
    recent_events: List[str]
    betrayal_susceptibility: float
    plot_twist_susceptibility: float

@dataclass
class BetrayalEvent:
    """Represents a betrayal event in the story"""
    betrayer: str
    betrayed: str
    betrayal_type: str
    emotional_impact: str
    story_opportunities: List[str]
    recovery_time: str
    contextual_triggers: List[str]

@dataclass
class PlotTwistEvent:
    """Represents a plot twist event in the story"""
    twist_type: str
    description: str
    emotional_impact: str
    story_opportunities: List[str]
    contextual_triggers: List[str]
    revelation_scope: str

class AdvancedStoryEngine:
    """Advanced storytelling engine with contextual plot twists and betrayal systems"""
    
    def __init__(self):
        self.story_context = StoryContext(
            location="unknown",
            context_type="neutral",
            emotional_state="neutral",
            trust_level=0.5,
            power_level=0.5,
            relationships={},
            recent_events=[],
            betrayal_susceptibility=0.3,
            plot_twist_susceptibility=0.4
        )
        self.betrayal_history = []
        self.plot_twist_history = []
        self.emotional_arcs = {}
        
    def update_context(self, **kwargs):
        """Update the current story context"""
        for key, value in kwargs.items():
            if hasattr(self.story_context, key):
                setattr(self.story_context, key, value)
    
    def analyze_context_for_events(self, scenario_data: Dict) -> Dict[str, Any]:
        """Analyze current context to determine if betrayal or plot twist should occur"""
        contextual_triggers = scenario_data.get("advanced_storytelling", {}).get("contextual_triggers", {})
        
        events = {
            "betrayal": False,
            "plot_twist": False,
            "event_details": None
        }
        
        # Check location-based triggers
        location_triggers = contextual_triggers.get("location_based", {}).get(self.story_context.location, {})
        if location_triggers:
            betrayal_chance = location_triggers.get("betrayal_chance", 0)
            plot_twist_chance = location_triggers.get("plot_twist_chance", 0)
            
            if random.random() < betrayal_chance * self.story_context.betrayal_susceptibility:
                events["betrayal"] = True
                events["event_details"] = self._generate_betrayal_event(location_triggers)
            
            if random.random() < plot_twist_chance * self.story_context.plot_twist_susceptibility:
                events["plot_twist"] = True
                events["event_details"] = self._generate_plot_twist_event(location_triggers)
        
        # Check relationship-based triggers
        for npc, trust_level in self.story_context.relationships.items():
            if trust_level > 0.7:  # High trust = higher betrayal potential
                relationship_triggers = contextual_triggers.get("relationship_based", {})
                for relationship_type, triggers in relationship_triggers.items():
                    betrayal_chance = triggers.get("betrayal_chance", 0)
                    plot_twist_chance = triggers.get("plot_twist_chance", 0)
                    
                    if random.random() < betrayal_chance * trust_level:
                        events["betrayal"] = True
                        events["event_details"] = self._generate_npc_betrayal_event(npc, triggers)
                    
                    if random.random() < plot_twist_chance * trust_level:
                        events["plot_twist"] = True
                        events["event_details"] = self._generate_npc_plot_twist_event(npc, triggers)
        
        return events
    
    def _generate_betrayal_event(self, triggers: Dict) -> BetrayalEvent:
        """Generate a contextual betrayal event"""
        betrayal_types = ["personal_betrayal", "institutional_betrayal", "self_betrayal"]
        betrayal_type = random.choice(betrayal_types)
        
        return BetrayalEvent(
            betrayer="unknown",
            betrayed="player",
            betrayal_type=betrayal_type,
            emotional_impact="devastating",
            story_opportunities=["redemption_arc", "revenge_plot", "forgiveness_journey"],
            recovery_time="long",
            contextual_triggers=triggers.get("triggers", [])
        )
    
    def _generate_plot_twist_event(self, triggers: Dict) -> PlotTwistEvent:
        """Generate a contextual plot twist event"""
        twist_types = ["revelation", "transformation", "awakening"]
        twist_type = random.choice(twist_types)
        
        return PlotTwistEvent(
            twist_type=twist_type,
            description="A shocking revelation changes everything...",
            emotional_impact="transformative",
            story_opportunities=["power_awakening", "perspective_shift", "purpose_revelation"],
            contextual_triggers=triggers.get("triggers", []),
            revelation_scope="personal"
        )
    
    def _generate_npc_betrayal_event(self, npc: str, triggers: Dict) -> BetrayalEvent:
        """Generate an NPC-specific betrayal event"""
        return BetrayalEvent(
            betrayer=npc,
            betrayed="player",
            betrayal_type="personal_betrayal",
            emotional_impact="devastating",
            story_opportunities=["redemption_arc", "revenge_plot", "forgiveness_journey"],
            recovery_time="long",
            contextual_triggers=triggers.get("triggers", [])
        )
    
    def _generate_npc_plot_twist_event(self, npc: str, triggers: Dict) -> PlotTwistEvent:
        """Generate an NPC-specific plot twist event"""
        return PlotTwistEvent(
            twist_type="revelation",
            description=f"{npc} reveals a shocking truth...",
            emotional_impact="transformative",
            story_opportunities=["trust_redefinition", "relationship_evolution", "perspective_shift"],
            contextual_triggers=triggers.get("triggers", []),
            revelation_scope="interpersonal"
        )
    
    def process_story_choice(self, choice_data: Dict, scenario_data: Dict) -> Dict[str, Any]:
        """Process a story choice and determine consequences"""
        # Update context based on choice
        effects = choice_data.get("effects", {})
        self.update_context(**effects)
        
        # Check for contextual events
        contextual_events = self.analyze_context_for_events(scenario_data)
        
        # Get next node
        next_node = choice_data.get("next_node")
        next_node_data = scenario_data.get("nodes", {}).get(next_node, {})
        
        # Enhance story with contextual events
        enhanced_story = self._enhance_story_with_events(next_node_data, contextual_events)
        
        return {
            "next_node": next_node,
            "story_data": enhanced_story,
            "contextual_events": contextual_events,
            "updated_context": asdict(self.story_context)
        }
    
    def _enhance_story_with_events(self, story_data: Dict, contextual_events: Dict) -> Dict:
        """Enhance story data with contextual events"""
        enhanced_story = story_data.copy()
        
        if contextual_events.get("betrayal"):
            betrayal_event = contextual_events["event_details"]
            enhanced_story["description"] += f"\n\n🚨 BETRAYAL ALERT: {betrayal_event.description}"
            enhanced_story["betrayal_effects"] = {
                "emotional_impact": betrayal_event.emotional_impact,
                "story_opportunities": betrayal_event.story_opportunities,
                "recovery_time": betrayal_event.recovery_time
            }
            self.betrayal_history.append(asdict(betrayal_event))
        
        if contextual_events.get("plot_twist"):
            plot_twist_event = contextual_events["event_details"]
            enhanced_story["description"] += f"\n\n✨ PLOT TWIST: {plot_twist_event.description}"
            enhanced_story["plot_twist_effects"] = {
                "emotional_impact": plot_twist_event.emotional_impact,
                "story_opportunities": plot_twist_event.story_opportunities,
                "revelation_scope": plot_twist_event.revelation_scope
            }
            self.plot_twist_history.append(asdict(plot_twist_event))
        
        return enhanced_story
    
    def get_emotional_arc_progression(self, arc_type: str) -> Dict[str, Any]:
        """Get the current progression of an emotional arc"""
        if arc_type not in self.emotional_arcs:
            self.emotional_arcs[arc_type] = {
                "current_stage": 0,
                "stages": ["suspicion", "caution", "trust", "loyalty"],
                "progress": 0.0
            }
        
        return self.emotional_arcs[arc_type]
    
    def advance_emotional_arc(self, arc_type: str, advancement: float = 0.25):
        """Advance an emotional arc"""
        if arc_type not in self.emotional_arcs:
            self.emotional_arcs[arc_type] = {
                "current_stage": 0,
                "stages": ["suspicion", "caution", "trust", "loyalty"],
                "progress": 0.0
            }
        
        arc = self.emotional_arcs[arc_type]
        arc["progress"] += advancement
        
        if arc["progress"] >= 1.0:
            arc["progress"] = 1.0
            if arc["current_stage"] < len(arc["stages"]) - 1:
                arc["current_stage"] += 1
                arc["progress"] = 0.0
        
        return arc
    
    def get_story_summary(self) -> Dict[str, Any]:
        """Get a summary of the current story state"""
        return {
            "context": asdict(self.story_context),
            "betrayal_count": len(self.betrayal_history),
            "plot_twist_count": len(self.plot_twist_history),
            "emotional_arcs": self.emotional_arcs,
            "recent_events": self.story_context.recent_events[-5:] if self.story_context.recent_events else []
        }

class ContextualEventManager:
    """Manages contextual events and their integration into the story"""
    
    def __init__(self):
        self.event_history = []
        self.active_events = []
        
    def check_contextual_triggers(self, story_context: StoryContext, scenario_data: Dict) -> List[Dict]:
        """Check for contextual triggers based on current story context"""
        triggers = []
        contextual_triggers = scenario_data.get("advanced_storytelling", {}).get("contextual_triggers", {})
        
        # Check location-based triggers
        location_triggers = contextual_triggers.get("location_based", {}).get(story_context.location, {})
        if location_triggers:
            for trigger_type, trigger_data in location_triggers.items():
                if self._should_trigger_event(trigger_data, story_context):
                    triggers.append({
                        "type": trigger_type,
                        "context": "location",
                        "data": trigger_data
                    })
        
        # Check relationship-based triggers
        for npc, trust_level in story_context.relationships.items():
            relationship_triggers = contextual_triggers.get("relationship_based", {})
            for relationship_type, trigger_data in relationship_triggers.items():
                if self._should_trigger_event(trigger_data, story_context, trust_level):
                    triggers.append({
                        "type": relationship_type,
                        "context": "relationship",
                        "npc": npc,
                        "data": trigger_data
                    })
        
        return triggers
    
    def _should_trigger_event(self, trigger_data: Dict, story_context: StoryContext, modifier: float = 1.0) -> bool:
        """Determine if an event should be triggered based on context"""
        base_chance = trigger_data.get("chance", 0.5)
        adjusted_chance = base_chance * modifier
        
        # Consider emotional state
        if story_context.emotional_state == "vulnerable":
            adjusted_chance *= 1.5
        elif story_context.emotional_state == "confident":
            adjusted_chance *= 0.7
        
        # Consider recent events
        if len(story_context.recent_events) > 3:
            adjusted_chance *= 0.8  # Less likely if many recent events
        
        return random.random() < adjusted_chance
    
    def generate_event_description(self, event_data: Dict) -> str:
        """Generate a compelling description for a contextual event"""
        event_type = event_data.get("type", "unknown")
        context = event_data.get("context", "general")
        
        descriptions = {
            "betrayal": {
                "location": "Bu yerde güvendiğin biri sana ihanet ediyor...",
                "relationship": "En yakın arkadaşın gerçek yüzünü gösteriyor...",
                "general": "Beklenmedik bir ihanet seni sarsıyor..."
            },
            "plot_twist": {
                "location": "Bu yerin gerçek sırrı ortaya çıkıyor...",
                "relationship": "İlişkinin gerçek doğası açığa çıkıyor...",
                "general": "Şok edici bir gerçek ortaya çıkıyor..."
            }
        }
        
        return descriptions.get(event_type, {}).get(context, "Beklenmedik bir olay gerçekleşiyor...")
    
    def apply_event_effects(self, event_data: Dict, story_context: StoryContext) -> StoryContext:
        """Apply the effects of a contextual event to the story context"""
        event_type = event_data.get("type")
        
        if event_type == "betrayal":
            story_context.trust_level = max(0.0, story_context.trust_level - 0.3)
            story_context.emotional_state = "devastated"
            story_context.betrayal_susceptibility = min(1.0, story_context.betrayal_susceptibility + 0.2)
        
        elif event_type == "plot_twist":
            story_context.plot_twist_susceptibility = min(1.0, story_context.plot_twist_susceptibility + 0.2)
            story_context.emotional_state = "shocked"
            story_context.power_level = min(1.0, story_context.power_level + 0.1)
        
        # Add to recent events
        story_context.recent_events.append(f"{event_type}_{datetime.now().isoformat()}")
        
        return story_context

# Initialize the advanced story engine
story_engine = AdvancedStoryEngine()
event_manager = ContextualEventManager()

def get_enhanced_story_progression(choice_data: Dict, scenario_data: Dict, current_context: Dict = None) -> Dict[str, Any]:
    """Get enhanced story progression with contextual events"""
    if current_context:
        story_engine.story_context = StoryContext(**current_context)
    
    result = story_engine.process_story_choice(choice_data, scenario_data)
    
    # Add visual effects for UI
    if result["contextual_events"].get("betrayal"):
        result["visual_effects"] = {
            "alert_type": "betrayal",
            "animation": "betrayalPulse",
            "color": "#dc2626"
        }
    
    if result["contextual_events"].get("plot_twist"):
        result["visual_effects"] = {
            "alert_type": "plot_twist",
            "animation": "plotTwistGlow",
            "color": "#7c3aed"
        }
    
    return result

def get_story_context_summary() -> Dict[str, Any]:
    """Get a summary of the current story context"""
    return story_engine.get_story_summary()

def advance_emotional_arc(arc_type: str, advancement: float = 0.25) -> Dict[str, Any]:
    """Advance an emotional arc"""
    return story_engine.advance_emotional_arc(arc_type, advancement) 