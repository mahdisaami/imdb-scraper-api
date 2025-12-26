from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import InternalError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from app.models import User
from app.services.exceptions import UserNotFoundException, EmailTakenException


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_username(self, username: str):
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        query = result.scalars().one_or_none()
        if not query:
            raise UserNotFoundException()
        return query

    async def get_user_by_id_or_404(self, user_id: int):
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        query = result.scalars().first()
        if not query:
            raise UserNotFoundException()
        return query

    async def get_all_users_db(self):
        result = await self.db.execute(select(User))
        users = result.scalars().all()
        return users


    async def db_delete_commit(self, instance):
        await self.db.delete(instance)
        await self.db.commit()

    async def db_commit_refresh(self, instance):
        try:
            await self.db.commit()
            await self.db.refresh(instance)
            return instance

        except IntegrityError:
            await self.db.rollback()
            raise EmailTakenException()

    async def db_add_commit_refresh(self, instance):
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance