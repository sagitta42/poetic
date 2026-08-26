from pathlib import Path

from poetic.item.db.base import BaseDBSetup
from poetic.item.db.builder import DBSetupBuilder
from poetic.item.db.sqlite import SQLiteSetup
from poetic.settings.item import DBSettings, DBType
from poetic.utils.docker import DBEnvVars, EnvVar


class DualDBSetup(BaseDBSetup):
    """
    Dual DB setup.

    Set up of given DB type with development mode switch to SQLite.
    """

    def __init__(self, path: Path, settings: DBSettings, core: bool) -> None:
        super().__init__(path, settings, core)

        db_setup_builder = DBSetupBuilder()
        db_settings = settings.model_copy()
        db_settings.dev_sqlite = False
        self._db_main = db_setup_builder.build(db_settings, self.path, core=False)

        self._sqlite_setup = SQLiteSetup(self.path, core=False)

    @property
    def env_vars(self) -> DBEnvVars:
        """
        docker env variables - vars of the main setup
        """
        return self._db_main.env_vars

    def setup(self):
        """
        Dual DB setup.

        Full setup of main DB.
        Set up only DB of the SQLite switch.
        Add SQLite variables commented out to .env
        Add SQLite notes to README.
        """

        self._db_main.setup()
        self._sqlite_setup.setup_db()
        self._env.add_comment(
            "Comment out these variables to replace psql with SQLite in alembic migrations and app"
        )
        self._sqlite_setup.add_env_vars(comment=True)
        self._sqlite_setup.setup_readme()
