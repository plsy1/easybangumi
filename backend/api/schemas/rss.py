from pydantic import BaseModel
from typing import Optional
from enum import Enum
from core.rss import RSS_Type

class Model_RSS_Add(BaseModel):
    type: RSS_Type
    url: str
    
class Model_RSS_Delete(BaseModel):
    type: RSS_Type
    id: str
    
class Model_RSS_Collect(BaseModel):
    url: str
    