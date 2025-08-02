from re import S
from ..LLMinterface import LLMinterface
from groq import Groq
class GrokProvider(LLMinterface):
    def __init__(self , api_key:str , api_url:str,
                 default_generation_max_output_token_size : int,
                 default_temperature:float,
                 default_input_max_chars : int):
        self.api_key = api_key
        self.api_url = api_url
        self.default_generation_max_output_token_size = default_generation_max_output_token_size
        self.default_temperature = default_temperature
        self.default_input_max_chars = default_input_max_chars

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_model_size = None

        self.client = Groq(api_key = self.api_key,api_url = self.api_url) #https://console.groq.com/docs/text-chat




