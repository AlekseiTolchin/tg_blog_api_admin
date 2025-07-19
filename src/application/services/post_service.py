from typing import List, Optional

from src.domain.models.post import Post
from src.domain.repositories.posts import IPostRepository
from src.application.schemas.post import PostCreate, PostUpdate


class PostService:
    def __init__(self, post_repo: IPostRepository):
        self.post_repo = post_repo

    async def get_post_by_id(self, post_id: int) -> Optional[Post]:
        return await self.post_repo.get_by_id(post_id)

    async def get_all_posts(self, skip: int = 0, limit: int = 100) -> List[Post]:
        return await self.post_repo.get_all(skip, limit)

    async def create_post(self, post_data: PostCreate) -> Post:
        new_post = Post(
            title=post_data.title,
            text=post_data.text,
        )

        return await self.post_repo.create(new_post)

    async def update_post(self, post_data: PostUpdate) -> Optional[Post]:
        existing_post = await self.post_repo.get_by_id(post_data.id)
        if not existing_post:
            return None
        updated_post = Post(
            id=post_data.id,
            title=post_data.title,
            text=post_data.text,
            created_at=existing_post.created_at
        )
        return await self.post_repo.update(updated_post)

    async def delete_post(self, post_id: int) -> bool:
        return await self.post_repo.delete(post_id)
