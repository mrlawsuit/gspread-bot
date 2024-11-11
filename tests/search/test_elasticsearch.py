import sys
import os
module_path = os.path.abspath('/home/oleg/Рабочий стол/shering/shering')
if module_path not in sys.path:
    sys.path.append(module_path)

import pytest
from unittest.mock import AsyncMock, patch

from app.search.elasticsearch import create_document_elastic
from app.models import User


class MockModel(User):
    def to_dict(self):
        return {
            'key1': 'value1',
            'key2': 'value2'
        }


@pytest.mark.asyncio
async def test_create_document_elastic_success():
    index_name = 'test_index'
    model_instance = MockModel()
    with patch(
        'app.search.elasticsearch.elastic_client.index',
        new_callable=AsyncMock
    ) as mock_index:
        mock_index.return_value = {'_id': 'test_elastic_index'}

        response = await create_document_elastic(index=index_name, model=model_instance)

        # Проверка, что метод index был вызван с ожидаемыми аргументами
        mock_index.assert_called_once_with(index=index_name, body=model_instance.to_dict())

        # Проверка ожидаемого результата
        assert response == 'Document was add into elastic id is test_elastic_index'
