from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette import status

from app.core.security import verify_password, create_access_token, hash_password
from app.deps import get_db, get_current_user, get_user_service
from app.models import User
from app.schemas.users import UserRead, UserCreate, UserResponse, UserPatch
from app.services.exceptions import EmailTakenException
from app.services.users import  UserService

router = APIRouter(tags=["users"])

@router.post("/users/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user:UserCreate, user_service: UserService = Depends(get_user_service)):
    db_user = user_service.db.query(User).filter(
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

    saved_instance = user_service.db_add_commit_refresh( new_user)

    return {"message": "User created successfully", "user": saved_instance}


@router.get("/users/get/{user_id}", response_model=UserResponse)
async def get_user(user_id:int, user_service: UserService = Depends(get_user_service)):
    db_user = user_service.get_user_by_id_or_404(user_id)
    return {"message": "User fetched successfully", "user": db_user}


@router.get("/users", response_model=list[UserRead])
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    db_users = user_service.get_all_users_db()
    return db_users


@router.post("/users/login")
def login(form: OAuth2PasswordRequestForm = Depends(), user_service: UserService = Depends(get_user_service)):
    user = user_service.get_user_by_username(username=form.username)

    if not verify_password(form.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials.", headers={'x-error-code': 'INVALID_CREDENTIALS'})

    token = create_access_token({"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/profile", response_model=UserResponse)
def profile(user = Depends(get_current_user)):
    return {"message": "Profile fetched successfully", "user": user}


@router.put("/users/update/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id:int, user_update: UserCreate, user_service: UserService = Depends(get_user_service)):
    db_user = user_service.get_user_by_id_or_404(user_id)
    email_exists = user_service.db.query(User).filter(User.email == user_update.email).first()

    if email_exists and email_exists.id != user_id:
        raise EmailTakenException()

    if user_update.username == "admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username 'admin' is not allowed.", headers={'x-error-code': 'INVALID_USERNAME'})

    user_update.password = hash_password(user_update.password)
    for key, value in user_update.model_dump().items():
        if hasattr(db_user, key):
            setattr(db_user, key, value)

    saved_instance = user_service.db_commit_refresh(db_user)

    return {"message": "User updated", "user": saved_instance}


@router.patch("/users/patch/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def patch_user(user_id:int, user_update: UserPatch, user_service: UserService = Depends(get_user_service)):
    db_user = user_service.get_user_by_id_or_404(user_id)
    email_exists = user_service.db.query(User).filter(User.email == user_update.email).first()

    if email_exists and email_exists.id != user_id:
        raise EmailTakenException()

    if user_update.username == "admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username 'admin' is not allowed.", headers={'x-error-code': 'INVALID_USERNAME'})

    if user_update.password:
        user_update.password = hash_password(user_update.password)

    for key, value in user_update.model_dump(exclude_unset=True).items():
        if hasattr(db_user, key):
            setattr(db_user, key, value)

    saved_instance = user_service.db_commit_refresh( db_user)

    return {"message": "User patched", "user": saved_instance}


@router.delete("/users/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id:int, user_service: UserService = Depends(get_user_service)):
    db_user = user_service.get_user_by_id_or_404(user_id)

    user_service.db_delete_commit( db_user)

    return {"message": "User deleted successfully"}