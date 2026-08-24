from typing import Literal, Self

from pydantic import Field, model_validator

from poetic.settings.base import SetupSettings, SetupType
from poetic.settings.item import DBType


class BaseTemplateSettings(SetupSettings):
    """
    Common settings for any template.
    """

    type: SetupType = Field(default=SetupType.package, description="Template type")
    name: str = Field(description="Template/repository name")

    def core_settings(self) -> dict:
        ret = self.model_dump(exclude={"no_commit": True, "update": True, "name": True})
        return ret


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


class AppTemplateSettings(BaseTemplateSettings):
    """
    Web app template settings.

    Web app template includes option to set up DB.
    """

    type: Literal[SetupType.app] = Field(
        default=SetupType.app, description="Template type"
    )
    db: DBType = Field(default=DBType.none, description="Database type")

    @classmethod
    def const(cls, arg: str) -> str:
        """
        Constant value for argument.

        If --db flag is used without value, default to SQLite.
        Use default value as const for all other arguments.
        """
        if arg == "db":
            return DBType.sqlite
        return super().const(arg)
