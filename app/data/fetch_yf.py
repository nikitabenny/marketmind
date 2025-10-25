import yfinance as yf
import pandas as pd
from database import SessionLocal, engine, Base
from models import Stock



#returns df of all publically traded companies
def get_nyse(path = "nyse-listed.csv"):
    nyse_df = pd.read_csv(path)
    
    return nyse_df

#retrieve historical data for given stocks
def get_history(tickers, startDate, endDate):
    history = pd.DataFrame()
    for ticker in tickers:
        history[ticker] = yf.download(ticker, start=startDate, end=endDate)

    return history


Base.metadata.create_all(bind=engine)

# Load data
session = SessionLocal()

try:
    # Example: Load stocks from fetch_yf
    stocks_data = get_nyse()  # adapt based on your function
    for __,row in stocks_data.iterrows():
        stock = Stock(ticker=row['ACT Symbol'],
                             name = row.get('Company Name', "Unknown"),
                             price=None
    )
    
    session.add(stock)
    session.commit()

finally:
    session.close()