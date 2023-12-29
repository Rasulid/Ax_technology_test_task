from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from models.book_model import Book as BookModel
from schemas.book_schema import BookCreateSchema, BookSchema, BookAuthorSchema

router = APIRouter(
    prefix='/book',
    tags=['book']
)


@router.post("/create-book/", response_model=BookSchema)
def create_book(book: BookCreateSchema, db: Session = Depends(get_db)):
    db_book = BookModel(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


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
