from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, status, HTTPException

from src.application.schemas.post import PostCreate, PostUpdate, PostResponse
from src.application.services.post_service import PostService
from src.presentation.dependencies import get_post_service

router = APIRouter(
    prefix='/api/posts',
    tags=['posts']
)


@router.get('/', response_model=List[PostResponse])
async def get_posts(
    service: Annotated[PostService, Depends(get_post_service)],
    skip: Optional[int] = None,
    limit: Optional[int] = None,
):
    """Получить все посты."""
    posts = await service.get_all_posts(skip, limit)
    return [PostResponse.model_validate(post) for post in posts]


@router.get('/{post_id}', response_model=PostResponse)
async def get_post(
    post_id: int,
    service: Annotated[PostService, Depends(get_post_service)]
):
    """Получить пост по ID."""
    post = await service.get_post_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found',
        )
    return PostResponse.model_validate(post)


@router.post('/', response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: Annotated[PostCreate, Depends()],
    service: Annotated[PostService, Depends(get_post_service)]
):
    """Создать новый пост."""
    try:
        new_post = await service.create_post(post_data)
        return PostResponse.model_validate(new_post)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'An unexpected error occurred: {e}')


@router.put('/{post_id}', response_model=PostResponse)
async def update_post(
    post_data: Annotated[PostUpdate, Depends()],
    service: Annotated[PostService, Depends(get_post_service)],
):
    """Обновить существующий пост."""
    updated_post = await service.update_post(post_data)
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    return PostResponse.model_validate(updated_post)


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    service: Annotated[PostService, Depends(get_post_service)],
    ):
    """Удалить существующий пост."""
    deleted = await service.delete_post(post_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found',
        )
