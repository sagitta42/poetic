import enum
from pathlib import Path

from poetiq.settings.setup import SetupType
from poetiq.settings.template import BaseTemplateSettings
from poetiq.template.app import AppTemplate
from poetiq.template.base import BaseTemplate
from poetiq.template.package import PackageTemplate


class TemplateClass(enum.Enum):
    package = PackageTemplate
    app = AppTemplate

    @classmethod
    def from_template_type(cls, template_type: SetupType):
        return cls[template_type.name]


class TemplateBuilder:
    def build(
        self,
        settings: BaseTemplateSettings,
        path: Path | None,
    ) -> BaseTemplate:
        """
        Build template setup.

        root_path (Path): path in which to do the setup.
            Default (None): setup path is same as package name.
        """
        template_class = TemplateClass.from_template_type(settings.type).value

        ret = template_class(settings, path)
        return ret
