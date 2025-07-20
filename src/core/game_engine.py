import random
import logging

logger = logging.getLogger(__name__)

class GameEngine:
    def __init__(self):
        self.active = True
        self.current_session = None
        self.dice_history = []
        # Merkezi düşman listesi
        self.enemies = [
            {"name": "Goblin", "hp": 30, "attack": 5, "defense": 2, "xpReward": 5},
            {"name": "Orman Ruhu", "hp": 40, "attack": 7, "defense": 3, "xpReward": 8},
            {"name": "Kayıp Ruh", "hp": 25, "attack": 6, "defense": 1, "xpReward": 6},
            {"name": "Karanlık Centurion", "hp": 60, "attack": 12, "defense": 6, "xpReward": 15},
            {"name": "Xenos Scout", "hp": 35, "attack": 8, "defense": 4, "xpReward": 10},
            {"name": "Daemonhost", "hp": 50, "attack": 14, "defense": 8, "xpReward": 18},
            {"name": "Harpy Swarm", "hp": 45, "attack": 10, "defense": 5, "xpReward": 12},
            {"name": "Ork Savaşçısı", "hp": 55, "attack": 11, "defense": 7, "xpReward": 14},
            {"name": "Ejderha", "hp": 300, "attack": 120, "defense": 80, "xpReward": 100}
        ]
        # Sınıf bazlı yetenek ağaçları
        self.skill_trees = {
            "warrior": [
                {"name": "Slash", "description": "Düz saldırı", "requiredXP": 0, "unlocked": True, "effect": "attack"},
                {"name": "Shield Bash", "description": "Rakibi sersemletir", "requiredXP": 10, "unlocked": False, "effect": "stun"},
                {"name": "Battle Cry", "description": "Takıma saldırı buff'u", "requiredXP": 20, "unlocked": False, "effect": "team_buff"},
                {"name": "Wrath of Titans", "description": "Ultimate: Devasa güçle saldırı", "requiredXP": 40, "unlocked": False, "effect": "ultimate_warrior"}
            ],
            "mage": [
                {"name": "Fire Bolt", "description": "Ateşli büyü saldırısı", "requiredXP": 0, "unlocked": True, "effect": "fire_attack"},
                {"name": "Arcane Shield", "description": "2 tur büyü kalkanı", "requiredXP": 10, "unlocked": False, "effect": "magic_shield"},
                {"name": "Mana Burn", "description": "Rakibin manasını yakar", "requiredXP": 20, "unlocked": False, "effect": "mana_burn"},
                {"name": "Meteor Storm", "description": "Ultimate: Tüm düşmanlara dev hasar", "requiredXP": 40, "unlocked": False, "effect": "ultimate_mage"}
            ],
            "rogue": [
                {"name": "Backstab", "description": "Kritik gizli saldırı", "requiredXP": 0, "unlocked": True, "effect": "crit_attack"},
                {"name": "Smoke Bomb", "description": "Kaçma şansı yaratır", "requiredXP": 10, "unlocked": False, "effect": "escape"},
                {"name": "Poison Blade", "description": "3 tur zehir etkisi", "requiredXP": 20, "unlocked": False, "effect": "poison"},
                {"name": "Death Dance", "description": "Ultimate: Çoklu hızlı saldırı", "requiredXP": 40, "unlocked": False, "effect": "ultimate_rogue"}
            ],
            "priest": [
                {"name": "Heal", "description": "Can yeniler", "requiredXP": 0, "unlocked": True, "effect": "heal"},
                {"name": "Holy Fire", "description": "Kutsal ateş saldırısı", "requiredXP": 10, "unlocked": False, "effect": "holy_fire"},
                {"name": "Curse Cleanse", "description": "Laneti temizler", "requiredXP": 20, "unlocked": False, "effect": "cleanse"},
                {"name": "Divine Judgment", "description": "Ultimate: İlahi yargı saldırısı", "requiredXP": 40, "unlocked": False, "effect": "ultimate_priest"}
            ],
            "space_marine": [
                {"name": "Plasma Shot", "description": "Plazma silahı saldırısı", "requiredXP": 0, "unlocked": True, "effect": "plasma_attack"},
                {"name": "Suppressive Fire", "description": "Düşmanı bastırır", "requiredXP": 10, "unlocked": False, "effect": "suppress"},
                {"name": "Cover Maneuver", "description": "Savunma pozisyonu", "requiredXP": 20, "unlocked": False, "effect": "cover"},
                {"name": "Orbital Strike", "description": "Ultimate: Yörüngeden bombardıman", "requiredXP": 40, "unlocked": False, "effect": "ultimate_space_marine"}
            ],
            "tech_priest": [
                {"name": "Servo Skull Hack", "description": "Düşman mekaniklerini hackler", "requiredXP": 0, "unlocked": True, "effect": "hack"},
                {"name": "Power Surge", "description": "Enerji patlaması", "requiredXP": 10, "unlocked": False, "effect": "power_surge"},
                {"name": "Shield Reboot", "description": "Kalkanı yeniler", "requiredXP": 20, "unlocked": False, "effect": "shield_reboot"},
                {"name": "Techno-Realm Overload", "description": "Ultimate: Tüm teknolojik düşmanlara dev hasar", "requiredXP": 40, "unlocked": False, "effect": "ultimate_tech_priest"}
            ],
            "inquisitor": [
                {"name": "Mind Probe", "description": "Zihin okuma", "requiredXP": 0, "unlocked": True, "effect": "mind_probe"},
                {"name": "Heretic Burn", "description": "Kafir yakma saldırısı", "requiredXP": 10, "unlocked": False, "effect": "heretic_burn"},
                {"name": "Interrogate", "description": "Bilgi toplama", "requiredXP": 20, "unlocked": False, "effect": "interrogate"},
                {"name": "Emperor's Wrath", "description": "Ultimate: İmparator'un gazabı", "requiredXP": 40, "unlocked": False, "effect": "ultimate_inquisitor"}
            ],
            "imperial_guard": [
                {"name": "Frag Grenade", "description": "El bombası saldırısı", "requiredXP": 0, "unlocked": True, "effect": "grenade"},
                {"name": "Tactical Advance", "description": "Taktiksel ilerleme, savunma artar", "requiredXP": 10, "unlocked": False, "effect": "tactical_advance"},
                {"name": "Rally Troops", "description": "Takımı güçlendirir", "requiredXP": 20, "unlocked": False, "effect": "rally"},
                {"name": "Regimental Fury", "description": "Ultimate: Alay öfkesiyle dev saldırı", "requiredXP": 40, "unlocked": False, "effect": "ultimate_imperial_guard"}
            ]
        }

    def roll_dice(self, dice_type="d20", modifier=0):
        """Zar atma fonksiyonu"""
        if dice_type.startswith("d"):
            sides = int(dice_type[1:])
        else:
            sides = 20
            
        result = random.randint(1, sides) + modifier
        self.dice_history.append({
            "dice": dice_type,
            "modifier": modifier,
            "result": result
        })
        
        logger.info(f"Dice roll: {dice_type}+{modifier} = {result}")
        return result
    
    def start_session(self, campaign_id, players):
        """Yeni oyun oturumu başlat"""
        self.current_session = {
            "campaign_id": campaign_id,
            "players": players,
            "current_step": "start",
            "current_scene": "burned_village",  # Default first scene
            "inventory": {},
            "npcs": {},
            "locations": {},
            "combat_state": None,
            "boss_fight": False
        }
        logger.info(f"New session started for campaign: {campaign_id}")
        return self.current_session
    
    def get_session_state(self):
        """Mevcut oturum durumunu döndür"""
        return self.current_session
    
    def update_session(self, step_id, data=None):
        """Oturum durumunu güncelle"""
        if self.current_session:
            self.current_session["current_step"] = step_id
            if data:
                self.current_session.update(data)
            logger.info(f"Session updated to step: {step_id}")
    
    def end_session(self):
        """Oturumu sonlandır"""
        if self.current_session:
            logger.info(f"Session ended for campaign: {self.current_session['campaign_id']}")
            self.current_session = None
    
    def get_enemy(self, name):
        for enemy in self.enemies:
            if enemy["name"].lower() == name.lower():
                return enemy.copy()
        return None

    def award_xp_and_unlock_skills(self, character, xp_gained):
        """Karaktere XP ekle ve skill aç"""
        character["xp"] = character.get("xp", 0) + xp_gained
        for skill in character.get("skills", []):
            if not skill.get("unlocked", False) and character["xp"] >= skill["requiredXP"]:
                skill["unlocked"] = True
        return character

    def add_item_to_inventory(self, character, item):
        """Karakterin envanterine eşya ekle"""
        if "inventory" not in character:
            character["inventory"] = []
        character["inventory"].append(item)
        return character

    def update_alignment(self, character, alignment_change):
        """Good/Evil puanını güncelle (alignment_change: + veya -)"""
        if "good_evil" not in character:
            character["good_evil"] = 0  # 0: nötr, +: good, -: evil
        character["good_evil"] += alignment_change
        return character

    def create_character(self, name, char_class):
        """Karakter oluştur, class'a göre skill tree ekle"""
        base_stats = {
            "warrior": {"hp": 120, "attack": 85, "defense": 90, "special": 0},
            "mage": {"hp": 60, "attack": 100, "defense": 40, "special": 150},
            "rogue": {"hp": 80, "attack": 90, "defense": 60, "special": 95},
            "priest": {"hp": 70, "attack": 50, "defense": 70, "special": 80},
            # ... diğer sınıflar ...
        }
        stats = base_stats.get(char_class, {"hp": 100, "attack": 50, "defense": 50, "special": 0})
        skills = [dict(skill) for skill in self.skill_trees.get(char_class, [])]
        return {
            "name": name,
            "class": char_class,
            "hp": stats["hp"],
            "attack": stats["attack"],
            "defense": stats["defense"],
            "special": stats["special"],
            "xp": 0,
            "skills": skills,
            "inventory": [],
            "good_evil": 0
        }

    def combat(self, player, enemy, skill_name=None):
        """Savaş sistemi: skill kullanımı ve XP/skill açma"""
        import random
        player_hp = player.get('hp', 100)
        enemy_hp = enemy.get('hp', 100)
        combat_log = []
        skill_used = None
        # Skill kullanımı
        if skill_name:
            skill = next((s for s in player.get('skills', []) if s['name'] == skill_name and s.get('unlocked')), None)
            if skill:
                skill_used = skill
                effect = skill.get('effect')
                combat_log.append(f"Yetenek kullanıldı: {skill['name']} - {skill['description']}")
                if effect == "double_attack":
                    player_damage = max(0, (player.get('attack', 50) * 2) - enemy.get('defense', 30) + random.randint(-5, 15))
                    enemy_hp -= player_damage
                    combat_log.append(f"Berserker Strike ile {player_damage} hasar!")
                elif effect == "heal":
                    heal_amount = 40
                    player_hp += heal_amount
                    combat_log.append(f"Heal ile {heal_amount} HP yenilendi!")
                # ... diğer skill efektleri ...
        # Normal döngü
        while player_hp > 0 and enemy_hp > 0:
            player_damage = max(0, player.get('attack', 50) - enemy.get('defense', 30) + random.randint(-5, 15))
            enemy_hp -= player_damage
            combat_log.append(f"Oyuncu saldırısı: {player_damage} hasar!")
            if enemy_hp <= 0:
                combat_log.append("Düşman yenildi! Zafer!")
                xp_gained = enemy.get("xpReward", 0)
                player = self.award_xp_and_unlock_skills(player, xp_gained)
                combat_log.append(f"{xp_gained} XP kazandın!")
                unlocked_skills = [s['name'] for s in player.get('skills', []) if s.get('unlocked', False) and player['xp'] >= s['requiredXP']]
                if unlocked_skills:
                    combat_log.append(f"Açılan yetenekler: {', '.join(unlocked_skills)}")
                return {"result": "victory", "log": combat_log, "player": player}
            enemy_damage = max(0, enemy.get('attack', 50) - player.get('defense', 30) + random.randint(-5, 15))
            player_hp -= enemy_damage
            combat_log.append(f"Düşman saldırısı: {enemy_damage} hasar!")
            if player_hp <= 0:
                combat_log.append("Oyuncu yenildi! Mağlubiyet!")
                return {"result": "defeat", "log": combat_log, "player": player}
        return {"result": "draw", "log": combat_log, "player": player} 