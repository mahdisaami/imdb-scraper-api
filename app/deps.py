from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session

from app.core.security import ALGORITHM, SECRET_KEY
from app.db.session import AsyncSessionLocal
from fastapi.security import OAuth2PasswordBearer

from app.services.users import UserService


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user_service(db: AsyncSession = Depends(get_db)):
    return UserService(db)


def payload_check(token: str = Depends(oauth2_scheme), user_service: UserService = Depends(get_user_service), ):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=401)

    return payload

