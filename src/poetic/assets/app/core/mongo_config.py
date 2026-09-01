from pydantic import BaseModel

from settings import MongoDBSettings

settings = MongoDBSettings()


class MongoConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    authSource: str = "admin"


def get_mongo_config() -> MongoConfig:
    """
    Get MongoConfig from .env settings
    """
    ret = MongoConfig(
        host=settings.mongo_host,
        port=settings.mongo_port,
        username=settings.mongo_initdb_root_username,
        password=settings.mongo_initdb_root_password,
        authSource="admin",
    )
    return ret
