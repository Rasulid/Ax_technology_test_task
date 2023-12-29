from datetime import date

from pydantic import BaseModel

from models.member_model import MembershipStatus


class LibraryMemberBaseSchema(BaseModel):
    name: str
    contact_info: str
    membership_status: MembershipStatus
    membership_start_date: date
    membership_end_date: date


class LibraryMemberCreateSchema(LibraryMemberBaseSchema):
    pass


class LibraryMemberSchema(LibraryMemberBaseSchema):
    id: int

    class Config:
        orm_mode = True
