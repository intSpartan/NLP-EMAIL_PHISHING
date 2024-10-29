from typing import Dict, List
import math
import random

class PhishingDetector:
    def __init__(self):
        self.weights = {}
        self.bias = 0
        self.learning_rate = 0.01
    
    def sigmoid(self, x: float) -> float:
        try:
            return 1 / (1 + math.exp(-x))
        except OverflowError:
            return 0 if x < 0 else 1
    
    def train(self, features_list: List[Dict[str, float]], labels: List[int], epochs: int = 100):
        # Initialize weights
        if not self.weights:
            self.weights = {feature: random.uniform(-1, 1) 
                          for feature in features_list[0].keys()}
        
        for _ in range(epochs):
            for features, label in zip(features_list, labels):
                # Forward pass
                prediction = self.predict(features)
                
                # Backward pass
                error = label - prediction
                
                # Update weights
                for feature, value in features.items():
                    self.weights[feature] += self.learning_rate * error * value
                self.bias += self.learning_rate * error
    
    def predict(self, features: Dict[str, float]) -> float:
        z = sum(self.weights[feature] * value 
                for feature, value in features.items()) + self.bias
        return self.sigmoid(z)
    
    def classify(self, features: Dict[str, float], threshold: float = 0.5) -> bool:
        return self.predict(features) >= threshold