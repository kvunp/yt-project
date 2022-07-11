from src.common.elastic_search import es_client
from src.common import settings

config = settings.Settings()

def bulk_insert_video_title_and_description_into_es(video_items):
    docs_to_be_inserted = []
    action = {"index":{"_index": config.ES_INDEX_VIDEOS}}
    for item in video_items:
        try:
            es_doc = {
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "mongo_id": item["id"]["videoId"]
            }
            docs_to_be_inserted.extend((action, es_doc))
        except Exception:
            # trusting yt api to give necessary details atleast for now
            # using docs which have all the required details
            pass
    es_client.bulk(index=config.ES_INDEX_VIDEOS, operations=docs_to_be_inserted)