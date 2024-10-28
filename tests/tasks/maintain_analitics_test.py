import sys
import os

import pytest
from unittest.mock import AsyncMock, patch, Mock

module_path = os.path.abspath('/home/oleg/Рабочий стол/shering/shering')
if module_path not in sys.path:
    sys.path.append(module_path)



@pytest.mark.ayncio
@patch('app.task.maintenance_and_analitics.config.mileage_threshold')
@patch('app.task.maintenance_and_analitics.config.days_maintenance_threshold')
@patch('app.task.maintenance_and_analitics.database.get_available_vehicles')
@patch('app.task.maintenance_and_analitics.database.maintenance_status_check')
@patch('app.task.maintenance_and_analitics.database.get_last_maintenance_by_id')
async def test_maintenance_needed_success(
    mock_config_mileage_threshold,
    mock_config_days_maintenance_threshold,
    mock_get_available_vehicles,
    mock_maintenance_status_check,
    mock_maintenance_get_last_maintenance_by_id,
):
    pass
