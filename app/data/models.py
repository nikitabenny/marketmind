from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

    # relationships- back_populates allows the two classes to sync
    watchlists = relationship("Watchlist", back_populates="owner")
    holdings = relationship("Holding", back_populates="owner")

class Stock(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True)
    name = Column(String)
    price = Column(Float)

class Watchlist(Base):
    __tablename__ = "watchlists"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    stock_id = Column(Integer, ForeignKey("stocks.id"))

    owner = relationship("User", back_populates="watchlists")
    stock = relationship("Stock")

class Holding(Base):
    __tablename__ = "holdings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    shares = Column(Float)

    owner = relationship("User", back_populates="holdings")
    stock = relationship("Stock")

