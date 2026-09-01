from typing import Annotated, Union

from pydantic import BaseModel, Field

from poetiq.settings.item import (
    DBSettings,
    GitignoreSetupSettings,
    LoggerSettings,
    VSCodeSetupSettings,
)
from poetiq.settings.template import AppTemplateSettings, PackageTemplateSettings

AcceptedSetupSettings = Annotated[
    PackageTemplateSettings
    | AppTemplateSettings
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
    PackageTemplateSettings | AppTemplateSettings,
    Field(discriminator="type"),
]


class TemplateOptions(BaseModel):
    """
    Exists for convenience of constructing and validating accepted template options.
    """

    settings: AcceptedTemplateSettings


SettingsOptions = Union[SetupOptions, TemplateOptions]
