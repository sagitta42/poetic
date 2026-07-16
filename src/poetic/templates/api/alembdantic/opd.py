from alembic import op
import sqlalchemy as sa
from typing import Type

from alembic_migrations.alembdantic.table_model import TableModel


def create_table(
    table_model: Type[TableModel],
    primary_keys: list[str] = [],
    foreign_keys: dict[str, str] = {},
):
    """
    Invoke alembic create table based on provided TableModel schema.

    primary_keys (list[str]): list of primary key column names
    foreign_keys (dict[str, str]): dictionary mapping {column name: foreign key column information}
        Format of foreign key is foreign_table.column

    Column names must correspond to TableModel field names.
    """
    columns = table_model.get_sa_columns(primary_keys, foreign_keys)
    op.create_table(table_model.table_name(), *columns)


def drop_table(table_model: Type[TableModel]):
    """
    Invoke alembic drop table based on provided TableModel schema.
    """
    op.drop_table(table_model.table_name())


def read_table(table: str | Type[TableModel]) -> sa.Table:
    """
    Get sqlalchemy table based on given table name or schema.
    """
    table_name = table if isinstance(table, str) else table.table_name()
    metadata = sa.MetaData()
    ret = sa.Table(table_name, metadata, autoload_with=op.get_bind())
    return ret


def insert(row: TableModel):
    """
    Insert given row to the table corresponding to its schema.

    Read table based on table name.
    Invoke alembic execute with model dump.
    """

    table = read_table(row.table_name())
    op.execute(table.insert().values(row.model_dump()))


def delete_row_by_id(row: TableModel):
    """
    Delete given row from the table it corresponds to based on ID.

    Applies only to tables that have an ID column.
    """
    if not row.has_id_column:
        raise ValueError(
            f"Table {row.table_name()} does not have an id column! Cannot delete row by ID"
        )
    table = read_table(row.table_name())
    op.execute(table.delete().where(table.c.id == row.id))
