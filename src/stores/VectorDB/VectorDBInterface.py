from abc import ABC ,abstractmethod

class VectorDBInterface(ABC):

    @abstractmethod
    def connect(self) -> None:
        pass
    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def is_collection_exist(self, collection_name: str) -> bool:
        """Check if a collection exists in the database."""
        pass

    @abstractmethod
    def list_all_collections(self)  -> list:
        """List all collections in the database."""
        pass

    @abstractmethod
    def get_collection_info(self,collection_name:str) -> dict:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str) -> None:
        """Delete a collection from the database."""
        pass

    @abstractmethod
    def create_collection(self, collection_name: str , embedding_size :int , do_reset : bool) -> None:
        """Create a new collection in the database."""
        pass

    @abstractmethod
    def insert_one(self,collection_name :str, text:str,vector:list,metadata:dict , rec_id:str = None):
        """Insert a single document into the specified collection."""
        pass

    @abstractmethod
    def insert_many(self,collection_name :str, text:list,vector:list,metadata:list , rec_id:list ,batch_size:int = 50):
        """Insert a single document into the specified collection."""
        pass


    @abstractmethod
    def search_by_vector(self, collection_name:str,vector:list, limit:int) -> list:
        """Search for documents in the specified collection by vector."""
        pass
    