import enum
from pathlib import Path
from typing import Literal, Self

from pydantic import Field, model_validator

from poetic.logger import logg
from poetic.settings.setup import SetupSettings, SetupType


class ItemSetupSettings(SetupSettings):
    subfolder: Path = Field(default=Path(""), description="Subfolder of setup")


class VSCodeSetupSettings(SetupSettings):
    type: Literal[SetupType.vscode] = Field(
        default=SetupType.vscode, description="Setup type"
    )


class GitignoreSetupSettings(SetupSettings):
    type: Literal[SetupType.gitignore] = Field(
        default=SetupType.gitignore, description="Setup type"
    )


class ProgressBarSettings(ItemSetupSettings):
    type: Literal[SetupType.progressbar] = Field(
        default=SetupType.progressbar, description="Setup type"
    )


class LoggerSettings(ItemSetupSettings):
    type: Literal[SetupType.logger] = Field(
        default=SetupType.logger, description="Setup type"
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


class DBSettings(SetupSettings):
    """
    Settings for DB setup.
    """

    type: Literal[SetupType.db] = Field(default=SetupType.db, description="Setup type")
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

    type: Literal[SetupType.dotenv] = Field(
        default=SetupType.dotenv, description="Setup type"
    )
