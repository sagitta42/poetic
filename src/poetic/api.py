import json
import os
from pathlib import Path
import sqlite3
import yaml

from poetic.base import Template
from poetic.pyproject_handler import PyProjectHandler
from poetic.settings import APITemplateSettings, DBType
from poetic.utils import add_new_line_to_file


class APITemplate(Template[APITemplateSettings]):
    def __init__(self, settings: APITemplateSettings) -> None:
        super().__init__(settings)

        self._db = settings.db
        self._has_db = self._db is not None

    def poetry_init(self):
        """
        Initialize package with poetry.

        Basic setup with only pyproject.toml.
        Disable package mode.
        """
        os.mkdir(self.name)

        self._run(
            "poetry",
            "init",
            "--no-interaction",
            "--name",
            self.name,
            "--description",
            "",
        )

        pyproject_handler = PyProjectHandler(self.path)
        pyproject_handler.add_section("tool.poetry", {"package-mode": False})
        pyproject_handler.del_section("build-system")
        pyproject_handler.save_toml()

    def setup_dependencies(self):
        super().setup_dependencies()

        self._poetry_add("fastapi")
        self._poetry_add("pydantic")
        self._poetry_add("pydantic_settings")
        self._poetry_add("uvicorn")
        if self._has_db:
            self._poetry_add("alembic")

    def setup_source_files(self):
        """
        Set up dummy source files
        """
        self._setup_subfolders()

        self._copy_template("config.py")

        package_filename = "dummy.py"

        self._copy_template(
            "core.py",
            path_in_package=self.path / "core",
            package_filename=package_filename,
        )

        path_to_app = self.path / "app"
        self._copy_template(
            "service.py",
            path_in_package=path_to_app / "services",
            package_filename=package_filename,
        )
        self._copy_template(
            "schemas.py",
            path_in_package=path_to_app / "schemas",
            package_filename=package_filename,
        )

        path_to_api = path_to_app / "api"
        self._copy_template(
            "route.py",
            path_in_package=path_to_api / "routes",
            package_filename=package_filename,
        )
        self._copy_template("router.py", path_in_package=path_to_api)

        self._copy_template("main.py")

    def setup_extra(self):
        """
        Additional setup.

        Set up docker compose file.
        Set up alembic migrations and DB if requested.
        """
        self._setup_docker_compose()

        if self._has_db:
            self.setup_db()

    def setup_db(self):
        """
        Set up DB.

        Set up alembic migrations.
        Set up alembic utils.
        If not present, initialize database of given type.
            Git add the initial file.
        Set DB path in .env template.
        Update .gitignore to not track the DB file.
        Add alembic upgrade debugger configuration to launch.json
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

        for filename in ["models.py", "utils.py"]:
            self._copy_template(
                filename,
                path_in_package=self.path / alembic_dir,
                template_subdir=template_subdir,
            )

        db_dir = Path("db")
        path_to_db = self.path / db_dir
        db_file = "db.db"
        if self._db == DBType.sqlite and not os.path.exists(path_to_db):
            os.mkdir(path_to_db)

            conn = sqlite3.connect(path_to_db / db_file)
            conn.close()

            self._git_template.run("add", db_dir / db_file)

        add_new_line_to_file(
            self.path / ".env.template", f"DB_URL=sqlite:///{db_dir / db_file}"
        )
        add_new_line_to_file(
            self.path / ".gitignore", f"{db_dir / db_file}\n", prepend=True
        )

        self._add_vscode_launch_configuration("alembic.launch.json")

    def _setup_subfolders(self):
        """
        Set up subfolders.

        app: app code (api, schemas, serviecs)
        core: code logic/engine code
        """

        for subfolder in ["app", "core"]:
            os.makedirs(self.path / subfolder, exist_ok=True)

        for app_subfolder in ["api", "schemas", "services"]:
            os.makedirs(self.path / "app" / app_subfolder, exist_ok=True)

        os.makedirs(self.path / "app" / "api" / "routes", exist_ok=True)

    def _setup_docker_compose(self):
        """
        Set up docker compose.

        Copy template and update app name.
        """
        path_to_yml = self._copy_template("docker-compose.yml", generic=False)

        with open(path_to_yml) as f:
            yml_info = yaml.safe_load(f)

        yml_info["services"]["api"]["environment"]["APP_NAME"] = self.name

        with open(path_to_yml, "w") as f:
            yaml.dump(yml_info, f)

    def _add_vscode_launch_configuration(self, template_filename: str):
        """
        Add configuration to VSCode launch.json contained in given template.
        """
        path_to_launch = self.path / ".vscode" / "launch.json"
        if not path_to_launch.exists():
            return

        with open(path_to_launch) as f:
            launch_dct = json.load(f)

        path_to_config = self._get_template_path(
            template_filename, generic=False, template_subdir="alembic"
        )
        with open(path_to_config) as f:
            config = json.load(f)

        launch_dct["configurations"].append(config)

        with open(path_to_launch, "w") as f:
            json.dump(launch_dct, f, indent=4)
