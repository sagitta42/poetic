from abc import abstractmethod
import os
from pathlib import Path

from dotenv import set_key

from poetic.item.env_settings import EnvSettingsSetup
from poetic.logger import logg
from poetic.settings.item import DBSettings
from poetic.setup.dependency import BaseDependencySetup


class BaseDBSetup(BaseDependencySetup[DBSettings]):
    """
    DB setup.
    """

    def __init__(self, path: Path, settings: DBSettings, core: bool) -> None:
        super().__init__(path, settings, core)

        self._env_settings_setup = EnvSettingsSetup(self.path, core=False)

    @property
    def title(self) -> str:
        return f"{super().title}: {self._settings.db.value}"

    @abstractmethod
    def setup_db(self):
        """
        Set up DB.
        """
        pass

    @property
    @abstractmethod
    def db_url(self) -> str:
        """
        DB URL for .env
        """
        pass

    def setup(self) -> None:
        """
        DB setup.

        In addition to standard setup:
            - DB
            - alembic migrations
            - update .env template if necessary
        """
        super().setup()

        self.setup_db()
        self.setup_alembic()

    def setup_dependencies(self):
        super().setup_dependencies()

        self._poetry_add("alembic")

    def setup_alembic(self):
        """
        Set up alembic migrations.

        Set up alembic.ini.
        Init alembic if not init already.
        Update .env.template setting DB_URL.
        Set up .env Settings class if does not exist yet (used in alembic env.py for DB URL)
        Set up alembic environment (env.py).
        Add alembic upgrade debugger configuration to launch.json
        Set up alembdantic.
        Set up example alembdantic model.
        Set up example migration for alembdantic usage.
        """
        logg.info("...setting up alembic", header=True)
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

        self._update_dotenv_template()

        if not self._env_settings_setup.is_present():
            self._env_settings_setup.setup()

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

    def _update_dotenv_template(self):
        """
        Update .env.template

        Add DB_URL to .env
        DB_URL variable is read in alembic env.py
        """
        path_to_dotenv = self._get_filepath_in_package(".env.template")
        var_name = "DB_URL"

        set_key(path_to_dotenv, var_name, self.db_url)
