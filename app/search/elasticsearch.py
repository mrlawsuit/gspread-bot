from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError

from ..main import app
from .. import models
from . import mapping


elastic_client = AsyncElasticsearch(['http://elastic:9200'])

app.state.elastic_client = elastic_client


async def elastic_init(index, body):
    if not await elastic_client.exists(index):
       await elastic_client.create(index=index, body=body)


async def create_document_elastic(index: str, model: models.Base):
    doc = model.to_dict()
    result = await elastic_client.index(index=index, body=doc)
    return f'Document was add into elastic id is {result['_id']}'


def search_query_by_id(id):
    return {
        'query': {'match': {'id': id}}
    }


async def get_document_id(id, index):
    body = search_query_by_id(id)
    try:
        result = await elastic_client.search(
            index=index,
            body=body
        )
    except NotFoundError:
        raise ValueError('There is no documents with such index')
    if not result['hits']['hits']:
        raise ValueError('No documents found with this id')
    return result['hits']['hits'][0]['_id']


async def update_document_elastic(
        index: str,
        update_body: dict,
        id: int
):
    elastic_id = await get_document_id(id=id, index=index)
    result = await elastic_client.update(index=index, id=elastic_id, body=update_body)
    return result['result']


async def delete_document_elastic(
        index: str,
        id: int
):
    elastic_id = await get_document_id(id=id, index=index)
    result = await elastic_client.delete(index=index, id=elastic_id)
    return result['result']
    

    
