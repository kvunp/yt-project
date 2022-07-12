from json import load
from typing import List
from pydantic import BaseModel

from src.db.api_key_collection import get_api_keys_from_db

class ApiKey(BaseModel):
    key: str 

# class ApiKeyList(BaseModel):
#     __root__: List[ApiKey]

class ApiKeyStore(BaseModel):
    api_keys_list: List[ApiKey] = []
    api_key_in_use_index: int = 0

    def __init__(self):
        api_keys_from_db = get_api_keys_from_db()
        if api_keys_from_db:
            print("db")
            # self.api_keys_list = (parse_obj_as(List[ApiKey], api_keys_from_db))
            # for item in api_keys_from_db:
            #     **item
        else:
            print("file")
            # self.api_keys_list = ApiKeyList.parse_file("src/common/static_json/api_key.json")
            # with open("src/common/static_json/api_key.json") as file:
            # self.api_keys_list = (parse_file_as(List[ApiKey], "src/common/static_json/api_key.json"))



    def get_api_key(self):
        if not self.api_keys_list:
            return None
        return self.api_keys_list[self.api_key_in_use_index]
        
    def inc_and_get_api_key_in_use_index(self):
        if not self.api_keys_list:
            return None
        self.api_key_in_use_index = (self.api_key_in_use_index + 1) % len(self.api_keys_list)
        #TODO: proper ApiKey
        return self.api_keys_list[self.api_key_in_use_index].get("key", None)
#TODO: api key store construct form api key collection
# apiKeyStore = ApiKeyStore()

api_keys_from_db = get_api_keys_from_db()
if api_keys_from_db:
    api_keys_list = api_keys_from_db
else:
    with open("src/common/static_json/api_key.json") as file:
        api_keys_list = load(file)