from typing import Literal

from pydantic import Field

from poetic.settings.base import SetupSettings, SetupType


class InstallSettings(SetupSettings):
    type: Literal[SetupType.install] = Field(
        default=SetupType.install, description="Setup type"
    )
    local: bool = Field(
        default=False, description="Install local dependencies defined in .poetic.toml"
    )
    package: str = Field(
        default="",
        description="Dual package to reinstall if local install; default all dual packages",
    )
