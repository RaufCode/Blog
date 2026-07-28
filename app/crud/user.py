from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserUpdate, UserDelete, UserRead


async def create_user(db: AsyncSession, data: UserCreate) -> User:
    user = User(**data.model_dump())

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User))
    return result.scalars().all()


async def login_user(db: AsyncSession, data: UserLogin) -> User | None:
    result = await db.execute(
        select(User).where(User.email == data.email)
    )
    return result.scalar_one_or_none()


async def update_user(
    db: AsyncSession,
    user: User,
    data: UserUpdate,
) -> User:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    return user

async def delete_user(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.commit()