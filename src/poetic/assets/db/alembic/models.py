
from pydantic import Field

from pydantic_table import TableModel


class ExampleTable(TableModel, table_name="examples"):
    id: int = Field(description="ID")
    name: str = Field(description="Name")
    value: float = Field(description="Value")
