from pydantic import BaseModel
from datetime import datetime


class CommentCreate(BaseModel):
    content: str


class CommentAuthor(BaseModel):
    id: int
    first_name: str
    last_name: str


class CommentRead(BaseModel):
    id: int
    content: str
    post_id: int
    created_at: datetime
    author: CommentAuthor
