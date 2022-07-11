from pydantic import BaseModel

class SearchYtResultsRequest(BaseModel):
    query: str
    
class GetYtResultsRequest(BaseModel):
    skip: int
    limit: int