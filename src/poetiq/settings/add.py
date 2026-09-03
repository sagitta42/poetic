from typing import Self

from pydantic import Field, model_validator

from poetiq.exceptions import PoetiqException
from poetiq.settings.base import BaseActionSettings


class AddSettings(BaseActionSettings):
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
