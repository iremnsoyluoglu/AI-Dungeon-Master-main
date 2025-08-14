#!/usr/bin/env python3
"""
AI Dungeon Master - Streaming Manager
Handles live game broadcasting and viewer interactions
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from flask_socketio import emit, join_room, leave_room
import threading

@dataclass
class StreamSession:
    """Represents a live streaming session"""
    stream_id: str
    broadcaster_id: str
    broadcaster_name: str
    title: str
    description: str
    game_scenario: str
    viewers: List[str]
    is_live: bool
    started_at: datetime
    chat_messages: List[Dict]
    game_events: List[Dict]
    max_viewers: int = 100

class StreamingManager:
    """Manages live streaming sessions and viewer interactions"""
    
    def __init__(self):
        self.active_streams: Dict[str, StreamSession] = {}
        self.viewer_sessions: Dict[str, str] = {}  # viewer_id -> stream_id
        self.stream_history: List[StreamSession] = []
        
    def create_stream(self, broadcaster_id: str, broadcaster_name: str, 
                     title: str, description: str, game_scenario: str) -> str:
        """Create a new streaming session"""
        stream_id = f"stream_{int(time.time())}_{broadcaster_id}"
        
        stream = StreamSession(
            stream_id=stream_id,
            broadcaster_id=broadcaster_id,
            broadcaster_name=broadcaster_name,
            title=title,
            description=description,
            game_scenario=game_scenario,
            viewers=[],
            is_live=True,
            started_at=datetime.now(),
            chat_messages=[],
            game_events=[]
        )
        
        self.active_streams[stream_id] = stream
        return stream_id
    
    def end_stream(self, stream_id: str) -> bool:
        """End a streaming session"""
        if stream_id in self.active_streams:
            stream = self.active_streams[stream_id]
            stream.is_live = False
            self.stream_history.append(stream)
            del self.active_streams[stream_id]
            
            # Remove all viewers
            for viewer_id in stream.viewers:
                if viewer_id in self.viewer_sessions:
                    del self.viewer_sessions[viewer_id]
            
            return True
        return False
    
    def join_stream(self, stream_id: str, viewer_id: str, viewer_name: str) -> bool:
        """Add a viewer to a stream"""
        if stream_id in self.active_streams:
            stream = self.active_streams[stream_id]
            if len(stream.viewers) < stream.max_viewers and viewer_id not in stream.viewers:
                stream.viewers.append(viewer_id)
                self.viewer_sessions[viewer_id] = stream_id
                return True
        return False
    
    def leave_stream(self, viewer_id: str) -> bool:
        """Remove a viewer from a stream"""
        if viewer_id in self.viewer_sessions:
            stream_id = self.viewer_sessions[viewer_id]
            if stream_id in self.active_streams:
                stream = self.active_streams[stream_id]
                if viewer_id in stream.viewers:
                    stream.viewers.remove(viewer_id)
            del self.viewer_sessions[viewer_id]
            return True
        return False
    
    def add_chat_message(self, stream_id: str, viewer_id: str, 
                        viewer_name: str, message: str) -> bool:
        """Add a chat message to a stream"""
        if stream_id in self.active_streams:
            stream = self.active_streams[stream_id]
            chat_msg = {
                "id": f"msg_{int(time.time())}_{viewer_id}",
                "viewer_id": viewer_id,
                "viewer_name": viewer_name,
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
            stream.chat_messages.append(chat_msg)
            
            # Keep only last 100 messages
            if len(stream.chat_messages) > 100:
                stream.chat_messages = stream.chat_messages[-100:]
            
            return True
        return False
    
    def add_game_event(self, stream_id: str, event_type: str, 
                      event_data: Dict) -> bool:
        """Add a game event to the stream"""
        if stream_id in self.active_streams:
            stream = self.active_streams[stream_id]
            game_event = {
                "id": f"event_{int(time.time())}",
                "type": event_type,
                "data": event_data,
                "timestamp": datetime.now().isoformat()
            }
            stream.game_events.append(game_event)
            
            # Keep only last 50 events
            if len(stream.game_events) > 50:
                stream.game_events = stream.game_events[-50:]
            
            return True
        return False
    
    def get_stream_info(self, stream_id: str) -> Optional[Dict]:
        """Get information about a stream"""
        if stream_id in self.active_streams:
            stream = self.active_streams[stream_id]
            return {
                "stream_id": stream.stream_id,
                "broadcaster_id": stream.broadcaster_id,
                "broadcaster_name": stream.broadcaster_name,
                "title": stream.title,
                "description": stream.description,
                "game_scenario": stream.game_scenario,
                "viewer_count": len(stream.viewers),
                "is_live": stream.is_live,
                "started_at": stream.started_at.isoformat(),
                "duration": (datetime.now() - stream.started_at).total_seconds()
            }
        return None
    
    def get_active_streams(self) -> List[Dict]:
        """Get list of all active streams"""
        streams = []
        for stream in self.active_streams.values():
            streams.append({
                "stream_id": stream.stream_id,
                "broadcaster_name": stream.broadcaster_name,
                "title": stream.title,
                "game_scenario": stream.game_scenario,
                "viewer_count": len(stream.viewers),
                "started_at": stream.started_at.isoformat()
            })
        return streams
    
    def get_stream_chat(self, stream_id: str) -> List[Dict]:
        """Get chat messages for a stream"""
        if stream_id in self.active_streams:
            return self.active_streams[stream_id].chat_messages
        return []
    
    def get_stream_events(self, stream_id: str) -> List[Dict]:
        """Get game events for a stream"""
        if stream_id in self.active_streams:
            return self.active_streams[stream_id].game_events
        return []

# Global streaming manager instance
streaming_manager = StreamingManager()
