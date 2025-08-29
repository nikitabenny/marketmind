from models import Stock, Watchlist, Holding

#crud ops by stock object and ticker

#helper
def get_stock(db, ticker_in):
    stock = db.query(Stock).filter(Stock.ticker == ticker_in).first()
    if stock:
        return stock


def add_stock(db, ticker_in, name_in, price_in):
    stock = Stock(ticker = ticker_in, name = name_in, price = price_in)
    db.add(stock)
    db.commit()
    db.refresh(stock) #creates id for the stock
    return stock


def remove_stock(db, stock_in):
    db.delete(stock_in)
    db.commit()
    return stock_in


def remove_stock_by_ticker(db, ticker):
    stock = get_stock(db,ticker)
    if stock:
        remove_stock(db,stock)


def update_stock_price(db, stock_in, new_price):
    stock_in.price = new_price
    db.commit()
    db.refresh(stock_in)
    return stock_in


def update_stock_by_ticker(db, ticker,new_price):
    stock = get_stock(db,ticker)
    if stock:
        update_stock_price(db,stock,new_price)







