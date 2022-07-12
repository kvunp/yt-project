from elasticsearch import Elasticsearch, BadRequestError

from src.common import settings

config = settings.Settings()
es_client = Elasticsearch(config.ES_CONNECTION_STRING)

try:
    es_client.indices.create(index=config.ES_INDEX_VIDEOS)
except BadRequestError:
    pass