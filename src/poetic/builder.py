import enum
from tempfile import template

from poetic.api import APITemplate
from poetic.base import Template
from poetic.package import PackageTemplate


class TemplateType(str, enum.Enum):
    package = "package"
    api = "api"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]


class TemplateClass(enum.Enum):
    package = PackageTemplate
    api = APITemplate

    @classmethod
    def from_template_type(cls, template_type: TemplateType):
        return cls[template_type.name]


class TemplateBuilder:
    def build(
        self,
        name: str,
        template_type: TemplateType,
    ) -> Template:
        template_type = TemplateType(template_type)
        template_class = TemplateClass.from_template_type(template_type).value
        ret = template_class(name)
        return ret
