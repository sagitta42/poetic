from poetiq.item.db.base.docker import DockerDBSetup
from poetiq.item.db.base.sql import DBSqlSetup
from poetiq.utils.db import PsqlDBEnvVars


class PsqlDBSetup(DBSqlSetup[PsqlDBEnvVars], DockerDBSetup[PsqlDBEnvVars]):
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
