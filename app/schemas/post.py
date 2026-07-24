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
