from pathlib import Path

from poetic.item.factory import ItemSetupFactory
from poetic.logger import logg
from poetic.settings.item import SetupSettings
from poetic.settings.template import BaseTemplateSettings
from poetic.setup.functionality import BaseFunctionalitySetup
from poetic.template.base import BaseTemplate
from poetic.template.builder import TemplateBuilder


class PoeticFactory:
    def build(
        self, settings: BaseTemplateSettings | SetupSettings, path: Path | None = None
    ) -> BaseTemplate | BaseFunctionalitySetup:
        """
        Build template or functionlaity setup.
        """
        if isinstance(settings, BaseTemplateSettings):
            builder_class = TemplateBuilder
        elif isinstance(settings, SetupSettings):
            builder_class = ItemSetupFactory
        else:
            raise ValueError(
                f"Settings class {settings.__class__.__name__} not supported in factory!"
            )

        builder = builder_class()
        ret = builder.build(settings, path)
        return ret
