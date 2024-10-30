import sys
import os
from datetime import datetime, UTC, timedelta
module_path = os.path.abspath('/home/oleg/Рабочий стол/shering/shering')
if module_path not in sys.path:
    sys.path.append(module_path)

import pytest
from unittest.mock import AsyncMock, patch, Mock, call
from app.tasks.maintenance_and_analitics import maintenance_needed


@pytest.mark.asyncio
@patch('app.tasks.maintenance_and_analitics.mileage_threshold', 10000)
@patch('app.tasks.maintenance_and_analitics.days_maintenance_threshold', 182)
async def test_maintenance_needed_success():
    with patch('app.tasks.maintenance_and_analitics.db.get_available_vehicles', new_callable=AsyncMock) as mock_get_available_vehicles, \
         patch('app.tasks.maintenance_and_analitics.db.maintenance_status_check', new_callable=AsyncMock) as mock_maintenance_status_check, \
         patch('app.tasks.maintenance_and_analitics.db.get_last_maintenance_by_id', new_callable=AsyncMock) as mock_get_last_maintenance_by_id:
        vehicle1 = Mock()
        vehicle1.id = 1
        vehicle1.mileage = 15000  # Требует обслуживания по пробегу

        vehicle2 = Mock()
        vehicle2.id = 2
        vehicle2.mileage = 2000   # Не требует обслуживания

        vehicle3 = Mock()
        vehicle3.id = 3
        vehicle3.mileage = 7000

        mock_get_available_vehicles.return_value = [vehicle1, vehicle2, vehicle3]
        
        mock_maintenance_status_check.side_effect = [True, False, True]

        mock_last_maintenance = Mock()
        mock_last_maintenance.date = datetime.now(UTC) - timedelta(days=200)
        mock_last_maintenance.mileage = 3000

        mock_get_last_maintenance_by_id.side_effect = [
            (mock_last_maintenance.date, mock_last_maintenance.mileage),
            (mock_last_maintenance.date, mock_last_maintenance.mileage),
            (mock_last_maintenance.date, mock_last_maintenance.mileage)
        ]

        maintenance_list = await maintenance_needed()
        assert maintenance_list == (1, 3)

        mock_get_available_vehicles.assert_called_once()
        mock_maintenance_status_check.assert_has_calls([
            call(vehicle1.id),
            call(vehicle2.id),
            call(vehicle3.id)
        ], any_order=False)
        mock_get_last_maintenance_by_id.assert_has_calls([
            call(vehicle1.id),
            call(vehicle3.id)
        ], any_order=False)



'''
@pytest.mark.asyncio
@patch('app.tasks.maintenance_and_analitics.mileage_threshold', 10000)
@patch('app.tasks.maintenance_and_analitics.days_maintenance_threshold', 182)
@patch('app.tasks.maintenance_and_analitics.db.get_available_vehicles', new_callable=AsyncMock)
@patch('app.tasks.maintenance_and_analitics.db.maintenance_status_check', new_callable=AsyncMock)
@patch('app.tasks.maintenance_and_analitics.db.get_last_maintenance_by_id', new_callable=AsyncMock)
async def test_maintenance_needed_success(
    mock_get_available_vehicles,
    mock_maintenance_status_check,
    mock_get_last_maintenance_by_id,
):

    vehicle1 = AsyncMock()
    vehicle1.id = 1
    vehicle1.mileage = 15000  # Требует обслуживания по пробегу

    vehicle2 = AsyncMock()
    vehicle2.id = 2
    vehicle2.mileage = 2000   # Не требует обслуживания

    vehicle3 = AsyncMock()
    vehicle3.id = 3
    vehicle3.mileage = 7000 

    mock_get_available_vehicles.__aiter__.return_value = [vehicle1, vehicle2, vehicle3]
    
    mock_maintenance_status_check.return_value = True

    mock_last_maintenance = Mock()
    mock_last_maintenance.date = datetime.now(UTC) - timedelta(days=200)
    mock_last_maintenance.mileage = 15000

    mock_get_last_maintenance_by_id.return_value = (
        mock_last_maintenance
    )

    maintenance_list = await maintenance_needed()
    assert maintenance_list == (1,)

    mock_get_available_vehicles.assert_called_once()
    mock_maintenance_status_check.assert_called_once_with(mock_vehicle.id)
    mock_get_last_maintenance_by_id.assert_called_once_with(mock_vehicle.id)'''