from pydantic import BaseModel


class Book(BaseModel):
    title: str
    isbn: str


class AuthorBaseSchema(BaseModel):
    name: str


class AuthorCreateSchema(AuthorBaseSchema):
    pass


class AuthorSchema(AuthorBaseSchema):
    id: int

    class Config:
        from_attributes = True


class AuthorBookSchema(AuthorBaseSchema):
    books: list[Book]

    class Config:
        from_attributes = True
