from abc import abstractmethod
from pathlib import Path
import shutil
from typing import Any, Generic

import yaml

from poetic.settings.base import T_Settings
from poetic.utils.git import Git

from poetic.logger import logg


class BaseSetup(Generic[T_Settings]):
    """
    General setup of any kind.

    path (Path): path to root directory of setup

    Main procedures:
        - setup: defines setup of folders, files etc.
        - launch: defines actions to be done if setup is launched

    Includes basic operations:
        - git control
        - copying templates
    """

    def __init__(self, path: Path, settings: T_Settings) -> None:
        self._settings = settings
        logg.debug(settings)
        self.path = path

        self._type: str = settings.type.value

        # FIXME: changes if source file folder depth does
        self._path_to_resources = Path(__file__).resolve().parent.parent
        # TODO: try to use resources - Path() does not convert MultiplexedPath
        # self._path_to_resources = Path(resources.files(__package__).__str__()).parent
        self._path_to_templates = self._path_to_resources / "assets"
        self._path_to_type_templates = self._path_to_templates / self._type

        self.git = Git(self.path)

        self._poetic_link = "[poetic](https://github.com/sagitta42/poetic)"

    @property
    def docker_compose(self) -> Path:
        """
        Default path to docker-compose.yml
        """
        return self.path / "docker-compose.yml"

    @abstractmethod
    def setup(self) -> bool | None:
        """
        Main setup.

        Optionally return a flag representing whether this setup existed before.
        """
        pass

    @abstractmethod
    def launch(self) -> None:
        """
        Launch action of this setup
        """
        pass

    def _copy_template(
        self,
        template_filename: str,
        path_in_package: Path | None = None,
        package_filename: str | None = None,
        template_subdir: Path | str | None = None,
        generic: bool = False,
    ) -> tuple[Path, bool]:
        """
        Copy template into package source code.

        template_filename (str): name of template to copy contained under templates of this package
        generic (bool): template is generic (independent of setup type)
        path_in_package (Path | None): path where to copy in package; default = root path
        package_filename (str | None): filename of template in package; default = same as original template

        Returns path to file in package and whether it existed before.
        """
        package_filename = package_filename or template_filename
        path_in_package = path_in_package or self.path

        path_to_package_file = self._get_filepath_in_package(
            package_filename, path_in_package
        )

        existed_before = path_to_package_file.exists()

        path_to_template = self._get_template_path(
            template_filename, generic, template_subdir=template_subdir
        )

        logg.debug(f"Copying {path_to_template} -> {path_to_package_file}")
        shutil.copy(path_to_template, path_to_package_file)

        return path_to_package_file, existed_before

    def _package_file_exists(
        self,
        filename_in_package: str,
        path_in_package: Path | None = None,
    ) -> bool:
        """
        Check if file already exists in package.

        filename_in_package (str | None): filename in package
        path_in_package (Path | None): file path in package; default = root path
        """
        filepath = self._get_filepath_in_package(filename_in_package, path_in_package)
        return filepath.exists()

    def _get_template_path(
        self,
        template_filename: str,
        generic: bool = False,
        template_subdir: Path | str | None = None,
    ) -> Path:
        """
        Get path to given template in assets.
        """
        path_to_templates = (
            self._path_to_templates if generic else self._path_to_type_templates
        )
        if template_subdir is not None:
            path_to_templates = path_to_templates / template_subdir

        ret = path_to_templates / template_filename
        return ret

    def _get_filepath_in_package(
        self,
        filename_in_package: str,
        path_in_package: Path | None = None,
    ) -> Path:
        """
        Get destination path of file in package being set up.

        filename_in_package (str | None): filename in package
        path_in_package (Path | None): file path in package; default = root path
        """
        path_in_package = path_in_package or self.path
        ret = path_in_package / filename_in_package
        return ret

    def _update_docker_compose_from_template(
        self, path_to_template: Path, path_to_docker_compose: Path | None = None
    ):
        """
        Update given docker-compose .yml file with contents of given template.

        Default to docker-compose.yml in root of setup.
        Create file if does not exist yet.
        """
        yml_info = self._get_docker_compose(path_to_docker_compose)

        with open(path_to_template) as f:
            yml_template = yaml.safe_load(f)

        yml_info["services"] |= yml_template["services"]

        self._write_docker_compose(yml_info, path_to_docker_compose)

    def _get_docker_compose(
        self, path_to_docker_compose: Path | None = None
    ) -> dict[str, Any]:
        """
        Get docker-compose from given path to .yml.

        If does not exist, set up empty "services" in dict.
        """
        path_to_yml = path_to_docker_compose or self.docker_compose

        yml_info = {}
        if path_to_yml.exists():
            with open(path_to_yml) as f:
                yml_info = yaml.safe_load(f)

        if "services" not in yml_info:
            yml_info["services"] = {}

        return yml_info

    def _write_docker_compose(
        self, yml_info: dict[str, Any], path_to_docker_compose: Path | None = None
    ):
        # FIXME: improve duplication
        path_to_yml = path_to_docker_compose or self.docker_compose
        with open(path_to_yml, "w") as f:
            yaml.dump(yml_info, f)
