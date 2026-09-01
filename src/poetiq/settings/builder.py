from typing import Type

from poetiq.settings.options import SettingsOptions, SetupOptions, TemplateOptions
from poetiq.settings.setup import SetupSettings
from poetiq.settings.template import BaseTemplateSettings
from poetiq.setup.functionality import BaseFunctionalitySetup


class SettingsBuilder:
    """
    Settings builder.
    """

    def build_setup(self, settings: dict) -> SetupSettings:
        """
        Build accepted setup settings.
        """
        ret = self._build_settings_from_options(settings, SetupOptions)
        return ret

    def build_template(self, settings: dict) -> BaseTemplateSettings:
        """
        Build accepted template settings.
        """
        ret = self._build_settings_from_options(settings, TemplateOptions)
        return ret

    def _build_settings_from_options(
        self, settings: dict, setting_options: Type[SettingsOptions]
    ) -> BaseFunctionalitySetup:
        ret = setting_options(**{"settings": settings}).settings
        return ret
