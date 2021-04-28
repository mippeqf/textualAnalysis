import pickle
import csv
import yfinance as yf
import pandas as pd

data = pickle.load(open("data/3toneAnalysisDump", "rb"))

# Dump dataset containing timeseries of textual analysis to csv
with open("data/dataExport.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, data[0].keys())
    writer.writeheader()
    writer.writerows(data)

# Download SPY data from Yahoo Finance
spy = yf.Ticker("SPY")
data = spy.history(period="max")
print(type(data))
data.to_csv("data/spy.csv", sep=";")
