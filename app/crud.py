from models import User, Stock, Watchlist, Holding
from typing import List, Optional
from sqlalchemy.orm import Session

#crud ops by stock object and ticker
#helper

# stock crud

# crud_stock.py
from sqlalchemy.orm import Session
from models import Stock
from typing import List, Optional

# ===== GET OPERATIONS =====

def get_stock_by_id(db: Session, stock_id: int) -> Optional[Stock]:
    """Get stock by ID"""
    return db.query(Stock).filter(Stock.id == stock_id).first()

def get_stock_by_ticker(db: Session, ticker: str) -> Optional[Stock]:
    """Get stock by ticker symbol (e.g., 'AAPL')"""
    return db.query(Stock).filter(Stock.ticker == ticker.upper()).first()

def get_all_stocks(db: Session, skip: int = 0, limit: int = 100) -> List[Stock]:
    """Get all stocks with pagination"""
    return db.query(Stock).offset(skip).limit(limit).all()

def search_stocks(db: Session, search_term: str) -> List[Stock]:
    """Search stocks by ticker or name"""
    search_term = f"%{search_term.upper()}%"
    return db.query(Stock).filter(
        (Stock.ticker.like(search_term)) | 
        (Stock.name.like(search_term))
    ).all()

# ===== CREATE OPERATIONS =====

def create_stock(db: Session, ticker: str, name: str, price: float) -> Stock:
    """Create a new stock"""
    # Check if stock already exists
    existing_stock = get_stock_by_ticker(db, ticker)
    if existing_stock:
        raise ValueError(f"Stock with ticker {ticker} already exists")
    
    stock = Stock(
        ticker=ticker.upper(),
        name=name,
        price=price
    )
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock

def get_or_create_stock(db: Session, ticker: str, name: str = None, price: float = 0.0) -> Stock:
    """Get existing stock or create if it doesn't exist"""
    stock = get_stock_by_ticker(db, ticker)
    if stock:
        return stock
    
    # If no name provided, use ticker as name
    if name is None:
        name = f"Stock {ticker.upper()}"
    
    return create_stock(db, ticker, name, price)

# ===== UPDATE OPERATIONS =====

def update_stock_price(db: Session, stock_id: int, new_price: float) -> Optional[Stock]:
    """Update stock price by ID"""
    stock = get_stock_by_id(db, stock_id)
    if not stock:
        return None
    
    stock.price = new_price
    db.commit()
    db.refresh(stock)
    return stock

def update_stock_price_by_ticker(db: Session, ticker: str, new_price: float) -> Optional[Stock]:
    """Update stock price by ticker"""
    stock = get_stock_by_ticker(db, ticker)
    if not stock:
        return None
    
    stock.price = new_price
    db.commit()
    db.refresh(stock)
    return stock

def update_stock_info(db: Session, stock_id: int, name: str = None, price: float = None) -> Optional[Stock]:
    """Update stock name and/or price"""
    stock = get_stock_by_id(db, stock_id)
    if not stock:
        return None
    
    if name is not None:
        stock.name = name
    if price is not None:
        stock.price = price
    
    db.commit()
    db.refresh(stock)
    return stock

# ===== DELETE OPERATIONS =====

def delete_stock_by_id(db: Session, stock_id: int) -> bool:
    """Delete stock by ID. Returns True if deleted, False if not found"""
    stock = get_stock_by_id(db, stock_id)
    if not stock:
        return False
    
    db.delete(stock)
    db.commit()
    return True

def delete_stock_by_ticker(db: Session, ticker: str) -> bool:
    """Delete stock by ticker. Returns True if deleted, False if not found"""
    stock = get_stock_by_ticker(db, ticker)
    if not stock:
        return False
    
    db.delete(stock)
    db.commit()
    return True

# ===== BULK OPERATIONS =====

def bulk_update_prices(db: Session, price_updates: dict) -> List[Stock]:
    """
    Bulk update multiple stock prices
    price_updates: {"AAPL": 150.0, "GOOGL": 2500.0}
    """
    updated_stocks = []
    
    for ticker, price in price_updates.items():
        stock = update_stock_price_by_ticker(db, ticker, price)
        if stock:
            updated_stocks.append(stock)
    
    return updated_stocks

def create_stocks_bulk(db: Session, stocks_data: List[dict]) -> List[Stock]:
    """
    Create multiple stocks at once
    stocks_data: [{"ticker": "AAPL", "name": "Apple Inc.", "price": 150.0}, ...]
    """
    created_stocks = []
    
    for stock_data in stocks_data:
        try:
            stock = create_stock(
                db,
                ticker=stock_data["ticker"],
                name=stock_data["name"],
                price=stock_data["price"]
            )
            created_stocks.append(stock)
        except ValueError:
            # Skip if stock already exists
            continue
    
    return created_stocks

# ===== UTILITY FUNCTIONS =====

def stock_exists(db: Session, ticker: str) -> bool:
    """Check if stock exists by ticker"""
    return get_stock_by_ticker(db, ticker) is not None

