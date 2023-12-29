from sqlalchemy import Column, Integer, String, Enum, Date
import enum
from db.DataBase import Base


class MembershipStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"


class Member(Base):
    __tablename__ = "member"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_info = Column(String)
    membership_status = Column(Enum(MembershipStatus))
    membership_start_date = Column(Date)
    membership_end_date = Column(Date)
