from typing import Annotated

from pydantic import BaseModel, Field

from poetic.settings.item import DBSettings, GitignoreSetupSettings, VSCodeSetupSettings
from poetic.settings.template import APITemplateSettings, PackageTemplateSettings

AcceptedSetupSettings = Annotated[
    PackageTemplateSettings
    | APITemplateSettings
    | VSCodeSetupSettings
    | GitignoreSetupSettings
    | DBSettings,
    Field(discriminator="type"),
]


class SettingsOptions(BaseModel):
    """
    Exists only for convenience of detecting type of settings provided in argparse
    """

    settings: AcceptedSetupSettings
