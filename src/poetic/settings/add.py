from pydantic import Field

from poetic.settings.base import BaseSettings


class AddSettings(BaseSettings):
    package: str = Field(description="Package source (name, https, git)")
    local: str = Field(default="", description="Add local dependency to poetic.toml")
