from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.posts import Post


class PostRepository:
    async def get_all(self, session: AsyncSession) -> List[Post]:
        result = await session.execute(
            select(Post).order_by(Post.created_at.desc())
        )
        posts = result.scalars().all()
        return posts

    async def get_by_id(
            self, session: AsyncSession, post_id: int) -> Optional[Post]:
        result = await session.execute(select(Post).where(Post.id == post_id))
        return result.scalar_one_or_none()

    async def create(self, session: AsyncSession, title: str, text: str) -> Post:
        post = Post(title=title, text=text)
        session.add(post)
        await session.commit()
        await session.refresh(post)
        return post

    async def update(self, session: AsyncSession, post_id: int, title: str, text: str) -> Optional[Post]:
        result = await session.execute(select(Post).where(Post.id == post_id))
        post = result.scalar_one_or_none()
        if not post:
            return None
        post.title = title
        post.text = text
        await session.commit()
        await session.refresh(post)
        return post

    async def delete(self, session: AsyncSession, post_id: int) -> bool:
        result = await session.execute(select(Post).where(Post.id == post_id))
        post = result.scalar_one_or_none()
        if not post:
            return False
        await session.delete(post)
        await session.commit()
        return True
