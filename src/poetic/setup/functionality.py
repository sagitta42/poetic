from abc import abstractmethod
from pathlib import Path
from typing import Any

from dotenv import set_key

from poetic.logger import logg
from poetic.settings.base import T_Settings
from poetic.setup.base import BaseSetup
from poetic.utils.readme import Readme
from poetic.utils.misc import POETIC_LINK


class BaseFunctionalitySetup(BaseSetup[T_Settings]):
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

    def __init__(self, path: Path, settings: T_Settings, core: bool) -> None:
        super().__init__(path, settings, core)

        self._readme = Readme(self.path)

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
        """
        self.global_setup()

        if self.git.is_git_repo:
            if self._settings.no_commit:
                self.display(self._commit_message("update"))
            else:
                self.git.commit_all(self._commit_message("setup"))
                self.display()
        else:
            self.display()

    def setup_dotenv_template(self):
        """
        Set up .env.template.
        """
        logg.info("...setting up .env template", header=True)
        self._update_env("DEBUG", 1)

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

    def _update_env(self, name: str, value: Any, path_to_dotenv: Path | None = None):
        """
        Update .env file with given variable value.

        Defaults to .env.template file in root directory of setup.

        .env file will be created if does not exist.
        """
        filepath = path_to_dotenv or self.path / ".env.template"

        set_key(filepath, name, str(value), quote_mode="never")
        logg.debug(f"{filepath} {name}={value}")

    def _commit_message(self, mod_type: str) -> str:
        """
        Suggested or utilized commit message.

        mod_type: e.g. setup/update
        """
        message = f"{self.title} {mod_type} with {POETIC_LINK}"
        return message
