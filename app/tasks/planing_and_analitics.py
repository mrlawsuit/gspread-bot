from datetime import datetime, UTC, timedelta

import redis
from celery import shared_task

from .reports import create_report
from .. import database as db
from ..config import (
    mileage_threshold,
    days_maintenance_threshold,
    current_workshop,
    redis_config_for_db
)
from ..schemas import CreateMaintenance, MaintenanceStatus


@shared_task
async def maintenance_needed():
    '''Проверяет нужно ли автомобилю обслуживание
    по пробегу, либо по времени последнего обслуживания'''
    maintenances = await get_vehicles_without_actual_maintenance()
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
            await schedule_maintenance(key[0])
            vehicles_list.append(key[0])
    redis_tool = redis.StrictRedis(**redis_config_for_db)
    redis_tool.set('vehicles_for_maintenance', vehicles_list)
    return tuple(vehicles_list)


async def get_vehicles_without_actual_maintenance() -> dict:
    '''Достает свободные автомобили из базы,
    проверяет на наличие запланированного,
    либо длящегося обслуживания,
    возвращает словарь с ключем в виде кортежа (id, пробег)
    и значением - датой последнего совершенного обслуживания '''
    maintenances = {}
    vehicles = await db.get_available_vehicles()
    for vehicle in vehicles:
        check = await db.maintenance_status_check(vehicle.id)
        if check:
            maintenance_data = await db.get_last_maintenance_by_id(vehicle.id)
            maintenances[(vehicle.id, vehicle.mileage)] = maintenance_data
    return maintenances


async def schedule_maintenance(vehicle_id: int):
    '''Создает запись на обслуживание в БД с датой на 7 дней от сегодняшнего.
    Мастерская определяется константой'''
    vehicle = await db.get_vehicle_by_id(vehicle_id)
    new_maintenance = CreateMaintenance(
        vehicle_id=vehicle.id,
        workshop_id=current_workshop,
        service_date=datetime.now(UTC) + timedelta(days=7),
        current_mileage=vehicle.mileage,
        status=MaintenanceStatus.planned
    )
    await db.add_maintenance(new_maintenance)


@shared_task
async def generate_report():
    report_data = await db.get_maintenances_per_month()
    create_report('maintenance_report', report_data)
