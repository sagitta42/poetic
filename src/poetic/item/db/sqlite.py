import os
from pathlib import Path
import sqlite3

from dotenv import dotenv_values, set_key

from poetic.item.db.base import BaseDBSetup
from poetic.item.env_settings import EnvSettingsSetup
from poetic.settings.item import DBSettings, DBType
from poetic.utils.utils import add_new_line_to_file


class SQLiteSetup(BaseDBSetup):
    """
    SQLite DB setup.

    db_dir: DB directory within the template; hard-coded db/
    filename: DB filename; hardcoded db.db
    db_path: full path to DB file within template i.e. path/db/db.db
    local_db_path (str): local path from root template directory i.e. db/db.db
    """

    def __init__(self, path: Path, settings: DBSettings, core: bool) -> None:
        super().__init__(path, settings, core)

        self._db_dir: Path = Path("db")
        self._filename: str = "db.db"

        self._db_path: Path = self.path / self._db_dir / self._filename
        self._local_db_path: str = str(self._db_dir / self._filename)

    @property
    def db_url(self) -> str:
        """
        SQLite DB URL.

        Path to .db file.
        """
        return f"sqlite:///{self._local_db_path}"

    def setup_db(self) -> bool:
        """
        Set up SQLite DB.

        If not present, create the DB directory.
        If not present, create the .db file.
        """
        existed = True

        os.makedirs(self.path / self._db_dir, exist_ok=True)

        if not self._db_path.exists():
            conn = sqlite3.connect(self._db_path)
            conn.close()
            existed = False

        # TODO: do not commit
        self.git.run("add", self._local_db_path)
        return existed

    def untrack_db(self):
        """
        Untrack DB from git tracking.

        Add DB path to .gignore.
        Remove from cached.
        """

        add_new_line_to_file(
            self.path / ".gitignore", f"{self._local_db_path}\n", prepend=True
        )

        self.git.run("rm", "--cached", self._local_db_path)
        self.git.commit_all("untrack database (poetic)")
