from database import SessionLocal
from models import Stock

#confirmed count is 2881
session = SessionLocal()
print(session.query(Stock).count())

stocks = session.query(Stock).all()
for s in stocks:
    print(s.ticker, s.name)

session.close()
