from pathlib import Path

from poetiq.item.factory import ItemSetupFactory
from poetiq.settings.setup import SetupSettings
from poetiq.settings.template import BaseTemplateSettings
from poetiq.setup.functionality import BaseFunctionalitySetup
from poetiq.template.base import BaseTemplate
from poetiq.template.builder import TemplateBuilder


class PoetiqFactory:
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
