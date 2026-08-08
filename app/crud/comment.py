from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment
from app.schemas.comment import CommentCreate


async def create_comment(
    db: AsyncSession, post_id: int, user_id: int, data: CommentCreate
) -> Comment:
    comment = Comment(content=data.content, post_id=post_id, user_id=user_id)
    db.add(comment)
    await db.commit()
    # re-fetch so the joined `author` relationship is populated (avoids
    # lazy-loading it later outside the async session context)
    return await get_comment(db, comment.id)


async def get_comments_for_post(db: AsyncSession, post_id: int) -> list[Comment]:
    result = await db.execute(
        select(Comment)
        .where(Comment.post_id == post_id)
        .order_by(Comment.created_at.asc())
    )
    return result.scalars().all()


async def get_comment(db: AsyncSession, comment_id: int) -> Comment | None:
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    return result.scalar_one_or_none()


async def delete_comment(db: AsyncSession, comment: Comment) -> None:
    await db.delete(comment)
    await db.commit()
