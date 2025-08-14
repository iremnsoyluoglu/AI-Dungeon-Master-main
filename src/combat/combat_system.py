import random
import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class ActionType(Enum):
    ATTACK = "attack"
    DEFEND = "defend"
    SPELL = "spell"
    ITEM = "item"
    FLEE = "flee"

class CombatState(Enum):
    INITIATIVE = "initiative"
    PLAYER_TURN = "player_turn"
    ENEMY_TURN = "enemy_turn"
    VICTORY = "victory"
    DEFEAT = "defeat"

@dataclass
class CombatAction:
    actor_id: str
    action_type: ActionType
    target_id: str = None
    damage: int = 0
    healing: int = 0
    effect: str = ""
    description: str = ""

@dataclass
class CombatEntity:
    id: str
    name: str
    health: int
    max_health: int
    armor_class: int
    attack_bonus: int
    damage_die: str
    initiative: int
    is_player: bool = True
    is_alive: bool = True
    status_effects: List[str] = None
    
    def __post_init__(self):
        if self.status_effects is None:
            self.status_effects = []

@dataclass
class CombatSession:
    id: str
    entities: Dict[str, CombatEntity]
    turn_order: List[str]
    current_turn: int
    round: int
    state: CombatState
    log: List[str] = None
    
    def __post_init__(self):
        if self.log is None:
            self.log = []

