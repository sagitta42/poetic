from poetic.logger import logg
from poetic.settings.item import GitignoreSetupSettings
from poetic.setup.functionality import BaseFunctionalitySetup


class GitignoreSetup(BaseFunctionalitySetup[GitignoreSetupSettings]):
    """
    Gitignore file setup.
    """

    def setup(self) -> bool:
        """
        Set up .gitignore.

        Python .gitignore covering everything:
        https://github.com/github/gitignore/blob/main/Python.gitignore

        Return flag signifying it existed before.
        """
        super().setup()

        _, existed = self._copy_template(
            "Python.gitignore", package_filename=".gitignore", generic=True
        )
        return existed

    def display(self, suggest_commit: str | None = None):
        super().display(suggest_commit)
        logg.info("-> .gitignore")
