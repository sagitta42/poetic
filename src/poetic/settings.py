import enum
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from poetic.logger import logg


class SetupSettings(BaseModel):
    """
    Base class for settings for any type of setup.
    """

    pass


class DBType(str, enum.Enum):
    sqlite = "sqlite"


class DBSettings(SetupSettings):
    """
    Settings for DB setup.
    """

    model_config = ConfigDict(extra="ignore")

    db: DBType | None = Field(
        description="Create/update DB functionalities of given DB type"
    )


class TemplateType(str, enum.Enum):
    package = "package"
    api = "api"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]


class TemplateSettings(SetupSettings):
    """
    Common settings for any template.
    """

    model_config = ConfigDict(extra="forbid")

    name: str = Field(description="Package name")
    type: TemplateType = Field(
        default=TemplateType.package, description="Template type"
    )

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


# FIXME: DB template settings (not only for API); or just unite settings
class APITemplateSettings(TemplateSettings, DBSettings):
    """
    API template settings.

    API template includes option to set up DB.
    """

    @model_validator(mode="after")
    def check_db(self) -> Self:
        if self.db is not None and self.type != TemplateType.api:
            logg.warning(
                f"DB functionalities not supported for {self.type.value} template; ignoring",
                important=True,
            )
        return self


class SettingsCrutch(BaseModel):
    """
    Exists only for convenience of detecting type of settings
    """

    settings: TemplateSettings | APITemplateSettings
