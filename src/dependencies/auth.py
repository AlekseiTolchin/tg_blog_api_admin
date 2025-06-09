from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.db import get_db
from src.models.users import User
from src.security import (
    CREDENTIALS_EXCEPTION,
    oauth2_scheme,
    verify_access_token,
)
from src.repositories.user_repository import UserRepository

user_repository = UserRepository()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_db),
) -> User:
    """
    Получить пользователя по access токену, используется как Depends.
    """
    payload = verify_access_token(token)
    user = await user_repository.get_by_id(session, payload['id'])
    if not user or not user.is_active:
        raise CREDENTIALS_EXCEPTION
    return user
