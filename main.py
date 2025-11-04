from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.routers import watchlist,news,sentiment
from app.data import database
from app.data import models
from app.background.price_updater import update_price

app = FastAPI()

app.include_router(watchlist.router, prefix="/watchlist")
app.include_router(news.router, prefix="/news")
app.include_router(sentiment.router, prefix="/sentiment")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def get_root():
    return "Welcome to Niki's first site"

@app.get("/stocks")
def get_stocks(db: Session = Depends(get_db)):
    stocks = db.query(models.Stock).limit(10).all()
    return [{"Symbol": s.ticker, "Name": s.name, "Price": s.price} for s in stocks]

@app.get("/stock/{ticker}")
def get_stock(ticker: str, db: Session = Depends(get_db)):
    stock = update_price(db=db, ticker_in=ticker)
    if not stock:
        return {"error": "Stock not found"}
    return {"Symbol": stock.ticker, "Name": stock.name, "Price": stock.price}