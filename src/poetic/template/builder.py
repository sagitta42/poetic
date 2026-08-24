import enum
from pathlib import Path

from poetic.settings.base import SetupType
from poetic.settings.template import BaseTemplateSettings
from poetic.template.api import APITemplate
from poetic.template.base import BaseTemplate
from poetic.template.package import PackageTemplate


class TemplateClass(enum.Enum):
    package = PackageTemplate
    api = APITemplate

    @classmethod
    def from_template_type(cls, template_type: SetupType):
        return cls[template_type.name]


class TemplateBuilder:
    def build(
        self,
        settings: BaseTemplateSettings,
        root_path: Path | None = None,
    ) -> BaseTemplate:
        """
        Build template setup.

        root_path (Path): path in which to do the setup. Used mainly for testing/debug.
            Default None -> setup path is same as package name. Otherwise prepend path
        """
        template_class = TemplateClass.from_template_type(settings.type).value

        ret = template_class(settings, root_path)
        return ret
