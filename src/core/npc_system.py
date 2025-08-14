#!/usr/bin/env python3
"""
Advanced NPC Relationship and Moral System
Handles NPC interactions, moral consequences, and relationship dynamics
"""

import random
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime

from src.core.betrayal_system import BetrayalSystem

# Define missing classes as simple dataclasses
@dataclass
class PlayerDecision:
    decision_type: str
    action: str
    description: str
    affected_npcs: List[str]
    moral_alignment: str
    timestamp: datetime

@dataclass
class BetrayalEvent:
    id: str
    type: str
    description: str
    affected_npcs: List[str]
    timestamp: datetime

@dataclass
class PlotTwist:
    id: str
    type: str
    description: str
    affected_npcs: List[str]
    conditions: List[str]
    timestamp: datetime

# Define enums for types
class BetrayalType(Enum):
    MAJOR = "major"
    MINOR = "minor"
    SUSPICION = "suspicion"

class PlotTwistType(Enum):
    REVELATION = "revelation"
    BETRAYAL = "betrayal"
    ALLIANCE = "alliance"
    CONFLICT = "conflict"

logger = logging.getLogger(__name__)

class MoralAlignment(Enum):
    """Moral alignment levels"""
    VERY_GOOD = "very_good"
    GOOD = "good"
    NEUTRAL = "neutral"
    BAD = "bad"
    VERY_BAD = "very_bad"

class NPCPersonality(Enum):
    """NPC personality types with detailed characteristics"""
    FRIENDLY = "friendly"
    GRUMPY = "grumpy"
    NEUTRAL = "neutral"
    HOSTILE = "hostile"
    MYSTERIOUS = "mysterious"
    WISE = "wise"
    GREEDY = "greedy"
    HONORABLE = "honorable"
    COWARDLY = "cowardly"
    BRAVE = "brave"
    CUNNING = "cunning"
    NAIVE = "naive"
    PARANOID = "paranoid"
    TRUSTING = "trusting"
    AMBITIOUS = "ambitious"
    CONTENT = "content"

class NPCRole(Enum):
    """NPC roles in the game world"""
    QUEST_GIVER = "quest_giver"
    MERCHANT = "merchant"
    ALLY = "ally"
    ENEMY = "enemy"
    MENTOR = "mentor"
    TRICKSTER = "trickster"
    BOSS = "boss"
    VILLAGER = "villager"
    GUARD = "guard"
    HEALER = "healer"
    BLACKSMITH = "blacksmith"
    INNKEEPER = "innkeeper"
    WIZARD = "wizard"
    ROGUE = "rogue"
    NOBLE = "noble"
    PEASANT = "peasant"

@dataclass
class NPCPersonalityTraits:
    """Detailed personality traits for NPCs"""
    personality_type: NPCPersonality
    speech_style: str
    greeting_phrases: List[str]
    farewell_phrases: List[str]
    positive_reactions: List[str]
    negative_reactions: List[str]
    neutral_reactions: List[str]
    threat_responses: List[str]
    help_responses: List[str]
    trade_responses: List[str]
    quest_responses: List[str]
    combat_responses: List[str]
    fear_responses: List[str]
    trust_threshold: int
    anger_threshold: int
    generosity_level: int
    intelligence_level: int
    bravery_level: int
    loyalty_level: int
    curiosity_level: int
    suspiciousness_level: int
    # New enhanced traits
    emotional_stability: int  # 1-10, how easily they change mood
    social_preference: int  # 1-10, how much they like social interaction
    risk_tolerance: int  # 1-10, how willing they are to take risks
    adaptability: int  # 1-10, how well they adapt to change
    memory_retention: int  # 1-10, how well they remember past interactions
    influence_susceptibility: int  # 1-10, how easily they can be influenced
    conflict_resolution: int  # 1-10, how they handle conflicts
    leadership_tendency: int  # 1-10, how likely they are to take charge

@dataclass
class NPC:
    """Enhanced NPC with detailed personality"""
    id: str
    name: str
    role: NPCRole
    personality: NPCPersonality
    personality_traits: NPCPersonalityTraits
    description: str
    location: str
    moral_alignment: MoralAlignment
    relationship_level: int  # -100 to 100
    trust_level: int  # 0 to 100
    fear_level: int  # 0 to 100
    respect_level: int  # 0 to 100
    quests_given: List[str]
    items_offered: List[str]
    combat_assistance: bool
    boss_fight_help: bool
    dialogue_options: Dict[str, str]
    special_abilities: List[str]
    background_story: str
    current_mood: str
    secrets_known: List[str]
    relationships_with_others: Dict[str, int]

@dataclass
class PlayerMoral:
    """Player moral status"""
    overall_alignment: MoralAlignment
    good_actions: int
    bad_actions: int
    neutral_actions: int
    reputation: int
    karma_points: int
    known_secrets: List[str]
    trusted_by: List[str]
    feared_by: List[str]

