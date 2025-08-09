import json
from .BaseController import BaseController
from models.schema import Project ,DataChunck
from typing import List
from stores.llm.LLMenum import LLMenumDocumentType

class NlpController(BaseController):
    
    def __init__(self ,vectordb_client , generation_client , embedding_client, template_parser):
        super().__init__()
        self.vectordb_client=vectordb_client
        self.generation_client=generation_client
        self.embedding_client = embedding_client
        self.template_client = template_parser
        
        
    def create_collection_name(self,project_id:str):
        return f"collection_{project_id}".strip()
    
    def reset_vector_dp_collection(self,do_reset:int):
        return self.vectordb_client.delete_collection(self.create_collection_name(project_id=Project.project_id))
    
    def get_vector_dbcollection_info(self,project:Project):
        collection_name =self.create_collection_name(project_id=project.id)
        return json.loads(json.dumps(self.vectordb_client.get_collection_info(collection_name=collection_name) , default= lambda x:x.__dict__))
    
    def index_into_vector_db(self, project:Project , chunk:List[DataChunck],chunk_ids:list[int] , do_reset:int = 0):
        collection_name =self.create_collection_name(project_id=project.id)
        
        texts = [c.chunck_text   for c in chunk]
        meta_data = [c.chunck_metadata for c in chunk]
        
        
        vectors  = [
            
            self.embedding_client.embed_text( text,document_type = LLMenumDocumentType.doc.value)
            for text in texts
        ]
        
        
        print(f" Creating collection: {collection_name}")
        collection = self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_model_size,
            do_reset=do_reset
        )
        print(f" Collection created: {collection}")
        
        result = self.vectordb_client.insert_many(
            collection_name=collection_name,
            text=texts,
            vector=vectors,
            rec_id=chunk_ids,
            metadata=meta_data
        )
        print(f" Insert result: {result}")


        return True

    def search_by_vector(self, project:Project , text:str, limit:int = 10):
        collection_name =self.create_collection_name(project_id=project.id)

        vector = self.embedding_client.embed_text(text = text , document_type = LLMenumDocumentType.query.value)

        if not vector or len(vector)==0:
            self.logger.error("No vector generated for the query text.")
            return False
        search_result = self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=vector,
            limit=limit
        )

        if not search_result or len(search_result)==0:
            self.logger.error("No results found for the query.")
            return False
        return json.loads(json.dumps(search_result, default=lambda x: x.__dict__))  # Convert to JSON serializable format


    def answer_rag_questions(self,project:Project ,quary :str ,limit:int =5):
        answer,full_prompt,chat_history = None, None, None
        retrived_chunks = self.search_by_vector(project=project , text=quary , limit=limit)

        if not retrived_chunks or len(retrived_chunks)==0:
            self.logger.error("No retrived chunks found for the query.")
            return None, None, None


        system_prompt = self.template_client.get(group = "rag",key = "system_prompt")

        document_prompt = "/n".join([
            
            self.template_client.get(group = "rag", key = "doc_prompt",vars = {
                    "doc_num":id + 1,
                    "doc_content": chunk["payload"]["text"],
                })
            

            for id, chunk in enumerate(retrived_chunks)
        ])

        footer_prompt  = self.template_client.get(group = "rag", key = "footer_prompt")


        chat_history = self.generation_client.contrust_prompt(
            prompt = system_prompt,
            role = self.generation_client.enum.SYSTEM.value
            )

        full_prompt = "/n/n".join([document_prompt,footer_prompt])

        print(f"Chat history: {chat_history}")
        print (f"Full prompt: {full_prompt}")
        

        answer = self.generation_client.generate_text(
            prompt=full_prompt,
            chat_history=chat_history,
            max_output_tokens=self.generation_client.default_generation_max_output_token_size,
            temprature=self.generation_client.default_temperature
        )

        return answer,full_prompt,chat_history