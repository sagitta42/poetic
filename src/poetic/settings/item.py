import enum
from pathlib import Path
from typing import Literal, Self

from pydantic import Field, model_validator

from poetic.logger import logg
from poetic.settings.setup import SetupSettings, SetupType


class VSCodeSetupSettings(SetupSettings):
    type: Literal[SetupType.vscode] = Field(
        default=SetupType.vscode, description="Setup type"
    )


class GitignoreSetupSettings(SetupSettings):
    type: Literal[SetupType.gitignore] = Field(
        default=SetupType.gitignore, description="Setup type"
    )


class ProgressBarSettings(SetupSettings):
    type: Literal[SetupType.progressbar] = Field(
        default=SetupType.progressbar, description="Setup type"
    )


class LoggerSettings(SetupSettings):
    type: Literal[SetupType.logger] = Field(
        default=SetupType.logger, description="Setup type"
    )
    subfolder: Path = Field(default=Path(""), description="Subfolder of setup")


class DBType(str, enum.Enum):
    sqlite = "sqlite"
    psql = "psql"
    none = "none"


class DBSettings(SetupSettings):
    """
    Settings for DB setup.
    """

    type: Literal[SetupType.db] = Field(default=SetupType.db, description="Setup type")
    db_type: DBType = Field(default=DBType.sqlite, description="Database type")
    pydantic_table: bool = Field(default=False, description="Set up pydantic-table for alembic migrations")
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


class DotenvSettings(SetupSettings):
    """
    Settings for .env Settings class setup
    """

    type: Literal[SetupType.dotenv] = Field(
        default=SetupType.dotenv, description="Setup type"
    )
