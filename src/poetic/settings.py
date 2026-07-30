import enum
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from poetic.logger import logg


class SetupSettings(BaseModel):
    """
    Base class for settings for any type of setup.
    """

    model_config = ConfigDict(extra="ignore")


class DBType(str, enum.Enum):
    sqlite = "sqlite"


class DBSettings(SetupSettings):
    """
    Settings for DB setup.
    """

    db: DBType | None = Field(
        description="Create/update DB functionalities of given DB type"
    )


class DotenvSettings(SetupSettings):
    """
    Settings for .env settings reading setup
    """

    settings: bool = Field(default=False, description="Set up .env settings module")


class TemplateType(str, enum.Enum):
    package = "package"
    api = "api"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]


class BaseTemplateSettings(SetupSettings):
    """
    Common settings for any template.
    """

    type: TemplateType = Field(
        default=TemplateType.package, description="Template type"
    )
    name: str = Field(description="Package name")

    @classmethod
    def description(cls, field_name: str) -> str:
        ret = cls.model_fields[field_name].description
        assert ret is not None
        return ret

    @classmethod
    def default(cls, field_name: str) -> Any:
        ret = cls.model_fields[field_name].default
        return ret

    @classmethod
    def options(cls, field_name: str) -> list | None:
        field_type = cls.model_fields[field_name].annotation
        assert field_type is not None
        if issubclass(field_type, enum.Enum):
            return [item.value for item in field_type]
        return None


class PackageTemplateSettings(BaseTemplateSettings):
    """
    Package template settings.

    Include option to set up .env pydantic settings.
    """

    type: Literal[TemplateType.package] = Field(description="Template type")


class APITemplateSettings(BaseTemplateSettings, DBSettings):
    """
    API template settings.

    API template includes option to set up DB.
    """

    type: Literal[TemplateType.api] = Field(description="Template type")


TemplateSettings = Annotated[
    PackageTemplateSettings | APITemplateSettings,
    Field(discriminator="type"),
]


class SettingsCrutch(BaseModel):
    """
    Exists only for convenience of detecting type of settings
    """

    settings: TemplateSettings
