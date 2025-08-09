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

        self.enum = LLMenumCohere
        self.client = cohere.ClientV2(api_key = self.api_key) # client version 2

        self.logger = logging.getLogger(__name__)


    def set_generation_model(self, model_name: str):
        self.logger.error("Cohere does not support generation models in this version")
        # Cohere does not support generation models in this version
        # This method is here to satisfy the LLMinterface contract
        # but it will not be used in this provider
        self.generation_model_id = model_name


    def set_embedings_model(self, model_name: str , embeding_size:int):
        self.embedding_model_id = model_name
        self.embedding_model_size = embeding_size


    def process_text(self, text:str):
        return [sentence.strip() for sentence in text.split('.') if sentence.strip()]

    
    def generate_text(self, prompt: str, max_output_tokens: int = None , chat_history : list =[] ,temprature : float = None):
        self.logger.error("Cohere does not support generation models in this version")
        # Cohere does not support generation models in this version
        # This method is here to satisfy the LLMinterface contract
        # but it will not be used in this provider
        return None


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

    def contrust_prompt(self, prompt: str, role: str):
        return {
            "role":role,
            "content" : self.process_text(prompt)
            }