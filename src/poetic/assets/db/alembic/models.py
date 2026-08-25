from typing import Literal

from pydantic import Field

from pydantibase import TableModel


class ExampleTable(TableModel):
    table_name_: Literal["examples"] = Field(
        default="examples", description="Table name", exclude=True
    )
    id: int = Field(description="ID")
    name: str = Field(description="Name")
    value: float = Field(description="Value")
