import yfinance as yf
import pandas as pd

def get_history_data(stock_ID='NaN',start_date='NaN',end_date='NaN'):

    if stock_ID == 'NaN':
        return 'please input symbol'
    try:
        data = yf.Ticker(stock_ID)
    except AttributeError:
        return 'please input symbol'


    df = data.history(period="max")
    if len(df) == 0:
        return 'symbol error'

    df.reset_index(inplace=True)

    if start_date == 'NaN' and end_date == 'NaN':
        history_data = df.iloc[:,:-2]
    elif start_date == 'NaN':
        history_data = df[df['Date'] < end_date].iloc[:,:-2]
    elif end_date == 'NaN':
        history_data = df[df['Date'] > start_date].iloc[:,:-2]
    else:
        history_data = df[(df['Date'] > start_date) & (df['Date'] < end_date)].iloc[:,:-2]

    return history_data
