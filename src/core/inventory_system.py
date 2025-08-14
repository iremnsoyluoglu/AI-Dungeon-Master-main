#!/usr/bin/env python3
"""
Inventory Management System
==========================

Comprehensive inventory system with item-based actions, equipment management,
and contextual item usage.
"""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum

class ItemType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"
    QUEST = "quest"
    MATERIAL = "material"
    TOOL = "tool"
    MAGIC = "magic"

class ItemRarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

class ItemSlot(Enum):
    WEAPON_MAIN = "weapon_main"
    WEAPON_OFF = "weapon_off"
    ARMOR_HEAD = "armor_head"
    ARMOR_CHEST = "armor_chest"
    ARMOR_LEGS = "armor_legs"
    ARMOR_FEET = "armor_feet"
    ACCESSORY_1 = "accessory_1"
    ACCESSORY_2 = "accessory_2"

class InventorySystem:
    """Comprehensive inventory management system"""
    
    def __init__(self):
        self.inventory_file = "data/inventories.json"
        self.items_file = "data/items.json"
        self._ensure_data_directory()
        self._load_items()
        self._load_inventories()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs("data", exist_ok=True)
    
    def _load_items(self):
        """Load item definitions"""
        try:
            if os.path.exists(self.items_file):
                with open(self.items_file, 'r', encoding='utf-8') as f:
                    self.items = json.load(f)
            else:
                self.items = self._create_default_items()
                self._save_items()
        except Exception as e:
            print(f"Error loading items: {e}")
            self.items = self._create_default_items()
    
    def _save_items(self):
        """Save item definitions"""
        try:
            with open(self.items_file, 'w', encoding='utf-8') as f:
                json.dump(self.items, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving items: {e}")
    
    def _load_inventories(self):
        """Load player inventories"""
        try:
            if os.path.exists(self.inventory_file):
                with open(self.inventory_file, 'r', encoding='utf-8') as f:
                    self.inventories = json.load(f)
            else:
                self.inventories = {}
        except Exception as e:
            print(f"Error loading inventories: {e}")
            self.inventories = {}
    
    def _save_inventories(self):
        """Save player inventories"""
        try:
            with open(self.inventory_file, 'w', encoding='utf-8') as f:
                json.dump(self.inventories, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving inventories: {e}")
    
    def _create_default_items(self) -> Dict[str, Any]:
        """Create default item definitions"""
        return {
            "steel_sword": {
                "id": "steel_sword",
                "name": "Çelik Kılıç",
                "type": ItemType.WEAPON.value,
                "rarity": ItemRarity.COMMON.value,
                "slot": ItemSlot.WEAPON_MAIN.value,
                "description": "Güvenilir bir çelik kılıç. Savaşta etkili.",
                "stats": {
                    "attack": 8,
                    "defense": 0,
                    "damage": "1d8",
                    "critical_chance": 0.05
                },
                "requirements": {
                    "level": 1,
                    "strength": 12
                },
                "effects": [],
                "value": 50,
                "weight": 3.0
            },
            "leather_armor": {
                "id": "leather_armor",
                "name": "Deri Zırh",
                "type": ItemType.ARMOR.value,
                "rarity": ItemRarity.COMMON.value,
                "slot": ItemSlot.ARMOR_CHEST.value,
                "description": "Hafif ve esnek deri zırh. Hareketi kısıtlamaz.",
                "stats": {
                    "attack": 0,
                    "defense": 4,
                    "armor_class": 12,
                    "movement_penalty": 0
                },
                "requirements": {
                    "level": 1,
                    "dexterity": 10
                },
                "effects": [],
                "value": 30,
                "weight": 2.0
            },
            "health_potion": {
                "id": "health_potion",
                "name": "Can İksiri",
                "type": ItemType.CONSUMABLE.value,
                "rarity": ItemRarity.COMMON.value,
                "slot": None,
                "description": "Yaralarınızı iyileştiren sihirli iksir.",
                "stats": {
                    "healing": 20,
                    "duration": 0
                },
                "requirements": {},
                "effects": ["heal"],
                "value": 25,
                "weight": 0.5,
                "stackable": True,
                "max_stack": 10
            },
            "mana_potion": {
                "id": "mana_potion",
                "name": "Mana İksiri",
                "type": ItemType.CONSUMABLE.value,
                "rarity": ItemRarity.COMMON.value,
                "slot": None,
                "description": "Mana enerjinizi yenileyen iksir.",
                "stats": {
                    "mana_restore": 25,
                    "duration": 0
                },
                "requirements": {},
                "effects": ["mana_restore"],
                "value": 30,
                "weight": 0.5,
                "stackable": True,
                "max_stack": 10
            },
            "fireball_scroll": {
                "id": "fireball_scroll",
                "name": "Ateş Topu Tomarı",
                "type": ItemType.MAGIC.value,
                "rarity": ItemRarity.UNCOMMON.value,
                "slot": None,
                "description": "Güçlü bir ateş topu büyüsü içeren tomar.",
                "stats": {
                    "damage": "8d6",
                    "range": 150,
                    "area_effect": True
                },
                "requirements": {
                    "level": 3,
                    "intelligence": 14
                },
                "effects": ["fire_damage", "area_effect"],
                "value": 150,
                "weight": 0.1,
                "consumable": True
            }
        }
    
    def get_item(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get item definition by ID"""
        return self.items.get(item_id)
    
    def get_player_inventory(self, player_id: str) -> Dict[str, Any]:
        """Get player's inventory"""
        if player_id not in self.inventories:
            self.inventories[player_id] = {
                "items": [],
                "equipped": {},
                "gold": 100,
                "capacity": 50,
                "max_capacity": 100,
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
        return self.inventories[player_id]
    
    def add_item(self, player_id: str, item_id: str, quantity: int = 1) -> Dict[str, Any]:
        """Add item to player's inventory"""
        try:
            item_def = self.get_item(item_id)
            if not item_def:
                return {"success": False, "error": f"Item {item_id} not found"}
            
            inventory = self.get_player_inventory(player_id)
            
            # Check if item is stackable
            if item_def.get("stackable", False):
                # Find existing stack
                existing_item = None
                for item in inventory["items"]:
                    if item["item_id"] == item_id and item.get("quantity", 1) < item_def.get("max_stack", 1):
                        existing_item = item
                        break
                
                if existing_item:
                    max_add = item_def.get("max_stack", 1) - existing_item.get("quantity", 1)
                    actual_add = min(quantity, max_add)
                    existing_item["quantity"] = existing_item.get("quantity", 1) + actual_add
                else:
                    # Create new stack
                    actual_add = min(quantity, item_def.get("max_stack", 1))
                    inventory["items"].append({
                        "id": str(uuid.uuid4()),
                        "item_id": item_id,
                        "quantity": actual_add,
                        "acquired_at": datetime.now().isoformat()
                    })
            else:
                # Non-stackable item
                for _ in range(quantity):
                    inventory["items"].append({
                        "id": str(uuid.uuid4()),
                        "item_id": item_id,
                        "quantity": 1,
                        "acquired_at": datetime.now().isoformat()
                    })
            
            inventory["last_updated"] = datetime.now().isoformat()
            self._save_inventories()
            
            return {
                "success": True,
                "item_id": item_id,
                "quantity": quantity,
                "message": f"Added {quantity}x {item_def['name']} to inventory"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error adding item: {str(e)}"}
    
    def remove_item(self, player_id: str, item_id: str, quantity: int = 1) -> Dict[str, Any]:
        """Remove item from player's inventory"""
        try:
            inventory = self.get_player_inventory(player_id)
            item_def = self.get_item(item_id)
            
            if not item_def:
                return {"success": False, "error": f"Item {item_id} not found"}
            
            # Find items to remove
            items_to_remove = []
            remaining_quantity = quantity
            
            for item in inventory["items"]:
                if item["item_id"] == item_id and remaining_quantity > 0:
                    item_qty = item.get("quantity", 1)
                    remove_qty = min(remaining_quantity, item_qty)
                    
                    if remove_qty >= item_qty:
                        items_to_remove.append(item)
                        remaining_quantity -= item_qty
                    else:
                        item["quantity"] = item_qty - remove_qty
                        remaining_quantity = 0
                        break
            
            # Remove items
            for item in items_to_remove:
                inventory["items"].remove(item)
            
            if remaining_quantity > 0:
                return {"success": False, "error": f"Insufficient quantity of {item_def['name']}"}
            
            inventory["last_updated"] = datetime.now().isoformat()
            self._save_inventories()
            
            return {
                "success": True,
                "item_id": item_id,
                "quantity": quantity,
                "message": f"Removed {quantity}x {item_def['name']} from inventory"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error removing item: {str(e)}"}
    
    def equip_item(self, player_id: str, item_id: str) -> Dict[str, Any]:
        """Equip an item"""
        try:
            inventory = self.get_player_inventory(player_id)
            item_def = self.get_item(item_id)
            
            if not item_def:
                return {"success": False, "error": f"Item {item_id} not found"}
            
            # Check if player has the item
            player_has_item = False
            for item in inventory["items"]:
                if item["item_id"] == item_id:
                    player_has_item = True
                    break
            
            if not player_has_item:
                return {"success": False, "error": f"You don't have {item_def['name']}"}
            
            # Check if item is equippable
            if not item_def.get("slot"):
                return {"success": False, "error": f"{item_def['name']} cannot be equipped"}
            
            slot = item_def["slot"]
            
            # Unequip existing item in slot
            if slot in inventory["equipped"]:
                unequipped_item = inventory["equipped"][slot]
                inventory["equipped"].pop(slot)
            
            # Equip new item
            inventory["equipped"][slot] = {
                "item_id": item_id,
                "equipped_at": datetime.now().isoformat()
            }
            
            inventory["last_updated"] = datetime.now().isoformat()
            self._save_inventories()
            
            return {
                "success": True,
                "item_id": item_id,
                "slot": slot,
                "message": f"Equipped {item_def['name']} in {slot}"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error equipping item: {str(e)}"}
    
    def unequip_item(self, player_id: str, slot: str) -> Dict[str, Any]:
        """Unequip an item from a slot"""
        try:
            inventory = self.get_player_inventory(player_id)
            
            if slot not in inventory["equipped"]:
                return {"success": False, "error": f"No item equipped in {slot}"}
            
            unequipped_item = inventory["equipped"][slot]
            item_def = self.get_item(unequipped_item["item_id"])
            
            inventory["equipped"].pop(slot)
            inventory["last_updated"] = datetime.now().isoformat()
            self._save_inventories()
            
            return {
                "success": True,
                "item_id": unequipped_item["item_id"],
                "slot": slot,
                "message": f"Unequipped {item_def['name']} from {slot}"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error unequipping item: {str(e)}"}
    
    def use_item(self, player_id: str, item_id: str, target: Optional[str] = None) -> Dict[str, Any]:
        """Use a consumable item"""
        try:
            inventory = self.get_player_inventory(player_id)
            item_def = self.get_item(item_id)
            
            if not item_def:
                return {"success": False, "error": f"Item {item_id} not found"}
            
            # Check if item is consumable
            if item_def["type"] != ItemType.CONSUMABLE.value:
                return {"success": False, "error": f"{item_def['name']} is not consumable"}
            
            # Check if player has the item
            item_found = False
            for item in inventory["items"]:
                if item["item_id"] == item_id:
                    if item.get("quantity", 1) > 0:
                        item_found = True
                        # Remove one from stack
                        if item.get("quantity", 1) > 1:
                            item["quantity"] = item["quantity"] - 1
                        else:
                            inventory["items"].remove(item)
                        break
            
            if not item_found:
                return {"success": False, "error": f"You don't have {item_def['name']}"}
            
            # Apply item effects
            effects = self._apply_item_effects(item_def, target)
            
            inventory["last_updated"] = datetime.now().isoformat()
            self._save_inventories()
            
            return {
                "success": True,
                "item_id": item_id,
                "effects": effects,
                "message": f"Used {item_def['name']}"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error using item: {str(e)}"}
    
    def _apply_item_effects(self, item_def: Dict[str, Any], target: Optional[str] = None) -> Dict[str, Any]:
        """Apply item effects"""
        effects = {}
        
        for effect in item_def.get("effects", []):
            if effect == "heal":
                healing = item_def["stats"].get("healing", 0)
                effects["healing"] = healing
            elif effect == "mana_restore":
                mana_restore = item_def["stats"].get("mana_restore", 0)
                effects["mana_restore"] = mana_restore
        
        return effects
    
    def get_equipment_stats(self, player_id: str) -> Dict[str, Any]:
        """Get combined stats from equipped items"""
        inventory = self.get_player_inventory(player_id)
        total_stats = {
            "attack": 0,
            "defense": 0,
            "armor_class": 0,
            "critical_chance": 0,
            "movement_penalty": 0
        }
        
        for slot, equipped_item in inventory["equipped"].items():
            item_def = self.get_item(equipped_item["item_id"])
            if item_def and "stats" in item_def:
                for stat, value in item_def["stats"].items():
                    if stat in total_stats:
                        total_stats[stat] += value
        
        return total_stats
    
    def get_contextual_actions(self, player_id: str, scenario_type: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get contextual inventory actions based on scenario and context"""
        inventory = self.get_player_inventory(player_id)
        contextual_actions = []
        
        # Check for healing items in combat
        if context.get("situation") == "combat":
            for item in inventory["items"]:
                item_def = self.get_item(item["item_id"])
                if item_def and item_def["type"] == ItemType.CONSUMABLE.value:
                    if "heal" in item_def.get("effects", []):
                        contextual_actions.append({
                            "type": "inventory",
                            "description": f"💊 {item_def['name']} kullan",
                            "action": "use_item",
                            "item_id": item["item_id"],
                            "context": "healing",
                            "dice": "1d20",
                            "skill": "medicine"
                        })
        
        # Check for magic items in magical scenarios
        if scenario_type == "fantasy" and context.get("situation") == "magical":
            for item in inventory["items"]:
                item_def = self.get_item(item["item_id"])
                if item_def and item_def["type"] == ItemType.MAGIC.value:
                    contextual_actions.append({
                        "type": "inventory",
                        "description": f"🔮 {item_def['name']} kullan",
                        "action": "use_item",
                        "item_id": item["item_id"],
                        "context": "magical",
                        "dice": "1d20",
                        "skill": "arcana"
                    })
        
        # Check for tools in exploration
        if context.get("situation") == "exploration":
            for item in inventory["items"]:
                item_def = self.get_item(item["item_id"])
                if item_def and item_def["type"] == ItemType.TOOL.value:
                    contextual_actions.append({
                        "type": "inventory",
                        "description": f"🔧 {item_def['name']} kullan",
                        "action": "use_item",
                        "item_id": item["item_id"],
                        "context": "exploration",
                        "dice": "1d20",
                        "skill": "tool_proficiency"
                    })
        
        return contextual_actions
