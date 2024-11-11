from elasticsearch import AsyncElasticsearch

from ..main import app
from .. import models
from . import mapping
from ..repositories import user_repository


elastic_client = AsyncElasticsearch(['http://elastic:9200'])

app.state.elastic_client = elastic_client


async def elastic_init(index, body):
    if not elastic_client.exists(index):
        elastic_client.create(index=index, body=body)


async def create_user_elastic(user: models.User):
    doc = user.to_dict()
    result = await elastic_client.index(index='users', body=doc)
    return f'Document was add into elastic id is {result['_id']}'



# async def create_user_elastic():
#     await elastic_client.indices.create(
#           index=mapping.user_index,
#           mappings=mapping.user_mapping
#     )
# elastic_client.indices.


# async def update_user_elastic():
#     await elastic_client.indices.