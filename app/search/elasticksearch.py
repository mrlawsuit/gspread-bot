from elasticsearch import AsyncElasticsearch

from ..main import app
from .. import models
from . import mapping


elastic_client = AsyncElasticsearch(['http://elastic:9200'])

app.state.elastic_client = elastic_client


async def elastic_init(index, body):
    if not elastic_client.exists(index):
        elastic_client.create(index=index, body=body)


async def create_document_elastic(index: str, model: models.Base):
    doc = model.to_dict()
    result = await elastic_client.index(index=index, body=doc)
    return f'Document was add into elastic id is {result['_id']}'


def search_query_by_id(id):
    return {
        'query': {'match': {'id': id}}
    }


def get_document(id, index):
    body = search_query_by_id(id)
    result = elastic_client.search(
        index=index,
        body=body
    )
    if not result:
        raise ValueError('There is no documents with such index')
    return result['hits']['hits'][0]['_id']


async def update_document_elastic(
        index: str,
        update_body: dict,
        id: int
):
    result = elastic_client.update(index=index, id=id, body=update_body)
    return result['result']
