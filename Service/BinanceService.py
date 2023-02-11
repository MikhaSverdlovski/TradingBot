import requests
from binance.client import Client
from Config import api_key, secret_key, AMOUNTORDER, INTERVAL, LIMIT
import pandas as pd


client = Client(api_key, secret_key, testnet=False)
USDTdict = []


def getUSDTTickers() -> list:
    """Получение всех Криптопар, которые торгуются к USDT"""
    tickers = client.get_all_tickers()
    tickers_df = pd.DataFrame(tickers)
    tickers_df = tickers_df['symbol']
    for i in tickers_df:
        if i[-4:] == 'USDT':
            USDTdict.append(i)
    return USDTdict


def getCandles(symbol):
    """Получение свечей по выбранному активу"""
    try:
        url = 'https://api.binance.com/api/v3/klines?symbol={}&interval={}&limit={}'.format(symbol, INTERVAL, LIMIT)
        res = requests.get(url)
        candles = []
        for each in res.json():
            candles.append(float(each[4]))
        candles = pd.Series(candles)
        return candles
    except:
        print('Не удалось связаться с бинанс или еще какая то херь')





