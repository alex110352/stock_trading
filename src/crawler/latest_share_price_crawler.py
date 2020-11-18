import time
import requests

from bs4 import BeautifulSoup

def  get_html_text(stock_symbol):

    global simular_symbol_dict,status
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

        status = 'error symbol'
        return status

    except ConnectionError :
        
        status = 'connect timeout'  
        return status

def get_currency(html_text):

    try :
        currency = html_text.find('span', attrs={"data-reactid": "9"}).text.split(" ")[-1]
    except AttributeError:
        return simular_symbol_dict
    except TypeError:
        return status
    else : 
        return currency

def get_current_price(html_text):

    try :
        current_price = html_text.find('span', attrs={"data-reactid": "32"}).text
    except AttributeError:
        return simular_symbol_dict
    except TypeError:
        return status
    else : 
        return current_price

def get_open_price(html_text):

    try :
        open_price = html_text.find('span', attrs={"data-reactid": "93"}).text
    except AttributeError:
        return simular_symbol_dict
    except TypeError:
        return status
    else :
        return open_price

def get_max_price(html_text):

    try :
        max_price = html_text.find('td', attrs={"data-reactid": "107"}).text.split(" ")[-1]
    except AttributeError:
        return simular_symbol_dict
    except TypeError:
        return status
    else :
        return max_price

def get_min_price(html_text):

    try :
        min_price = html_text.find('td', attrs={"data-reactid": "107"}).text.split(" ")[0]
    except AttributeError:
        return simular_symbol_dict
    except TypeError:
        return status
    else :
        return min_price


