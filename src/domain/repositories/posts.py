from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.models.post import Post


class IPostRepository(ABC):
    @abstractmethod
    async def get_by_id(self, post_id: int) -> Optional[Post]:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Post]:
        pass

    @abstractmethod
    async def create(self, post: Post) -> Post:
        pass

    @abstractmethod
    async def update(self, post: Post) -> Post:
        pass

    @abstractmethod
    async def delete(self, post_id: int) -> bool:
        pass
