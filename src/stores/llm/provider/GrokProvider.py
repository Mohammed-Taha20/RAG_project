from ..LLMinterface import LLMinterface
from ..LLMenum import LLMenumGroq
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
        self.enum = LLMenumGroq
        self.generation_model_id = None


        self.client = Groq(api_key = self.api_key ,base_url = api_url ) #https://console.groq.com/docs/text-chat

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_name: str): 
        self.generation_model_id = model_name

    def set_embedings_model(self, model_name: str , embeding_size:int):
        self.logger.error("Groq does not support embedding models in this version")

    def embed_text(self, text: str,document_type:str):
        self.logger.error("Groq does not support embedding in this version")
        return None


    def process_text(self, text:str):
        if not text:  
            self.logger.error("No text provided to process_text")
            return None
        return text[:self.default_input_max_chars].strip()

    def generate_text(self, prompt: str, max_output_tokens: int = None , chat_history : list =[] ,temprature : float = None):
        if not self.client:
            self.logger.error("set the client")

        if not self.generation_model_id:
            self.logger.error("set the generation model")

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_token_size
        temprature = temprature if temprature else self.default_temperature

        messages = []
        messages.append(chat_history)
        messages.append(self.contrust_prompt(prompt=prompt , role = LLMenumGroq.User.value))

        response = self.client.chat.completions.create(
            model = self.generation_model_id,
            messages=messages,
            temperature = temprature,
            max_tokens = max_output_tokens
            )
        if not response or not response.choices or len(response.choices)==0:
            self.logger.error("empty response")

        return response.choices[0].message.content


    def contrust_prompt(self, prompt: str, role: str):
        return {
            "role":role,
            "content" : self.process_text(prompt)
            }
    




