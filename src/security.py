from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.db import get_db
from src.config import JWT_SECRET_KEY
from src.config import JWT_ALGORITHM
from src.models.users import User
from src.repositories.user_repository import UserRepository
from src.repositories.token_repository import RefreshTokenRepository


CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid authentication credentials',
    headers={'WWW-Authenticate': 'Bearer'}
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')
user_repository = UserRepository()
refresh_token_repo = RefreshTokenRepository()


async def authenticate_user(
        session: Annotated[AsyncSession, Depends(get_db)],
        username: str,
        password: str,
) -> User:
    """
    Проверяет имя пользователя и пароль, возвращает пользователя, если всё ок.
    """
    user = await user_repository.get_by_username(session, username)
    if not user or not bcrypt_context.verify(password, user.hashed_password) or not user.is_active:
        raise CREDENTIALS_EXCEPTION
    return user


def create_token(
    username: str,
    user_id: int,
    expires_delta: timedelta,
    token_type: str = None
) -> str:
    """
    Универсальная функция создания access/refresh токена.
    """
    payload = {
        'sub': username,
        'id': user_id,
        'exp': int((datetime.now(timezone.utc) + expires_delta).timestamp()),
        'token_type': token_type,
    }

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_access_token(username: str, user_id: int, expires_delta: timedelta) -> str:
    """Создание access токена."""
    return create_token(username, user_id, expires_delta, token_type='access')


def create_refresh_token(username: str, user_id: int, expires_delta: timedelta) -> str:
    """Создание refresh токена."""
    return create_token(username, user_id, expires_delta, token_type='refresh')


def verify_access_token(token: str) -> dict:
    """
    Проверяет access токен. Возвращает данные пользователя.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        if payload.get('token_type') != 'access':
            raise CREDENTIALS_EXCEPTION
        username = payload.get('sub')
        user_id = payload.get('id')
        expire = payload.get('exp')

        if not username or not user_id or not expire:
            raise CREDENTIALS_EXCEPTION

        if expire < datetime.now(timezone.utc).timestamp():
            raise CREDENTIALS_EXCEPTION

        return {'username': username, 'id': user_id}

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Access token expired!',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    except jwt.PyJWTError:
        raise CREDENTIALS_EXCEPTION


async def verify_refresh_token(refresh_token: str, session: AsyncSession) -> dict:
    """
    Проверяет refresh токен, возвращает словарь с username и id, если всё ок.
    """
    try:
        payload = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        if payload.get('token_type') != 'refresh':
            raise CREDENTIALS_EXCEPTION

        if payload.get('sub') is None or payload.get('id') is None:
            raise CREDENTIALS_EXCEPTION

        expire = payload.get('exp')
        if expire is None or expire < datetime.now(timezone.utc).timestamp():
            raise CREDENTIALS_EXCEPTION

        db_token = await refresh_token_repo.get_by_token(
            session=session,
            token=refresh_token,
            active_only=True
        )

        if not db_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Refresh token not found or revoked'
            )
        expires_at = db_token.expires_at
        if not expires_at.tzinfo:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if expires_at < datetime.now(timezone.utc):
            db_token.is_revoked = True
            await session.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Refresh token expired in database'
            )

        return {
            'username': payload['sub'],
            'id': payload['id']
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token expired!'
        )

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid refresh token'
        )
