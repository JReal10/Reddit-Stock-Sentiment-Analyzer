import streamlit as st
import pandas as pd
import plotly.express as px
import schedule
import time
import threading
from scripts import fetch_reddit_data, process_reddit_data, DatabaseManager
from datetime import datetime, timedelta


@st.cache_resource
def get_db_manager():
    return DatabaseManager()

db_manager = get_db_manager()

def fetch_and_process_data(subreddit):
    reddit_data = fetch_reddit_data(subreddit)
    processed_data = process_reddit_data(reddit_data)
    
    return processed_data
   # db_manager.save_data(processed_data)

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


    # User input for stock symbol
    stock_symbol = st.text_input("Enter stock symbol (e.g., MSFT):").upper()
    
    if update_button:
        d = fetch_and_process_data('wallstreetbets')
        redditdata = fetch_reddit_data('wallstreetbets')
        a = process_reddit_data(redditdata)
        st.text(a)
        #fetch_and_process_data('wallstreetbets')
                
    if delete_button:
        db_manager.delete_data()
        st.sidebar.write(f"Data deleted at {datetime.now()}")

    """if stock_symbol:
        sentiment_data = get_stock_sentiment(stock_symbol)
        
        if sentiment_data:
            st.header(f"Sentiment Analysis for {stock_symbol}")
            
            # Display overall sentiment
            st.metric("Overall Sentiment Score", f"{sentiment_data['overall_score']:.2f}")
            st.write(f"The overall sentiment for {stock_symbol} is **{sentiment_data['sentiment']}**")

            # Sentiment distribution pie chart
            fig_pie = px.pie(
                values=list(sentiment_data['sentiment_dist'].values()),
                names=list(sentiment_data['sentiment_dist'].keys()),
                title="Sentiment Distribution"
            )
            st.plotly_chart(fig_pie)

            # Sentiment over time line chart
            fig_line = px.line(
                sentiment_data['data'],
                x='created_utc',
                y='sentiment_score',
                title=f"{stock_symbol} Sentiment Over Time"
            )
            st.plotly_chart(fig_line)

            # Display recent posts
            st.subheader("Recent Posts")
            for _, row in sentiment_data['data'].sort_values('created_utc', ascending=False).head(5).iterrows():
                st.text(f"Date: {row['created_utc']}")
                st.text(f"Sentiment: {row['sentiment']} (Score: {row['sentiment_score']:.2f})")
                st.text(f"Text: {row['text'][:200]}...")
                st.markdown("---")
        else:
            st.warning(f"No data found for {stock_symbol}. Check the stock symbol or wait for the next data update.")"""

if __name__ == "__main__":
    main()