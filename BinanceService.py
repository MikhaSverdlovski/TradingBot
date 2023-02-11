from time import sleep

import numpy as np
import requests
from binance.client import Client
from Config import api_key, secret_key, amountOrder
import pandas as pd
import asyncio
import matplotlib.pyplot as plt



client = Client(api_key, secret_key, testnet=False)
USDTdict = []
INTERVAL = '1h'
LIMIT = '100'
QNTY = 12
candles = []


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
        return_data = []
        for each in res.json():
            return_data.append(float(each[4]))
        return_data = pd.Series(return_data)
        return return_data
    except:
        print('Не удалось связаться с бинанс или еще какая то херь')


def getTrendLineCandles(symbol):
    """Построение по точкам трендовой линии"""
    """Потом переписать, чтоб не вызывать второй раз getCandles()"""
    diff = candles[0] - candles[int(LIMIT) - 1]
    step = diff/int(LIMIT)
    arrayX = []
    iter = 0
    while iter < int(LIMIT):
        arrayX.append(candles[0] - step*iter)
        iter = iter+1
    # Это точка трендовой линии в моменте
    return arrayX


def calcStrength(symbol):
    vol = 0
    iter = 0
    while iter < int(LIMIT):
        if candles[iter]>arrayTrend[iter]:
            vol = vol + 1
        else:
            vol = vol - 1
        iter = iter + 1
    return vol


def getTrendLineDirection():
    """Направление линии тренда"""
    if candles[0]-candles[int(LIMIT)-1] > 0:
        direction = 'ВНИЗ'
    else:
        direction = 'ВВЕРХ'
    return direction



candles = getCandles("DOGEUSDT")
arrayTrend = getTrendLineCandles("DOGEUSDT")
print(calcStrength("DOGEUSDT"))
print((getTrendLineDirection()))
y = np.arange(0,int(LIMIT),1)
plt.plot(y,candles)
plt.plot(y,arrayTrend)
plt.grid()
plt.show()


"""Суть затеи такова:
    Если линия тренда вниз, и количество силы равна более чем -40% (возможно варьироваться) от общего числа свечей, то это сигнал на покупку
"""






