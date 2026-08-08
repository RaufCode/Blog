from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentRead
from app.crud import comment as comment_crud, post as post_crud

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["comments"])


@router.get("/", response_model=list[CommentRead])
async def read_comments(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await post_crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return await comment_crud.get_comments_for_post(db, post_id)


@router.post("/", response_model=CommentRead, status_code=201)
async def create_comment(
    post_id: int,
    data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = await post_crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return await comment_crud.create_comment(db, post_id, current_user.id, data)


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(
    post_id: int,
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = await comment_crud.get_comment(db, comment_id)
    if not comment or comment.post_id != post_id:
        raise HTTPException(status_code=404, detail="Comment not found")

    post = await post_crud.get_post(db, post_id)
    is_comment_author = comment.user_id == current_user.id
    is_post_owner = post is not None and post.user_id == current_user.id
    if not is_comment_author and not is_post_owner:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own comments",
        )

    await comment_crud.delete_comment(db, comment)
