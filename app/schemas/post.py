from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    content: str
    author: str | None = None


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    author: str | None = None

class PostDelete(BaseModel):
    id: int


class PostRead(BaseModel):
    id: int
    title: str
    content: str
    author: str | None = None
    user_id: int | None = None
    created_at: datetime
