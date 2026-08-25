import os
from pathlib import Path
import sqlite3


from poetic.item.db.base import BaseDBSetup, EnvVar
from poetic.settings.item import DBSettings
from poetic.utils.files import add_new_line_to_file


class SQLiteSetup(BaseDBSetup):
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

    def __init__(self, path: Path, settings: DBSettings, core: bool) -> None:
        super().__init__(path, settings, core)

        self._db_host = EnvVar(name="DB_HOST", value="db")
        self._env_vars += [self._db_host]

        self._db_dir = Path(self._db_host.value)
        self._filename = f"{self._db_name.value}.db"

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

        add_new_line_to_file(
            self.path / ".gitignore", f"{local_path_to_file}\n", prepend=True
        )
