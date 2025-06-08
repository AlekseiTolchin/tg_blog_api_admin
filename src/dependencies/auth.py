from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.dependencies.db import get_db
from src.models.users import User
from src.security import verify_access_token, CREDENTIALS_EXCEPTION
from src.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')
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
