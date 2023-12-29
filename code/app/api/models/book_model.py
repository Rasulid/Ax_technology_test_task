from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from db.DataBase import Base
from .author_model import Author


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer, ForeignKey('author.id'))
    language = Column(String)
    publication_date = Column(Date)
    category = Column(String)
    isbn = Column(String)

    author = relationship('Author', back_populates='books')
