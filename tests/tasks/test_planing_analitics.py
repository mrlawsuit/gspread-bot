import sys
import os
from datetime import datetime, UTC, timedelta
module_path = os.path.abspath('/home/oleg/Рабочий стол/shering/shering')
if module_path not in sys.path:
    sys.path.append(module_path)

import pytest
from unittest.mock import AsyncMock, patch, Mock
from app.tasks.planing_and_analitics import maintenance_needed


@pytest.mark.asyncio
async def test_no_available_vehicles():
    with patch(
        'app.tasks.planing_and_analitics.db.get_available_vehicles',
        new_callable=AsyncMock
    ) as mock_get_available_vehicles, \
        patch(
            'app.tasks.planing_and_analitics.get_last_outdated_maintenance',
            new_callable=AsyncMock
        ) as mock_get_last_outdated_maintenance:
        mock_get_available_vehicles.return_value = []
        mock_get_last_outdated_maintenance.return_value = {}
        result = await maintenance_needed()
        assert result == ()


@pytest.mark.asyncio
async def test_all_vehicles_have_active_maintenance():
    with patch(
        'app.tasks.planing_and_analitics.db.get_available_vehicles',
        new_callable=AsyncMock
    ) as mock_get_available_vehicles, \
         patch(
             'app.tasks.planing_and_analitics.db.maintenance_status_check',
             new_callable=AsyncMock
         ) as mock_maintenance_status_check:
        vehicle = Mock()
        vehicle.id = 1
        vehicle.mileage = 5000
        mock_get_available_vehicles.return_value = [vehicle]
        mock_maintenance_status_check.return_value = False  # У машины ведется обслуживание
        result = await maintenance_needed()
        assert result == ()


@pytest.mark.asyncio
async def test_vehicle_needs_maintenance_due_to_date():
    with patch(
        'app.tasks.planing_and_analitics.get_last_outdated_maintenance',
        new_callable=AsyncMock
    ) as mock_get_last_outdated_maintenance:
        vehicle = Mock()
        vehicle.id = 1
        vehicle.mileage = 5000
        mock_get_last_outdated_maintenance.return_value = {(1, 20000): vehicle}
        result = await maintenance_needed()
        assert result == (1,)


@pytest.mark.asyncio
async def test_vehicle_needs_maintenance_due_to_mileage():
    with patch(
        'app.tasks.planing_and_analitics.db.get_available_vehicles',
        new_callable=AsyncMock
    ) as mock_get_available_vehicles, \
         patch(
             'app.tasks.planing_and_analitics.db.maintenance_status_check',
             new_callable=AsyncMock
         ) as mock_maintenance_status_check, \
         patch(
             'app.tasks.planing_and_analitics.db.get_last_maintenance_by_id',
             new_callable=AsyncMock
         ) as mock_get_last_maintenance_by_id:
        vehicle = Mock()
        vehicle.id = 1
        vehicle.mileage = 15000
        mock_get_available_vehicles.return_value = [vehicle]
        mock_maintenance_status_check.return_value = True
        last_maintenance_date = datetime.now(UTC)
        last_maintenance_mileage = 4000
        mock_get_last_maintenance_by_id.return_value = (
            last_maintenance_date,
            last_maintenance_mileage
        )
        result = await maintenance_needed()
        assert result == (1,)


@pytest.mark.asyncio
async def test_vehicle_does_not_need_maintenance():
    with patch(
        'app.tasks.planing_and_analitics.db.get_available_vehicles',
        new_callable=AsyncMock
    ) as mock_get_available_vehicles, \
         patch(
             'app.tasks.planing_and_analitics.db.maintenance_status_check',
             new_callable=AsyncMock
         ) as mock_maintenance_status_check, \
         patch(
             'app.tasks.planing_and_analitics.db.get_last_maintenance_by_id',
             new_callable=AsyncMock
         ) as mock_get_last_maintenance_by_id:
        vehicle = Mock()
        vehicle.id = 1
        vehicle.mileage = 5000
        mock_get_available_vehicles.return_value = [vehicle]
        mock_maintenance_status_check.return_value = True
        last_maintenance_date = datetime.now(UTC) - timedelta(days=100)
        last_maintenance_mileage = 4000
        mock_get_last_maintenance_by_id.return_value = (
            last_maintenance_date,
            last_maintenance_mileage
        )
        result = await maintenance_needed()
        assert result == ()
