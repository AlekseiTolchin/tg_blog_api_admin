from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.models.post import Post
from src.domain.repositories.posts import IPostRepository
from src.infrastructure.persistence.sqlalchemy.models import PostORM


class SQLAlchemyPostRepository(IPostRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    def _to_domain_model(self, orm_model: PostORM) -> Optional[Post]:
        if not orm_model:
            return None
        return Post(
            id=orm_model.id,
            title=orm_model.title,
            text=orm_model.text,
            created_at=orm_model.created_at,
        )

    def _to_orm_model(self, domain_model: Post) -> PostORM:
        return PostORM(
            title=domain_model.title,
            text=domain_model.text,
        )

    async def get_by_id(self, post_id: int) -> Optional[Post]:
        orm_post = await self.db_session.scalar(select(PostORM).where(PostORM.id == post_id))
        return self._to_domain_model(orm_post)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Post]:
        res = await self.db_session.scalars(select(PostORM).offset(skip).limit(limit))
        orm_posts = list(res.all())
        return [self._to_domain_model(post) for post in orm_posts]

    async def create(self, post: Post) -> Post:
        post_orm = self._to_orm_model(post)
        self.db_session.add(post_orm)

        await self.db_session.commit()
        await self.db_session.refresh(post_orm)

        return self._to_domain_model(post_orm)

    async def update(self, post: Post) -> Post:
        orm_post = await self.db_session.scalar(select(PostORM).where(PostORM.id == post.id))
        if not orm_post:
            return None

        orm_post.title = post.title
        orm_post.text = post.text

        await self.db_session.commit()
        await self.db_session.refresh(orm_post)

        return self._to_domain_model(orm_post)

    async def delete(self, post_id: int) -> bool:
        orm_post = await self.db_session.scalar(select(PostORM).where(PostORM.id == post_id))
        if not orm_post:
            return False

        await self.db_session.delete(orm_post)
        await self.db_session.commit()

        return True
