"""
Data Preparation for Fine-tuning
Handles training data creation and validation for model fine-tuning.
"""

import json
import os
from typing import List, Dict, Any
from langchain_openai import OpenAI

class FineTuningDataPreparation:
    def __init__(self):
        self.training_data = []
        
        # Check if OpenAI API key is available
        if not os.getenv('OPENAI_API_KEY'):
            print("⚠️  Warning: OPENAI_API_KEY not found. Using fallback LLM for data preparation.")
            self.llm = None
            self.api_key_missing = True
        else:
            try:
                self.llm = OpenAI(temperature=0.7)
                self.api_key_missing = False
            except Exception as e:
                print(f"⚠️  Warning: Failed to initialize OpenAI LLM for data preparation: {e}")
                self.llm = None
                self.api_key_missing = True
    
    def create_training_pairs(self, documents: List[Dict]):
        """Creates training pairs for fine-tuning"""
        for doc in documents:
            # Create question-answer pairs
            qa_pairs = self.generate_qa_pairs(doc['content'])
            
            for qa in qa_pairs:
                self.training_data.append({
                    'instruction': qa['question'],
                    'input': doc.get('context', ''),
                    'output': qa['answer']
                })
    
    def generate_qa_pairs(self, content: str) -> List[Dict[str, str]]:
        """Generates question-answer pairs from content using LLM"""
        try:
            if self.api_key_missing:
                # Return fallback Q&A pairs when API key is missing
                return [
                    {'question': 'What is the main topic of this content?', 'answer': 'This content discusses fantasy role-playing game elements.'},
                    {'question': 'How can this content help with game development?', 'answer': 'This content provides guidance for creating engaging game scenarios and mechanics.'},
                    {'question': 'What are the key elements of a good RPG scenario?', 'answer': 'A good RPG scenario should have engaging storytelling, meaningful choices, balanced challenges, and immersive world-building.'}
                ]
            
            prompt = f"""
            Based on the following content, generate 3-5 question-answer pairs that would be useful for training an AI assistant for a fantasy role-playing game.
            
            Content: {content[:2000]}  # Limit content length
            
            Generate pairs in this format:
            Q: [Question about the content]
            A: [Detailed answer based on the content]
            
            Focus on questions about game mechanics, lore, character development, or storytelling elements.
            """
            
            response = self.llm.predict(prompt)
            
            # Parse the response to extract Q&A pairs
            qa_pairs = self.parse_qa_response(response)
            
            return qa_pairs
            
        except Exception as e:
            # Fallback to basic Q&A pairs
            return [
                {'question': 'What is the main topic of this content?', 'answer': 'This content discusses fantasy role-playing game elements.'},
                {'question': 'How can this content help with game development?', 'answer': 'This content provides guidance for creating engaging game scenarios and mechanics.'},
                {'question': 'What are the key elements of a good RPG scenario?', 'answer': 'A good RPG scenario should have engaging storytelling, meaningful choices, balanced challenges, and immersive world-building.'}
            ]
    
    def parse_qa_response(self, response: str) -> List[Dict[str, str]]:
        """Parses LLM response to extract Q&A pairs"""
        qa_pairs = []
        lines = response.split('\n')
        
        current_question = ""
        current_answer = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith('Q:') or line.startswith('Question:'):
                # Save previous pair if exists
                if current_question and current_answer:
                    qa_pairs.append({
                        'question': current_question.strip(),
                        'answer': current_answer.strip()
                    })
                
                current_question = line.split(':', 1)[1] if ':' in line else line[2:]
                current_answer = ""
                
            elif line.startswith('A:') or line.startswith('Answer:'):
                current_answer = line.split(':', 1)[1] if ':' in line else line[2:]
                
            elif current_answer and line:
                # Continue building the answer
                current_answer += " " + line
        
        # Add the last pair
        if current_question and current_answer:
            qa_pairs.append({
                'question': current_question.strip(),
                'answer': current_answer.strip()
            })
        
        return qa_pairs
    
    def create_game_specific_pairs(self, game_content: Dict[str, Any]) -> List[Dict[str, str]]:
        """Creates training pairs specifically for game content"""
        pairs = []
        
        # Scenario-based pairs
        if 'scenarios' in game_content:
            for scenario in game_content['scenarios']:
                pairs.append({
                    'question': f"What is the main conflict in the {scenario.get('name', 'scenario')}?",
                    'answer': scenario.get('description', 'A fantasy adventure scenario.')
                })
        
        # Character-based pairs
        if 'characters' in game_content:
            for char in game_content['characters']:
                pairs.append({
                    'question': f"What are the abilities of a {char.get('class', 'character')}?",
                    'answer': char.get('description', 'A character with various abilities and skills.')
                })
        
        # Rule-based pairs
        if 'rules' in game_content:
            for rule in game_content['rules']:
                pairs.append({
                    'question': f"How does {rule.get('name', 'this rule')} work?",
                    'answer': rule.get('description', 'A game rule that affects gameplay.')
                })
        
        return pairs
    
    def export_training_data(self, filename: str):
        """Exports training data in required format"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for item in self.training_data:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
            
            return {"success": True, "message": f"Training data exported to {filename}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def load_training_data(self, filename: str):
        """Loads training data from file"""
        try:
            self.training_data = []
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        self.training_data.append(json.loads(line.strip()))
            
            return {"success": True, "message": f"Loaded {len(self.training_data)} training pairs"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def validate_training_data(self) -> Dict[str, Any]:
        """Validates training data quality"""
        valid_count = 0
        total_count = len(self.training_data)
        
        for item in self.training_data:
            if (len(item.get('instruction', '')) > 10 and 
                len(item.get('output', '')) > 20 and
                'instruction' in item and 'output' in item):
                valid_count += 1
        
        validation_rate = valid_count / total_count if total_count > 0 else 0
        
        return {
            'total_samples': total_count,
            'valid_samples': valid_count,
            'validation_rate': validation_rate,
            'quality_score': 'high' if validation_rate > 0.8 else 'medium' if validation_rate > 0.6 else 'low'
        }
    
    def get_training_stats(self) -> Dict[str, Any]:
        """Gets statistics about the training data"""
        if not self.training_data:
            return {"error": "No training data available"}
        
        avg_question_length = sum(len(item.get('instruction', '')) for item in self.training_data) / len(self.training_data)
        avg_answer_length = sum(len(item.get('output', '')) for item in self.training_data) / len(self.training_data)
        
        return {
            'total_pairs': len(self.training_data),
            'average_question_length': round(avg_question_length, 2),
            'average_answer_length': round(avg_answer_length, 2),
            'validation_status': self.validate_training_data()
        }
