from abc import abstractmethod
import json
import os
from pathlib import Path
import subprocess
from typing import Any
import venv

from dotenv import set_key

from poetic.item.vscode import VSCodeSetup
from poetic.logger import logg
from poetic.settings.base import T_Settings
from poetic.setup.functionality import BaseFunctionalitySetup


class BaseDependencySetup(BaseFunctionalitySetup[T_Settings]):
    """
    General functionality setup with dependencies.

    core (bool): this is a core setup (impacts only cosmetics e.g. info header)

    Includes additional operations:
        - running subprocesses
        - venv setup
        - setting up dependencies with poetry
        - .env template setup
    """

    def __init__(self, path: Path, settings: T_Settings, core: bool) -> None:
        super().__init__(path, settings)

        self._core = core
        self._path_to_venv = (self.path / "venv").resolve()

        self._vscode_setup = VSCodeSetup(self.path)

    @abstractmethod
    def setup_dependencies(self) -> None:
        logg.info("...setting up dependencies", header=True)
        self._run(self.venv("pip"), "install", "poetry", env=True)

    def setup(self) -> None:
        """
        Main setup.
        """
        line = "-" * 60
        if self._core:
            logg.info(line, header=True)
        super().setup()
        if self._core:
            logg.info(line, header=True)

        self.setup_dotenv_template()
        self.setup_venv()
        self.setup_dependencies()

    def setup_dotenv_template(self):
        """
        Set up .env.template.
        """
        logg.info("...setting up .env template", header=True)
        self._update_env("DEBUG", 1)

    def setup_venv(self):
        """
        Set up venv.

        Create venv if does not exist.
        Install poetry into that venv.
        """
        if not self._path_to_venv.exists():
            logg.info("...creating venv", header=True)
            venv.create(self._path_to_venv, with_pip=True)

    def venv(self, exe: str) -> Path:
        """
        Get venv path to executable.
        """
        ret = self._path_to_venv / "bin" / exe
        return ret

    def _poetry_add(self, package: str, group: str | None = None):
        """
        Poetry add.

        Invoke poetry add in template's venv to install added package while adding to pyproject.toml
        """
        args = [self.venv("poetry"), "add"]
        if group is not None:
            args += ["--group", group]
        args.append(package)

        self._run(*args, env=True)

    def _run(self, *args, env: bool = False):
        """
        Run command in template root directory.
        """
        subprocess.run(
            args,
            cwd=self.path,
            env=(
                {
                    **os.environ,
                    "POETRY_VIRTUALENVS_CREATE": "false",
                    "VIRTUAL_ENV": self._path_to_venv,
                }
                if env
                else None
            ),
        )

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

    def _update_env(self, name: str, value: Any, path_to_dotenv: Path | None = None):
        """
        Update .env file with given variable value.

        Defaults to .env.template file in root directory of setup.

        .env file will be created if does not exist.
        """
        filepath = path_to_dotenv or self.path / ".env.template"

        set_key(filepath, name, str(value), quote_mode="never")
