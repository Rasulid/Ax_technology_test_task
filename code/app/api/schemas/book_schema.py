from pydantic import BaseModel
from datetime import date
from api.schemas.author_schema import AuthorSchema


class BookBaseSchema(BaseModel):
    title: str
    language: str
    publication_date: date
    category: str
    isbn: str


class BookCreateSchema(BookBaseSchema):
    pass


class BookSchema(BookBaseSchema):

    class Config:
        orm_mode = True


class BookAuthorSchema(BookBaseSchema):

    author: 'AuthorSchema'

    class Config:
        orm_mode = True
