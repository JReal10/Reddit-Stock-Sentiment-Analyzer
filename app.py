import streamlit as st
import pandas as pd
import plotly.express as px
from models.transformer_model import SentimentAnalyzer
from scripts import fetch_reddit_data, process_reddit_data ,DatabaseManager
from utils import get_stock_symbol, plot_sentiment_distribution, plot_sentiment_over_time
import re
from datetime import datetime, timedelta

#@st.cache_resource
def get_db_manager():
    return DatabaseManager()

@st.cache_resource
def get_sentiment_analyzer():
    return SentimentAnalyzer()

db_manager = get_db_manager()
sentiment_analyzer = get_sentiment_analyzer()
 
def analyze_sentiment(texts):
    sentiments = []
    scores = []
    for text in texts:
        label, score = sentiment_analyzer.predict(text)
        sentiments.append(label)
        scores.append(score)

    return pd.DataFrame({'text': texts, 'sentiment': sentiments, 'score': scores})

def main():
    st.title("Stock Sentiment Analyzer")
    
    # Add sidebar for subreddit selection
    st.sidebar.header("Settings")
    
    subreddit_options = ["stocks", "wallstreetbets"]
    selected_subreddits = st.sidebar.multiselect(
        "Choose subreddit(s) to analyze:",
        options=subreddit_options,
        default=["stocks"]
    )
    
        
    # Date range selection
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)  # Default to last 30 days
    
    start_date = st.sidebar.date_input("Start date", start_date)
    end_date = st.sidebar.date_input("End date", end_date)
    
    if start_date > end_date:
        st.sidebar.error("Error: End date must be after start date.")
        return
    
    stock_symbol = st.text_input("Enter stock symbol (e.g., MSFT):").upper()

    if stock_symbol and selected_subreddits:
        with st.spinner("Fetching data..."):
            # Fetch data from selected subreddits
            df = pd.DataFrame()
            for subreddit in selected_subreddits:
                df = pd.Dataframe(fetch_reddit_data(subreddit, start_date, end_date))
                #db_manager.insert_data(subreddit_df)
            
            #df = db_manager.fetch_data()            
            symbol_df = get_stock_symbol(stock_symbol, df)
        
        if symbol_df.empty:
            st.warning(f"No comments found for {stock_symbol} in the selected subreddits.")
        else:
            st.subheader("Reddit Comments")
            st.dataframe(symbol_df.head(5)[['body', 'created_utc']])
            
            with st.spinner("Analyzing sentiment..."):
                texts = symbol_df['body'].tolist()
                sentiment_df = analyze_sentiment(texts)
                symbol_df['sentiment'] = sentiment_df['sentiment']
                symbol_df['sentiment_score'] = sentiment_df['sentiment'].map({'positive': 1, 'neutral': 0, 'negative': -1})
            
            st.subheader("Sentiment Analysis Results")
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(plot_sentiment_distribution(sentiment_df))
            
            with col2:
                st.plotly_chart(plot_sentiment_over_time(symbol_df))

if __name__ == "__main__":
    main()