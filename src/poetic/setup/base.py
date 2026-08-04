from abc import abstractmethod
from importlib import resources
import json
import os
from pathlib import Path
import shutil
import subprocess
from typing import Generic, TypeVar
import venv

from poetic.settings import SetupSettings
from poetic.utils.git import Git

from poetic.logger import logg

T_Settings = TypeVar("T_Settings", bound=SetupSettings)


class BaseSetup(Generic[T_Settings]):
    """
    General setup of any kind.

    path (Path): path to root directory of setup

    Includes basic operations:
        - git control
        - copying templates
        - running subprocesses
        - venv setup
        - setting up dependencies with poetry
        - .env template setup

    NOTE: does not include venv or poetry setup
    """

    def __init__(self, settings: T_Settings, path: Path) -> None:
        self._settings = settings
        self.path = path

        self._type: str = settings.type.value
        # FIXME: changes if source file folder depth does
        self._path_to_resources = Path(__file__).resolve().parent.parent
        # TODO: try to use resources - Path() does not convert MultiplexedPath
        # self._path_to_resources = Path(resources.files(__package__).__str__()).parent
        self._path_to_templates = self._path_to_resources / "templates"
        self._path_to_type_templates = self._path_to_templates / self._type

        self._path_to_venv = (self.path / "venv").resolve()

        self.git = Git(self.path)

    def setup(self, skip_super: bool = False) -> None:
        """
        Main setup.

        skip_super: do not perform superclass setup
            (e.g. to skip for "assistive" internal setups)
        """
        # FIXME: improve
        self.setup_dotenv_template()
        self.setup_venv()
        self.setup_dependencies()

    def setup_dotenv_template(self) -> Path:
        """
        Set up .env.template.

        Return path to template.
        """
        return self._copy_template(
            "env.template", package_filename=".env.template", generic=True
        )

    def setup_venv(self):
        """
        Set up venv.

        Create venv.
        Install poetry into that venv.
        """
        if not self._path_to_venv.exists():
            venv.create(self._path_to_venv, with_pip=True)
        self._run(self.venv("pip"), "install", "poetry", env=True)

    @abstractmethod
    def setup_dependencies(self) -> None:
        pass

    def _copy_template(
        self,
        template_filename: str,
        path_in_package: Path | None = None,
        package_filename: str | None = None,
        template_subdir: Path | str | None = None,
        generic: bool = False,
    ) -> Path:
        """
        Copy template into package source code if does not yet exist.

        template_filename (str): name of template to copy contained under templates of this package
        generic (bool): template is generic (independent of setup type)
        path_in_package (Path | None): path where to copy in package; default = root path
        package_filename (str | None): filename of template in package; default = same as original template

        Returns path to file in package.
        """
        path_in_package = path_in_package or self.path
        package_filename = package_filename or template_filename
        path_to_package_file = path_in_package / package_filename

        path_to_template = self._get_template_path(
            template_filename, generic, template_subdir=template_subdir
        )

        shutil.copy(path_to_template, path_to_package_file)

        return path_to_package_file

    def _get_template_path(
        self, template_filename: str, generic: bool, template_subdir: Path | str | None
    ) -> Path:
        """
        Get path given template.
        """
        path_to_templates = (
            self._path_to_templates if generic else self._path_to_type_templates
        )
        if template_subdir is not None:
            path_to_templates = path_to_templates / template_subdir

        ret = path_to_templates / template_filename
        return ret

    def _poetry_add(self, package: str, group: str | None = None):
        """
        Poetry add.

        Invoke poetry add in template's venv to install added package while adding to pyproject.toml
        """
        args = [self.venv("poetry"), "add"]
        if group is not None:
            args += ["--group", group]
        args.append(package)

        self._run(*args, env=True)

    def _run(self, *args, env: bool = False):
        """
        Run command in template root directory.
        """
        subprocess.run(
            args,
            cwd=self.path,
            env=(
                {
                    **os.environ,
                    "POETRY_VIRTUALENVS_CREATE": "false",
                    "VIRTUAL_ENV": self._path_to_venv,
                }
                if env
                else None
            ),
        )

    def _add_vscode_launch_configurations(self, template_filename: str):
        """
        Add configurations to VSCode launch.json contained in given template.
        """
        path_to_launch = self.path / ".vscode" / "launch.json"
        if not path_to_launch.exists():
            return

        with open(path_to_launch) as f:
            launch_dct = json.load(f)

        path_to_template = self._get_template_path(
            template_filename, generic=False, template_subdir="alembic"
        )
        with open(path_to_template) as f:
            template_config = json.load(f)

        configuration_names = [
            config["name"] for config in launch_dct["configurations"]
        ]

        for config in template_config["configurations"]:
            if config["name"] not in configuration_names:
                launch_dct["configurations"].append(config)

        with open(path_to_launch, "w") as f:
            json.dump(launch_dct, f, indent=4)

    def venv(self, exe: str) -> Path:
        """
        Get venv path to executable.
        """
        ret = self._path_to_venv / "bin" / exe
        return ret
