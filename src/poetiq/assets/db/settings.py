from abc import ABC, abstractmethod
import enum
import logging
from pathlib import Path
from typing import Any, Self

from pydantic import Field, model_validator

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class DBType(enum.StrEnum):
    sqlite = "sqlite"
    psql = "psql"


class DBDriver(enum.StrEnum):
    sqlite = "sqlite"
    psql = "postgresql+psycopg"

    @classmethod
    def from_db_type(cls, db_type: DBType):
        return cls[db_type.name]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    debug: bool = False


class DBSettings(Settings):
    db_type: DBType = Field(description="DB type codename")
    db_name: str = Field(
        description="DB name (psql) or .db filename without extension (SQLite)"
    )
    db_host: str = Field(description="DB host (psql) or .db directory path (SQLite)")
    db_port: int | None = Field(default=None, description="DB port (psql only)")
    db_user: str | None = Field(default=None, description="DB username (psql only)")
    db_password: str | None = Field(default=None, description="DB password (psql only)")

    @property
    def psql_fields(self) -> list[str]:
        return ["db_port", "db_user", "db_password"]

    def psql_component(self, name: str) -> Any:
        return getattr(self, name)

    @property
    def has_psql_components(self) -> bool:
        ret = not any(self.psql_component(name) is None for name in self.psql_fields)
        return ret

    @model_validator(mode="after")
    def check_db_info(self) -> Self:
        """
        Check that Settings contain full necessary DB info
        """
        if self.db_type == DBType.sqlite and self.has_psql_components:
            logging.warning(
                f"{self.db_type} driver is requested but extra psql components are found; ignoring"
            )

        if self.db_type == DBType.psql:
            for c in self.psql_fields:
                if self.psql_component(c) is None:
                    raise ValueError(f"psql component {c} missing from .env!")

        return self


class DBUrl(ABC):
    def __init__(self, db_type: DBType) -> None:
        self._type = db_type

    @abstractmethod
    def create(self, settings: DBSettings) -> URL:
        pass

    def _get_drivername(self) -> str:
        ret = DBDriver.from_db_type(self._type).value
        return ret


class SqliteUrl(DBUrl):
    def create(self, settings: DBSettings) -> URL:
        db_path = Path(settings.db_host) / f"{settings.db_name}.db"
        url = URL.create(
            drivername=self._get_drivername(),
            database=str(db_path),
        )
        return url


class PsqlUrl(DBUrl):
    def create(self, settings: DBSettings) -> URL:
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


def get_url(settings: DBSettings) -> URL:
    """
    Get DB URL based on .env variables
    """
    db_url_class = DBUrlClass.from_db_type(settings.db_type)
    db_url = db_url_class(settings.db_type)

    url = db_url.create(settings)

    return url


class MongoDBSettings(Settings):
    mongo_host: str
    mongo_port: int
    mongo_initdb_root_username: str
    mongo_initdb_root_password: str


settings = Settings()
