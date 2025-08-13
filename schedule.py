import telebot
import os
import json
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
from functions import findLastClose, calculatePandL, generate_pie_chart, getTotalCost, getTotalPortfolio, getTopThreeStocks, get_usd_to_sgd
from news import getTopMarketNews
from scrape import calculateIv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # hardcode like "123456789" if needed

bot = telebot.TeleBot(TOKEN)
today = datetime.today().strftime("%d-%m-%Y")
tickerSymbolArray = ["GOOGL", "ADBE", "AMZN", "NVDA", "ASML", "META", "TSM", "VEEV", "PANW", "SCHG", "UNH", "CPRT", "FTNT", "NVO", "DUOL", "HCC"]
with open('portfolio.json', 'r') as file:
    currentPortfolio = json.load(file)

lastClose = findLastClose(tickerSymbolArray)
totalPortfolio = getTotalPortfolio(currentPortfolio, lastClose, tickerSymbolArray)
print(type(totalPortfolio))
totalPortfolioInSGD = format(round(float(get_usd_to_sgd()) * float(np.float64(totalPortfolio)), 2),",")
print(totalPortfolioInSGD)
topThreeStocksPositions = getTopThreeStocks(currentPortfolio, lastClose, tickerSymbolArray)

lastCloseMessage = "\n\n*LAST CLOSE FOR YOUR STOCK*\n" 
ivMessage = "\n\n*IV FOR YOUR STOCK*\n" 

pAndLMessage, portfolioPandL = calculatePandL(lastClose, currentPortfolio, tickerSymbolArray)
portfolioPandLInSGD = format(round(portfolioPandL * get_usd_to_sgd(), 2), ",")

fullMessage = f"*KIT WEI'S Investments breakdown as of {today}*\n\n"    
infoMessage = f"_Portfolio:_ 💲*{format(totalPortfolio,",")} USD | {totalPortfolioInSGD} SGD*\n_P&L:_ 💲*{format(portfolioPandL,",")} USD | {portfolioPandLInSGD} SGD*\n_No of Stocks:_ *{len(tickerSymbolArray)}*\n_Top 3 positions:_\n*1. {tickerSymbolArray[topThreeStocksPositions[0]]}*\n*2. {tickerSymbolArray[topThreeStocksPositions[1]]}*\n*3. {tickerSymbolArray[topThreeStocksPositions[2]]}*\n"

for index, price in enumerate(lastClose):
    lastCloseMessage += f"{tickerSymbolArray[index]}: _${format(round(price,2),",")}_\n"

fullMessage += infoMessage + lastCloseMessage + pAndLMessage

# Get top market news
newsArray = getTopMarketNews()
newsMessage = f"<b>Top Market News By CNBC</b>\n"
for x in newsArray:
    newsMessage += f'<a href="{x["url"]}">{x["headline"]}</a>\n\n'

totalCost = getTotalCost(currentPortfolio, lastClose, tickerSymbolArray)
generate_pie_chart(totalCost)
with open("portfolio_pie.png", "rb") as photo:
    bot.send_photo(CHAT_ID, photo, caption=f"📊 Your Portfolio Breakdown {today}")

for i in tickerSymbolArray:
    ivM = calculateIv(i)
    ivMessage += ivM

bot.send_message(CHAT_ID, fullMessage, parse_mode="Markdown")
bot.send_message(CHAT_ID, ivMessage, parse_mode="Markdown")
bot.send_message(CHAT_ID, newsMessage, parse_mode="HTML", disable_web_page_preview=True)
