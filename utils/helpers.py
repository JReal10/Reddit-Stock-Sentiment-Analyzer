# utils/helpers.py

import re
import pandas as pd
import plotly.express as px

# Helper function to filter comments by stock symbol
def filter_comments_by_symbol(stock_symbol, df):
    symbol_pattern = r'\b' + re.escape(stock_symbol) + r'\b'
    return df[df['body'].str.contains(symbol_pattern, case=False, regex=True)].reset_index(drop=True)

def plot_sentiment_distribution(sentiment_df):
    return px.pie(sentiment_df, names='sentiment', title='Sentiment Distribution')

def plot_sentiment_over_time(df):
    return px.scatter(df, x='created_utc', y='sentiment_score', color='sentiment', title='Sentiment Over Time')
