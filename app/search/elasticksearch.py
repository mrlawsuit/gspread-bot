from elasticsearch import AsyncElasticsearch

from .. import models
from . import mapping


elastic_client = AsyncElasticsearch(['http://elastic:9200'])


# async def elastic_init(index, mapping):
#     if not elastic_client.exists(index):
#         elastic_client.create(index=index, body=mapping)


# async def create_user_elastic():
#     await elastic_client.indices.create(
#           index=mapping.user_index,
#           mappings=mapping.user_mapping
#     )
# elastic_client.indices.

# async def update_user_elastic():
#     await elastic_client.indices.