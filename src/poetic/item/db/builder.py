import enum
from pathlib import Path

from poetic.item.db.mongo import MongoDBSetup
from poetic.item.db.psql import PsqlDBSetup
from poetic.item.db.base.single import SingleDBSetup
from poetic.item.db.sqlite import SQLiteSetup
from poetic.logger import logg
from poetic.settings.item import DBSettings, DBType
from poetic.setup.builder import BaseSetupBuilder
from poetic.utils.db import DBEnvVars, EnvVar


class DBSetupClass(enum.Enum):
    sqlite = SQLiteSetup
    psql = PsqlDBSetup
    mongo = MongoDBSetup

    @classmethod
    def from_db_type(cls, db_type: DBType):
        return cls[db_type.name]


class DBPort(int, enum.Enum):
    psql = 5432
    mongo = 27017

    @classmethod
    def from_db_type(cls, db_type: DBType) -> int:
        return cls[db_type.name].value


class DBSetupBuilder(BaseSetupBuilder[DBSettings]):
    """
    Builder for DB setup of specific DB type.
    """

    def build(self, settings: DBSettings, path: Path, core: bool) -> SingleDBSetup:
        """
        Build DB setup based on DB type.

        If SQLite development mode requested, build dual DB setup (given type + )
        """
        setup_class = DBSetupClass.from_db_type(settings.db_type).value
        env_vars = self._build_db_env_vars(settings.db_type)
        ret = setup_class(path, env_vars, settings, core)
        return ret

    def _build_db_env_vars(self, db_type: DBType) -> DBEnvVars:
        """
        Build DB env vars for given type of DB.

        In case of SQLite, host = directory of .db file, name = filename; otherwise host and name of database
        """
        host_var_name = "MONGO_HOST" if db_type == DBType.mongo else "DB_HOST"

        if db_type == DBType.sqlite:
            host_var_value = "db"
            user = None
            password = None
            port = None
        else:
            host_var_value = "localhost"
            auth_name_prefix = "MONGO_INITDB_ROOT" if db_type == DBType.mongo else "DB"
            user = EnvVar(
                name=f"{auth_name_prefix}_USER",
                value="changeme",
                service_name="POSTGRES_USER" if db_type == DBType.psql else None,
            )
            password = EnvVar(name=f"{auth_name_prefix}_PASSWORD", value="changeme", service_name="POSTGRES_PASSWORD" if db_type == DBType.psql else None)
            port_var_name_prefix = "MONGO" if db_type == DBType.mongo else "DB"
            port = EnvVar(
                name=f"{port_var_name_prefix}_PORT", value=DBPort.from_db_type(db_type)
            )

        ret = DBEnvVars(
            db_type=EnvVar(name="DB_TYPE", value=db_type.value),
            name=EnvVar(
                name="DB_NAME",
                value="database",
                service_name="POSTGRES_DB" if db_type == DBType.psql else None,
            ),
            host=EnvVar(name=host_var_name, value=host_var_value),
            port=port,
            user=user,
            password=password,
        )

        logg.debug(f"Env vars for {db_type}: {ret}")
        # ret.display() # TODO: MyBaseModel
        return ret
