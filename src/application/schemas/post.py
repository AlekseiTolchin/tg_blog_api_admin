from datetime import datetime

from pydantic import BaseModel, ConfigDict

class PostBase(BaseModel):
    title: str
    text: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    id: int


class PostResponse(PostBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
