from datetime import timedelta

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from auth.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash, \
    verify_password, get_current_user
from db.session import get_db
from models.user_model import User
from schemas.user_schema import UserResponseSchema, UserCreate, ChangePasswordSchema

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


@router.post("/create-user/", response_model=UserResponseSchema)
async def create_user(user: UserCreate, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)
                      ):

    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    query = db.query(User).filter(User.email == user.email).first()
    if query is not None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f"user {user.email} already exists"
        )
    db_user = User(email=user.email,
                   username=user.username,
                   hashed_password=get_password_hash(user.hashed_password),
                   is_staff=user.is_staff,
                   is_superuser=user.is_superuser,
                   is_active=user.is_active,
                   is_moderator=user.is_moderator
                   )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/user/me", response_model=UserResponseSchema)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/update-user-put/{user_id}", response_model=UserResponseSchema)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for var, value in vars(user).items():
        if value is not None:
            if var == 'password':
                hashed_password = get_password_hash(value)
                setattr(db_user, var, hashed_password)
            else:
                setattr(db_user, var, value)

    db.commit()
    return db_user


@router.patch("/update-user-patch/{user_id}", response_model=UserResponseSchema)
def patch_user(user_id: int, user: UserCreate, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):

    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for var, value in vars(user).items():
        if value is not None:
            if var == 'password':
                hashed_password = get_password_hash(value)
                setattr(db_user, var, hashed_password)
            else:
                setattr(db_user, var, value)

    db.commit()
    return db_user


@router.delete("/delete-user/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}


@router.post("/change-password")
def change_password(password_data: ChangePasswordSchema, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user.id).first()

    if not verify_password(password_data.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()
    return {"message": "Password changed successfully"}
