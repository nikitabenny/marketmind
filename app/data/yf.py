import yfinance as yf

msft = yf.Ticker("MSFT")
print(msft.get_news())