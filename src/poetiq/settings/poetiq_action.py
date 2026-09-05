from pydantic import Field, model_validator
from typing import Literal, Self

from poetiq.enums import ActionType
from poetiq.exceptions import PoetiqException
from poetiq.settings.base import BasePoetiqActionSettings, BaseSplitActionSettings


class InstallSettings(BasePoetiqActionSettings):
    """
    poetiq install settings

    Note that install action is not a true split poetiq action.
    The --local flag is a boolean that installs from all split directoreis or none.
    TODO: similar to add/lock, accept optional DIR name to install from only specific split dir.
    """

    type: Literal[ActionType.install] = Field(
        default=ActionType.install, description="Action type"
    )
    split: bool = Field(
        default=False,
        description="Install from multiple split pyproject.toml files defined in poetiq.toml",
    )
    local: bool = Field(
        default=False, description="Install local dependencies defined in poetiq.toml"
    )
    package: str = Field(
        default="",
        description="Specific package to install in split or local model; otherwise all local/split",
    )

    @property
    def split_requested(self) -> bool:
        return self.split


class AddSettings(BaseSplitActionSettings):
    type: Literal[ActionType.add] = Field(
        default=ActionType.add, description="Action type"
    )
    package: str = Field(description="Package source (name, https, git)")
    split: str = Field(
        default="",
        description="Add to split pyproject.toml file(s) (all or specified DIR)",
    )
    local: str = Field(
        default="", description="Add local dependency to poetiq.toml in given path"
    )

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


class LockSettings(BaseSplitActionSettings):
    type: Literal[ActionType.lock] = Field(
        default=ActionType.lock, description="Action type"
    )
    split: str = Field(
        default="",
        description="Update split poetry.lock(s) (all or specified DIR)",
    )