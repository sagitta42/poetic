import os
from pathlib import Path

from poetic.item.db.base import BaseDBSetup
from poetic.item.db.docker import DockerDBSetup
from poetic.item.db.factory import DBSetupFactory
from poetic.item.env_settings import EnvSettingsSetup
from poetic.settings.item import DBSettings, DBType
from poetic.settings.setup import SetupType
from poetic.settings.template import AppTemplateSettings
from poetic.template.base import BaseTemplate
from poetic.utils.docker import DockerComposeServiceHandler


class AppTemplate(BaseTemplate[AppTemplateSettings]):
    def __init__(self, settings: AppTemplateSettings, path: Path | None) -> None:
        super().__init__(settings, path)

        self._env_settings_setup = EnvSettingsSetup(
            self.path, template_setup=SetupType.db, core=False
        )
        db_setup_builder = DBSetupFactory()
        self._db: BaseDBSetup | None = (
            None
            if settings.db_type == DBType.none
            else db_setup_builder.build(
                DBSettings(db_type=settings.db_type, dev_sqlite=settings.dev_sqlite),
                self.path,
                core=False,
            )
        )

        self._service = DockerComposeServiceHandler(self.path, "app")

    def _poetry_init(self):
        """
        Initialize package with poetry.

        Basic setup with only pyproject.toml.
        Disable package mode.
        """
        os.makedirs(self.path, exist_ok=True)

        super()._poetry_init()

    def setup(self) -> None:
        """
        App template setup.

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

    def setup_pyproject(self):
        """
        Set up pyproject.toml.

        Additional setup: set package-mode as False and remove build-system section.
        """
        super().setup_pyproject()

        self._pyproject_handler.add_section("project", {"package-mode": False})
        self._pyproject_handler.del_section("build-system")
        self._pyproject_handler.write()

    def setup_source_files(self):
        """
        Set up source files.

        Set up subfolder structure.
        Set up settings and app info.
        Set up dummy source files for core logic, services, schemas, and routers.
        Set up main uvicorn launchable script.
        """
        self._setup_subfolders()

        self._templates.copy("app_info.py")

        package_filename = "dummy.py"

        path_to_core = self.path / "core"
        self._templates.copy(
            "core.py",
            package_path=path_to_core,
            package_filename=package_filename,
        )
        if self._db is not None:
            self._templates.copy("db.py", package_path=path_to_core)
            self._templates.copy(
                "model.py",
                package_path=path_to_core / "models",
                package_filename="example.py",
            )

        path_to_app = self.path / "app"
        self._templates.copy(
            "service.py",
            package_path=path_to_app / "services",
            package_filename=package_filename,
        )
        self._templates.copy(
            "schemas.py",
            package_path=path_to_app / "schemas",
            package_filename=package_filename,
        )

        route_file = "route.py" if self._db is None else "route_db.py"
        path_to_api = path_to_app / "api"
        self._templates.copy(
            route_file,
            package_path=path_to_api / "routes",
            package_filename=package_filename,
        )
        self._templates.copy("router.py", package_path=path_to_api)

        self._templates.copy("main.py")

    def setup_docker_compose(self):
        """
        Set up docker compose.

        Copy template and set container name.
        Set up dockerfile.
        Set up DB env variables in app service.
        Set app host env variable to db service name.
        """
        path_to_template = self._templates.get_filepath("docker-compose.yml")
        self._service.set_from_template(path_to_template)
        self._service.set_container_name(f"{self.name}_app")

        self._templates.copy("dockerfile")
        self._service.set_dockerfile("dockerfile")

        if isinstance(self._db, DockerDBSetup):
            self._service.update_env_vars(
                self._db.docker_env_vars.set_vars, user_service_var_names=False
            )

            host = self._db.docker_env_vars.host.model_copy()
            self._service.set_env_var(host.name, self._db.service_name)

    def _setup_subfolders(self):
        """
        Set up subfolders.

        app: app code (api, schemas, routers, serviecs)
        core: core logic/engine code
        """

        for subfolder in ["app", "core"]:
            os.makedirs(self.path / subfolder, exist_ok=True)

        os.makedirs(self.path / "core" / "models", exist_ok=True)

        for app_subfolder in ["api", "schemas", "services"]:
            os.makedirs(self.path / "app" / app_subfolder, exist_ok=True)

        os.makedirs(self.path / "app" / "api" / "routes", exist_ok=True)
