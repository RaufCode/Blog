from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate, PostRead
from app.crud import post as post_crud
from app.services import ai as ai_service


router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostRead)
async def create_post(
    data: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await post_crud.create_post(db, data, current_user.id)

@router.get("/{post_id}", response_model=PostRead)
async def read_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await post_crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.get("/", response_model=list[PostRead])
async def read_post(db: AsyncSession = Depends(get_db)):
    return await post_crud.get_posts(db)

@router.put("/{post_id}", response_model=PostRead)
async def update_post(post_id: int, data: PostUpdate, db: AsyncSession = Depends(get_db)):
    post = await post_crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return await post_crud.update_post(db, post, data)

@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await post_crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await post_crud.delete_post(db, post)



@router.post("/{post_id}/summarize")
async def summarize_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await post_crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    summary = await ai_service.summarize_text(post.content)
    return {"summary": summary}
    