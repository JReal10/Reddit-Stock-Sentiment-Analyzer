# utils/helpers.py

import re
import pandas as pd
import plotly.express as px

def get_stock_symbol(stock_symbol, df):
    symbol_pattern = r'\b' + re.escape(stock_symbol) + r'\b'
    symbol_df = df[df['body'].str.contains(symbol_pattern, case=False, regex=True)]
    return symbol_df.reset_index(drop=True)

def process_dataframe(df, stock_symbol):
    symbol_df = get_stock_symbol(stock_symbol, df)
    if not symbol_df.empty:
        symbol_df['created_utc'] = pd.to_datetime(symbol_df['created_utc'], unit='s')
        symbol_df = symbol_df.sort_values('created_utc')
    return symbol_df

def plot_sentiment_distribution(sentiment_df):
    return px.pie(sentiment_df, names='sentiment', title='Sentiment Distribution')

def plot_sentiment_over_time(df):
    return px.scatter(df, x='created_utc', y='sentiment_score', color='sentiment', title='Sentiment Over Time')


