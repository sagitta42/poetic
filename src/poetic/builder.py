import enum

from poetic.api import APITemplate
from poetic.base import Template
from poetic.logger import logg
from poetic.package import PackageTemplate
from poetic.settings import TemplateSettings, TemplateType


class TemplateClass(enum.Enum):
    package = PackageTemplate
    api = APITemplate

    @classmethod
    def from_template_type(cls, template_type: TemplateType):
        return cls[template_type.name]


class TemplateBuilder:
    def build(self, settings: TemplateSettings) -> Template:
        template_class = TemplateClass.from_template_type(settings.type).value

        ret = template_class(settings)
        return ret
