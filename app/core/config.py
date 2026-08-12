from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    app_version: str
    debug: bool

    database_url: str

    secret_key: str
    gemini_api_key: str
    qdrant_url: str
    qdrant_collection: str

    class Config:
        env_file = ".env"


settings = Settings()