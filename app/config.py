from typing import Dict
from pydantic import BaseSettings


class Settings(BaseSettings):
    mongodb_uri: str
    mongodb_dbname: str
    mongodb_collections: Dict[str, str] = {}
    mongodb_max_pool_size: int = 1000
    mongodb_min_poll_size: int = 100

    class Config:

        env_file = ".env"

settings = Settings()