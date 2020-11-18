import requests
import pandas as pd

from bs4 import BeautifulSoup

def get_exchange_html():

    try:
        url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
        r = requests.get(url,timeout=10).text
        soup = BeautifulSoup(r,'lxml')
    except ConnectionError :
        return 'connect failed'
    else:
        return soup

def get_exchange_df(soup):

    exchange_df = pd.DataFrame()
    for num in range(len(soup.find_all("div",class_="visible-phone print_hide"))):

        name = soup.find_all("div",class_="visible-phone print_hide")[num].text.strip().split("\r\n")[0].split(" ")[0]
        currency = soup.find_all("div",class_="visible-phone print_hide")[num].text.strip().split("\r\n")[0].split(" ")[1][1:-1]
        bought_cash_exchange_rate = soup.find_all('td',attrs={'data-table':'本行現金買入'})[num].text
        sold_cash_exchange_rate = soup.find_all('td',attrs={'data-table':'本行現金賣出'})[num].text
        bought_spot_exchange_rate = soup.find_all('td',attrs={'data-table':'本行即期買入'})[num].text
        sold_spot_exchange_rate = soup.find_all('td',attrs={'data-table':'本行即期賣出'})[num].text

        exchange_series = pd.Series({"name":name,"currency":currency,"bought_cash_exchange_rate":bought_cash_exchange_rate,"sold_cash_exchange_rate":sold_cash_exchange_rate,"currencybought_spot_exchange_rate":bought_spot_exchange_rate,"sold_spot_exchange_rate":sold_spot_exchange_rate,},name=num)
        exchange_df = exchange_df.append(exchange_series)

    exchange_df = exchange_df.replace('-','NaN')

    return exchange_df

def get_exchange_rate(exchange_df,currency_name):

    if currency_name in list(exchange_df['currency']):
        return exchange_df[exchange_df['currency'] == currency_name] 
    elif currency_name in list(exchange_df['name']):
        return exchange_df[exchange_df['name'] == currency_name] 
    else :
        return exchange_df[['name','currency']]


