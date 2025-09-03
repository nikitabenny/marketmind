from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

engine = create_engine("sqlite:///./portfolio.db", echo=True)

from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass



metadata_obj = MetaData()


