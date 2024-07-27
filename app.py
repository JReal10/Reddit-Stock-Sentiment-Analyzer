import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px


def main():
  
  #df = dp.read_database()
  #data = st.dataframe(df)
  #df = CleanData(df)
  
  ticker = st.sidebar.text_input("Enter Ticker", "AAPL")
  start_date = st.sidebar.date_input("Start Date")
  end_date = st.sidebar.date_input("End Date", datetime.today())

if __name__ == "__main__":
  main()
