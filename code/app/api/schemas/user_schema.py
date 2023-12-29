from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False
    is_moderator: bool = False


class UserInDB(UserCreate):
    hashed_password: str


class UserResponseSchema(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False
    is_moderator: bool = False


class Config:
    orm_mode = True
