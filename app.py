import streamlit as st
import pandas as pd
import plotly.express as px
from scripts import fetch_reddit_data, process_reddit_data, DatabaseManager
from datetime import datetime, timedelta
import re


@st.cache_resource
def get_db_manager():
    return DatabaseManager()

db_manager = get_db_manager()
        
def get_stock_sentiment(stock_symbol):
    # Fetch data for the specific stock from the database
    df = db_manager.fetch_stock_data(stock_symbol)
        
    # Calculate overall sentiment score
    overall_score = df['sentiment_score'].mean()
    
    # Determine if bullish or bearish
    sentiment = "Bullish" if overall_score > 0 else "Bearish"
    
    # Calculate sentiment distribution
    sentiment_dist = df['sentiment'].value_counts(normalize=True).to_dict()
    
    return {
        'overall_score': overall_score,
        'sentiment': sentiment,
        'sentiment_dist': sentiment_dist,
        'data': df
    }

def main():
    st.title("Reddit Stock Sentiment Analyzer")

    # Sidebar for configuration
    st.sidebar.title("Configuration")
      
    # Display last update time
    st.sidebar.write(f"Last data update: 7 days ago")
    update_button = st.sidebar.button("Update Data")
    delete_button = st.sidebar.button("Delete Data")
    analyze_sentiment = st.sidebar.button("Analyze Sentiment")
    
    # User input for stock symbol
    stock_symbol = st.text_input("Enter stock symbol (e.g., MSFT):").upper()
    df = pd.DataFrame(fetch_reddit_data("stocks"))
    
    if analyze_sentiment:
        a = get_stock_sentiment(stock_symbol)
    
    if update_button:
        st.text(df)
                              
    if delete_button:
        db_manager.delete_data()
        st.sidebar.write(f"Data deleted at {datetime.now()}")
        
    if stock_symbol:
        symbol_pattern = r'\b' + re.escape(stock_symbol) + r'\b'
        df = df[df['body'].str.contains(symbol_pattern, case=False, regex=True)]
        st.write(df)

if __name__ == "__main__":
    main()