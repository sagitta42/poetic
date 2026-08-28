from abc import abstractmethod
import os
from pathlib import Path
import subprocess

from poetic.item.gitignore import GitignoreSetup
from poetic.item.vscode import VSCodeSetup
from poetic.logger import logg
from poetic.settings.setup import T_Settings
from poetic.setup.venv import BaseVenvSetup
from poetic.utils.misc import find_line
from poetic.utils.path import File
from poetic.utils.pip import Pip
from poetic.utils.poetry import Poetry
from poetic.utils.template import TemplateLocation
from poetic.utils.toml import PyProjectHandler


class BasePoetrySetup(BaseVenvSetup[T_Settings]):
    """
    General functionality setup with poetry dependencies.

    core (bool): this is a core setup (impacts only cosmetics e.g. info header)

    Includes additional operations:
        - set up poetry
        - set up dependencies with poetry
    """

    def __init__(self, path: Path, settings: T_Settings, core: bool) -> None:
        super().__init__(path, settings, core)

        self._vscode = VSCodeSetup(self.path, core=False)
        self._gitignore = GitignoreSetup(self.path)
        self._pyproject_handler = PyProjectHandler(self.path)
        self._poetry = Poetry(self.path)
        self._pip = Pip(self.path)

    @abstractmethod
    def setup_dependencies(self) -> None:
        """
        Set up dependencies.

        Set up poetry into current environment.
            (the one from which poetic is run, not project's venv)
        """
        logg.info("...setting up dependencies", header=True)

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

        if not self.git.is_git_repo:
            self.git.run("init", info=True)

    def setup(self) -> None:
        """
        Main setup.

        If no pyproject.toml found, do fresh init.
        (standalone setup rather than adding to existing)
        Consider name of directory in which setup is launched as project name.

        Set up dependencies.
        """

        super().setup()

        self._gitignore.setup()

        self.setup_dependencies()
        self._setup_poetic_toml()

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

        try:
            self._poetry.add(*args, capture_output=True)
        except subprocess.CalledProcessError as e:
            if "EnvCommandError" in e.stdout:
                stdout_lines = e.stdout.split("\n")
                idx_process_error = find_line(stdout_lines, "CalledProcessError")
                logg.warning(
                    f"EnvCommandError when trying to run poetry add:", important=True
                )
                for line in stdout_lines[:idx_process_error]:
                    logg.warning(line)
                raise e

    def _setup_poetic_toml(self):
        """
        Setup poetic.toml template if does not exist.

        Set up poetic.toml.template file.
        Add poetic.toml to .gitignore.
        """
        path_to_toml = self.path / "poetic.toml.template"
        if not path_to_toml.exists():
            self._templates.copy(
                "poetic.toml.template", template_location=TemplateLocation.common_ass
            )

        File(self.path / ".gitignore").add_new_line("poetic.toml", prepend=True)
