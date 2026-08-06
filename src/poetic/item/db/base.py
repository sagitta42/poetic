from abc import abstractmethod
import os
from pathlib import Path

from dotenv import dotenv_values, set_key

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
    def setup_db(self) -> bool:
        """
        Set up DB.

        Return bool flag to represent whether this setup already existed.
        """
        pass

    @property
    @abstractmethod
    def db_url(self) -> str:
        """
        DB URL for .env
        """
        pass

    def setup(self) -> bool:
        """
        DB setup.

        In addition to standard setup:
            - DB
            - alembic migrations
            - update .env template if necessary
        """
        existed = super().setup()

        existed = existed or self.setup_db()
        existed = existed or self.setup_alembic()

        return existed

    def setup_dependencies(self) -> None:
        super().setup_dependencies()
        
        self._poetry_add("alembic")

    def setup_alembic(self) -> bool:
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

        Returns bool on whether this setup existed before.
        """
        logg.info("...setting up alembic", header=True)
        template_subdir = "alembic"

        _, existed = self._copy_template(
            "alembic.ini.template",
            package_filename="alembic.ini",
            template_subdir=template_subdir,
        )

        alembic_dir = "alembic_migrations"
        path_to_alembic = self.path / alembic_dir
        if not os.path.exists(path_to_alembic):
            self._run(self.venv("alembic"), "init", alembic_dir, env=True)
        else:
            existed = True

        existed = existed or self._update_dotenv_template()

        if not self._env_settings_setup.is_present():
            self._env_settings_setup.setup()
        else:
            existed = True

        _, env_existed = self._copy_template(
            "env.py", path_in_package=path_to_alembic, template_subdir=template_subdir
        )
        existed = existed or env_existed

        existed = existed or self._add_vscode_launch_configurations(
            "alembic.launch.json"
        )

        alembdantic_subdir = "alembdantic"
        path_to_alembdandic = path_to_alembic / alembdantic_subdir
        os.makedirs(path_to_alembdandic, exist_ok=True)
        for filename in ["table_model.py", "opd.py"]:
            _, file_existed = self._copy_template(
                filename,
                path_in_package=path_to_alembdandic,
                template_subdir=alembdantic_subdir,
            )
            existed = existed or file_existed

        _, file_existed = self._copy_template(
            "models.py",
            path_in_package=self.path / alembic_dir,
            template_subdir=template_subdir,
        )
        existed = existed or file_existed

        path_to_revisions = path_to_alembic / "versions"
        os.makedirs(path_to_revisions, exist_ok=True)
        _, file_existed = self._copy_template(
            "2026_07_15_143709-36648a63d305-example.py",
            path_in_package=path_to_revisions,
            template_subdir=template_subdir,
        )
        existed = existed or file_existed

        return existed

    def _update_dotenv_template(self) -> bool:
        """
        Update .env.template

        Add DB_URL to .env
        DB_URL variable is read in alembic env.py

        Return flag reprsenting whether this variable already existed in .env
        """
        path_to_dotenv = self._get_filepath_in_package(".env.template")

        var_name = "DB_URL"

        var_existed = dotenv_values(path_to_dotenv).get(var_name, None) is not None
        set_key(path_to_dotenv, var_name, self.db_url)

        return var_existed
