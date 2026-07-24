from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate, PostDelete, PostRead
async def create_post(db: AsyncSession, data: PostCreate) -> Post:
    post = Post(**data.model_dump())
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post
