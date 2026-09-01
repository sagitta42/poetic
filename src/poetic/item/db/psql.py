from pathlib import Path


from poetic.item.db.base.docker import DockerDBSetup
from poetic.item.db.base.sql import DBSqlSetup
from poetic.logger import logg
from poetic.settings.item import DBSettings
from poetic.utils.db import DBEnvVars


class PsqlDBSetup(DBSqlSetup, DockerDBSetup):
    """
    PSQL database setup.
    """

    def setup_dependencies(self):
        """
        Set up dependencies for PSQL functionality.

        psycopg[binary] is needed for alembic migrations.
        """
        super().setup_dependencies()

        self._poetry_add("psycopg[binary]")
