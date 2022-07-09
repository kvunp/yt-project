from pymongo import MongoClient
from pymongo.errors import ConfigurationError
from src.common import settings

config = settings.Settings()

myclient = MongoClient(config.MONGO_CONNECTION_STRING)
try:
    mydb = myclient.get_default_database()
except ConfigurationError:
    mydb = myclient["yt_service"]

video_collection = mydb["videos"]
api_key_collection = mydb["api_keys"]