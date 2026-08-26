import enum
import logging
from typing import Self

from pydantic import Field, model_validator

from pydantic_settings import BaseSettings, SettingsConfigDict


class DBType(str, enum.Enum):
    sqlite = "sqlite"
    psql = "psql"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    db_type: DBType = Field(description="DB type codename")
    db_name: str = Field(
        description="DB name (psql) or .db filename without extension (SQLite)"
    )
    db_host: str = Field(description="DB host (psql) or .db directory path (SQLite)")
    db_port: int | None = Field(default=None, description="DB port (psql only)")
    db_user: str | None = Field(default=None, description="DB username (psql only)")
    db_password: str | None = Field(default=None, description="DB password (psql only)")
    debug: bool = False

    @property
    def has_psql_components(self) -> bool:
        """
        Settings have all necessary psql components
        """
        psql_components = [self.db_port, self.db_user, self.db_password]

        ret = not any(component is None for component in psql_components)
        return ret

    @model_validator(mode="after")
    def check_db_info(self) -> Self:
        """
        Check that Settings contain full necessary DB info
        """
        if self.db_type == DBType.sqlite and self.has_psql_components:
            logging.warning(
                f"{self.db_type.value} driver is requested but extra psql components are found; ignoring"
            )

        if self.db_type == DBType.psql and not self.has_psql_components:
            raise ValueError(
                "psql components missing from .env! Provide DB port, username, and password"
            )

        return self


settings = Settings()
