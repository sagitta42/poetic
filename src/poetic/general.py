from importlib import resources
from pathlib import Path
import shutil

from poetic.logger import logg
from poetic.tree import tree

PATH_TO_RESOURCES = Path(resources.files(__package__).__str__())
PATH_TO_TEMPLATES: Path = PATH_TO_RESOURCES / "templates"


class GeneralSetup:
    _TYPE: str

    def __init__(self, name: str) -> None:
        self.name = name
        self._inner_name = self.name.replace("-", "_")
        self.path = Path(self.name)
        self._path_to_src = self.path

        logg.info(f"Setting up {self._TYPE}: {self.name}")

    def setup_gitignore(self):
        """
        Set up .gitignore.

        Python .gitignore covering everything:
        https://github.com/github/gitignore/blob/main/Python.gitignore
        """
        self._copy_template("Python.gitignore", self.path, ".gitignore")

    def setup_dotenv_template(self):
        """
        Set up .env.template
        """
        self._copy_template(".env.template", self.path)

    def display(self):
        logg.info(self.name)
        for line in tree(self.path):
            logg.info(line)

    def _copy_template(
        self,
        template_filename: str,
        path_in_package: Path | None = None,
        package_filename: str | None = None,
    ):
        path_in_package = path_in_package or self._path_to_src
        package_filename = package_filename or template_filename
        shutil.copy(
            PATH_TO_TEMPLATES / template_filename,
            path_in_package / package_filename,
        )