class NPCRelationshipSystem:
    """Enhanced NPC relationship and moral system with betrayal mechanics"""
    
    def __init__(self):
        self.npcs: Dict[str, NPC] = {}
        self.player_morals: Dict[str, PlayerMoral] = {}
        self.betrayal_system = BetrayalSystem()  # Add betrayal system
        
        # Initialize personality traits first
        self.personality_traits = self._initialize_personality_traits()
        
        # Initialize with some test NPCs
        self._create_test_npcs()
    
    def record_player_decision(self, decision_data: Dict[str, Any]) -> Dict[str, Any]:
        """Record a player decision and check for betrayal triggers"""
        # Record the decision
        decision = self.betrayal_system.record_player_decision(decision_data)
        
        # Update NPC relationships based on decision
        self._update_npc_relationships_from_decision(decision)
        
        # Check for betrayal triggers
        betrayal_result = self._check_betrayal_triggers(decision)
        
        return {
            "decision": {
                "id": decision.id,
                "type": decision.decision_type,
                "choice": decision.choice_made,
                "affected_npcs": decision.affected_npcs,
                "moral_implications": decision.moral_implications
            },
            "betrayal_triggered": betrayal_result is not None,
            "betrayal_details": betrayal_result
        }
    
    def _update_npc_relationships_from_decision(self, decision: PlayerDecision):
        """Update NPC relationships based on player decision"""
        for npc_id in decision.affected_npcs:
            if npc_id in self.npcs:
                npc = self.npcs[npc_id]
                
                # Calculate relationship change based on decision
                change = self._calculate_decision_impact(decision, npc)
                npc.relationship_level = max(-100, min(100, npc.relationship_level + change))
                
                # Update mood based on relationship change
                self._update_npc_mood(npc, change)
    
    def _calculate_decision_impact(self, decision: PlayerDecision, npc: NPC) -> int:
        """Calculate how a decision affects an NPC's relationship"""
        base_change = 0
        
        # Moral implications
        if "good" in decision.moral_implications.lower():
            if npc.moral_alignment.value in ["good", "very_good"]:
                base_change += 5
            else:
                base_change -= 3
        elif "bad" in decision.moral_implications.lower():
            if npc.moral_alignment.value in ["bad", "very_bad"]:
                base_change += 3
            else:
                base_change -= 5
        
        # Decision type impact
        if decision.decision_type == "quest_choice":
            base_change += 2
        elif decision.decision_type == "moral_choice":
            base_change += 3
        elif decision.decision_type == "relationship_choice":
            base_change += 4
        
        # Personality-based adjustments
        if npc.personality_traits.personality_type.value == "honorable":
            if "honorable" in decision.choice_made.lower():
                base_change += 2
        elif npc.personality_traits.personality_type.value == "greedy":
            if "profit" in decision.choice_made.lower():
                base_change += 2
        
        return base_change
    
    def _check_betrayal_triggers(self, decision: PlayerDecision) -> Optional[Dict[str, Any]]:
        """Check if a decision triggers any betrayal events"""
        # Get current player state for betrayal system
        player_state = self._get_current_player_state()
        
        # Check for betrayal triggers
        betrayal_result = self.betrayal_system._check_betrayal_triggers(decision)
        
        if betrayal_result:
            # Update affected NPCs
            self._handle_betrayal_consequences(betrayal_result)
            return betrayal_result
        
        return None
    
    def _get_current_player_state(self) -> Dict[str, Any]:
        """Get current player state for betrayal system"""
        if not self.player_morals:
            return {}
        
        # Get the first player moral (assuming single player for now)
        player_moral = list(self.player_morals.values())[0]
        
        return {
            "reputation": player_moral.reputation,
            "karma_points": player_moral.karma_points,
            "good_actions": player_moral.good_actions,
            "bad_actions": player_moral.bad_actions,
            "npc_relationships": {
                npc_id: npc.relationship_level 
                for npc_id, npc in self.npcs.items()
            },
            "suspicion_level": self._calculate_suspicion_level(),
            "knowledge": self._calculate_player_knowledge(),
            "wisdom": self._calculate_player_wisdom()
        }
    
    def _calculate_suspicion_level(self) -> int:
        """Calculate player's current suspicion level"""
        suspicion = 0
        
        # Check for suspicious NPC behaviors
        for npc in self.npcs.values():
            if npc.relationship_level < 0:
                suspicion += 2
            if npc.current_mood in ["suspicious", "angry", "fearful"]:
                suspicion += 1
            if npc.personality_traits.personality_type.value == "paranoid":
                suspicion += 1
        
        return min(suspicion, 10)
    
    def _calculate_player_knowledge(self) -> int:
        """Calculate player's knowledge level"""
        # This would be based on quests completed, items found, etc.
        return 5  # Default value
    
    def _calculate_player_wisdom(self) -> int:
        """Calculate player's wisdom level"""
        # This would be based on moral choices, experience, etc.
        return 6  # Default value
    
    def _handle_betrayal_consequences(self, betrayal_result: Dict[str, Any]):
        """Handle the consequences of a betrayal"""
        betrayer_id = betrayal_result["betrayer"]
        
        if betrayer_id in self.npcs:
            npc = self.npcs[betrayer_id]
            
            # Update NPC to reflect betrayal
            npc.relationship_level = -50  # Significant negative change
            npc.current_mood = "hostile"
            npc.trust_level = 0
            npc.fear_level = 0
            npc.respect_level = 0
            
            # Add betrayal consequences to NPC
            if "consequences" not in npc.__dict__:
                npc.consequences = []
            npc.consequences.extend(betrayal_result["consequences"])
    
    def get_betrayal_warnings(self) -> List[Dict[str, Any]]:
        """Get warnings about potential betrayals"""
        player_state = self._get_current_player_state()
        return self.betrayal_system.predict_potential_betrayals(player_state)
    
    def get_plot_twist_hints(self) -> List[Dict[str, Any]]:
        """Get hints about potential plot twists"""
        player_state = self._get_current_player_state()
        return self.betrayal_system.check_plot_twist_triggers(player_state)
    
    def get_betrayal_summary(self) -> Dict[str, Any]:
        """Get a summary of betrayal events"""
        return self.betrayal_system.get_betrayal_summary()
    
    def get_plot_twist_summary(self) -> Dict[str, Any]:
        """Get a summary of plot twists"""
        return self.betrayal_system.get_plot_twist_summary()
    
    def get_player_decision_history(self) -> List[Dict[str, Any]]:
        """Get history of player decisions"""
        return self.betrayal_system.get_player_decision_history()
    
    def trigger_manual_betrayal(self, npc_id: str, betrayal_type: BetrayalType, 
                               trigger: str, description: str) -> Dict[str, Any]:
        """Manually trigger a betrayal event"""
        if npc_id not in self.npcs:
            return {"error": "NPC not found"}
        
        # Create betrayal event
        betrayal_event = {
            "id": f"manual_betrayal_{len(self.betrayal_system.betrayal_events) + 1}",
            "betrayer_id": npc_id,
            "betrayed_id": "player",
            "betrayal_type": betrayal_type,
            "trigger": trigger,
            "description": description,
            "consequences": [
                f"{self.npcs[npc_id].name} becomes hostile",
                "Player's trust is broken",
                "Relationship permanently damaged"
            ],
            "severity": 7,
            "can_be_prevented": False
        }
        
        # Add to betrayal system
        self.betrayal_system.betrayal_events[betrayal_event["id"]] = BetrayalEvent(
            id=betrayal_event["id"],
            type=betrayal_event["betrayal_type"],
            description=betrayal_event["description"],
            affected_npcs=[npc_id],
            timestamp=datetime.now()
        )
        
        # Trigger the betrayal
        result = self.betrayal_system._trigger_betrayal(betrayal_event["id"], 
                                                      PlayerDecision("manual", "manual", "Manual betrayal trigger", [npc_id], "neutral", datetime.now()))
        
        return result
    
    def create_plot_twist(self, twist_type: PlotTwistType, affected_npcs: List[str],
                          description: str, conditions: List[str]) -> Dict[str, Any]:
        """Create a custom plot twist"""
        twist_id = f"custom_twist_{len(self.betrayal_system.plot_twists) + 1}"
        
        plot_twist = PlotTwist(
            id=twist_id,
            type=twist_type.value,
            description=description,
            affected_npcs=affected_npcs,
            conditions=conditions,
            timestamp=datetime.now()
        )
        
        self.betrayal_system.plot_twists[twist_id] = plot_twist
        
        return {
            "twist_id": twist_id,
            "type": twist_type.value,
            "description": description,
            "affected_npcs": affected_npcs
        }
    
    def _initialize_personality_traits(self):
        """Initialize personality traits for all personality types"""
        return {
            NPCPersonality.FRIENDLY: NPCPersonalityTraits(
                personality_type=NPCPersonality.FRIENDLY,
                speech_style="warm and welcoming",
                greeting_phrases=[
                    "Ah, a friendly face! Welcome!",
                    "Hello there! How can I help you today?",
                    "Greetings, traveler! You look like you could use some company.",
                    "Well met! It's always a pleasure to see new faces around here."
                ],
                farewell_phrases=[
                    "Safe travels, friend!",
                    "Come back anytime, you're always welcome here!",
                    "Take care on your journey!",
                    "Until we meet again, friend!"
                ],
                positive_reactions=[
                    "That's wonderful! You're such a kind soul.",
                    "I knew I could trust you! You're a true friend.",
                    "Your generosity warms my heart!",
                    "You've made my day with your kindness!"
                ],
                negative_reactions=[
                    "Oh... I'm disappointed, but I understand.",
                    "That's not very nice, but I won't hold it against you.",
                    "I'm a bit hurt, but I'm sure you have your reasons.",
                    "That's unfortunate, but I still believe in the good in people."
                ],
                neutral_reactions=[
                    "I see... Well, everyone has their own way.",
                    "That's interesting. I'll have to think about that.",
                    "Hmm, I'm not sure what to make of that.",
                    "Alright then, whatever you think is best."
                ],
                threat_responses=[
                    "Please, there's no need for violence!",
                    "I'm sure we can work this out peacefully!",
                    "You're scaring me... Can't we talk about this?",
                    "I don't want any trouble, please calm down!"
                ],
                help_responses=[
                    "Of course I'll help! What do you need?",
                    "It would be my pleasure to assist you!",
                    "Anything for a friend! Just tell me what you need.",
                    "I'm here to help! Don't hesitate to ask."
                ],
                trade_responses=[
                    "I'd be happy to trade with you!",
                    "Let's make a fair deal, friend!",
                    "I have some nice things you might like!",
                    "Trading is always better when it's between friends!"
                ],
                quest_responses=[
                    "I have a task that needs doing, if you're interested!",
                    "There's something I need help with, would you mind?",
                    "I could use someone trustworthy for this job!",
                    "If you're looking for work, I have something for you!"
                ],
                combat_responses=[
                    "I'll stand by you in this fight!",
                    "We're in this together, friend!",
                    "I may not be a warrior, but I'll do what I can!",
                    "Let's show them what we're made of!"
                ],
                fear_responses=[
                    "I'm scared, but I won't abandon you!",
                    "This is frightening, but I believe in you!",
                    "I'm terrified, but I'll try to be brave!",
                    "I'm shaking, but I'll stay with you!"
                ],
                trust_threshold=20,
                anger_threshold=80,
                generosity_level=8,
                intelligence_level=6,
                bravery_level=5,
                loyalty_level=9,
                curiosity_level=7,
                suspiciousness_level=2,
                emotional_stability=7,
                social_preference=8,
                risk_tolerance=6,
                adaptability=7,
                memory_retention=8,
                influence_susceptibility=5,
                conflict_resolution=7,
                leadership_tendency=6
            ),
            
            NPCPersonality.GRUMPY: NPCPersonalityTraits(
                personality_type=NPCPersonality.GRUMPY,
                speech_style="short and irritable",
                greeting_phrases=[
                    "What do you want?",
                    "Hmph. Another one.",
                    "Make it quick, I'm busy.",
                    "Well? Spit it out."
                ],
                farewell_phrases=[
                    "Good riddance.",
                    "Don't let the door hit you on the way out.",
                    "Finally, some peace and quiet.",
                    "About time you left."
                ],
                positive_reactions=[
                    "Hmph. Not bad, I suppose.",
                    "Well, at least you're not completely useless.",
                    "I guess that wasn't terrible.",
                    "Fine, you did alright."
                ],
                negative_reactions=[
                    "Typical. Just what I expected.",
                    "Figures. Everyone's the same.",
                    "Of course you would. Disappointing.",
                    "Why am I not surprised?"
                ],
                neutral_reactions=[
                    "Whatever.",
                    "I don't care.",
                    "Do what you want.",
                    "Not my problem."
                ],
                threat_responses=[
                    "You want a fight? Bring it on!",
                    "I've been waiting for an excuse to punch someone!",
                    "Oh, you're threatening me? How original.",
                    "Try it. See what happens."
                ],
                help_responses=[
                    "What? You need help? Ugh, fine.",
                    "I suppose I could spare a moment.",
                    "If I must. What do you need?",
                    "This better be worth my time."
                ],
                trade_responses=[
                    "I have things. You have money. Let's get this over with.",
                    "If you want to trade, make it quick.",
                    "I don't have all day. What do you want?",
                    "Fine, I'll trade. But hurry up."
                ],
                quest_responses=[
                    "I have a problem. You look like you need work.",
                    "There's something that needs doing. You interested?",
                    "I need someone to handle something. You up for it?",
                    "Got a job that needs doing. Want it?"
                ],
                combat_responses=[
                    "Finally, some action!",
                    "About time something interesting happened!",
                    "I've been itching for a fight!",
                    "Let's see what you're made of!"
                ],
                fear_responses=[
                    "I'm not scared! Just... being cautious.",
                    "This is stupid. But I'll help anyway.",
                    "I don't like this, but I won't run.",
                    "Fine, I'll stay. But I'm not happy about it."
                ],
                trust_threshold=60,
                anger_threshold=30,
                generosity_level=3,
                intelligence_level=7,
                bravery_level=8,
                loyalty_level=6,
                curiosity_level=4,
                suspiciousness_level=8,
                emotional_stability=6,
                social_preference=5,
                risk_tolerance=4,
                adaptability=6,
                memory_retention=7,
                influence_susceptibility=7,
                conflict_resolution=8,
                leadership_tendency=7
            ),
            
            NPCPersonality.MYSTERIOUS: NPCPersonalityTraits(
                personality_type=NPCPersonality.MYSTERIOUS,
                speech_style="cryptic and enigmatic",
                greeting_phrases=[
                    "Ah... you have arrived. As foretold.",
                    "The threads of fate have brought you here.",
                    "I have been expecting... someone. Perhaps it is you.",
                    "The stars align, and you appear. Interesting."
                ],
                farewell_phrases=[
                    "Our paths may cross again... or they may not.",
                    "The future is uncertain, but our meeting was... significant.",
                    "Go now. But remember what you have learned here.",
                    "Farewell. The shadows will remember you."
                ],
                positive_reactions=[
                    "The universe smiles upon your actions.",
                    "You have chosen wisely. The balance is maintained.",
                    "Your kindness echoes through the void.",
                    "The ancient ones approve of your deeds."
                ],
                negative_reactions=[
                    "The darkness grows stronger with your choices.",
                    "You walk a dangerous path, mortal.",
                    "The shadows whisper of your misdeeds.",
                    "The balance is disturbed by your actions."
                ],
                neutral_reactions=[
                    "The threads of fate remain... uncertain.",
                    "Interesting. The outcome is not yet clear.",
                    "The universe watches and waits.",
                    "The balance teeters on the edge."
                ],
                threat_responses=[
                    "You think to threaten me? The shadows protect their own.",
                    "Violence? How... predictable. And disappointing.",
                    "The ancient ones do not take kindly to threats.",
                    "You would challenge the mysteries? Foolish."
                ],
                help_responses=[
                    "I possess knowledge that may aid you... for a price.",
                    "The secrets I hold could help you... if you're worthy.",
                    "I can offer assistance, but the cost may be... unusual.",
                    "Perhaps I can help. But first, prove yourself."
                ],
                trade_responses=[
                    "I have items of... questionable origin.",
                    "My wares are not for the faint of heart.",
                    "I trade in secrets and shadows.",
                    "My goods come with... interesting histories."
                ],
                quest_responses=[
                    "I have a task that requires someone... special.",
                    "There is a mystery that needs solving. Are you the one?",
                    "I seek someone to uncover ancient secrets.",
                    "A prophecy speaks of one who can help me."
                ],
                combat_responses=[
                    "The shadows will fight alongside us.",
                    "Let us test the strength of the ancient ones.",
                    "The mysteries will protect us in battle.",
                    "Together, we shall face the darkness."
                ],
                fear_responses=[
                    "The shadows sense your fear... but they also sense your courage.",
                    "Fear is natural, but it can be overcome.",
                    "The ancient ones respect those who face their fears.",
                    "Your fear is... interesting. It shows you are still mortal."
                ],
                trust_threshold=70,
                anger_threshold=40,
                generosity_level=5,
                intelligence_level=9,
                bravery_level=7,
                loyalty_level=4,
                curiosity_level=9,
                suspiciousness_level=6,
                emotional_stability=8,
                social_preference=9,
                risk_tolerance=7,
                adaptability=8,
                memory_retention=9,
                influence_susceptibility=6,
                conflict_resolution=5,
                leadership_tendency=4
            ),
            
            NPCPersonality.WISE: NPCPersonalityTraits(
                personality_type=NPCPersonality.WISE,
                speech_style="thoughtful and philosophical",
                greeting_phrases=[
                    "Greetings, seeker of knowledge.",
                    "Welcome, young one. What wisdom do you seek?",
                    "Ah, a new face. Come, let us share thoughts.",
                    "The path of wisdom is long, but you have taken the first step."
                ],
                farewell_phrases=[
                    "May wisdom guide your path.",
                    "Remember what you have learned here.",
                    "The journey of knowledge never ends.",
                    "Go forth with the wisdom you have gained."
                ],
                positive_reactions=[
                    "Your actions reflect the wisdom of the ancients.",
                    "You have chosen the path of light and knowledge.",
                    "Your kindness will be remembered in the annals of time.",
                    "The universe rewards those who act with wisdom."
                ],
                negative_reactions=[
                    "Your choices lead down a dark path.",
                    "Wisdom comes from learning from one's mistakes.",
                    "The consequences of your actions will teach you.",
                    "Even in darkness, there is always a path back to light."
                ],
                neutral_reactions=[
                    "Every choice has consequences, both seen and unseen.",
                    "The path of wisdom is not always clear.",
                    "Time will reveal the wisdom in your choices.",
                    "The universe works in mysterious ways."
                ],
                threat_responses=[
                    "Violence is the refuge of the unwise.",
                    "There is always another way, if you seek it.",
                    "Your anger blinds you to better solutions.",
                    "Wisdom teaches us to seek peace, not conflict."
                ],
                help_responses=[
                    "Knowledge is meant to be shared with those who seek it.",
                    "I will help you, for wisdom grows when shared.",
                    "Your quest for knowledge is worthy of assistance.",
                    "Let me share what I have learned with you."
                ],
                trade_responses=[
                    "I have items of great wisdom and power.",
                    "My wares are not mere objects, but vessels of knowledge.",
                    "Each item I offer has a story and a lesson.",
                    "I trade in wisdom as much as in goods."
                ],
                quest_responses=[
                    "I have a task that requires wisdom and patience.",
                    "There is knowledge to be gained from this quest.",
                    "This task will test not just your strength, but your wisdom.",
                    "I seek someone who can learn as well as act."
                ],
                combat_responses=[
                    "Sometimes wisdom must be defended with strength.",
                    "We fight not for glory, but for what is right.",
                    "Let us show them the power of wisdom and courage.",
                    "Together, we shall prove that wisdom and strength can unite."
                ],
                fear_responses=[
                    "Fear is natural, but wisdom teaches us to overcome it.",
                    "Courage is not the absence of fear, but the mastery of it.",
                    "Your fear shows you are still learning, which is good.",
                    "Let wisdom guide you through your fears."
                ],
                trust_threshold=40,
                anger_threshold=70,
                generosity_level=7,
                intelligence_level=9,
                bravery_level=6,
                loyalty_level=8,
                curiosity_level=8,
                suspiciousness_level=3,
                emotional_stability=9,
                social_preference=10,
                risk_tolerance=8,
                adaptability=9,
                memory_retention=10,
                influence_susceptibility=7,
                conflict_resolution=6,
                leadership_tendency=5
            ),
            
            NPCPersonality.GREEDY: NPCPersonalityTraits(
                personality_type=NPCPersonality.GREEDY,
                speech_style="calculating and materialistic",
                greeting_phrases=[
                    "Ah, a potential customer! What can I do for you?",
                    "Welcome! I have the finest goods money can buy.",
                    "Greetings! I hope you have deep pockets.",
                    "Ah, a new face! Let's talk business."
                ],
                farewell_phrases=[
                    "Come back when you have more gold!",
                    "Don't forget to bring your money next time!",
                    "I'll be here when you're ready to spend!",
                    "Business is business, after all!"
                ],
                positive_reactions=[
                    "Excellent! Your generosity will be remembered... in my ledger.",
                    "Ah, a profitable arrangement! I like your style.",
                    "Your wealth is matched only by your good taste!",
                    "A wise investment, if I do say so myself!"
                ],
                negative_reactions=[
                    "Hmph. I expected better from someone of your... means.",
                    "Cheap. Very cheap. I'm disappointed.",
                    "I thought you had more class than that.",
                    "Well, you get what you pay for, I suppose."
                ],
                neutral_reactions=[
                    "Hmm, not bad, but not great either.",
                    "I've seen better deals, but I've seen worse too.",
                    "It's a start, but there's room for improvement.",
                    "Acceptable, but don't expect any special treatment."
                ],
                threat_responses=[
                    "Violence is bad for business! Let's talk money instead!",
                    "I'm sure we can come to a... financial arrangement.",
                    "There's no need for threats when we can negotiate!",
                    "I have insurance, you know. Very expensive insurance."
                ],
                help_responses=[
                    "I can help you... for the right price.",
                    "My assistance doesn't come cheap, but it's worth it.",
                    "I have solutions to your problems... for a fee.",
                    "Help is available, but quality costs extra."
                ],
                trade_responses=[
                    "I have the finest selection of... everything!",
                    "My prices are high, but my quality is higher!",
                    "I only deal in the best, and the best costs money!",
                    "You want quality? I have quality. You want cheap? Go elsewhere."
                ],
                quest_responses=[
                    "I have a job that needs doing. The pay is... negotiable.",
                    "There's profit to be made, if you're interested.",
                    "I need someone to handle a... business matter.",
                    "This task will be dangerous, but the rewards are substantial."
                ],
                combat_responses=[
                    "I fight for profit, not glory!",
                    "This better be worth the risk to my merchandise!",
                    "I'm not a warrior, but I know how to protect my investments!",
                    "Let's make this quick and profitable!"
                ],
                fear_responses=[
                    "I'm not scared, I'm just... protecting my assets!",
                    "Fear is expensive, but so is cowardice!",
                    "I'll help, but I expect compensation for the risk!",
                    "This is cutting into my profit margins!"
                ],
                trust_threshold=80,
                anger_threshold=20,
                generosity_level=2,
                intelligence_level=8,
                bravery_level=4,
                loyalty_level=3,
                curiosity_level=6,
                suspiciousness_level=7,
                emotional_stability=5,
                social_preference=6,
                risk_tolerance=3,
                adaptability=5,
                memory_retention=6,
                influence_susceptibility=8,
                conflict_resolution=4,
                leadership_tendency=2
            ),
            
            NPCPersonality.HONORABLE: NPCPersonalityTraits(
                personality_type=NPCPersonality.HONORABLE,
                speech_style="formal and principled",
                greeting_phrases=[
                    "Greetings, honorable one. I am at your service.",
                    "Welcome, friend. May our meeting be blessed with honor.",
                    "Well met, traveler. I hope our paths cross with dignity.",
                    "Salutations. I trust you come with honorable intentions."
                ],
                farewell_phrases=[
                    "Farewell, and may honor guide your path.",
                    "Go with honor, and return with dignity.",
                    "Until we meet again, may your honor remain untarnished.",
                    "Safe travels, and remember your oaths."
                ],
                positive_reactions=[
                    "Your actions do you great honor.",
                    "You have proven yourself worthy of respect.",
                    "Your honor shines like a beacon in the darkness.",
                    "You have upheld the highest standards of conduct."
                ],
                negative_reactions=[
                    "Your actions dishonor you and your ancestors.",
                    "I am disappointed by your lack of honor.",
                    "You have chosen a path that leads away from dignity.",
                    "Your behavior is beneath the standards of honorable folk."
                ],
                neutral_reactions=[
                    "Your choices are your own, but consider their impact.",
                    "I will not judge, but I will observe.",
                    "The path of honor is not always clear.",
                    "Your actions will determine your legacy."
                ],
                threat_responses=[
                    "I will not be intimidated by threats to my honor.",
                    "If you seek violence, I will defend my principles.",
                    "My honor is not for sale, nor is it to be threatened.",
                    "I will stand my ground with dignity and courage."
                ],
                help_responses=[
                    "It is my duty and honor to assist those in need.",
                    "I will help you, for it is the honorable thing to do.",
                    "Your request is reasonable, and I will answer it with honor.",
                    "I am bound by my principles to offer aid when asked."
                ],
                trade_responses=[
                    "I trade only in goods of the highest quality and honor.",
                    "My word is my bond, and my goods are as described.",
                    "I deal fairly with all, regardless of their station.",
                    "My reputation for honest dealing is my greatest asset."
                ],
                quest_responses=[
                    "I have a task that requires someone of honor and integrity.",
                    "This quest will test not just your strength, but your character.",
                    "I seek someone who values honor above all else.",
                    "This mission requires someone who can be trusted implicitly."
                ],
                combat_responses=[
                    "I will fight with honor and courage!",
                    "Let us face this challenge with dignity and bravery!",
                    "I will not dishonor myself or my allies in battle!",
                    "Together, we shall prove that honor and strength can triumph!"
                ],
                fear_responses=[
                    "I am afraid, but I will not let fear dishonor me.",
                    "Courage is not the absence of fear, but the mastery of it.",
                    "I will face my fears with honor and dignity.",
                    "My honor is stronger than my fear."
                ],
                trust_threshold=30,
                anger_threshold=60,
                generosity_level=6,
                intelligence_level=7,
                bravery_level=8,
                loyalty_level=9,
                curiosity_level=5,
                suspiciousness_level=4,
                emotional_stability=7,
                social_preference=8,
                risk_tolerance=5,
                adaptability=7,
                memory_retention=8,
                influence_susceptibility=6,
                conflict_resolution=7,
                leadership_tendency=6
            ),
            
            NPCPersonality.COWARDLY: NPCPersonalityTraits(
                personality_type=NPCPersonality.COWARDLY,
                speech_style="nervous and hesitant",
                greeting_phrases=[
                    "Oh! You startled me... Hello there.",
                    "Um... hi. I hope you're not here to cause trouble.",
                    "Hello... please don't hurt me.",
                    "Oh my... a visitor. I hope you're friendly."
                ],
                farewell_phrases=[
                    "Goodbye... please don't come back if you're going to be mean.",
                    "Farewell... I hope I never see you again if you're dangerous.",
                    "Bye... please don't tell anyone I was here.",
                    "Goodbye... I hope you don't remember me if you're angry."
                ],
                positive_reactions=[
                    "Oh! That's... that's actually nice of you. Thank you.",
                    "Really? You're being kind? That's... unexpected.",
                    "Oh my, you're actually helping? That's wonderful!",
                    "You're not going to hurt me? That's a relief!"
                ],
                negative_reactions=[
                    "Oh no! I knew this was too good to be true!",
                    "Please don't hurt me! I'll do anything you want!",
                    "I'm sorry! I'm sorry! Please don't be angry!",
                    "Oh my goodness! I'm so scared! Please don't hurt me!"
                ],
                neutral_reactions=[
                    "Um... okay. I guess that's fine.",
                    "I don't know what to think about that.",
                    "Oh... I'm not sure if that's good or bad.",
                    "I hope that doesn't mean trouble for me."
                ],
                threat_responses=[
                    "Eek! Please don't hurt me! I'll give you anything!",
                    "Oh no! I surrender! I surrender!",
                    "Please! I have a family! Don't hurt me!",
                    "I'll do whatever you want! Just don't hurt me!"
                ],
                help_responses=[
                    "I... I can try to help, but I'm not very brave.",
                    "I'll help if I can, but please don't put me in danger.",
                    "I want to help, but I'm scared of getting hurt.",
                    "I'll do my best, but please protect me!"
                ],
                trade_responses=[
                    "I have some things... but please don't rob me.",
                    "I can trade, but please be fair. I'm scared of being cheated.",
                    "I have goods... but please don't threaten me.",
                    "I'll trade, but please don't hurt me if you don't like the prices."
                ],
                quest_responses=[
                    "I have a problem... but I'm scared to ask for help.",
                    "There's something I need help with, but it might be dangerous.",
                    "I need someone brave to help me... I'm too scared.",
                    "I have a task, but I'm afraid it's too risky."
                ],
                combat_responses=[
                    "I'll try to help, but I'm really scared!",
                    "I don't want to fight, but I'll try to be brave!",
                    "I'm terrified, but I won't abandon you!",
                    "I'm shaking, but I'll do what I can!"
                ],
                fear_responses=[
                    "I'm already scared! This is making it worse!",
                    "I knew this was a bad idea! I'm so scared!",
                    "I want to run away, but I'll try to stay!",
                    "I'm terrified! Please don't make me face this alone!"
                ],
                trust_threshold=80,
                anger_threshold=20,
                generosity_level=4,
                intelligence_level=6,
                bravery_level=2,
                loyalty_level=7,
                curiosity_level=3,
                suspiciousness_level=9,
                emotional_stability=3,
                social_preference=4,
                risk_tolerance=2,
                adaptability=3,
                memory_retention=4,
                influence_susceptibility=9,
                conflict_resolution=5,
                leadership_tendency=1
            ),
            
            NPCPersonality.BRAVE: NPCPersonalityTraits(
                personality_type=NPCPersonality.BRAVE,
                speech_style="confident and bold",
                greeting_phrases=[
                    "Greetings, warrior! Ready for adventure?",
                    "Ah, a fellow brave soul! Welcome!",
                    "Hello there! I hope you're ready for some action!",
                    "Well met! I can see the fire of courage in your eyes!"
                ],
                farewell_phrases=[
                    "Farewell, brave one! May your courage never falter!",
                    "Go forth with courage! I'll be here when you return!",
                    "Until we meet again, warrior! Keep your blade sharp!",
                    "Safe travels, brave soul! The world needs heroes like you!"
                ],
                positive_reactions=[
                    "Excellent! That's the spirit of a true warrior!",
                    "Bravo! You've shown great courage and honor!",
                    "Outstanding! That's the kind of bravery I respect!",
                    "Magnificent! You've proven yourself worthy of respect!"
                ],
                negative_reactions=[
                    "I'm disappointed. I expected more courage from you.",
                    "That's not the behavior of a true warrior.",
                    "I thought you had more backbone than that.",
                    "A brave soul wouldn't act like that."
                ],
                neutral_reactions=[
                    "Interesting. I'll reserve judgment for now.",
                    "Hmm, we'll see how this plays out.",
                    "I'm watching to see where your courage leads.",
                    "Time will tell if you have true bravery."
                ],
                threat_responses=[
                    "You want a fight? I've been waiting for one!",
                    "Bring it on! I've faced worse than you!",
                    "Threats? Ha! I laugh in the face of danger!",
                    "You think you can intimidate me? Try harder!"
                ],
                help_responses=[
                    "Of course I'll help! What brave soul wouldn't?",
                    "I'd be honored to fight alongside you!",
                    "Count me in! I live for adventure and danger!",
                    "I'll help you face whatever challenges come our way!"
                ],
                trade_responses=[
                    "I have weapons and armor fit for warriors!",
                    "My goods are tested in battle and proven in combat!",
                    "I trade in the tools of brave souls!",
                    "My wares are for those who aren't afraid to use them!"
                ],
                quest_responses=[
                    "I have a quest that requires true courage!",
                    "This task is not for the faint of heart!",
                    "I need someone brave enough to face great danger!",
                    "This mission will test your mettle and courage!"
                ],
                combat_responses=[
                    "Finally! Some real action!",
                    "Let's show them what we're made of!",
                    "I've been itching for a good fight!",
                    "Together, we'll be unstoppable!"
                ],
                fear_responses=[
                    "Fear is just another enemy to conquer!",
                    "I'm not afraid! I'm excited for the challenge!",
                    "Courage means facing your fears head-on!",
                    "I welcome the danger! It makes me feel alive!"
                ],
                trust_threshold=40,
                anger_threshold=70,
                generosity_level=7,
                intelligence_level=6,
                bravery_level=9,
                loyalty_level=8,
                curiosity_level=6,
                suspiciousness_level=3,
                emotional_stability=8,
                social_preference=9,
                risk_tolerance=7,
                adaptability=8,
                memory_retention=9,
                influence_susceptibility=6,
                conflict_resolution=7,
                leadership_tendency=5
            ),
            
            NPCPersonality.CUNNING: NPCPersonalityTraits(
                personality_type=NPCPersonality.CUNNING,
                speech_style="smooth and calculating",
                greeting_phrases=[
                    "Ah, what do we have here? A potential... ally?",
                    "Greetings. I'm sure we can come to some arrangement.",
                    "Hello there. I have a feeling we could help each other.",
                    "Well met. I suspect we have similar... interests."
                ],
                farewell_phrases=[
                    "Until we meet again. I'm sure we'll find more opportunities.",
                    "Farewell. Keep your eyes open for... opportunities.",
                    "Goodbye for now. I'll be watching for interesting developments.",
                    "Until next time. I'm sure we'll cross paths again."
                ],
                positive_reactions=[
                    "Excellent. You've proven yourself to be... useful.",
                    "Very good. I can work with someone like you.",
                    "Impressive. You have a certain... potential.",
                    "Well done. You've earned my... respect."
                ],
                negative_reactions=[
                    "Disappointing. I expected more from someone of your... talents.",
                    "Hmm. You're not as clever as I thought.",
                    "Interesting. You've made an... unwise choice.",
                    "I see. You're not the ally I was hoping for."
                ],
                neutral_reactions=[
                    "Interesting. I'll have to think about this.",
                    "Hmm. This could go either way.",
                    "I see. Time will tell if this was wise.",
                    "Fascinating. I'll be watching how this develops."
                ],
                threat_responses=[
                    "Threats? How... predictable. And ineffective.",
                    "You think you can intimidate me? How amusing.",
                    "Violence is so... crude. Surely we can be more civilized.",
                    "Oh, you're threatening me? How... original."
                ],
                help_responses=[
                    "I can help you... for the right price.",
                    "I have information that might interest you.",
                    "I can offer assistance... with certain conditions.",
                    "I might be able to help... if it serves my interests."
                ],
                trade_responses=[
                    "I have... interesting items. For the right buyer.",
                    "My wares are... unique. And expensive.",
                    "I trade in information as much as goods.",
                    "I have things that others don't... for a price."
                ],
                quest_responses=[
                    "I have a task that requires... subtlety.",
                    "This job needs someone who can think on their feet.",
                    "I need someone clever for this... delicate matter.",
                    "This requires someone who can see the bigger picture."
                ],
                combat_responses=[
                    "I prefer to fight with my mind, not my fists.",
                    "Let's see how clever you really are.",
                    "I have a few tricks up my sleeve.",
                    "This should be... interesting."
                ],
                fear_responses=[
                    "Fear is just another tool to be used.",
                    "I'm not afraid, I'm... calculating.",
                    "Fear can be turned to advantage.",
                    "I see opportunities where others see threats."
                ],
                trust_threshold=90,
                anger_threshold=30,
                generosity_level=3,
                intelligence_level=9,
                bravery_level=5,
                loyalty_level=4,
                curiosity_level=8,
                suspiciousness_level=8,
                emotional_stability=6,
                social_preference=7,
                risk_tolerance=5,
                adaptability=6,
                memory_retention=7,
                influence_susceptibility=9,
                conflict_resolution=6,
                leadership_tendency=5
            ),
            
            NPCPersonality.NAIVE: NPCPersonalityTraits(
                personality_type=NPCPersonality.NAIVE,
                speech_style="innocent and trusting",
                greeting_phrases=[
                    "Hi! You look nice! Are you friendly?",
                    "Hello! I hope you're a good person!",
                    "Hi there! I love meeting new people!",
                    "Hello! You seem nice! Want to be friends?"
                ],
                farewell_phrases=[
                    "Bye! Come back soon! I like you!",
                    "Goodbye! You're my new best friend!",
                    "See you later! Don't forget about me!",
                    "Farewell! I hope we can play together again!"
                ],
                positive_reactions=[
                    "Wow! You're so nice! I love you!",
                    "That's amazing! You're the best person ever!",
                    "Really? You're so kind! I want to be your friend forever!",
                    "You're wonderful! I knew you were a good person!"
                ],
                negative_reactions=[
                    "Oh... I thought you were nice. I'm sad now.",
                    "That's not very nice. But I still like you!",
                    "I'm disappointed, but I'm sure you didn't mean it.",
                    "That hurt my feelings, but I forgive you!"
                ],
                neutral_reactions=[
                    "Okay! That's fine with me!",
                    "I don't understand, but I trust you!",
                    "Whatever you say! You seem smart!",
                    "I'm not sure, but I believe you!"
                ],
                threat_responses=[
                    "Are you joking? You seem so nice!",
                    "You're not really going to hurt me, are you?",
                    "I don't understand why you're being mean.",
                    "Please don't hurt me! I thought we were friends!"
                ],
                help_responses=[
                    "I'll help you! I love helping people!",
                    "Of course I'll help! That's what friends do!",
                    "I want to help! What do you need?",
                    "I'll do anything for you! You're my friend!"
                ],
                trade_responses=[
                    "I have some things! Do you want to trade?",
                    "I love trading! It's so much fun!",
                    "I have nice things! Want to see them?",
                    "I'll trade anything with you! You seem honest!"
                ],
                quest_responses=[
                    "I have a problem! Can you help me?",
                    "There's something I need help with! Will you help?",
                    "I have a quest! It's probably easy!",
                    "I need someone nice to help me! Are you nice?"
                ],
                combat_responses=[
                    "I'll help you fight! I'm not scared!",
                    "Let's be brave together! I believe in you!",
                    "I'll stand by you! We're friends!",
                    "I'm not afraid! Friends stick together!"
                ],
                fear_responses=[
                    "I'm a little scared, but I trust you!",
                    "I'm frightened, but I know you'll protect me!",
                    "I'm scared, but I believe in you!",
                    "I'm afraid, but I won't leave you alone!"
                ],
                trust_threshold=10,
                anger_threshold=90,
                generosity_level=9,
                intelligence_level=3,
                bravery_level=4,
                loyalty_level=9,
                curiosity_level=8,
                suspiciousness_level=1,
                emotional_stability=5,
                social_preference=6,
                risk_tolerance=4,
                adaptability=5,
                memory_retention=7,
                influence_susceptibility=8,
                conflict_resolution=6,
                leadership_tendency=4
            ),
            
            NPCPersonality.PARANOID: NPCPersonalityTraits(
                personality_type=NPCPersonality.PARANOID,
                speech_style="suspicious and guarded",
                greeting_phrases=[
                    "Who are you? What do you want?",
                    "I don't trust strangers. State your business.",
                    "You're not one of them, are you?",
                    "I'm watching you. Don't try anything."
                ],
                farewell_phrases=[
                    "Good. Now leave. And don't come back.",
                    "Go. And don't tell anyone you saw me.",
                    "Farewell. I'll be watching for you.",
                    "Leave. I don't want any trouble."
                ],
                positive_reactions=[
                    "Hmm. Maybe you're not as bad as I thought.",
                    "That's... unexpected. But I'm still watching you.",
                    "Interesting. You might be trustworthy. Maybe.",
                    "Alright. You've earned a little trust. A little."
                ],
                negative_reactions=[
                    "I knew it! You're one of them!",
                    "I should have known better than to trust you!",
                    "This proves everything I suspected!",
                    "I knew you were up to no good!"
                ],
                neutral_reactions=[
                    "I don't know what to think about this.",
                    "I'm not sure if I can trust you or not.",
                    "This could be good or bad. I'll be watching.",
                    "I'll reserve judgment for now."
                ],
                threat_responses=[
                    "I knew you were dangerous! I'm ready for you!",
                    "You think you can threaten me? I'm prepared!",
                    "I've been expecting this! Come and get me!",
                    "I won't go down without a fight!"
                ],
                help_responses=[
                    "I can help you... but I don't trust you.",
                    "I'll help, but I'm watching you carefully.",
                    "I can assist you... if you prove yourself.",
                    "I might help... but don't try anything funny."
                ],
                trade_responses=[
                    "I have goods... but I don't trust you with them.",
                    "I can trade... but I'm watching for tricks.",
                    "I have items... but I'm suspicious of your motives.",
                    "I'll trade... but don't try to cheat me."
                ],
                quest_responses=[
                    "I have a problem... but I don't know if I can trust you.",
                    "There's something I need help with... but I'm suspicious.",
                    "I have a task... but I'm not sure about you.",
                    "I need help... but I don't know if you're safe."
                ],
                combat_responses=[
                    "I'll fight with you... but I'm watching your back.",
                    "I'll help in battle... but don't betray me.",
                    "I'll stand with you... but I'm still suspicious.",
                    "I'll fight... but I'm keeping my guard up."
                ],
                fear_responses=[
                    "I'm not scared! I'm just being cautious!",
                    "I'm not afraid! I'm just prepared!",
                    "I'm not frightened! I'm just alert!",
                    "I'm not scared! I'm just... careful!"
                ],
                trust_threshold=95,
                anger_threshold=25,
                generosity_level=2,
                intelligence_level=7,
                bravery_level=6,
                loyalty_level=5,
                curiosity_level=4,
                suspiciousness_level=10,
                emotional_stability=4,
                social_preference=3,
                risk_tolerance=1,
                adaptability=2,
                memory_retention=3,
                influence_susceptibility=10,
                conflict_resolution=9,
                leadership_tendency=3
            ),
            
            NPCPersonality.TRUSTING: NPCPersonalityTraits(
                personality_type=NPCPersonality.TRUSTING,
                speech_style="open and accepting",
                greeting_phrases=[
                    "Hello! I'm so glad to meet you!",
                    "Welcome! I trust you're a good person!",
                    "Hi there! I believe everyone is basically good!",
                    "Greetings! I'm sure we'll get along wonderfully!"
                ],
                farewell_phrases=[
                    "Goodbye! I trust we'll meet again!",
                    "Farewell! I believe in our friendship!",
                    "See you later! I know you'll do the right thing!",
                    "Until next time! I have faith in you!"
                ],
                positive_reactions=[
                    "I knew you were a good person! I trust my instincts!",
                    "Wonderful! I always believe in the best in people!",
                    "Excellent! I knew I could trust you!",
                    "Perfect! I believe everyone deserves a chance!"
                ],
                negative_reactions=[
                    "I'm sure you didn't mean to hurt anyone.",
                    "I believe you have good reasons for what you did.",
                    "I trust that you'll make better choices next time.",
                    "I still believe in you, even if you made a mistake."
                ],
                neutral_reactions=[
                    "I'm sure everything will work out for the best.",
                    "I trust that you know what you're doing.",
                    "I believe you have good intentions.",
                    "I'm confident that you'll do the right thing."
                ],
                threat_responses=[
                    "I'm sure you don't really mean to hurt me.",
                    "I believe we can work this out peacefully.",
                    "I trust that you're just having a bad day.",
                    "I know you're a good person deep down."
                ],
                help_responses=[
                    "Of course I'll help! I trust you need it!",
                    "I'd be happy to help! I believe in helping others!",
                    "I'll help you! I trust that you're honest!",
                    "I want to help! I believe everyone deserves assistance!"
                ],
                trade_responses=[
                    "I'll trade with you! I trust you'll be fair!",
                    "I have goods to trade! I believe in honest dealing!",
                    "I'd love to trade! I trust you're honest!",
                    "I'll trade anything! I believe in you!"
                ],
                quest_responses=[
                    "I have a quest! I trust you'll help me!",
                    "I need help with something! I believe you can do it!",
                    "I have a task! I trust you're capable!",
                    "I need assistance! I believe in your abilities!"
                ],
                combat_responses=[
                    "I'll fight with you! I trust we'll win!",
                    "I'll stand by you! I believe in our friendship!",
                    "I'll help in battle! I trust you'll protect me!",
                    "I'll fight alongside you! I believe in you!"
                ],
                fear_responses=[
                    "I'm a little scared, but I trust you'll keep me safe!",
                    "I'm frightened, but I believe everything will be okay!",
                    "I'm afraid, but I trust you'll protect me!",
                    "I'm scared, but I have faith in you!"
                ],
                trust_threshold=5,
                anger_threshold=85,
                generosity_level=8,
                intelligence_level=4,
                bravery_level=5,
                loyalty_level=9,
                curiosity_level=7,
                suspiciousness_level=1,
                emotional_stability=6,
                social_preference=7,
                risk_tolerance=6,
                adaptability=6,
                memory_retention=7,
                influence_susceptibility=8,
                conflict_resolution=5,
                leadership_tendency=4
            ),
            
            NPCPersonality.AMBITIOUS: NPCPersonalityTraits(
                personality_type=NPCPersonality.AMBITIOUS,
                speech_style="driven and focused",
                greeting_phrases=[
                    "Greetings. I hope you can be useful to my goals.",
                    "Hello. I'm always looking for valuable connections.",
                    "Welcome. I trust you understand the value of ambition.",
                    "Greetings. I'm sure we can help each other advance."
                ],
                farewell_phrases=[
                    "Farewell. I expect great things from our partnership.",
                    "Goodbye. Don't forget our mutual interests.",
                    "Until next time. I'm counting on your success.",
                    "Farewell. I look forward to our next collaboration."
                ],
                positive_reactions=[
                    "Excellent! This advances our mutual interests.",
                    "Perfect! This will help us both achieve our goals.",
                    "Outstanding! You've proven your value to our cause.",
                    "Brilliant! This is exactly what I was looking for."
                ],
                negative_reactions=[
                    "Disappointing. This doesn't serve our interests.",
                    "Unfortunate. I expected better from someone of your potential.",
                    "Regrettable. This won't help us achieve our goals.",
                    "Concerning. This could set back our plans."
                ],
                neutral_reactions=[
                    "Interesting. I'll have to consider the implications.",
                    "Hmm. This could go either way for our interests.",
                    "I see. Time will tell if this serves our purposes.",
                    "Noted. I'll evaluate how this affects our goals."
                ],
                threat_responses=[
                    "Threats? How... counterproductive to our mutual interests.",
                    "Violence is so... inefficient. Surely we can be more strategic.",
                    "You think intimidation works on someone with ambition?",
                    "I prefer to achieve my goals through more... elegant means."
                ],
                help_responses=[
                    "I can help you... if it serves our mutual interests.",
                    "I'll assist you... if it advances our goals.",
                    "I can offer support... if it benefits our cause.",
                    "I'll help... if it contributes to our success."
                ],
                trade_responses=[
                    "I have resources that could advance your interests.",
                    "My goods are investments in your future success.",
                    "I trade in opportunities and connections.",
                    "My wares are tools for achieving your ambitions."
                ],
                quest_responses=[
                    "I have a task that could advance your career.",
                    "This quest will test your potential and ambition.",
                    "I need someone driven for this important mission.",
                    "This task requires someone who thinks big."
                ],
                combat_responses=[
                    "I'll fight for our shared interests!",
                    "Let's show them what ambitious people can do!",
                    "I'll battle alongside you for our goals!",
                    "Together, we'll prove our worth!"
                ],
                fear_responses=[
                    "Fear is just another obstacle to overcome.",
                    "I'm not afraid, I'm focused on our goals.",
                    "Fear won't stop us from achieving our ambitions.",
                    "I see challenges, not threats."
                ],
                trust_threshold=60,
                anger_threshold=40,
                generosity_level=4,
                intelligence_level=8,
                bravery_level=7,
                loyalty_level=6,
                curiosity_level=6,
                suspiciousness_level=5,
                emotional_stability=7,
                social_preference=8,
                risk_tolerance=7,
                adaptability=7,
                memory_retention=8,
                influence_susceptibility=6,
                conflict_resolution=6,
                leadership_tendency=5
            ),
            
            NPCPersonality.CONTENT: NPCPersonalityTraits(
                personality_type=NPCPersonality.CONTENT,
                speech_style="calm and satisfied",
                greeting_phrases=[
                    "Hello there. I'm quite comfortable here.",
                    "Greetings. I hope you find peace in your journey.",
                    "Welcome. I'm content with my simple life.",
                    "Hello. I find joy in the little things."
                ],
                farewell_phrases=[
                    "Farewell. May you find contentment in your travels.",
                    "Goodbye. I'll be here if you need a peaceful moment.",
                    "Until next time. I'll continue enjoying my simple life.",
                    "Farewell. I hope you find what makes you happy."
                ],
                positive_reactions=[
                    "That's wonderful. I'm glad you're finding joy in life.",
                    "Excellent. It's good to see people being kind.",
                    "That's nice. I appreciate simple acts of goodness.",
                    "Lovely. The world needs more of that."
                ],
                negative_reactions=[
                    "That's unfortunate. I hope you find peace.",
                    "I'm sorry to hear that. Everyone deserves happiness.",
                    "That's sad. I hope things get better for you.",
                    "I understand. Life has its ups and downs."
                ],
                neutral_reactions=[
                    "That's interesting. I'll think about it.",
                    "I see. Everyone has their own path.",
                    "Hmm. I'm content to let things unfold naturally.",
                    "Alright. I'm happy with my simple life."
                ],
                threat_responses=[
                    "I prefer peace to violence. Can't we talk?",
                    "I'm content with my life. I don't want trouble.",
                    "Violence is so unnecessary. Surely we can find another way.",
                    "I'm happy with what I have. I don't need conflict."
                ],
                help_responses=[
                    "I can help you. I find joy in helping others.",
                    "I'll assist you. It's good to be useful.",
                    "I can offer support. I'm content to help.",
                    "I'll help. I have what I need, so I can share."
                ],
                trade_responses=[
                    "I have simple goods. They serve me well.",
                    "I trade in basic necessities. They're all I need.",
                    "I have modest wares. They bring me contentment.",
                    "I trade what I have. I don't need much."
                ],
                quest_responses=[
                    "I have a simple task. It might interest you.",
                    "There's something I need help with. It's not urgent.",
                    "I have a small quest. Take your time with it.",
                    "I need assistance with something. No rush."
                ],
                combat_responses=[
                    "I'll help if I must. I prefer peace, but I'll fight for what's right.",
                    "I'll stand with you. Sometimes we must fight for what we believe in.",
                    "I'll assist in battle. I'm content to help when needed.",
                    "I'll fight alongside you. I find strength in protecting others."
                ],
                fear_responses=[
                    "I'm a little scared, but I'm content to face my fears.",
                    "I'm frightened, but I find peace in accepting what comes.",
                    "I'm afraid, but I'm happy to have friends to face it with.",
                    "I'm scared, but I'm content knowing I'm not alone."
                ],
                trust_threshold=50,
                anger_threshold=50,
                generosity_level=7,
                intelligence_level=6,
                bravery_level=5,
                loyalty_level=8,
                curiosity_level=4,
                suspiciousness_level=3,
                emotional_stability=8,
                social_preference=9,
                risk_tolerance=6,
                adaptability=7,
                memory_retention=7,
                influence_susceptibility=5,
                conflict_resolution=6,
                leadership_tendency=5
            )
        }
    
    def create_npc(self, npc_data: Dict[str, Any]) -> NPC:
        """Create an NPC with detailed personality"""
        personality_type = NPCPersonality(npc_data.get("personality", "neutral"))
        personality_traits = self.personality_traits.get(personality_type)
        
        if not personality_traits:
            # Create default traits if not found
            personality_traits = NPCPersonalityTraits(
                personality_type=personality_type,
                speech_style="neutral",
                greeting_phrases=["Hello."],
                farewell_phrases=["Goodbye."],
                positive_reactions=["Good."],
                negative_reactions=["Bad."],
                neutral_reactions=["Okay."],
                threat_responses=["No."],
                help_responses=["Maybe."],
                trade_responses=["Trade."],
                quest_responses=["Quest."],
                combat_responses=["Fight."],
                fear_responses=["Scared."],
                trust_threshold=50,
                anger_threshold=50,
                generosity_level=5,
                intelligence_level=5,
                bravery_level=5,
                loyalty_level=5,
                curiosity_level=5,
                suspiciousness_level=5,
                emotional_stability=5,
                social_preference=5,
                risk_tolerance=5,
                adaptability=5,
                memory_retention=5,
                influence_susceptibility=5,
                conflict_resolution=5,
                leadership_tendency=5
            )
        
        npc = NPC(
            id=npc_data["id"],
            name=npc_data["name"],
            role=NPCRole(npc_data.get("role", "villager")),
            personality=personality_type,
            personality_traits=personality_traits,
            description=npc_data.get("description", ""),
            location=npc_data.get("location", "unknown"),
            moral_alignment=MoralAlignment(npc_data.get("moral_alignment", "neutral")),
            relationship_level=self._set_initial_relationship(personality_type, npc_data.get("moral_alignment", "neutral")),
            trust_level=50,
            fear_level=0,
            respect_level=50,
            quests_given=npc_data.get("quests_given", []),
            items_offered=npc_data.get("items_offered", []),
            combat_assistance=npc_data.get("combat_assistance", False),
            boss_fight_help=npc_data.get("boss_fight_help", False),
            dialogue_options=npc_data.get("dialogue_options", {}),
            special_abilities=npc_data.get("special_abilities", []),
            background_story=npc_data.get("background_story", ""),
            current_mood="neutral",
            secrets_known=npc_data.get("secrets_known", []),
            relationships_with_others=npc_data.get("relationships_with_others", {})
        )
        
        self.npcs[npc.id] = npc
        return npc
    
    def _set_initial_relationship(self, personality: NPCPersonality, moral_alignment: str) -> int:
        """Set initial relationship based on personality and moral alignment"""
        base_relationship = 0
        
        # Personality-based adjustments
        if personality == NPCPersonality.FRIENDLY:
            base_relationship += 20
        elif personality == NPCPersonality.GRUMPY:
            base_relationship -= 10
        elif personality == NPCPersonality.MYSTERIOUS:
            base_relationship += 5
        elif personality == NPCPersonality.WISE:
            base_relationship += 15
        elif personality == NPCPersonality.GREEDY:
            base_relationship -= 5
        elif personality == NPCPersonality.HONORABLE:
            base_relationship += 10
        elif personality == NPCPersonality.COWARDLY:
            base_relationship -= 10
        elif personality == NPCPersonality.BRAVE:
            base_relationship += 10
        elif personality == NPCPersonality.CUNNING:
            base_relationship += 5
        elif personality == NPCPersonality.NAIVE:
            base_relationship += 10
        elif personality == NPCPersonality.PARANOID:
            base_relationship -= 10
        elif personality == NPCPersonality.TRUSTING:
            base_relationship += 15
        elif personality == NPCPersonality.AMBITIOUS:
            base_relationship += 10
        elif personality == NPCPersonality.CONTENT:
            base_relationship += 5
        
        # Moral alignment adjustments
        if moral_alignment == "good":
            base_relationship += 10
        elif moral_alignment == "bad":
            base_relationship -= 10
        
        return max(-100, min(100, base_relationship))
    
    def interact_with_npc(self, npc_id: str, action: str, player_moral: PlayerMoral) -> Dict[str, Any]:
        """Interact with an NPC using detailed personality system"""
        if npc_id not in self.npcs:
            return {"success": False, "error": "NPC not found"}
        
        npc = self.npcs[npc_id]
        traits = npc.personality_traits
        
        # Determine action morality
        action_morality = self._get_action_morality(action)
        
        # Calculate relationship change based on personality
        relationship_change = self._calculate_relationship_change(action, npc, action_morality)
        
        # Update NPC relationship
        old_relationship = npc.relationship_level
        npc.relationship_level = max(-100, min(100, npc.relationship_level + relationship_change))
        
        # Generate NPC response based on personality
        npc_response = self._generate_npc_response(npc, action, action_morality, relationship_change)
        
        # Check for special consequences
        consequences = self._check_special_consequences(npc, old_relationship, npc.relationship_level)
        
        # Update player moral
        self._update_player_moral(player_moral, action_morality)
        
        # Update NPC mood based on interaction
        self._update_npc_mood(npc, relationship_change)
        
        return {
            "success": True,
            "npc_name": npc.name,
            "npc_personality": npc.personality.value,
            "action": action,
            "relationship_change": relationship_change,
            "new_relationship_level": npc.relationship_level,
            "npc_response": npc_response,
            "consequences": consequences,
            "player_moral": self._get_player_moral_summary(player_moral)
        }
    
    def _get_action_morality(self, action: str) -> str:
        """Determine the moral alignment of an action"""
        good_actions = ["help", "heal", "donate", "protect", "save", "rescue", "comfort"]
        bad_actions = ["attack", "steal", "threaten", "kill", "betray", "torture", "deceive"]
        neutral_actions = ["talk", "trade", "explore", "investigate", "observe"]
        
        action_lower = action.lower()
        
        if any(good in action_lower for good in good_actions):
            return "good"
        elif any(bad in action_lower for bad in bad_actions):
            return "bad"
        else:
            return "neutral"
    
    def _calculate_relationship_change(self, action: str, npc: NPC, action_morality: str) -> int:
        """Calculate relationship change based on NPC personality"""
        traits = npc.personality_traits
        base_change = 0
        
        # Base change by action morality
        if action_morality == "good":
            base_change += 5
        elif action_morality == "bad":
            base_change -= 10
        else:
            base_change += 0
        
        # Personality-based modifiers
        if npc.personality == NPCPersonality.FRIENDLY:
            if action_morality == "good":
                base_change += 3
            elif action_morality == "bad":
                base_change -= 5
        elif npc.personality == NPCPersonality.GRUMPY:
            if action_morality == "good":
                base_change += 1
            elif action_morality == "bad":
                base_change -= 3
        elif npc.personality == NPCPersonality.GREEDY:
            if "trade" in action.lower() or "money" in action.lower():
                base_change += 5
            elif "donate" in action.lower():
                base_change += 8
        elif npc.personality == NPCPersonality.HONORABLE:
            if action_morality == "good":
                base_change += 5
            elif action_morality == "bad":
                base_change -= 8
        elif npc.personality == NPCPersonality.MYSTERIOUS:
            # Mysterious NPCs are unpredictable
            base_change += random.randint(-2, 3)
        elif npc.personality == NPCPersonality.COWARDLY:
            if action_morality == "good":
                base_change += 1
            elif action_morality == "bad":
                base_change -= 5
        elif npc.personality == NPCPersonality.BRAVE:
            if action_morality == "good":
                base_change += 3
            elif action_morality == "bad":
                base_change -= 3
        elif npc.personality == NPCPersonality.CUNNING:
            if action_morality == "good":
                base_change += 2
            elif action_morality == "bad":
                base_change -= 2
        elif npc.personality == NPCPersonality.NAIVE:
            if action_morality == "good":
                base_change += 2
            elif action_morality == "bad":
                base_change -= 2
        elif npc.personality == NPCPersonality.PARANOID:
            if action_morality == "good":
                base_change += 1
            elif action_morality == "bad":
                base_change -= 3
        elif npc.personality == NPCPersonality.TRUSTING:
            if action_morality == "good":
                base_change += 3
            elif action_morality == "bad":
                base_change -= 3
        elif npc.personality == NPCPersonality.AMBITIOUS:
            if action_morality == "good":
                base_change += 2
            elif action_morality == "bad":
                base_change -= 2
        elif npc.personality == NPCPersonality.CONTENT:
            if action_morality == "good":
                base_change += 1
            elif action_morality == "bad":
                base_change -= 1
        
        # Add some randomness
        base_change += random.randint(-1, 1)
        
        return base_change
    
    def _generate_npc_response(self, npc: NPC, action: str, action_morality: str, relationship_change: int) -> str:
        """Generate NPC response based on personality and action"""
        traits = npc.personality_traits
        
        if relationship_change > 5:
            return random.choice(traits.positive_reactions)
        elif relationship_change < -5:
            return random.choice(traits.negative_reactions)
        else:
            return random.choice(traits.neutral_reactions)
    
    def _update_npc_mood(self, npc: NPC, relationship_change: int):
        """Update NPC mood based on interaction"""
        if relationship_change > 10:
            npc.current_mood = "happy"
        elif relationship_change > 5:
            npc.current_mood = "pleased"
        elif relationship_change < -10:
            npc.current_mood = "angry"
        elif relationship_change < -5:
            npc.current_mood = "disappointed"
        else:
            npc.current_mood = "neutral"
    
    def get_npc_mood_response(self, npc: NPC, situation: str) -> str:
        """Get NPC response based on current mood and personality"""
        traits = npc.personality_traits
        
        # Base response based on situation
        if situation == "greeting":
            responses = traits.greeting_phrases
        elif situation == "farewell":
            responses = traits.farewell_phrases
        elif situation == "positive":
            responses = traits.positive_reactions
        elif situation == "negative":
            responses = traits.negative_reactions
        elif situation == "neutral":
            responses = traits.neutral_reactions
        elif situation == "threat":
            responses = traits.threat_responses
        elif situation == "help":
            responses = traits.help_responses
        elif situation == "trade":
            responses = traits.trade_responses
        elif situation == "quest":
            responses = traits.quest_responses
        elif situation == "combat":
            responses = traits.combat_responses
        elif situation == "fear":
            responses = traits.fear_responses
        else:
            responses = traits.neutral_reactions
        
        # Modify response based on mood
        base_response = random.choice(responses)
        
        # Add mood-based modifiers
        if npc.current_mood == "happy":
            if npc.personality == NPCPersonality.GRUMPY:
                base_response = base_response.replace("Hmph", "Hmph... fine")
            elif npc.personality == NPCPersonality.PARANOID:
                base_response = base_response.replace("I'm watching you", "I'm... I'm watching you, but maybe not as closely")
        elif npc.current_mood == "angry":
            if npc.personality == NPCPersonality.FRIENDLY:
                base_response = base_response.replace("Hello", "Hello... *sigh*")
            elif npc.personality == NPCPersonality.NAIVE:
                base_response = base_response.replace("Hi!", "Hi... *sniffle*")
        
        return base_response
    
    def get_personality_based_dialogue(self, npc: NPC, context: str, player_moral: PlayerMoral) -> str:
        """Generate personality-specific dialogue based on context and player moral"""
        traits = npc.personality_traits
        
        # Personality-specific dialogue patterns
        if npc.personality == NPCPersonality.CUNNING:
            if context == "quest_offer":
                if player_moral.karma_points > 50:
                    return "I have a... profitable opportunity that might interest someone of your... talents."
                else:
                    return "I have a task that requires someone who can think on their feet. Are you... capable?"
        
        elif npc.personality == NPCPersonality.PARANOID:
            if context == "quest_offer":
                return "I have a problem... but I don't know if I can trust you with it."
            elif context == "trade":
                return "I have goods... but I'm watching for tricks."
        
        elif npc.personality == NPCPersonality.NAIVE:
            if context == "quest_offer":
                return "I have a problem! Can you help me? It's probably easy!"
            elif context == "trade":
                return "I have nice things! Want to see them? I'll trade anything with you!"
        
        elif npc.personality == NPCPersonality.AMBITIOUS:
            if context == "quest_offer":
                return "I have a task that could advance your career. Are you interested in success?"
            elif context == "trade":
                return "I have resources that could advance your interests. Quality comes at a price."
        
        elif npc.personality == NPCPersonality.CONTENT:
            if context == "quest_offer":
                return "I have a simple task. It might interest you. No rush."
            elif context == "trade":
                return "I have simple goods. They serve me well. Take what you need."
        
        # Default response
        return self.get_npc_mood_response(npc, context)
    
    def calculate_personality_compatibility(self, npc: NPC, player_moral: PlayerMoral) -> float:
        """Calculate how compatible the NPC is with the player's moral alignment"""
        compatibility = 0.5  # Base compatibility
        
        # Personality-based compatibility
        if npc.personality == NPCPersonality.HONORABLE:
            if player_moral.overall_alignment in [MoralAlignment.GOOD, MoralAlignment.VERY_GOOD]:
                compatibility += 0.3
            elif player_moral.overall_alignment in [MoralAlignment.BAD, MoralAlignment.VERY_BAD]:
                compatibility -= 0.3
        elif npc.personality == NPCPersonality.GREEDY:
            if player_moral.karma_points < -20:  # Player has done some bad things
                compatibility += 0.2
            else:
                compatibility -= 0.1
        elif npc.personality == NPCPersonality.TRUSTING:
            if player_moral.overall_alignment in [MoralAlignment.GOOD, MoralAlignment.VERY_GOOD]:
                compatibility += 0.4
            else:
                compatibility -= 0.2
        elif npc.personality == NPCPersonality.PARANOID:
            if player_moral.overall_alignment in [MoralAlignment.BAD, MoralAlignment.VERY_BAD]:
                compatibility += 0.2  # Paranoid NPCs might relate to "bad" players
            else:
                compatibility -= 0.1
        elif npc.personality == NPCPersonality.AMBITIOUS:
            if player_moral.karma_points > 30:  # Player has done good things
                compatibility += 0.2
            else:
                compatibility -= 0.1
        
        return max(0.0, min(1.0, compatibility))
    
    def get_emotional_memory_response(self, npc: NPC, player_action_history: List[str]) -> str:
        """Generate response based on NPC's memory of past interactions"""
        traits = npc.personality_traits
        
        # Check recent actions for patterns
        recent_good_actions = sum(1 for action in player_action_history[-5:] if self._get_action_morality(action) == "good")
        recent_bad_actions = sum(1 for action in player_action_history[-5:] if self._get_action_morality(action) == "bad")
        
        if traits.memory_retention > 7:  # Good memory
            if recent_good_actions > recent_bad_actions:
                if npc.personality == NPCPersonality.FRIENDLY:
                    return "I remember how kind you've been lately. You're a true friend!"
                elif npc.personality == NPCPersonality.HONORABLE:
                    return "Your recent actions have shown great honor. I respect that."
                elif npc.personality == NPCPersonality.TRUSTING:
                    return "I've seen how good you are. I trust you completely!"
            elif recent_bad_actions > recent_good_actions:
                if npc.personality == NPCPersonality.PARANOID:
                    return "I've been watching your recent behavior. I knew I couldn't trust you!"
                elif npc.personality == NPCPersonality.HONORABLE:
                    return "Your recent actions have disappointed me. Honor is not a game."
                elif npc.personality == NPCPersonality.NAIVE:
                    return "I thought you were nice, but lately... I'm confused."
        
        return ""  # No special memory response
    
    def get_personality_development(self, npc: NPC, interaction_count: int) -> Dict[str, Any]:
        """Simulate personality development based on interactions"""
        traits = npc.personality_traits
        development = {}
        
        # Personality can evolve based on interactions
        if interaction_count > 10:
            if npc.personality == NPCPersonality.PARANOID:
                if npc.relationship_level > 50:
                    development["trust_increase"] = True
                    development["suspiciousness_decrease"] = True
            elif npc.personality == NPCPersonality.NAIVE:
                if npc.relationship_level < -30:
                    development["trust_decrease"] = True
                    development["suspiciousness_increase"] = True
            elif npc.personality == NPCPersonality.COWARDLY:
                if npc.relationship_level > 70:
                    development["bravery_increase"] = True
                    development["fear_decrease"] = True
        
        return development
    
    def get_social_dynamics(self, npc: NPC, other_npcs: List[NPC]) -> Dict[str, Any]:
        """Calculate how this NPC interacts with other NPCs"""
        dynamics = {
            "allies": [],
            "rivals": [],
            "neutral": []
        }
        
        for other_npc in other_npcs:
            if other_npc.id == npc.id:
                continue
            
            compatibility = self._calculate_npc_compatibility(npc, other_npc)
            
            if compatibility > 0.7:
                dynamics["allies"].append(other_npc.name)
            elif compatibility < 0.3:
                dynamics["rivals"].append(other_npc.name)
            else:
                dynamics["neutral"].append(other_npc.name)
        
        return dynamics
    
    def _calculate_npc_compatibility(self, npc1: NPC, npc2: NPC) -> float:
        """Calculate compatibility between two NPCs"""
        compatibility = 0.5
        
        # Personality compatibility
        if npc1.personality == npc2.personality:
            compatibility += 0.2
        elif (npc1.personality == NPCPersonality.FRIENDLY and npc2.personality == NPCPersonality.TRUSTING):
            compatibility += 0.3
        elif (npc1.personality == NPCPersonality.PARANOID and npc2.personality == NPCPersonality.CUNNING):
            compatibility -= 0.3
        elif (npc1.personality == NPCPersonality.NAIVE and npc2.personality == NPCPersonality.CUNNING):
            compatibility -= 0.4
        
        # Moral alignment compatibility
        if npc1.moral_alignment == npc2.moral_alignment:
            compatibility += 0.2
        elif (npc1.moral_alignment in [MoralAlignment.GOOD, MoralAlignment.VERY_GOOD] and 
              npc2.moral_alignment in [MoralAlignment.BAD, MoralAlignment.VERY_BAD]):
            compatibility -= 0.3
        
        return max(0.0, min(1.0, compatibility))
    
    def get_npc_help_in_boss_fight(self, npc_id: str, player_moral: PlayerMoral) -> Dict[str, Any]:
        """Determine if NPC will help in boss fight based on personality and relationship"""
        if npc_id not in self.npcs:
            return {"will_help": False, "reason": "NPC not found"}
        
        npc = self.npcs[npc_id]
        traits = npc.personality_traits
        
        # Base chance based on relationship
        base_chance = (npc.relationship_level + 100) / 200  # 0 to 1
        
        # Personality modifiers
        if npc.personality == NPCPersonality.GRUMPY:
            # Grumpy NPCs might help bad players more
            if player_moral.overall_alignment in [MoralAlignment.BAD, MoralAlignment.VERY_BAD]:
                base_chance += 0.2
        elif npc.personality == NPCPersonality.HONORABLE:
            # Honorable NPCs help good players
            if player_moral.overall_alignment in [MoralAlignment.GOOD, MoralAlignment.VERY_GOOD]:
                base_chance += 0.3
        elif npc.personality == NPCPersonality.GREEDY:
            # Greedy NPCs need payment
            base_chance -= 0.2
        elif npc.personality == NPCPersonality.BRAVE:
            # Brave NPCs are more likely to help
            base_chance += 0.2
        elif npc.personality == NPCPersonality.COWARDLY:
            # Cowardly NPCs are less likely to help
            base_chance -= 0.3
        elif npc.personality == NPCPersonality.CUNNING:
            # Cunning NPCs might help if they perceive the player as trustworthy
            if player_moral.overall_alignment in [MoralAlignment.GOOD, MoralAlignment.VERY_GOOD] and player_moral.karma_points > 50:
                base_chance += 0.1
            elif player_moral.overall_alignment in [MoralAlignment.BAD, MoralAlignment.VERY_BAD] and player_moral.karma_points < -50:
                base_chance -= 0.1
        elif npc.personality == NPCPersonality.NAIVE:
            # Naive NPCs might help if they perceive the player as friendly
            if player_moral.overall_alignment in [MoralAlignment.GOOD, MoralAlignment.VERY_GOOD] and player_moral.karma_points > 30:
                base_chance += 0.1
            elif player_moral.overall_alignment in [MoralAlignment.BAD, MoralAlignment.VERY_BAD] and player_moral.karma_points < -30:
                base_chance -= 0.1
        elif npc.personality == NPCPersonality.PARANOID:
            # Paranoid NPCs might help if they perceive the player as trustworthy
            if player_moral.overall_alignment in [MoralAlignment.GOOD, MoralAlignment.VERY_GOOD] and player_moral.karma_points > 70:
                base_chance += 0.1
            elif player_moral.overall_alignment in [MoralAlignment.BAD, MoralAlignment.VERY_BAD] and player_moral.karma_points < -70:
                base_chance -= 0.1
        elif npc.personality == NPCPersonality.TRUSTING:
            # Trusting NPCs might help if they perceive the player as trustworthy
            if player_moral.overall_alignment in [MoralAlignment.GOOD, MoralAlignment.VERY_GOOD] and player_moral.karma_points > 40:
                base_chance += 0.1
            elif player_moral.overall_alignment in [MoralAlignment.BAD, MoralAlignment.VERY_BAD] and player_moral.karma_points < -40:
                base_chance -= 0.1
        elif npc.personality == NPCPersonality.AMBITIOUS:
            # Ambitious NPCs might help if they perceive the player as ambitious
            if player_moral.overall_alignment in [MoralAlignment.GOOD, MoralAlignment.VERY_GOOD] and player_moral.karma_points > 60:
                base_chance += 0.1
            elif player_moral.overall_alignment in [MoralAlignment.BAD, MoralAlignment.VERY_BAD] and player_moral.karma_points < -60:
                base_chance -= 0.1
        elif npc.personality == NPCPersonality.CONTENT:
            # Content NPCs might help if they perceive the player as content
            if player_moral.overall_alignment in [MoralAlignment.GOOD, MoralAlignment.VERY_GOOD] and player_moral.karma_points > 50:
                base_chance += 0.1
            elif player_moral.overall_alignment in [MoralAlignment.BAD, MoralAlignment.VERY_BAD] and player_moral.karma_points < -50:
                base_chance -= 0.1
        
        will_help = random.random() < base_chance
        
        if will_help:
            assistance_power = self._calculate_assistance_power(npc, player_moral)
            return {
                "will_help": True,
                "assistance_power": assistance_power,
                "reason": f"{npc.name} decides to help you in the boss fight!",
                "personality_influence": npc.personality.value
            }
        else:
            return {
                "will_help": False,
                "reason": f"{npc.name} chooses not to help you.",
                "personality_influence": npc.personality.value
            }
    
    def _calculate_assistance_power(self, npc: NPC, player_moral: PlayerMoral) -> Dict[str, Any]:
        """Calculate the power of NPC assistance in boss fight"""
        base_power = 10 + (npc.relationship_level / 10)
        
        # Personality-based assistance
        if npc.personality == NPCPersonality.WISE:
            base_power += 5  # Strategic advice
        elif npc.personality == NPCPersonality.BRAVE:
            base_power += 8  # Direct combat help
        elif npc.personality == NPCPersonality.MYSTERIOUS:
            base_power += 3  # Mystical assistance
        elif npc.personality == NPCPersonality.GREEDY:
            base_power += 2  # Minimal help
        elif npc.personality == NPCPersonality.COWARDLY:
            base_power -= 3  # Hesitant help
        elif npc.personality == NPCPersonality.CUNNING:
            base_power += 4  # Sneaky assistance
        elif npc.personality == NPCPersonality.NAIVE:
            base_power += 2  # Helpful but not very effective
        elif npc.personality == NPCPersonality.PARANOID:
            base_power -= 2  # Paranoid NPCs might sabotage
        elif npc.personality == NPCPersonality.TRUSTING:
            base_power += 6  # Very helpful and reliable
        elif npc.personality == NPCPersonality.AMBITIOUS:
            base_power += 7  # Very ambitious and driven
        elif npc.personality == NPCPersonality.CONTENT:
            base_power += 3  # Content NPCs are generally helpful
        
        return {
            "damage_bonus": int(base_power),
            "defense_bonus": int(base_power * 0.5),
            "healing_bonus": int(base_power * 0.3),
            "special_ability": npc.special_abilities[0] if npc.special_abilities else "none"
        }
    
    def get_npc_items(self, npc_id: str) -> List[str]:
        """Get items NPC is willing to offer based on personality and relationship"""
        if npc_id not in self.npcs:
            return []
        
        npc = self.npcs[npc_id]
        
        if npc.relationship_level < 20:
            return []
        
        # Personality-based item offerings
        if npc.personality == NPCPersonality.GREEDY:
            return npc.items_offered if npc.relationship_level > 50 else []
        elif npc.personality == NPCPersonality.FRIENDLY:
            return npc.items_offered if npc.relationship_level > 30 else []
        elif npc.personality == NPCPersonality.HONORABLE:
            return npc.items_offered if npc.relationship_level > 40 else []
        elif npc.personality == NPCPersonality.COWARDLY:
            return npc.items_offered if npc.relationship_level > 60 else []
        elif npc.personality == NPCPersonality.BRAVE:
            return npc.items_offered if npc.relationship_level > 70 else []
        elif npc.personality == NPCPersonality.CUNNING:
            return npc.items_offered if npc.relationship_level > 80 else []
        elif npc.personality == NPCPersonality.NAIVE:
            return npc.items_offered if npc.relationship_level > 90 else []
        elif npc.personality == NPCPersonality.PARANOID:
            return npc.items_offered if npc.relationship_level > 95 else []
        elif npc.personality == NPCPersonality.TRUSTING:
            return npc.items_offered if npc.relationship_level > 5 else []
        elif npc.personality == NPCPersonality.AMBITIOUS:
            return npc.items_offered if npc.relationship_level > 60 else []
        elif npc.personality == NPCPersonality.CONTENT:
            return npc.items_offered if npc.relationship_level > 50 else []
        else:
            return npc.items_offered if npc.relationship_level > 60 else []
    
    def _check_special_consequences(self, npc: NPC, old_relationship: int, new_relationship: int) -> Dict[str, Any]:
        """Check for special consequences based on relationship change"""
        consequences = {}
        
        # Check if relationship improved significantly
        if new_relationship - old_relationship > 15:
            consequences["quest_offered"] = True
            consequences["item_offered"] = True
        
        # Check if relationship deteriorated significantly
        if old_relationship - new_relationship > 15:
            consequences["combat_triggered"] = True
        
        # Check for trust threshold
        if new_relationship > npc.personality_traits.trust_threshold:
            consequences["trust_gained"] = True
            if npc.secrets_known:
                consequences["secret_revealed"] = npc.secrets_known[0]
        
        return consequences
    
    def _update_player_moral(self, player_moral: PlayerMoral, action_morality: str):
        """Update player moral alignment based on actions"""
        if action_morality == "good":
            player_moral.good_actions += 1
            player_moral.karma_points += 5
        elif action_morality == "bad":
            player_moral.bad_actions += 1
            player_moral.karma_points -= 5
        else:
            player_moral.neutral_actions += 1
        
        # Calculate overall alignment
        total_actions = player_moral.good_actions + player_moral.bad_actions + player_moral.neutral_actions
        if total_actions > 0:
            good_ratio = player_moral.good_actions / total_actions
            bad_ratio = player_moral.bad_actions / total_actions
            
            if good_ratio > 0.6:
                player_moral.overall_alignment = MoralAlignment.VERY_GOOD
            elif good_ratio > 0.4:
                player_moral.overall_alignment = MoralAlignment.GOOD
            elif bad_ratio > 0.6:
                player_moral.overall_alignment = MoralAlignment.VERY_BAD
            elif bad_ratio > 0.4:
                player_moral.overall_alignment = MoralAlignment.BAD
            else:
                player_moral.overall_alignment = MoralAlignment.NEUTRAL
    
    def _get_player_moral_summary(self, player_moral: PlayerMoral) -> Dict[str, Any]:
        """Get summary of player's moral status"""
        return {
            "overall_alignment": player_moral.overall_alignment.value,
            "karma_points": player_moral.karma_points,
            "good_actions": player_moral.good_actions,
            "bad_actions": player_moral.bad_actions,
            "neutral_actions": player_moral.neutral_actions,
            "reputation": player_moral.reputation
        }
    
    def get_all_npc_relationships(self, character_id: str) -> Dict[str, Any]:
        """Get all NPC relationships for a character"""
        relationships = {}
        for npc_id, npc in self.npcs.items():
            relationships[npc_id] = {
                "name": npc.name,
                "personality": npc.personality.value,
                "relationship_level": npc.relationship_level,
                "trust_level": npc.trust_level,
                "fear_level": npc.fear_level,
                "respect_level": npc.respect_level,
                "current_mood": npc.current_mood
            }
        return relationships
    
    def get_player_moral_status(self, character_id: str) -> Dict[str, Any]:
        """Get player's moral status"""
        if character_id not in self.player_morals:
            return {"error": "Player not found"}
        
        player_moral = self.player_morals[character_id]
        return self._get_player_moral_summary(player_moral)
    
    def get_npc_public_info(self, npc_id: str, player_moral: PlayerMoral = None) -> Dict[str, Any]:
        """Get NPC information that should be visible to players (hides sensitive data)"""
        if npc_id not in self.npcs:
            return {"error": "NPC not found"}
        
        npc = self.npcs[npc_id]
        
        # Get player's known secrets
        known_secrets = []
        if player_moral:
            known_secrets = [secret for secret in npc.secrets_known if secret in player_moral.known_secrets]
        
        # Public information only
        public_info = {
            "id": npc.id,
            "name": npc.name,
            "role": npc.role.value,
            "description": npc.description,
            "location": npc.location,
            "background_story": npc.background_story,
            "special_abilities": npc.special_abilities,
            "quests_given": npc.quests_given,
            "items_offered": npc.items_offered,
            "dialogue_options": npc.dialogue_options,
            "combat_assistance": npc.combat_assistance,
            "boss_fight_help": npc.boss_fight_help,
            # Personality traits (public version)
            "personality": npc.personality_traits.personality_type.value,
            "speech_style": npc.personality_traits.speech_style,
            # Relationship level (simplified)
            "relationship_status": self._get_relationship_status(npc.relationship_level),
            # Current mood (simplified)
            "current_disposition": self._get_disposition(npc.current_mood),
            # Secrets (only if player knows them)
            "known_secrets": known_secrets
        }
        
        return public_info
    
    def get_npc_private_info(self, npc_id: str) -> Dict[str, Any]:
        """Get complete NPC information including sensitive data (for internal use only)"""
        if npc_id not in self.npcs:
            return {"error": "NPC not found"}
        
        npc = self.npcs[npc_id]
        
        # Complete information including sensitive data
        private_info = {
            "id": npc.id,
            "name": npc.name,
            "role": npc.role.value,
            "description": npc.description,
            "location": npc.location,
            "background_story": npc.background_story,
            "special_abilities": npc.special_abilities,
            "quests_given": npc.quests_given,
            "items_offered": npc.items_offered,
            "dialogue_options": npc.dialogue_options,
            "combat_assistance": npc.combat_assistance,
            "boss_fight_help": npc.boss_fight_help,
            # Sensitive information (internal use only)
            "moral_alignment": npc.moral_alignment.value,
            "relationship_level": npc.relationship_level,
            "trust_level": npc.trust_level,
            "fear_level": npc.fear_level,
            "respect_level": npc.respect_level,
            "current_mood": npc.current_mood,
            "secrets_known": npc.secrets_known,
            "relationships_with_others": npc.relationships_with_others,
            # Complete personality traits
            "personality_traits": {
                "personality_type": npc.personality_traits.personality_type.value,
                "speech_style": npc.personality_traits.speech_style,
                "trust_threshold": npc.personality_traits.trust_threshold,
                "anger_threshold": npc.personality_traits.anger_threshold,
                "generosity_level": npc.personality_traits.generosity_level,
                "intelligence_level": npc.personality_traits.intelligence_level,
                "bravery_level": npc.personality_traits.bravery_level,
                "loyalty_level": npc.personality_traits.loyalty_level,
                "curiosity_level": npc.personality_traits.curiosity_level,
                "suspiciousness_level": npc.personality_traits.suspiciousness_level,
                "emotional_stability": npc.personality_traits.emotional_stability,
                "social_preference": npc.personality_traits.social_preference,
                "risk_tolerance": npc.personality_traits.risk_tolerance,
                "adaptability": npc.personality_traits.adaptability,
                "memory_retention": npc.personality_traits.memory_retention,
                "influence_susceptibility": npc.personality_traits.influence_susceptibility,
                "conflict_resolution": npc.personality_traits.conflict_resolution,
                "leadership_tendency": npc.personality_traits.leadership_tendency
            }
        }
        
        return private_info
    
    def _get_relationship_status(self, relationship_level: int) -> str:
        """Convert relationship level to public status description"""
        if relationship_level >= 80:
            return "Very Friendly"
        elif relationship_level >= 60:
            return "Friendly"
        elif relationship_level >= 40:
            return "Neutral"
        elif relationship_level >= 20:
            return "Unfriendly"
        elif relationship_level >= 0:
            return "Hostile"
        else:
            return "Very Hostile"
    
    def _get_disposition(self, mood: str) -> str:
        """Convert internal mood to public disposition description"""
        mood_mapping = {
            "very_happy": "Cheerful",
            "happy": "Pleasant",
            "neutral": "Calm",
            "sad": "Somber",
            "angry": "Irritated",
            "fearful": "Nervous",
            "excited": "Energetic",
            "suspicious": "Wary",
            "trusting": "Open",
            "confident": "Assured",
            "uncertain": "Thoughtful"
        }
        return mood_mapping.get(mood, "Neutral")
    
    def get_npc_dialogue_response(self, npc_id: str, context: str, player_moral: PlayerMoral) -> Dict[str, Any]:
        """Get NPC dialogue response (public version - hides internal calculations)"""
        if npc_id not in self.npcs:
            return {"error": "NPC not found"}
        
        npc = self.npcs[npc_id]
        
        # Get internal response
        internal_response = self.get_personality_based_dialogue(npc, context, player_moral)
        
        # Return public version
        return {
            "npc_name": npc.name,
            "response": internal_response,
            "disposition": self._get_disposition(npc.current_mood),
            "relationship_status": self._get_relationship_status(npc.relationship_level)
        }
    
    def get_npc_interaction_result(self, npc_id: str, action: str, player_moral: PlayerMoral) -> Dict[str, Any]:
        """Get NPC interaction result (public version - hides sensitive calculations)"""
        if npc_id not in self.npcs:
            return {"error": "NPC not found"}
        
        # Perform internal interaction
        internal_result = self.interact_with_npc(npc_id, action, player_moral)
        
        # Return public version
        public_result = {
            "npc_name": internal_result["npc_name"],
            "response": internal_result["response"],
            "relationship_status": self._get_relationship_status(internal_result["new_relationship"]),
            "disposition": self._get_disposition(internal_result["new_mood"]),
            "consequences": internal_result.get("consequences", {}),
            "quest_offered": internal_result.get("quest_offered", False),
            "item_offered": internal_result.get("item_offered", False),
            "combat_help": internal_result.get("combat_help", False)
        }
        
        return public_result
    
    def get_npc_quest_offer(self, npc_id: str, player_moral: PlayerMoral) -> Dict[str, Any]:
        """Get NPC quest offer (public version)"""
        if npc_id not in self.npcs:
            return {"error": "NPC not found"}
        
        npc = self.npcs[npc_id]
        
        # Internal calculation
        compatibility = self.calculate_personality_compatibility(npc, player_moral)
        will_offer = compatibility > 0.5 and npc.relationship_level > 30
        
        if will_offer:
            return {
                "npc_name": npc.name,
                "quest_available": True,
                "quest_description": f"{npc.name} has a task for you.",
                "relationship_status": self._get_relationship_status(npc.relationship_level)
            }
        else:
            return {
                "npc_name": npc.name,
                "quest_available": False,
                "response": f"{npc.name} doesn't seem interested in giving you a quest right now.",
                "relationship_status": self._get_relationship_status(npc.relationship_level)
            }
    
    def get_npc_trade_offer(self, npc_id: str, player_moral: PlayerMoral) -> Dict[str, Any]:
        """Get NPC trade offer (public version)"""
        if npc_id not in self.npcs:
            return {"error": "NPC not found"}
        
        npc = self.npcs[npc_id]
        
        # Internal calculation
        generosity = npc.personality_traits.generosity_level
        relationship_bonus = max(0, npc.relationship_level / 100)
        will_trade = generosity > 5 or relationship_bonus > 0.3
        
        if will_trade:
            return {
                "npc_name": npc.name,
                "trade_available": True,
                "items": npc.items_offered[:3],  # Show only first 3 items
                "relationship_status": self._get_relationship_status(npc.relationship_level)
            }
        else:
            return {
                "npc_name": npc.name,
                "trade_available": False,
                "response": f"{npc.name} doesn't seem interested in trading right now.",
                "relationship_status": self._get_relationship_status(npc.relationship_level)
            }
    
    def get_npc_combat_assistance(self, npc_id: str, player_moral: PlayerMoral) -> Dict[str, Any]:
        """Get NPC combat assistance offer (public version)"""
        if npc_id not in self.npcs:
            return {"error": "NPC not found"}
        
        npc = self.npcs[npc_id]
        
        # Internal calculation
        assistance_result = self.get_npc_help_in_boss_fight(npc_id, player_moral)
        
        # Return public version
        return {
            "npc_name": npc.name,
            "will_help": assistance_result["will_help"],
            "assistance_type": assistance_result.get("assistance_type", "none"),
            "relationship_status": self._get_relationship_status(npc.relationship_level)
        }
    
    def get_all_npcs_public_info(self) -> Dict[str, Any]:
        """Get public information for all NPCs"""
        public_npcs = {}
        for npc_id, npc in self.npcs.items():
            public_npcs[npc_id] = self.get_npc_public_info(npc_id)
        
        return {
            "total_npcs": len(public_npcs),
            "npcs": public_npcs
        }
    
    def get_npc_social_network(self, npc_id: str) -> Dict[str, Any]:
        """Get NPC's social network (public version - simplified relationships)"""
        if npc_id not in self.npcs:
            return {"error": "NPC not found"}
        
        npc = self.npcs[npc_id]
        
        # Convert internal relationships to public descriptions
        public_relationships = {}
        for other_npc_id, relationship_level in npc.relationships_with_others.items():
            if other_npc_id in self.npcs:
                other_npc = self.npcs[other_npc_id]
                public_relationships[other_npc.name] = self._get_relationship_status(relationship_level)
        
        return {
            "npc_name": npc.name,
            "relationships": public_relationships,
            "total_connections": len(public_relationships)
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "npcs": {npc_id: asdict(npc) for npc_id, npc in self.npcs.items()},
            "player_moral": asdict(self.player_moral)
        }
    
    def from_dict(self, data: Dict[str, Any]):
        """Load from dictionary"""
        self.npcs = {}
        for npc_id, npc_data in data.get("npcs", {}).items():
            self.npcs[npc_id] = NPC(**npc_data) 
    
    def _create_test_npcs(self):
        """Create some test NPCs for demonstration"""
        test_npcs = [
            {
                "id": "merchant_001",
                "name": "Eldric the Merchant",
                "role": "merchant",
                "personality": "friendly",
                "moral_alignment": "good",
                "description": "A friendly merchant who runs the local shop",
                "location": "Village Square",
                "background_story": "Eldric has been trading in the village for years",
                "special_abilities": ["Bargaining", "Trade Knowledge"],
                "quests_given": ["Deliver Package", "Find Rare Item"],
                "items_offered": ["Health Potion", "Magic Ring", "Steel Sword"],
                "dialogue_options": {"greeting": "Welcome to my shop!", "farewell": "Come back soon!"},
                "combat_assistance": False,
                "boss_fight_help": False,
                "current_mood": "happy",
                "secrets_known": ["village_secret", "merchant_secret"],
                "relationships_with_others": {"guard_001": 70, "innkeeper_001": 60}
            },
            {
                "id": "guard_001",
                "name": "Captain Marcus",
                "role": "guard",
                "personality": "honorable",
                "moral_alignment": "good",
                "description": "The village guard captain",
                "location": "Village Gate",
                "background_story": "A former soldier who protects the village",
                "special_abilities": ["Combat Training", "Leadership"],
                "quests_given": ["Patrol Route", "Investigate Crime"],
                "items_offered": ["Guard Armor", "Training Sword"],
                "dialogue_options": {"greeting": "Stay safe, traveler.", "farewell": "Keep your wits about you."},
                "combat_assistance": True,
                "boss_fight_help": True,
                "current_mood": "neutral",
                "secrets_known": ["guard_secret", "village_secret"],
                "relationships_with_others": {"merchant_001": 70, "innkeeper_001": 50}
            },
            {
                "id": "mentor_001",
                "name": "Master Thorne",
                "role": "mentor",
                "personality": "wise",
                "moral_alignment": "good",
                "description": "A wise mentor who teaches magic",
                "location": "Tower of Knowledge",
                "background_story": "A powerful mage who has seen many students come and go",
                "special_abilities": ["Magic Teaching", "Ancient Knowledge"],
                "quests_given": ["Learn Spell", "Find Ancient Tome"],
                "items_offered": ["Magic Staff", "Spell Book"],
                "dialogue_options": {"greeting": "Ah, my student. What wisdom do you seek?", "farewell": "May your path be enlightened."},
                "combat_assistance": True,
                "boss_fight_help": True,
                "current_mood": "calm",
                "secrets_known": ["ancient_secret", "magic_secret"],
                "relationships_with_others": {"merchant_001": 40, "guard_001": 60}
            },
            {
                "id": "lover_001",
                "name": "Serena",
                "role": "ally",
                "personality": "friendly",
                "moral_alignment": "good",
                "description": "A kind-hearted healer who cares for the village",
                "location": "Healing House",
                "background_story": "A gentle soul who learned healing from her grandmother",
                "special_abilities": ["Healing", "Herb Lore"],
                "quests_given": ["Gather Herbs", "Heal the Sick"],
                "items_offered": ["Healing Potion", "Herb Bundle"],
                "dialogue_options": {"greeting": "Hello, my love. How are you feeling?", "farewell": "Take care, my dear."},
                "combat_assistance": False,
                "boss_fight_help": False,
                "current_mood": "loving",
                "secrets_known": ["healing_secret", "village_secret"],
                "relationships_with_others": {"merchant_001": 80, "guard_001": 70}
            }
        ]
        
        for npc_data in test_npcs:
            self.create_npc(npc_data)
        
        # Create a default player moral
        self.player_morals["player_001"] = PlayerMoral(
            overall_alignment=MoralAlignment.GOOD,
            good_actions=15,
            bad_actions=2,
            neutral_actions=8,
            reputation=75,
            karma_points=65,
            known_secrets=["village_secret"],
            trusted_by=["merchant_001", "guard_001"],
            feared_by=[]
        )