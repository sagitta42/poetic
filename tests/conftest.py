import json
from pathlib import Path
import pytest
import sys
import os

from dotenv import dotenv_values

from poetic.settings.options import AcceptedSetupSettings, SettingsOptions
from poetic.settings.template import BaseTemplateSettings

env_config = dotenv_values()
is_debug = env_config.get("DEBUG", "").lower() in ("true", "1")
test_eann = env_config.get("TEST_EANN", "").lower() in ("true", "1")

if is_debug:
    path_current = os.path.dirname(__file__)
    # make src modules accessible in all test_* files without having to install the package
    path_to_src = os.path.join(path_current, "..", "src")
    path_to_src_absolute = os.path.abspath(path_to_src)
    sys.path.insert(0, path_to_src_absolute)

PATH_TO_ASSETS = Path(os.path.dirname(__file__))
PATH_TO_CONFIGS = PATH_TO_ASSETS / "configs"


def get_setup_settings(filename: str) -> AcceptedSetupSettings:
    """
    Get setup settings from given config filename (with extension).
    """
    filepath = PATH_TO_CONFIGS / filename
    with open(filepath) as f:
        settings = SettingsOptions(**{"settings": json.load(f)}).settings
    return settings


def create_setup_test_cases(filenames: list[str] | None = None):
    """
    Create setup test cases based on given config filenames (with extension).

    If no names given, use all test configs.
    """
    config_filenames = filenames or os.listdir(PATH_TO_CONFIGS)

    ret = []
    for fname in config_filenames:
        settings = get_setup_settings(fname)
        ret.append(pytest.param(settings, id=Path(fname).stem))
    return ret


@pytest.fixture(params=create_setup_test_cases())
def test_case_template(request) -> AcceptedSetupSettings:
    return request.param
