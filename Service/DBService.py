from datetime import datetime

import mysql.connector
from Config import AMOUNTORDER


myconn = mysql.connector.connect(host= '127.0.0.1',
        user= 'vsearch',
        password= 'vsearchpasswd',
        database= 'webapp')
cursor = myconn.cursor()
symbols = []


def writeBuyOrder(currency, amountOrder, buyCost):
    """Запись ордера о покупке в БД"""
    sql = """INSERT INTO transactions (Currency, amountWallet, AMOUNTORDER, countofbuy, transactionDate, buyCost, Sellcost, isActive)
    VALUES
    (%s, %s, %s, %s, %s, %s ,%s, %s)"""
    cursor.execute(sql, (currency, getWalletAmount()-amountOrder, amountOrder, amountOrder/buyCost, datetime.now(), buyCost, 0, True,))
    myconn.commit()


def getWalletAmount() -> float:
    """Проверка сколько есть сейчас в кошельке"""
    sql = """SELECT amount
                FROM wallet 
                where idWallet=1"""
    cursor.execute(sql)
    records = cursor.fetchall()
    currentWallet = 0.0
    for row in records:
        currentWallet = row[0]
    return currentWallet


def setWalletAmount(amountOrder) -> float:
    """Устанавливаем значение в кошельке сколько есть сейчас в кошельке после транзы"""
    sql = """UPDATE wallet
                SET amount = %s
                where idWallet=1"""
    cursor.execute(sql,(getWalletAmount() - amountOrder,))
    records = cursor.fetchall()
    currentWallet = 0.0
    myconn.commit()
    for row in records:
        currentWallet = row[0]
    return currentWallet


def getOpenTransactionId(currency: str) -> int:
    """Возвращает айди открытой транзакции (ордера) (Применяется для продажи)"""
    sql = """SELECT idtransactions 
                FROM transactions 
                where Currency = %s and isActive = True"""
    cursor.execute(sql, (currency,))
    records = cursor.fetchall()
    if len(records) == 0:
        return 0
    else:
        for row in records:
            currentOpenId = row[0]
        return currentOpenId


def writeSellOrder(currency: str, sellcost: float):
    """Внесение изменений в запись о продаже, что ордер продан"""
    sql = """UPDATE transactions 
            set sellCost = %s, transactionDate = %s
            where idtransactions = %s"""
    cursor.execute(sql, (sellcost, datetime.now(), getOpenTransactionId(currency),))
    myconn.commit()


def setPnl(currency: str):
    """Внесение изменений в PNL"""
    sql = """UPDATE transactions 
                set PNL = (1 - (buyCost / sellCost)) * 100, isActive = false
                where idtransactions = %s"""
    cursor.execute(sql, (getOpenTransactionId(currency),))
    myconn.commit()


def getAmountBuyVal(symbol) -> float:
    """Получение суммы ордера на покупку"""
    sql = "SELECT buycost from transactions where currency = %s and isActive = true"
    cursor.execute(sql, (symbol,))
    records = cursor.fetchall()
    buyVal = 0
    for row in records:
        buyVal = row[0]
    return buyVal


def getCountOfBuy(symbol) -> float:
    """Получение количества купленных монет на покупку"""
    sql = "SELECT countOfBuy from transactions where currency = %s and isActive = true"
    cursor.execute(sql, (symbol,))
    records = cursor.fetchall()
    countVal = 0
    for row in records:
        countVal = row[0]
    return countVal


def getSymbolsBought() -> list:
    """Получение всех криптовалютных пар, по которым есть тразакции"""
    sql = """SELECT * FROM transactions where isActive = true"""
    cursor.execute(sql,)
    records = cursor.fetchall()
    for row in records:
        symbols.append(row[1])
    return symbols