from .LLMenum import LLMenum
from .provider import CohereProvider,GrokProvider,EmbeddingProvider
from helpers.config import Settings

class LLMProviderFactory:

    def __init__(self,config:Settings):
        self.config = config

    def create(self,provider:str):
        if provider == LLMenum.Cohere.value:
            
            return CohereProvider(api_key=self.config.cohere_api_key,
                                  default_generation_max_output_token_size=self.config.default_generation_max_output_token_size,
                                  default_input_max_chars=self.config.default_input_max_chars,
                                  default_temperature=self.config.default_temperature)


        if provider == LLMenum.Groq.value:  

            return GrokProvider(api_key=self.config.groq_api_key ,
                               api_url=self.config.groq_api_url,
                               default_generation_max_output_token_size=self.config.default_generation_max_output_token_size,
                               default_input_max_chars=self.config.default_input_max_chars,
                               default_temperature=self.config.default_temperature)

        if provider == LLMenum.CohereEmbedding.value:
            return EmbeddingProvider(api_key=self.config.cohere_api_key,
                                    default_generation_max_output_token_size=self.config.default_generation_max_output_token_size,
                                    default_input_max_chars=self.config.default_input_max_chars,
                                    default_temperature=self.config.default_temperature)
        return None

