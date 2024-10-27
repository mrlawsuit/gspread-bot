from datetime import datetime, timedelta, UTC

from celery import shared_task
from sqlalchemy.orm import Session

from ..models import Vehicle, VehicleMaintenance
from .. import database
from .. import config


@shared_task
async def check_vehicle_maintenance():
    async with database.get_session() as session:
        vehicles = await database.get_all_available_vehicles(session)
        for vehicle in vehicles:
            if maintenance_needed(vehicle):
                schedule_maintenance()



async def maintenance_needed(vehicle_id: Vehicle):
    async with database.get_session() as session:
        maintenance = await database.get_maintenance_by_id(session, vehicle_id)
        date = maintenance.service_date
        if datetime.now(UTC) - date > 6:
            return True
        


