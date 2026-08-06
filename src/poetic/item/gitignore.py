from pathlib import Path

from poetic.logger import logg
from poetic.settings.item import GitignoreSetupSettings
from poetic.setup.functionality import BaseFunctionalitySetup


class GitignoreSetup(BaseFunctionalitySetup[GitignoreSetupSettings]):
    """
    Gitignore file setup.
    """

    def __init__(
        self, path: Path, settings: GitignoreSetupSettings = GitignoreSetupSettings()
    ) -> None:
        super().__init__(path, settings)

    def setup(self) -> None:
        """
        Set up .gitignore.

        Python .gitignore covering everything:
        https://github.com/github/gitignore/blob/main/Python.gitignore
        """
        super().setup()

        self._copy_template(
            "Python.gitignore", package_filename=".gitignore", generic=True
        )

    def display(self, suggest_commit: str | None = None):
        super().display(suggest_commit)
        logg.info("-> .gitignore")
