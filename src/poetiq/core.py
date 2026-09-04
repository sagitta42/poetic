import os
from pathlib import Path
from send2trash import send2trash
from time import sleep

from poetiq.factory import PoetiqFactory
from poetiq.action.install import InstallAction
from poetiq.logger import logg
from poetiq.settings.poetiq_action import InstallSettings
from poetiq.settings.builder import SettingsBuilder
from poetiq.template.base import BaseTemplate
from poetiq.utils.path import Dir
from poetiq.utils.toml import PyProjectHandler


def launch_action(settings: dict, path: Path | None = None, overwrite: bool = False):
    """
    Launch action with given settings in given path.

    path: set up in given path; default (None) = tempalte name
    overwrite (bool): overwrite if package already exists
    """
    settings_builder = SettingsBuilder()
    action_settings = settings_builder.build_action(settings)

    poetiq_factory = PoetiqFactory()
    action = poetiq_factory.build(action_settings, path)

    if overwrite and Dir(action.path).exists_and_non_empty():
        logg.warning(
            f"Cleaning directory in path {action.path} before setup in 5 seconds! Press Ctrl+C, or stop test to cancel",
            important=True,
        )
        sleep(5)
        for item in os.listdir(action.path):
            send2trash(action.path / item)

        logg.warning(
            f"Old contents of directory in {action.path} moved to trash",
            important=True,
        )

    action.launch()


# TODO: move to tests?
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

    poetiq_factory = PoetiqFactory()
    template = poetiq_factory.build(settings_pyproject, path)
    assert isinstance(template, BaseTemplate)
    template.update()
