from fastapi import FastAPI
from app.routers import watchlist,news,sentiment,forecast
from app.database import SessionLocal, engine


app = FastAPI()

app.include_router(watchlist.router, prefix="/watchlist")
app.include_router(news.router, prefix="/news")
app.include_router(forecast.router, prefix="/forecast")
app.include_router(sentiment.router, prefix="/sentiment")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





