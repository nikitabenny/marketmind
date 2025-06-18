from fastapi import APIRouter
from app.schemas import Ticker
from datetime import datetime

router = APIRouter()


watchlist = { "AAPL": {
              "note": "Buy below 160", 
              "date": datetime(2025, 6, 10, hour=11, minute=30),
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
def remove_ticker(tck : str):
    if tck in watchlist:
        del watchlist[tck]
        return {"message": f"{tck} removed."}
    return {"error": "Ticker not found."}

#note handling
@router.post('/add-note/{ticker}')
def add_note(note : str, tck: str):
    if tck in watchlist:
        watchlist[tck]["note"] = note
        return {"message": "Note added"}
    return {"error": "Ticker not found."}

@router.delete('/remove-note/{ticker}')
def remove_note(tck: str):
    if tck in watchlist and "note" in watchlist[tck]:
        del watchlist[tck]["note"]
        return {"message": "Note removed"}
    return {"error": "Note or ticker not found."}

@router.put('/update-note/{ticker}')
def update_note(tck: str, new_note: str):
    if tck in watchlist and watchlist[tck]["note"] == "":
        watchlist[tck]["note"] = new_note
        return {"message": "Note updated"}
    return {"error": "Bad Request"}