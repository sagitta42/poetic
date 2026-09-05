from pathlib import Path

from poetiq.logger import logg
from poetiq.settings.setup import GitignoreSetupSettings
from poetiq.setup.base.functionality import BaseFunctionalitySetup
from poetiq.utils.path import File
from poetiq.utils.template import TemplateLocation


class GitignoreSetup(BaseFunctionalitySetup[GitignoreSetupSettings]):
    """
    Gitignore file setup.
    """

    def __init__(
        self,
        path: Path,
        settings: GitignoreSetupSettings = GitignoreSetupSettings(),
        core: bool = False,
    ) -> None:
        super().__init__(path, settings, core)

        self._file = ".gitignore"
        self._path_to_file = self.path / self._file

    def setup(self) -> None:
        """
        Set up .gitignore.

        Python .gitignore covering everything:
        https://github.com/github/gitignore/blob/main/Python.gitignore
        """
        super().setup()

        self._setup_gitignore()

    def display(self, suggest_commit: str | None = None):
        super().display(suggest_commit)
        logg.info("-> .gitignore")

    def _setup_gitignore(self):
        """
        Set up standard python gitignore.

        If .gitignore does not exist, simply copy the template.
        Otherwise add lines missing in existing gitignore.
        """

        if not self._path_to_file.exists():
            self._templates.copy(
                self._file, template_location=TemplateLocation.poetiq_build
            )
            return

        gitignore_file = File(self._path_to_file)
        path_to_template = self._templates.get_filepath(
            self._file, template_location=TemplateLocation.poetiq_build
        )
        gitignore_template = File(path_to_template)

        for line in gitignore_template.lines:
            gitignore_file.add_new_line(line)
