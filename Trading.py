from Config import LIMIT
from Strategy.Strategy import getTrendLineCandles, getSupportLine, \
    getAVGline, getResistLine
from Service.BinanceService import getCandles
from Service.DBService import writeBuyOrder
from matplotlib import pyplot




candles = getCandles("DOGEUSDT")
trend = getTrendLineCandles(candles)
a = []
for i in range(0,int(LIMIT)-1):
    a.append(i)
pyplot.plot(candles)
pyplot.scatter(a,getSupportLine(candles),c='deeppink', s = 6)
pyplot.scatter(a,getResistLine(candles),c='black', s = 6)
pyplot.show()








