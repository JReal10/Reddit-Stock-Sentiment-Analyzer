import pandas as pd
import numpy as np
import psycopg2
from psycopg2 import sql

from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
from scipy.special import softmax

# scripts/reddit_scraper.py
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from . import config
    
def connect_to_db():
    """Establish connection to PostgreSQL database"""
    return psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT
    )

def load_model(MODEL):
    """Load the model from Hugging Face model hub"""
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    return tokenizer, config, model

def get_sentiment(text, tokenizer, config, model):
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

def read_database():
    
    df = []

    """Save scraped df to PostgreSQL database"""
    conn = connect_to_db()
    cur = conn.cursor()
    
    # Read df from the existing table in the database
    read_query = sql.SQL("""
      SELECT body FROM reddit_comments
    """)
    cur.execute(read_query)
    result = cur.fetchall()
    for row in result:
      df.append(row[0])
      
    conn.commit()
    cur.close()
    conn.close()
    
    return pd.DataFrame(df, columns=['body'])
    

def main():
  MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
  df = read_database()
  tokenizer, config, model = load_model(MODEL)
  get_sentiment(df['body'][0], tokenizer, config, model)
      
if __name__ == "__main__":
    main()