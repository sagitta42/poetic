import os
from pathlib import Path
import sqlite3

from poetic.item.base import BaseDependencySetup
from poetic.settings.item import DBSettings, DBType
from poetic.utils.utils import add_new_line_to_file


class DBSetup(BaseDependencySetup[DBSettings]):
    """
    DB setup.
    """

    def __init__(self, settings: DBSettings, path: Path) -> None:
        super().__init__(settings, path)

        self._db_dir: Path = Path("db")
        self._filename: str = "db.db"

        self._db_path: Path = self.path / self._db_dir / self._filename
        self._local_db_path: str = str(self._db_dir / self._filename)

    def setup_dotenv_template(self):
        """
        Setup .env template.

        Add DB_URL to .env
        """
        path_to_dotenv = super().setup_dotenv_template()

        if self._settings.db == DBType.sqlite:
            add_new_line_to_file(
                path_to_dotenv, f"DB_URL=sqlite:///{self._local_db_path}"
            )

        return path_to_dotenv

    def setup_dependencies(self) -> None:
        self._poetry_add("alembic")

    def setup(self, skip_super: bool = False) -> None:
        """
        DB setup.

        In addition to standard setup:
            - DB
            - alembic migrations
        """
        super().setup(skip_super)

        self.setup_db()
        self.setup_alembic()

    def setup_db(self):
        """
        Set up DB.

        If not present, initialize database of given type, git add the initial file.
        Set DB path in .env template.
        Update .gitignore to not track the DB file.
        """
        if self._settings.db == DBType.sqlite:
            os.makedirs(self.path / self._db_dir, exist_ok=True)

            if not self._db_path.exists():
                conn = sqlite3.connect(self._db_path)
                conn.close()

            self.git.run("add", self._local_db_path)

    def setup_alembic(self):
        """
        Set up alembic migrations.

        Set up alembic.ini.
        Init alembic.
        Set up alembic environment.
        Add alembic upgrade debugger configuration to launch.json
        Set up alembdantic.
        Set up example alembdantic model.
        Set up example migration for alembdantic usage.

        Note that alembic setup is independent from DB setup.
        Note that providing DB URL in .env is not managed by this setup.
        """
        template_subdir = "alembic"

        self._copy_template(
            "alembic.ini.template",
            package_filename="alembic.ini",
            template_subdir=template_subdir,
        )

        alembic_dir = "alembic_migrations"
        path_to_alembic = self.path / alembic_dir
        if not os.path.exists(path_to_alembic):
            self._run(self.venv("alembic"), "init", alembic_dir, env=True)

        self._copy_template(
            "env.py", path_in_package=path_to_alembic, template_subdir=template_subdir
        )

        self._add_vscode_launch_configurations("alembic.launch.json")

        alembdantic_subdir = "alembdantic"
        path_to_alembdandic = path_to_alembic / alembdantic_subdir
        os.makedirs(path_to_alembdandic, exist_ok=True)
        for filename in ["table_model.py", "opd.py"]:
            self._copy_template(
                filename,
                path_in_package=path_to_alembdandic,
                template_subdir=alembdantic_subdir,
            )

        self._copy_template(
            "models.py",
            path_in_package=self.path / alembic_dir,
            template_subdir=template_subdir,
        )

        path_to_revisions = path_to_alembic / "versions"
        os.makedirs(path_to_revisions, exist_ok=True)
        self._copy_template(
            "2026_07_15_143709-36648a63d305-example.py",
            path_in_package=path_to_revisions,
            template_subdir=template_subdir,
        )

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
