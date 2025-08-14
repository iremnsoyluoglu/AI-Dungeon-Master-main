#!/usr/bin/env python3
"""
WebSocket Handler for Multiplayer
================================

Handles real-time WebSocket connections for:
- Player connections/disconnections
- Game state synchronization
- Chat messages
- Combat actions
- Character updates
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class MessageType(Enum):
    # Connection messages
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    PING = "ping"
    PONG = "pong"
    
    # Session messages
    JOIN_SESSION = "join_session"
    LEAVE_SESSION = "leave_session"
    SESSION_UPDATE = "session_update"
    
    # Game messages
    GAME_ACTION = "game_action"
    COMBAT_ACTION = "combat_action"
    CHARACTER_UPDATE = "character_update"
    DICE_ROLL = "dice_roll"
    
    # Chat messages
    CHAT_MESSAGE = "chat_message"
    
    # System messages
    ERROR = "error"
    SUCCESS = "success"
    NOTIFICATION = "notification"

class WebSocketHandler:
    """Handles WebSocket connections for multiplayer"""
    
    def __init__(self, session_manager, game_engine):
        self.session_manager = session_manager
        self.game_engine = game_engine
        self.connections: Dict[str, Any] = {}
        self.message_handlers: Dict[str, Callable] = {}
        self._setup_message_handlers()
    
    def _setup_message_handlers(self):
        """Setup message handlers"""
        self.message_handlers = {
            MessageType.CONNECT.value: self._handle_connect,
            MessageType.DISCONNECT.value: self._handle_disconnect,
            MessageType.JOIN_SESSION.value: self._handle_join_session,
            MessageType.LEAVE_SESSION.value: self._handle_leave_session,
            MessageType.GAME_ACTION.value: self._handle_game_action,
            MessageType.COMBAT_ACTION.value: self._handle_combat_action,
            MessageType.CHARACTER_UPDATE.value: self._handle_character_update,
            MessageType.DICE_ROLL.value: self._handle_dice_roll,
            MessageType.CHAT_MESSAGE.value: self._handle_chat_message,
            MessageType.PING.value: self._handle_ping,
        }
    
    async def handle_connection(self, websocket, path):
        """Handle new WebSocket connection"""
        connection_id = str(id(websocket))
        self.connections[connection_id] = {
            "websocket": websocket,
            "connected_at": datetime.now(),
            "player_id": None,
            "session_id": None,
            "last_ping": datetime.now()
        }
        
        logger.info(f"New WebSocket connection: {connection_id}")
        
        try:
            async for message in websocket:
                await self._handle_message(connection_id, message)
        except Exception as e:
            logger.error(f"WebSocket error for {connection_id}: {e}")
        finally:
            await self._handle_disconnect(connection_id)
    
    async def _handle_message(self, connection_id: str, message: str):
        """Handle incoming WebSocket message"""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            if message_type in self.message_handlers:
                await self.message_handlers[message_type](connection_id, data)
            else:
                await self._send_error(connection_id, f"Unknown message type: {message_type}")
                
        except json.JSONDecodeError:
            await self._send_error(connection_id, "Invalid JSON message")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await self._send_error(connection_id, "Internal server error")
    
    async def _handle_connect(self, connection_id: str, data: Dict[str, Any]):
        """Handle player connection"""
        player_id = data.get("player_id")
        username = data.get("username")
        
        if not player_id or not username:
            await self._send_error(connection_id, "Missing player_id or username")
            return
        
        # Update connection info
        self.connections[connection_id]["player_id"] = player_id
        
        # Send connection confirmation
        await self._send_message(connection_id, {
            "type": MessageType.SUCCESS.value,
            "message": "Connected successfully",
            "player_id": player_id,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"Player {username} connected: {connection_id}")
    
    async def _handle_disconnect(self, connection_id: str, data: Dict[str, Any] = None):
        """Handle player disconnection"""
        connection = self.connections.get(connection_id)
        if not connection:
            return
        
        player_id = connection.get("player_id")
        session_id = connection.get("session_id")
        
        # Leave session if in one
        if session_id:
            self.session_manager.leave_session(player_id)
        
        # Remove connection
        del self.connections[connection_id]
        
        logger.info(f"Player {player_id} disconnected: {connection_id}")
    
    async def _handle_join_session(self, connection_id: str, data: Dict[str, Any]):
        """Handle join session request"""
        session_id = data.get("session_id")
        player_id = data.get("player_id")
        username = data.get("username")
        
        if not all([session_id, player_id, username]):
            await self._send_error(connection_id, "Missing required fields")
            return
        
        # Join session
        result = self.session_manager.join_session(session_id, player_id, username, connection_id)
        
        if result["success"]:
            # Update connection info
            self.connections[connection_id]["session_id"] = session_id
            
            # Send success response
            await self._send_message(connection_id, {
                "type": MessageType.SUCCESS.value,
                "message": "Joined session successfully",
                "session": result["session"]
            })
            
            # Send session update to all players
            await self._broadcast_to_session(session_id, {
                "type": MessageType.SESSION_UPDATE.value,
                "session": result["session"]
            })
        else:
            await self._send_error(connection_id, result["error"])
    
    async def _handle_leave_session(self, connection_id: str, data: Dict[str, Any]):
        """Handle leave session request"""
        player_id = data.get("player_id")
        
        if not player_id:
            await self._send_error(connection_id, "Missing player_id")
            return
        
        # Leave session
        result = self.session_manager.leave_session(player_id)
        
        if result["success"]:
            # Update connection info
            self.connections[connection_id]["session_id"] = None
            
            await self._send_message(connection_id, {
                "type": MessageType.SUCCESS.value,
                "message": "Left session successfully"
            })
            
            # Send session update to remaining players
            if "session" in result:
                await self._broadcast_to_session(result["session"]["id"], {
                    "type": MessageType.SESSION_UPDATE.value,
                    "session": result["session"]
                })
        else:
            await self._send_error(connection_id, result["error"])
    
    async def _handle_game_action(self, connection_id: str, data: Dict[str, Any]):
        """Handle game action"""
        session_id = data.get("session_id")
        player_id = data.get("player_id")
        action = data.get("action")
        
        if not all([session_id, player_id, action]):
            await self._send_error(connection_id, "Missing required fields")
            return
        
        # Process game action
        try:
            # This would integrate with the game engine
            result = {
                "success": True,
                "action": action,
                "result": "Action processed successfully"
            }
            
            # Broadcast to all players in session
            await self._broadcast_to_session(session_id, {
                "type": MessageType.GAME_ACTION.value,
                "player_id": player_id,
                "action": action,
                "result": result
            })
            
        except Exception as e:
            logger.error(f"Error processing game action: {e}")
            await self._send_error(connection_id, "Failed to process action")
    
    async def _handle_combat_action(self, connection_id: str, data: Dict[str, Any]):
        """Handle combat action"""
        session_id = data.get("session_id")
        player_id = data.get("player_id")
        action = data.get("action")
        
        if not all([session_id, player_id, action]):
            await self._send_error(connection_id, "Missing required fields")
            return
        
        # Process combat action
        try:
            # This would integrate with the combat system
            result = {
                "success": True,
                "action": action,
                "combat_result": "Combat action processed"
            }
            
            # Broadcast to all players in session
            await self._broadcast_to_session(session_id, {
                "type": MessageType.COMBAT_ACTION.value,
                "player_id": player_id,
                "action": action,
                "result": result
            })
            
        except Exception as e:
            logger.error(f"Error processing combat action: {e}")
            await self._send_error(connection_id, "Failed to process combat action")
    
    async def _handle_character_update(self, connection_id: str, data: Dict[str, Any]):
        """Handle character update"""
        session_id = data.get("session_id")
        player_id = data.get("player_id")
        character_data = data.get("character")
        
        if not all([session_id, player_id, character_data]):
            await self._send_error(connection_id, "Missing required fields")
            return
        
        # Update character in game engine
        try:
            # This would update the character in the game engine
            result = {
                "success": True,
                "character": character_data
            }
            
            # Broadcast to all players in session
            await self._broadcast_to_session(session_id, {
                "type": MessageType.CHARACTER_UPDATE.value,
                "player_id": player_id,
                "character": character_data
            })
            
        except Exception as e:
            logger.error(f"Error updating character: {e}")
            await self._send_error(connection_id, "Failed to update character")
    
    async def _handle_dice_roll(self, connection_id: str, data: Dict[str, Any]):
        """Handle dice roll"""
        dice_notation = data.get("dice_notation", "1d20")
        player_id = data.get("player_id")
        session_id = data.get("session_id")
        
        try:
            # Roll dice using game engine
            result = self.game_engine.roll_dice(dice_notation)
            
            # Send result to player
            await self._send_message(connection_id, {
                "type": MessageType.DICE_ROLL.value,
                "dice_notation": dice_notation,
                "result": result,
                "player_id": player_id
            })
            
            # Broadcast to session if in one
            if session_id:
                await self._broadcast_to_session(session_id, {
                    "type": MessageType.DICE_ROLL.value,
                    "dice_notation": dice_notation,
                    "result": result,
                    "player_id": player_id
                })
                
        except Exception as e:
            logger.error(f"Error rolling dice: {e}")
            await self._send_error(connection_id, "Failed to roll dice")
    
    async def _handle_chat_message(self, connection_id: str, data: Dict[str, Any]):
        """Handle chat message"""
        session_id = data.get("session_id")
        player_id = data.get("player_id")
        message = data.get("message")
        
        if not all([session_id, player_id, message]):
            await self._send_error(connection_id, "Missing required fields")
            return
        
        # Send chat message to session
        result = self.session_manager.send_chat_message(session_id, player_id, message)
        
        if result["success"]:
            # Chat message is already broadcasted by session manager
            await self._send_message(connection_id, {
                "type": MessageType.SUCCESS.value,
                "message": "Chat message sent"
            })
        else:
            await self._send_error(connection_id, result["error"])
    
    async def _handle_ping(self, connection_id: str, data: Dict[str, Any]):
        """Handle ping message"""
        # Update last ping time
        if connection_id in self.connections:
            self.connections[connection_id]["last_ping"] = datetime.now()
        
        # Send pong response
        await self._send_message(connection_id, {
            "type": MessageType.PONG.value,
            "timestamp": datetime.now().isoformat()
        })
    
    async def _send_message(self, connection_id: str, message: Dict[str, Any]):
        """Send message to specific connection"""
        if connection_id not in self.connections:
            return
        
        try:
            websocket = self.connections[connection_id]["websocket"]
            await websocket.send(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending message to {connection_id}: {e}")
            await self._handle_disconnect(connection_id)
    
    async def _send_error(self, connection_id: str, error_message: str):
        """Send error message to connection"""
        await self._send_message(connection_id, {
            "type": MessageType.ERROR.value,
            "error": error_message,
            "timestamp": datetime.now().isoformat()
        })
    
    async def _broadcast_to_session(self, session_id: str, message: Dict[str, Any], 
                                   exclude_player_id: str = None):
        """Broadcast message to all players in session"""
        session = self.session_manager.active_sessions.get(session_id)
        if not session:
            return
        
        for player in session.current_players:
            if player.id == exclude_player_id:
                continue
            
            # Find connection for player
            for connection_id, connection in self.connections.items():
                if connection.get("player_id") == player.id:
                    await self._send_message(connection_id, message)
                    break
    
    async def broadcast_notification(self, session_id: str, notification: str, 
                                   notification_type: str = "info"):
        """Broadcast notification to session"""
        await self._broadcast_to_session(session_id, {
            "type": MessageType.NOTIFICATION.value,
            "notification": notification,
            "notification_type": notification_type,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get WebSocket connection statistics"""
        total_connections = len(self.connections)
        active_players = len(set(c.get("player_id") for c in self.connections.values() if c.get("player_id")))
        active_sessions = len(set(c.get("session_id") for c in self.connections.values() if c.get("session_id")))
        
        return {
            "total_connections": total_connections,
            "active_players": active_players,
            "active_sessions": active_sessions
        }
    
    async def cleanup_inactive_connections(self, max_idle_minutes: int = 30):
        """Clean up inactive connections"""
        cutoff_time = datetime.now().replace(minute=datetime.now().minute - max_idle_minutes)
        
        connections_to_remove = []
        for connection_id, connection in self.connections.items():
            if connection["last_ping"] < cutoff_time:
                connections_to_remove.append(connection_id)
        
        for connection_id in connections_to_remove:
            await self._handle_disconnect(connection_id)
        
        if connections_to_remove:
            logger.info(f"Cleaned up {len(connections_to_remove)} inactive connections") 