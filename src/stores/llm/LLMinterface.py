from abc import ABC, abstractmethod
class LLMinterface(ABC):
    @abstractmethod
    def set_generation_model(self, model_name: str):
        """Set the model to be used for text generation."""
        pass
    @abstractmethod
    def set_embedings_model(self, model_name: str , embeding_size:int):
        """Set the model to be used for embeddings."""
        pass
    @abstractmethod
    def generate_text(self, prompt: str, max_output_tokens: int = None , chat_history : list =[] ,temprature : float = None):
        pass
    @abstractmethod
    def embed_text(self, text: str,document_type:str):
        """Generate embeddings for the given text."""
        pass
    @abstractmethod
    def contrust_prompt(self, prompt: str, chat_history: list):
        """Construct a prompt for the LLM based on the input and chat history."""
        pass



