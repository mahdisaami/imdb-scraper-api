from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_, exists, select
from sqlalchemy.orm import Session
from starlette import status

from app.core.security import verify_password, create_access_token, hash_password
from app.deps import get_db
from app.models import User
from app.schemas.users import UserRead, UserCreate, UserResponse, UserPatch
from app.services.exceptions import UserNotFoundException, EmailTakenException
from app.services.users import get_user_by_username, get_current_user

router = APIRouter(tags=["users"])

@router.post("/users/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user:UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        or_(
            User.username == user.username,
            User.email == user.email
        )
    ).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username Or Email already registered.", headers={'x-error-code': 'USERNAME_OR_EMAIL_TAKEN'})

    elif user.username == "admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username 'admin' is not allowed.", headers={'x-error-code': 'INVALID_USERNAME'})
    user.password = hash_password(user.password)
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user": new_user}

@router.get("/users/get/{user_id}", response_model=UserResponse)
async def get_user(user_id:int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise UserNotFoundException()
    return {"message": "User fetched successfully", "user": db_user}

@router.get("/users", response_model=list[UserRead])
async def get_all_users(db: Session = Depends(get_db)):
    db_users = db.query(User).all()
    return db_users



@router.post("/users/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(username=form.username, db=db)

    if not user or not verify_password(form.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials.", headers={'x-error-code': 'INVALID_CREDENTIALS'})

    token = create_access_token({"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/profile", response_model=UserResponse)
def profile(user = Depends(get_current_user)):
    return {"message": "Profile fetched successfully", "user": user}


@router.put("/users/update/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id:int, user_update: UserCreate, db: Session = Depends(get_db)):
    db_user = db.get(User, user_id)
    email_exists = db.query(User).filter(User.email == user_update.email).first()

    if email_exists and email_exists.id != user_id:
        raise EmailTakenException()

    if not db_user:
        raise UserNotFoundException()

    if user_update.username == "admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username 'admin' is not allowed.", headers={'x-error-code': 'INVALID_USERNAME'})

    user_update.password = hash_password(user_update.password)
    for key, value in user_update.model_dump().items():
        if hasattr(db_user, key):
            setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return {"message": "User updated", "user": db_user}


@router.patch("/users/patch/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def patch_user(user_id:int, user_update: UserPatch, db: Session = Depends(get_db)):
    db_user = db.get(User, user_id)
    email_exists = db.query(User).filter(User.email == user_update.email).first()

    if email_exists and email_exists.id != user_id:
        raise EmailTakenException()
    if not db_user:
        raise UserNotFoundException()
    if user_update.username == "admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username 'admin' is not allowed.", headers={'x-error-code': 'INVALID_USERNAME'})

    if user_update.password:
        user_update.password = hash_password(user_update.password)

    for key, value in user_update.model_dump(exclude_unset=True).items():
        if hasattr(db_user, key):
            setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return {"message": "User patched", "user": db_user}

@router.delete("/users/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id:int, db: Session = Depends(get_db)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise UserNotFoundException()
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}