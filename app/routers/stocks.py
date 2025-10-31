from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.data.database import SessionLocal
from app.data.models import Stock
from pydantic import BaseModel

router = APIRouter(prefix="/stocks", tags=["Stocks"])

# -----------------------------
# Pydantic models
# -----------------------------
class StockOut(BaseModel):
    symbol: str
    name: str
    price: float  # adjust fields based on your Stock model

    class Config:
        orm_mode = True

# -----------------------------
# DB Dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# Routes
# -----------------------------

# 1. Search stocks by name (case-insensitive)
@router.get("/search/", response_model=List[StockOut])
def search_stocks(query: str, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(Stock)\
             .filter(Stock.name.ilike(f"%{query}%"))\
             .offset(skip)\
             .limit(limit)\
             .all()

# 2. Get stock by symbol (case-insensitive)
@router.get("/{symbol}", response_model=StockOut)
def get_stock(symbol: str, db: Session = Depends(get_db)):
    stock = db.query(Stock)\
              .filter(func.upper(Stock.symbol) == symbol.upper())\
              .first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

# 3. Get all stocks (with pagination)
@router.get("/", response_model=List[StockOut])
def get_stocks(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Stock).offset(skip).limit(limit).all()
