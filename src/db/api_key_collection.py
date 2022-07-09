from src.common.mongo_db import api_key_collection

def get_api_keys():
    api_keys = api_key_collection.find({})
    print(api_keys)
    return api_keys