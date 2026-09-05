from abc import abstractmethod
from pathlib import Path

from poetiq.exceptions import PoetiqException
from poetiq.logger import logg
from poetiq.settings.base import T_SetupSettings
from poetiq.setup.base import BaseSetup
from poetiq.utils.env import DotEnv
from poetiq.utils.path import File
from poetiq.utils.readme import Readme
from poetiq.utils.misc import POETIQ_LINK


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

    def __init__(
        self, path: Path | None, settings: T_SetupSettings, core: bool
    ) -> None:
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
        Add "made with poetiq" at the end of readme if does not exist.
        """
        super().launch()
        
        self._check_for_changes()

        self.setup()

        self._add_poetiq_line()

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
        logg.info(f"- setting up {self.title} .env template")
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

    def _add_poetiq_line(self):
        self._readme.add_poetiq_line(prep="using")

    def _check_for_changes(self):
        if self._git.is_git_repo and self._git.has_uncommitted_changes:
            raise PoetiqException(
                f"Repository {self.path} has uncommitted changes! Commit or stash before proceeding with {self._type} setup."
            )

    def _commit_message(self, mod_type: str) -> str:
        """
        Suggested or utilized commit message.

        mod_type: e.g. setup/update
        """
        message = f"{self.title} {mod_type} with {POETIQ_LINK}"
        return message
