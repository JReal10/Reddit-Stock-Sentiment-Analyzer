import pandas as pd
import numpy as np

#from transformers import AutoModelForSequenceClassification
#from transformers import AutoTokenizer, AutoConfig
#from scipy.special import softmax

from transformers import pipeline
import torch
    
class SentimentAnalyzer:
  def __init__(self):
    device = 0 if torch.cuda.is_available() else -1
    self.model = pipeline('sentiment-analysis', model = "cardiffnlp/twitter-roberta-base-sentiment", device=device)
  
  def predict(self, text):
    result = self.model(text)[0]
    return result['label'], result['score']


#def load_model(MODEL):
    """Load the model from Hugging Face model hub"""
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    return tokenizer, config, model

#def get_sentiment(text, tokenizer, config, model):
    # Tokenize the input text
    encoded_input = tokenizer(text, return_tensors='pt', padding='max_length', truncation=True, max_length=512)  # Pad and truncate to 3625 tokens)
    
    # Get model output
    output = model(**encoded_input)
    
    # Calculate softmax scores
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    # Get the predicted label and its score
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    predicted_label = config.id2label[ranking[0]]
    predicted_score = scores[ranking[0]]

    return predicted_label, predicted_score