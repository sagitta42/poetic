from pathlib import Path

from poetic.item.vscode import VSCodeSetup
from poetic.logger import logg
from poetic.settings.base import T_Settings
from poetic.setup.venv import BaseVenvSetup


class BaseDependencySetup(BaseVenvSetup[T_Settings]):
    """
    General functionality setup with dependencies.

    core (bool): this is a core setup (impacts only cosmetics e.g. info header)

    Includes additional operations:
        - setting up dependencies with poetry
    """

    def __init__(self, path: Path, settings: T_Settings, core: bool) -> None:
        super().__init__(path, settings)

        self._core = core

        self._vscode_setup = VSCodeSetup(self.path)

    def setup(self) -> None:
        """
        Main setup.
        """
        super().setup()

        line = "-" * 60
        if self._core:
            logg.info(line, header=True)
        super().setup()
        if self._core:
            logg.info(line, header=True)

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
