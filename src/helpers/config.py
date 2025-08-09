from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    groq_api_key :str  
    APP_ID:str
    APP_name:str
    APP_description:str
    APP_version:str
    APP_author:str
    file_allowed_types : list
    file_max_size : int
    file_default_chunk_size : int
    MONGODB_URI : str
    mongo_db_name : str

    generation_groq_backend : str
    generation_cohere_backend : str
    Embedding_backend : str
    
    groq_api_key: str
    groq_api_url : str
    
    cohere_api_key : str
    
    Generation_model_id : str
    
    Embedding_model_id: str
    Embedding_model_size: int
    
    default_generation_max_output_token_size : int
    default_temperature : float
    default_input_max_chars : int


    vector_db_backend : str
    vector_db_path    : str
    vector_db_distance: str 

    qdrant_api_key : str 
    qdrant_api_url : str 

    Default_language :str
    supported_languages : list[str]


def get_settings() -> Settings:
    """
    Load and return the application settings.
    """
    return Settings()