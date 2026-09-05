from pathlib import Path

from poetiq.enums import DBType
from poetiq.setup.db.base.base import BaseDBSetup
from poetiq.setup.db.base.single import SingleDBSetup
from poetiq.setup.db.builder import DBSetupBuilder
from poetiq.logger import logg
from poetiq.settings.setup import DBSettings


class DualDBSetup(BaseDBSetup):
    """
    Dual DB setup.

    Set up of given DB type with development mode switch to SQLite.
    """

    def __init__(self, path: Path | None, settings: DBSettings, core: bool) -> None:
        super().__init__(path, settings, core)

        db_setup_builder = DBSetupBuilder()
        db_settings = settings.model_copy()
        db_settings.dev_sqlite = False

        self._db_main = db_setup_builder.build(self.path, db_settings, core=False)
        self._sqlite_setup = db_setup_builder.build(
            self.path, DBSettings(db_type=DBType.sqlite), core=False
        )

    @property
    def main(self) -> SingleDBSetup:
        return self._db_main

    def setup_db(self):
        """
        Dual DB setup.

        Full setup of main DB.
        Set up only DB of the SQLite switch.
        Add SQLite variables commented out to .env
        Add SQLite notes to README.
        """
        logg.info(
            f"@ Dual DB setup with {self.db_type} / SQLite .env switch",
            header=True,
        )

        self.main.setup()
        self._sqlite_setup.setup_db()
        self._env.add_comment(
            "Comment out these variables to replace psql with SQLite in alembic migrations and app"
        )
        self._sqlite_setup._add_env_vars(comment=True)
        self._sqlite_setup.setup_readme()
