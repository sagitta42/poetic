import enum
from typing import Any, Literal, Self

from pydantic import Field, model_validator

from poetic.settings.item import DBSettings, DotenvSettings, SetupSettings, SetupType


class BaseTemplateSettings(SetupSettings):
    """
    Common settings for any template.
    """

    type: SetupType = Field(default=SetupType.package, description="Template type")
    name: str = Field(description="Package name")
    update: bool = Field(description="Update template rather than create new")

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
        if isinstance(ret, enum.Enum):
            ret = ret.value
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
