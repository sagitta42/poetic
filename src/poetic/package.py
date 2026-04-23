from importlib import resources
import os
from pathlib import Path
import shutil
import subprocess
import venv

from poetic.logger import logg

PATH_TO_RESOURCES = Path(resources.files(__package__).__str__())
PATH_TO_TEMPLATES: Path = PATH_TO_RESOURCES / "templates"


class Package:
    def __init__(self, package_name: str) -> None:
        self._package_name = package_name
        self.path = Path(self._package_name)

        logg.info(f"Setting up package: {self._package_name}")
        os.system(f"poetry new {self._package_name}")

        self._path_to_src: Path = self.path / "src" / self._package_name

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

        with open(PATH_TO_TEMPLATES / "test_foo.py") as f:
            test_foo_lines = f.readlines()
        test_foo_lines[0] = test_foo_lines[0].replace("$PACKAGE", self._package_name)
        with open(path_to_tests / "test_foo.py", "w") as f:
            f.writelines(test_foo_lines)

        self._poetry_add("pytest", "dev")

        path_to_vscode = self.path / ".vscode"
        os.mkdir(path_to_vscode)
        self._copy_template("VSCode.settings.json", path_to_vscode, "settings.json")

    def setup_logger(self):
        shutil.copy(PATH_TO_RESOURCES / "logger.py", self._path_to_src / "logger.py")
        self._poetry_add("dotenv")

    def init_commit(self):
        subprocess.run(["git", "init"], cwd=self.path)
        subprocess.run(["git", "add", "*"], cwd=self.path)
        subprocess.run(["git", "commit", "-am", "template"], cwd=self.path)

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

    def _poetry_add(self, package: str, group: str | None = None):
        args = ["poetry", "add"]
        if group is not None:
            args += ["--group", group]
        args.append(package)

        subprocess.run(
            args,
            cwd=self.path,
            env={
                **os.environ,
                "PATH": str(self.venv / "bin") + ":" + os.environ["PATH"],
                "POETRY_VIRTUALENVS_CREATE": "false",
            },
        )

    @property
    def venv(self) -> Path:
        path_to_venv = self.path / "venv"
        if not os.path.exists(path_to_venv):
            venv.create(path_to_venv, with_pip=True)
            subprocess.run([path_to_venv / "bin" / "pip", "install", "poetry"])
        return path_to_venv
