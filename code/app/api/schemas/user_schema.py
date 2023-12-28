from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    hashed_password: str
    is_active: bool = True
    is_admin: bool = False


class UserInDB(UserCreate):
    hashed_password: str


class UserResponseSchema(BaseModel):
    username: str
    email: str
    is_active: bool = True
    is_admin: bool = False

    class Config:
        orm_mode = True
