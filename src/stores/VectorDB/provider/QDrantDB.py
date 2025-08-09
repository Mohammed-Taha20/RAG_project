from operator import truediv
from qdrant_client import models, QdrantClient
from ..VectorDBInterface  import VectorDBInterface
from ..VectorsEnums import VectorDBenum, DistanceMetricEnum
import logging

class QDrantDB(VectorDBInterface):

    def __init__(self,QDrantDB_api : str, QDrantDB_url : str , distance_method:str):

        self.client =None
        self .QDrantDB_api = QDrantDB_api
        self .QDrantDB_url = QDrantDB_url
        self .distance_method = None

        if distance_method is  DistanceMetricEnum.COSINE.value: # may be the is should be == 
            self.distance_method = DistanceMetricEnum.COSINE.value
        else:
            self.distance_method = DistanceMetricEnum.EUCLIDEAN.value

        self.logger = logging.getLogger(__name__)


    def connect(self) -> None:
        self.client = QdrantClient(url = self.QDrantDB_url,api_key=self.QDrantDB_api)

    def disconnect(self) -> None:
        self.client =  None

    def is_collection_exist(self, collection_name: str) -> bool:
        try:
            return self.client.collection_exists(collection_name=collection_name)
        except Exception as e:
            self.logger.error(f"Error checking collection existence: {e}")
            return False
    
    def list_all_collections(self)  -> list:
        try:
            return self.client.get_collections()
        except Exception as e:
            self.logger.error(f"Error listing collections: {e}")
            return []

    def get_collection_info(self,collection_name:str) -> dict:
        try:
            return self.client.get_collection(collection_name=collection_name)
        except Exception as e:
            self.logger.error(f"Error getting collection info: {e}")
            return {}
    def delete_collection(self, collection_name: str) -> None:
        if self.is_collection_exist(collection_name):
            try:
                self.client.delete_collection(collection_name=collection_name)
            except Exception as e:
                self.logger.error(f"Error deleting collection {collection_name}: {e}")

    def create_collection(self, collection_name: str, embedding_size: int, do_reset: int) -> bool:
        if self.is_collection_exist(collection_name):
            if do_reset:
                self.logger.info(f"Collection {collection_name} exists. Resetting it.")
                self.delete_collection(collection_name)
            else:
                self.logger.warning(f"Collection {collection_name} already exists. Use do_reset=True to recreate it.")
                return False  
    
        try:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=embedding_size, distance=self.distance_method)
            )
            self.logger.info(f"Collection created: {collection_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating collection {collection_name}: {e}")
            return False
    



    def insert_one(self,collection_name :str, text:str,vector:list,metadata:dict , rec_id:str = None):
        if not self.is_collection_exist(collection_name=collection_name):
            self.logger.error(f"Collection {collection_name} does not exist.")
            return False
        try:
            _ = self.client.upload_collection(
                collection_name = collection_name,
                records = [
                    models.Record(
                        id = rec_id,  # Optional, can be None
                    vector = vector,
                    payload = {"text": text, "metadata": metadata},

                    )  
                        ])
            return True
        except Exception as e:
            self.logger.error(f"Error inserting document into collection {collection_name}: {e}")
            return False


    def insert_many(self,collection_name :str, text:list,vector:list,metadata:list , rec_id:list ,batch_size:int = 50):
        if not self.is_collection_exist(collection_name=collection_name):
            self.logger.error(f"Collection {collection_name} does not exist.")
            return False
        
        if metadata is None:
            metadata = [None]*len(text)
        if rec_id is None:
            rec_id = list(range(len(text)))  # Generate default IDs if rec_id is None

        for i in range (0,len(text),batch_size):
            batch_text = text[i:i+batch_size]
            batch_vector = vector[i:i+batch_size]
            batch_metadata = metadata[i:i+batch_size]
            batch_rec_id = rec_id[i:i+batch_size]


            batch_records = [
                models.Record(
                    id = rec_id_item,  
                    vector = vector_item,
                    payload = {"text": text_item, "metadata": metadata_item},
                )
                for rec_id_item, text_item, vector_item, metadata_item in zip(batch_rec_id, batch_text, batch_vector, batch_metadata)
]
            try:
                _ = self.client.upload_collection(
                    collection_name = collection_name,
                    vectors = [r.vector for r in batch_records],
                    payload = [r.payload for r in batch_records],
                    ids = [r.id for r in batch_records],
                )

                

        

            except Exception as e:
                self.logger.error(f"Error inserting document into collection {collection_name}: {e}")
                return False
        return True

    def search_by_vector(self, collection_name:str,vector:list, limit:int) -> list:

        return self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit
            )