import streamlit as st
import pandas as pd
import plotly.express as px
from models.transformer_model import SentimentAnalyzer
from scripts import fetch_reddit_data
import re
from datetime import datetime, timedelta

# Caching the sentiment analyzer model for reusability
@st.cache_resource
def get_sentiment_analyzer():
    return SentimentAnalyzer()

# Initialize the sentiment analyzer
sentiment_analyzer = get_sentiment_analyzer()

# Helper function to filter comments by stock symbol
def filter_comments_by_symbol(stock_symbol, df):
    symbol_pattern = r'\b' + re.escape(stock_symbol) + r'\b'
    return df[df['body'].str.contains(symbol_pattern, case=False, regex=True)].reset_index(drop=True)

# Perform sentiment analysis on a list of texts
def analyze_sentiment(texts):
    results = [sentiment_analyzer.predict(text) for text in texts]
    sentiments, scores = zip(*results)
    return pd.DataFrame({'text': texts, 'sentiment': sentiments, 'score': scores})

# Plot the distribution of sentiments
def plot_sentiment_distribution(sentiment_df):
    return px.pie(sentiment_df, names='sentiment', title='Sentiment Distribution')

# Plot the sentiment score trend over time
def plot_sentiment_over_time(df):
    df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')
    df = df.sort_values('created_utc')
    return px.line(df, x='created_utc', y='sentiment_score', title='Sentiment Over Time')

# Main Streamlit app function
def main():
    st.title("Stock Sentiment Analyzer")

    # Sidebar for settings
    st.sidebar.header("Settings")
    subreddit_options = ["stocks", "stockmarket"]
    selected_subreddits = st.sidebar.multiselect("Choose subreddit(s) to analyze:", options=subreddit_options, default=["stocks", "stockmarket"])

    # Date range selection
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    start_date = st.sidebar.date_input("Start date", start_date)
    end_date = st.sidebar.date_input("End date", end_date)

    if start_date > end_date:
        st.sidebar.error("Error: End date must be after start date.")
        return

    # Stock symbol input
    stock_symbol = st.text_input("Enter stock symbol (e.g., MSFT):").upper()

    if stock_symbol and selected_subreddits:
        with st.spinner("Fetching data..."):
            # Fetch and concatenate data from selected subreddits
            df = pd.concat([
                pd.DataFrame(fetch_reddit_data(subreddit, start_date, end_date)).assign(source=subreddit)
                for subreddit in selected_subreddits
            ], ignore_index=True)

            # Filter comments by stock symbol
            symbol_df = filter_comments_by_symbol(stock_symbol, df)

        if symbol_df.empty:
            st.warning(f"No comments found for {stock_symbol} in the selected subreddits.")
        else:
            st.subheader("Reddit Comments")
            st.dataframe(symbol_df[['body', 'created_utc', 'source']].head(5))

            with st.spinner("Analyzing sentiment..."):
                sentiment_df = analyze_sentiment(symbol_df['body'].tolist())
                symbol_df = pd.concat([symbol_df, sentiment_df[['sentiment', 'score']]], axis=1)
                symbol_df['sentiment_score'] = symbol_df['sentiment'].map({'positive': 1, 'neutral': 0, 'negative': -1})

            # Sentiment Analysis Results
            st.subheader("Sentiment Analysis Results")
            col1, col2 = st.columns(2)

            with col1:
                st.plotly_chart(plot_sentiment_distribution(sentiment_df))

            with col2:
                st.plotly_chart(plot_sentiment_over_time(symbol_df))

if __name__ == "__main__":
    main()