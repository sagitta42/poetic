import enum
from typing import Any, Self

from pydantic import BaseModel, Field, model_validator

from poetic.logger import logg


class TemplateType(str, enum.Enum):
    package = "package"
    api = "api"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]


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


class APITemplateSettings(TemplateSettings):
    db: bool = Field(default=False, description="Create/update DB functionalities")

    @model_validator(mode="after")
    def check_db(self) -> Self:
        if self.db and self.type != TemplateType.api:
            logg.warning(
                f"DB functionalities not supported for {self.type.value} type; ignoring",
                important=True,
            )
        return self


class SettingsCrutch(BaseModel):
    """
    Exists only for convenience of detecting type of settings
    """

    settings: TemplateSettings | APITemplateSettings
