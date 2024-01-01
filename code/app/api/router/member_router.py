from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from models.user_model import User as UserModel
from auth.auth import get_current_user
from db.session import get_db
from schemas.member_schema import LibraryMemberSchema, LibraryMemberCreateSchema
from models.member_model import Member as LibraryMemberModel

router = APIRouter(
    prefix="/members",
    tags=['library member']
)


@router.post("/create-member/", response_model=LibraryMemberSchema)
async def create_member(member: LibraryMemberCreateSchema, db: Session = Depends(get_db),
                        current_staff: UserModel = Depends(get_current_user)):
    if not current_staff.is_staff:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    db_member = LibraryMemberModel(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.get("/get-member/{member_id}", response_model=LibraryMemberSchema, )
async def read_member(member_id: int, db: Session = Depends(get_db),
                      current_staff: UserModel = Depends(get_current_user)):
    if not current_staff.is_staff:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    db_member = db.query(LibraryMemberModel).filter(LibraryMemberModel.id == member_id).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Library member not found")
    return db_member


@router.get("/get-all-members/", response_model=list[LibraryMemberSchema])
async def read_members(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                       current_staff: UserModel = Depends(get_current_user)):
    if not current_staff.is_staff:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    members = db.query(LibraryMemberModel).offset(skip).limit(limit).all()
    return members


@router.put("/update-member/{member_id}", response_model=LibraryMemberSchema)
async def update_member(member_id: int, member: LibraryMemberCreateSchema,
                        db: Session = Depends(get_db),
                        current_staff: UserModel = Depends(get_current_user)):
    if not current_staff.is_staff:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    db_member = db.query(LibraryMemberModel).filter(LibraryMemberModel.id == member_id).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Library member not found")

    for var, value in vars(member).items():
        setattr(db_member, var, value) if value else None

    db.commit()
    return db_member


@router.delete("/delete-member/{member_id}", status_code=204)
async def delete_member(member_id: int, db: Session = Depends(get_db),
                        current_staff: UserModel = Depends(get_current_user)):
    if not current_staff.is_staff:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    db_member = db.query(LibraryMemberModel).filter(LibraryMemberModel.id == member_id).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Library member not found")
    db.delete(db_member)
    db.commit()
    return {"message": "Library member deleted successfully"}


@router.patch("/update-member-status", response_model=LibraryMemberSchema)
async def update_member(member_id: int, member: LibraryMemberCreateSchema,
                        db: Session = Depends(get_db),
                        current_staff: UserModel = Depends(get_current_user)):
    if not current_staff.is_staff:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    db_member = db.query(LibraryMemberModel).filter(LibraryMemberModel.id == member_id).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Library member not found")

    for var, value in vars(member).items():
        setattr(db_member, var, value) if value else None

    db.commit()
    return db_member


@router.get("/check_member_status")
async def check_member_status(member_id: int, db: Session = Depends(get_db),
                              current_staff: UserModel = Depends(get_current_user)):
    if not current_staff.is_staff:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    member = db.query(LibraryMemberModel).filter(LibraryMemberModel.id == member_id).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")


    return {"member_id": member.id, "membership_status": member.membership_status}
