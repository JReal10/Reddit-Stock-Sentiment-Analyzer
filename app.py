import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from scripts import DatabaseManager, fetch_reddit_data


def main():
  
  db_manager = DatabaseManager()
  data = db_manager.fetch_data()
  test = st.write(data[1])
  
  ticker = st.sidebar.text_input("Enter Ticker", "AAPL")
  start_date = st.sidebar.date_input("Start Date")
  end_date = st.sidebar.date_input("End Date", datetime.today())

if __name__ == "__main__":
  main()
