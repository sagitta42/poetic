import os
from pathlib import Path
import shutil

from poetic.item.env_settings import EnvSettingsSetup
from poetic.settings.item import DotenvSettings, SetupType
from poetic.settings.template import PackageTemplateSettings
from poetic.template.base import BaseTemplate
from poetic.utils.utils import add_new_line_to_file


class PackageTemplate(BaseTemplate[PackageTemplateSettings]):

    def __init__(self, init: PackageTemplateSettings | str) -> None:
        settings = (
            init
            if isinstance(init, PackageTemplateSettings)
            else PackageTemplateSettings(
                name=init, type=SetupType.package, update=False
            )
        )
        super().__init__(settings)

        src_subdir = Path("src") / self._inner_name
        self._path_to_src: Path = self.path / src_subdir

        dotenv_settings = DotenvSettings(
            type=SetupType.dotenv, **self._settings.model_dump()
        )
        dotenv_settings.package_subdir = src_subdir
        self._dotenv_settings = (
            EnvSettingsSetup(dotenv_settings, self.path)
            if self._settings.settings
            else None
        )

    def poetry_init(self):
        """
        Initialize package with poetry.

        Standard setup with src/package_name structure.
        """
        super().poetry_init()
        # TODO: use subprocess
        os.system(f"poetry new {self.name}")

    def setup_source_files(self):
        """
        Set up source files.

        Set up core.py: contains core routines to be imported directly from package.
        Create a dummy source file (convenient for tests)
        Set up MyBaseModel.
        Set up py.typed enabling package imports.
        """
        self._create_source_file("core.py")

        add_new_line_to_file(
            self._path_to_src / "__init__.py", f"from {self._inner_name}.core import *"
        )

        self._copy_template("foo.py", path_in_package=self._path_to_src)

        source_file_path, _ = self._copy_template(
            "models.py",
            path_in_package=self._path_to_src,
            generic=True,
        )
        self._replace_package_placeholder(source_file_path)

        self._create_source_file("py.typed")

    def setup_dependencies(self):
        super().setup_dependencies()

        self._poetry_add("pytest", "dev")

    def setup(self, skip_super: bool = False):
        super().setup(skip_super)

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
        path_to_configs = path_to_tests / "configs"
        os.makedirs(path_to_configs, exist_ok=True)

        conftest_filepath, _ = self._copy_template("conftest.py", path_to_tests)
        self._replace_package_placeholder(conftest_filepath)

        self._copy_template("test_model.json", path_in_package=path_to_configs)

        test_unit_filepath, _ = self._copy_template(
            "test_unit.py", path_in_package=path_to_tests
        )
        self._replace_package_placeholder(test_unit_filepath)

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

    def _replace_package_placeholder(self, filepath: Path):
        """
        Replace $PACKAGE with package name in given source file.
        """
        with open(filepath) as f:
            source_file_lines = f.readlines()

        source_file_lines = [
            line.replace("$PACKAGE", self._inner_name) for line in source_file_lines
        ]

        with open(filepath, "w") as f:
            f.writelines(source_file_lines)
