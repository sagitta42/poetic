import os
from pathlib import Path

from poetic.command_runner import BaseCommandRunner
from poetic.utils.venv import Venv


class Poetry(BaseCommandRunner):
    def __init__(self, path: Path | None) -> None:
        super().__init__(path, command="poetry")

        self._venv = Venv(self.path)

    def init_basic(self, name: str | None = None):
        """
        Basic poetry init with no structure.
        """
        package_name = name or self.path.stem
        self.run(
            "init",
            "--no-interaction",
            "--name",
            package_name,
            "--description",
            "",
        )

    def add(self, *args, **kwargs):
        self.run("add", *args, **kwargs)

    def run(self, *args, **kwargs) -> list[str] | None:
        """
        Run a poetry command.

        A poetry call is outside of a venv of the project.
        It is called from the same environment in which poetic is installed and being used.

        """
        return super().run(
            *args,
            info=True,
            env={
                **os.environ,
                "POETRY_VIRTUALENVS_CREATE": "false",
                "VIRTUAL_ENV": self._venv.venv,
            },
            **kwargs,
        )
