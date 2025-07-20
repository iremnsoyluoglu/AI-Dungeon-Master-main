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

    @app.route('/api/campaign/<campaign_id>/choice/<choice_id>')
    def get_choice_result(campaign_id, choice_id):
        """Seçim sonucunu getir"""
        try:
            result = campaign_manager.get_choice_result(campaign_id, choice_id)
            if result:
                return jsonify({
                    "success": True,
                    "result": result
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Seçim sonucu bulunamadı"
                }), 404
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
    
    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'healthy', 'version': '1.0.0'})
    
    logger.info("Web routes registered successfully") 