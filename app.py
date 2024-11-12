import streamlit as st
import pandas as pd
from models.transformer_model import SentimentAnalyzer
from utils.helpers import plot_sentiment_distribution, plot_sentiment_over_time, filter_comments_by_symbol
from scripts import fetch_reddit_data

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
    st.title("Stock Sentiment Analyzer")
    subreddit = "wallstreetbets"

    # Stock symbol input
    stock_symbol = st.text_input("Enter stock symbol (e.g., MSFT):").upper()

    if stock_symbol and subreddit:
        with st.spinner("Fetching data..."):
            # Fetch and concatenate data from selected subreddits
            df = reddit_data_to_dataframe(subreddit)
            # Filter comments by stock symbol
            symbol_df = filter_comments_by_symbol(stock_symbol, df)
            st.write(f"Comment Analyzed{symbol_df.count()}")

        if symbol_df.empty:
            st.warning(f"Not enough data for {stock_symbol} in the selected subreddits.")
        else:
            st.subheader("Reddit Comments")
            st.dataframe(symbol_df.head(5))

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
