from abc import ABC, abstractmethod
import enum
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import URL, engine_from_config
from sqlalchemy import pool

from alembic import context

from settings import DBType, settings


class DBDriver(str, enum.Enum):
    sqlite = "sqlite"
    psql = "postgresql+psycopg"

    @classmethod
    def from_db_type(cls, db_type: DBType):
        return cls[db_type.name]


class DBUrl(ABC):
    def __init__(self, db_type: DBType) -> None:
        self._type = db_type

    @abstractmethod
    def create(self) -> URL:
        pass

    def _get_drivername(self) -> str:
        ret = DBDriver.from_db_type(self._type).value
        return ret


class SqliteUrl(DBUrl):
    def create(self) -> URL:
        db_path = Path(settings.db_host) / f"{settings.db_name}.db"
        url = URL.create(
            drivername=self._get_drivername(),
            database=str(db_path),
        )
        return url


class PsqlUrl(DBUrl):
    def create(self) -> URL:
        url = URL.create(
            drivername=self._get_drivername(),
            database=settings.db_name,
            host=settings.db_host,
            port=settings.db_port,
            username=settings.db_user,
            password=settings.db_password,
        )
        return url


class DBUrlClass(enum.Enum):
    sqlite = SqliteUrl
    psql = PsqlUrl

    @classmethod
    def from_db_type(cls, db_type: DBType):
        return cls[db_type.name].value


def get_url() -> URL:
    """
    Get DB URL based on .env variables
    """
    db_url_class = DBUrlClass.from_db_type(settings.db_type)
    db_url = db_url_class(settings.db_type)

    url = db_url.create()

    return url


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DB to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=get_url(),
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
