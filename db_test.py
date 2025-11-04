from app.data.database import SessionLocal, engine
from app.data import models

# Create the database tables (if they don't already exist)
print("Creating tables (if not exist)...")
models.Base.metadata.create_all(bind=engine)

# Open a new database session
db = SessionLocal()

try:
    # Test basic connection
    print("Connected to database successfully.")


    stocks = db.query(models.Stock)
    for stock in stocks:
        print(stock.ticker)
    

finally:
    db.close()
    print("Database session closed.")


    