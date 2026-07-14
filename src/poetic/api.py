import os
import subprocess


from poetic.general import GeneralTemplate
from poetic.pyproject_handler import PyProjectHandler


class APITemplate(GeneralTemplate):
    _TYPE: str = "api"

    def poetry_init(self):
        """
        Initialize package with poetry.

        Basic setup with only pyproject.toml.
        Disable package mode.
        """
        os.mkdir(self.name)
        subprocess.run(
            [
                "poetry",
                "init",
                "--no-interaction",
                "--name",
                self.name,
                "--description",
                "",
            ],
            cwd=self.name,
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

    def _setup_subfolders(self):
        """
        Set up subfolders.

        app: app code (api, schemas, serviecs)
        core: code logic/engine code
        """

        for subfolder in ["app", "core"]:
            os.mkdir(self.path / subfolder)

        for app_subfolder in ["api", "schemas", "services"]:
            os.mkdir(self.path / "app" / app_subfolder)

        os.mkdir(self.path / "app" / "api" / "routes")

    def setup_source_files(self):
        """
        Set up dummy source files
        """
        self._setup_subfolders()

        self._copy_template("config.py")
        self._copy_template("main.py")

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
