from fastapi import FastAPI
from app.routers import watchlist,news


app = FastAPI()

app.include_router(watchlist.router, prefix="/watchlist")
app.include_router(news.router, prefix="/news")






