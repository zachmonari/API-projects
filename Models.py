from sqlalchemy import Column, Integer, String
from Database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    pages = Column(Integer)
    description = Column(String, nullable=True)
