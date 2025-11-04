import yfinance as yf

import yfinance as yf
from sqlalchemy.orm import Session
from app.data.models import Stock

def update_price(db: Session, ticker_in: str):
    # Query the DB for this stock symbol
    db_stock = db.query(Stock).filter(Stock.ticker == ticker_in).first()
    if not db_stock:
        return None
    
    # Fetch latest price
    yf_data = yf.Ticker(ticker_in).history(period="1d")
    
    if yf_data.empty:
        return None
    
    # Extract latest closing price
    latest_price = float(yf_data["Close"].iloc[-1])
    
    # Update and commit
    db_stock.price = latest_price
    db.commit()
    db.refresh(db_stock)
    
    return db_stock