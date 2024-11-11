from datetime import datetime, UTC, timedelta


from sqlalchemy import select, desc, or_, and_

from ..schemas import CreateMaintenance, MaintenanceStatus
from ..models import VehicleMaintenance
from ..database import async_session


async def get_active_maintenances(vehicle_id: int):
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
    return maintenances


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
