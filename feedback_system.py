#!/usr/bin/env python3
"""
Feedback System for AI Dungeon Master

This module provides comprehensive feedback collection and management
for the AI Dungeon Master project, including surveys, analytics, and reporting.
"""

import json
import os
import smtplib
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeedbackSystem:
    """
    Comprehensive feedback collection and management system.
    
    Features:
    - User experience surveys
    - Feature request tracking
    - Bug report system
    - Performance monitoring
    - Email notifications
    - Analytics and reporting
    """
    
    def __init__(self, db_path: str = "feedback.db", config_path: str = "feedback_config.json"):
        """Initialize the feedback system."""
        self.db_path = db_path
        self.config_path = config_path
        self.config = self._load_config()
        
        # Initialize database
        self._init_database()
        
        # Feedback categories
        self.categories = {
            "game_interface": "Game Interface",
            "ai_agents": "AI Agents",
            "rag_system": "RAG System",
            "performance": "Performance",
            "features": "Features",
            "documentation": "Documentation",
            "bug_report": "Bug Report",
            "feature_request": "Feature Request",
            "general": "General Feedback"
        }
        
        # Survey templates
        self.survey_templates = self._load_survey_templates()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load feedback system configuration."""
        default_config = {
            "email": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "feedback@aidungeonmaster.com",
                "sender_password": "",
                "admin_email": "admin@aidungeonmaster.com"
            },
            "notifications": {
                "enable_email": True,
                "enable_dashboard": True,
                "auto_response": True
            },
            "analytics": {
                "track_metrics": True,
                "generate_reports": True,
                "report_frequency": "weekly"
            },
            "surveys": {
                "auto_send": False,
                "reminder_frequency": "weekly",
                "max_reminders": 3
            }
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge with default config
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                logger.error(f"Error loading config: {e}")
                return default_config
        else:
            # Create default config file
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            return default_config
    
    def _init_database(self):
        """Initialize the feedback database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                user_type TEXT,
                rating INTEGER,
                categories TEXT,
                feedback_text TEXT,
                timestamp TEXT,
                status TEXT DEFAULT 'new',
                priority TEXT DEFAULT 'medium',
                assigned_to TEXT,
                response TEXT,
                response_timestamp TEXT
            )
        ''')
        
        # Create surveys table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS surveys (
                id TEXT PRIMARY KEY,
                title TEXT,
                questions TEXT,
                responses TEXT,
                created_at TEXT,
                active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Create analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id TEXT PRIMARY KEY,
                metric_name TEXT,
                metric_value REAL,
                timestamp TEXT,
                category TEXT
            )
        ''')
        
        # Create notifications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id TEXT PRIMARY KEY,
                type TEXT,
                message TEXT,
                recipient TEXT,
                sent_at TEXT,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_survey_templates(self) -> Dict[str, Any]:
        """Load survey templates."""
        return {
            "user_experience": {
                "title": "User Experience Survey",
                "description": "Help us improve your experience with AI Dungeon Master",
                "questions": [
                    {
                        "id": "overall_satisfaction",
                        "type": "rating",
                        "question": "How satisfied are you with AI Dungeon Master?",
                        "options": ["Very Dissatisfied", "Dissatisfied", "Neutral", "Satisfied", "Very Satisfied"]
                    },
                    {
                        "id": "ease_of_use",
                        "type": "rating",
                        "question": "How easy is it to use the interface?",
                        "options": ["Very Difficult", "Difficult", "Neutral", "Easy", "Very Easy"]
                    },
                    {
                        "id": "feature_rating",
                        "type": "multiple_choice",
                        "question": "Which features do you find most useful?",
                        "options": ["AI Agents", "RAG System", "Theme Selection", "Character Creation", "Scenario Generation"]
                    },
                    {
                        "id": "improvement_suggestions",
                        "type": "text",
                        "question": "What improvements would you like to see?"
                    }
                ]
            },
            "feature_request": {
                "title": "Feature Request Survey",
                "description": "Tell us what features you'd like to see in future updates",
                "questions": [
                    {
                        "id": "desired_features",
                        "type": "multiple_choice",
                        "question": "Which features would you like to see added?",
                        "options": ["Multiplayer Support", "Voice Integration", "Mobile App", "More Themes", "Advanced AI", "Cloud Save"]
                    },
                    {
                        "id": "priority_level",
                        "type": "rating",
                        "question": "How important are these features to you?",
                        "options": ["Not Important", "Low Priority", "Medium Priority", "High Priority", "Critical"]
                    },
                    {
                        "id": "use_case",
                        "type": "text",
                        "question": "How would you use these new features?"
                    }
                ]
            },
            "bug_report": {
                "title": "Bug Report Form",
                "description": "Help us identify and fix issues",
                "questions": [
                    {
                        "id": "bug_type",
                        "type": "multiple_choice",
                        "question": "What type of issue are you experiencing?",
                        "options": ["Interface Bug", "Performance Issue", "AI Agent Problem", "RAG System Error", "Game Logic Bug", "Other"]
                    },
                    {
                        "id": "severity",
                        "type": "rating",
                        "question": "How severe is this issue?",
                        "options": ["Minor", "Low", "Medium", "High", "Critical"]
                    },
                    {
                        "id": "bug_description",
                        "type": "text",
                        "question": "Please describe the issue in detail:"
                    },
                    {
                        "id": "steps_to_reproduce",
                        "type": "text",
                        "question": "Steps to reproduce the issue:"
                    }
                ]
            }
        }
    
    def submit_feedback(self, feedback_data: Dict[str, Any]) -> str:
        """Submit user feedback."""
        feedback_id = str(uuid.uuid4())
        
        # Validate required fields
        required_fields = ["feedback_text"]
        for field in required_fields:
            if field not in feedback_data or not feedback_data[field]:
                raise ValueError(f"Missing required field: {field}")
        
        # Prepare feedback record
        feedback_record = {
            "id": feedback_id,
            "name": feedback_data.get("name", ""),
            "email": feedback_data.get("email", ""),
            "user_type": feedback_data.get("user_type", "User"),
            "rating": feedback_data.get("rating", 0),
            "categories": json.dumps(feedback_data.get("categories", {})),
            "feedback_text": feedback_data["feedback_text"],
            "timestamp": datetime.now().isoformat(),
            "status": "new",
            "priority": self._determine_priority(feedback_data),
            "assigned_to": "",
            "response": "",
            "response_timestamp": ""
        }
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO feedback (
                id, name, email, user_type, rating, categories, feedback_text,
                timestamp, status, priority, assigned_to, response, response_timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            feedback_record["id"], feedback_record["name"], feedback_record["email"],
            feedback_record["user_type"], feedback_record["rating"], feedback_record["categories"],
            feedback_record["feedback_text"], feedback_record["timestamp"], feedback_record["status"],
            feedback_record["priority"], feedback_record["assigned_to"], feedback_record["response"],
            feedback_record["response_timestamp"]
        ))
        
        conn.commit()
        conn.close()
        
        # Track analytics
        self._track_feedback_analytics(feedback_record)
        
        # Send notifications
        if self.config["notifications"]["enable_email"]:
            self._send_feedback_notification(feedback_record)
        
        # Send auto-response
        if self.config["notifications"]["auto_response"] and feedback_record["email"]:
            self._send_auto_response(feedback_record)
        
        logger.info(f"Feedback submitted: {feedback_id}")
        return feedback_id
    
    def _determine_priority(self, feedback_data: Dict[str, Any]) -> str:
        """Determine feedback priority based on content and rating."""
        rating = feedback_data.get("rating", 0)
        feedback_text = feedback_data.get("feedback_text", "").lower()
        
        # High priority indicators
        high_priority_keywords = ["bug", "error", "crash", "broken", "not working", "urgent", "critical"]
        if any(keyword in feedback_text for keyword in high_priority_keywords):
            return "high"
        
        # Rating-based priority
        if rating <= 2:
            return "high"
        elif rating <= 3:
            return "medium"
        else:
            return "low"
    
    def _track_feedback_analytics(self, feedback_record: Dict[str, Any]):
        """Track feedback analytics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Track overall feedback count
        cursor.execute('''
            INSERT INTO analytics (id, metric_name, metric_value, timestamp, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            str(uuid.uuid4()), "feedback_count", 1,
            datetime.now().isoformat(), "feedback"
        ))
        
        # Track rating
        if feedback_record["rating"] > 0:
            cursor.execute('''
                INSERT INTO analytics (id, metric_name, metric_value, timestamp, category)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                str(uuid.uuid4()), "average_rating", feedback_record["rating"],
                datetime.now().isoformat(), "rating"
            ))
        
        # Track categories
        categories = json.loads(feedback_record["categories"])
        for category, value in categories.items():
            if value:
                cursor.execute('''
                    INSERT INTO analytics (id, metric_name, metric_value, timestamp, category)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    str(uuid.uuid4()), f"category_{category}", 1,
                    datetime.now().isoformat(), "categories"
                ))
        
        conn.commit()
        conn.close()
    
    def _send_feedback_notification(self, feedback_record: Dict[str, Any]):
        """Send notification about new feedback."""
        if not self.config["email"]["sender_password"]:
            logger.warning("Email password not configured, skipping notification")
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config["email"]["sender_email"]
            msg['To'] = self.config["email"]["admin_email"]
            msg['Subject'] = f"New Feedback - AI Dungeon Master"
            
            body = f"""
            New feedback received:
            
            ID: {feedback_record['id']}
            From: {feedback_record['name']} ({feedback_record['email']})
            Type: {feedback_record['user_type']}
            Rating: {feedback_record['rating']}/5
            Priority: {feedback_record['priority']}
            
            Feedback:
            {feedback_record['feedback_text']}
            
            Categories: {feedback_record['categories']}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.config["email"]["smtp_server"], self.config["email"]["smtp_port"])
            server.starttls()
            server.login(self.config["email"]["sender_email"], self.config["email"]["sender_password"])
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Feedback notification sent to {self.config['email']['admin_email']}")
            
        except Exception as e:
            logger.error(f"Error sending feedback notification: {e}")
    
    def _send_auto_response(self, feedback_record: Dict[str, Any]):
        """Send automatic response to user."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config["email"]["sender_email"]
            msg['To'] = feedback_record["email"]
            msg['Subject'] = "Thank you for your feedback - AI Dungeon Master"
            
            body = f"""
            Dear {feedback_record['name'] or 'User'},
            
            Thank you for taking the time to provide feedback about AI Dungeon Master.
            We have received your message and will review it carefully.
            
            Your feedback ID: {feedback_record['id']}
            Priority: {feedback_record['priority']}
            
            We typically respond to feedback within 24-48 hours. If your feedback is urgent,
            please contact us directly at {self.config['email']['admin_email']}.
            
            Best regards,
            The AI Dungeon Master Team
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.config["email"]["smtp_server"], self.config["email"]["smtp_port"])
            server.starttls()
            server.login(self.config["email"]["sender_email"], self.config["email"]["sender_password"])
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Auto-response sent to {feedback_record['email']}")
            
        except Exception as e:
            logger.error(f"Error sending auto-response: {e}")
    
    def get_feedback(self, feedback_id: str = None, status: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get feedback records."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if feedback_id:
            cursor.execute('SELECT * FROM feedback WHERE id = ?', (feedback_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return self._format_feedback_record(row)
            else:
                return None
        
        # Build query
        query = 'SELECT * FROM feedback'
        params = []
        
        if status:
            query += ' WHERE status = ?'
            params.append(status)
        
        query += ' ORDER BY timestamp DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._format_feedback_record(row) for row in rows]
    
    def _format_feedback_record(self, row: tuple) -> Dict[str, Any]:
        """Format database row as feedback record."""
        return {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "user_type": row[3],
            "rating": row[4],
            "categories": json.loads(row[5]) if row[5] else {},
            "feedback_text": row[6],
            "timestamp": row[7],
            "status": row[8],
            "priority": row[9],
            "assigned_to": row[10],
            "response": row[11],
            "response_timestamp": row[12]
        }
    
    def update_feedback_status(self, feedback_id: str, status: str, response: str = None, assigned_to: str = None):
        """Update feedback status and add response."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        update_data = {
            "status": status,
            "response": response or "",
            "response_timestamp": datetime.now().isoformat() if response else "",
            "assigned_to": assigned_to or ""
        }
        
        cursor.execute('''
            UPDATE feedback 
            SET status = ?, response = ?, response_timestamp = ?, assigned_to = ?
            WHERE id = ?
        ''', (
            update_data["status"], update_data["response"],
            update_data["response_timestamp"], update_data["assigned_to"], feedback_id
        ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Feedback {feedback_id} status updated to {status}")
    
    def create_survey(self, survey_type: str, custom_questions: List[Dict[str, Any]] = None) -> str:
        """Create a new survey."""
        survey_id = str(uuid.uuid4())
        
        if survey_type not in self.survey_templates:
            raise ValueError(f"Unknown survey type: {survey_type}")
        
        template = self.survey_templates[survey_type]
        questions = custom_questions or template["questions"]
        
        survey_data = {
            "id": survey_id,
            "title": template["title"],
            "questions": json.dumps(questions),
            "responses": json.dumps([]),
            "created_at": datetime.now().isoformat(),
            "active": True
        }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO surveys (id, title, questions, responses, created_at, active)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            survey_data["id"], survey_data["title"], survey_data["questions"],
            survey_data["responses"], survey_data["created_at"], survey_data["active"]
        ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Survey created: {survey_id}")
        return survey_id
    
    def submit_survey_response(self, survey_id: str, responses: Dict[str, Any]) -> bool:
        """Submit survey response."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current survey
        cursor.execute('SELECT responses FROM surveys WHERE id = ?', (survey_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return False
        
        current_responses = json.loads(row[0])
        current_responses.append({
            "responses": responses,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update survey
        cursor.execute('''
            UPDATE surveys SET responses = ? WHERE id = ?
        ''', (json.dumps(current_responses), survey_id))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Survey response submitted for survey {survey_id}")
        return True
    
    def get_survey_results(self, survey_id: str) -> Dict[str, Any]:
        """Get survey results and analytics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM surveys WHERE id = ?', (survey_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        survey_data = {
            "id": row[0],
            "title": row[1],
            "questions": json.loads(row[2]),
            "responses": json.loads(row[3]),
            "created_at": row[4],
            "active": row[5]
        }
        
        # Calculate analytics
        analytics = self._calculate_survey_analytics(survey_data)
        
        return {
            "survey": survey_data,
            "analytics": analytics
        }
    
    def _calculate_survey_analytics(self, survey_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate survey analytics."""
        responses = survey_data["responses"]
        questions = survey_data["questions"]
        
        analytics = {
            "total_responses": len(responses),
            "response_rate": 0,  # Would need total sent to calculate
            "question_analytics": {}
        }
        
        for question in questions:
            question_id = question["id"]
            question_type = question["type"]
            
            if question_type == "rating":
                ratings = [r["responses"].get(question_id, 0) for r in responses if question_id in r["responses"]]
                if ratings:
                    analytics["question_analytics"][question_id] = {
                        "type": "rating",
                        "average": sum(ratings) / len(ratings),
                        "distribution": self._calculate_rating_distribution(ratings)
                    }
            
            elif question_type == "multiple_choice":
                choices = {}
                for response in responses:
                    if question_id in response["responses"]:
                        choice = response["responses"][question_id]
                        choices[choice] = choices.get(choice, 0) + 1
                
                analytics["question_analytics"][question_id] = {
                    "type": "multiple_choice",
                    "choices": choices
                }
        
        return analytics
    
    def _calculate_rating_distribution(self, ratings: List[int]) -> Dict[str, int]:
        """Calculate rating distribution."""
        distribution = {}
        for rating in range(1, 6):  # Assuming 1-5 scale
            distribution[str(rating)] = ratings.count(rating)
        return distribution
    
    def generate_feedback_report(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Generate comprehensive feedback report."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build date filter
        date_filter = ""
        params = []
        if start_date and end_date:
            date_filter = "WHERE timestamp BETWEEN ? AND ?"
            params = [start_date, end_date]
        
        # Get feedback statistics
        cursor.execute(f'''
            SELECT 
                COUNT(*) as total_feedback,
                AVG(rating) as average_rating,
                COUNT(CASE WHEN status = 'new' THEN 1 END) as new_feedback,
                COUNT(CASE WHEN status = 'in_progress' THEN 1 END) as in_progress,
                COUNT(CASE WHEN status = 'resolved' THEN 1 END) as resolved,
                COUNT(CASE WHEN priority = 'high' THEN 1 END) as high_priority,
                COUNT(CASE WHEN priority = 'medium' THEN 1 END) as medium_priority,
                COUNT(CASE WHEN priority = 'low' THEN 1 END) as low_priority
            FROM feedback {date_filter}
        ''', params)
        
        stats = cursor.fetchone()
        
        # Get category breakdown
        cursor.execute(f'''
            SELECT categories FROM feedback {date_filter}
        ''', params)
        
        category_rows = cursor.fetchall()
        category_stats = {}
        
        for row in category_rows:
            if row[0]:
                categories = json.loads(row[0])
                for category, value in categories.items():
                    if value:
                        category_stats[category] = category_stats.get(category, 0) + 1
        
        # Get recent feedback
        cursor.execute(f'''
            SELECT * FROM feedback {date_filter}
            ORDER BY timestamp DESC LIMIT 10
        ''', params)
        
        recent_feedback = [self._format_feedback_record(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            "period": {
                "start_date": start_date,
                "end_date": end_date
            },
            "statistics": {
                "total_feedback": stats[0],
                "average_rating": round(stats[1], 2) if stats[1] else 0,
                "new_feedback": stats[2],
                "in_progress": stats[3],
                "resolved": stats[4],
                "high_priority": stats[5],
                "medium_priority": stats[6],
                "low_priority": stats[7]
            },
            "category_breakdown": category_stats,
            "recent_feedback": recent_feedback,
            "generated_at": datetime.now().isoformat()
        }
    
    def export_feedback_data(self, format: str = "json", filename: str = None) -> str:
        """Export feedback data to file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"feedback_export_{timestamp}.{format}"
        
        feedback_data = self.get_feedback(limit=1000)  # Get all feedback
        
        if format == "json":
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(feedback_data, f, indent=2, ensure_ascii=False)
        elif format == "csv":
            import csv
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                if feedback_data:
                    writer = csv.DictWriter(f, fieldnames=feedback_data[0].keys())
                    writer.writeheader()
                    writer.writerows(feedback_data)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        logger.info(f"Feedback data exported to {filename}")
        return filename

# Example usage
if __name__ == "__main__":
    # Initialize feedback system
    feedback_system = FeedbackSystem()
    
    # Submit sample feedback
    sample_feedback = {
        "name": "Test User",
        "email": "test@example.com",
        "user_type": "Player",
        "rating": 4,
        "categories": {
            "game_interface": True,
            "ai_agents": True,
            "performance": False
        },
        "feedback_text": "Great game! The AI agents are working well and the interface is intuitive. Would love to see more themes in the future."
    }
    
    feedback_id = feedback_system.submit_feedback(sample_feedback)
    print(f"Feedback submitted with ID: {feedback_id}")
    
    # Get feedback
    feedback = feedback_system.get_feedback(feedback_id)
    print(f"Retrieved feedback: {feedback}")
    
    # Create survey
    survey_id = feedback_system.create_survey("user_experience")
    print(f"Survey created with ID: {survey_id}")
    
    # Submit survey response
    survey_response = {
        "overall_satisfaction": 4,
        "ease_of_use": 5,
        "feature_rating": ["AI Agents", "Theme Selection"],
        "improvement_suggestions": "Add more character customization options"
    }
    
    success = feedback_system.submit_survey_response(survey_id, survey_response)
    print(f"Survey response submitted: {success}")
    
    # Get survey results
    results = feedback_system.get_survey_results(survey_id)
    print(f"Survey results: {json.dumps(results['analytics'], indent=2)}")
    
    # Generate report
    report = feedback_system.generate_feedback_report()
    print(f"Feedback report generated: {report['statistics']}")
    
    # Export data
    export_file = feedback_system.export_feedback_data("json")
    print(f"Feedback data exported to: {export_file}")
