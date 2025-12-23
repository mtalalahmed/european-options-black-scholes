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

def get_price(ticker): #retrive the price of the stock, +validation
    try:
        dat = yf.Ticker(ticker.upper())
        if dat.info["exchange"] in european_exchanges:
            return(f"{dat.info['currentPrice']:.2f}") #price to 2sf
        else:
            return("Not a european stock")
    except:
        return("stock not found")

def get_option(ticker):
    one_expiry = "2026/10/10"
    one_expiry = datetime.strptime(one_expiry, "%Y/%m/%d")
    t = (one_expiry - datetime.today()).days
    t = t / 365


def calc_volatility(ticker):
    dat = yf.Ticker(ticker.upper())
    historic_dat = dat.history(period="1y") 
    daily_returns = (historic_dat['Close'] / historic_dat['Close'].shift(1)).apply(np.log).dropna()
    daily_std = daily_returns.std()
    annualized_vol = daily_std * math.sqrt(252)
    return round(annualized_vol, 6)

def get_basic_rate(T_years):

    gilt_yields = {
        2: 0.0374,
        5: 0.0395,
        10: 0.0452,
        30: 0.0527
    }

    df = pd.DataFrame(list(gilt_yields.items()), columns=["Maturity", "Yield"]).sort_values("Maturity")

    if T_years <= df["Maturity"].min():
        return df["Yield"].iloc[0]
    if T_years >= df["Maturity"].max():
        return df["Yield"].iloc[-1]

    lower = df[df["Maturity"] <= T_years].iloc[-1]
    upper = df[df["Maturity"] >= T_years].iloc[0]

    if lower["Maturity"] == upper["Maturity"]:
        return lower["Yield"]

    r = lower["Yield"] + (upper["Yield"] - lower["Yield"]) * ((T_years - lower["Maturity"]) / (upper["Maturity"] - lower["Maturity"]))
    return r

def calculate_option(price, time, r, volatility, strike, opt_type):
    d1 = ((math.log(price/strike)) + (r + (0.5 * volatility * volatility)) * time)/(volatility * (math.sqrt(time)))
    d2 = d1 - (volatility * (math.sqrt(time)))
    if opt_type == "call":
        opt_price = price * norm.cdf(d1) - strike * math.exp(r * time * -1) * norm.cdf(d2)
    else:
        opt_price = -price * norm.cdf(-d1) + strike * math.exp(r * time * -1) * norm.cdf(-d2)
    return(opt_price)


ticker = input("enter stock").strip()
print(get_option(ticker))