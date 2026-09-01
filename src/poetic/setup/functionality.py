from abc import abstractmethod
from pathlib import Path

from poetic.exceptions import PoeticException
from poetic.logger import logg
from poetic.settings.setup import T_SetupSettings
from poetic.setup.base import BaseSetup
from poetic.utils.env import DotEnv
from poetic.utils.path import File
from poetic.utils.readme import Readme
from poetic.utils.misc import POETIC_LINK


class BaseFunctionalitySetup(BaseSetup[T_SetupSettings]):
    """
    General setup for functionalities.

    Set up individual functionality:
    - as part of a template: via setup()
    - as an independent setup: via launch()

    Standard launch action:
    - set up
    - if git repo, commit changes unless requested otherwise
    - display setup results

    Included setup:
        - readme setup
        - .env template setup and update
    """

    def __init__(self, path: Path, settings: T_SetupSettings, core: bool) -> None:
        super().__init__(path, settings, core)

        self._readme = Readme(self.path)
        self._env = DotEnv(self.path)
        self._gitignore_file = File(self.path / ".gitignore")

    @abstractmethod
    def setup(self) -> None:
        """
        Main setup.

        Set up README.
        """
        super().setup()

        self.setup_readme()

    def launch(self) -> None:
        """
        Launch independent functionality setup.

        Perform global setup.
        Commit setup if in git repository and files did not exist before.
        Add "made with poetic" at the end of readme if does not exist.
        """
        if self._git.is_git_repo and self._git.has_uncommitted_changes:
            raise PoeticException(
                f"Repository {self.path} has uncommitted changes! Commit or stash before proceeding with {self._type.value} setup."
            )

        self.setup()

        self._add_poetic_line()

        if self._git.is_git_repo:
            if self._settings.no_commit:
                self.display(self._commit_message("update"))
            else:
                self._git.commit_all(self._commit_message("setup"))
                self.display()
        else:
            self.display()

    def setup_dotenv_template(self):
        """
        Set up .env.template.
        """
        logg.info("...setting up .env template", header=True)
        self._env.set("DEBUG", 1)
        self._gitignore_file.add_new_line(".env", prepend=True)

    def setup_readme(self):
        """
        Set up README.md
        """
        pass

    def display(self, suggest_commit: str | None = None):
        """
        Display setup.

        suggest_commit: suggest commit message
        """
        if suggest_commit is not None:
            logg.info(f"[not committed] {suggest_commit}")
        else:
            logg.info(f"{self.title} functionality setup DONE")

    def _add_poetic_line(self):
        self._readme.add_poetic_line(prep="using")

    def _commit_message(self, mod_type: str) -> str:
        """
        Suggested or utilized commit message.

        mod_type: e.g. setup/update
        """
        message = f"{self.title} {mod_type} with {POETIC_LINK}"
        return message
