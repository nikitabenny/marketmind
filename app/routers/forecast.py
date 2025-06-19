from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

forecast = {
  "TSLA":
    {
     "forecast": 
         [
            { datetime(2025, 6, 10, hour=11, minute=30):  177.45},
            { datetime(2025, 6, 11, hour=11, minute=30):  177.90}
         ]
    }
}

@router.get('/get-sentiment/{ticker}')
def senti(ticker : str, date : datetime):
    if ticker in forecast:
        return forecast[ticker][date]
    
    return {"Stock does not exist"}