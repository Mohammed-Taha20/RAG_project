from .provider import QDrantDB
from .VectorsEnums import VectorDBenum, DistanceMetricEnum
from controller.BaseController import BaseController

class VectorProviderFactory():
    def __init__(self,config:dict):
        self.config = config
        self.baseController = BaseController()

    def create(self,provider_name:str):
        if provider_name == VectorDBenum.VectorDB.value:

            return QDrantDB(QDrantDB_api = self.config.qdrant_api_key,
                            QDrantDB_url = self.config.qdrant_api_url,
                            distance_method=self.config.vector_db_distance)
        else:
            raise ValueError(f"Unsupported vector database provider: {provider_name}")


