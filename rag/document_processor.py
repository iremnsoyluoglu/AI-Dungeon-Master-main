"""
Document Processor for RAG System
Handles document loading, chunking, and metadata management.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
import os
from typing import List, Dict, Any

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
    
    def load_document(self, file_path: str):
        """Loads document based on file type"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            loader = PyPDFLoader(file_path)
        elif file_extension == '.txt':
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        return loader.load()
    
    def chunk_document(self, documents):
        """Splits documents into chunks"""
        return self.text_splitter.split_documents(documents)
    
    def process_uploaded_file(self, file_path: str):
        """Complete document processing pipeline"""
        # 1. Load document
        documents = self.load_document(file_path)
        
        # 2. Split into chunks
        chunks = self.chunk_document(documents)
        
        # 3. Add metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata['chunk_id'] = i
            chunk.metadata['source'] = file_path
            chunk.metadata['file_type'] = os.path.splitext(file_path)[1].lower()
        
        return chunks
    
    def validate_document(self, file_path: str) -> Dict[str, Any]:
        """Validates document before processing"""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return {"valid": False, "error": "File does not exist"}
            
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > 50 * 1024 * 1024:  # 50MB limit
                return {"valid": False, "error": "File too large (max 50MB)"}
            
            # Check file extension
            file_extension = os.path.splitext(file_path)[1].lower()
            supported_extensions = ['.pdf', '.txt']
            if file_extension not in supported_extensions:
                return {"valid": False, "error": f"Unsupported file type: {file_extension}"}
            
            return {"valid": True, "file_size": file_size, "file_type": file_extension}
            
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    def get_document_info(self, file_path: str) -> Dict[str, Any]:
        """Gets basic information about the document"""
        try:
            validation = self.validate_document(file_path)
            if not validation["valid"]:
                return validation
            
            documents = self.load_document(file_path)
            chunks = self.chunk_document(documents)
            
            return {
                "valid": True,
                "file_path": file_path,
                "file_size": validation["file_size"],
                "file_type": validation["file_type"],
                "total_pages": len(documents),
                "total_chunks": len(chunks),
                "average_chunk_size": sum(len(chunk.page_content) for chunk in chunks) / len(chunks) if chunks else 0
            }
            
        except Exception as e:
            return {"valid": False, "error": str(e)}
