import os
from pathlib import Path
import shutil
import subprocess
import venv

from poetic.general import GeneralSetup
from poetic.logger import logg


class PackageSetup(GeneralSetup):
    _TYPE: str = "package"

    def __init__(self, name: str) -> None:
        super().__init__(name)

        os.system(f"poetry new {self.name}")
        self._path_to_src: Path = self.path / "src" / self._inner_name

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

        self._copy_template("foo.py")

        self._create_source_file("py.typed")

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
        test_foo_lines[0] = test_foo_lines[0].replace("$PACKAGE", self._inner_name)
        with open(path_to_tests / "test_foo.py", "w") as f:
            f.writelines(test_foo_lines)

        self._poetry_add("pytest", "dev")

    def setup_vscode(self):
        path_to_vscode = self.path / ".vscode"
        os.mkdir(path_to_vscode)
        self._copy_template("VSCode.settings.json", path_to_vscode, "settings.json")
        self._copy_template("VSCode.launch.json", path_to_vscode, "launch.json")

    def setup_logger(self):
        shutil.copy(PATH_TO_RESOURCES / "logger.py", self._path_to_src / "logger.py")
        self._poetry_add("dotenv")

    def init_commit(self):
        subprocess.run(["git", "init"], cwd=self.path)
        stuff_to_commit = [
            "README.md",
            "src/",
            ".vscode/",
            ".gitignore",
            ".env.template",
            "pyproject.toml",
            "tests/",
        ]
        for stuff in stuff_to_commit:
            stuff_to_add = f"{stuff}*" if stuff.endswith("/") else stuff
            subprocess.run(["git", "add", stuff_to_add], cwd=self.path)
        subprocess.run(["git", "commit", "-am", "template"], cwd=self.path)

    def _poetry_add(self, package: str, group: str | None = None):
        args = ["poetry", "add"]
        if group is not None:
            args += ["--group", group]
        args.append(package)
        args.append("--lock")

        subprocess.run(
            args,
            cwd=self.path,
            env={
                **os.environ,
                "PATH": str(self.venv / "bin") + ":" + os.environ["PATH"],
                "POETRY_VIRTUALENVS_CREATE": "false",
            },
        )

    def _create_source_file(self, filepath: str | Path):
        """
        Create empty source file with given name or path.
        """
        f = open(self._path_to_src / filepath, "w")
        f.close()

    @property
    def venv(self) -> Path:
        path_to_venv = self.path / "venv"
        if not os.path.exists(path_to_venv):
            venv.create(path_to_venv, with_pip=True)
            subprocess.run([path_to_venv / "bin" / "pip", "install", "poetry"])
        return path_to_venv
