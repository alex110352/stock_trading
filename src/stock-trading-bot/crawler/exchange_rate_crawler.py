from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

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

def get_exchange_df():

    soup = get_exchange_html()

    if soup == 'connect failed':
        return 'connect failed'

    exchange_df = pd.DataFrame()

    for num in range(len(soup.find_all("div",class_="visible-phone print_hide"))):

        name = soup.find_all("div",class_="visible-phone print_hide")[num].text.strip().split("\r\n")[0].split(" ")[0]
        currency = soup.find_all("div",class_="visible-phone print_hide")[num].text.strip().split("\r\n")[0].split(" ")[1][1:-1]
        bought_cash = soup.find_all('td',attrs={'data-table':'本行現金買入'})[num].text
        sold_cash = soup.find_all('td',attrs={'data-table':'本行現金賣出'})[num].text
        bought_spot = soup.find_all('td',attrs={'data-table':'本行即期買入'})[num].text
        sold_spot = soup.find_all('td',attrs={'data-table':'本行即期賣出'})[num].text

        exchange_series = pd.Series({"name":name,"currency":currency,"bought_cash":bought_cash,"sold_cash":sold_cash,"currency_bought_spot":bought_spot,"currency_sold_spot":sold_spot,},name=num)
        exchange_df = exchange_df.append(exchange_series)

    exchange_df = exchange_df.replace('-','NaN')

    return exchange_df

def get_exchange_rate(currency_name="NaN"):

    exchange_df = get_exchange_df() 

    if str(type(exchange_df)) != "<class 'pandas.core.frame.DataFrame'>":
        return 'connect failed'

    if currency_name in list(exchange_df['currency']):
        return exchange_df[exchange_df['currency'] == currency_name] 
    elif currency_name in list(exchange_df['name']):
        return exchange_df[exchange_df['name'] == currency_name] 
    else :
        return exchange_df[['name','currency']]