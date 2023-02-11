import Service.BinanceService
from Config import LIMIT


def getTrendLineCandles(symbol, candles):
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


def buyCondition(candles, arrayTrend) -> bool:
    if calcStrength(candles, arrayTrend) > 40 and getTrendLineDirection(candles) == 'ВНИЗ':
        return True
    else:
        return False

