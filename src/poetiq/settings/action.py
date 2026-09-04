from pydantic import Field, model_validator
from typing import Self

from poetiq.exceptions import PoetiqException
from poetiq.settings.base import BaseActionSettings, BaseSplitActionSettings


class InstallSettings(BaseActionSettings):
    split: bool = Field(
        default=False,
        description="Install from multiple split pyproject.toml files defined in poetiq.toml",
    )
    local: bool = Field(
        default=False, description="Install local dependencies defined in poetiq.toml"
    )
    package: str = Field(
        default="",
        description="Package to install in split or local mode",
    )

    @property
    def split_requested(self) -> bool:
        return self.split


class AddSettings(BaseSplitActionSettings):
    package: str = Field(description="Package source (name, https, git)")
    split: str = Field(
        default="",
        description="Add split dependency to pyproject.toml of given directory",
    )
    local: str = Field(default="", description="Add local dependency to poetiq.toml")

    @property
    def split_requested(self) -> bool:
        return self.split != ""

    @model_validator(mode="after")
    def check_split_local(self) -> Self:
        """
        Split and local are mutually exclusive options.
        """
        if self.split and self.local:
            raise PoetiqException(
                "Provide either --split or --local argument, not both!"
            )
        return self
