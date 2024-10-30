from datetime import datetime, UTC
from celery import shared_task
from .. import database as db
from ..config import mileage_threshold, days_maintenance_threshold


@shared_task
async def maintenance_needed() -> tuple:
    
    maintenances = {}
    vehicles = await db.get_available_vehicles()
    for vehicle in vehicles:
        check = await db.maintenance_status_check(vehicle.id)
        if check:
            maintenance_data = await db.get_last_maintenance_by_id(vehicle.id)
            maintenances[(vehicle.id, vehicle.mileage)] = maintenance_data
    vehicles_list = []
    # key - кортеж из id и пробега,
    # value - кортеж из даты и пробега на дату последнего обслуживания
    for key, value in maintenances.items():
        date_difference = datetime.now(UTC) - value[0]
        mile_difference = key[1] - value[1]
        if (
            date_difference.days >= days_maintenance_threshold or
            mile_difference >= mileage_threshold
        ):
            vehicles_list.append(key[0])
    return tuple(vehicles_list)


if __name__ == '__main__':
    print()