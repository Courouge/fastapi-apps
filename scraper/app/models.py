from sqlalchemy import  Column,   Integer, String
from sqlalchemy.schema import ForeignKey
from database import Base

class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class Leboncoin(Base):
    __tablename__ = "leboncoin"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(String, unique=True, index=True)
    url = Column(String, unique=True, index=True)
    description = Column(String, unique=True, index=True)
    date = Column(String, unique=True, index=True)

class Leboncoin_imgs(Base):
    __tablename__ = "leboncoin_imgs"

    id = Column(Integer, primary_key=True, index=True)
    lbc_url = Column(String, ForeignKey("leboncoin.url"), nullable=False)
    img = Column(String, unique=True, index=True)
