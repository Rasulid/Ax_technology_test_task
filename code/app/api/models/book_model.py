from sqlalchemy import Column, Integer, String, ForeignKey, Date
from db.DataBase import Base
from .author_model import Author


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer, ForeignKey(Author.id))
    language = Column(String)
    publication_date = Column(Date)
    category = Column(String)
    isbn = Column(String)

