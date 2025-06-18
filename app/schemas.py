from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Ticker (BaseModel):
    name: str
    note: Optional [str]
    date: datetime
    price: float


