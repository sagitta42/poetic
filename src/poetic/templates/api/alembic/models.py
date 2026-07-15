import enum
from typing import Type

from pydantic import BaseModel, Field

class TableModel(BaseModel):
    id: int = Field(description="ID")

class ExampleTable(TableModel):
    name: str = Field(description="Name")
    value: float = Field(description="Value")

class TableNames(str, enum.Enum):
    ExampleTable = "examples"

    @classmethod
    def from_table_model(cls, table_model: Type[TableModel]) -> str:
        return cls[table_model.__name__].value

    @classmethod
    def from_row(cls, table_model: TableModel) -> str:
        return cls.from_table_model(table_model.__class__)
    
