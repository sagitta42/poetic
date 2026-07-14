import enum
from typing import Any
from pydantic import BaseModel, Field

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


class TemplateSettings(BaseModel):
    name: str = Field(description="Package name")
    type: TemplateType = Field(
        default=TemplateType.package, description="Template type"
    )

    @classmethod
    def description(cls, field_name: str) -> str:
        ret = cls.model_fields[field_name].description
        assert ret is not None
        return ret

    @classmethod
    def default(cls, field_name: str) -> Any:
        ret = cls.model_fields[field_name].default
        return ret

    @classmethod
    def options(cls, field_name: str) -> list | None:
        field_type = cls.model_fields[field_name].annotation
        assert field_type is not None
        if issubclass(field_type, enum.Enum):
            return [item.value for item in field_type]
        return None

class TemplateBuilder:
    def build(self, settings: TemplateSettings) -> Template:
        template_type = TemplateType(settings.type)
        template_class = TemplateClass.from_template_type(template_type).value
        ret = template_class(settings.name)
        return ret
