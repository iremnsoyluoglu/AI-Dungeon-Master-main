import random
import logging

logger = logging.getLogger(__name__)

# Eşya işlevleri sözlüğü (kısa açıklama ve işlev)
ITEM_FUNCTIONS = {
    "healing_potion": {"desc": "Kullanıldığında 30 HP yeniler.", "use": lambda p: p.update({"hp": p.get("hp", 0) + 30})},
    "apple": {"desc": "Kullanıldığında 5 HP yeniler.", "use": lambda p: p.update({"hp": p.get("hp", 0) + 5})},
    "mushroom": {"desc": "Kullanıldığında 3 HP yeniler veya bir bulmacada kullanılabilir.", "use": lambda p: p.update({"hp": p.get("hp", 0) + 3})},
    "old_stone": {"desc": "Bir NPC'ye verildiğinde gizli bir kapı açar.", "use": None},
    "clue_scroll": {"desc": "Bir bulmacada ipucu verir.", "use": None},
    "herbs": {"desc": "İksir yapımında kullanılır.", "use": None},
    "special_sword": {"desc": "Savaşta saldırı gücünü artırır.", "use": None},
    "ancient_map": {"desc": "Gizli bir bölgeyi açar.", "use": None},
    "magic_ring": {"desc": "Pyraxis'e karşı koruma sağlar.", "use": None},
    "holy_shield": {"desc": "Pyraxis'e karşı koruma sağlar.", "use": None},
    "mysterious_potion": {"desc": "Kullanıldığında rastgele bir buff verir.", "use": None},
    "random_loot": {"desc": "Kullanıldığında rastgele bir eşya verir.", "use": None},
    "charm_of_gratitude": {"desc": "NPC'lerle etkileşimde bonus sağlar.", "use": None},
    "spellbook": {"desc": "Yeni bir büyü öğrenmeni sağlar.", "use": None},
    # ... diğer eşyalar ...
}

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
        # Skill ağacı örneği (her class için, seviye ve upgrade destekli)
        # self.skill_trees güncellendi
        self.skill_trees = {
            "warrior": [
                {"name": "Slash", "description": "Düz saldırı", "requiredXP": 0, "unlocked": True, "level": 1, "max_level": 3, "effect": "attack", "upgrade_effect": "attack+"},
                {"name": "Shield Bash", "description": "Rakibi sersemletir", "requiredXP": 10, "unlocked": False, "level": 0, "max_level": 2, "effect": "stun", "upgrade_effect": "stun+"},
                {"name": "Battle Cry", "description": "Takıma saldırı buff'u", "requiredXP": 20, "unlocked": False, "level": 0, "max_level": 2, "effect": "team_buff", "upgrade_effect": "team_buff+"},
                {"name": "Wrath of Titans", "description": "Ultimate: Devasa güçle saldırı", "requiredXP": 40, "unlocked": False, "level": 0, "max_level": 1, "effect": "ultimate_warrior", "upgrade_effect": None}
            ],
            "mage": [
                {"name": "Fire Bolt", "description": "Ateşli büyü saldırısı", "requiredXP": 0, "unlocked": True, "level": 1, "max_level": 3, "effect": "fire_attack", "upgrade_effect": "fire_attack+"},
                {"name": "Arcane Shield", "description": "2 tur büyü kalkanı", "requiredXP": 10, "unlocked": False, "level": 0, "max_level": 2, "effect": "magic_shield", "upgrade_effect": "magic_shield+"},
                {"name": "Mana Burn", "description": "Rakibin manasını yakar", "requiredXP": 20, "unlocked": False, "level": 0, "max_level": 2, "effect": "mana_burn", "upgrade_effect": "mana_burn+"},
                {"name": "Meteor Storm", "description": "Ultimate: Tüm düşmanlara dev hasar", "requiredXP": 40, "unlocked": False, "level": 0, "max_level": 1, "effect": "ultimate_mage", "upgrade_effect": None}
            ],
            "rogue": [
                {"name": "Backstab", "description": "Kritik gizli saldırı", "requiredXP": 0, "unlocked": True, "level": 1, "max_level": 3, "effect": "crit_attack", "upgrade_effect": "crit_attack+"},
                {"name": "Smoke Bomb", "description": "Kaçma şansı yaratır", "requiredXP": 10, "unlocked": False, "level": 0, "max_level": 2, "effect": "escape", "upgrade_effect": "escape+"},
                {"name": "Poison Blade", "description": "3 tur zehir etkisi", "requiredXP": 20, "unlocked": False, "level": 0, "max_level": 2, "effect": "poison", "upgrade_effect": "poison+"},
                {"name": "Death Dance", "description": "Ultimate: Çoklu hızlı saldırı", "requiredXP": 40, "unlocked": False, "level": 0, "max_level": 1, "effect": "ultimate_rogue", "upgrade_effect": None}
            ],
            "priest": [
                {"name": "Heal", "description": "Can yeniler", "requiredXP": 0, "unlocked": True, "level": 1, "max_level": 3, "effect": "heal", "upgrade_effect": "heal+"},
                {"name": "Holy Fire", "description": "Kutsal ateş saldırısı", "requiredXP": 10, "unlocked": False, "level": 0, "max_level": 2, "effect": "holy_fire", "upgrade_effect": "holy_fire+"},
                {"name": "Curse Cleanse", "description": "Laneti temizler", "requiredXP": 20, "unlocked": False, "level": 0, "max_level": 2, "effect": "cleanse", "upgrade_effect": "cleanse+"},
                {"name": "Divine Judgment", "description": "Ultimate: İlahi yargı saldırısı", "requiredXP": 40, "unlocked": False, "level": 0, "max_level": 1, "effect": "ultimate_priest", "upgrade_effect": None}
            ],
            "space_marine": [
                {"name": "Plasma Shot", "description": "Plazma silahı saldırısı", "requiredXP": 0, "unlocked": True, "level": 1, "max_level": 3, "effect": "plasma_attack", "upgrade_effect": "plasma_attack+"},
                {"name": "Suppressive Fire", "description": "Düşmanı bastırır", "requiredXP": 10, "unlocked": False, "level": 0, "max_level": 2, "effect": "suppress", "upgrade_effect": "suppress+"},
                {"name": "Cover Maneuver", "description": "Savunma pozisyonu", "requiredXP": 20, "unlocked": False, "level": 0, "max_level": 2, "effect": "cover", "upgrade_effect": "cover+"},
                {"name": "Orbital Strike", "description": "Ultimate: Yörüngeden bombardıman", "requiredXP": 40, "unlocked": False, "level": 0, "max_level": 1, "effect": "ultimate_space_marine", "upgrade_effect": None}
            ],
            "tech_priest": [
                {"name": "Servo Skull Hack", "description": "Düşman mekaniklerini hackler", "requiredXP": 0, "unlocked": True, "level": 1, "max_level": 3, "effect": "hack", "upgrade_effect": "hack+"},
                {"name": "Power Surge", "description": "Enerji patlaması", "requiredXP": 10, "unlocked": False, "level": 0, "max_level": 2, "effect": "power_surge", "upgrade_effect": "power_surge+"},
                {"name": "Shield Reboot", "description": "Kalkanı yeniler", "requiredXP": 20, "unlocked": False, "level": 0, "max_level": 2, "effect": "shield_reboot", "upgrade_effect": "shield_reboot+"},
                {"name": "Techno-Realm Overload", "description": "Ultimate: Tüm teknolojik düşmanlara dev hasar", "requiredXP": 40, "unlocked": False, "level": 0, "max_level": 1, "effect": "ultimate_tech_priest", "upgrade_effect": None}
            ],
            "inquisitor": [
                {"name": "Mind Probe", "description": "Zihin okuma", "requiredXP": 0, "unlocked": True, "level": 1, "max_level": 3, "effect": "mind_probe", "upgrade_effect": "mind_probe+"},
                {"name": "Heretic Burn", "description": "Kafir yakma saldırısı", "requiredXP": 10, "unlocked": False, "level": 0, "max_level": 2, "effect": "heretic_burn", "upgrade_effect": "heretic_burn+"},
                {"name": "Interrogate", "description": "Bilgi toplama", "requiredXP": 20, "unlocked": False, "level": 0, "max_level": 2, "effect": "interrogate", "upgrade_effect": "interrogate+"},
                {"name": "Emperor's Wrath", "description": "Ultimate: İmparator'un gazabı", "requiredXP": 40, "unlocked": False, "level": 0, "max_level": 1, "effect": "ultimate_inquisitor", "upgrade_effect": None}
            ],
            "imperial_guard": [
                {"name": "Frag Grenade", "description": "El bombası saldırısı", "requiredXP": 0, "unlocked": True, "level": 1, "max_level": 3, "effect": "grenade", "upgrade_effect": "grenade+"},
                {"name": "Tactical Advance", "description": "Taktiksel ilerleme, savunma artar", "requiredXP": 10, "unlocked": False, "level": 0, "max_level": 2, "effect": "tactical_advance", "upgrade_effect": "tactical_advance+"},
                {"name": "Rally Troops", "description": "Takımı güçlendirir", "requiredXP": 20, "unlocked": False, "level": 0, "max_level": 2, "effect": "rally", "upgrade_effect": "rally+"},
                {"name": "Regimental Fury", "description": "Ultimate: Alay öfkesiyle dev saldırı", "requiredXP": 40, "unlocked": False, "level": 0, "max_level": 1, "effect": "ultimate_imperial_guard", "upgrade_effect": None}
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
                enemy_copy = enemy.copy()
                # Boss ve özel yaratıklar için skill listesi ekle
                if name.lower() == "pyraxis":
                    enemy_copy["skills"] = [
                        {"name": "Fire Breath", "description": "Alev püskürtür", "effect": "fire_breath"},
                        {"name": "Claw Swipe", "description": "Pençe saldırısı", "effect": "claw_swipe"},
                        {"name": "Tail Whip", "description": "Kuyruk darbesi", "effect": "tail_whip"},
                        {"name": "Roar", "description": "Kükreyerek korkutur", "effect": "roar"}
                    ]
                elif name.lower() == "brakk":
                    enemy_copy["skills"] = [
                        {"name": "Berserk", "description": "Çılgın saldırı", "effect": "berserk"},
                        {"name": "Smash", "description": "Güçlü darbe", "effect": "smash"}
                    ]
                # ... diğer boss/yaratıklar için skill eklenebilir ...
                return enemy_copy
        return None

    def enemy_choose_skill(self, enemy, combat_state=None):
        """AI ile boss/yaratık skill seçimi. (Basit: rastgele, gelişmiş: HP'ye göre)"""
        import random
        skills = enemy.get("skills", [])
        if not skills:
            return None
        # Örnek: Eğer HP düşükse savunma/kaçış skill'i, yoksa rastgele saldırı
        if combat_state and enemy.get('hp', 100) < 0.3 * enemy.get('max_hp', 100):
            for s in skills:
                if "defense" in s["effect"] or "heal" in s["effect"]:
                    return s["name"]
        # Aksi halde rastgele skill
        return random.choice(skills)["name"]

    def award_xp_and_unlock_skills(self, character, xp_gained):
        """Karaktere XP ekle ve skill aç"""
        character["xp"] = character.get("xp", 0) + xp_gained
        for skill in character.get("skills", []):
            if not skill.get("unlocked", False) and character["xp"] >= skill["requiredXP"]:
                skill["unlocked"] = True
        return character

    def add_item_to_inventory(self, character, item):
        """Karakterin envanterine eşya ekle, açıklama ekle"""
        if "inventory" not in character:
            character["inventory"] = []
        character["inventory"].append(item)
        # Eşya açıklamasını da ekle (isteğe bağlı)
        if "item_descriptions" not in character:
            character["item_descriptions"] = {}
        desc = ITEM_FUNCTIONS.get(item, {}).get("desc", "Koleksiyon eşyası.")
        character["item_descriptions"][item] = desc
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

    def combat_turn(self, players, enemies, action, combat_state=None):
        """
        Multiplayer destekli gelişmiş dövüş sistemi.
        - players: oyuncu karakter dict listesi
        - enemies: düşman(lar) dict listesi
        - action: {"actor": "player1"/"enemy1"/..., "type": ..., "skill_name": ..., "target": ...}
        - combat_state: dövüş durumu dict
        """
        import random
        num_players = len(players)
        num_enemies = len(enemies)
        # Düşmanları oyuncu sayısına göre güçlendir
        for e in enemies:
            e["hp"] = int(e.get("base_hp", e.get("hp", 100)) * (1 + 0.5 * (num_players-1)))
            e["attack"] = int(e.get("base_attack", e.get("attack", 40)) * (1 + 0.3 * (num_players-1)))
            e["defense"] = int(e.get("base_defense", e.get("defense", 20)) * (1 + 0.2 * (num_players-1)))
        # Combat state başlat
        if not combat_state:
            combat_state = {
                "initiative_order": [f"player{i+1}" for i in range(num_players)] + [f"enemy{i+1}" for i in range(num_enemies)],
                "positions": {**{f"player{i+1}": "front" for i in range(num_players)}, **{f"enemy{i+1}": "front" for i in range(num_enemies)}},
                "movement_points": {**{f"player{i+1}": 2 for i in range(num_players)}, **{f"enemy{i+1}": 1 for i in range(num_enemies)}},
                **{f"player{i+1}_hp": p.get("hp", 100) for i, p in enumerate(players)},
                **{f"enemy{i+1}_hp": e.get("hp", 100) for i, e in enumerate(enemies)},
                "turn": 1,
                "log": [],
                "player_buffs": {f"player{i+1}": [] for i in range(num_players)},
                "enemy_buffs": {f"enemy{i+1}": [] for i in range(num_enemies)},
                "player_cooldowns": {f"player{i+1}": {} for i in range(num_players)},
                "enemy_cooldowns": {f"enemy{i+1}": {} for i in range(num_enemies)},
                "player_dot": {f"player{i+1}": {} for i in range(num_players)},
                "enemy_dot": {f"enemy{i+1}": {} for i in range(num_enemies)},
                "element_weakness": {f"enemy{i+1}": e.get("element_weakness") for i, e in enumerate(enemies)},
                "player_crit": {f"player{i+1}": 0.1 for i in range(num_players)},
                "enemy_crit": {f"enemy{i+1}": 0.05 for i in range(num_enemies)},
            }
        log = combat_state["log"]
        order = combat_state["initiative_order"]
        current = order[(combat_state["turn"]-1) % len(order)]
        # --- Aktörün turu ---
        if current.startswith("player"):
            idx = int(current.replace("player", "")) - 1
            player = players[idx]
            # Hareket puanı kontrolü
            if action.get("type") == "move":
                if combat_state["movement_points"][current] > 0:
                    combat_state["positions"][current] = action.get("to", "front")
                    combat_state["movement_points"][current] -= 1
                    log.append(f"{current} pozisyonunu {combat_state['positions'][current]} yaptı.")
                else:
                    log.append("Hareket puanın yok!")
            elif action.get("type") == "defend":
                combat_state["player_buffs"][current].append({"type": "defend", "turns": 1})
                log.append(f"{current} savunmaya geçti, bu tur alınan hasar yarıya inecek.")
            elif action.get("type") == "delay_turn":
                log.append(f"{current} turunu erteledi.")
                order.append(order.pop(0))
            elif action.get("type") in ["attack", "skill"]:
                skill = None
                if action.get("type") == "skill":
                    for s in player.get("skills", []):
                        if s["name"] == action.get("skill_name") and s.get("unlocked", True):
                            skill = s
                            break
                target = action.get("target", "enemy1")
                if target not in [f"enemy{i+1}" for i in range(num_enemies)]:
                    target = "enemy1"
                crit = random.random() < (combat_state["player_crit"][current] + (0.2 if combat_state["positions"][target] == "back" else 0))
                element = skill.get("element") if skill else None
                weak = element and combat_state["element_weakness"].get(target) == element
                # Zar atarak saldırı gücü belirle
                attack_roll = self.roll_dice("d20") + player.get('attack', 50)
                defense_roll = self.roll_dice("d20") + enemies[int(target.replace("enemy", ""))-1].get('defense', 30)
                base_dmg = max(0, attack_roll - defense_roll)
                if weak:
                    base_dmg += 20
                if crit:
                    base_dmg = int(base_dmg * 1.5)
                if skill and skill.get("aoe"):
                    for i in range(num_enemies):
                        t = f"enemy{i+1}"
                        aoe_attack = self.roll_dice("d20") + player.get('attack', 50)
                        aoe_defense = self.roll_dice("d20") + enemies[i].get('defense', 30)
                        aoe_dmg = max(0, aoe_attack - aoe_defense)
                        if crit:
                            aoe_dmg = int(aoe_dmg * 1.5)
                        combat_state[f"{t}_hp"] -= aoe_dmg
                        log.append(f"AoE: {t} {aoe_dmg} hasar aldı! (Saldırı zar: {aoe_attack}, Savunma zar: {aoe_defense}){' (kritik!)' if crit else ''}")
                elif skill and skill.get("effect") == "combo":
                    hits = 3
                    for h in range(hits):
                        combo_attack = self.roll_dice("d20") + player.get('attack', 50) // 2
                        combo_defense = self.roll_dice("d20") + enemies[int(target.replace("enemy", ""))-1].get('defense', 30)
                        combo_dmg = max(0, combo_attack - combo_defense)
                        combat_state[f"{target}_hp"] -= combo_dmg
                        log.append(f"Combo zinciri: {target} {combo_dmg} hasar aldı! (Saldırı zar: {combo_attack}, Savunma zar: {combo_defense})")
                elif skill and skill.get("effect") == "heavy_attack":
                    heavy_attack = self.roll_dice("d20") + player.get('attack', 50) * 2
                    heavy_defense = self.roll_dice("d20") + enemies[int(target.replace("enemy", ""))-1].get('defense', 30)
                    heavy_dmg = max(0, heavy_attack - heavy_defense)
                    combat_state[f"{target}_hp"] -= heavy_dmg
                    log.append(f"Ağır saldırı: {target} {heavy_dmg} hasar aldı! (Saldırı zar: {heavy_attack}, Savunma zar: {heavy_defense}) Sonraki tur bekleme süresi.")
                    combat_state["player_cooldowns"][current][skill["name"]] = 1
                else:
                    combat_state[f"{target}_hp"] -= base_dmg
                    log.append(f"{target} {base_dmg} hasar aldı! (Saldırı zar: {attack_roll}, Savunma zar: {defense_roll}){' (kritik!)' if crit else ''}")
        else:
            idx = int(current.replace("enemy", "")) - 1
            enemy = enemies[idx]
            skill_name = self.enemy_choose_skill(enemy, combat_state)
            skill = None
            for s in enemy.get("skills", []):
                if s["name"] == skill_name:
                    skill = s
                    break
            target = f"player{random.randint(1, num_players)}"
            crit = random.random() < combat_state["enemy_crit"][current]
            element = skill.get("element") if skill else None
            weak = element and players[int(target.replace("player", ""))-1].get("element_weakness") == element
            # Zar atarak saldırı gücü belirle
            attack_roll = self.roll_dice("d20") + enemy.get('attack', 40)
            defense_roll = self.roll_dice("d20") + players[int(target.replace("player", ""))-1].get('defense', 30)
            base_dmg = max(0, attack_roll - defense_roll)
            if weak:
                base_dmg += 20
            if crit:
                base_dmg = int(base_dmg * 1.5)
            if skill and skill.get("aoe"):
                for i in range(num_players):
                    t = f"player{i+1}"
                    aoe_attack = self.roll_dice("d20") + enemy.get('attack', 40)
                    aoe_defense = self.roll_dice("d20") + players[i].get('defense', 30)
                    aoe_dmg = max(0, aoe_attack - aoe_defense)
                    if crit:
                        aoe_dmg = int(aoe_dmg * 1.5)
                    combat_state[f"{t}_hp"] -= aoe_dmg
                    log.append(f"Düşman AoE saldırısı: {t} {aoe_dmg} hasar aldı! (Saldırı zar: {aoe_attack}, Savunma zar: {aoe_defense}){' (kritik!)' if crit else ''}")
            elif skill and skill.get("effect") == "combo":
                hits = 2
                for h in range(hits):
                    combo_attack = self.roll_dice("d20") + enemy.get('attack', 40) // 2
                    combo_defense = self.roll_dice("d20") + players[int(target.replace("player", ""))-1].get('defense', 30)
                    combo_dmg = max(0, combo_attack - combo_defense)
                    combat_state[f"{target}_hp"] -= combo_dmg
                    log.append(f"Düşman combo zinciri: {target} {combo_dmg} hasar aldı! (Saldırı zar: {combo_attack}, Savunma zar: {combo_defense})")
            elif skill and skill.get("effect") == "heavy_attack":
                heavy_attack = self.roll_dice("d20") + enemy.get('attack', 40) * 2
                heavy_defense = self.roll_dice("d20") + players[int(target.replace("player", ""))-1].get('defense', 30)
                heavy_dmg = max(0, heavy_attack - heavy_defense)
                combat_state[f"{target}_hp"] -= heavy_dmg
                log.append(f"Düşman ağır saldırı: {target} {heavy_dmg} hasar aldı! (Saldırı zar: {heavy_attack}, Savunma zar: {heavy_defense}) Sonraki tur bekleme süresi.")
                combat_state["enemy_cooldowns"][current][skill["name"]] = 1
            else:
                combat_state[f"{target}_hp"] -= base_dmg
                log.append(f"Düşman {current} saldırısı: {target} {base_dmg} hasar aldı! (Saldırı zar: {attack_roll}, Savunma zar: {defense_roll}){' (kritik!)' if crit else ''}")
        combat_state["turn"] += 1
        # Savaş sonu kontrolü
        for i in range(num_players):
            if combat_state[f"player{i+1}_hp"] > 0:
                break
        else:
            log.append("Tüm oyuncular yenildi! Mağlubiyet!")
            return {"result": "defeat", "log": log, "combat_state": combat_state}
        for i in range(num_enemies):
            if combat_state[f"enemy{i+1}_hp"] > 0:
                break
        else:
            log.append("Tüm düşmanlar yenildi! Zafer!")
            return {"result": "victory", "log": log, "combat_state": combat_state}
        return {"result": "in_progress", "log": log, "combat_state": combat_state}

    def apply_effects(self, player, effect_string):
        """
        Sahne seçimlerindeki effect stringini parse edip oyuncuya uygular.
        Desteklenen efektler:
        - gain_xp:NN
        - lose_xp:NN
        - gain_gold:NN
        - lose_gold:NN
        - gain_hp:NN
        - lose_hp:NN
        - item:isim (veya item:magic_ring)
        - buff:attack_up (geçici saldırı artışı, player['buffs'] listesine eklenir)
        - debuff:poisoned (zehirlenme, player['debuffs'] listesine eklenir)
        - reputation:+N veya reputation:-N (ün puanı, player['reputation'] içinde tutulur)
        - relationship:NPC:delta (ör: relationship:Eloria:+5, player['relationships']['Eloria'] += 5)
        - no_change (hiçbir şey yapmaz)
        Birden fazla efekt virgül ile ayrılır.
        """
        if not effect_string or effect_string.strip() == "no_change":
            return player
        effects = [e.strip() for e in effect_string.split(',')]
        for eff in effects:
            if eff.startswith("gain_xp:"):
                try:
                    xp = int(eff.split(":")[1])
                    player = self.award_xp_and_unlock_skills(player, xp)
                except Exception:
                    pass
            elif eff.startswith("lose_xp:"):
                try:
                    xp = int(eff.split(":")[1])
                    player["xp"] = max(0, player.get("xp", 0) - xp)
                except Exception:
                    pass
            elif eff.startswith("gain_gold:"):
                try:
                    gold = int(eff.split(":")[1])
                    player["gold"] = player.get("gold", 0) + gold
                except Exception:
                    pass
            elif eff.startswith("lose_gold:"):
                try:
                    gold = int(eff.split(":")[1])
                    player["gold"] = max(0, player.get("gold", 0) - gold)
                except Exception:
                    pass
            elif eff.startswith("gain_hp:"):
                try:
                    hp = int(eff.split(":")[1])
                    player["hp"] = player.get("hp", 0) + hp
                except Exception:
                    pass
            elif eff.startswith("lose_hp:"):
                try:
                    hp = int(eff.split(":")[1])
                    player["hp"] = max(0, player.get("hp", 0) - hp)
                except Exception:
                    pass
            elif eff.startswith("item:"):
                item_name = eff.split(":")[1]
                self.add_item_to_inventory(player, item_name)
            elif eff.startswith("buff:"):
                buff = eff.split(":")[1]
                if "buffs" not in player:
                    player["buffs"] = []
                player["buffs"].append(buff)
            elif eff.startswith("debuff:"):
                debuff = eff.split(":")[1]
                if "debuffs" not in player:
                    player["debuffs"] = []
                player["debuffs"].append(debuff)
            elif eff.startswith("reputation:"):
                try:
                    rep = int(eff.split(":")[1])
                    player["reputation"] = player.get("reputation", 0) + rep
                except Exception:
                    pass
            elif eff.startswith("relationship:"):
                # relationship:NPC:delta
                try:
                    _, npc, delta = eff.split(":")
                    delta = int(delta)
                    if "relationships" not in player:
                        player["relationships"] = {}
                    player["relationships"][npc] = player["relationships"].get(npc, 0) + delta
                except Exception:
                    pass
            # İleride başka efektler eklenebilir
        return player 

    def unlock_skill(self, player, skill_name):
        """XP ile yeni skill açar."""
        for skill in player.get("skills", []):
            if skill["name"] == skill_name and not skill["unlocked"] and player["xp"] >= skill["requiredXP"]:
                skill["unlocked"] = True
                skill["level"] = 1
                return True
        return False

    def upgrade_skill(self, player, skill_name):
        """XP ile skill seviyesini yükseltir."""
        for skill in player.get("skills", []):
            if skill["name"] == skill_name and skill["unlocked"] and skill["level"] < skill["max_level"]:
                # Upgrade için XP maliyeti: (level+1)*10
                xp_cost = (skill["level"]+1)*10
                if player["xp"] >= xp_cost:
                    player["xp"] -= xp_cost
                    skill["level"] += 1
                    # Upgrade efektini uygula (isteğe bağlı)
                    if skill["upgrade_effect"]:
                        skill["effect"] = skill["upgrade_effect"]
                    return True
        return False 