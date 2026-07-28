from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserUpdate, UserRead, Token
from app.crud import user as user_crud
from app.security import create_access_token, verify_password

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", response_model=UserRead)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    return await user_crud.create_user(db, data)


@router.post("/login", response_model=Token)
async def login(
    data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    user = await user_crud.login_user(db, data)

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    })
    return Token(access_token=access_token)


@router.get("/{user_id}", response_model=UserRead)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    user = await user_crud.get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.get("/", response_model=list[UserRead])
async def read_users(
    db: AsyncSession = Depends(get_db),
):
    return await user_crud.get_users(db)


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
):
    user = await user_crud.get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return await user_crud.update_user(db, user, data)


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    user = await user_crud.get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    await user_crud.delete_user(db, user)