import enum

from poetic.settings.item import SetupType
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
    def build(self, settings: BaseTemplateSettings) -> BaseTemplate:
        """
        Build template setup.
        """
        template_class = TemplateClass.from_template_type(settings.type).value

        ret = template_class(settings)
        return ret
