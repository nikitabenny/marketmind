from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.data.database import SessionLocal
from app.data.models import Watchlist

router = APIRouter(prefix="/watchlist", tags=["Watchlist"])

# -----------------------------
# Schemas
# -----------------------------
class Ticker(BaseModel):
    symbol: str
    note: Optional[str] = ""
    date: Optional[datetime] = None
    price: Optional[float] = None

class NoteUpdate(BaseModel):
    note: str

# -----------------------------
# DB dependency
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

# 1. Get all tickers
@router.get("/", response_model=list[Ticker])
def get_watchlist(db: Session = Depends(get_db)):
    return db.query(Watchlist).all()

# 2. Add a ticker
@router.post("/add-ticker/")
def add_ticker(tck: Ticker, db: Session = Depends(get_db)):
    db_ticker = db.query(Watchlist).filter(Watchlist.symbol == tck.symbol.upper()).first()
    if db_ticker:
        raise HTTPException(status_code=400, detail="Ticker already exists.")
    
    new_ticker = Watchlist(
        symbol=tck.symbol.upper(),
        note=tck.note,
        date=tck.date or datetime.utcnow(),
        price=tck.price
    )
    db.add(new_ticker)
    db.commit()
    db.refresh(new_ticker)
    return {"message": f"{tck.symbol.upper()} added to watchlist."}

# 3. Remove a ticker
@router.delete("/remove-ticker/{symbol}")
def remove_ticker(symbol: str, db: Session = Depends(get_db)):
    db_ticker = db.query(Watchlist).filter(Watchlist.symbol == symbol.upper()).first()
    if not db_ticker:
        raise HTTPException(status_code=404, detail="Ticker not found.")
    db.delete(db_ticker)
    db.commit()
    return {"message": f"{symbol.upper()} removed from watchlist."}

# 4. Add/update note
@router.put("/note/{symbol}")
def add_or_update_note(symbol: str, note_data: NoteUpdate, db: Session = Depends(get_db)):
    db_ticker = db.query(Watchlist).filter(Watchlist.symbol == symbol.upper()).first()
    if not db_ticker:
        raise HTTPException(status_code=404, detail="Ticker not found.")
    db_ticker.note = note_data.note
    db.commit()
    db.refresh(db_ticker)
    return {"message": "Note added/updated."}

# 5. Remove note
@router.delete("/note/{symbol}")
def remove_note(symbol: str, db: Session = Depends(get_db)):
    db_ticker = db.query(Watchlist).filter(Watchlist.symbol == symbol.upper()).first()
    if not db_ticker:
        raise HTTPException(status_code=404, detail="Ticker not found.")
    db_ticker.note = ""
    db.commit()
    db.refresh(db_ticker)
    return {"message": "Note removed."}
