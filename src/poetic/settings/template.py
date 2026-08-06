import enum
from typing import Any, Literal, Self

from pydantic import Field, model_validator

from poetic.settings.base import SetupSettings, SetupType
from poetic.settings.item import DBSettings, DBType


class BaseTemplateSettings(SetupSettings):
    """
    Common settings for any template.
    """

    type: SetupType = Field(default=SetupType.package, description="Template type")
    name: str = Field(description="Template/repository name")
    update: bool = Field(description="Update template rather than create new")

    # FIXME: improve
    @classmethod
    def type_options(cls) -> list[SetupType]:
        return [SetupType.package, SetupType.api]

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


class PackageTemplateSettings(BaseTemplateSettings):
    """
    Package template settings.

    Include option to set up .env pydantic settings.
    """

    type: Literal[SetupType.package] = Field(
        default=SetupType.package, description="Template type"
    )
    settings: bool = Field(default=False, description="Set up .env Settings class")
    progressbar: bool = Field(
        default=False, description="Set up progress bar source code"
    )


class APITemplateSettings(BaseTemplateSettings):
    """
    API template settings.

    API template includes option to set up DB.
    """

    type: Literal[SetupType.api] = Field(
        default=SetupType.api, description="Template type"
    )
    db: DBType | None = Field(
        default=None, description="Create/update DB functionalities of given DB type"
    )
