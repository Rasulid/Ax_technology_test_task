from datetime import timedelta

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from auth.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash, \
    verify_password, get_current_user
from db.session import get_db
from models.user_model import User
from schemas.user_schema import UserCreate, UserResponseSchema

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/", response_model=UserResponseSchema)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    query = db.query(User).filter(User.email == user.email).first()
    if query is not None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f"user {user.email} already exists"
        )
    db_user = User(email=user.email, username=user.username, hashed_password=get_password_hash(user.hashed_password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/users/me", response_model=UserResponseSchema)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

