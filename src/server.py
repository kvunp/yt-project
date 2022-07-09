from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every
from googleapiclient.discovery import build
from json import loads, dumps, load


from src.common import settings
from src.common.mongo_db import video_collection
from src.db.video_collection import insert_many_into_video_collection
from src.common.api_keys import all_api_keys

config = settings.Settings()
app = FastAPI()

api_key = "AIzaSyDuj7STMh7y4WoDWrrnyU7vLifSNGvpXU4"

youtube = build("youtube", "v3", developerKey=api_key)

@app.on_event("startup")
def startup_method():
    api_key = all_api_keys
    # with open("src/common/static_json/db.json") as file:
    #     yt_response = load(file)
    #     try:
    #         insert_many_into_video_collection(yt_response.get("items", {}))
    #     except Exception as e:
    #         print(e)


print(config)
@app.get("/")
# @app.on_event("startup")
# @repeat_every(seconds=config.SEARCH_RESULTS_REFRESH_INTERVAL_IN_SECONDS)
def fun():
    request = youtube.search().list(
        part = 'snippet',
        q = 'How to make tea?',
        type = 'video',
        maxResults = 50
    )
    response = request.execute()
    return JSONResponse(
        status_code=200,
        content=response
    )
    # return "done"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
