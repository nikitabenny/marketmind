from fastapi import APIRouter

router = APIRouter()

mood = {
  "TSLA": 
    {"positive": ["prices up", "earnings increased", "increased profit"]
     }
  
}

@router.get('/get-sentiment/{ticker}')
def senti(ticker : str):
    if ticker in mood:
        return mood[ticker]
    
    return {"Stock does not exist"}