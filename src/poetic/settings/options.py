from typing import Annotated

from pydantic import BaseModel, Field

from poetic.settings.item import GitignoreSetupSettings, VSCodeSetupSettings
from poetic.settings.template import APITemplateSettings, PackageTemplateSettings


TemplateSettings = Annotated[
    PackageTemplateSettings
    | APITemplateSettings
    | VSCodeSetupSettings
    | GitignoreSetupSettings,
    Field(discriminator="type"),
]


class SettingsCrutch(BaseModel):
    """
    Exists only for convenience of detecting type of settings
    """

    settings: TemplateSettings
