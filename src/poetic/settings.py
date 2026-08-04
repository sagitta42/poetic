import enum
from pathlib import Path
from typing import Annotated, Any, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from poetic.logger import logg


class SetupType(str, enum.Enum):
    package = "package"
    api = "api"
    db = "db"
    dotenv = "dotenv"

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


class BaseTemplateSettings(SetupSettings):
    """
    Common settings for any template.
    """

    type: SetupType = Field(default=SetupType.package, description="Template type")
    name: str = Field(description="Package name")

    # FIXME: improve
    @classmethod
    def type_options(cls) -> list[SetupType]:
        return [SetupType.package, SetupType.api]

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
    def options(cls, field_name: str) -> list:
        if field_name == "type":
            return [type.value for type in cls.type_options()]
        return super().options(field_name)

    @model_validator(mode="after")
    def check_type(self) -> Self:
        if self.type not in self.__class__.type_options():
            raise ValueError(f"Template type {self.type} not supported!")
        return self


class PackageTemplateSettings(BaseTemplateSettings, DotenvSettings):
    """
    Package template settings.

    Include option to set up .env pydantic settings.
    """

    type: Literal[SetupType.package] = Field(description="Template type", exclude=True)


class APITemplateSettings(BaseTemplateSettings, DBSettings):
    """
    API template settings.

    API template includes option to set up DB.
    """

    type: Literal[SetupType.api] = Field(description="Template type", exclude=True)


TemplateSettings = Annotated[
    PackageTemplateSettings | APITemplateSettings,
    Field(discriminator="type"),
]


class SettingsCrutch(BaseModel):
    """
    Exists only for convenience of detecting type of settings
    """

    settings: TemplateSettings
