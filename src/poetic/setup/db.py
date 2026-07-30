import os
from pathlib import Path
import sqlite3

from poetic.utils.git import Git
from poetic.settings import DBType
from poetic.utils.utils import add_new_line_to_file


class DBSetup:
    """
    DB setup.

    path (Path): path to root directory where DB is set up

    """

    def __init__(self, path: Path, type: DBType) -> None:
        self.root_path: Path = path
        self._type: DBType = type

        self._db_dir: Path = Path("db")
        self._filename: str = "db.db"

        self._db_path: Path = self.root_path / self._db_dir / self._filename
        self._local_db_path: str = str(self._db_dir / self._filename)

        self.git = Git(self.root_path)

    def setup(self):
        """
        Set up DB.

        If not present, initialize database of given type, git add the initial file.
        Set DB path in .env template.
        Update .gitignore to not track the DB file.
        """

        if self._type == DBType.sqlite:
            os.makedirs(self.root_path / self._db_dir, exist_ok=True)

            if not self._db_path.exists():
                conn = sqlite3.connect(self._db_path)
                conn.close()

            self.git.run("add", self._local_db_path)

        add_new_line_to_file(
            self.root_path / ".env.template", f"DB_URL=sqlite:///{self._local_db_path}"
        )

    def untrack_db(self):
        """
        Untrack DB from git tracking.

        Add DB path to .gignore.
        Remove from cached.
        """

        add_new_line_to_file(
            self.root_path / ".gitignore", f"{self._local_db_path}\n", prepend=True
        )

        self.git.run("rm", "--cached", self._local_db_path)
        self.git.commit_all("untrack database (poetic)")
