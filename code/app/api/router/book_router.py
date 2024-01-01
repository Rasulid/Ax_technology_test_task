from typing import Optional, List

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from auth.auth import get_current_user
from db.session import get_db
from models.book_model import Book as BookModel
from models.user_model import User as UserModel
from schemas.book_schema import BookCreateSchema, BookSchema, BookAuthorSchema

router = APIRouter(
    prefix='/book',
    tags=['book']
)


@router.post("/create-book/", response_model=BookSchema)
def create_book(book: BookCreateSchema, db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)):

    if not current_user.is_moderator:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    db_book = BookModel(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/search_books/", response_model=List[BookAuthorSchema])
def search_books(
        title: Optional[str] = Query(None, min_length=3),
        category: Optional[str] = Query(None),
        isbn: Optional[str] = Query(None, min_length=10, max_length=13),
        db: Session = Depends(get_db)
):
    query = db.query(BookModel)

    if title:
        query = query.filter(BookModel.title.ilike(f"%{title}%"))
    if category:
        query = query.filter(BookModel.category == category)
    if isbn:
        query = query.filter(BookModel.isbn == isbn)

    books = query.all()
    return books



@router.get("/get-book/{book_id}", response_model=BookAuthorSchema)
def read_book(book_id: int, db: Session = Depends(get_db)):

    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.get("/get-all-books/", response_model=list[BookAuthorSchema])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = db.query(BookModel).offset(skip).limit(limit).all()
    return books


@router.put("/update-book/{book_id}", response_model=BookSchema)
def update_book(book_id: int, book: BookCreateSchema, db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)):

    if not current_user.is_moderator:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    for var, value in vars(book).items():
        setattr(db_book, var, value) if value else None

    db.commit()
    return db_book


@router.delete("/delete-book/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)):

    if not current_user.is_moderator:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}
