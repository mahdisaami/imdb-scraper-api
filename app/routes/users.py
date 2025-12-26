from fastapi import Depends, HTTPException, APIRouter, Body
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from starlette import status

from app.core.security import verify_password, create_access_token, hash_password, create_refresh_token, SECRET_KEY, \
    ALGORITHM
from app.deps import get_db, payload_check, get_user_service
from app.models import User
from app.schemas.users import UserRead, UserCreate, UserResponse, UserPatch
from app.services.exceptions import EmailTakenException
from app.services.users import  UserService

router = APIRouter(tags=["users"])

@router.post("/users/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user:UserCreate, user_service: UserService = Depends(get_user_service)):
    stmt = select(User).where(
        or_(
            User.username == user.username,
            User.email == user.email
        )
    )

    result = await user_service.db.execute(stmt)
    db_user = result.scalars().one_or_none()

    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username Or Email already registered.", headers={'x-error-code': 'USERNAME_OR_EMAIL_TAKEN'})

    elif user.username == "admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username 'admin' is not allowed.", headers={'x-error-code': 'INVALID_USERNAME'})

    user.password = hash_password(user.password)
    new_user = User(**user.model_dump())

    saved_instance = await user_service.db_add_commit_refresh( new_user)

    return {"message": "User created successfully", "user": saved_instance}


@router.get("/users/get/{user_id}", response_model=UserResponse)
async def get_user(user_id:int, user_service: UserService = Depends(get_user_service), payload = Depends(payload_check)):
    db_user = await user_service.get_user_by_id_or_404(user_id)
    return {"message": "User fetched successfully", "user": db_user}


@router.get("/users", response_model=list[UserRead])
async def get_all_users(user_service: UserService = Depends(get_user_service), user=Depends(payload_check)):
    db_users = await user_service.get_all_users_db()
    return db_users


@router.post("/users/login")
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.get_user_by_username(form.username)

    if not verify_password(form.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/users/refresh")
async def refresh(refresh_token: str = Body(...)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Wrong token type")

    username = payload.get("sub")
    new_access_token = create_access_token({"sub": username})

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }



@router.get("/profile", response_model=UserResponse)
async def profile(payload = Depends(payload_check), user_service: UserService = Depends(get_user_service)):
    username = payload.get("sub")
    user = await user_service.get_user_by_username(username=username)

    return {"message": "Profile fetched successfully", "user": user}


@router.put("/users/update/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_update: UserCreate, user_service: UserService = Depends(get_user_service), payload = Depends(payload_check)):
    username = payload.get("sub")
    db_user = await user_service.get_user_by_username(username=username)

    if user_update.username == "admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username 'admin' is not allowed.", headers={'x-error-code': 'INVALID_USERNAME'})

    user_update.password = hash_password(user_update.password)
    for key, value in user_update.model_dump().items():
        if hasattr(db_user, key):
            setattr(db_user, key, value)

    saved_instance = await user_service.db_commit_refresh(db_user)

    return {"message": "User updated", "user": saved_instance}


@router.patch("/users/patch/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def patch_user(user_update: UserPatch, user_service: UserService = Depends(get_user_service), payload = Depends(payload_check)):
    username = payload.get("sub")
    db_user = await user_service.get_user_by_username(username)

    if user_update.username == "admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username 'admin' is not allowed.", headers={'x-error-code': 'INVALID_USERNAME'})

    if user_update.password:
        user_update.password = hash_password(user_update.password)

    for key, value in user_update.model_dump(exclude_unset=True).items():
        if hasattr(db_user, key):
            setattr(db_user, key, value)

    saved_instance = await user_service.db_commit_refresh( db_user)

    return {"message": "User patched", "user": saved_instance}


@router.delete("/users/delete/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_service: UserService = Depends(get_user_service),payload = Depends(payload_check)):
    username = payload.get("sub")
    db_user = await user_service.get_user_by_username(username)

    await user_service.db_delete_commit( db_user)

    return {"message": "User deleted successfully"}