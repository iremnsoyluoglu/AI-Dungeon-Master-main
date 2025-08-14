#!/usr/bin/env python3
"""
User Management System
=====================

Handles user registration, login, and session management.
"""

import os
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional, Any

class UserManager:
    """Manages user authentication and sessions"""
    
    def __init__(self):
        self.users_file = "data/users.json"
        self.sessions_file = "data/sessions.json"
        self._ensure_data_directory()
        self._load_users()
        self._load_sessions()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs("data", exist_ok=True)
    
    def _load_users(self):
        """Load users from file"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
            else:
                self.users = {}
                self._save_users()
        except Exception as e:
            print(f"Error loading users: {e}")
            self.users = {}
    
    def _save_users(self):
        """Save users to file"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def _load_sessions(self):
        """Load sessions from file"""
        try:
            if os.path.exists(self.sessions_file):
                with open(self.sessions_file, 'r', encoding='utf-8') as f:
                    self.sessions = json.load(f)
            else:
                self.sessions = {}
                self._save_sessions()
        except Exception as e:
            print(f"Error loading sessions: {e}")
            self.sessions = {}
    
    def _save_sessions(self):
        """Save sessions to file"""
        try:
            with open(self.sessions_file, 'w', encoding='utf-8') as f:
                json.dump(self.sessions, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving sessions: {e}")
    
    def register_user(self, username: str, password: str, email: str = None) -> Dict[str, Any]:
        """Register a new user"""
        try:
            if username in self.users:
                return {"success": False, "error": "Username already exists"}
            
            user_id = str(uuid.uuid4())
            user_data = {
                "id": user_id,
                "username": username,
                "password": password,  # In production, hash this
                "email": email,
                "created_at": datetime.now().isoformat(),
                "last_login": None
            }
            
            self.users[username] = user_data
            self._save_users()
            
            return {
                "success": True,
                "user_id": user_id,
                "message": "User registered successfully"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def login_user(self, username: str, password: str) -> Dict[str, Any]:
        """Login a user"""
        try:
            if username not in self.users:
                return {"success": False, "error": "User not found"}
            
            user = self.users[username]
            if user["password"] != password:  # In production, verify hash
                return {"success": False, "error": "Invalid password"}
            
            # Create session
            session_id = str(uuid.uuid4())
            session_data = {
                "user_id": user["id"],
                "username": username,
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
            }
            
            self.sessions[session_id] = session_data
            self._save_sessions()
            
            # Update last login
            user["last_login"] = datetime.now().isoformat()
            self._save_users()
            
            return {
                "success": True,
                "session_id": session_id,
                "user_id": user["id"],
                "username": username
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_guest_user(self) -> Dict[str, Any]:
        """Create a guest user for quick access"""
        try:
            guest_id = f"guest_{str(uuid.uuid4())[:8]}"
            username = f"Guest_{guest_id}"
            
            user_data = {
                "id": guest_id,
                "username": username,
                "password": "",
                "email": None,
                "created_at": datetime.now().isoformat(),
                "last_login": datetime.now().isoformat(),
                "is_guest": True
            }
            
            self.users[username] = user_data
            self._save_users()
            
            # Create session
            session_id = str(uuid.uuid4())
            session_data = {
                "user_id": guest_id,
                "username": username,
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=2)).isoformat(),
                "is_guest": True
            }
            
            self.sessions[session_id] = session_data
            self._save_sessions()
            
            return {
                "success": True,
                "session_id": session_id,
                "user_id": guest_id,
                "username": username
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def verify_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Verify if a session is valid"""
        try:
            if session_id not in self.sessions:
                return None
            
            session = self.sessions[session_id]
            expires_at = datetime.fromisoformat(session["expires_at"])
            
            if datetime.now() > expires_at:
                # Session expired
                del self.sessions[session_id]
                self._save_sessions()
                return None
            
            return session
        except Exception as e:
            print(f"Error verifying session: {e}")
            return None
    
    def logout_user(self, session_id: str) -> bool:
        """Logout a user by removing their session"""
        try:
            if session_id in self.sessions:
                del self.sessions[session_id]
                self._save_sessions()
                return True
            return False
        except Exception as e:
            print(f"Error logging out user: {e}")
            return False
    
    def create_token(self, user_id: str, username: str) -> str:
        """Create a session token for user"""
        try:
            session_id = str(uuid.uuid4())
            session_data = {
                "user_id": user_id,
                "username": username,
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
            }
            self.sessions[session_id] = session_data
            self._save_sessions()
            return session_id
        except Exception as e:
            print(f"Error creating token: {e}")
            return None
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify a session token"""
        try:
            if token in self.sessions:
                session = self.sessions[token]
                expires_at = datetime.fromisoformat(session["expires_at"])
                if datetime.now() < expires_at:
                    return session
                else:
                    # Token expired, remove it
                    del self.sessions[token]
                    self._save_sessions()
            return None
        except Exception as e:
            print(f"Error verifying token: {e}")
            return None 