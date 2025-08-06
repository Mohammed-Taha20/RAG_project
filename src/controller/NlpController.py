from .BaseController import BaseController
from models.schema import Project ,DataChunck
from typing import List
from ..stores.llm.LLMenum import LLMenumDocumentType

class NlpController(BaseController):
    
    def __init__(self ,vectordb_client , generation_client , embedding_client):
        super().__init__()
        self.vectordb_client=vectordb_client
        self.generation_client=generation_client
        self.embedding_client = embedding_client
        
    def create_collection_name(self,project_id:str):
        return f"collection_{project_id}".strip()
    
    def reset_vector_dp_collection(self,do_reset:int):
        return self.vectordb_client.delete_collection(self.create_collection_name(project_id=Project.project_id))
    
    def get_vector_dbcollection_info(self,project:Project):
        collection_name =self.create_collection_name(project_id=Project.project_id)
        return self.vectordb_client.get_collection_info(collection_name)
    
    def index_into_vector_db(self, project:Project , chunk:List[DataChunck],do_reset:int = 0):
        collection_name =self.create_collection_name(project_id=Project.project_id)
        
        texts = [c.chunck_text   for c in chunk]
        meta_data = [c.chunck_metadata for c in chunk]
        
        
        vectors  = [
            
            self.embedding_client.embed_text( text,document_type = LLMenumDocumentType.doc.value)
            for text in texts
        ]
        
        
        collection = self.vectordb_client.create_collection(collection_name=collection_name  , embedding_size =self.embedding_client.embedding_model_size , do_reset =do_reset)
        
        _ = self.vectordb_client.insert_many(collection_name =collection_name, text=texts , vector=vectors , metadata = meta_data)

        return True