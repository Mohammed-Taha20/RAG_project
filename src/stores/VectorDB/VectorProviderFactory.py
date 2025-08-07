from .provider import QDrantDB
from .VectorsEnums import VectorDBenum, DistanceMetricEnum
from controller.BaseController import BaseController

class VectorProviderFactory():
    def __init__(self,config:dict):
        self.config = config
        self.baseController = BaseController()

    def create(self,provider_name:str):
        if provider_name == VectorDBenum.VectorDB.value:
            db_path = self.baseController.get_db_path(db_name=self.config.vector_db_path)

            return QDrantDB(db_path=db_path, 
                            distance_method=self.config.vector_db_distance)
        else:
            raise ValueError(f"Unsupported vector database provider: {provider_name}")


