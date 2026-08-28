import os
from pathlib import Path

from poetic.core import install, launch, update

test_path = Path.cwd().parent / "poetic_test"


def test_launch(test_case_setup):
    """
    Test setup.

    Create directory in test path in case of functionality setup.
    """

    if not test_path.exists():
        os.mkdir(test_path)

    settings = test_case_setup.settings

    test_dir = test_path / test_case_setup.dir_name
    if not test_dir.exists():
        os.makedirs(test_dir)

    launch(settings, path=test_dir, overwrite=True)


def test_install(test_case_template):
    template_path = test_path / test_case_template.settings["name"]
    install({}, path=template_path)


def test_update(test_case_template):
    """
    Test template update.
    """
    if not test_path.exists():
        os.mkdir(test_path)

    update(path=test_path / test_case_template.settings["name"])
