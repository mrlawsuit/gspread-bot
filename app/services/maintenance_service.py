from ..repositories.maintenances_repository import get_active_maintenances


# вернет false, если есть активные заявки на обслуживание
async def maintenance_status_check(vehicle_id: int):
    maintenances = await get_active_maintenances(vehicle_id)
    if maintenances:
        return False
    return True
