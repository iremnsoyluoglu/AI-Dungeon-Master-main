"""
Main RAG System for AI Dungeon Master
Combines document processing, vector storage, and fine-tuning capabilities.
"""

import json
import os
from typing import Dict, Any, List
from .rag_pipeline import RAGPipeline
from .fine_tuning.fine_tuning_pipeline import FineTuningPipeline
from .fine_tuning.data_preparation import FineTuningDataPreparation

class RAGSystem:
    def __init__(self):
        self.rag_pipeline = RAGPipeline()
        self.fine_tuning_pipeline = FineTuningPipeline()
        self.data_preparation = FineTuningDataPreparation()
        
        # Ensure directories exist
        os.makedirs("rag/uploads/user_documents", exist_ok=True)
        os.makedirs("rag/fine_tuning/training_data", exist_ok=True)
        os.makedirs("rag/vector_db/chroma_db", exist_ok=True)
    
    def upload_document(self, file_path: str):
        """Upload and process document"""
        try:
            result = self.rag_pipeline.process_upload(file_path)
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def ask_question(self, question: str):
        """Ask question about uploaded documents"""
        try:
            result = self.rag_pipeline.answer_question(question)
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_summary(self):
        """Get document summary"""
        try:
            result = self.rag_pipeline.get_document_summary()
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_scenario(self, theme: str = "fantasy", player_level: int = 1):
        """Generate game scenario using RAG"""
        try:
            result = self.rag_pipeline.generate_scenario(theme, player_level)
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def search_similar_content(self, query: str, k: int = 5):
        """Search for similar content"""
        try:
            result = self.rag_pipeline.search_similar_content(query, k)
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def prepare_training_data(self, documents: List[Dict]):
        """Prepare training data for fine-tuning"""
        try:
            self.data_preparation.create_training_pairs(documents)
            
            # Export training data
            export_path = "rag/fine_tuning/training_data/processed_data.json"
            export_result = self.data_preparation.export_training_data(export_path)
            
            if export_result["success"]:
                stats = self.data_preparation.get_training_stats()
                return {
                    "success": True,
                    "message": f"Training data prepared and exported",
                    "export_path": export_path,
                    "stats": stats
                }
            else:
                return export_result
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def fine_tune_model(self, training_data_path: str = None, **kwargs):
        """Fine-tune model with custom data"""
        try:
            # Load training data
            if training_data_path is None:
                training_data_path = "rag/fine_tuning/training_data/processed_data.json"
            
            if not os.path.exists(training_data_path):
                return {"success": False, "error": "Training data file not found"}
            
            load_result = self.data_preparation.load_training_data(training_data_path)
            if not load_result["success"]:
                return load_result
            
            # Validate training data
            validation = self.data_preparation.validate_training_data()
            if validation["validation_rate"] < 0.5:
                return {"success": False, "error": "Training data quality too low"}
            
            # Perform fine-tuning
            output_dir = "rag/fine_tuned_model"
            result = self.fine_tuning_pipeline.fine_tune(
                self.data_preparation.training_data, 
                output_dir, 
                **kwargs
            )
            
            return result
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def load_fine_tuned_model(self, model_path: str):
        """Load a fine-tuned model"""
        try:
            result = self.fine_tuning_pipeline.load_fine_tuned_model(model_path)
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_with_fine_tuned_model(self, prompt: str, max_length: int = 100):
        """Generate text using fine-tuned model"""
        try:
            generated_text = self.fine_tuning_pipeline.generate_text(prompt, max_length)
            return {
                "success": True,
                "generated_text": generated_text,
                "prompt": prompt
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def evaluate_fine_tuned_model(self, test_data: List[Dict]):
        """Evaluate fine-tuned model performance"""
        try:
            result = self.fine_tuning_pipeline.evaluate_model(test_data)
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_system_status(self):
        """Get comprehensive system status"""
        try:
            # RAG pipeline status
            rag_status = self.rag_pipeline.get_pipeline_status()
            
            # Fine-tuning pipeline status
            model_info = self.fine_tuning_pipeline.get_model_info()
            
            # Training data status
            training_stats = self.data_preparation.get_training_stats()
            
            return {
                "success": True,
                "rag_pipeline": rag_status,
                "fine_tuning_pipeline": model_info,
                "training_data": training_stats,
                "system_ready": rag_status.get("success", False) and "error" not in model_info
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_sample_document(self, content: str, filename: str = "sample_document.txt"):
        """Create a sample document for testing"""
        try:
            file_path = os.path.join("rag/uploads/user_documents", filename)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                "success": True,
                "message": f"Sample document created: {file_path}",
                "file_path": file_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run_demo(self):
        """Run a complete demo of the RAG system"""
        try:
            # 1. Create sample document
            sample_content = """
            Fantasy Role-Playing Game Guide
            
            This guide covers the basics of fantasy RPG gameplay including character creation, combat mechanics, and storytelling elements.
            
            Character Classes:
            - Warrior: Strong melee fighter with high health and armor
            - Mage: Spellcaster with powerful magical abilities
            - Rogue: Stealthy character with high agility and critical hit chance
            
            Combat System:
            Combat is turn-based with initiative rolls determining action order. Each character can perform one action per turn including attack, cast spell, or use item.
            
            Storytelling:
            The game master creates immersive scenarios with branching narratives. Players make choices that affect the story outcome and character development.
            """
            
            doc_result = self.create_sample_document(sample_content)
            if not doc_result["success"]:
                return doc_result
            
            # 2. Upload and process document
            upload_result = self.upload_document(doc_result["file_path"])
            if not upload_result["success"]:
                return upload_result
            
            # 3. Ask a question
            question_result = self.ask_question("What are the different character classes?")
            
            # 4. Generate a scenario
            scenario_result = self.generate_scenario("fantasy", 1)
            
            # 5. Get system status
            status_result = self.get_system_status()
            
            return {
                "success": True,
                "demo_results": {
                    "document_creation": doc_result,
                    "document_upload": upload_result,
                    "question_answering": question_result,
                    "scenario_generation": scenario_result,
                    "system_status": status_result
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

# Usage example
if __name__ == "__main__":
    rag_system = RAGSystem()
    
    # Run demo
    demo_result = rag_system.run_demo()
    print(f"Demo result: {demo_result}")
    
    # Get system status
    status = rag_system.get_system_status()
    print(f"System status: {status}")
