from ..LLMinterface import LLMinterface
from ..LLMenum import LLMenumCohere , LLMenumDocumentType
import logging
import cohere

class EmbeddingProvider(LLMinterface):
    def __init__(self , api_key:str ,
                 default_generation_max_output_token_size : int,
                 default_temperature:float,
                 default_input_max_chars : int):
        self.api_key = api_key
        self.default_generation_max_output_token_size = default_generation_max_output_token_size
        self.default_temperature = default_temperature
        self.default_input_max_chars = default_input_max_chars

        self.embedding_model_id = None
        self.embedding_model_size = None

        self.client = cohere.ClientV2(api_key = self.api_key) # client version 2

        self.logger = logging.getLogger(__name__)





    def set_embedings_model(self, model_name: str , embeding_size:int):
        self.embedding_model_id = model_name
        self.embedding_model_size = embeding_size


    def process_text(self, text:str):
        return text[:self.default_input_max_chars].strip()


    def embed_text(self, text: str,document_type:str):

        if not self.client:
            self.logger.error("set the client")

        if not self.embedding_model_id:
            self.logger.error("set the generation model")


        input_type = LLMenumCohere.search_doc.value
        if document_type == LLMenumDocumentType.query.value:
            input_type  = LLMenumCohere.search_query.value

        response = self.client.embed(model= self.embedding_model_id ,texts=self.process_text(text),input_type=input_type ,embedding_types=["float"] )

        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("empty embedding")

        return response.embeddings.float[0]