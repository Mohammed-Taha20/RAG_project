from .MyBaseModel import MyBaseModel
from .schema import Project
from .enums.db_enum import DBEnum
from models.schema import DataChunck
from bson.objectid import ObjectId
from pymongo import InsertOne

class ChunkModel(MyBaseModel):
    def __init__(self, dp_client):
        super().__init__(dp_client)
        self.collection = self.dp_client[DBEnum.CollectionChunckName.value]
    
    async def create_chunk(self, chunk_data : DataChunck):
        result = await self.collection.insert_one(chunk_data.dict(by_alias=True , exclude_unset= True))
        return result.inserted_id
    
    async def get_chunk_by_id(self, chunk_id: str):
        chunk_data = await self.collection.find_one({"_id": ObjectId(chunk_id)})
        if chunk_data:
            return DataChunck(**chunk_data)
        return None

    async def insert_many_chunks(self,chunk:list,batch_size :int = 100 ):
        for i in range(0, len(chunk), batch_size):
            batch = chunk[i:i + batch_size]
            requests = [InsertOne(data.dict(by_alias=True , exclude_unset= True)) for data in batch]
            if requests:
                await self.collection.bulk_write(requests)

        return len(chunk)

    async def delete_chunks_by_project_id(self, project_id: ObjectId):
        result = await self.collection.delete_many({"chunck_project_id": project_id})
        return result.deleted_count





