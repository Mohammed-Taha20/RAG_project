from pydantic import BaseModel, Field
from typing import Optional, List
from bson.objectid import ObjectId

class DataChunck(BaseModel):
    id: Optional[ObjectId] = Field(default=None , alias = "_id")
    chunck_order: int = Field(..., ft= 0)
    chunck_project_id: ObjectId
    chunck_text: str = Field(..., min_length=1)
    chunck_metadata: dict

    class Config:
        arbitrary_types_allowed = True