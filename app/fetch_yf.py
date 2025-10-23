import yfinance as yf
import pandas as pd



#returns tickers of all publically traded companies
def get_nyse(path = "data/nyse-listed.csv"):
    df = pd.read_csv(path)
    tickers = df["ACT Symbol"]
    return tickers

#retrieve historical data for given stocks
def get_history(tickers, startDate, endDate):
    history = pd.DataFrame()
    for ticker in tickers:
        history[ticker] = yf.download(ticker, start=startDate, end=endDate)

    return history

