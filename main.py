import os
import telebot
import json
from dotenv import load_dotenv
from datetime import datetime
from functions import findLastClose, calculatePandL, generate_pie_chart, getTotalCost

with open('portfolio.json', 'r') as file:
    currentPortfolio = json.load(file)

today = datetime.today().strftime("%d-%m-%Y")

tickerSymbolArray = ["GOOGL", "ADBE", "AMZN", "NVDA", "ASML", "META", "TSM", "VEEV", "PANW", "SCHG", "UNH"]
totalCost = getTotalCost(currentPortfolio,tickerSymbolArray)

load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

# When user sends /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Welcome to my bot. 🤖")

# When user sends /message
@bot.message_handler(commands=['message'])
def send_welcome(message):
    lastClose = findLastClose(tickerSymbolArray)
    fullMessage = f"*KIT WEI'S Investments breakdown as of {today}*\n\n"    
    infoMessage = f"_Portfolio: xx_\n_P&L (%): xx_\n_No of Stocks: x_\n_Top 3 positions: x, x, x_\n"
    lastCloseMessage = "\n\n*LAST CLOSE FOR YOUR STOCK*\n\n" 
    pAndLMessage = calculatePandL(lastClose, currentPortfolio, tickerSymbolArray)

    for index, price in enumerate(lastClose):
        lastCloseMessage += f"{tickerSymbolArray[index]}: ${round(price,2)}\n"
    
    fullMessage += infoMessage + lastCloseMessage + pAndLMessage
    bot.reply_to(message, fullMessage, parse_mode="Markdown")

# When user sends /portfolio
@bot.message_handler(commands=['portfolio'])
def send_welcome(message):
    generate_pie_chart(totalCost)
    with open("portfolio_pie.png", "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption="📊 Your Portfolio Breakdown")

# When user sends a normal text message
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"You said: {message.text}")

# Keep the bot running
bot.infinity_polling()
