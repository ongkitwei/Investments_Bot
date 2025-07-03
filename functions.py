import yfinance as yf
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
import requests

def findLastClose(ticker):
    lastCLoseArray = []
    for symbol in ticker:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")
            last_close = hist["Close"].iloc[-1]
            print(f"{symbol}: Last close price: {last_close}")
            lastCLoseArray.append(last_close)
        except Exception as e:
            print(f"Error for {symbol}: {e}")
    return lastCLoseArray

def calculatePandL(lastClose, portfolio, ticker):
    pAndLMessage = "\n\n*P&L:*\n" 
    portfolioPandL = 0
    for index, x in enumerate(ticker):
        pAndLPerShare = lastClose[index] - portfolio[ticker[index]]["costPrice"] 
        totalPAndL = round(pAndLPerShare*portfolio[ticker[index]]["noOfShares"], 2)
        portfolioPandL += totalPAndL
        pAndLMessage += f"{ticker[index]}: _${format(totalPAndL,",")}_\n"
    return pAndLMessage, format(round(portfolioPandL,2),",")

def generate_pie_chart(data_dict, filename="portfolio_pie.png"):
    labels = list(data_dict.keys())
    sizes = list(data_dict.values())
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Portfolio Breakdown", pad=20)
    plt.axis('equal')  # Equal aspect ratio ensures pie is a circle.
    plt.savefig(filename)
    plt.close()

def getTotalCost(portfolio, lastclose, ticker):
    totalCostPrice = {}
    for index, x in enumerate(ticker):
        tickerSymbol = ticker[index]
        cost = lastclose[index] * portfolio[tickerSymbol]["noOfShares"]
        totalCostPrice[tickerSymbol] = cost
    return totalCostPrice

def getTotalPortfolio(portfolio, lastclose, ticker):
    totalPortfolio = 0
    for index, x in enumerate(lastclose):
        tickerSymbol = ticker[index]
        totalPortfolio += portfolio[tickerSymbol]["noOfShares"] * lastclose[index]
    return round(totalPortfolio,2)

def getTopThreeStocks(portfolio, lastclose, ticker):
    valuePerStock = []
    for index, x in enumerate(lastclose):
        valuePerStock.append(portfolio[ticker[index]]["noOfShares"] * lastclose[index])
    topThreeWithIndices = sorted(enumerate(valuePerStock), key=lambda x: x[1], reverse=True)[:3]
    topThreePositions = [index for index, value in topThreeWithIndices]
    return topThreePositions

def get_usd_to_sgd():
    url = "https://api.frankfurter.app/latest?from=USD&to=SGD"
    response = requests.get(url)
    data = response.json()
    rate = data['rates']['SGD']
    return rate