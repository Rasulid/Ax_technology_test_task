from typing import Optional

from pydantic import BaseModel
from datetime import date
from api.schemas.author_schema import AuthorSchema


class BookBaseSchema(BaseModel):
    author_id: int
    title: str
    language: str
    publication_date: date
    category: str
    author_id: Optional[int] = None
    isbn: str


class BookCreateSchema(BookBaseSchema):
    pass


class BookSchema(BookBaseSchema):
    id: int

    class Config:
        from_attributes = True


class BookAuthorSchema(BookBaseSchema):
    author: Optional[AuthorSchema] = None

    class Config:
        from_attributes = True
