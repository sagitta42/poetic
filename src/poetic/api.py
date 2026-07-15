import os
import yaml

from poetic.base import Template
from poetic.logger import logg
from poetic.pyproject_handler import PyProjectHandler
from poetic.settings import APITemplateSettings


class APITemplate(Template[APITemplateSettings]):
    def __init__(self, settings: APITemplateSettings) -> None:
        super().__init__(settings)

        self._db = settings.db

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
        if self._db:
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
        self._setup_docker_compose()

    def setup_extra(self):
        if self._db:
            self.setup_alembic()

    def setup_alembic(self):
        """
        Set up alembic migrations
        """
        self._copy_template("alembic.ini.template", package_filename="alembic.ini")
        self._run(self.venv("alembic"), "init", "alembic", env=True)

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
