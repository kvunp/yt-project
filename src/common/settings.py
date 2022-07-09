from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGO_CONNECTION_STRING: str
    SEARCH_RESULTS_REFRESH_INTERVAL_IN_SECONDS: int