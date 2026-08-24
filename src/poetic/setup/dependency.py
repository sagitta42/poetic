from abc import abstractmethod
import os
from pathlib import Path

from poetic.item.vscode import VSCodeSetup
from poetic.logger import logg
from poetic.settings.base import T_Settings
from poetic.setup.venv import BaseVenvSetup


class BaseDependencySetup(BaseVenvSetup[T_Settings]):
    """
    General functionality setup with poetry dependencies.

    core (bool): this is a core setup (impacts only cosmetics e.g. info header)

    Includes additional operations:
        - set up poetry
        - set up dependencies with poetry
    """

    def __init__(self, path: Path, settings: T_Settings, core: bool) -> None:
        super().__init__(path, settings)

        self._core = core

        self._path_to_venv = (self.path / "venv").resolve()
        self._vscode_setup = VSCodeSetup(self.path)

    @abstractmethod
    def setup_dependencies(self) -> None:
        """
        Set up dependencies.

        Set up poetry into current environment.
            (the one from which poetic is run, not project's venv)
        """
        logg.info("...setting up dependencies", header=True)

    def setup(self) -> None:
        """
        Main setup.

        In addition to previous setup:
            - set up poetry: install poetry in current environment (the one from which poetic is launched)
            - set up dependencies
        """
        super().setup()

        line = "-" * 60
        if self._core:
            logg.info(line, header=True)
        super().setup()
        if self._core:
            logg.info(line, header=True)

        self.run("pip", "install", "poetry (>=2.0.0,<3.0.0)", env=True)
        self.setup_dependencies()

    def _poetry_add(self, package: str, group: str | None = None):
        """
        Poetry add.

        Invoke poetry add in template's venv to install added package while adding to pyproject.toml
        """
        args = ["add", package]
        if group is not None:
            args += ["--group", group]

        self.poetry(*args)

    def poetry(self, *args):
        """
        Run a poetry command adding to project's venv.

        Poetry is envoked from current environment (one in which poetic is run)
            rather than project's venv.
        """
        self.run("poetry", *args, env=True)

    def run(self, *args, check: bool = False, env: bool = False) -> list[str] | None:
        """
        Run command in template root directory.

        env (bool): run with poetry/venv environment variables.
        """
        return super().run(
            *args,
            check=check,
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
