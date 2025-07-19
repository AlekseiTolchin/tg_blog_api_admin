from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Post:
    title: str
    text: str
    created_at: Optional[datetime] = None
    id: Optional[int] = None
