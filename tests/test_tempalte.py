import os
from pathlib import Path
import shutil
from time import sleep

from poetic.logger import logg
from poetic.template.builder import TemplateBuilder


def test_template(test_case_template):
    """
    Test template setup.
    """
    template_builder = TemplateBuilder()

    test_path = Path.cwd().parent / "poetic_test"
    if not test_path.exists():
        os.mkdir(test_path)

    settings = test_case_template.settings
    setupper = template_builder.build(settings, path=test_path / settings.name)

    if test_case_template.overwrite and setupper.path.exists():
        logg.warning(
            f"Removing directory in path {setupper.path} before setup in 5 seconds! Press Ctrl+C or stop test to cancel",
            important=True,
        )
        sleep(5)
        shutil.rmtree(setupper.path)
        logg.warning(f"Removed old directory in {setupper.path}", important=True)

    setupper.launch()
