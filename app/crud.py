from models import Stock, Watchlist, Holding


def add_stock(db, ticker_in, name_in, price_in):
    stock = Stock(ticker = ticker_in, name = name_in, price = price_in)
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock

def remove_stock(db, stock_in):
    db.remove(stock_in)
    db.commit()
    db.refresh()
    return stock_in








