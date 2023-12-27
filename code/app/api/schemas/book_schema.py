from datetime import date
from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author_id: int
    language: str
    publication_date: date
    category: str
    isbn: str
