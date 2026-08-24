from typing import Annotated, Union

from pydantic import BaseModel, Field

from poetic.settings.item import (
    DBSettings,
    GitignoreSetupSettings,
    LoggerSettings,
    VSCodeSetupSettings,
)
from poetic.settings.template import APITemplateSettings, PackageTemplateSettings

AcceptedSetupSettings = Annotated[
    PackageTemplateSettings
    | APITemplateSettings
    | VSCodeSetupSettings
    | GitignoreSetupSettings
    | DBSettings
    | LoggerSettings,
    Field(discriminator="type"),
]


class SetupOptions(BaseModel):
    """
    Exists for convenience of constructing and validating accepted setup settings.
    """

    settings: AcceptedSetupSettings


AcceptedTemplateSettings = Annotated[
    PackageTemplateSettings | APITemplateSettings,
    Field(discriminator="type"),
]


class TemplateOptions(BaseModel):
    """
    Exists for convenience of constructing and validating accepted template options.
    """

    settings: AcceptedTemplateSettings

SettingsOptions = Union[SetupOptions, TemplateOptions]