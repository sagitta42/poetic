from abc import abstractmethod
import json
import os
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field


from poetic.item.env_settings import EnvSettingsSetup
from poetic.logger import logg
from poetic.settings.item import DBSettings, DBType
from poetic.setup.poetry import BasePoetrySetup
from poetic.utils.docker import DBEnvVars, EnvVar


class BaseDBSetup(BasePoetrySetup[DBSettings]):
    """
    Base class for DB setup.

    service_name: Service name in docker-compose
    """

    def __init__(self, path: Path, settings: DBSettings, core: bool) -> None:
        super().__init__(path, settings, core)

        self.service_name: str = f"db_{self._settings.db_type.value}"
        self.db_type = self._settings.db_type

    # TODO: improve - not all DBs are docker related (e.g. SQLite) - possibly subclass
    @property
    @abstractmethod
    def env_vars(self) -> DBEnvVars:
        """
        DB env variables.

        Are set up in docker.
        May be same as .env variables or contain fewer or more variables.
        """
        pass


class DBSetup(BaseDBSetup):
    """
    DB setup.

    env_vars: DB environment variables (e.g. in docker-compose)
    """

    def __init__(self, path: Path, settings: DBSettings, core: bool) -> None:
        super().__init__(path, settings, core)

        self._env_vars = DBEnvVars(
            db_type=EnvVar(name="DB_TYPE", value=self._settings.db_type.value),
            name=EnvVar(name="DB_NAME", value="database"),
            host=EnvVar(name="DB_HOST", value="changeme"),
        )

        self._env_settings_setup = EnvSettingsSetup(
            self.path, template_setup=self._type, core=False
        )

    @property
    def env_vars(self) -> DBEnvVars:
        """
        docker env variables
        """
        return self._env_vars

    @property
    def dotenv_vars(self) -> DBEnvVars:
        """
        .env variables
        """
        return self._env_vars

    @property
    def title(self) -> str:
        return f"{super().title}: {self.db_type.value}"

    @abstractmethod
    def setup_db(self):
        """
        Set up DB.
        """
        logg.info(f"...setting up {self.db_type.value} DB", header=True)

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
        self.setup_dotenv_template()

    def setup_dependencies(self):
        super().setup_dependencies()

        self._poetry_add("alembic")
        self._poetry_add("git+https://github.com/sagitta42/pydantic-table.git@v0.2.0")

    def setup_alembic(self):
        """
        Set up alembic migrations.

        Set up alembic.ini.
        Init alembic if not init already.
        Set up .env Settings class if does not exist yet (used in alembic env.py for DB URL)
        Set up alembic environment (env.py).
        Add alembic upgrade debugger configuration to launch.json
        Set up example alembdantic model.
        Set up example migration for alembdantic usage.
        """
        logg.info("...setting up alembic", header=True)
        template_subdir = "alembic"

        self._templates.copy(
            "alembic.ini.template",
            package_filename="alembic.ini",
            template_subdir=template_subdir,
        )

        alembic_dir = "alembic_migrations"
        path_to_alembic = self.path / alembic_dir
        if not os.path.exists(path_to_alembic):
            self.run(self.venv("alembic"), "init", alembic_dir, env=True)

        self._env_settings_setup.setup()

        self._templates.copy(
            "env.py", package_path=path_to_alembic, template_subdir=template_subdir
        )

        self._add_vscode_launch_configurations("alembic.launch.json")

        self._templates.copy(
            "models.py",
            package_path=self.path / alembic_dir,
            template_subdir=template_subdir,
        )

        path_to_revisions = path_to_alembic / "versions"
        os.makedirs(path_to_revisions, exist_ok=True)
        self._templates.copy(
            "2026_07_15_143709-36648a63d305-example.py",
            package_path=path_to_revisions,
            template_subdir=template_subdir,
        )

    def setup_dotenv_template(self):
        """
        Set up DB .env variables in .env.template.
        """
        super().setup_dotenv_template()

        self.add_env_vars()

    def add_env_vars(self, comment: bool = False):
        """
        Add env vars to .env template as values or commented out.
        """
        for env_var in self.dotenv_vars.set_vars:
            self._env.set(**env_var.model_dump(), comment=comment)

    def setup_readme(self):
        """
        Set up README.

        Add DB readme.
        Add alembic readme.
        """
        super().setup_readme()
        logg.info("...setting up README.md")

        self._readme.add_section("DB", header=2)
        path_to_db_readme = self._templates.get_filepath(
            "README.md", subdir=self.db_type.value
        )
        self._readme.update_from_template(path_to_db_readme)

        self._readme.add_section("alembic", header=3)
        path_to_alembic_readme = self._templates.get_filepath(
            "README.md", subdir="alembic"
        )
        self._readme.update_from_template(path_to_alembic_readme)

    def _add_vscode_launch_configurations(self, template_filename: str):
        """
        Add configurations to VSCode launch.json contained in given template.
        """

        path_to_launch = self.path / ".vscode" / "launch.json"
        if not path_to_launch.exists():
            self._vscode.setup()

        with open(path_to_launch) as f:
            launch_dct = json.load(f)

        path_to_template = self._templates.get_filepath(
            template_filename, subdir="alembic"
        )
        with open(path_to_template) as f:
            template_config = json.load(f)

        configuration_names = [
            config["name"] for config in launch_dct["configurations"]
        ]

        for config in template_config["configurations"]:
            if config["name"] not in configuration_names:
                launch_dct["configurations"].append(config)

        with open(path_to_launch, "w") as f:
            json.dump(launch_dct, f, indent=4)
