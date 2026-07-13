import os
from pathlib import Path
import subprocess

from dulwich import F

from poetic.general import GeneralSetup
from poetic.pyproject_handler import PyProjectHandler


class APISetup(GeneralSetup):
    _TYPE: str = "API"

    def __init__(self, name: str) -> None:
        super().__init__(name)

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
            cwd=name,
        )

        pyproject_handler = PyProjectHandler(self.path)
        pyproject_handler.add_section("tool.poetry", {"package-mode": False})
        pyproject_handler.del_section("build-system")
        pyproject_handler.save_toml()

    def setup_subfolders(self):
        """
        Set up subfolders.

        app: app code
        code: code logic/engine code
        """

        for subfolder in ["app", "core"]:
            os.mkdir(self.path / subfolder)

        for app_subfolder in ["api", "schemas", "services"]:
            os.mkdir(self.path / "app" / app_subfolder)

        os.mkdir(self.path / "app" / "api" / "routes")
