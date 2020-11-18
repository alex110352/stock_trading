import pandas as pd
import requests
import time

from bs4 import BeautifulSoup

def get_html_text():

    try:
        url = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
        r = requests.get(url,timeout=20)
        html_text = BeautifulSoup(r.text,'lxml')
    except ConnectionError :
        return 'connect failed'
    else:
        return html_text

def get_finance_text(html_text):

    finance_text = []
    finance_htmls = html_text.find_all('td',attrs={"bgcolor": "#FAFAD2"})
    for finance_html in finance_htmls:
        finance_text.append(finance_html.text.strip())
    return finance_text

def get_subject_list_index(html_text,finance_text):

    subject_list = []
    subject_list_index = []

    subjects_html = html_text.find_all('td',attrs={"colspan": "7"})
    for subject_html in subjects_html:
        subject_list.append(subject_html.text.strip())

    for subject in subject_list:
        if finance_text.index(subject) in subject_list_index:
            tmp = finance_text
            tmp[tmp.index(subject)] = 'NaN'
            subject_list_index.append(tmp.index(subject))
        else:
            subject_list_index.append(finance_text.index(subject))
    
    return subject_list_index

def get_stock_df(finance_text,subject_list_index):

    stock_df = pd.DataFrame()
    for num in range((subject_list_index[1])//7):

        symbol = finance_text[7*num+1].split("\u3000")[0]
        name = finance_text[7*num+1].split("\u3000")[-1]
        industry = finance_text[7*num+5]

        stock_series = pd.Series({"symbol":symbol,"name":name,"industry":industry},name=num)
        stock_df = stock_df.append(stock_series)

    return stock_df

def get_call_warrant_df(finance_text,subject_list_index):

    call_warrant_df = pd.DataFrame()
    for num in range((subject_list_index[2]-subject_list_index[1])//7):

        symbol = finance_text[7*num+(subject_list_index[1]+1)].split("\u3000")[0]
        name = finance_text[7*num+(subject_list_index[1]+1)].split("\u3000")[-1]

        call_warrant_series = pd.Series({"symbol":symbol,"name":name},name=num)
        call_warrant_df = call_warrant_df.append(call_warrant_series)

    return call_warrant_df

def get_ETN_df(finance_text,subject_list_index):

    ETN_df = pd.DataFrame()
    for num in range((subject_list_index[3]-subject_list_index[2])//7):
        symbol = finance_text[7*num+(subject_list_index[2]+1)].split("\u3000")[0]
        name = finance_text[7*num+(subject_list_index[2]+1)].split("\u3000")[-1]

        ETN_series = pd.Series({"symbol":symbol,"name":name},name=num)
        ETN_df = ETN_df.append(ETN_series)

    return ETN_df

def get_preferred_stock_df(finance_text,subject_list_index):

    preferred_stock_df = pd.DataFrame()
    for num in range((subject_list_index[4]-subject_list_index[3])//7):
        symbol = finance_text[7*num+(subject_list_index[3]+1)].split("\u3000")[0]
        name = finance_text[7*num+(subject_list_index[3]+1)].split("\u3000")[-1]
        industry = finance_text[7*num+(subject_list_index[3]+5)]
        industry = 'NaN' if industry == '' else industry
            
        preferred_stock_series = pd.Series({"symbol":symbol,"name":name,"industry":industry},name=num)
        preferred_stock_df = preferred_stock_df.append(preferred_stock_series)
    
    return preferred_stock_df

def get_ETF_df(finance_text,subject_list_index):

    ETF_df = pd.DataFrame()
    for num in range((subject_list_index[5]-subject_list_index[4])//7):
        symbol = finance_text[7*num+(subject_list_index[4]+1)].split("\u3000")[0]
        name = finance_text[7*num+(subject_list_index[4]+1)].split("\u3000")[-1]
            
        ETF_series = pd.Series({"symbol":symbol,"name":name},name=num)
        ETF_df = ETF_df.append(ETF_series)
    
    return ETF_df

def get_ETN2_df(finance_text,subject_list_index):

    ETN2_df = pd.DataFrame()
    for num in range((subject_list_index[6]-subject_list_index[5])//7):
        symbol = finance_text[7*num+(subject_list_index[5]+1)].split("\u3000")[0]
        name = finance_text[7*num+(subject_list_index[5]+1)].split("\u3000")[-1]

        ETN2_series = pd.Series({"symbol":symbol,"name":name},name=num)
        ETN2_df = ETN2_df.append(ETN2_series)
    
    return ETN2_df

def get_TDR_df(finance_text,subject_list_index):

    TDR_df = pd.DataFrame()
    for num in range((subject_list_index[7]-subject_list_index[6])//7):
        symbol = finance_text[7*num+(subject_list_index[6]+1)].split("\u3000")[0]
        name = finance_text[7*num+(subject_list_index[6]+1)].split("\u3000")[-1]

        TDR_series = pd.Series({"symbol":symbol,"name":name},name=num)
        TDR_df = TDR_df.append(TDR_series)

    return TDR_df

def get_REIT_df(finance_text,subject_list_index):

    REIT_df = pd.DataFrame()
    for num in range((len(finance_text)-subject_list_index[7])//7):
        symbol = finance_text[7*num+(subject_list_index[7]+1)].split("\u3000")[0]
        name = finance_text[7*num+(subject_list_index[7]+1)].split("\u3000")[-1]

        REIT_series = pd.Series({"symbol":symbol,"name":name},name=num)
        REIT_df = REIT_df.append(REIT_series)
    
    return REIT_df