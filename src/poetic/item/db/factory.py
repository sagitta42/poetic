from pathlib import Path

from poetic.item.db.base import BaseDBSetup
from poetic.item.db.builder import DBSetupBuilder
from poetic.item.db.dual import DualDBSetup
from poetic.settings.item import DBSettings
from poetic.setup.builder import BaseSetupBuilder


class DBSetupFactory(BaseSetupBuilder[DBSettings]):
    """
    Factory for general DB setup.
    """

    def build(self, settings: DBSettings, path: Path, core: bool) -> BaseDBSetup:
        """
        Build DB setup based on DB type.

        If SQLite development mode requested, build dual DB setup (given type + )
        """
        if settings.dev_sqlite:
            return DualDBSetup(path, settings, core)

        db_setup_builder = DBSetupBuilder()
        ret = db_setup_builder.build(settings, path, core)
        return ret
