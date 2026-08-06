import enum
from typing import Literal

from pydantic import Field

from poetic.settings.base import SetupSettings, SetupType


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


class DBType(str, enum.Enum):
    sqlite = "sqlite"


class DBSettings(SetupSettings):
    """
    Settings for DB setup.
    """

    type: Literal[SetupType.db] = Field(default=SetupType.db, description="Setup type")
    db: DBType = Field(description="Database type")


class DotenvSettings(SetupSettings):
    """
    Settings for .env Settings class setup
    """

    type: Literal[SetupType.dotenv] = Field(
        default=SetupType.dotenv, description="Setup type"
    )
