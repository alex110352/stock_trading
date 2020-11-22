import time
import requests

from bs4 import BeautifulSoup

def  get_share_html(stock_symbol='NaN'):

    if stock_symbol == 'NaN':
        return 'please input symbol'

    url = 'https://finance.yahoo.com/quote/'+stock_symbol+'?p='+stock_symbol+'&.tsrc=fin-srch'

    try:

        r = requests.get(url,timeout=5)
        html_text = BeautifulSoup(r.text,'lxml')
        status = html_text.find('span', attrs={"data-reactid": "6"}).text


        if status != 'All':

            symbol_html = html_text.find('tbody', attrs={"data-reactid": "54"}).find_all('a')
            simular_symbol_dict = {}

            if len(symbol_html) % 2 == 1:

                for num in range(int((len(symbol_html)+1)/2)):
                    symbol = symbol_html[num*2].get('data-symbol')
                    name = symbol_html[num*2].get('title')
                    simular_symbol_dict[symbol] = name

                return simular_symbol_dict
            
            else:

                for num in range(int(len(symbol_html)/2)):
                    symbol = symbol_html[num*2].get('data-symbol')
                    name = symbol_html[num*2].get('title')
                    simular_symbol_dict[symbol] = name

                return simular_symbol_dict

        else : 
            return html_text

    except AttributeError :

        return 'error symbol'

    except ConnectionError :
        
        return 'connect timeout'  

def get_currency(stock_symbol='NaN'):

    if stock_symbol == 'NaN':
        return 'please input symbol'
        
    html_text = get_share_html(stock_symbol)

    if html_text == 'error symbol':
        return 'error symbol'
    elif html_text == 'connect timeout':
        return 'connect timeout'

    try :
        currency = html_text.find('span', attrs={"data-reactid": "9"}).text.split(" ")[-1]
    except AttributeError:
        return html_text
    except TypeError:
        return 'error symbol'
    else : 
        return currency

def get_current_price(stock_symbol='NaN'):

    if stock_symbol == 'NaN':
        return 'please input symbol'
        
    html_text = get_share_html(stock_symbol)

    if html_text == 'error symbol':
        return 'error symbol'
    elif html_text == 'connect timeout':
        return 'connect timeout'

    try :
        current_price = html_text.find('span', attrs={"data-reactid": "32"}).text
    except AttributeError:
        return html_text
    except TypeError:
        return 'error symbol'
    else : 
        return current_price

def get_open_price(stock_symbol='NaN'):

    if stock_symbol == 'NaN':
        return 'please input symbol'
        
    html_text = get_share_html(stock_symbol)
    
    if html_text == 'error symbol':
        return 'error symbol'
    elif html_text == 'connect timeout':
        return 'connect timeout'
    
    try :
        open_price = html_text.find('span', attrs={"data-reactid": "93"}).text
    except AttributeError:
        return html_text
    except TypeError:
        return 'error symbol'
    else :
        return open_price

def get_max_price(stock_symbol='NaN'):

    if stock_symbol == 'NaN':
        return 'please input symbol'
        
    html_text = get_share_html(stock_symbol)
    
    if html_text == 'error symbol':
        return 'error symbol'
    elif html_text == 'connect timeout':
        return 'connect timeout'
    
    try :
        max_price = html_text.find('td', attrs={"data-reactid": "107"}).text.split(" ")[-1]
    except AttributeError:
        return html_text
    except TypeError:
        return 'error symbol'
    else :
        return max_price

def get_min_price(stock_symbol='NaN'):

    if stock_symbol == 'NaN':
        return 'please input symbol'
        
    html_text = get_share_html(stock_symbol)
    
    if html_text == 'error symbol':
        return 'error symbol'
    elif html_text == 'connect timeout':
        return 'connect timeout'
    
    try :
        min_price = html_text.find('td', attrs={"data-reactid": "107"}).text.split(" ")[0]
    except AttributeError:
        return html_text
    except TypeError:
        return 'error symbol'
    else :
        return min_price