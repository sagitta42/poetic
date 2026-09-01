from pydantic_table import ColumnField, TableModel


class ExampleTable(TableModel, table_name="examples"):
    id: int = ColumnField(description="ID", primary_key=True)
    name: str = ColumnField(description="Name")
    value: float = ColumnField(description="Value", nullable=True)
