from datetime import datetime
from pydantic import BaseModel

class File(BaseModel):
    path: str
    name: str
    created: datetime
    modified: datetime

class Context(BaseModel):
    query: str

class SearchRequest(BaseModel):
    query: str
    directory: str = "~/Documents"  # Default directory