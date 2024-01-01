from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.auth import get_current_user
from db.session import get_db
from models.author_model import Author as AuthorModel
from models.user_model import User as UserModel
from schemas.author_schema import AuthorSchema, AuthorCreateSchema, AuthorBookSchema

router = APIRouter(
    prefix="/author",
    tags=['author']
)


@router.post("/create-author/", response_model=AuthorSchema)
def create_author(author: AuthorCreateSchema, db: Session = Depends(get_db),
                  current_user: UserModel = Depends(get_current_user)):

    if not current_user.is_moderator:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    db_author = AuthorModel(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


@router.get("/get-author/{author_id}", response_model=AuthorBookSchema)
def read_author(author_id: int, db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)):

    if not current_user.is_moderator:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    db_author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@router.get("/get-all-authors/", response_model=list[AuthorBookSchema])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                 current_user: UserModel = Depends(get_current_user)):

    if not current_user.is_moderator:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    authors = db.query(AuthorModel).offset(skip).limit(limit).all()
    return authors


@router.put("/update-author/{author_id}", response_model=AuthorSchema)
def update_author(author_id: int, author: AuthorCreateSchema, db: Session = Depends(get_db),
                  current_user: UserModel = Depends(get_current_user)):

    if not current_user.is_moderator:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    db_author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    for var, value in vars(author).items():
        setattr(db_author, var, value) if value else None

    db.commit()
    return db_author


@router.delete("/delete-author/{author_id}", status_code=204)
def delete_author(author_id: int, db: Session = Depends(get_db),
                  current_user: UserModel = Depends(get_current_user)):

    if not current_user.is_moderator:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    db_author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(db_author)
    db.commit()
    return {"message": "Author deleted successfully"}