def get_stock_count(db: Session) -> int:
    """Get total number of stocks in database"""
    return db.query(Stock).count()

def get_stocks_by_price_range(db: Session, min_price: float, max_price: float) -> List[Stock]:
    """Get stocks within a price range"""
    return db.query(Stock).filter(
        Stock.price >= min_price,
        Stock.price <= max_price
    ).all()

def get_stock(db: Session, ticker: str) -> Optional[Stock]:
    """Get stock by ticker symbol (e.g., 'AAPL') - MAIN FUNCTION"""
    return db.query(Stock).filter(Stock.ticker == ticker.upper()).first()

def get_stock_by_id(db: Session, stock_id: int) -> Optional[Stock]:
    """Get stock by ID"""
    return db.query(Stock).filter(Stock.id == stock_id).first()

def get_stock_by_ticker(db: Session, ticker: str) -> Optional[Stock]:
    """Get stock by ticker symbol (e.g., 'AAPL')"""
    return db.query(Stock).filter(Stock.ticker == ticker.upper()).first()

def get_all_stocks(db: Session, skip: int = 0, limit: int = 100) -> List[Stock]:
    """Get all stocks with pagination"""
    return db.query(Stock).offset(skip).limit(limit).all()

def search_stocks(db: Session, search_term: str) -> List[Stock]:
    """Search stocks by ticker or name"""
    search_term = f"%{search_term.upper()}%"
    return db.query(Stock).filter(
        (Stock.ticker.like(search_term)) | 
        (Stock.name.like(search_term))
    ).all()

# ===== CREATE OPERATIONS =====
def add_stock(db: Session, ticker: str, name: str, price: float) -> Stock:
    """Add a new stock to database - MAIN FUNCTION"""
    # Check if stock already exists
    existing_stock = get_stock(db, ticker)
    if existing_stock:
        raise ValueError(f"Stock with ticker {ticker} already exists")
    
    stock = Stock(
        ticker=ticker.upper(),
        name=name,
        price=price
    )
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock

def create_stock(db: Session, ticker: str, name: str, price: float) -> Stock:
    """Create a new stock"""
    # Check if stock already exists
    existing_stock = get_stock_by_ticker(db, ticker)
    if existing_stock:
        raise ValueError(f"Stock with ticker {ticker} already exists")
    
    stock = Stock(
        ticker=ticker.upper(),
        name=name,
        price=price
    )
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock

def get_or_create_stock(db: Session, ticker: str, name: str = None, price: float = 0.0) -> Stock:
    """Get existing stock or create if it doesn't exist"""
    stock = get_stock_by_ticker(db, ticker)
    if stock:
        return stock
    
    # If no name provided, use ticker as name
    if name is None:
        name = f"Stock {ticker.upper()}"
    
    return create_stock(db, ticker, name, price)

# ===== UPDATE OPERATIONS =====

def update_stock_price(db: Session, stock_id: int, new_price: float) -> Optional[Stock]:
    """Update stock price by ID"""
    stock = get_stock_by_id(db, stock_id)
    if not stock:
        return None
    
    stock.price = new_price
    db.commit()
    db.refresh(stock)
    return stock

def update_stock_price_by_ticker(db: Session, ticker: str, new_price: float) -> Optional[Stock]:
    """Update stock price by ticker"""
    stock = get_stock_by_ticker(db, ticker)
    if not stock:
        return None
    
    stock.price = new_price
    db.commit()
    db.refresh(stock)
    return stock

def update_stock_info(db: Session, stock_id: int, name: str = None, price: float = None) -> Optional[Stock]:
    """Update stock name and/or price"""
    stock = get_stock_by_id(db, stock_id)
    if not stock:
        return None
    
    if name is not None:
        stock.name = name
    if price is not None:
        stock.price = price
    
    db.commit()
    db.refresh(stock)
    return stock

# ===== DELETE OPERATIONS =====

def delete_stock_by_id(db: Session, stock_id: int) -> bool:
    """Delete stock by ID. Returns True if deleted, False if not found"""
    stock = get_stock_by_id(db, stock_id)
    if not stock:
        return False
    
    db.delete(stock)
    db.commit()
    return True

def delete_stock_by_ticker(db: Session, ticker: str) -> bool:
    """Delete stock by ticker. Returns True if deleted, False if not found"""
    stock = get_stock_by_ticker(db, ticker)
    if not stock:
        return False
    
    db.delete(stock)
    db.commit()
    return True

# ===== BULK OPERATIONS =====

def bulk_update_prices(db: Session, price_updates: dict) -> List[Stock]:
    """
    Bulk update multiple stock prices
    price_updates: {"AAPL": 150.0, "GOOGL": 2500.0}
    """
    updated_stocks = []
    
    for ticker, price in price_updates.items():
        stock = update_stock_price_by_ticker(db, ticker, price)
        if stock:
            updated_stocks.append(stock)
    
    return updated_stocks

