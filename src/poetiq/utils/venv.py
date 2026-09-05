import os
from pathlib import Path
import venv

from poetiq.utils.command_runner import BaseCommandRunner
from poetiq.logger import logg
from poetiq.utils.misc import list_as_args


class Venv(BaseCommandRunner):
    def __init__(self, path: Path | None) -> None:
        super().__init__(path)

        self.venv = (self.path / "venv").resolve()

    def setup(self):
        if not self.venv.exists():
            logg.info("- creating venv")
            venv.create(self.venv, with_pip=True)

    def run(self, command: str, *args, **kwargs) -> list[str] | None:
        """
        Run a venv-based command with given arguments.

        Invoke path/to/venv/command.
        """
        return super().run(
            self.exe(command),
            *args,
            env={
                **os.environ,
                "VIRTUAL_ENV": self.venv,
            },
            **kwargs,
        )

    def exe(self, exe: str) -> Path:
        """
        Get venv path to executable.
        """
        ret = self.venv / "bin" / exe
        return ret
