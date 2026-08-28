import enum
from typing import TypeVar

from pydantic import Field

from poetic.settings.base import BaseSettings


class SetupType(str, enum.Enum):
    package = "package"
    app = "app"
    db = "db"
    dotenv = "dotenv"
    vscode = "vscode"
    gitignore = "gitignore"
    progressbar = "progressbar"
    logger = "logger"
    install = "install"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]


class SetupSettings(BaseSettings):
    """
    Base class for settings for any type of setup.
    """

    type: SetupType = Field(description="Setup type")
    no_commit: bool = Field(default=False, description="Do not commit changes")


T_SetupSettings = TypeVar("T_SetupSettings", bound=SetupSettings)
