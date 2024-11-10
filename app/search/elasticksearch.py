from elasticsearch import AsyncElasticsearch


elastic_client = AsyncElasticsearch


async def elastic_init(index, mapping):
    if not elastic_client.exists(index):
        elastic_client.create(index=index, body=mapping)
