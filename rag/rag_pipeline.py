"""
RAG Pipeline for AI Dungeon Master
Combines document processing, vector storage, and LLM generation.
"""

from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from .document_processor import DocumentProcessor
from .vector_store import VectorStoreManager
import json
import os
from typing import Dict, Any, List

class RAGPipeline:
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.vector_store_manager = VectorStoreManager()
        
        # Check if OpenAI API key is available
        if not os.getenv('OPENAI_API_KEY'):
            print("⚠️  Warning: OPENAI_API_KEY not found. Using fallback LLM.")
            self.llm = None
            self.api_key_missing = True
        else:
            try:
                self.llm = OpenAI(temperature=0.7)
                self.api_key_missing = False
            except Exception as e:
                print(f"⚠️  Warning: Failed to initialize OpenAI LLM: {e}")
                self.llm = None
                self.api_key_missing = True
        
        # Custom prompt template for game-related queries
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""
            You are an AI assistant for a fantasy role-playing game. You help players understand game mechanics, lore, and provide guidance based on the provided context.
            
            Context: {context}
            
            Question: {question}
            
            Answer the question based on the context provided. If the context doesn't contain enough information, provide a general helpful response for a fantasy RPG player. Be creative and engaging in your responses.
            """
        )
        
        # Game-specific prompt for scenario generation
        self.scenario_prompt_template = PromptTemplate(
            input_variables=["context", "theme", "player_level"],
            template="""
            You are a master storyteller for a fantasy role-playing game. Based on the provided context and game theme, create an engaging scenario.
            
            Game Context: {context}
            Theme: {theme}
            Player Level: {player_level}
            
            Create a detailed scenario that includes:
            1. Setting description
            2. Main conflict or quest
            3. Key NPCs and their motivations
            4. Potential challenges and rewards
            5. Multiple branching paths for player choice
            
            Make it immersive and suitable for the specified player level.
            """
        )
    
    def process_upload(self, file_path: str):
        """Process uploaded document and create vector store"""
        try:
            # 1. Validate document
            validation = self.document_processor.validate_document(file_path)
            if not validation["valid"]:
                return {"success": False, "error": validation["error"]}
            
            # 2. Process document
            chunks = self.document_processor.process_uploaded_file(file_path)
            
            # 3. Create vector store (with API key check)
            if self.vector_store_manager.api_key_missing:
                return {
                    "success": False, 
                    "error": "OpenAI API key required for document processing. Please set OPENAI_API_KEY environment variable.",
                    "file_info": validation
                }
            
            vectorstore = self.vector_store_manager.create_vector_store(chunks)
            
            return {
                "success": True, 
                "message": f"Document processed and indexed. Created {len(chunks)} chunks.",
                "chunks_created": len(chunks),
                "file_info": validation
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def answer_question(self, question: str):
        """Answer question using RAG"""
        try:
            # Check if LLM is available
            if self.api_key_missing:
                return {
                    "success": False,
                    "error": "OpenAI API key required for question answering. Please set OPENAI_API_KEY environment variable.",
                    "fallback_answer": "I'm sorry, but I need an OpenAI API key to answer questions. Please configure your API key and try again."
                }
            
            # 1. Retrieve relevant documents
            relevant_docs = self.vector_store_manager.similarity_search(question)
            
            if not relevant_docs:
                return {
                    "success": True,
                    "answer": "I don't have enough context to answer that question. Please upload some documents first.",
                    "sources": [],
                    "context": ""
                }
            
            # 2. Create context from retrieved documents
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            # 3. Generate answer using LLM
            prompt = self.prompt_template.format(context=context, question=question)
            answer = self.llm.predict(prompt)
            
            return {
                "success": True,
                "answer": answer,
                "sources": [doc.metadata for doc in relevant_docs],
                "context": context,
                "documents_used": len(relevant_docs)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_scenario(self, theme: str = "fantasy", player_level: int = 1):
        """Generate game scenario using RAG"""
        try:
            # Check if LLM is available
            if self.api_key_missing:
                return {
                    "success": False,
                    "error": "OpenAI API key required for scenario generation. Please set OPENAI_API_KEY environment variable.",
                    "fallback_scenario": self._generate_fallback_scenario(theme, player_level)
                }
            
            # 1. Retrieve relevant documents for scenario generation
            relevant_docs = self.vector_store_manager.similarity_search("fantasy scenario quest adventure", k=10)
            
            context = ""
            if relevant_docs:
                context = "\n\n".join([doc.page_content for doc in relevant_docs])
            else:
                context = "Fantasy role-playing game with magic, monsters, and adventure."
            
            # 2. Generate scenario using game-specific prompt
            prompt = self.scenario_prompt_template.format(
                context=context,
                theme=theme,
                player_level=player_level
            )
            
            scenario_text = self.llm.predict(prompt)
            
            # 3. Parse and structure the scenario
            scenario = self._parse_scenario_text(scenario_text, theme, player_level)
            
            return {
                "success": True,
                "scenario": scenario,
                "theme": theme,
                "player_level": player_level,
                "sources_used": len(relevant_docs) if relevant_docs else 0
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _generate_fallback_scenario(self, theme: str, player_level: int):
        """Generate a fallback scenario when API key is missing"""
        fallback_scenarios = {
            "fantasy": {
                "title": f"🎭 {theme.title()} Macerası - Seviye {player_level}",
                "description": f"Klasik {theme} temasında, seviye {player_level} oyuncular için tasarlanmış macera.",
                "difficulty": "medium",
                "theme": theme,
                "story": f"Bu {theme} dünyasında, kahramanların cesaretini ve becerilerini test eden bir macera başlıyor. Seviye {player_level} oyuncular için uygun zorlukta tasarlanmış bu hikaye, klasik RPG elementlerini içeriyor.",
                "choices": [
                    "Kahramanlık yolunu seç",
                    "Bilgelik yolunu seç", 
                    "Gizlilik yolunu seç",
                    "Diplomasi yolunu seç"
                ],
                "note": "Bu senaryo OpenAI API anahtarı olmadığı için otomatik olarak üretildi."
            },
            "warhammer40k": {
                "title": f"⚔️ {theme.title()} Görevi - Seviye {player_level}",
                "description": f"Warhammer 40K evreninde, seviye {player_level} oyuncular için tasarlanmış görev.",
                "difficulty": "hard",
                "theme": theme,
                "story": f"İmperium'un karanlık köşelerinde, Chaos'un tehdidi altında bir görev. Seviye {player_level} oyuncular için uygun zorlukta tasarlanmış bu hikaye, Warhammer 40K evreninin atmosferini yansıtıyor.",
                "choices": [
                    "Adeptus Astartes yaklaşımı",
                    "Inquisition yaklaşımı",
                    "Imperial Guard yaklaşımı",
                    "Rogue Trader yaklaşımı"
                ],
                "note": "Bu senaryo OpenAI API anahtarı olmadığı için otomatik olarak üretildi."
            },
            "cyberpunk": {
                "title": f"🌃 {theme.title()} Operasyonu - Seviye {player_level}",
                "description": f"Cyberpunk dünyasında, seviye {player_level} oyuncular için tasarlanmış operasyon.",
                "difficulty": "medium",
                "theme": theme,
                "story": f"Neon ışıkların altında, megacorporation'ların gölgesinde bir operasyon. Seviye {player_level} oyuncular için uygun zorlukta tasarlanmış bu hikaye, cyberpunk atmosferini yansıtıyor.",
                "choices": [
                    "Netrunner yaklaşımı",
                    "Street Samurai yaklaşımı",
                    "Corporate yaklaşımı",
                    "Nomad yaklaşımı"
                ],
                "note": "Bu senaryo OpenAI API anahtarı olmadığı için otomatik olarak üretildi."
            }
        }
        
        return fallback_scenarios.get(theme, fallback_scenarios["fantasy"])
    
    def _parse_scenario_text(self, scenario_text: str, theme: str, player_level: int):
        """Parse LLM-generated scenario text into structured format"""
        # Simple parsing - in a real implementation, you might want more sophisticated parsing
        return {
            "title": f"AI Üretilen {theme.title()} Senaryosu",
            "description": f"Seviye {player_level} için özel olarak üretilen senaryo.",
            "difficulty": "medium",
            "theme": theme,
            "story": scenario_text,
            "choices": [
                "İleri git",
                "Keşfet", 
                "Savaş",
                "Diplomasi"
            ],
            "note": "Bu senaryo AI tarafından üretildi."
        }
    
    def get_document_summary(self):
        """Generate document summary"""
        try:
            # Check if LLM is available
            if self.api_key_missing:
                return {
                    "success": False,
                    "error": "OpenAI API key required for document summarization. Please set OPENAI_API_KEY environment variable."
                }
            
            # Retrieve all documents for summary
            all_docs = self.vector_store_manager.similarity_search("", k=50)
            
            if not all_docs:
                return {"success": False, "error": "No documents found in vector store"}
            
            summary_prompt = f"""
            Summarize the following document content for a fantasy role-playing game:
            
            {' '.join([doc.page_content for doc in all_docs])}
            
            Provide a comprehensive summary of the main topics, key points, and how they relate to fantasy RPG gameplay.
            """
            
            summary = self.llm.predict(summary_prompt)
            
            return {
                "success": True,
                "summary": summary,
                "documents_summarized": len(all_docs)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def search_similar_content(self, query: str, k: int = 5):
        """Search for similar content in the vector store"""
        try:
            results = self.vector_store_manager.similarity_search_with_score(query, k=k)
            
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "similarity_score": score
                })
            
            return {
                "success": True,
                "results": formatted_results,
                "query": query,
                "total_results": len(formatted_results)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_pipeline_status(self):
        """Get status of the RAG pipeline"""
        try:
            collection_info = self.vector_store_manager.get_collection_info()
            
            return {
                "success": True,
                "vector_store_status": collection_info,
                "document_processor": "active",
                "llm_configured": not self.api_key_missing,
                "api_key_status": "configured" if not self.api_key_missing else "missing"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
