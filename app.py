import streamlit as st
import pandas as pd
from models.transformer_model import SentimentAnalyzer
from utils.helpers import plot_sentiment_distribution, filter_comments_by_symbol
from scripts import fetch_reddit_data
import plotly.graph_objects as go

# Caching the sentiment analyzer model for reusability
@st.cache_resource
def get_sentiment_analyzer():
    return SentimentAnalyzer()

# Initialize the sentiment analyzer
sentiment_analyzer = get_sentiment_analyzer()

@st.cache_data
def reddit_data_to_dataframe(subreddit):
    return pd.DataFrame(fetch_reddit_data(subreddit))

# Perform sentiment analysis on a list of texts
def analyze_sentiment(texts):
    results = [sentiment_analyzer.predict(text) for text in texts]
    sentiments, scores = zip(*results)
    return pd.DataFrame({'text': texts, 'sentiment': sentiments, 'score': scores})


# Main Streamlit app function
def main():
    # Title and Introduction
    st.title("Stock Sentiment Analyzer")
    st.markdown("Analyze Reddit sentiment on popular stocks from the [r/wallstreetbets](https://www.reddit.com/r/wallstreetbets/) subreddit.")

    # Define default subreddit and get user input for stock symbol
    subreddit = "wallstreetbets"
    stock_symbol = st.text_input("Enter Stock Symbol (e.g., MSFT):").upper()

    if stock_symbol:
        with st.spinner("Fetching data..."):
            df = reddit_data_to_dataframe(subreddit)
            symbol_df = filter_comments_by_symbol(stock_symbol, df)
            total_comments = symbol_df.shape[0]

        if symbol_df.empty:
            st.warning(f"No data found for {stock_symbol} in {subreddit}.")
        else:
            with st.spinner("Analyzing sentiment..."):
                sentiment_df = analyze_sentiment(symbol_df['body'].tolist())
                symbol_df = pd.concat([symbol_df, sentiment_df[['sentiment']]], axis=1)
                symbol_df['sentiment_score'] = symbol_df['sentiment'].map({'positive': 1, 'neutral': 0, 'negative': -1})

            # Centered Sentiment Gauge Chart
            st.subheader(f"Sentiment Distribution of {stock_symbol} Over a Month")
            gauge_col1, gauge_col2, gauge_col3 = st.columns([1, 2, 1])  # Center gauge chart with blank columns

            with gauge_col2:
                st.plotly_chart(plot_sentiment_distribution(sentiment_df), use_container_width=True)

        # Display Top Comments
        st.subheader("Top Reddit Comments")

        # Iterate through the top 5 comments and display each with sentiment
        for i, row in symbol_df[['body', 'sentiment', 'created_utc']].head(5).iterrows():
            st.text_area(label=f"User {i + 1}", value=row['body'], height=100, key=f"comment_{i}")
            st.markdown(f"*Sentiment:* {row['sentiment'].capitalize()}")
            st.markdown(f"*Commented at:* {row['created_utc']}")
            st.write("---")  # Adds 

if __name__ == "__main__":
    main()


