import yfinance as yf
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_eps_next_5y(ticker):
    url = f"https://finviz.com/quote.ashx?t={ticker}&ty=c&ta=1&p=d"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        table = soup.find("table", class_="snapshot-table2")
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            for i in range(0, len(cells), 2):
                key = cells[i].text.strip()
                value = cells[i + 1].text.strip()
                if key == "EPS next 5Y":
                    return value
        return "EPS next 5Y not found"
    except Exception as e:
        return f"Error: {e}"

def getTickerType(tickerSymbol):
    ticker = yf.Ticker(tickerSymbol)
    info = ticker.info
    return info.get("quoteType", "unknown")

def getTtmFcf(tickerSymbol):
    ticker = yf.Ticker(tickerSymbol)

    # Get quarterly cash flow (latest quarters)
    quarterly_cashflow = ticker.quarterly_cashflow

    try:
        # Get Free Cash Flow row from quarterly data
        free_cash_flow_q = quarterly_cashflow.loc["Free Cash Flow"]

        # Sum last 4 quarters to get TTM Free Cash Flow
        ttm_fcf = free_cash_flow_q[:4].sum()

        print(f"TTM Free Cash Flow (quarterly) for GOOG: ${ttm_fcf:,.0f}")
        return ttm_fcf
    except KeyError:
        print("Free Cash Flow row not found in quarterly cash flow.")
        return None
    
def getTotalDebt(tickerSymbol):
    ticker = yf.Ticker(tickerSymbol)
    totalDebt = ticker.balance_sheet.loc["Total Debt"][:1]
    print(totalDebt)
    return totalDebt

def getCashEquiv(tickerSymbol):
    ticker = yf.Ticker(tickerSymbol)
    cashEquiv = ticker.balance_sheet.loc["Cash Cash Equivalents And Short Term Investments"][:1]
    print(cashEquiv)
    return cashEquiv

def getTotalShares(tickerSymbol):
    ticker = yf.Ticker(tickerSymbol)
    totalShares = ticker.info.get("impliedSharesOutstanding")
    print(totalShares)
    return totalShares

def getGrowthEstimate(tickerSymbol):
    ticker = yf.Ticker(tickerSymbol)
    finvizEpsFiveyear = float(get_eps_next_5y(tickerSymbol).replace("%",""))
    growthEstimate = ticker.growth_estimates.loc["+1y","stockTrend"]
    # returnOnEquity = ticker.info.get("returnOnEquity")
    averageGrowthEstimate = round((((growthEstimate*100) + finvizEpsFiveyear)/2),2)
    if averageGrowthEstimate > 25:
        return 25
    else:
        print(averageGrowthEstimate)
        return averageGrowthEstimate

def getCurrentYear():
    currentYear = datetime.now().year
    print(type(currentYear))

def calculateIv(ticker):
    fcfArray = []
    fcfDiscountedArray = []
    checkTicker = getTickerType(ticker)
    if checkTicker != "EQUITY":
        print(f"{ticker} is not a stock (it's a {checkTicker}). Skipping...")
        return f"NO IV FOR {ticker}\n"

    ttmFcf = getTtmFcf(ticker)
    growthEstimate = getGrowthEstimate(ticker)
    cashEquiv = getCashEquiv(ticker)
    noOfShares = getTotalShares(ticker)
    totalDebt = getTotalDebt(ticker)
    for i in range(20):
        lastIndex = len(fcfArray) - 1

        if i == 0:
            fcfArray.append(float((ttmFcf/100)*(100+growthEstimate)))
        elif i > 0 and i< 5:
            fcfArray.append(float((fcfArray[lastIndex]/100)*(100+growthEstimate)))

        elif i >= 5 and i < 10:
            fcfArray.append(float((fcfArray[lastIndex]/100)*(100+(growthEstimate/2))))
        
        else:
            fcfArray.append(float((fcfArray[lastIndex]/100)*(100+4)))

    for i in range(20):
        fcfDiscountedArray.append(fcfArray[i]/((1+0.063)**(i+1)))

    intrinsicValue = ((sum(fcfDiscountedArray) + cashEquiv - totalDebt )/ noOfShares)
    ivMessage = f"{ticker}: {round(intrinsicValue.values[0],2)}\n"
    print(ticker + str(round(intrinsicValue.values[0],2)))
    return ivMessage
