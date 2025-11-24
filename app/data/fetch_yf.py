import yfinance as yf
import pandas as pd
from app.data.database import SessionLocal, engine, Base
from app.data.models import Stock,User



#returns df of all publically traded companies
# def get_nas(path = 'app/data/nasdaq-listed.csv'):
#     nasdaq_df = pd.read_csv(path)
    
#     return nasdaq_df

#return json object with newest news on ticker
def get_recent(ticker):
    cleaned_news = []

    for news in ticker.news:
        cleaned_news.append( 
            {
                "title": news["content"].get("title", None),
                "summary": news["content"].get("summary", None)
            }
        )

    return cleaned_news


def get_nyse(path = 'app/data/nyse-listed.csv'):
    nyse_df = pd.read_csv(path)
    
    return nyse_df

#return json object with newest news on ticker
def get_recent(ticker):
    cleaned_news = []

    for news in ticker.news:
        cleaned_news.append( 
            {
                "title": news["content"].get("title", None),
                "summary": news["content"].get("summary", None)
            }
        )

    return cleaned_news


msft = yf.Ticker("MSFT")


get_recent(msft)

# #retrieve historical data for given stocks
# def get_history(tickers, startDate, endDate):
#     history = pd.DataFrame()
#     for ticker in tickers:
#         history[ticker] = yf.download(ticker, start=startDate, end=endDate)

#     return history




Base.metadata.create_all(bind=engine)

# Load data
session = SessionLocal()

# try:
# #     stocks_data = get_nyse()

#     for _, row in stocks_data.iterrows():
#         stock = Stock(
#             ticker=row['ACT Symbol'],
#             name=row.get('Company Name', "Unknown"),
#             price=None
#         )
#         session.add(stock)

#     session.commit()
#     print("✅ NYSE stocks inserted successfully!")

# except Exception as e:
#     session.rollback()
#     print("❌ Error:", e)



# finally:
#     session.close()


# Base.metadata.drop_all(bind=engine)  # WARNING: deletes all tables
# Base.metadata.create_all(bind=engine)