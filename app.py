import streamlit as st
import pandas as pd
import plotly.express as px
from models.transformer_model import SentimentAnalyzer
from scripts import fetch_reddit_data, process_reddit_data, DatabaseManager
from datetime import datetime, timedelta
import re

@st.cache_resource
def get_db_manager():
    return DatabaseManager()

@st.cache_resource
def get_sentiment_analyzer():
    return SentimentAnalyzer()

db_manager = get_db_manager()
sentiment_analyzer = get_sentiment_analyzer()

def get_stock_symbol(stock_symbol, df):
    symbol_pattern = r'\b' + re.escape(stock_symbol) + r'\b'
    return df[df['body'].str.contains(symbol_pattern, case=False, regex=True)]

def analyze_sentiment(texts):
    sentiments = []
    scores = []
    for text in texts:
        try:
            label, score = sentiment_analyzer.predict(text)
            sentiments.append(label)
            scores.append(score)
        except Exception as e:
            print(f"Error analyzing text: {text[:50]}... Error: {str(e)}")
            sentiments.append("ERROR")
            scores.append(0.0)
    
    return pd.DataFrame({'text': texts, 'sentiment': sentiments, 'score': scores})

def plot_sentiment_distribution(sentiment_df):
    fig = px.pie(sentiment_df, names='sentiment', title='Sentiment Distribution')
    return fig

def plot_sentiment_over_time(df):
    df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')
    df = df.sort_values('created_utc')
    fig = px.line(df, x='created_utc', y='sentiment', title='Sentiment Over Time')
    return fig

def main():
    st.title("Reddit Stock Sentiment Analyzer")
    
    stock_symbol = st.text_input("Enter stock symbol (e.g., MSFT):").upper()
    
    if stock_symbol:
        with st.spinner("Fetching data..."):
            df = pd.DataFrame(fetch_reddit_data("stocks"))
            wallstreetbets_df = pd.DataFrame(fetch_reddit_data("wallstreetbets"))
            #df = pd.concat([stocks_df, wallstreetbets_df])
            symbol_df = get_stock_symbol(stock_symbol, df)
        
        if symbol_df.empty:
            st.warning(f"No comments found for {stock_symbol}.")
        else:
            st.subheader("Reddit Comments")
            st.dataframe(symbol_df[[ 'body', 'created_utc']])
            
            with st.spinner("Analyzing sentiment..."):
                texts = symbol_df['body'].tolist()
                print(texts)
                sentiment_df = analyze_sentiment(texts)
                symbol_df['sentiment'] = sentiment_df['sentiment']
                symbol_df['sentiment'] = symbol_df['sentiment'].map({'positive': 1, 'neutral': 0, 'negative': -1})
            
            st.subheader("Sentiment Analysis Results")
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(plot_sentiment_distribution(sentiment_df))
            
            with col2:
                st.plotly_chart(plot_sentiment_over_time(symbol_df))
            
            st.subheader("Key Statistics")
            total_comments = len(symbol_df)
            positive_ratio = (symbol_df['sentiment'] == 'positive').mean()
            negative_ratio = (symbol_df['sentiment'] == 'negative').mean()
            neutral_ratio = (symbol_df['sentiment'] == 'neutral').mean()
            
            st.write(f"Total comments analyzed: {total_comments}")
            st.write(f"Positive sentiment: {positive_ratio:.2%}")
            st.write(f"Negative sentiment: {negative_ratio:.2%}")
            st.write(f"Neutral sentiment: {neutral_ratio:.2%}")
            
            st.subheader("Most Recent Comments")
            st.dataframe(symbol_df.sort_values('created_utc', ascending=False).head(5)[[ 'body', 'sentiment', 'created_utc']])

if __name__ == "__main__":
    main()