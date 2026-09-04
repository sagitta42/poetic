from typing import Type

from poetiq.action.base import BaseAction
from poetiq.settings.base import BaseActionSettings
from poetiq.settings.options import SettingsOptions, ActionOptions, TemplateOptions
from poetiq.settings.template import BaseTemplateSettings


class SettingsBuilder:
    """
    Settings builder.
    """

    def build_action(self, settings: dict) -> BaseActionSettings:
        """
        Build accepted setup settings.
        """
        ret = self._build_settings_from_options(settings, ActionOptions)
        return ret

    def build_template(self, settings: dict) -> BaseTemplateSettings:
        """
        Build accepted template settings.
        """
        ret = self._build_settings_from_options(settings, TemplateOptions)
        return ret

    def _build_settings_from_options(
        self, settings: dict, setting_options: Type[SettingsOptions]
    ) -> BaseAction:
        ret = setting_options(**{"settings": settings}).settings
        return ret
