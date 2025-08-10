from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.repositories.posts import IPostRepository
from src.infrastructure.persistence.sqlalchemy.post_repository import \
    SQLAlchemyPostRepository
from src.application.services.post_service import PostService
from src.infrastructure.database.connection import async_session


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


def get_post_repository_impl(db_session: AsyncSession = Depends(get_db_session)) -> IPostRepository:
    return SQLAlchemyPostRepository(db_session=db_session)


def get_post_service_impl(post_repo: IPostRepository = Depends(get_post_repository_impl)) -> PostService:
    return PostService(post_repo=post_repo)
