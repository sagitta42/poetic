from abc import abstractmethod
from pathlib import Path

from poetiq.item.vscode import VSCodeSetup
from poetiq.logger import logg
from poetiq.settings.base import T_SetupSettings
from poetiq.setup.venv import BaseVenvSetup
from poetiq.utils.pip import Pip
from poetiq.utils.poetry import Poetry
from poetiq.utils.toml import PyProjectHandler


class BasePoetrySetup(BaseVenvSetup[T_SetupSettings]):
    """
    General functionality setup with poetry dependencies.

    core (bool): this is a core setup (impacts only cosmetics e.g. info header)

    Includes additional operations:
        - set up poetry
        - set up dependencies with poetry
    """

    def __init__(
        self, path: Path | None, settings: T_SetupSettings, core: bool
    ) -> None:
        super().__init__(path, settings, core)

        self._vscode = VSCodeSetup(self.path, core=False)
        self._pyproject_handler = PyProjectHandler(self.path)
        self._poetry = Poetry(self.path)
        self._pip = Pip(self.path)

    @abstractmethod
    def setup_dependencies(self) -> None:
        """
        Set up dependencies.

        Set up poetry into current environment.
            (the one from which poetiq is run, not project's venv)
        """
        logg.info(f"- setting up dependencies for {self._type.value}")

    def launch(self) -> None:
        """
        Launch procedure for dependency setup.

        Initialize repository if necessary.
        Since launch() is used for independent functionality setup,
            it may be done in an already existing git repository
            with existing poetry setup.
            Do not initialize if already present.

        Proceed with further setup.
        """
        self.init()

        super().launch()

    def init(self):
        """
        Initialize setup.

        Initialize poetry.
        Initialize git.
        """
        if not self._pyproject_handler.path.exists():
            self._poetry_init()

        if not self._git.is_git_repo:
            self._git.run("init", info=True)

    def setup(self) -> None:
        """
        Main setup.

        If no pyproject.toml found, do fresh init.
        (standalone setup rather than adding to existing)
        Consider name of directory in which setup is launched as project name.

        Set up dependencies.
        """

        super().setup()

        self.setup_dependencies()

        self._gitignore_file.add_new_line("__pycache__")

    def _poetry_init(self):
        """
        Poetry init.

        Default poetry init for a poetry setup is basic init with no structure.
        """
        self._poetry.init_basic()

    def _poetry_add(self, package: str, group: str | None = None):
        """
        Poetry add.

        Invoke poetry add in template's venv to install added package while adding to pyproject.toml
        """
        args = [package]
        if group is not None:
            args += ["--group", group]

        self._poetry.add(*args)
