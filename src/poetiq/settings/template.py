from typing import Literal, Self

from pydantic import Field, model_validator

from poetiq.settings.item import DBSettings, DBType
from poetiq.settings.setup import SetupSettings, SetupType


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


class AppTemplateSettings(BaseTemplateSettings, DBSettings):
    """
    Web app template settings.

    Web app template includes option to set up DB.

    NOTE: SQL-type DB arrives via --db-type flag while mongodb with separate bool.
    """

    type: Literal[SetupType.app] = Field(
        default=SetupType.app, description="Template type"
    )
    db_type: DBType = Field(default=DBType.none, description="Database type")
    mongodb: bool = Field(default=False, description="Add MongoDB service")

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

    @model_validator(mode="after")
    def check_db_type(self) -> Self:
        if self.db_type == DBType.mongo:
            raise ValueError("Not accepting MongoDB as DB type in app settings - reserved for the mongodb setting")
        return self