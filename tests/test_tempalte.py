import os
from pathlib import Path

from poetic.settings.template import APITemplateSettings, PackageTemplateSettings
from poetic.template.builder import TemplateBuilder


def test_template(test_case_template):
    """
    Test template setup.
    """
    template_builder = TemplateBuilder()

    root_path = Path.cwd().parent / "poetic_test"
    if not root_path.exists():
        os.mkdir(root_path)

    setupper = template_builder.build(test_case_template, root_path=root_path)

    setupper.launch()
