from poetic.item.base import BaseItemSetup
from poetic.item.builder import ItemBuilder
from poetic.settings.item import SetupSettings
from poetic.settings.template import BaseTemplateSettings
from poetic.template.base import BaseTemplate
from poetic.template.builder import TemplateBuilder


class PoeticFactory:
    def build(
        self, settings: BaseTemplateSettings | SetupSettings
    ) -> BaseTemplate | BaseItemSetup:
        """
        Build template or functionlaity setup.
        """
        if isinstance(settings, BaseTemplateSettings):
            builder_class = TemplateBuilder
        elif isinstance(settings, SetupSettings):
            builder_class = ItemBuilder
        else:
            raise ValueError(
                f"Settings class {settings.__class__.__name__} not supported in factory!"
            )

        builder = builder_class()
        ret = builder.build(settings)
        return ret
