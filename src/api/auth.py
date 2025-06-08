from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.models.users import User
from src.schemas.auth import CreateUser, TokenResponse, RefreshRequest, ReadUser
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from src.dependencies.db import get_db
from src.dependencies.auth import get_current_user
from src.security import bcrypt_context
from src.repositories.user_repository import UserRepository
from src.repositories.token_repository import RefreshTokenRepository
from src.security import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)


router = APIRouter(prefix='/auth', tags=['auth'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')
refresh_token_repo = RefreshTokenRepository()
user_repository = UserRepository()


@router.post('/token', response_model=TokenResponse)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_db)
):
    """Аутентификация и выдача access и refresh токенов."""
    user = await authenticate_user(session, form_data.username, form_data.password)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        username=user.username,
        user_id=user.id,
        expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        username=user.username,
        user_id=user.id,
        expires_delta=refresh_token_expires
    )

    expires_at = datetime.now(timezone.utc) + refresh_token_expires

    await refresh_token_repo.create(
        session=session,
        token=refresh_token,
        user_id=user.id,
        expires_at=expires_at,
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type':'Bearer'
    }


@router.post('/refresh', response_model=TokenResponse)
async def refresh_access_token(
        body: RefreshRequest,
        session: AsyncSession = Depends(get_db)
):
    """Обновление access и refresh токена (рефреш токен инвалидируется после использования)."""
    token_payload = await verify_refresh_token(body.refresh_token, session)

    old_token = await refresh_token_repo.get_by_token(
        session=session,
        token=body.refresh_token,
        active_only=True
    )

    if old_token:
        await refresh_token_repo.revoke(session, body.refresh_token)

    user = await session.scalar(select(User).where(User.id == token_payload['id']))
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        username=user.username,
        user_id=user.id,
        expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        username=user.username,
        user_id=user.id,
        expires_delta=refresh_token_expires
    )

    expires_at = datetime.now(timezone.utc) + refresh_token_expires

    await refresh_token_repo.create(
        session=session,
        token=refresh_token,
        user_id=user.id,
        expires_at=expires_at,
        is_revoked=False,
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer'
    }


@router.post('/register', status_code=201)
async def create_user(
    session: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[CreateUser, Depends()],
):
    """Регистрация нового пользователя."""
    if await user_repository.get_by_username(session, user.username):
        raise HTTPException(status_code=400, detail='User already exists')

    await user_repository.create(
        session=session,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        hashed_password=bcrypt_context.hash(user.password),
    )

    return {'transaction': 'Successful'}


@router.get('/read_current_user', response_model=ReadUser)
async def read_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    """Вернуть текущего пользователя (по access токену)."""
    return current_user
