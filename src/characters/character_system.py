#!/usr/bin/env python3
"""
Character System
===============

Handles character creation, classes, races, and character management.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class CharacterClass:
    """Character class definition"""
    id: str
    name: str
    description: str
    base_hp: int
    base_attack: int
    base_defense: int
    base_special: int
    special_abilities: List[str]
    starting_equipment: List[str]
    base_stats: Dict[str, int]
    theme: str
    role: str

@dataclass
class CharacterRace:
    """Character race definition"""
    id: str
    name: str
    description: str
    hp_bonus: int
    attack_bonus: int
    defense_bonus: int
    special_traits: List[str]

@dataclass
class Character:
    """Character data structure"""
    id: str
    name: str
    user_id: str
    character_class: str
    character_race: str
    level: int
    experience: int
    health: int
    max_health: int
    attack: int
    defense: int
    inventory: List[str]
    skills: List[str]
    created_at: str
    last_updated: str

class CharacterSystem:
    """Manages character creation and management"""
    
    def __init__(self):
        self.characters_file = "data/characters.json"
        self.classes_file = "data/character_classes.json"
        self.races_file = "data/character_races.json"
        self._ensure_data_directory()
        self._load_characters()
        self._load_classes()
        self._load_races()
        self._initialize_default_data()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        import os
        os.makedirs("data", exist_ok=True)
    
    def _load_characters(self):
        """Load characters from file"""
        try:
            import os
            if os.path.exists(self.characters_file):
                with open(self.characters_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.characters = {char_id: Character(**char_data) for char_id, char_data in data.items()}
            else:
                self.characters = {}
        except Exception as e:
            print(f"Error loading characters: {e}")
            self.characters = {}
    
    def _save_characters(self):
        """Save characters to file"""
        try:
            with open(self.characters_file, 'w', encoding='utf-8') as f:
                json.dump({char_id: asdict(char) for char_id, char in self.characters.items()}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving characters: {e}")
    
    def _load_classes(self):
        """Load character classes from file"""
        try:
            import os
            if os.path.exists(self.classes_file):
                with open(self.classes_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.classes = {class_id: CharacterClass(**class_data) for class_id, class_data in data.items()}
            else:
                self.classes = {}
        except Exception as e:
            print(f"Error loading character classes: {e}")
            self.classes = {}
    
    def _save_classes(self):
        """Save character classes to file"""
        try:
            with open(self.classes_file, 'w', encoding='utf-8') as f:
                json.dump({class_id: asdict(char_class) for class_id, char_class in self.classes.items()}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving character classes: {e}")
    
    def _load_races(self):
        """Load character races from file"""
        try:
            import os
            if os.path.exists(self.races_file):
                with open(self.races_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.races = {race_id: CharacterRace(**race_data) for race_id, race_data in data.items()}
            else:
                self.races = {}
        except Exception as e:
            print(f"Error loading character races: {e}")
            self.races = {}
    
    def _save_races(self):
        """Save character races to file"""
        try:
            with open(self.races_file, 'w', encoding='utf-8') as f:
                json.dump({race_id: asdict(race) for race_id, race in self.races.items()}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving character races: {e}")
    
    def _initialize_default_data(self):
        """Initialize default character classes and races if they don't exist"""
        if not self.classes:
            self._create_default_classes()
        
        if not self.races:
            self._create_default_races()
    
    def _create_default_classes(self):
        """Create default character classes"""
        default_classes = {
            "warrior": CharacterClass(
                id="warrior",
                name="Savaşçı",
                description="Güçlü ve dayanıklı savaşçı",
                base_hp=120,
                base_attack=85,
                base_defense=90,
                base_special=0,
                special_abilities=["Kalkan Kullanımı", "Zırh Uzmanlığı", "Shield Wall", "Sword Strike"],
                starting_equipment=["Kılıç", "Kalkan", "Zırh"],
                base_stats={"strength": 16, "dexterity": 12, "constitution": 15, "intelligence": 10, "wisdom": 8, "charisma": 12},
                theme="fantasy",
                role="tank"
            ),
            "mage": CharacterClass(
                id="mage",
                name="Büyücü",
                description="Güçlü büyüler kullanan büyücü",
                base_hp=60,
                base_attack=100,
                base_defense=40,
                base_special=150,
                special_abilities=["Ateş Topu", "Buz Duvarı", "Fireball", "Ice Bolt"],
                starting_equipment=["Asa", "Büyü Kitabı", "Mana İksiri"],
                base_stats={"strength": 8, "dexterity": 10, "constitution": 12, "intelligence": 16, "wisdom": 14, "charisma": 12},
                theme="fantasy",
                role="damage_dealer"
            ),
            "rogue": CharacterClass(
                id="rogue",
                name="Hırsız",
                description="Hızlı ve gizli hareket eden hırsız",
                base_hp=80,
                base_attack=90,
                base_defense=60,
                base_special=95,
                special_abilities=["Gizlenme", "Kritik Vuruş", "Stealth", "Backstab"],
                starting_equipment=["Hançer", "Gizli Ceket", "Kilit Açma Takımı"],
                base_stats={"strength": 12, "dexterity": 16, "constitution": 10, "intelligence": 14, "wisdom": 12, "charisma": 14},
                theme="fantasy",
                role="damage_dealer"
            ),
            "priest": CharacterClass(
                id="priest",
                name="Rahip",
                description="İyileştirici, yüksek heal ve savunma",
                base_hp=70,
                base_attack=50,
                base_defense=70,
                base_special=80,
                special_abilities=["İyileştirme", "Kutsama", "Heal", "Bless"],
                starting_equipment=["Kutsal Asa", "İyileştirme İksiri", "Kutsal Kitap"],
                base_stats={"strength": 10, "dexterity": 8, "constitution": 14, "intelligence": 12, "wisdom": 16, "charisma": 14},
                theme="fantasy",
                role="support"
            ),
            "paladin": CharacterClass(
                id="paladin",
                name="Paladin",
                description="Kutsal savaşçı, tank ve healer karışımı",
                base_hp=100,
                base_attack=70,
                base_defense=85,
                base_special=40,
                special_abilities=["Kutsal Kalkan", "İyileştirme Dokunuşu", "Divine Smite", "Lay on Hands"],
                starting_equipment=["Kutsal Kılıç", "Kutsal Kalkan", "Kutsal Zırh"],
                base_stats={"strength": 14, "dexterity": 10, "constitution": 14, "intelligence": 10, "wisdom": 14, "charisma": 16},
                theme="fantasy",
                role="tank"
            ),
            "druid": CharacterClass(
                id="druid",
                name="Druid",
                description="Doğa büyücüsü, şekil değiştirme uzmanı",
                base_hp=85,
                base_attack=65,
                base_defense=65,
                base_special=90,
                special_abilities=["Şekil Değiştirme", "Doğa Büyüleri", "Wild Shape", "Nature's Wrath"],
                starting_equipment=["Doğa Asası", "Druid Kitabı", "Doğa Tılsımı"],
                base_stats={"strength": 12, "dexterity": 12, "constitution": 12, "intelligence": 12, "wisdom": 16, "charisma": 10},
                theme="fantasy",
                role="support"
            ),
            "hunter": CharacterClass(
                id="hunter",
                name="Avcı",
                description="Uzak mesafe savaşçısı, hayvan arkadaşları",
                base_hp=90,
                base_attack=80,
                base_defense=70,
                base_special=95,
                special_abilities=["Çoklu Ok", "Keskin Nişan", "Beast Companion", "Precise Shot"],
                starting_equipment=["Yay", "Ok", "Deri Zırh"],
                base_stats={"strength": 12, "dexterity": 16, "constitution": 12, "intelligence": 10, "wisdom": 14, "charisma": 10},
                theme="fantasy",
                role="balanced"
            ),
            "warlock": CharacterClass(
                id="warlock",
                name="Warlock",
                description="Karanlık büyücü, demon paktları",
                base_hp=65,
                base_attack=85,
                base_defense=45,
                base_special=100,
                special_abilities=["Karanlık Büyü", "Demon Çağırma", "Dark Magic", "Demon Pact"],
                starting_equipment=["Karanlık Asa", "Demon Kitabı", "Karanlık Tılsım"],
                base_stats={"strength": 8, "dexterity": 10, "constitution": 10, "intelligence": 16, "wisdom": 12, "charisma": 16},
                theme="fantasy",
                role="damage_dealer"
            ),
            "space_marine": CharacterClass(
                id="space_marine",
                name="Space Marine",
                description="Süper asker, yüksek HP ve savunma",
                base_hp=150,
                base_attack=95,
                base_defense=100,
                base_special=120,
                special_abilities=["Bolter Fire", "Power Armor", "Chainsword Strike", "Tactical Advance"],
                starting_equipment=["Bolter", "Power Armor", "Chainsword"],
                base_stats={"strength": 18, "dexterity": 14, "constitution": 16, "intelligence": 12, "wisdom": 10, "charisma": 12},
                theme="warhammer40k",
                role="tank"
            ),
            "tech_priest": CharacterClass(
                id="tech_priest",
                name="Tech-Priest",
                description="Teknoloji uzmanı, yüksek tech ve savunma",
                base_hp=90,
                base_attack=60,
                base_defense=80,
                base_special=100,
                special_abilities=["Repair", "Tech Scan", "Machine Spirit", "Techno-ritual"],
                starting_equipment=["Tech Staff", "Servo Skull", "Tech Armor"],
                base_stats={"strength": 12, "dexterity": 10, "constitution": 14, "intelligence": 16, "wisdom": 12, "charisma": 10},
                theme="warhammer40k",
                role="support"
            ),
            "inquisitor": CharacterClass(
                id="inquisitor",
                name="Inquisitor",
                description="Araştırmacı, dengeli istatistikler",
                base_hp=100,
                base_attack=85,
                base_defense=75,
                base_special=95,
                special_abilities=["Purge", "Investigate", "Interrogation", "Divine Authority"],
                starting_equipment=["Inquisitor Staff", "Inquisitor Armor", "Holy Relic"],
                base_stats={"strength": 14, "dexterity": 12, "constitution": 12, "intelligence": 14, "wisdom": 16, "charisma": 16},
                theme="warhammer40k",
                role="balanced"
            ),
            "imperial_guard": CharacterClass(
                id="imperial_guard",
                name="Imperial Guard",
                description="Asker, takım çalışması odaklı",
                base_hp=80,
                base_attack=70,
                base_defense=60,
                base_special=90,
                special_abilities=["Teamwork", "Suppression", "Cover Fire", "Tactical Formation"],
                starting_equipment=["Lasgun", "Flak Armor", "Grenades"],
                base_stats={"strength": 14, "dexterity": 12, "constitution": 12, "intelligence": 10, "wisdom": 12, "charisma": 12},
                theme="warhammer40k",
                role="balanced"
            )
        }
        
        self.classes.update(default_classes)
        self._save_classes()
    
    def _create_default_races(self):
        """Create default character races"""
        default_races = {
            "human": CharacterRace(
                id="human",
                name="İnsan",
                description="Dengeli ve uyumlu insan",
                hp_bonus=0,
                attack_bonus=0,
                defense_bonus=0,
                special_traits=["Uyumluluk", "Çok Yönlülük"]
            ),
            "elf": CharacterRace(
                id="elf",
                name="Elf",
                description="Zarif ve büyüye yatkın elf",
                hp_bonus=-10,
                attack_bonus=2,
                defense_bonus=1,
                special_traits=["Büyü Uzmanlığı", "Doğa Bağlantısı"]
            ),
            "dwarf": CharacterRace(
                id="dwarf",
                name="Cüce",
                description="Güçlü ve dayanıklı cüce",
                hp_bonus=20,
                attack_bonus=1,
                defense_bonus=3,
                special_traits=["Zırh Uzmanlığı", "Madencilik"]
            ),
            "orc": CharacterRace(
                id="orc",
                name="Ork",
                description="Vahşi ve güçlü ork",
                hp_bonus=15,
                attack_bonus=3,
                defense_bonus=0,
                special_traits=["Vahşi Güç", "Dayanıklılık"]
            )
        }
        
        self.races.update(default_races)
        self._save_races()
    
    def create_character(self, user_id: str, name: str, character_class: str, character_race: str) -> Dict[str, Any]:
        """Create a new character"""
        try:
            # Validate class and race
            if character_class not in self.classes:
                return {"success": False, "error": "Invalid character class"}
            
            if character_race not in self.races:
                return {"success": False, "error": "Invalid character race"}
            
            # Get class and race data
            char_class = self.classes[character_class]
            char_race = self.races[character_race]
            
            # Calculate base stats
            base_hp = char_class.base_hp + char_race.hp_bonus
            base_attack = char_class.base_attack + char_race.attack_bonus
            base_defense = char_class.base_defense + char_race.defense_bonus
            
            # Create character
            character_id = str(uuid.uuid4())
            now = datetime.now().isoformat()
            
            character = Character(
                id=character_id,
                name=name,
                user_id=user_id,
                character_class=character_class,
                character_race=character_race,
                level=1,
                experience=0,
                health=base_hp,
                max_health=base_hp,
                attack=base_attack,
                defense=base_defense,
                inventory=char_class.starting_equipment.copy(),
                skills=char_class.special_abilities.copy(),
                created_at=now,
                last_updated=now
            )
            
            self.characters[character_id] = character
            self._save_characters()
            
            return {
                "success": True,
                "character_id": character_id,
                "character": asdict(character),
                "message": "Character created successfully"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_character(self, character_id: str) -> Optional[Character]:
        """Get character by ID"""
        return self.characters.get(character_id)
    
    def get_user_characters(self, user_id: str) -> List[Character]:
        """Get all characters for a user"""
        return [char for char in self.characters.values() if char.user_id == user_id]
    
    def get_character_classes(self) -> Dict[str, CharacterClass]:
        """Get all character classes"""
        return self.classes
    
    def get_character_races(self) -> Dict[str, CharacterRace]:
        """Get all character races"""
        return self.races
    
    def update_character(self, character_id: str, updates: Dict[str, Any]) -> bool:
        """Update character data"""
        character = self.characters.get(character_id)
        if not character:
            return False
        
        # Update fields
        for field, value in updates.items():
            if hasattr(character, field):
                setattr(character, field, value)
        
        character.last_updated = datetime.now().isoformat()
        self._save_characters()
        return True
    
    def delete_character(self, character_id: str) -> bool:
        """Delete a character"""
        if character_id in self.characters:
            del self.characters[character_id]
            self._save_characters()
            return True
        return False
    
    def get_classes_by_theme(self, theme: str) -> Dict[str, CharacterClass]:
        """Get character classes filtered by theme (fantasy or warhammer40k)"""
        return {class_id: char_class for class_id, char_class in self.classes.items() 
                if char_class.theme == theme}
    
    def get_classes_by_role(self, role: str) -> Dict[str, CharacterClass]:
        """Get character classes filtered by role (tank, damage_dealer, support, balanced)"""
        return {class_id: char_class for class_id, char_class in self.classes.items() 
                if char_class.role == role}
    
    def get_class_stats(self, character_class: str) -> Optional[Dict[str, Any]]:
        """Get detailed stats for a character class"""
        if character_class not in self.classes:
            return None
        
        char_class = self.classes[character_class]
        return {
            "id": char_class.id,
            "name": char_class.name,
            "description": char_class.description,
            "base_hp": char_class.base_hp,
            "base_attack": char_class.base_attack,
            "base_defense": char_class.base_defense,
            "base_special": char_class.base_special,
            "special_abilities": char_class.special_abilities,
            "starting_equipment": char_class.starting_equipment,
            "base_stats": char_class.base_stats,
            "theme": char_class.theme,
            "role": char_class.role
        }
    
    def get_all_themes(self) -> List[str]:
        """Get all available themes"""
        return list(set(char_class.theme for char_class in self.classes.values()))
    
    def get_all_roles(self) -> List[str]:
        """Get all available roles"""
        return list(set(char_class.role for char_class in self.classes.values())) 