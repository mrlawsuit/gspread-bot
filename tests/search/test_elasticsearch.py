import sys
import os
module_path = os.path.abspath('/home/oleg/Рабочий стол/shering/shering')
if module_path not in sys.path:
    sys.path.append(module_path)

import pytest
from unittest.mock import AsyncMock, patch

from app.search.es_client import (
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
        'app.search.es_client.elastic_client.index',
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
        'app.search.es_client.elastic_client.index',
        new_callable=AsyncMock
    ) as mock_index:
        mock_index.side_effect = Exception('es_client index error')
        with pytest.raises(Exception) as ex_info:
            await create_document_elastic(
                index=index_name,
                model=model_instance
            )

    assert str(ex_info.value) == 'es_client index error'


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
    with patch(
        'app.search.es_client.elastic_client.search',
        new_callable=AsyncMock
    ) as mock_search:
        mock_search.return_value = mock_result
        response = await get_document_id(
            id=mock_id,
            index=mock_index
        )
        assert response == 'abc123'
        mock_search.assert_awaited_once_with(
            index=mock_index,
            body=search_query_by_id(mock_id)
        )


@pytest.mark.asyncio
async def test_get_document_id_error():
    mock_index = 'test_index'
    mock_id = 1
    mock_result = {
        'hits': {
            'hits': []
        }
    }
    with patch(
        'app.search.es_client.elastic_client.search',
        new_callable=AsyncMock
    ) as mock_search:
        mock_search.return_value = mock_result

        with pytest.raises(ValueError, match='No documents found with this id'):
            await get_document_id(id=mock_id, index=mock_index)
        mock_search.assert_awaited_once_with(
            index=mock_index,
            body=search_query_by_id(mock_id)
        )


@pytest.mark.asyncio
async def test_update_document_elastic():
    '''Проверяет успешное выполнение функции update_document_elastic'''
    with patch(
        'app.search.es_client.elastic_client.update',
        new_callable=AsyncMock
    ) as mock_update, \
        patch(
            'app.search.es_client.get_document_id',
            new_callable=AsyncMock
        ) as mock_get_document_id:
        # Настройка возвращаемых значений для моков
        mock_get_document_id.return_value = 'mock_elastic_id'
        mock_update.return_value = {'result': 'updated'}
        # Входные данные для теста
        index = 'test_index'
        update_body = {'field': 'value'}
        id = 123
        # Вызов тестируемой функции
        response = await update_document_elastic(index, update_body, id)
        # Проверка результатов
        assert response == 'updated'
        # Проверка, что get_document_id был вызван с правильными аргументами
        mock_get_document_id.assert_awaited_once_with(id=id, index=index)
        # Проверка, что elastic_client.update был вызван с правильными аргументами
        mock_update.assert_awaited_once_with(
            index=index,
            id='mock_elastic_id',
            body=update_body
        )


@pytest.mark.asyncio
async def test_delete_document_elastic():
    '''Проверяет успешное выполнение функции delete_document_elastic'''
    with patch(
        'app.search.es_client.get_document_id',
        new_callable=AsyncMock
    ) as mock_get_document_id, \
        patch(
            'app.search.es_client.elastic_client.delete',
            new_callable=AsyncMock
        ) as mock_delete:
        mock_get_document_id.return_value = 'mock_elastic_id'
        mock_delete.return_value = {'result': 'deleted'}
        index = 'test_index'
        id = 123

        response = await delete_document_elastic(index=index, id=id)

        assert response == 'deleted'

        mock_get_document_id.assert_awaited_once_with(id=id, index=index)
        mock_delete.assert_awaited_once_with(index=index, id='mock_elastic_id')


@pytest.mark.asyncio
async def test_elastic_init():
    with patch(
        'app.search.es_client.elastic_client.indices.exists',
        new_callable=AsyncMock
    )  as mock_exists, \
    patch(
        'app.search.es_client.elastic_client.indices.create',
        new_callable=AsyncMock
    ) as mock_create:
        mock_exists.return_value = None
        index = 'test_index'
        mapping = {
            'properties': {
                'id': {'type': 'integer'}
            }
        }
        response = await elastic_init(index=index, mappings=mapping)

        assert response == None

        mock_create.assert_awaited_once_with(index=index, mappings=mapping)
        mock_exists.assert_awaited_once_with(index=index)


@pytest.mark.asyncio
async def test_search_query_by_id():
    pass
