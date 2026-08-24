import os
from pathlib import Path

from poetic.core import launch

test_path = Path.cwd().parent / "poetic_test"


def test_launch(test_case_template):
    """
    Test template setup.
    """

    if not test_path.exists():
        os.mkdir(test_path)

    launch(test_case_template, path=test_path, overwrite=True)
