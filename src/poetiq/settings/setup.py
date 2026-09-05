from pathlib import Path
from typing import Literal, Self

from pydantic import Field, model_validator

from poetiq.enums import ActionType, DBType
from poetiq.logger import logg
from poetiq.settings.base import BaseSetupSettings


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

    type: Literal[ActionType.envsettings] = Field(
        default=ActionType.envsettings, description="Setup type"
    )
