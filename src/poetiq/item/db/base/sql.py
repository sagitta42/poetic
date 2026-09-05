import json
import os


from poetiq.item.db.base.single import SingleDBSetup
from poetiq.logger import logg
from poetiq.utils.db import T_SqlDBEnvVars


class DBSqlSetup(SingleDBSetup[T_SqlDBEnvVars]):
    """
    SQL type DB setup (SQLite, psql).

    Includes alembic setup
    """

    def setup(self) -> None:
        """
        DB setup.

        In addition to standard setup:
            - alembic migrations
            - update .env template if necessary
        """
        super().setup()

        self.setup_alembic()

    def setup_dependencies(self):
        super().setup_dependencies()

        self._poetry_add("alembic")
        if self._settings.pydantic_table:
            self._poetry_add("pydantic-table")

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
        logg.info(f"- setting up alembic migrations")
        template_subdir = "alembic"

        self._templates.copy(
            "alembic.ini.template",
            package_filename="alembic.ini",
            template_subdir=template_subdir,
        )

        alembic_dir = "alembic_migrations"
        path_to_alembic = self.path / alembic_dir
        if not path_to_alembic.exists():
            self._venv.run("alembic", "init", alembic_dir, info=True)

        self._env_settings_setup.setup()

        self._templates.copy(
            "env.py", package_path=path_to_alembic, template_subdir=template_subdir
        )

        self._add_vscode_launch_configurations("alembic.launch.json")

        if self._settings.pydantic_table:
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

    def setup_readme(self):
        super().setup_readme()

        self._readme.add_new_section("alembic", header=3)
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
