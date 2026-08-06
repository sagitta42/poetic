import enum
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SetupType(str, enum.Enum):
    package = "package"
    api = "api"
    db = "db"
    dotenv = "dotenv"
    vscode = "vscode"
    gitignore = "gitignore"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]


class SetupSettings(BaseModel):
    """
    Base class for settings for any type of setup.
    """

    model_config = ConfigDict(extra="ignore")

    type: SetupType = Field(description="Setup type")

    @classmethod
    def options(cls, field_name: str) -> list:
        field_type = cls.model_fields[field_name].annotation
        assert field_type is not None
        if issubclass(field_type, enum.Enum):
            return [item.value for item in field_type if not item.name == "none"]
        return []


class VSCodeSetupSettings(SetupSettings):
    type: Literal[SetupType.vscode] = Field(
        default=SetupType.vscode, description="Setup type"
    )


class GitignoreSetupSettings(SetupSettings):
    type: Literal[SetupType.gitignore] = Field(
        default=SetupType.gitignore, description="Setup type"
    )


class DBType(str, enum.Enum):
    sqlite = "sqlite"
    none = "none"


class DBSettings(SetupSettings):
    """
    Settings for DB setup.
    """

    type: Literal[SetupType.db] = Field(description="Setup type")
    db: DBType = Field(description="Create/update DB functionalities of given DB type")


class DotenvSettings(SetupSettings):
    """
    Settings for .env settings reading setup
    """

    type: Literal[SetupType.dotenv] = Field(description="Setup type")
    settings: bool = Field(default=False, description="Set up .env settings module")
    package_subdir: Path | None = Field(
        default=None,
        description="Subdirectory in package where to set up the settings source file; None defaults to root path",
    )
