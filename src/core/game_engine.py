import random
import logging

logger = logging.getLogger(__name__)

class GameEngine:
    def __init__(self):
        self.active = True
        self.current_session = None
        self.dice_history = []
        
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
    
    def combat(self, player, enemy):
        """Basit savaş sistemi"""
        import random
        
        player_hp = player.get('hp', 100)
        enemy_hp = enemy.get('hp', 100)
        
        combat_log = []
        
        while player_hp > 0 and enemy_hp > 0:
            # Oyuncu saldırısı
            player_damage = max(0, player.get('attack', 50) - enemy.get('defense', 30) + random.randint(-5, 15))
            enemy_hp -= player_damage
            combat_log.append(f"Oyuncu saldırısı: {player_damage} hasar!")
            
            if enemy_hp <= 0:
                combat_log.append("Düşman yenildi! Zafer!")
                return {"result": "victory", "log": combat_log}
            
            # Düşman saldırısı
            enemy_damage = max(0, enemy.get('attack', 50) - player.get('defense', 30) + random.randint(-5, 15))
            player_hp -= enemy_damage
            combat_log.append(f"Düşman saldırısı: {enemy_damage} hasar!")
            
            if player_hp <= 0:
                combat_log.append("Oyuncu yenildi! Mağlubiyet!")
                return {"result": "defeat", "log": combat_log}
        
        return {"result": "draw", "log": combat_log} 