from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class Ticker (BaseModel):
    name: str
    note: Optional [str]
    date: str
    price: float

watchlist = { "AAPL": {
              "note": "Buy below 160", 
              "date": "2024-06-10",
              "price" : 78.99}
              }


#return all tickers
@router.get('/')
def root():
    return watchlist

@router.post('/add-ticker/{ticker}')
def add_ticker(tck: Ticker):
    watchlist[tck.name] = {
              "note": tck.note,
              "date": tck.date,
              "price" : tck.price
              }
    
    {"message": f"{tck.name} added to watchlist."}
              
    
@router.delete('/remove-ticker/{ticker}')
def remove_ticker(tck : Ticker):
    if tck in watchlist:
        del watchlist[tck]
        return {"message": f"{tck} removed."}
    return {"error": "Ticker not found."}

#note handling
@router.post('/add-note/{ticker}')
def add_note(note : str, tck: Ticker):
    if tck in watchlist:
        watchlist[tck]["note"] = note
        return {"message": "Note added"}
    return {"error": "Ticker not found."}

@router.delete('/remove-note/{ticker}')
def remove_note(tck: Ticker):
    if tck in watchlist and "note" in watchlist[tck]:
        del watchlist[tck]["note"]
        return {"message": "Note removed"}
    return {"error": "Note or ticker not found."}

@router.put('/update-note/{ticker}')
def update_note(tck: Ticker, new_note: str):
    if tck in watchlist:
        watchlist[tck]["note"] = new_note
        return {"message": "Note updated"}
    return {"error": "Ticker not found."}