import enum
from pathlib import Path
from typing import Literal, Self

from pydantic import Field, model_validator

from poetiq.logger import logg
from poetiq.settings.base import ActionType, BaseSetupSettings


class ItemSetupSettings(BaseSetupSettings):
    subfolder: Path = Field(default=Path(""), description="Subfolder of setup")


class VSCodeSetupSettings(BaseSetupSettings):
    type: Literal[ActionType.vscode] = Field(
        default=ActionType.vscode, description="Setup type"
    )


class GitignoreSetupSettings(BaseSetupSettings):
    type: Literal[ActionType.gitignore] = Field(
        default=ActionType.gitignore, description="Setup type"
    )


class ProgressBarSettings(ItemSetupSettings):
    type: Literal[ActionType.progressbar] = Field(
        default=ActionType.progressbar, description="Setup type"
    )


class LoggerSettings(ItemSetupSettings):
    type: Literal[ActionType.logger] = Field(
        default=ActionType.logger, description="Setup type"
    )


class DBType(str, enum.Enum):
    sqlite = "sqlite"
    psql = "psql"
    mongo = "mongo"
    none = "none"

    @classmethod
    def all(cls) -> list[str]:
        """
        All DB types.

        None (no DB) is excluded (not a DB type, a flag to set up no DB)
        """
        all_types = [db_type for db_type in cls if not db_type == cls.none]
        ret = cls._values(all_types)
        return ret

    @classmethod
    def sql(cls) -> list[str]:
        """
        SQL based DB types.
        """
        sql_types = [cls.sqlite, cls.psql]
        ret = cls._values(sql_types)
        return ret

    @classmethod
    def service(cls):
        """
        Service DBs
        """
        ret = [cls.psql, cls.mongo]
        return ret

    @classmethod
    def with_none(cls, db_types: list[str]) -> list[str]:
        """
        Include none (no DB) with given types
        """
        ret = db_types + [cls.none.value]
        return ret

    @classmethod
    def _values(cls, db_types: list) -> list[str]:
        """
        Return str values of list of given db types.
        """
        ret = [db.value for db in db_types]
        return ret


class DBSettings(BaseSetupSettings):
    """
    Settings for DB setup.
    """

    type: Literal[ActionType.db] = Field(
        default=ActionType.db, description="Setup type"
    )
    db_type: DBType = Field(default=DBType.sqlite, description="Database type")
    pydantic_table: bool = Field(
        default=False, description="Set up pydantic-table for alembic migrations"
    )
    dev_sqlite: bool = Field(
        default=False, description="Development mode switch to SQLite"
    )

    @model_validator(mode="after")
    def check_dev(self) -> Self:
        """
        Check DB type VS development mode.
        """
        # TODO: improve - separate subclasses with settings for each DB type, discriminator db_type
        if self.db_type == DBType.mongo and (self.pydantic_table or self.dev_sqlite):
            raise ValueError(
                "pydantic-table or dev-sqlite settings are not applicable for MongoDB!"
            )

        if self.dev_sqlite and self.db_type == DBType.sqlite:
            logg.warning(
                f"Development mode with switch to SQLite requested but main DB type requested is SQLite; ignoring"
            )
            self.dev_sqlite = False

        return self


class DotenvSettings(ItemSetupSettings):
    """
    Settings for .env Settings class setup
    """

    type: Literal[ActionType.dotenv] = Field(
        default=ActionType.dotenv, description="Setup type"
    )
