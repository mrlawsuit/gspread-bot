from sqlalchemy import select

from ..models import Vehicle
from ..database import async_session, get_session


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


async def get_vehicle_by_id(vehicle_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(Vehicle).where(Vehicle.id == vehicle_id)
        )
        vehicle = result.scalar_one_or_none()
        return vehicle
