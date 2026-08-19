import os
from pathlib import Path
import subprocess
import venv

from poetic.logger import logg
from poetic.settings.base import T_Settings
from poetic.setup.functionality import BaseFunctionalitySetup


class BaseVenvSetup(BaseFunctionalitySetup[T_Settings]):
    """
    General functionality setup with venv.

    Includes additional operations:
        - running subprocesses
        - venv setup
    """

    def __init__(self, path: Path, settings: T_Settings) -> None:
        super().__init__(path, settings)
        self._path_to_venv = (self.path / "venv").resolve()

    def setup(self) -> None:
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
        self._run(self.venv("pip"), *args, env=env)

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
