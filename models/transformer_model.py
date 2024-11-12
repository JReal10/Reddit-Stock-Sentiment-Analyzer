from transformers import pipeline, AutoTokenizer
import torch

class SentimentAnalyzer:
    def __init__(self):
        device = 0 if torch.cuda.is_available() else -1
        self.model_name = "cardiffnlp/twitter-roberta-base-sentiment"
        self.model = pipeline('sentiment-analysis', model=self.model_name, device=device)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.max_length = 512  # RoBERTa typically has a max length of 512 tokens
        self.label_map = {
            'LABEL_0': 'negative',
            'LABEL_1': 'neutral',
            'LABEL_2': 'positive'
        }
  
    def predict(self, text):
        # Directly pass the text to the pipeline
        result = self.model(text)[0]
        mapped_label = self.label_map[result['label']]
        
        return mapped_label, result['score']

