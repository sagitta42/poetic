import os
from pathlib import Path
import shutil

from poetic.base import Template


class PackageTemplate(Template):
    _TYPE: str = "package"

    def __init__(self, name: str) -> None:
        super().__init__(name)

        self._path_to_src: Path = self.path / "src" / self._inner_name

    def poetry_init(self):
        """
        Initialize package with poetry.

        Standard setup with src/package_name structure.
        """
        os.system(f"poetry new {self.name}")

    def setup_source_files(self):
        """
        Set up source files.

        Set up core.py: contains core routines to be imported directly from package.
        Create a dummy source file (convenient for tests)
        Set up py.typed enabling package imports.
        """
        self._create_source_file("core.py")

        with open(self._path_to_src / "__init__.py", "a") as f:
            f.write(f"from {self._inner_name}.core import *")

        self._copy_template("foo.py", path_in_package=self._path_to_src)

        self._create_source_file("py.typed")

    def setup_extra(self):
        """
        Additional setup.
        """
        self.setup_tests()
        self.setup_logger()

    def setup_tests(self):
        """
        Set up tests.

        Create conftest.py that allows testing in dev mode without installing the package.
        Create dummy test corresponding to the dummy source file.
        Add pytest as dev dependency.
        """
        path_to_tests: Path = self.path / "tests"

        self._copy_template("conftest.py", path_to_tests)

        with open(self._path_to_type_templates / "test_foo.py") as f:
            test_foo_lines = f.readlines()
        test_foo_lines[0] = test_foo_lines[0].replace("$PACKAGE", self._inner_name)
        with open(path_to_tests / "test_foo.py", "w") as f:
            f.writelines(test_foo_lines)

        self._poetry_add("pytest", "dev")

    def setup_logger(self):
        shutil.copy(
            self._path_to_resources / "logger.py", self._path_to_src / "logger.py"
        )

    def _create_source_file(self, filepath: str | Path):
        """
        Create empty source file with given name or path.
        """
        f = open(self._path_to_src / filepath, "w")
        f.close()
