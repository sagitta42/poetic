import os
from pathlib import Path

from poetic.core import launch, update

test_path = Path.cwd().parent / "poetic_test"


def test_launch(test_case_template):
    """
    Test template setup.
    """

    if not test_path.exists():
        os.mkdir(test_path)

    settings = test_case_template.settings
    launch(settings, path=test_path / settings["name"], overwrite=True)


def test_update(test_case_template):
    """
    Test template update.
    """
    if not test_path.exists():
        os.mkdir(test_path)

    update(path=test_path / test_case_template.settings["name"])
