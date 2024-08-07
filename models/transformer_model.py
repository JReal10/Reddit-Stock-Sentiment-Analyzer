import pandas as pd
import numpy as np
from transformers import pipeline
import torch

class SentimentAnalyzer:
    def __init__(self):
        device = 0 if torch.cuda.is_available() else -1
        self.model = pipeline('sentiment-analysis', model="cardiffnlp/twitter-roberta-base-sentiment", device=device)
        self.label_map = {
            'LABEL_0': 'negative',
            'LABEL_1': 'neutral',
            'LABEL_2': 'positive'
        }
  
    def predict(self, text):
        result = self.model(text)[0]
        mapped_label = self.label_map[result['label']]
        return mapped_label, result['score']