import yfinance as yf
import pandas as pd
from app.data.database import SessionLocal, engine, Base
from app.data.models import Stock



#returns df of all publically traded companies
def get_nas(path = 'app/data/nasdaq-listed.csv'):
    nasdaq_df = pd.read_csv(path)
    
    return nasdaq_df
    

# #retrieve historical data for given stocks
# def get_history(tickers, startDate, endDate):
#     history = pd.DataFrame()
#     for ticker in tickers:
#         history[ticker] = yf.download(ticker, start=startDate, end=endDate)

#     return history




Base.metadata.create_all(bind=engine)

# Load data
session = SessionLocal()

try:
    stocks_data = get_nas()

    for _, row in stocks_data.iterrows():
        stock = Stock(
            ticker=row['Symbol'],
            name=row.get('Company Name', "Unknown"),
            price=None
        )
        session.add(stock)

    session.commit()
    print("✅ NASDAQ stocks inserted successfully!")

except Exception as e:
    session.rollback()
    print("❌ Error:", e)

finally:
    session.close()