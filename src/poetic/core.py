from pathlib import Path
import shutil
from time import sleep

from poetic.factory import PoeticFactory
from poetic.logger import logg
from poetic.settings.options import SettingsOptions
from poetic.template.builder import TemplateBuilder


def launch(settings_dict: dict, path: Path | None = None, overwrite: bool = False):
    """
    Launch setup with given settings in given path.

    path: set up in given path; default (None) = tempalte name
    overwrite (bool): overwrite if package already exists
    """
    setup_settings = SettingsOptions(**{"settings": settings_dict}).settings
    poetic_factory = PoeticFactory()
    setupper = poetic_factory.build(setup_settings, path)

    if overwrite and setupper.path.exists():
        logg.warning(
            f"Removing directory in path {setupper.path} before setup in 5 seconds! Press Ctrl+C or stop test to cancel",
            important=True,
        )
        sleep(5)
        shutil.rmtree(setupper.path)
        logg.warning(f"Removed old directory in {setupper.path}", important=True)

    setupper.launch()


def update(path: Path | None = None):
    """
    Update existing template in given path.

    path: default None = current directory
    """
    template_builder = TemplateBuilder()
    setupper = template_builder.find(path)
    setupper.update()
