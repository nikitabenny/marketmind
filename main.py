from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.routers import watchlist,sentiment,auth,stocks
from app.data import database
from app.data import models
from app.background.price_updater import update_price

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(watchlist.router, prefix="/watchlist")
app.include_router(sentiment.router, prefix="/sentiment")
app.include_router(auth.router, prefix = "/auth")
app.include_router(stocks.router, prefix = "/stocks")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def get_root():
    return "Niki's site"

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

