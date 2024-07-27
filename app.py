import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from scripts import DatabaseManager, fetch_reddit_data, process_reddit_data
from models import SentimentAnalyzer

def main():
  
  #db_manager = DatabaseManager()
  #data = db_manager.fetch_data()
  data = fetch_reddit_data('stocks')
  df = process_reddit_data(data)
  print(df[0])
  
  text = 'This is the worst thing ever'
  sentiment_analyzer = SentimentAnalyzer()
  prediction = sentiment_analyzer.predict(text)
  
  st.write(text)
  st.write(prediction)
  
  ticker = st.sidebar.text_input("Enter Ticker", "AAPL")
  start_date = st.sidebar.date_input("Start Date")
  end_date = st.sidebar.date_input("End Date", datetime.today())

if __name__ == "__main__":
  main()
