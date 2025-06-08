from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User


class UserRepository:
    async def create(
            self,
            session: AsyncSession,
            first_name: str,
            last_name: str,
            username: str,
            hashed_password: str,
            is_active: bool = True,
    ) -> User:
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            hashed_password=hashed_password,
            is_active=is_active,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def get_by_id(self, session: AsyncSession, user_id: int) -> Optional[User]:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_username(self, session: AsyncSession, username: str) -> Optional[User]:
        """Получает пользователя по имени пользователя"""
        result = await session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
