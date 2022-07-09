from src.db.api_key_collection import get_api_keys


all_api_keys = []

for api_key_dcument in get_api_keys():
    print(api_key_dcument)
    # all_api_keys.append()
