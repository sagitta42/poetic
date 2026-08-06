from pathlib import Path

from poetic.item.builder import ItemSetupBuilder
from poetic.item.db.builder import DBSetupBuilder
from poetic.settings.base import SetupSettings
from poetic.settings.item import DBSettings
from poetic.setup.base import BaseSetup


class ItemSetupFactory:
    """
    Factory for item setup independent of template.

    Creates item setup in current directory.
    Marks it as core setup.
    """

    def build(self, settings: SetupSettings) -> BaseSetup:
        """
        Build item setup based on settings.

        Create builder based on settings type.
        Build setup.
        """
        builder_class = (
            DBSetupBuilder if isinstance(settings, DBSettings) else ItemSetupBuilder
        )
        builder = builder_class()
        ret = builder.build(settings, path=Path.cwd(), core=True)
        return ret
