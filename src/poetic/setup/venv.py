from abc import abstractmethod
import os
from pathlib import Path
import venv

from poetic.command_runner import BaseCommandRunner
from poetic.logger import logg
from poetic.settings.base import T_Settings
from poetic.setup.functionality import BaseFunctionalitySetup
from poetic.utils.utils import list_as_args


class BaseVenvSetup(BaseFunctionalitySetup[T_Settings], BaseCommandRunner):
    """
    General functionality setup with venv.

    Includes additional operations:
        - running subprocesses
        - venv setup
    """

    def __init__(self, path: Path, settings: T_Settings) -> None:
        BaseFunctionalitySetup.__init__(self, path, settings)
        BaseCommandRunner.__init__(self, path)

        self._path_to_venv = (self.path / "venv").resolve()

    @abstractmethod
    def setup_dependencies(self) -> None:
        logg.info("...setting up dependencies", header=True)
        self.pip("install", "poetry", env=True)

    def setup(self) -> None:
        """
        Main setup.

        Additional setup: set up venv
        """
        super().setup()

        self.setup_venv()

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

    def pip(self, *args, env: bool = False):
        """
        Run a pip command in project's venv.
        """
        self._venv_command("pip", *args, env=env)

    def poetry(self, *args):
        """
        Run a poetry command in project's venv.
        """
        # TODO: should it use venv poetry or global poetry (same env as poetic itself)?
        self._venv_command("poetry", *args, env=True)

    def _venv_command(self, command: str, *args, env: bool = False):
        """
        Run a venv-based command with given arguments.

        Invoke path/to/venv/command.
        """
        logg.info(f"poetic: {command} {list_as_args(args)}", header=True)
        self.run(self.venv(command), *args, env=env)

    def run(self, *args, check: bool = False, env: bool = False) -> list[str] | None:
        """
        Run command in template root directory.

        env (bool): run with environment variables.
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
