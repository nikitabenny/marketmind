from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.data.database import SessionLocal
from app.data.models import User
from pydantic import BaseModel
import hashlib

router = APIRouter(prefix="", tags=["auth"])



class userOut(BaseModel):
    id: int
    email: str
    password : str
    fullName : str


    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup", response_model=userOut)
def add_user(email_in: str, fName: str, lName: str, pword: str, db: Session = Depends(get_db)):
    pHash = hashlib.sha256(pword.encode("utf-8")).hexdigest()
    fullName_in = fName + " " + lName

    new_user = User(email = email_in, password = pHash, fullName = fullName_in)
    db.add(new_user)

    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/signin", response_model = userOut)
def get_user(email_in: str, pword: str, db: Session = Depends(get_db)):
    found_hash = hashlib.sha256(pword.encode("utf-8")).hexdigest()
    user = db.query(User)\
        .filter(User.email == email_in)\
        .filter(User.password == found_hash)\
        .first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return user
