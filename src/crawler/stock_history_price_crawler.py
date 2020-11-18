import yfinance as yf
import pandas as pd

def get_history_data(stock_ID,start_date,end_date):

    data = yf.Ticker(stock_ID)
    df = data.history(period="max")
    df.reset_index(inplace=True)
    history_data = df[(df['Date'] > start_date) & (df['Date'] < end_date)].iloc[:,:-2]

    return history_data

