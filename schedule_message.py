# daily_message.py
import os
import telebot
import json
from dotenv import load_dotenv
from datetime import datetime
from functions import findLastClose, calculatePandL, getTotalPortfolio, getTopThreeStocks

load_dotenv()

with open('portfolio.json', 'r') as file:
    currentPortfolio = json.load(file)

tickerSymbolArray = ["GOOGL", "ADBE", "AMZN", "NVDA", "ASML", "META", "TSM", "VEEV", "PANW", "SCHG", "UNH"]
today = datetime.today().strftime("%d-%m-%Y")

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
CHAT_ID = os.getenv("CHAT_ID")

def build_message():
    lastClose = findLastClose(tickerSymbolArray)
    totalPortfolio = format(getTotalPortfolio(currentPortfolio, lastClose, tickerSymbolArray), ",")
    topThreeStocksPositions = getTopThreeStocks(currentPortfolio, lastClose, tickerSymbolArray)

    lastCloseMessage = "\n\n*LAST CLOSE FOR YOUR STOCK*\n" 
    pAndLMessage, portfolioPandL = calculatePandL(lastClose, currentPortfolio, tickerSymbolArray)
    fullMessage = f"*KIT WEI'S Investments breakdown as of {today}*\n\n"    
    infoMessage = f"_Portfolio:_ 💲*{totalPortfolio} USD*\n_P&L:_ 💲*{portfolioPandL} USD*\n_No of Stocks:_ *{len(tickerSymbolArray)}*\n_Top 3 positions: {tickerSymbolArray[topThreeStocksPositions[0]]}, {tickerSymbolArray[topThreeStocksPositions[1]]}, {tickerSymbolArray[topThreeStocksPositions[2]]}_\n"

    for index, price in enumerate(lastClose):
        lastCloseMessage += f"{tickerSymbolArray[index]}: ${format(round(price,2),",")}\n"

    return fullMessage + infoMessage + lastCloseMessage + pAndLMessage

bot.send_message(CHAT_ID, build_message(), parse_mode="Markdown")
