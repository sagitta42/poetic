import os

from poetic.item.db.base import BaseDBSetup
from poetic.item.db.builder import DBSetupBuilder
from poetic.item.env_settings import EnvSettingsSetup
from poetic.settings.item import DBSettings
from poetic.settings.template import APITemplateSettings
from poetic.template.base import BaseTemplate
from poetic.utils.docker import DockerHandler
from poetic.utils.toml import PyProjectHandler


class APITemplate(BaseTemplate[APITemplateSettings]):
    def __init__(self, settings: APITemplateSettings) -> None:
        super().__init__(settings)

        self._env_settings_setup = EnvSettingsSetup(self.path, core=False)
        db_setup_builder = DBSetupBuilder()
        self._db: BaseDBSetup | None = (
            None
            if settings.db is None
            else db_setup_builder.build(
                DBSettings(db=settings.db), self.path, core=False
            )
        )

        self._docker = DockerHandler(self.path)

    def poetry_init(self):
        """
        Initialize package with poetry.

        Basic setup with only pyproject.toml.
        Disable package mode.
        """
        super().poetry_init()
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

    def setup(self) -> None:
        """
        API template setup.

        In addition to standard template setup:
            - docker compose file
            - DB if requested
        """
        super().setup()

        self.setup_docker_compose()

        if self._db is not None:
            self._db.setup()

    def setup_dependencies(self) -> None:
        """
        Set up dependencies.
        """
        super().setup_dependencies()

        self._poetry_add("fastapi")
        self._poetry_add("uvicorn")

    def setup_source_files(self):
        """
        Set up source files.

        Set up subfolder structure.
        Set up settings and app info.
        Set up dummy source files for core logic, services, schemas, and routers.
        Set up main uvicorn launchable script.
        """
        self._setup_subfolders()

        self._copy_template("app_info.py")

        package_filename = "dummy.py"

        path_to_core = self.path / "core"
        self._copy_template(
            "core.py",
            path_in_package=path_to_core,
            package_filename=package_filename,
        )
        self._copy_template("db.py", path_in_package=path_to_core)
        self._copy_template(
            "model.py",
            path_in_package=path_to_core / "models",
            package_filename="example.py",
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

    def setup_docker_compose(self):
        """
        Set up docker compose.

        Copy template and set container name.
        TODO: Set up DB URL in API service if exists.
        TODO: update DB service container name.
        """
        path_to_template = self._get_template_path("docker-compose.yml")
        self._docker.update_docker_compose_from_template(path_to_template)

        self._docker.update_service_container_name("api", f"{self.name}_api")

    def _setup_subfolders(self):
        """
        Set up subfolders.

        app: app code (api, schemas, serviecs)
        core: code logic/engine code
        """

        for subfolder in ["app", "core"]:
            os.makedirs(self.path / subfolder, exist_ok=True)

        os.makedirs(self.path / "core" / "models", exist_ok=True)

        for app_subfolder in ["api", "schemas", "services"]:
            os.makedirs(self.path / "app" / app_subfolder, exist_ok=True)

        os.makedirs(self.path / "app" / "api" / "routes", exist_ok=True)
