from pydantic import Field

from poetiq.settings.base import BaseActionSettings


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
        description="Dual package to reinstall if local install; default all dual packages",
    )

    @property
    def split_requested(self) -> bool:
        return self.split
