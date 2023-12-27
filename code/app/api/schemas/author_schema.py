from pydantic import BaseModel


class AuthorCreate(BaseModel):
    name: str
