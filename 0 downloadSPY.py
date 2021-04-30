import yfinance as yf
import pandas as pd

# Download SPY data from Yahoo Finance
spy = yf.Ticker("SPY")
data = spy.history(period="max")
print(type(data))
data.to_csv("data/spy.csv", sep=";")
