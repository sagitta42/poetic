from pathlib import Path

from poetiq.item.db.base.base import BaseDBSetup
from poetiq.item.db.builder import DBSetupBuilder
from poetiq.item.db.dual import DualDBSetup
from poetiq.settings.item import DBSettings


class DBSetupFactory:
    """
    Factory for general DB setup.
    """

    def build(self, path: Path | None, settings: DBSettings, core: bool) -> BaseDBSetup:
        """
        Build DB setup based on DB type.

        If SQLite development mode requested, build dual DB setup (given type + )
        """
        if settings.dev_sqlite:
            return DualDBSetup(path, settings, core)

        db_setup_builder = DBSetupBuilder()
        ret = db_setup_builder.build(path, settings, core)
        return ret
