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
    fullName : str


    class Config:
        orm_mode = True
        extra = "ignore"


class SignIn(BaseModel):
    email_in: str
    pword: str

class SignUp(BaseModel):
    email_in: str
    pword: str
    fName: str
    lName: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup", response_model=userOut)
def add_user(data: SignUp, db: Session = Depends(get_db)):
    pHash = hashlib.sha256(data.pword.encode("utf-8")).hexdigest()
    fullName_in = data.fName + " " + data.lName

    new_user = User(email = data.email_in, password = pHash, fullName = fullName_in)
    db.add(new_user)

    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/signin", response_model = userOut)
def get_user(data: SignIn, db: Session = Depends(get_db)):
    found_hash = hashlib.sha256(data.pword.encode("utf-8")).hexdigest()
    user = db.query(User)\
        .filter(User.email == data.email_in)\
        .filter(User.password == found_hash)\
        .first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return user