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

    @classmethod
    async def create_instance(cls,dp_client):
        instance = cls(dp_client = dp_client)
        await instance.init_collections()
        return instance

    async def init_collections(self):
        all_collections = await self.dp_client.list_collection_names()

        if DBEnum.CollectionChunckName.value not in all_collections:
            self.collection = await self.dp_client.create_collection(DBEnum.CollectionChunckName.value)
        else:
            self.collection = self.dp_client[DBEnum.CollectionChunckName.value]

        # Always try to create indexes
        indexes = DataChunck.get_indexes()
        for index in indexes:
            try:
                await self.collection.create_index(index["key"], unique=index["unique"], name=index["name"])
            except Exception as e:
                print(f"Index creation skipped or failed: {e}")
    
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

    async def delete_chunks_by_project_id(self, project_id: str):
        result = await self.collection.delete_many({"chunck_project_id": ObjectId(project_id) if isinstance(project_id, str) else project_id})
        return result.deleted_count

    async def reset(self):
        result  = await self.collection.delete_many({})
        return result.deleted_count
    
    async def get_all_project_chunks(self,project_id : str , page_no=1 , page_size=50):
        records =  self.collection.find({"chunck_project_id": ObjectId(project_id)}).skip((page_no-1)*page_size).limit(page_size)
        return [
            DataChunck(**rec)
            for rec in records
        ]




