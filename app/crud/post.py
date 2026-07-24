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


async def get_posts(db: AsyncSession) -> Post:
    result = await db.execute(select(Post))
    return result.scalars().all()


async def get_post(db: AsyncSession, post_id: int) -> Post | None:
    result = await db.execute(select(Post).where(Post.id == post_id))
    return result.scalar_one_or_none()
