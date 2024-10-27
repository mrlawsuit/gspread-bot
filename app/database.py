from typing import List, AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
)
from sqlalchemy import select, update, delete, desc
from .models import User, Vehicle, VehicleMaintenance
from app.config import DB_URL

engine = create_async_engine(DB_URL, echo=True)


async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_maintenance_by_id(session: AsyncSession, vehicle_id: int):
    result = await session.execute(
        select(VehicleMaintenance).
        where(VehicleMaintenance.vehicle_id == vehicle_id).
        order_by(desc(VehicleMaintenance.id))
    )
    maintenance = result.scalars().first()
    if not maintenance:
        raise ValueError('У машины ещё не проводилось обслуживания')
    return maintenance

async def get_all_available_vehicles(
        session: AsyncSession
):
    result = await session.execute(
        select(Vehicle).
        where(Vehicle.status == 'available')
    )
    vehicles = result.all()
    if not vehicles:
        raise ValueError('Нет свободных автомобилей')
    return vehicles


async def get_user_by_id_db(
        session: AsyncSession,
        id: int
):
    result = await session.execute(
        select(User).
        where(User.id == id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise ValueError('Нет такого пользователя')
    return user
