from importlib import resources
import os
from pathlib import Path
import shutil
import subprocess
import venv


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

    def setup_gitignore(self):
        """
        Set up .gitignore.

        Python .gitignore covering everything:
        https://github.com/github/gitignore/blob/main/Python.gitignore
        """
        self._copy_template("Python.gitignore", self.path, ".gitignore")

    def setup_source_files(self):
        """
        Set up source files.

        Set up core.py: contains core routines to be imported directly from package.
        Create a dummy source file (convenient for tests)
        """
        f = open(self._path_to_src / "core.py", "w")
        f.close()

        with open(self._path_to_src / "__init__.py", "a") as f:
            f.write(f"from {self._package_name}.core import *")

        self._copy_template("foo.py")

    def setup_tests(self):
        """
        Set up tests.

        Create conftest.py that allows testing in dev mode without installing the package.
        Create dummy test corresponding to the dummy source file.
        Add pytest to package.
        Set up VSCode Testing suite.
        """
        path_to_tests: Path = self.path / "tests"

        self._copy_template("conftest.py", path_to_tests)

        with open(self._path_to_templates / "test_foo.py") as f:
            test_foo_lines = f.readlines()
        test_foo_lines[0] = test_foo_lines[0].replace("$PACKAGE", self._package_name)
        with open(path_to_tests / "test_foo.py", "w") as f:
            f.writelines(test_foo_lines)

        subprocess.run(
            ["poetry", "add", "--group", "dev", "pytest"],
            cwd=self.path,
            env={
                **os.environ,
                "PATH": str(self.venv / "bin") + ":" + os.environ["PATH"],
                "POETRY_VIRTUALENVS_CREATE": "false",
            },
        )

        path_to_vscode = self.path / ".vscode"
        os.mkdir(path_to_vscode)
        self._copy_template("VSCode.settings.json", path_to_vscode, "settings.json")

    def _copy_template(
        self,
        template_filename: str,
        path_in_package: Path | None = None,
        package_filename: str | None = None,
    ):
        path_in_package = path_in_package or self._path_to_src
        package_filename = package_filename or template_filename
        shutil.copy(
            self._path_to_templates / template_filename,
            path_in_package / package_filename,
        )

    @property
    def venv(self) -> Path:
        path_to_venv = self.path / "venv"
        if not os.path.exists(path_to_venv):
            venv.create(path_to_venv, with_pip=True)
            subprocess.run([path_to_venv / "bin" / "pip", "install", "poetry"])
        return path_to_venv
