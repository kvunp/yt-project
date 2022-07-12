from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every
from googleapiclient.errors import HttpError


from src.common import settings
from src.common.mongo_db import video_collection
from src.db.video_collection import insert_many_into_video_collection
from src.common.elastic_search import es_client
from src.youtube.youtube_api import get_latest_youtube_results
from src.es.video_es import bulk_insert_video_title_and_description_into_es
from src.models import api_models

config = settings.Settings()
app = FastAPI()

#TODO: api keys list pydantic error in common/api_keys
# api_keys_list = ["AIzaSyDuj7STMh7y4WoDWrrnyU7vLifSNGvpXU4"]
from src.common.api_keys import api_keys_list
api_key_curr = 0

@app.on_event("startup")
@repeat_every(seconds=config.SEARCH_RESULTS_REFRESH_INTERVAL_IN_SECONDS)
def startup_method():
    global api_key_curr
    yt_response = None
    retries_with_api_keys = len(api_keys_list)
    # with open("src/common/static_json/db.json") as file:
    #     yt_response = load(file)
    while (not yt_response) and retries_with_api_keys:
        try:
            response = get_latest_youtube_results(api_keys_list[api_key_curr]["key"])
        except HttpError:
            api_key_curr = (api_key_curr + 1) % len(api_keys_list)
            retries_with_api_keys -= 1
            continue
        except Exception as e:
            print(e)
            return
        yt_response = response
    if not yt_response:
        print("Fetching results from youtube failed. All api keys might have been expired")
        return
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
            content=list(video_collection.aggregate(query_sequence))
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
            "bool":{
                "should": [
                    {
                        "match": {
                            "title": request.query
                        }
                    },
                    {
                        "match": {
                            "description": request.query
                        }
                    }
                ]
            }
            }
        mongo_ids = set()
        for doc in es_client.search(index=config.ES_INDEX_VIDEOS, query=query)["hits"]["hits"]:
            mongo_id = doc.get("_source", {}).get("mongo_id", None)
            if mongo_id:
                mongo_ids.add(mongo_id)
        return JSONResponse(
            status_code=200,
            content=list(video_collection.find(
                {
                    '_id': {
                        '$in': list(mongo_ids)
                    }
                }
            ))
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
