import os
from pathlib import Path
from send2trash import send2trash
from time import sleep

from poetic.factory import PoeticFactory
from poetic.action.install import InstallAction
from poetic.logger import logg
from poetic.settings.builder import SettingsBuilder
from poetic.settings.install import InstallSettings
from poetic.template.builder import TemplateBuilder
from poetic.utils.path import Dir
from poetic.utils.toml import PyProjectHandler


def launch(settings: dict, path: Path | None = None, overwrite: bool = False):
    """
    Launch setup with given settings in given path.

    path: set up in given path; default (None) = tempalte name
    overwrite (bool): overwrite if package already exists
    """
    settings_builder = SettingsBuilder()
    setup_settings = settings_builder.build_setup(settings)

    poetic_factory = PoeticFactory()
    setupper = poetic_factory.build(setup_settings, path)

    if overwrite and Dir(setupper.path).exists_and_non_empty():
        logg.warning(
            f"Cleaning directory in path {setupper.path} before setup in 5 seconds! Press Ctrl+C, or stop test to cancel",
            important=True,
        )
        sleep(5)
        for item in os.listdir(setupper.path):
            send2trash(setupper.path / item)

        logg.warning(
            f"Old contents of directory in {setupper.path} moved to trash",
            important=True,
        )

    setupper.launch()


def install(settings: dict, path: Path = Path.cwd()):
    install_action = InstallAction(path, InstallSettings(**settings))
    install_action.launch()


def update(path: Path = Path.cwd()):
    """
    Update existing template in given path.

    Read pyproject.toml settings.
    Combine them with provided settings.
    """
    template_path = path or Path.cwd()

    pyproject_handler = PyProjectHandler(template_path)
    pyproject_handler.read()
    settings_pyproject_dict = pyproject_handler.get_template_settings()

    settings_builder = SettingsBuilder()
    settings_pyproject = settings_builder.build_template(settings_pyproject_dict)

    template_builder = TemplateBuilder()
    setupper = template_builder.build(settings_pyproject, template_path)
    setupper.update()
