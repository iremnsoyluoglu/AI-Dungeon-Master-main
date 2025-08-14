"""
Vector Store Manager for RAG System
Handles ChromaDB integration and similarity search operations.
"""

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb
import os
from typing import List, Dict, Any, Tuple

class VectorStoreManager:
    def __init__(self):
        # Check if OpenAI API key is available
        if not os.getenv('OPENAI_API_KEY'):
            print("⚠️  Warning: OPENAI_API_KEY not found. Using fallback embeddings.")
            # Use a fallback embedding method or dummy embeddings
            self.embeddings = None
            self.api_key_missing = True
        else:
            try:
                self.embeddings = OpenAIEmbeddings()
                self.api_key_missing = False
            except Exception as e:
                print(f"⚠️  Warning: Failed to initialize OpenAI embeddings: {e}")
                self.embeddings = None
                self.api_key_missing = True
        
        self.persist_directory = "rag/vector_db/chroma_db"
        
        # Ensure directory exists
        os.makedirs(self.persist_directory, exist_ok=True)
        
    def create_vector_store(self, documents):
        """Creates vector store from documents"""
        try:
            if self.api_key_missing:
                return {"success": False, "error": "OpenAI API key required for vector store creation"}
            
            vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            vectorstore.persist()
            return vectorstore
        except Exception as e:
            raise Exception(f"Failed to create vector store: {str(e)}")
    
    def load_vector_store(self):
        """Loads existing vector store"""
        try:
            if self.api_key_missing:
                return {"success": False, "error": "OpenAI API key required for vector store operations"}
            
            return Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        except Exception as e:
            raise Exception(f"Failed to load vector store: {str(e)}")
    
    def similarity_search(self, query: str, k: int = 5):
        """Performs similarity search"""
        try:
            if self.api_key_missing:
                return []  # Return empty list if API key is missing
            
            vectorstore = self.load_vector_store()
            return vectorstore.similarity_search(query, k=k)
        except Exception as e:
            print(f"⚠️  Warning: Similarity search failed: {e}")
            return []  # Return empty list on error
    
    def similarity_search_with_score(self, query: str, k: int = 5):
        """Performs similarity search with scores"""
        try:
            if self.api_key_missing:
                return []  # Return empty list if API key is missing
            
            vectorstore = self.load_vector_store()
            return vectorstore.similarity_search_with_score(query, k=k)
        except Exception as e:
            print(f"⚠️  Warning: Similarity search with score failed: {e}")
            return []  # Return empty list on error
    
    def hybrid_search(self, query: str, k: int = 5):
        """Performs hybrid search (semantic + keyword)"""
        try:
            if self.api_key_missing:
                return []  # Return empty list if API key is missing
            
            vectorstore = self.load_vector_store()
            return vectorstore.similarity_search_with_score(query, k=k)
        except Exception as e:
            print(f"⚠️  Warning: Hybrid search failed: {e}")
            return []  # Return empty list on error
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Gets information about the vector store collection"""
        try:
            if self.api_key_missing:
                return {
                    "error": "OpenAI API key required",
                    "status": "inactive"
                }
            
            vectorstore = self.load_vector_store()
            collection = vectorstore._collection
            
            return {
                "collection_name": collection.name,
                "total_documents": collection.count(),
                "embedding_dimension": collection.metadata.get("hnsw:space", "cosine"),
                "persist_directory": self.persist_directory,
                "status": "active"
            }
        except Exception as e:
            return {"error": str(e), "status": "error"}
    
    def delete_collection(self):
        """Deletes the entire collection"""
        try:
            import shutil
            if os.path.exists(self.persist_directory):
                shutil.rmtree(self.persist_directory)
            return {"success": True, "message": "Collection deleted successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def add_documents(self, documents):
        """Adds new documents to existing vector store"""
        try:
            if self.api_key_missing:
                return {"success": False, "error": "OpenAI API key required for adding documents"}
            
            vectorstore = self.load_vector_store()
            vectorstore.add_documents(documents)
            vectorstore.persist()
            return {"success": True, "message": f"Added {len(documents)} documents"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def search_by_metadata(self, metadata_filter: Dict[str, Any], k: int = 5):
        """Searches documents by metadata filter"""
        try:
            vectorstore = self.load_vector_store()
            return vectorstore.similarity_search("", k=k, filter=metadata_filter)
        except Exception as e:
            raise Exception(f"Failed to search by metadata: {str(e)}")
