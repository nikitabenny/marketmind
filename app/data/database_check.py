from database import SessionLocal
from models import Stock
from sqlalchemy import func


#confirmed count is 2881
session = SessionLocal()
print(session.query(Stock).count())

#confirmed ticker and names are valid
# stocks = session.query(Stock).all()
# for s in stocks:
#     print(s.ticker, s.name)

#confirmed keys are correct
print(Stock.__table__.columns.keys())

#confirmed no duplicate values
duplicates = session.query(Stock.ticker, func.count()).group_by(Stock.ticker).having(func.count() > 1).all()
print(duplicates)




session.close()
