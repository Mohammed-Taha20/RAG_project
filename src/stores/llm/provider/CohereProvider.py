from ..LLMinterface import LLMinterface
from ..LLMenum import LLMenumCohere , LLMenumDocumentType
import logging
import cohere

class CohereProvider(LLMinterface):
    def __init__(self , api_key:str ,
                 default_generation_max_output_token_size : int,
                 default_temperature:float,
                 default_input_max_chars : int):
        self.api_key = api_key
        self.default_generation_max_output_token_size = default_generation_max_output_token_size
        self.default_temperature = default_temperature
        self.default_input_max_chars = default_input_max_chars

        self.generation_model_id = None


        self.client = cohere.ClientV2(api_key = self.api_key) # client version 2

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_name: str): 
        self.generation_model_id = model_name


    def process_text(self, text:str):
        return text[:self.default_input_max_chars].strip()

    def generate_text(self, prompt: str, max_output_tokens: int = None , chat_history : list =[] ,temprature : float = None):
        if not self.client:
            self.logger.error("set the client")

        if not self.generation_model_id:
            self.logger.error("set the generation model")

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_token_size
        temprature = temprature if temprature else self.default_temperature

        chat_history.append(self.contrust_prompt(prompt=prompt , role = LLMenumCohere.User.value))

        response = self.client.chat(
            model = self.generation_model_id,
            message = chat_history,
            temperature = temprature,
            max_tokens = max_output_tokens
            )
        if not response or not response.message or not response.message.content  or len(response.message.content)==0:
            self.logger.error("empty response")

        return response.message.content[0].text

    

    def contrust_prompt(self, prompt: str, role: str):
        return {
            "role":role,
            "content" : self.process_text(prompt)
            }


    