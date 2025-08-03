from ..LLMinterface import LLMinterface
from ..LLMenum import LLMenum
from groq import Groq
import logging

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

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_name: str): 
        self.generation_model_id = model_name

    def set_embedings_model(self, model_name: str , embeding_size:int):
        self.embedding_model_id = model_name
        self.embedding_model_size = embeding_size

    def generate_text(self, prompt: str, max_output_tokens: int = None , chat_history : list =[] ,temprature : float = None):
        if not self.client:
            self.logger.error("set the client")

        if not self.generation_model_id:
            self.logger.error("set the generation model")

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_token_size
        temprature = temprature if temprature else self.default_temperature

        chat_history.append(self.contrust_prompt(prompt=prompt , role = LLMenum.User.value))

        response = self.client.chat.completions(
            model = self.generation_model_id,
            message=chat_history,
            temprature = temprature,
            max_output_tokens = max_output_tokens
            )
        if not response or not response.choices or len(response.choices)==0:
            self.logger.error("empty response")

        return response.choices[0].message.content


    def embed_text(self, text: str,document_type:str):

        if not self.client:
            self.logger.error("set the client")

        if not self.generation_model_id:
            self.logger.error("set the generation model")


        response = self.client.chat.completions(
            model = self.embedding_model_id,
            message=text,
            )
        if not response or not response.choices or len(response.choices)==0:
            self.logger.error("empty response")

        return response.choices[0].data

    

    def contrust_prompt(self, prompt: str, role: str):
        return {
            "role":role,
            "content" : prompt
            }
    