class CombatSystem:
    def __init__(self):
        self.combat_sessions_file = "data/combat_sessions.json"
        self._ensure_data_directory()
        self._load_combat_sessions()
    
    def _ensure_data_directory(self):
        """Veri dizinini oluştur"""
        os.makedirs("data", exist_ok=True)
    
    def _load_combat_sessions(self):
        """Savaş oturumlarını dosyadan yükle"""
        try:
            if os.path.exists(self.combat_sessions_file):
                with open(self.combat_sessions_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.combat_sessions = {}
                    for session_id, session_data in data.items():
                        # Enum değerlerini geri yükle
                        session_data['state'] = CombatState(session_data['state'])
                        for entity_data in session_data['entities'].values():
                            entity_data['action_type'] = ActionType(entity_data.get('action_type', 'attack'))
                        self.combat_sessions[session_id] = CombatSession(**session_data)
            else:
                self.combat_sessions = {}
        except Exception as e:
            print(f"Savaş oturumu yükleme hatası: {e}")
            self.combat_sessions = {}
    
    def _save_combat_sessions(self):
        """Savaş oturumlarını dosyaya kaydet"""
        try:
            with open(self.combat_sessions_file, 'w', encoding='utf-8') as f:
                data = {}
                for session_id, session in self.combat_sessions.items():
                    session_dict = asdict(session)
                    session_dict['state'] = session.state.value
                    # Enum değerlerini string'e çevir
                    for entity_data in session_dict['entities'].values():
                        if 'action_type' in entity_data and isinstance(entity_data['action_type'], ActionType):
                            entity_data['action_type'] = entity_data['action_type'].value
                    data[session_id] = session_dict
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Savaş oturumu kaydetme hatası: {e}")
    
    def start_combat(self, player_character: Dict[str, Any], enemies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Savaş başlat"""
        import secrets
        
        session_id = f"combat_{secrets.token_hex(8)}"
        
        # Oyuncu karakterini oluştur
        player_entity = CombatEntity(
            id="player",
            name=player_character["name"],
            health=player_character["health"],
            max_health=player_character["max_health"],
            armor_class=player_character["armor_class"],
            attack_bonus=player_character.get("attack_bonus", 5),
            damage_die=player_character.get("damage_die", "1d8"),
            initiative=self._roll_initiative(player_character.get("dexterity", 10)),
            is_player=True
        )
        
        # Düşmanları oluştur
        entities = {"player": player_entity}
        for i, enemy_data in enumerate(enemies):
            enemy_id = f"enemy_{i}"
            enemy_entity = CombatEntity(
                id=enemy_id,
                name=enemy_data["name"],
                health=enemy_data["health"],
                max_health=enemy_data["health"],
                armor_class=enemy_data["armor_class"],
                attack_bonus=enemy_data.get("attack_bonus", 3),
                damage_die=enemy_data.get("damage_die", "1d6"),
                initiative=self._roll_initiative(enemy_data.get("dexterity", 10)),
                is_player=False
            )
            entities[enemy_id] = enemy_entity
        
        # Turn sırasını belirle
        turn_order = self._determine_turn_order(entities)
        
        # Savaş oturumu oluştur
        combat_session = CombatSession(
            id=session_id,
            entities=entities,
            turn_order=turn_order,
            current_turn=0,
            round=1,
            state=CombatState.INITIATIVE
        )
        
        self.combat_sessions[session_id] = combat_session
        self._save_combat_sessions()
        
        return {
            "success": True,
            "session_id": session_id,
            "combat_info": {
                "turn_order": turn_order,
                "current_entity": turn_order[0],
                "round": 1,
                "state": combat_session.state.value
            },
            "message": "Savaş başladı!"
        }
    
    def _roll_initiative(self, dexterity: int) -> int:
        """Initiative roll"""
        modifier = (dexterity - 10) // 2
        return random.randint(1, 20) + modifier
    
    def _determine_turn_order(self, entities: Dict[str, CombatEntity]) -> List[str]:
        """Turn sırasını belirle"""
        # Initiative'e göre sırala
        sorted_entities = sorted(
            entities.items(),
            key=lambda x: x[1].initiative,
            reverse=True
        )
        return [entity_id for entity_id, _ in sorted_entities]
    
    def get_combat_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Savaş durumunu getir"""
        session = self.combat_sessions.get(session_id)
        if not session:
            return None
        
        current_entity_id = session.turn_order[session.current_turn]
        current_entity = session.entities[current_entity_id]
        
        return {
            "session_id": session_id,
            "round": session.round,
            "current_entity": current_entity_id,
            "current_entity_name": current_entity.name,
            "state": session.state.value,
            "entities": {
                entity_id: {
                    "name": entity.name,
                    "health": entity.health,
                    "max_health": entity.max_health,
                    "armor_class": entity.armor_class,
                    "is_player": entity.is_player,
                    "is_alive": entity.is_alive
                }
                for entity_id, entity in session.entities.items()
            },
            "turn_order": session.turn_order,
            "log": session.log[-10:]  # Son 10 log
        }
    
    def perform_action(self, session_id: str, action_type: str, target_id: str = None, 
                      item_name: str = None, spell_name: str = None) -> Dict[str, Any]:
        """Savaş aksiyonu gerçekleştir"""
        session = self.combat_sessions.get(session_id)
        if not session:
            return {"success": False, "error": "Savaş oturumu bulunamadı"}
        
        current_entity_id = session.turn_order[session.current_turn]
        current_entity = session.entities[current_entity_id]
        
        if not current_entity.is_alive:
            return {"success": False, "error": "Ölü karakter aksiyon yapamaz"}
        
        # Aksiyonu gerçekleştir
        if action_type == ActionType.ATTACK.value:
            result = self._perform_attack(session, current_entity_id, target_id)
        elif action_type == ActionType.DEFEND.value:
            result = self._perform_defend(session, current_entity_id)
        elif action_type == ActionType.SPELL.value:
            result = self._perform_spell(session, current_entity_id, target_id, spell_name)
        elif action_type == ActionType.ITEM.value:
            result = self._perform_item(session, current_entity_id, item_name)
        elif action_type == ActionType.FLEE.value:
            result = self._perform_flee(session, current_entity_id)
        else:
            return {"success": False, "error": "Geçersiz aksiyon türü"}
        
        # Turn'ü ilerlet
        self._advance_turn(session)
        
        # Savaş durumunu kontrol et
        self._check_combat_end(session)
        
        self._save_combat_sessions()
        
        return result
    
    def _perform_attack(self, session: CombatSession, attacker_id: str, target_id: str) -> Dict[str, Any]:
        """Saldırı gerçekleştir"""
        attacker = session.entities[attacker_id]
        target = session.entities.get(target_id)
        
        if not target or not target.is_alive:
            return {"success": False, "error": "Geçersiz hedef"}
        
        # Saldırı rollü
        attack_roll = random.randint(1, 20) + attacker.attack_bonus
        
        if attack_roll >= target.armor_class:
            # Vuruş başarılı
            damage = self._roll_damage(attacker.damage_die)
            target.health = max(0, target.health - damage)
            
            if target.health <= 0:
                target.is_alive = False
                target.health = 0
            
            log_message = f"{attacker.name} {target.name}'a {damage} hasar verdi!"
            session.log.append(log_message)
            
            return {
                "success": True,
                "action": "attack",
                "attacker": attacker.name,
                "target": target.name,
                "attack_roll": attack_roll,
                "damage": damage,
                "hit": True,
                "target_alive": target.is_alive,
                "log": log_message
            }
        else:
            # Vuruş başarısız
            log_message = f"{attacker.name} {target.name}'ı ıskaladı!"
            session.log.append(log_message)
            
            return {
                "success": True,
                "action": "attack",
                "attacker": attacker.name,
                "target": target.name,
                "attack_roll": attack_roll,
                "damage": 0,
                "hit": False,
                "log": log_message
            }
    
    def _perform_defend(self, session: CombatSession, defender_id: str) -> Dict[str, Any]:
        """Savunma gerçekleştir"""
        defender = session.entities[defender_id]
        
        # Savunma bonusu ver
        defender.armor_class += 2
        defender.status_effects.append("defending")
        
        log_message = f"{defender.name} savunma pozisyonu aldı!"
        session.log.append(log_message)
        
        return {
            "success": True,
            "action": "defend",
            "defender": defender.name,
            "armor_class_bonus": 2,
            "log": log_message
        }
    
    def _perform_spell(self, session: CombatSession, caster_id: str, target_id: str, spell_name: str) -> Dict[str, Any]:
        """Büyü gerçekleştir"""
        caster = session.entities[caster_id]
        target = session.entities.get(target_id) if target_id else caster
        
        # Basit büyü sistemi
        spell_effects = {
            "Fireball": {"damage": 20, "type": "damage"},
            "Heal": {"healing": 15, "type": "healing"},
            "Lightning": {"damage": 25, "type": "damage"},
            "Shield": {"armor_bonus": 5, "type": "defense"}
        }
        
        spell = spell_effects.get(spell_name, {"damage": 10, "type": "damage"})
        
        if spell["type"] == "damage":
            damage = spell["damage"]
            target.health = max(0, target.health - damage)
            if target.health <= 0:
                target.is_alive = False
                target.health = 0
            
            log_message = f"{caster.name} {spell_name} büyüsü ile {target.name}'a {damage} hasar verdi!"
            session.log.append(log_message)
            
            return {
                "success": True,
                "action": "spell",
                "caster": caster.name,
                "target": target.name,
                "spell": spell_name,
                "damage": damage,
                "target_alive": target.is_alive,
                "log": log_message
            }
        
        elif spell["type"] == "healing":
            healing = spell["healing"]
            target.health = min(target.max_health, target.health + healing)
            
            log_message = f"{caster.name} {spell_name} büyüsü ile {target.name}'ı {healing} HP iyileştirdi!"
            session.log.append(log_message)
            
            return {
                "success": True,
                "action": "spell",
                "caster": caster.name,
                "target": target.name,
                "spell": spell_name,
                "healing": healing,
                "log": log_message
            }
    
    def _perform_item(self, session: CombatSession, user_id: str, item_name: str) -> Dict[str, Any]:
        """Eşya kullan"""
        user = session.entities[user_id]
        
        # Basit eşya sistemi
        item_effects = {
            "Health Potion": {"healing": 20, "type": "healing"},
            "Strength Potion": {"attack_bonus": 2, "type": "buff"},
            "Shield": {"armor_bonus": 3, "type": "defense"}
        }
        
        item = item_effects.get(item_name, {"healing": 10, "type": "healing"})
        
        if item["type"] == "healing":
            healing = item["healing"]
            user.health = min(user.max_health, user.health + healing)
            
            log_message = f"{user.name} {item_name} kullandı ve {healing} HP iyileşti!"
            session.log.append(log_message)
            
            return {
                "success": True,
                "action": "item",
                "user": user.name,
                "item": item_name,
                "healing": healing,
                "log": log_message
            }
    
    def _perform_flee(self, session: CombatSession, entity_id: str) -> Dict[str, Any]:
        """Kaçma denemesi"""
        entity = session.entities[entity_id]
        
        # Kaçma başarı şansı
        flee_roll = random.randint(1, 20)
        if flee_roll >= 10:  # %50 şans
            log_message = f"{entity.name} başarıyla kaçtı!"
            session.log.append(log_message)
            
            return {
                "success": True,
                "action": "flee",
                "entity": entity.name,
                "flee_roll": flee_roll,
                "escaped": True,
                "log": log_message
            }
        else:
            log_message = f"{entity.name} kaçamadı!"
            session.log.append(log_message)
            
            return {
                "success": True,
                "action": "flee",
                "entity": entity.name,
                "flee_roll": flee_roll,
                "escaped": False,
                "log": log_message
            }
    
    def _roll_damage(self, damage_die: str) -> int:
        """Hasar rollü"""
        try:
            if "d" in damage_die:
                num_dice, die_size = damage_die.split("d")
                num_dice = int(num_dice) if num_dice else 1
                die_size = int(die_size)
                return sum(random.randint(1, die_size) for _ in range(num_dice))
            else:
                return int(damage_die)
        except:
            return random.randint(1, 8)
    
    def _advance_turn(self, session: CombatSession):
        """Turn'ü ilerlet"""
        session.current_turn += 1
        
        # Round kontrolü
        if session.current_turn >= len(session.turn_order):
            session.current_turn = 0
            session.round += 1
        
        # Ölü karakterleri turn sırasından çıkar
        alive_entities = [entity_id for entity_id in session.turn_order 
                         if session.entities[entity_id].is_alive]
        
        if len(alive_entities) != len(session.turn_order):
            session.turn_order = alive_entities
            session.current_turn = min(session.current_turn, len(session.turn_order) - 1)
    
    def _check_combat_end(self, session: CombatSession):
        """Savaş sonu kontrolü"""
        players = [entity for entity in session.entities.values() if entity.is_player and entity.is_alive]
        enemies = [entity for entity in session.entities.values() if not entity.is_player and entity.is_alive]
        
        if not players:
            session.state = CombatState.DEFEAT
        elif not enemies:
            session.state = CombatState.VICTORY
    
    def get_available_actions(self, session_id: str) -> Dict[str, Any]:
        """Mevcut aksiyonları getir"""
        session = self.combat_sessions.get(session_id)
        if not session:
            return {"success": False, "error": "Savaş oturumu bulunamadı"}
        
        current_entity_id = session.turn_order[session.current_turn]
        current_entity = session.entities[current_entity_id]
        
        actions = []
        
        # Saldırı aksiyonları
        for entity_id, entity in session.entities.items():
            if entity_id != current_entity_id and entity.is_alive:
                actions.append({
                    "type": "attack",
                    "target": entity_id,
                    "target_name": entity.name,
                    "description": f"{entity.name}'a saldır"
                })
        
        # Savunma
        actions.append({
            "type": "defend",
            "description": "Savunma pozisyonu al"
        })
        
        # Kaçma
        actions.append({
            "type": "flee",
            "description": "Kaçmaya çalış"
        })
        
        # Büyüler (sadece oyuncu için)
        if current_entity.is_player:
            spells = ["Fireball", "Heal", "Lightning", "Shield"]
            for spell in spells:
                actions.append({
                    "type": "spell",
                    "spell": spell,
                    "description": f"{spell} büyüsü kullan"
                })
        
        # Eşyalar (sadece oyuncu için)
        if current_entity.is_player:
            items = ["Health Potion", "Strength Potion", "Shield"]
            for item in items:
                actions.append({
                    "type": "item",
                    "item": item,
                    "description": f"{item} kullan"
                })
        
        return {
            "success": True,
            "current_entity": current_entity_id,
            "current_entity_name": current_entity.name,
            "actions": actions
        } 