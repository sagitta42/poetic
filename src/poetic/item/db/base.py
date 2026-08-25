from abc import abstractmethod
import json
import os
from pathlib import Path


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
        logg.info(f"...setting up {self._settings.db.value} DB", header=True)

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

    def setup_alembic(self):
        """
        Set up alembic migrations.

        Set up alembic.ini.
        Init alembic if not init already.
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
            self.run(self.venv("alembic"), "init", alembic_dir, env=True)

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

    def setup_readme(self):
        """
        Set up README.

        Add DB readme.
        Add alembic readme.
        """
        self._add_readme_section("DB", header=2)
        path_to_db_readme = self._get_template_path(
            "README.md", template_subdir=self._settings.db
        )
        self._update_readme_from_template(path_to_db_readme)

        self._add_readme_section("alembic", header=3)
        path_to_alembic_readme = self._get_template_path(
            "README.md", template_subdir="alembic"
        )
        self._update_readme_from_template(path_to_alembic_readme)

    def _add_vscode_launch_configurations(self, template_filename: str):
        """
        Add configurations to VSCode launch.json contained in given template.
        """

        path_to_launch = self.path / ".vscode" / "launch.json"
        if not path_to_launch.exists():
            self._vscode_setup.setup()

        with open(path_to_launch) as f:
            launch_dct = json.load(f)

        path_to_template = self._get_template_path(
            template_filename, generic=False, template_subdir="alembic"
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
