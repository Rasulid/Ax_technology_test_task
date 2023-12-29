from pydantic import BaseModel


class AdminCreate(BaseModel):
    username: str
    email: str
    hashed_password: str
    is_active: bool = True
    is_admin: bool
    is_staff: bool


class AdminInDB(AdminCreate):
    hashed_password: str


class AdminResponseSchema(BaseModel):
    username: str
    email: str
    is_active: bool = True
    is_admin: bool
    is_staff: bool

    class Config:
        orm_mode = True
