import yfinance as yf

def refresh():
    dat = yf.Ticker("MSFT")
    print(dat.live())

refresh()