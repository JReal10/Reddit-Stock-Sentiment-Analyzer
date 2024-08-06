import pandas as pd
from models import SentimentAnalyzer

def process_reddit_data(data):
  """"

  Args:
      data (list): Reddit data, including sentiment analysis

  Returns:
      list: Processed data with added sentiment analysis 
  """
  
  processed_data = []
  
  for post in data:
    sentiment, confidence = SentimentAnalyzer().predict(post['body'])

    processed_post = {
    'id': post['id'],
    'body': post['body'],
    'sentiment': sentiment,
    'confidence': confidence,
    'score': post['score'],
    'created_utc': post['created_utc'],
    'post_url':post['post_url'],
    }
    processed_data.append(processed_post)
    
    return processed_data

#import nltk
#from nltk.corpus import stopwords
#from nltk.stem import WordNetLemmatizer, PorterStemmer
#from nltk.tokenize import word_tokenize

#def CleanData(df):
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

#def LoadNLTK():
  nltk.download('stopwords')
  nltk.download('punkt')
  nltk.download('wordnet')

#def text_preprocessing(txt):
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