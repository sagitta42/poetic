from pydantic import BaseModel


class MyMongoDocument(BaseModel):
    dummy: str