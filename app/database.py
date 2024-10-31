from typing import AsyncGenerator
from datetime import datetime, UTC, timedelta

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from contextlib import asynccontextmanager
from sqlalchemy import select, desc, or_, and_ 

from .models import User, Vehicle, VehicleMaintenance
from .config import DB_URL
from .schemas import CreateMaintenance, Role, MaintenanceStatus


engine = create_async_engine(DB_URL, echo=True)


async_session = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


# хэндлеры для таблицы машин и обслуживания
async def get_available_vehicles():
    async with get_session() as session:
        result = await session.execute(
            select(Vehicle).
            where(Vehicle.status == 'available')
        )
        vehicles = result.scalars().all()
        if not vehicles:
            raise ValueError('Нет свободных автомобилей')
        return vehicles


# вернет false, если есть акттивные заявки на обслуживание
async def maintenance_status_check(vehicle_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(VehicleMaintenance).
            where(
                VehicleMaintenance.vehicle_id == vehicle_id,
                or_(
                    VehicleMaintenance.status == 'in_process',
                    VehicleMaintenance.status == 'planned'
                )
            )
        )
        maintenances = result.scalars().all()
        if maintenances:
            return False
        return True


# вернет кортеж из даты обслуживания и пробега на момент обслуживания
async def get_last_maintenance_by_id(vehicle_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(VehicleMaintenance).
            where(
                VehicleMaintenance.vehicle_id == vehicle_id,
            ).
            order_by(desc(VehicleMaintenance.service_date))
        )
        maintenance = result.scalars().first()

        return (maintenance.service_date, maintenance.current_mileage)


# добавляет забись на обслуживание
async def add_maintenance(maintenance: CreateMaintenance):
    async with async_session() as session:
        new_maintenance = maintenance.model_dump()
        await session.add(VehicleMaintenance(**new_maintenance))
        await session.commit()


async def get_vehicle_by_id(vehicle_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(Vehicle).where(Vehicle.id == vehicle_id)
        )
        vehicle = result.scalar_one_or_none()
        return vehicle


async def get_admins_id() -> list:
    async with async_session() as session:
        result = await session.execute(
            select(User.id).
            where(
                User.role == Role.admin,
                User.acc_status
            )
        )
        admins_id = result.scalars().all()
    return admins_id


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


async def get_maintenances_per_month():
    time_period = datetime.now(UTC) - timedelta(days=30)
    async with async_session() as session:
        result = await session.execute(
            select(VehicleMaintenance).
            where(
                VehicleMaintenance.service_date >= time_period,
                and_(VehicleMaintenance.status == MaintenanceStatus.done)
            )
        )
        maintenances = result.scalars().all()
    return maintenances
