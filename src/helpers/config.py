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

def get_settings() -> Settings:
    """
    Load and return the application settings.
    """
    return Settings()