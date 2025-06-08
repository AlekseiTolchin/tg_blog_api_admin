from typing import List, Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.auth import get_current_user
from src.schemas.posts import PostCreate, PostResponse, PostUpdate
from src.models.users import User
from src.repositories.post_repository import PostRepository
from src.dependencies.db import get_db

router = APIRouter(
    prefix='/api/posts',
    tags=['posts']
)

post_repository = PostRepository()


@router.get('/', response_model=List[PostResponse])
async def get_posts(
    session: AsyncSession = Depends(get_db)
):
    """Получить все посты."""
    posts = await post_repository.get_all(session)
    return posts


@router.get('/{post_id}', response_model=PostResponse)
async def get_post(
    post_id: int,
    session: AsyncSession = Depends(get_db),
):
    """Получить пост по ID."""
    post = await post_repository.get_by_id(session, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found',
        )
    return post


@router.post('/', response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: Annotated[PostCreate, Depends()],
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Создать новый пост (требуется аутентификация)."""
    new_post = await post_repository.create(
        session,
        title=post_data.title,
        text=post_data.text,
    )
    return new_post


@router.put('/{post_id}', response_model=PostResponse)
async def update_post(
    post_id: int,
    post_data: Annotated[PostUpdate, Depends()],
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Обновить существующий пост (требуется аутентификация)."""
    post = await post_repository.update(
        session,
        post_id,
        title=post_data.title,
        text=post_data.text
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    return post


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Обновить существующий пост (требуется аутентификация)."""
    deleted = await post_repository.delete(session, post_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found',
        )
