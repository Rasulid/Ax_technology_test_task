from pydantic import BaseModel


class Book(BaseModel):
    title: str
    isbn: str


class AuthorBaseSchema(BaseModel):
    name: str


class AuthorCreateSchema(AuthorBaseSchema):
    pass


class AuthorSchema(AuthorBaseSchema):

    class Config:
        orm_mode = True


class AuthorBookSchema(AuthorBaseSchema):

    books: list[Book]

    class Config:
        orm_mode = True