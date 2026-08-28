from pydantic import Field

from poetic.settings.base import BaseSettings


class InstallSettings(BaseSettings):
    local: bool = Field(
        default=False, description="Install local dependencies defined in .poetic.toml"
    )
    package: str = Field(
        default="",
        description="Dual package to reinstall if local install; default all dual packages",
    )