def create_stocks_bulk(db: Session, stocks_data: List[dict]) -> List[Stock]:
    """
    Create multiple stocks at once
    stocks_data: [{"ticker": "AAPL", "name": "Apple Inc.", "price": 150.0}, ...]
    """
    created_stocks = []
    
    for stock_data in stocks_data:
        try:
            stock = create_stock(
                db,
                ticker=stock_data["ticker"],
                name=stock_data["name"],
                price=stock_data["price"]
            )
            created_stocks.append(stock)
        except ValueError:
            # Skip if stock already exists
            continue
    
    return created_stocks

# ===== UTILITY FUNCTIONS =====

def stock_exists(db: Session, ticker: str) -> bool:
    """Check if stock exists by ticker"""
    return get_stock_by_ticker(db, ticker) is not None

def get_stock_count(db: Session) -> int:
    """Get total number of stocks in database"""
    return db.query(Stock).count()

def get_stocks_by_price_range(db: Session, min_price: float, max_price: float) -> List[Stock]:
    """Get stocks within a price range"""
    return db.query(Stock).filter(
        Stock.price >= min_price,
        Stock.price <= max_price
    ).all()



#User
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, username: str, email: str):
    user = User(username=username, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_all_users(db: Session):
    return db.query(User).all()


#Watchlist
def add_to_watchlist(db: Session, user_id: int, stock_id: int):
    # Check if already in watchlist
    existing = db.query(Watchlist).filter(
        Watchlist.user_id == user_id, 
        Watchlist.stock_id == stock_id
    ).first()
    
    if existing:
        return existing  # Already exists
    
    watchlist_item = Watchlist(user_id=user_id, stock_id=stock_id)
    db.add(watchlist_item)
    db.commit()
    db.refresh(watchlist_item)
    return watchlist_item

def remove_from_watchlist(db: Session, user_id: int, stock_id: int):
    watchlist_item = db.query(Watchlist).filter(
        Watchlist.user_id == user_id, 
        Watchlist.stock_id == stock_id
    ).first()
    
    if watchlist_item:
        db.delete(watchlist_item)
        db.commit()
        return True
    return False

def get_user_watchlist(db: Session, user_id: int):
    # Get all watchlist items for a user with stock details
    return db.query(Watchlist).filter(Watchlist.user_id == user_id).all()

def add_to_watchlist_by_ticker(db: Session, user_id: int, ticker: str):
    stock = get_stock(db, ticker)
    if not stock:
        # You might want to fetch real stock data here
        stock = add_stock(db, ticker, f"Stock {ticker}", 0.0)
    
    return add_to_watchlist(db, user_id, stock.id)

def remove_from_watchlist_by_ticker(db: Session, user_id: int, ticker: str):
    stock = get_stock(db, ticker)
    if stock:
        return remove_from_watchlist(db, user_id, stock.id)
    return False


    
#Holdings
def add_holding(db: Session, user_id: int, stock_id: int, shares: float):
    # Check if user already has this stock
    existing = db.query(Holding).filter(
        Holding.user_id == user_id, 
        Holding.stock_id == stock_id
    ).first()
    
    if existing:
        # Add to existing shares
        existing.shares += shares
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new holding
        holding = Holding(user_id=user_id, stock_id=stock_id, shares=shares)
        db.add(holding)
        db.commit()
        db.refresh(holding)
        return holding

def sell_holding(db: Session, user_id: int, stock_id: int, shares: float):
    holding = db.query(Holding).filter(
        Holding.user_id == user_id, 
        Holding.stock_id == stock_id
    ).first()
    
    if not holding:
        return None  # User doesn't own this stock
    
    if holding.shares < shares:
        return None  # Not enough shares to sell
    
    holding.shares -= shares
    
    # If no shares left, remove the holding
    if holding.shares <= 0:
        db.delete(holding)
    
    db.commit()
    if holding.shares > 0:
        db.refresh(holding)
    return holding

def get_user_holdings(db: Session, user_id: int):
    return db.query(Holding).filter(Holding.user_id == user_id).all()

def get_holding(db: Session, user_id: int, stock_id: int):
    return db.query(Holding).filter(
        Holding.user_id == user_id, 
        Holding.stock_id == stock_id
    ).first()

def buy_stock_by_ticker(db: Session, user_id: int, ticker: str, shares: float):    
    stock = get_stock(db, ticker)
    if not stock:
        # Create stock if it doesn't exist (you might want to fetch real data)
        stock = add_stock(db, ticker, f"Stock {ticker}", 0.0)
    
    return add_holding(db, user_id, stock.id, shares)

def sell_stock_by_ticker(db: Session, user_id: int, ticker: str, shares: float):    
    stock = get_stock(db, ticker)
    if stock:
        return sell_holding(db, user_id, stock.id, shares)
    return None

def get_portfolio_value(db: Session, user_id: int):
    holdings = get_user_holdings(db, user_id)
    total_value = 0.0
    
    for holding in holdings:
        stock_value = holding.shares * holding.stock.price
        total_value += stock_value
    
    return total_value