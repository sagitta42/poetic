from abc import abstractmethod
import os
from pathlib import Path

from poetic.exceptions import PoeticException
from poetic.item.gitignore import GitignoreSetup
from poetic.item.vscode import VSCodeSetup
from poetic.logger import logg
from poetic.settings.base import T_Settings
from poetic.setup.venv import BaseVenvSetup
from poetic.utils.path import File
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
            self.git.run("init")

    def setup(self) -> None:
        """
        Main setup.

        If no pyproject.toml found, do fresh init.
        (standalone setup rather than adding to existing)
        Consider name of directory in which setup is launched as project name.

        Set up dependencies.
        """

        super().setup()

        path_to_gitignore = self.path / ".gitignore"
        if not path_to_gitignore.exists():
            self._gitignore.setup()

        self.setup_dependencies()
        self._setup_poetic_toml()

    def _poetry_init(self):
        """
        Poetry init.

        Default poetry init for a poetry setup is basic init with no structure.
        """
        self._poetry_basic_init(self.path.stem)

    def _poetry_basic_init(self, name: str):
        """
        Basic poetry init with no structure.
        """
        self.run(
            "poetry",
            "init",
            "--no-interaction",
            "--name",
            name,
            "--description",
            "",
        )

    def _poetry_add(self, package: str, group: str | None = None):
        """
        Poetry add.

        Invoke poetry add in template's venv to install added package while adding to pyproject.toml
        """
        args = ["add", package]
        if group is not None:
            args += ["--group", group]

        self.poetry(*args)

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
