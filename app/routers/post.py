from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.post import PostCreate, PostUpdate, PostRead
from app.crud import post as post_crud


router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostRead)
async def create_post(data: PostCreate, db: AsyncSession = Depends(get_db)):
    return await post_crud.create_post(db, data)
