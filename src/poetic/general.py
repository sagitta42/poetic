from abc import ABC, abstractmethod
from importlib import resources
import os
from pathlib import Path
import shutil
import subprocess
import venv

from poetic.logger import logg
from poetic.tree import tree


class GeneralSetup(ABC):
    _TYPE: str

    def __init__(self, name: str) -> None:
        self.name = name
        self._inner_name = self.name.replace("-", "_")
        self.path = Path(self.name)

        self._path_to_resources = Path(resources.files(__package__).__str__())
        self._path_to_templates = self._path_to_resources / "templates"
        self._path_to_type_templates = self._path_to_templates / self._TYPE

        logg.info(f"Setting up {self._TYPE}: {self.name}")

    def setup_dependencies(self):
        self._poetry_add("dotenv")

    def setup_gitignore(self):
        """
        Set up .gitignore.

        Python .gitignore covering everything:
        https://github.com/github/gitignore/blob/main/Python.gitignore
        """
        self._copy_template("Python.gitignore", package_filename=".gitignore")

    def setup_dotenv_template(self):
        """
        Set up .env.template
        """
        self._copy_template(".env.template")

    def display(self):
        logg.info(self.name)
        for line in tree(self.path):
            logg.info(line)

    @abstractmethod
    def setup_source_files(self):
        """
        Set up source files.
        """
        pass

    def _copy_template(
        self,
        template_filename: str,
        path_in_package: Path | None = None,
        package_filename: str | None = None,
        generic: bool = True,
    ):
        """
        Copy template into package source code.

        template_filename (str): name of template to copy contained under templates of this package
        generic (bool): template is generic (independent of setup type)
        path_in_package (Path | None): path where to copy in package; default = root path
        package_filename (str | None): filename of template in package; default = same as original template
        """
        path_in_package = path_in_package or self.path
        package_filename = package_filename or template_filename

        path_to_templates = (
            self._path_to_templates if generic else self._path_to_type_templates
        )

        shutil.copy(
            path_to_templates / template_filename,
            path_in_package / package_filename,
        )

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

    @property
    def venv(self) -> Path:
        path_to_venv = self.path / "venv"
        if not os.path.exists(path_to_venv):
            venv.create(path_to_venv, with_pip=True)
            subprocess.run([path_to_venv / "bin" / "pip", "install", "poetry"])
        return path_to_venv
