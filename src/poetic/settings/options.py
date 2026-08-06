from typing import Annotated

from pydantic import BaseModel, Field

from poetic.settings.item import GitignoreSetupSettings, VSCodeSetupSettings
from poetic.settings.template import APITemplateSettings, PackageTemplateSettings

AcceptedSetupSettings = Annotated[
    PackageTemplateSettings
    | APITemplateSettings
    | VSCodeSetupSettings
    | GitignoreSetupSettings,
    Field(discriminator="type"),
]


class SettingsOptions(BaseModel):
    """
    Exists only for convenience of detecting type of settings provided in argparse
    """

    settings: AcceptedSetupSettings
