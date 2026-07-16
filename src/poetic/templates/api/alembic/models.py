from typing import Literal

from pydantic import Field

from alembic_migrations.alembdantic.table_model import TableModel


class ExampleTable(TableModel):
    table_name_: Literal["examples"] = Field(
        default="examples", description="Table name"
    )
    id: int = Field(description="ID")
    name: str = Field(description="Name")
    value: float = Field(description="Value")
