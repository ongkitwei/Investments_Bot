import yfinance as yf
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt

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
    pAndLMessage = "\n\n*P&L FOR THE DAY:*\n\n" 
    for index, x in enumerate(ticker):
        pAndLPerShare = lastClose[index] - portfolio[ticker[index]]["costPrice"] 
        totalPAndL = round(pAndLPerShare*portfolio[ticker[index]]["noOfShares"], 2)
        pAndLMessage += f"{ticker[index]}: _{totalPAndL}_\n"
    return pAndLMessage

def generate_pie_chart(data_dict, filename="portfolio_pie.png"):
    labels = list(data_dict.keys())
    sizes = list(data_dict.values())
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Portfolio Breakdown", pad=20)
    plt.axis('equal')  # Equal aspect ratio ensures pie is a circle.
    plt.savefig(filename)
    plt.close()

def getTotalCost(portfolio, ticker):
    totalCostPrice = {}
    for index, x in enumerate(ticker):
        tickerSymbol = ticker[index]
        cost = portfolio[tickerSymbol]["costPrice"] * portfolio[tickerSymbol]["noOfShares"]
        totalCostPrice[tickerSymbol] = cost
    return totalCostPrice