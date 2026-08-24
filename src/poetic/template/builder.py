import enum
from pathlib import Path

from poetic.settings.base import SetupType
from poetic.settings.template import BaseTemplateSettings
from poetic.template.app import AppTemplate
from poetic.template.base import BaseTemplate
from poetic.template.package import PackageTemplate


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
