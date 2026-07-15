import enum
from typing import Type

from alembic import op
from pydantic import BaseModel
import sqlalchemy as sa

from alembic_migrations.models import TableModel, TableNames


class SaColumnType(enum.Enum):
    int = sa.Integer
    float = sa.Float
    str = sa.String

    @classmethod
    def from_type(cls, t: type):
        return cls[t.__name__]


class Column(BaseModel):
    name: str
    description: str
    type: type
    primary_key: bool = False
    nullable: bool = False
    foreign_key: str | None = None

    @property
    def sa_type(self) -> sa.types.TypeEngine:
        return SaColumnType.from_type(self.type).value()

    def get_sa_column(self) -> sa.Column:
        foreign_key_args = []
        if self.foreign_key is not None:
            foreign_key = sa.ForeignKey(
                name=f"fk_{self.foreign_key.replace('.','_')}",
                column=self.foreign_key,
            )
            foreign_key_args = [foreign_key]

        return sa.Column(
            self.name,
            self.sa_type,
            nullable=self.nullable,
            primary_key=self.primary_key,
            *foreign_key_args,
        )


class Table(BaseModel):
    name: str
    columns: list[Column]


def get_table_columns(table_model: Type[TableModel]) -> list[Column]:
    ret = []
    for name, info in table_model.model_fields.items():
        col = Column(name=name, description=info.description, type=info.annotation)
        ret.append(col)
    return ret


def make_table_columns(
    model: Type[TableModel],
    primary_keys: list[str] = [],
    foreign_keys: dict[str, str] = {},
) -> list[Column]:
    # TODO: validation (columns in primary/foreign keys do not exist)
    cols = get_table_columns(model)
    for col in cols:
        if col.name in primary_keys:
            col.primary_key = True
        if col.name in foreign_keys:
            col.foreign_key = foreign_keys[col.name]
    return cols


def create_table(table_model: Type[TableModel]):
    columns = get_table_columns(table_model)
    table_name = TableNames.from_table_model(table_model)

    table = Table(name=table_name, columns=columns)

    op.create_table(
        table.name,
        *(c.get_sa_column() for c in table.columns),
    )

def drop_table(table_model: Type[TableModel]):
    table_name = TableNames.from_table_model(table_model)
    op.drop_table(table_name)


def read_table(table_name: str) -> sa.Table:
    metadata = sa.MetaData()
    ret = sa.Table(table_name, metadata, autoload_with=op.get_bind())
    return ret


def add_row(row: TableModel):
    table_name = TableNames.from_row(row)
    table = read_table(table_name)
    op.execute(table.insert().values(row.model_dump()))


def delete_row_by_id(row: TableModel):
    table_name = TableNames.from_row(row)
    table = read_table(table_name)
    op.execute(table.delete().where(table.c.id == row.id))