from pydantic import BaseSettings

class Settings(BaseSettings):
    path: int
    database_username: str
    secret_key: str

settings = Settings()