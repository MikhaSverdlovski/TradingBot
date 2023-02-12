import pandas as pd

from Config import LIMIT
import numpy as np


def getTrendLineCandles(candles):
    """Построение по точкам трендовой линии"""
    diff = candles[0] - candles[int(LIMIT) - 1]
    step = diff/int(LIMIT)
    arrayX = []
    iter = 0
    while iter < int(LIMIT):
        arrayX.append(candles[0] - step*iter)
        iter = iter+1
    # Это точка трендовой линии в моменте
    return arrayX


def calcStrength(candles, arrayTrend) -> int:
    vol = 0
    iter = 0
    while iter < int(LIMIT):
        if candles[iter] > arrayTrend[iter]:
            vol = vol + 1
        else:
            vol = vol - 1
        iter = iter + 1
    return vol


def getTrendLineDirection(candles) -> str:
    """Направление линии тренда"""
    if candles[0]-candles[int(LIMIT)-1] > 0:
        direction = 'ВНИЗ'
    else:
        direction = 'ВВЕРХ'
    return direction


def moving_avg(candles, n):
    """n - период для скользящей средней"""
    df = pd.DataFrame(candles).rolling(window=n).mean()
    return df


def getAVGline(candles):
    average = pd.Series(candles).mean()
    return average


def getSupportLine(candles):
    """Находит уровень точек поддеркжи"""
    iter = 0
    arrayX = []
    while iter < len(candles) - 1:
        if iter == 0:
            if candles[iter] < candles[iter + 1]:
                arrayX.append(candles[iter])
            else:
                arrayX.append(0)
        else:
            if candles[iter] < candles[iter + 1] and candles[iter] < candles[iter - 1]:
                arrayX.append(candles[iter])
            else:
                arrayX.append(None)
        iter = iter + 1
    return arrayX


def getResistLine(candles):
    """Точки сопротивления"""
    iter = 0
    arrayX = []
    while iter < len(candles) - 1:
        if iter == 0:
            if candles[iter] > candles[iter + 1]:
                arrayX.append(candles[iter])
            else:
                arrayX.append(None)
        else:
            if candles[iter] > candles[iter + 1] and candles[iter] > candles[iter - 1]:
                arrayX.append(candles[iter])
            else:
                arrayX.append(None)
        iter = iter + 1
    return arrayX






