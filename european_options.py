import yfinance as yf
import math
from scipy.stats import norm

european_exchanges = [ #checks if stock is european
    "LSE", "AIM", "PAR", "AMS", "BRU", "DUB",
    "LIS", "XETRA", "SIX", "BIT", "STO", "CPH",
    "HEL", "ICEX", "TALSE", "RIX", "VIL", "WSE",
    "VIE", "ATHEX", "OB", "BME", "BSE", "PSE"
]

def get_price(ticker): #retrive the price of the stock, +validation
    try:
        dat = yf.Ticker(ticker.upper())
        if dat.info["exchange"] in european_exchanges:
            return(f"{dat.info['currentPrice']:.2f}") #price to 2sf
        else:
            return("Not a european stock")
    except:
        return("stock not found")
