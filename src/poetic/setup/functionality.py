from abc import abstractmethod

from poetic.logger import logg
from poetic.setup.base import BaseSetup, T_Settings


class BaseFunctionalitySetup(BaseSetup[T_Settings]):
    """
    General setup for functionalities.

    Set up individual functionality:
    - as part of a template: via setup()
    - as an independent setup: via launch()

    Standard launch action:
    - set up
    - if git repo and fresh setup, commit
    - otherwise only suggest commit message (need to pick desired changes)
    - display setup results
    """

    @property
    def title(self) -> str:
        """
        Functionality title
        """
        return self._settings.type.value

    @abstractmethod
    def setup(self) -> bool | None:
        logg.info(f"@ Setting up {self.title}", header=True)

    def launch(self) -> None:
        """
        Launch independent functionality setup.

        Perform setup.
        Commit setup if in git repository and files did not exist before.
        """
        existed_before = self.setup()
        assert existed_before is not None

        if self.git.is_git_repo:
            if not existed_before:
                self.git.commit_all(self._commit_message("setup"))
                self.display()
            else:
                self.display(self._commit_message("update"))
        else:
            self.display()

    def display(self, suggest_commit: str | None = None):
        """
        Display setup.

        suggest_commit: suggest commit message
        """
        if suggest_commit is not None:
            logg.info(suggest_commit)
        else:
            logg.info(f"{self.title} functionality setup")

    def _commit_message(self, mod_type: str) -> str:
        """
        Suggested or utilized commit message.

        mod_type: e.g. setup/update
        """
        message = f"{self.title} {mod_type} with {self._poetic_link}"
        return message
