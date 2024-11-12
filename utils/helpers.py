# utils/helpers.py

import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Helper function to filter comments by stock symbol
def filter_comments_by_symbol(stock_symbol, df):
    symbol_pattern = r'\b' + re.escape(stock_symbol) + r'\b'
    return df[df['body'].str.contains(symbol_pattern, case=False, regex=True)].reset_index(drop=True)

def plot_sentiment_distribution(sentiment_df):
    # Custom Gauge Chart Function
    positive_count = (sentiment_df['sentiment'] == 'positive').sum()
    neutral_count = (sentiment_df['sentiment'] == 'neutral').sum()
    negative_count = (sentiment_df['sentiment'] == 'negative').sum()
    total = positive_count + neutral_count + negative_count
    
    positive_percentage = positive_count / total * 100
    negative_percentage = negative_count / total * 100
    gauge_value = (positive_percentage - negative_percentage) / 2 + 50  # Scaled to 0-100

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=gauge_value,
        title={'text': ""},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#6A76FC"},
            'steps': [
                {'range': [0, 33], 'color': "#FD3216"},
                {'range': [33, 66], 'color': "#FF9616"},
                {'range': [66, 100], 'color': "#00FE35"},
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': gauge_value,
            }
        }
    ))
    fig.update_layout(width=350, height=300, margin=dict(l=0, r=0, t=0, b=0))
    return fig


def plot_sentiment_over_time(df):
    return px.scatter(df, x='created_utc', y='sentiment_score', color='sentiment', title='Sentiment Over Time')
