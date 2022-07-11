from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every
from googleapiclient.discovery import build
from json import loads, dumps, load


from src.common import settings
from src.common.mongo_db import video_collection
from src.db.video_collection import insert_many_into_video_collection
from src.common.api_keys import apiKeyStore
from src.common.elastic_search import es_client
from src.youtube.youtube_api import get_latest_youtube_results
from src.es.video_es import bulk_insert_video_title_and_description_into_es
from src.models import api_models

config = settings.Settings()
app = FastAPI()

api_key = "AIzaSyDuj7STMh7y4WoDWrrnyU7vLifSNGvpXU4"

# youtube = build("youtube", "v3", developerKey=api_key)


@app.on_event("startup")
@repeat_every(seconds=config.SEARCH_RESULTS_REFRESH_INTERVAL_IN_SECONDS)
def startup_method():
    yt_response = None
    with open("src/common/static_json/db.json") as file:
        yt_response = load(file)
    while not yt_response:
        # response = get_latest_youtube_results(api_key)
        break
    video_items = yt_response.get("items", {})

    try:
        insert_many_into_video_collection(video_items)
    except Exception as e:
        print(e)

    try:
        bulk_insert_video_title_and_description_into_es(video_items)
    except Exception as e:
        print(e)


@app.get("/get_yt_results")
def get_yt_results(request: api_models.GetYtResultsRequest):
    try:
        skip_query = {"$skip": request.skip}
        limit_query = {"$limit": request.limit}
        query_sequence = [skip_query, limit_query]
        return JSONResponse(
            status_code=200,
            content=[doc for doc in video_collection.aggregate(query_sequence)]
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content="Server Error"
        )


@app.get("/search_yt_results")
def search_yt_results(request: api_models.SearchYtResultsRequest):
    try:
        query = {
            # "bool":{},
            "multi_match":{
                    "query":request.query,
                    "fields": ["title"]
                }
            }
        mongo_ids = set()
        for doc in es_client.search(index=config.ES_INDEX_VIDEOS, query=query)["hits"]["hits"]:
            mongo_id = doc.get("_source", {}).get("mongo_id", None)
            if mongo_id:
                mongo_ids.add(mongo_id)
        return JSONResponse(
            status_code=200,
            content=[doc for doc in video_collection.find(
                {
                    '_id': {
                        '$in': list(mongo_ids)
                    }
                }
            )]
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content="Server Error"
        )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
