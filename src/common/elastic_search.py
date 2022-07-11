from elasticsearch import Elasticsearch, BadRequestError

from src.common import settings

config = settings.Settings()

es_client = Elasticsearch("http://localhost:9200")

try:
    es_client.indices.create(index=config.ES_INDEX_VIDEOS)
except BadRequestError:
    pass