from src.common.mongo_db import api_key_collection

def get_api_keys_from_db():
    api_keys = api_key_collection.find()
    if api_keys:
        return list(api_keys)
    return None