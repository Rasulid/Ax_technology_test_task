from fastapi import HTTPException, APIRouter

from fastapi import Depends
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.member_schema import LibraryMemberSchema, LibraryMemberCreateSchema
from models.member_model import Member as LibraryMemberModel

router = APIRouter(
    prefix="/members",
    tags=['library member']
)


@router.post("/create-member/", response_model=LibraryMemberSchema)
def create_member(member: LibraryMemberCreateSchema, db: Session = Depends(get_db)):
    db_member = LibraryMemberModel(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.get("/get-member/{member_id}", response_model=LibraryMemberSchema)
def read_member(member_id: int, db: Session = Depends(get_db)):
    db_member = db.query(LibraryMemberModel).filter(LibraryMemberModel.id == member_id).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Library member not found")
    return db_member


@router.get("/get-all-members/", response_model=list[LibraryMemberSchema])
def read_members(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    members = db.query(LibraryMemberModel).offset(skip).limit(limit).all()
    return members
