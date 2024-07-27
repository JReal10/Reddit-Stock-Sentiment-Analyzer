import pandas as pd
import psycopg2
from psycopg2 import sql

# scripts/reddit_scraper.py
import sys
import os

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(project_root)  

from config import config
    
def connect_to_db():
    """Establish connection to PostgreSQL database"""
    return psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT
    )
    
def test():
  text = "Hello"
  
  return str(text)

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

def CleanData(df):
  #Makes the text lowercase
  df.loc[:, 'body'] = df['body'].str.lower()
  
  #Removes any special characters
  df.loc[:, 'body'] = df['body'].str.replace(r'\W+', ' ')
  
  # Remove rows with missing values
  df.loc[:, 'body'] = df[~df['body'].str.contains('\[removed\]|\[deleted\]', na=False, regex = True)]
  
  #Replacing the Paragraph Brake
  df.loc[:, 'body'] = df['body'].str.replace('\n', ' ')
  
  #Removing the URL
  df.loc[:, 'body'] = df['body'].str.replace(r'http\S+', '')
  
  # Removing other subreddit mentions  
  df.loc[:, 'body'] = df['body'].str.replace(r'r/[\w]+', '')
  
  #Removing the User
  df.loc[:, 'body'] = df['body'].str.replace(r'@\w+', '')
  df = df.reset_index(drop=True)
  
  return df

def LoadNLTK():
  nltk.download('stopwords')
  nltk.download('punkt')
  nltk.download('wordnet')



def text_preprocessing(txt):
  # Initialize the lemmatizer and stop words
  stop_words = set(stopwords.words('english'))
  lemmatizer = WordNetLemmatizer()

  # Tokenize the text
  word_tokens = word_tokenize(txt)

  # Remove stop words
  filtered_words = [w for w in word_tokens if w not in stop_words]

  # Stem or Lemmatize each word
  lemmatized_words = [lemmatizer.lemmatize(w) for w in filtered_words]

  # Join the words back into a single string
  return ' '.join(lemmatized_words)

  
def main():
  LoadNLTK()
  df = read_database()
  df = CleanData(df)
  
  #text_preprocessing(df['body'][0])
   
if __name__ == "__main__":
    main()