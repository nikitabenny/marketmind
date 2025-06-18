from fastapi import FastAPI
from app.routers import watchlist


app = FastAPI()

app.include_router(watchlist.router, prefix="/watchlist")






