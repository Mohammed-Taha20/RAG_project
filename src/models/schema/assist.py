from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime

class Assist(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    assist_project_id : ObjectId
    assist_type : str = Field(..., min_length=1)
    assist_name: str = Field(..., min_length=1)
    assist_size: int = Field(ge=0,default=None)
    assist_config: dict = Field(default=None)
    assist_pushed_at:datetime = Field(default=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [("assist_project_id", 1)],
                "unique": False,
                "name": "assist_project_id_index"
            },
            {
                "key": [("assist_project_id", 1) , ("assist_name", 1)],
                "unique": True,
                "name": "assist_project_id_name_index"
            },
        ]
