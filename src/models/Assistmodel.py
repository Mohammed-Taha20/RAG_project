from models.schema.assist import ObjectId
from .MyBaseModel import MyBaseModel
from .schema import Assist
from .enums.db_enum import DBEnum

class AssistModel(MyBaseModel):
    def __init__(self,dp_client):
        super().__init__(dp_client)
        self.collection = self.dp_client[DBEnum.CollectionAssistName.value]

    @classmethod
    async def create_instance(cls, dp_client):
        instance = cls(dp_client=dp_client)
        await instance.init_collections()
        return instance

    async def init_collections(self):
        all_collections = await self.dp_client.list_collection_names()
        if DBEnum.CollectionAssistName.value not in all_collections:
            self.collection = await self.dp_client.create_collection(DBEnum.CollectionAssistName.value)
        else:
            self.collection = self.dp_client[DBEnum.CollectionAssistName.value]
        
        indexes = Assist.get_indexes()
        for index in indexes:
            try:
                await self.collection.create_index(index["key"], unique=index["unique"], name=index["name"])
            except Exception as e:
                print(f"Index creation skipped or failed: {e}")

    async def create_assist(self,assist:Assist):
        result =  await self.collection.insert_one(assist.dict(by_alias = True , exclude_unset = True)) 
        assist.id = result.inserted_id
        return  assist


    async def get_all_project_assists(self, assist_project_id: str):
        return await self.collection.find({"assist_project_id": ObjectId(assist_project_id)}).to_list(length=None)
        