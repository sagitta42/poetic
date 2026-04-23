from importlib import resources
import os
from pathlib import Path
import shutil


class PackageSetup:
    def __init__(self, package_name: str) -> None:
        self._package_name = package_name
        self.path = Path(self._package_name)

        print(f"Setting up package: {self._package_name}")
        os.system(f"poetry new {self._package_name}")

        self._path_to_src: Path = self.path / "src" / self._package_name
        self._path_to_templates: Path = (
            Path(resources.files(__package__).__str__()) / "templates"
        )

    def setup_source_files(self):
        """
        Set up source files.

        Set up core.py: contains core routines to be imported directly from package.
        Create a dummy source file (convenient for tests)
        """
        f = open(self._path_to_src / "core.py", "w")
        f.close()

        with open(self._path_to_src / "__init__.py", "a") as f:
            f.write("from core import *")

        shutil.copy(self._path_to_templates / "foo.py", self._path_to_src / "foo.py")
