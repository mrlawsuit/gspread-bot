import sys
import os
module_path = os.path.abspath('/home/oleg/Рабочий стол/shering/shering')
if module_path not in sys.path:
    sys.path.append(module_path)

import pytest
from unittest.mock import AsyncMock, patch

from app.search.elasticsearch import (
    create_document_elastic,
    search_query_by_id,
    get_document_id,
    update_document_elastic,
    delete_document_elastic,
    elastic_init
)
from app.models import User

from elasticsearch.exceptions import NotFoundError

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

        response = await create_document_elastic(
            index=index_name,
            model=model_instance
        )

        # Проверка, что метод index был вызван с ожидаемыми аргументами
        mock_index.assert_called_once_with(
            index=index_name,
            body=model_instance.to_dict()
        )

        # Проверка ожидаемого результата
        assert response == 'Document was add into elastic id is test_elastic_index'


@pytest.mark.asyncio
async def test_create_document_elastic_error():
    index_name = 'test_index'
    model_instance = MockModel()

    with patch(
        'app.search.elasticsearch.elastic_client.index',
        new_callable=AsyncMock
    ) as mock_index:
        mock_index.side_effect = Exception('Elasticsearch index error')
        with pytest.raises(Exception) as ex_info:
            await create_document_elastic(
                index=index_name,
                model=model_instance
            )

    assert str(ex_info.value) == 'Elasticsearch index error'


@pytest.mark.asyncio
async def test_get_document_id_success():
    mock_index = 'test_index'
    mock_id = 1
    mock_result = {
        'hits': {
            'hits': [
                {'_id': 'abc123'}
            ]
        }
    }
    with patch('app.search.elasticsearch.elastic_client.search', new_callable=AsyncMock) as mock_search:
        mock_search.return_value = mock_result
        response = await get_document_id(
            id=mock_id,
            index=mock_index
        )
        assert response == 'abc123'
        mock_search.assert_awaited_once_with(index=mock_index, body=search_query_by_id(mock_id))


@pytest.mark.asyncio
async def test_get_document_id_error():
    mock_index = 'test_index'
    mock_id = 1
    mock_result = {
        'hits': {
            'hits': []
        }
    }
    with patch('app.search.elasticsearch.elastic_client.search', new_callable=AsyncMock) as mock_search:
        mock_search.return_value = mock_result

        with pytest.raises(ValueError, match='No documents found with this id'):
            await get_document_id(id=mock_id, index=mock_index)
        mock_search.assert_awaited_once_with(index=mock_index, body=search_query_by_id(mock_id))


@pytest.mark.asyncio
async def test_update_document_elastic():
    pass


@pytest.mark.asyncio
async def test_delete_document_elastic():
    pass


@pytest.mark.asyncio
async def test_elastic_init():
    pass


@pytest.mark.asyncio
async def test_search_query_by_id():
    pass
