import yfinance as yf
import math
from datetime import datetime
import pandas
import numpy as np
from scipy.stats import norm

stock = ""
european_exchanges = [ #checks if stock is european
    "LSE", "AIM", "PAR", "AMS", "BRU", "DUB",
    "LIS", "XETRA", "SIX", "BIT", "STO", "CPH",
    "HEL", "ICEX", "TALSE", "RIX", "VIL", "WSE",
    "VIE", "ATHEX", "OB", "BME", "BSE", "PSE"
]

def get_price(): #retrive the price of the stock, +validation
    try:
        dat = yf.Ticker(ticker.upper())
        if dat.info["exchange"] in european_exchanges:
            return(f"{dat.info['currentPrice']:.2f}") #price to 2sf
        else:
            return("Not a european stock")
    except:
        return("stock not found")

def get_option():
    index = 0
    dat = yf.Ticker(ticker.upper())
    expiries = dat.options
    one_expiry = datetime.strptime(dat.options[index], "%Y-%m-%d")
    t = (one_expiry - datetime.today()).days
    t = t / 365
    option_chain = dat.option_chain(dat.options[index])
    calls = option_chain.calls
    puts = option_chain.puts
    call_strikes = calls['strike'].tolist()
    put_strikes = puts['strike'].tolist()

def calc_volatility():
    dat = yf.Ticker(ticker.upper())
    historic_dat = dat.history(period="1y") 
    daily_returns = (historic_dat['Close'] / historic_dat['Close'].shift(1)).apply(np.log).dropna()
    daily_std = daily_returns.std()
    annualized_vol = daily_std * math.sqrt(252)
    return round(annualized_vol, 6)

ticker = input("enter stock").strip()
print(calc_volatility())