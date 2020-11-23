from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import datetime 
from GoogleNews import GoogleNews

def get_company_news_link(company = 'NaN',news_num=5,time_range = 'today'):

    if company == 'NaN':
        return 'please input company name'

    news_link = []
    googlenews = GoogleNews()
    googlenews.clear()

    if time_range != 'today':
        start_date = "{1}/{2}/{0}".format(time_range[0:4],time_range[5:7],time_range[8:10])
        end_date = "{1}/{2}/{0}".format(time_range[11:15],time_range[16:18],time_range[19:21])
        googlenews.set_time_range(start_date,end_date)

    googlenews.search(company)
    result = googlenews.result()
    
    try :
        for num in range(news_num):
            news_link.append(result[num]['link'])
    except IndexError :
        if len(news_link) == 0:
            return '此時段無'+company+'新聞 OR 網路不穩'
        return news_link
    else :
        return news_link
