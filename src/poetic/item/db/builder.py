import enum
from pathlib import Path

from poetic.item.db.base import BaseDBSetup
from poetic.item.db.psql import PsqlDBSetup
from poetic.item.db.sqlite import SQLiteSetup
from poetic.settings.item import DBSettings, DBType
from poetic.setup.builder import BaseSetupBuilder


class DBSetupClass(enum.Enum):
    sqlite = SQLiteSetup
    psql = PsqlDBSetup

    @classmethod
    def from_db_type(cls, db_type: DBType):
        return cls[db_type.name]


class DBSetupBuilder(BaseSetupBuilder[DBSettings]):
    """
    Builder for DB setup.
    """

    def build(self, settings: DBSettings, path: Path, core: bool) -> BaseDBSetup:
        """
        Build DB setup based on DB type.
        """
        # FIXME: avoid duplication with ItemSetupBuilder
        setup_class = DBSetupClass.from_db_type(settings.db_type).value
        ret = setup_class(path, settings, core)
        return ret
