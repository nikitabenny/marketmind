from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.data.database import SessionLocal
from app.data.models import User
from pydantic import BaseModel

class userOut(BaseModel):
    id: int
    username = str
    email = str
    password = str 


    class Config:
        orm_mode = True


