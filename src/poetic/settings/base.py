import enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SetupType(str, enum.Enum):
    package = "package"
    api = "api"
    db = "db"
    dotenv = "dotenv"
    vscode = "vscode"
    gitignore = "gitignore"
    progressbar = "progressbar"

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

    @classmethod
    def default(cls, field_name: str) -> Any:
        ret = cls.model_fields[field_name].default
        if isinstance(ret, enum.Enum):
            ret = ret.value
        return ret