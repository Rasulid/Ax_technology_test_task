from sqlalchemy import Column, Integer, String, Enum
import enum
from db.DataBase import Base


class MembershipStatus(enum.Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"


class Member(Base):
    __tablename__ = "member"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_info = Column(String)
    membership_status = Column(Enum(MembershipStatus))
    membership_period = Column(Integer)
