from typing import List, AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
)
from sqlalchemy import select, update, delete
from .models import User, Vehicle
from app.config import DB_URL

engine = create_async_engine(DB_URL, echo=True)


async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_all_available_vehicles(
        session: AsyncSession
):
    result = await session.execute(
        select(Vehicle).where(Vehicle.status == 'available')
    )
    vehicles = result.all()
    if not vehicles:
        raise ValueError('Нет свободных автомобилей')
    return vehicles


async def get_user_by_id_db(
        session: AsyncSession,
        id: int
):
    result = await session.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    if not user:
        raise ValueError('Нет такого пользователя')
    return user
