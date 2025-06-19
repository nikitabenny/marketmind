from fastapi import APIRouter

router = APIRouter()


articles = {
  "TSLA": [
    {"title": "Tesla stock rallies", "url": "https://..."},
    {"title": "Musk announces...", "url": "https://..."}
  ]
}


@router.get('/get-articles/{ticker}')
def news(ticker : str):
    target = {}
    if ticker in articles:
        for article in articles[ticker]:
            target[article["title"]] = article["url"]

        return target
    
    else:
        return {"error" : "no articles found"}
    
    



