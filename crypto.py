import requests
from bs4 import BeautifulSoup as bs
from pycbrf import ExchangeRates
import time


def delete_brackets(elem):
    ans = ''
    state = False
    for i in elem:
        if i == '<':
            state = False
        elif i == '>':
            state = True
        if state and (i != '<' and i != '>'):
            ans += i
    ans = ans.strip()
    ans = ans.replace(',', '.')
    return ans


def get_crypto_dict(url):
    r = requests.get(url)
    soup = bs(r.text, features='lxml')
    table_time = soup.find('div', {'class': 'currencies__date'})

    add = False
    time = []
    temp_time = None
    for i in table_time:
        temp_time = i.replace(' ', '')
    time = ''
    for i in temp_time:
        if i.isdigit() or i == ':':
            time += i

    temp_btc = soup.find_all('span', {'class': 'currencies__td__inner'})
    crypto_dict = {}
    btc = []
    k = 0
    for i in range(0, len(temp_btc), 3):
        if i + 1 <= len(temp_btc):
            valuta = delete_brackets(str(temp_btc[i])).find('USD') != -1
            valuta *= delete_brackets(str(temp_btc[i])) != 'BNBUSDT'
            valuta *= delete_brackets(str(temp_btc[i])).find('USDT') == -1
            if valuta:
                try:
                    crypto_dict[delete_brackets(str(temp_btc[i]))] = int(
                        delete_brackets(str(temp_btc[i + 1]).replace(' ', '')))
                except ValueError:
                    crypto_dict[delete_brackets(str(temp_btc[i]))] = float(
                        delete_brackets(str(temp_btc[i + 1]).replace(' ', '')))

    return crypto_dict


rbc = 'https://www.rbc.ru/crypto/'


def rub():
    return float(ExchangeRates('2021-05-03')['USD'][4])
