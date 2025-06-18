import yfinance as yf

def refresh():
    dat = yf.Ticker("MSFT")
    print(dat.history(period="1d", interval="1m"))

refresh()
