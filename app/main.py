from fastapi import FastAPI
from app.routers import watchlist,news,sentiment


app = FastAPI()

app.include_router(watchlist.router, prefix="/watchlist")
app.include_router(news.router, prefix="/news")
app.include_router(sentiment.router, prefix="/news")







