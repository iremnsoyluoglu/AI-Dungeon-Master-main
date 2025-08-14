"""
Fine-tuning Pipeline for RAG System
Handles model training and optimization for custom datasets.
"""

import json
import os
from typing import List, Dict, Any
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from datasets import Dataset
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FineTuningPipeline:
    def __init__(self, model_name: str = "gpt2"):
        self.model_name = model_name
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Move model to device
            self.model.to(self.device)
            
        except Exception as e:
            logger.error(f"Failed to initialize model: {str(e)}")
            raise
    
    def prepare_dataset(self, training_data: List[Dict]) -> Dataset:
        """Prepares dataset for fine-tuning"""
        try:
            # Convert to HuggingFace dataset format
            dataset = Dataset.from_list(training_data)
            
            def tokenize_function(examples):
                # Combine instruction, input, and output
                texts = []
                for i in range(len(examples['instruction'])):
                    text = f"Instruction: {examples['instruction'][i]}\n"
                    if examples.get('input') and examples['input'][i]:
                        text += f"Input: {examples['input'][i]}\n"
                    text += f"Output: {examples['output'][i]}"
                    texts.append(text)
                
                return self.tokenizer(
                    texts,
                    truncation=True,
                    padding=True,
                    max_length=512,
                    return_tensors="pt"
                )
            
            tokenized_dataset = dataset.map(tokenize_function, batched=True)
            return tokenized_dataset
            
        except Exception as e:
            logger.error(f"Failed to prepare dataset: {str(e)}")
            raise
    
    def fine_tune(self, training_data: List[Dict], output_dir: str, **kwargs):
        """Performs fine-tuning with custom parameters"""
        try:
            # 1. Prepare dataset
            logger.info("Preparing dataset...")
            dataset = self.prepare_dataset(training_data)
            
            # 2. Define training arguments with defaults
            training_args = TrainingArguments(
                output_dir=output_dir,
                num_train_epochs=kwargs.get('num_epochs', 3),
                per_device_train_batch_size=kwargs.get('batch_size', 4),
                save_steps=kwargs.get('save_steps', 1000),
                save_total_limit=kwargs.get('save_total_limit', 2),
                logging_steps=kwargs.get('logging_steps', 100),
                learning_rate=kwargs.get('learning_rate', 5e-5),
                warmup_steps=kwargs.get('warmup_steps', 500),
                weight_decay=kwargs.get('weight_decay', 0.01),
                fp16=kwargs.get('fp16', True),
                gradient_accumulation_steps=kwargs.get('gradient_accumulation_steps', 1),
                evaluation_strategy=kwargs.get('evaluation_strategy', 'no'),
                load_best_model_at_end=kwargs.get('load_best_model_at_end', False),
                metric_for_best_model=kwargs.get('metric_for_best_model', 'loss'),
                greater_is_better=kwargs.get('greater_is_better', False),
            )
            
            # 3. Initialize trainer
            trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=dataset,
                tokenizer=self.tokenizer,
            )
            
            # 4. Start training
            logger.info("Starting fine-tuning...")
            trainer.train()
            
            # 5. Save model
            logger.info("Saving model...")
            trainer.save_model()
            self.tokenizer.save_pretrained(output_dir)
            
            # 6. Save training metadata
            self.save_training_metadata(output_dir, training_data, kwargs)
            
            return {
                "success": True,
                "message": f"Model fine-tuned and saved to {output_dir}",
                "output_dir": output_dir,
                "training_samples": len(training_data)
            }
            
        except Exception as e:
            logger.error(f"Fine-tuning failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def save_training_metadata(self, output_dir: str, training_data: List[Dict], training_params: Dict):
        """Saves training metadata for future reference"""
        metadata = {
            "model_name": self.model_name,
            "training_samples": len(training_data),
            "training_parameters": training_params,
            "device_used": str(self.device),
            "model_config": self.model.config.to_dict()
        }
        
        metadata_path = os.path.join(output_dir, "training_metadata.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def load_fine_tuned_model(self, model_path: str):
        """Loads a fine-tuned model"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForCausalLM.from_pretrained(model_path)
            self.model.to(self.device)
            
            return {"success": True, "message": f"Model loaded from {model_path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_text(self, prompt: str, max_length: int = 100) -> str:
        """Generates text using the fine-tuned model"""
        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=max_length,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return generated_text
            
        except Exception as e:
            logger.error(f"Text generation failed: {str(e)}")
            return f"Generation failed: {str(e)}"
    
    def evaluate_model(self, test_data: List[Dict]) -> Dict[str, Any]:
        """Evaluates the fine-tuned model on test data"""
        try:
            correct_predictions = 0
            total_predictions = len(test_data)
            
            for item in test_data:
                prompt = f"Instruction: {item['instruction']}\n"
                if item.get('input'):
                    prompt += f"Input: {item['input']}\n"
                prompt += "Output:"
                
                generated = self.generate_text(prompt, max_length=200)
                
                # Simple evaluation - check if key words from expected output are in generated text
                expected_keywords = item['output'].lower().split()[:5]  # First 5 words
                generated_lower = generated.lower()
                
                if any(keyword in generated_lower for keyword in expected_keywords):
                    correct_predictions += 1
            
            accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
            
            return {
                "success": True,
                "accuracy": accuracy,
                "correct_predictions": correct_predictions,
                "total_predictions": total_predictions
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_model_info(self) -> Dict[str, Any]:
        """Gets information about the current model"""
        try:
            return {
                "model_name": self.model_name,
                "device": str(self.device),
                "model_parameters": sum(p.numel() for p in self.model.parameters()),
                "trainable_parameters": sum(p.numel() for p in self.model.parameters() if p.requires_grad),
                "vocab_size": self.tokenizer.vocab_size,
                "max_length": self.tokenizer.model_max_length
            }
        except Exception as e:
            return {"error": str(e)}
