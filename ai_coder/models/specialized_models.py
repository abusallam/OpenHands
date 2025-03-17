from typing import Dict, List, Optional
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import numpy as np

class SpecializedAIModels:
    """
    Enhanced AI model management with specialized models.
    
    Features:
    - Multiple specialized models
    - Model ensembling
    - Task-specific optimization
    - Automatic model selection
    - Performance monitoring
    """

    def __init__(self):
        self.models = {
            # Code Generation Models
            "codegen": AutoModelForCausalLM.from_pretrained("codegen-16B-mono"),
            "gpt_neo": AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-2.7B"),
            "codet5": AutoModelForCausalLM.from_pretrained("Salesforce/codet5-base"),
            
            # Code Understanding Models
            "codebert": AutoModelForCausalLM.from_pretrained("microsoft/codebert-base"),
            "graphcodebert": AutoModelForCausalLM.from_pretrained("microsoft/graphcodebert-base"),
            
            # Documentation Models
            "docstring": AutoModelForCausalLM.from_pretrained("microsoft/codebert-base-mlm"),
            
            # Bug Detection Models
            "bug_detector": AutoModelForCausalLM.from_pretrained("microsoft/codebert-base-bug-detection"),
            
            # Code Review Models
            "code_reviewer": AutoModelForCausalLM.from_pretrained("microsoft/codebert-base-review"),
            
            # Test Generation Models
            "test_generator": AutoModelForCausalLM.from_pretrained("microsoft/codebert-base-test"),
            
            # Security Analysis Models
            "security_analyzer": AutoModelForCausalLM.from_pretrained("microsoft/codebert-base-security"),
            
            # Performance Optimization Models
            "performance_optimizer": AutoModelForCausalLM.from_pretrained("performance-model")
        }
        
        self.tokenizers = {name: AutoTokenizer.from_pretrained(model.config.name_or_path) 
                          for name, model in self.models.items()}

    async def get_best_model(self, task_type: str, context: Dict[str, Any]) -> str:
        """Selects the best model for a specific task"""
        model_scores = await self._evaluate_models_for_task(task_type, context)
        return max(model_scores.items(), key=lambda x: x[1])[0]

    async def generate_with_ensemble(self,
                                   prompt: str,
                                   models: List[str],
                                   weights: Optional[List[float]] = None) -> str:
        """Generates code using multiple models with weighted ensemble"""
        if weights is None:
            weights = [1.0 / len(models)] * len(models)
            
        results = []
        for model_name in models:
            model = self.models[model_name]
            tokenizer = self.tokenizers[model_name]
            
            inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
            outputs = model.generate(**inputs, max_length=512)
            decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
            results.append(decoded)
            
        # Combine results using weights
        return await self._combine_results(results, weights) 