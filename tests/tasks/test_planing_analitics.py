import sys
import os
from datetime import datetime, UTC, timedelta
module_path = os.path.abspath('/home/oleg/Рабочий стол/shering/shering')
if module_path not in sys.path:
    sys.path.append(module_path)

# test_tasks.py

import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
import json

# Импортируем тестируемые функции
from app.tasks.planing_and_analitics import (
    maintenance_needed,
    get_last_outdated_maintenance,
    schedule_maintenance,
    generate_report
)

# Импортируем конфигурационные переменные
from app.tasks.planing_and_analitics import (
    mileage_threshold,
    days_maintenance_threshold,
    current_workshop,
    redis_config_for_db,
    MaintenanceStatus
)



# Тест для функции get_last_outdated_maintenance
@pytest.mark.asyncio
async def test_get_last_outdated_maintenance():
    # Мокируем функции модуля db
    with patch('app.tasks.planing_and_analitics.db.get_available_vehicles', new_callable=AsyncMock) as mock_get_available_vehicles, \
         patch('app.tasks.planing_and_analitics.db.maintenance_status_check', new_callable=AsyncMock) as mock_maintenance_status_check, \
         patch('app.tasks.planing_and_analitics.db.get_last_maintenance_by_id', new_callable=AsyncMock) as mock_get_last_maintenance_by_id:

        # Настраиваем мок-данные
        vehicle1 = MagicMock()
        vehicle1.id = 1
        vehicle1.mileage = 12000

        vehicle2 = MagicMock()
        vehicle2.id = 2
        vehicle2.mileage = 8000

        # Мокируем возвращаемое значение функции get_available_vehicles
        mock_get_available_vehicles.return_value = [vehicle1, vehicle2]

        # Мокируем возвращаемое значение функции maintenance_status_check для каждого автомобиля
        # Предположим, что для vehicle1 возвращается True, для vehicle2 - False
        mock_maintenance_status_check.side_effect = [True, False]

        # Мокируем возвращаемое значение функции get_last_maintenance_by_id
        last_maintenance_date = datetime.now(UTC) - timedelta(days=100)
        last_maintenance_mileage = 5000
        mock_get_last_maintenance_by_id.return_value = (last_maintenance_date, last_maintenance_mileage)

        # Вызываем тестируемую функцию
        result = await get_last_outdated_maintenance()

        # Ожидаемый результат должен включать только vehicle1
        expected_result = {
            (vehicle1.id, vehicle1.mileage): (last_maintenance_date, last_maintenance_mileage)
        }

        assert result == expected_result
        mock_get_available_vehicles.assert_awaited_once()
        assert mock_maintenance_status_check.await_count == 2
        mock_get_last_maintenance_by_id.assert_awaited_once_with(vehicle1.id)

# Тест для функции schedule_maintenance
@pytest.mark.asyncio
async def test_schedule_maintenance():
    # Мокируем функции модуля db
    with patch('app.tasks.planing_and_analitics.db.get_vehicle_by_id', new_callable=AsyncMock) as mock_get_vehicle_by_id, \
         patch('app.tasks.planing_and_analitics.db.add_maintenance', new_callable=AsyncMock) as mock_add_maintenance:
        # Настраиваем мок-данные
        vehicle_id = 1
        vehicle = MagicMock()
        vehicle.id = vehicle_id
        vehicle.mileage = 15000

        mock_get_vehicle_by_id.return_value = vehicle

        # Вызываем тестируемую функцию
        await schedule_maintenance(vehicle_id)

        # Проверяем вызовы моков
        mock_get_vehicle_by_id.assert_awaited_once_with(vehicle_id)
        mock_add_maintenance.assert_awaited_once()

        # Проверяем данные переданные в add_maintenance
        args, kwargs = mock_add_maintenance.call_args
        maintenance_record = args[0]  # Предполагается, что add_maintenance вызывается с объектом записи

        # Проверяем, что запись обслуживания содержит правильные данные
        assert maintenance_record.vehicle_id == vehicle_id
        assert maintenance_record.workshop_id == current_workshop
        expected_service_date = datetime.now(UTC) + timedelta(days=7)
        # Допускаем небольшую разницу во времени выполнения
        assert abs((maintenance_record.service_date - expected_service_date).total_seconds()) < 5
        assert maintenance_record.current_mileage == vehicle.mileage
        assert maintenance_record.status == MaintenanceStatus.planned

# Тест для функции maintenance_needed
@pytest.mark.asyncio
async def test_maintenance_needed():
    # Мокируем функции и внешние зависимости
    with patch('app.tasks.planing_and_analitics.get_last_outdated_maintenance', new_callable=AsyncMock) as mock_get_last_outdated_maintenance, \
         patch('app.tasks.planing_and_analitics.schedule_maintenance', new_callable=AsyncMock) as mock_schedule_maintenance, \
         patch('redis.StrictRedis') as mock_redis_class:

        # Настраиваем мок-данные
        vehicle_id = 1
        current_mileage = 15000
        last_service_date = datetime.now(UTC) - timedelta(days=100)
        last_service_mileage = 5000

        mock_get_last_outdated_maintenance.return_value = {
            (vehicle_id, current_mileage): (last_service_date, last_service_mileage)
        }

        # Мокируем экземпляр Redis
        mock_redis_instance = MagicMock()
        mock_redis_class.return_value = mock_redis_instance

        # Вызываем тестируемую функцию
        result = await maintenance_needed()

        # Проверяем вызовы моков
        mock_get_last_outdated_maintenance.assert_awaited_once()
        mock_schedule_maintenance.assert_awaited_once_with(vehicle_id)

        mock_redis_class.assert_called_with(**redis_config_for_db)
        # Проверяем, что данные записаны в Redis
        vehicles_list = [vehicle_id]
        vehicles_list_json = json.dumps(vehicles_list)
        mock_redis_instance.set.assert_called_with('vehicles_for_maintenance', vehicles_list_json)

        # Проверяем, что функция возвращает ожидаемый результат
        assert result == tuple(vehicles_list)

# Тест для функции generate_report
@pytest.mark.asyncio
async def test_generate_report():
    with patch('app.tasks.planing_and_analitics.db.get_maintenances_per_month', new_callable=AsyncMock) as mock_get_maintenances_per_month, \
         patch('app.tasks.planing_and_analitics.create_report') as mock_create_report:

        # Настраиваем мок-данные
        report_data = [
            {'month': '2023-01', 'count': 10},
            {'month': '2023-02', 'count': 15},
        ]

        mock_get_maintenances_per_month.return_value = report_data

        # Вызываем тестируемую функцию
        await generate_report()

        # Проверяем вызовы моков
        mock_get_maintenances_per_month.assert_awaited_once()
        mock_create_report.assert_called_once_with('maintenance_report', report_data)
