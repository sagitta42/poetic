from pydantic import BaseModel, Field


class DummyResponse(BaseModel):
    message: str = Field(description="Response message")


class DummyRequest(BaseModel):
    foo: int = Field(description="Dummy request information")
