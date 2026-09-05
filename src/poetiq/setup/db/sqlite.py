import os
from pathlib import Path
import sqlite3


from poetiq.enums import DBType
from poetiq.setup.db.base.sql import DBSqlSetup
from poetiq.settings.setup import DBSettings
from poetiq.utils.db import SqlDBEnvVars
from poetiq.utils.path import File


class SQLiteSetup(DBSqlSetup[SqlDBEnvVars]):
    """
    SQLite DB setup.

    In case of SQLite,
        DB_HOST is treated as path to .db file
        DB_NAME is treated as .db filename (without extension)

    db_dir: DB directory within the template; hard-coded db/
    filename: DB filename; hardcoded db.db
    db_path: full path to DB file within template i.e. path/db/db.db
    local_db_path (str): local path from root template directory i.e. db/db.db
    """

    def __init__(
        self,
        path: Path,
        env_vars: SqlDBEnvVars,
        settings: DBSettings = DBSettings(db_type=DBType.sqlite),
        core: bool = False,
    ) -> None:
        super().__init__(path, env_vars, settings, core)

        self._db_dir = Path(self._env_vars.host.value)
        self._filename = f"{self._env_vars.name.value}.db"
        self._local_db_path: str = str(self._db_dir / self._filename)

    def setup_db(self):
        """
        Set up SQLite DB.

        If not present, create the .db file.
        Add path to .db file to .gitignore if not yet present.
        """
        super().setup_db()

        local_path_to_file = self._db_dir / self._filename
        full_path_to_file = self.path / local_path_to_file
        if not full_path_to_file.exists():
            os.makedirs(full_path_to_file.parent, exist_ok=True)
            conn = sqlite3.connect(full_path_to_file)
            conn.close()

        File(self.path / ".gitignore").add_new_line(
            str(local_path_to_file), prepend=True
        )
