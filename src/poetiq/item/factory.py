from pathlib import Path

from poetiq.item.builder import ItemSetupBuilder
from poetiq.item.db.factory import DBSetupFactory
from poetiq.settings.item import DBSettings
from poetiq.settings.setup import SetupSettings
from poetiq.setup.base import BaseSetup


class ItemSetupFactory:
    """
    Factory for item setup independent of template.

    Creates item setup in current directory.
    Marks it as core setup.
    """

    def build(self, settings: SetupSettings, path: Path | None) -> BaseSetup:
        """
        Build item setup based on settings.

        Create builder based on settings type.
        Build setup in provided path. Default (None): build in current path
        """
        builder_class = (
            DBSetupFactory if isinstance(settings, DBSettings) else ItemSetupBuilder
        )
        builder = builder_class()
        ret = builder.build(settings, path=path or Path.cwd(), core=True)
        return ret
