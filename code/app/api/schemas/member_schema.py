from enum import Enum

from pydantic import BaseModel


class MembershipStatus(Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"


class MemberCreate(BaseModel):
    name: str
    contact_info: str
    membership_status: MembershipStatus
    membership_period: int
