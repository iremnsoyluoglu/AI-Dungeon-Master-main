from flask import jsonify, request, render_template
import logging

logger = logging.getLogger(__name__)

def register_routes(app, game_engine, campaign_manager, ai_dm):
    """Web route'larını kaydet"""
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/api/campaigns')
    def get_campaigns():
        """Mevcut kampanyaları listele"""
        try:
            campaigns = campaign_manager.list_campaigns()
            return jsonify({
                "success": True,
                "campaigns": campaigns
            })
        except Exception as e:
            logger.error(f"Error getting campaigns: {e}")
            return jsonify({
                "success": False,
                "error": "Kampanyalar yüklenirken hata oluştu"
            }), 500
    
    @app.route('/api/campaigns/add', methods=['POST'])
    def add_campaign():
        """Yeni kampanya ekle"""
        try:
            data = request.get_json()
            if not data or 'id' not in data:
                return jsonify({
                    "success": False,
                    "error": "Kampanya ID gerekli"
                }), 400
            
            success = campaign_manager.add_campaign(data)
            if success:
                return jsonify({
                    "success": True,
                    "message": f"Kampanya '{data.get('name', data['id'])}' eklendi"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Kampanya eklenirken hata oluştu"
                }), 500
        except Exception as e:
            logger.error(f"Error adding campaign: {e}")
            return jsonify({
                "success": False,
                "error": "Kampanya eklenirken hata oluştu"
            }), 500
    
    @app.route('/api/campaigns/remove/<campaign_id>', methods=['DELETE'])
    def remove_campaign(campaign_id):
        """Kampanya sil"""
        try:
            success = campaign_manager.remove_campaign(campaign_id)
            if success:
                return jsonify({
                    "success": True,
                    "message": f"Kampanya '{campaign_id}' silindi"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Kampanya bulunamadı"
                }), 404
        except Exception as e:
            logger.error(f"Error removing campaign {campaign_id}: {e}")
            return jsonify({
                "success": False,
                "error": "Kampanya silinirken hata oluştu"
            }), 500
    
    @app.route('/api/campaign/<campaign_id>')
    def get_campaign(campaign_id):
        """Belirli bir kampanyayı getir"""
        try:
            campaign = campaign_manager.get_campaign(campaign_id)
            if campaign:
                return jsonify({
                    "success": True,
                    "campaign": campaign
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Kampanya bulunamadı"
                }), 404
        except Exception as e:
            logger.error(f"Error getting campaign {campaign_id}: {e}")
            return jsonify({
                "success": False,
                "error": "Kampanya yüklenirken hata oluştu"
            }), 500
    
    @app.route('/api/campaign/<campaign_id>/step/<step_id>')
    def get_campaign_step(campaign_id, step_id):
        """Kampanya adımını getir"""
        try:
            step = campaign_manager.get_campaign_step(campaign_id, step_id)
            if step:
                return jsonify({
                    "success": True,
                    "step": step
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Adım bulunamadı"
                }), 404
        except Exception as e:
            logger.error(f"Error getting step {step_id} for campaign {campaign_id}: {e}")
            return jsonify({
                "success": False,
                "error": "Adım yüklenirken hata oluştu"
            }), 500

    def _hide_moral_fields(player):
        if not player:
            return player
        filtered = dict(player)
        # Tüm gizli stat ve puanları çıkar
        for key in ["good_evil", "reputation", "alignment", "relationships", "buffs", "debuffs"]:
            if key in filtered:
                del filtered[key]
        return filtered

    @app.route('/api/campaign/<campaign_id>/choice/<choice_id>', methods=['POST'])
    def get_choice_result(campaign_id, choice_id):
        """Çoklu oyuncu desteği: Her oyuncu kendi seçimini yapar, state'i güncellenir. Grup kararı gereken sahnelerde çoğunluk uygulanır."""
        try:
            data = request.get_json() or {}
            players = data.get('players', [])  # Oyuncu listesi
            group_decision = data.get('group_decision')  # Grup kararı (opsiyonel)
            # Her oyuncu için ayrı ayrı seçim uygula
            updated_players = []
            for player in players:
                result = campaign_manager.get_choice_result(campaign_id, choice_id)
                # Effect uygula (her oyuncuya ayrı)
                scenes = campaign_manager.get_campaign(campaign_id).get('scenes', [])
                effect = None
                for scene in scenes:
                    for choice in scene.get('choices', []):
                        if choice['id'] == choice_id:
                            effect = choice.get('effect')
                updated_player = player
                if effect and player:
                    updated_player = game_engine.apply_effects(player, effect)
                updated_players.append(updated_player)
            # Grup kararı gereken sahnede çoğunluğa göre karar uygula (örnek)
            if group_decision:
                # group_decision: {"choice_id": "...", "votes": {"player1": "A", "player2": "B", ...}}
                # Çoğunluğa göre next_scene belirlenebilir
                pass  # (Burada grup kararı işlenebilir)
            return jsonify({
                "success": True,
                "players": updated_players
            })
        except Exception as e:
            logger.error(f"Error getting choice result {choice_id} for campaign {campaign_id}: {e}")
            return jsonify({
                "success": False,
                "error": "Seçim sonucu alınırken hata oluştu"
            }), 500

    @app.route('/api/campaign/<campaign_id>/boss')
    def get_campaign_boss(campaign_id):
        """Kampanya boss'unu getir"""
        try:
            boss = campaign_manager.get_boss(campaign_id)
            if boss:
                return jsonify({
                    "success": True,
                    "boss": boss
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Boss bulunamadı"
                }), 404
        except Exception as e:
            logger.error(f"Error getting boss for campaign {campaign_id}: {e}")
            return jsonify({
                "success": False,
                "error": "Boss bilgisi alınırken hata oluştu"
            }), 500
    
    @app.route('/api/ai/generate', methods=['POST'])
    def generate_ai_content():
        """AI ile içerik oluştur"""
        try:
            data = request.get_json()
            content_type = data.get('type', 'story')
            prompt = data.get('prompt', '')
            context = data.get('context', {})
            
            if content_type == 'npc':
                result = ai_dm.generate_npc(prompt, context)
            elif content_type == 'location':
                result = ai_dm.generate_location(prompt, context)
            elif content_type == 'quest':
                result = ai_dm.generate_quest(prompt, context)
            else:
                result = ai_dm.run_campaign(prompt, context)
            
            return jsonify({
                "success": True,
                "content": result
            })
        except Exception as e:
            logger.error(f"Error generating AI content: {e}")
            return jsonify({
                "success": False,
                "error": "AI içerik oluşturulurken hata oluştu"
            }), 500
    
    @app.route('/api/game/roll-dice', methods=['POST'])
    def roll_dice():
        """Zar at"""
        try:
            data = request.get_json()
            dice_type = data.get('dice_type', 'd20')
            modifier = data.get('modifier', 0)
            
            result = game_engine.roll_dice(dice_type, modifier)
            
            return jsonify({
                "success": True,
                "result": result,
                "dice_type": dice_type,
                "modifier": modifier
            })
        except Exception as e:
            logger.error(f"Error rolling dice: {e}")
            return jsonify({
                "success": False,
                "error": "Zar atılırken hata oluştu"
            }), 500
    
    @app.route('/api/game/session/start', methods=['POST'])
    def start_session():
        """Oyun oturumu başlat"""
        try:
            data = request.get_json()
            campaign_id = data.get('campaign_id')
            players = data.get('players', [])
            
            if not campaign_id:
                return jsonify({
                    "success": False,
                    "error": "Kampanya ID gerekli"
                }), 400
            
            session = game_engine.start_session(campaign_id, players)
            
            return jsonify({
                "success": True,
                "session": session
            })
        except Exception as e:
            logger.error(f"Error starting session: {e}")
            return jsonify({
                "success": False,
                "error": "Oturum başlatılırken hata oluştu"
            }), 500
    
    @app.route('/api/game/session/state')
    def get_session_state():
        """Mevcut oturum durumunu getir"""
        try:
            state = game_engine.get_session_state()
            return jsonify({
                "success": True,
                "state": state
            })
        except Exception as e:
            logger.error(f"Error getting session state: {e}")
            return jsonify({
                "success": False,
                "error": "Oturum durumu alınırken hata oluştu"
            }), 500
    
    @app.route('/api/game/session/update', methods=['POST'])
    def update_session():
        """Oturum durumunu güncelle"""
        try:
            data = request.get_json()
            step_id = data.get('step_id')
            update_data = data.get('data', {})
            
            if not step_id:
                return jsonify({
                    "success": False,
                    "error": "Adım ID gerekli"
                }), 400
            
            game_engine.update_session(step_id, update_data)
            
            return jsonify({
                "success": True,
                "message": "Oturum güncellendi"
            })
        except Exception as e:
            logger.error(f"Error updating session: {e}")
            return jsonify({
                "success": False,
                "error": "Oturum güncellenirken hata oluştu"
            }), 500
    
    @app.route('/api/game/session/end', methods=['POST'])
    def end_session():
        """Oturumu sonlandır"""
        try:
            game_engine.end_session()
            return jsonify({
                "success": True,
                "message": "Oturum sonlandırıldı"
            })
        except Exception as e:
            logger.error(f"Error ending session: {e}")
            return jsonify({
                "success": False,
                "error": "Oturum sonlandırılırken hata oluştu"
            }), 500
    
    @app.route('/api/ai/history')
    def get_ai_history():
        """AI konuşma geçmişini getir"""
        try:
            history = ai_dm.get_conversation_history()
            return jsonify({
                "success": True,
                "history": history
            })
        except Exception as e:
            logger.error(f"Error getting AI history: {e}")
            return jsonify({
                "success": False,
                "error": "AI geçmişi alınırken hata oluştu"
            }), 500
    
    @app.route('/api/ai/history/clear', methods=['POST'])
    def clear_ai_history():
        """AI konuşma geçmişini temizle"""
        try:
            ai_dm.clear_history()
            return jsonify({
                "success": True,
                "message": "AI geçmişi temizlendi"
            })
        except Exception as e:
            logger.error(f"Error clearing AI history: {e}")
            return jsonify({
                "success": False,
                "error": "AI geçmişi temizlenirken hata oluştu"
            }), 500
    
    @app.route('/api/game/battle', methods=['POST'])
    def battle():
        """Karakter ile düşman arasında savaş başlat, XP ve skill güncelle"""
        try:
            data = request.get_json()
            player = data.get('player')  # dict: karakter
            enemy_name = data.get('enemy_name')  # string: düşman adı
            if not player or not enemy_name:
                return jsonify({
                    "success": False,
                    "error": "Karakter ve düşman adı gerekli"
                }), 400
            enemy = game_engine.get_enemy(enemy_name)
            if not enemy:
                return jsonify({
                    "success": False,
                    "error": f"Düşman bulunamadı: {enemy_name}"
                }), 404
            result = game_engine.combat(player, enemy)
            return jsonify({
                "success": True,
                "battle_result": result["result"],
                "log": result["log"],
                "player": result["player"]
            })
        except Exception as e:
            logger.error(f"Error in battle: {e}")
            return jsonify({
                "success": False,
                "error": "Savaş sırasında hata oluştu"
            }), 500
    
    @app.route('/api/game/battle/turn', methods=['POST'])
    def battle_turn():
        """Tur bazlı dövüş: Her turda oyuncu bir skill seçer, sonuçlar ve yeni combat_state döner. Sonuç victory ise uygun sona yönlendir."""
        try:
            data = request.get_json() or {}
            player = data.get('player')
            enemy = data.get('enemy')
            skill_name = data.get('skill_name')
            combat_state = data.get('combat_state')
            npc_ally = data.get('npc_ally')  # Yardımcı NPC (Brakk, Forest Fairy, None)
            if not player or not enemy or not skill_name:
                return jsonify({
                    "success": False,
                    "error": "player, enemy ve skill_name zorunlu."
                }), 400
            result = game_engine.combat_turn(player, enemy, skill_name, combat_state)
            # Sona yönlendirme
            ending_scene = None
            if result["result"] == "victory":
                # Pyraxis'e katılım ayrı endpointte, burada sadece savaş sonucu
                if npc_ally == "Brakk":
                    ending_scene = "victory_evil"
                elif npc_ally == "Forest Fairy":
                    ending_scene = "victory_good_fairy"
                else:
                    # Oyuncunun good_evil puanına bakarak nötr/kötü ayrımı
                    ge = player.get('good_evil', 0)
                    if ge < 0:
                        ending_scene = "victory_evil"
                    elif ge > 0:
                        ending_scene = "victory_good_fairy"
                    else:
                        ending_scene = "victory_neutral"
            elif result["result"] == "defeat":
                ending_scene = "game_over"
            return jsonify({
                "success": True,
                "result": result["result"],
                "log": result["log"],
                "combat_state": result["combat_state"],
                "ending_scene": ending_scene
            })
        except Exception as e:
            logger.error(f"Error in battle turn: {e}")
            return jsonify({
                "success": False,
                "error": "Dövüş turu sırasında hata oluştu"
            }), 500
    
    @app.route('/api/game/npc-interact', methods=['POST'])
    def npc_interact():
        """NPC ile ilişki kur, ödül/potion ver, alignment güncelle"""
        data = request.get_json()
        player = data.get('player')
        npc = data.get('npc')  # ör: {"name": "Elder Varn", "type": "good"}
        choice = data.get('choice')  # oyuncunun seçimi
        # Good/Evil alignment güncelle
        alignment_change = 0
        item_reward = None
        message = ""
        if npc and npc.get('type') == 'good':
            if choice == 'help' or choice == 'save':
                alignment_change = 5
                item_reward = {"name": "Potion of Healing", "type": "potion", "heal": 15, "usable": True}
                message = f"{npc['name']} sana bir iyileştirme iksiri verdi!"
            elif choice == 'betray' or choice == 'rob':
                alignment_change = -5
                message = f"{npc['name']} ile ilişkin bozuldu."
            else:
                message = f"{npc['name']} ile nötr bir etkileşim gerçekleşti."
        elif npc and npc.get('type') == 'evil':
            if player.get('good_evil', 0) < 0:
                # Evil storyline: özel ödül
                item_reward = {"name": "Shadow Elixir", "type": "potion", "heal": 30, "usable": True}
                alignment_change = -5
                message = f"{npc['name']} sana karanlık bir iksir verdi!"
            else:
                message = f"{npc['name']} seni küçümsedi."
        else:
            message = "NPC ile etkileşim gerçekleşti."
        # Alignment güncelle
        player['good_evil'] = player.get('good_evil', 0) + alignment_change
        # Envanter güncelle
        if item_reward:
            if 'inventory' not in player:
                player['inventory'] = []
            player['inventory'].append(item_reward)
        return jsonify({
            "success": True,
            "message": message,
            "alignment": player['good_evil'],
            "inventory": player.get('inventory', []),
            "player": player
        })
    
    @app.route('/api/game/use-item', methods=['POST'])
    def use_item():
        """Envanterdeki potion/eşya kullanımı"""
        data = request.get_json()
        item = data.get('item')
        index = data.get('index')
        # Karakteri session'dan veya request'ten al (örnek: tek oyunculu için basit)
        # Burada örnek olarak session'daki ilk karakteri alıyoruz
        session = getattr(game_engine, 'current_session', None)
        if not session or not session.get('characters'):
            return jsonify({"success": False, "error": "Oyun oturumu veya karakter bulunamadı"}), 400
        character = session['characters'][0]
        inventory = character.get('inventory', [])
        if not inventory or index is None or index >= len(inventory):
            return jsonify({"success": False, "error": "Geçersiz envanter veya indeks"}), 400
        used_item = inventory.pop(index)
        message = f"{used_item.get('name', str(used_item))} kullanıldı."
        # Basit efekt: Potion ise HP artır
        if used_item.get('type') == 'potion':
            heal = used_item.get('heal', 10)
            character['hp'] = character.get('hp', 20) + heal
            message += f" HP +{heal}!"
        # Diğer eşya türleri için buraya eklenebilir
        character['inventory'] = inventory
        return jsonify({
            "success": True,
            "message": message,
            "inventory": inventory,
            "character": character
        })
    
    @app.route('/api/game/skill/unlock', methods=['POST'])
    def unlock_skill():
        """XP ile yeni skill açar."""
        try:
            data = request.get_json() or {}
            player = data.get('player')
            skill_name = data.get('skill_name')
            if not player or not skill_name:
                return jsonify({"success": False, "error": "player ve skill_name zorunlu."}), 400
            ok = game_engine.unlock_skill(player, skill_name)
            return jsonify({
                "success": ok,
                "player": player,
                "message": "Skill açıldı." if ok else "Skill açılamadı. XP yetersiz veya zaten açık."
            })
        except Exception as e:
            logger.error(f"Error unlocking skill: {e}")
            return jsonify({"success": False, "error": "Skill açılırken hata oluştu"}), 500

    @app.route('/api/game/skill/upgrade', methods=['POST'])
    def upgrade_skill():
        """XP ile skill seviyesini yükseltir."""
        try:
            data = request.get_json() or {}
            player = data.get('player')
            skill_name = data.get('skill_name')
            if not player or not skill_name:
                return jsonify({"success": False, "error": "player ve skill_name zorunlu."}), 400
            ok = game_engine.upgrade_skill(player, skill_name)
            return jsonify({
                "success": ok,
                "player": player,
                "message": "Skill seviyesi yükseltildi." if ok else "Skill yükseltilemedi. XP yetersiz veya maksimum seviyede."
            })
        except Exception as e:
            logger.error(f"Error upgrading skill: {e}")
            return jsonify({"success": False, "error": "Skill yükseltilirken hata oluştu"}), 500
    
    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'healthy', 'version': '1.0.0'})
    
    logger.info("Web routes registered successfully") 