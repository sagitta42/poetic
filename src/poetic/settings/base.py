import enum
from typing import Any, TypeVar

from pydantic import BaseModel, ConfigDict
from pydantic.fields import FieldInfo


class BaseSettings(BaseModel):
    """
    Base class for settings.

    Adaptor utils to argparse.
    """

    model_config = ConfigDict(extra="ignore")

    @classmethod
    def options(cls, arg: str, none_is_option: bool = False) -> list | None:
        field_type = cls._get_field(arg).annotation
        assert field_type is not None
        if issubclass(field_type, enum.Enum):
            ret = [item.value for item in field_type]
            if not none_is_option:
                ret = [value for value in ret if not value == "none"]
            return ret
        return None

    @classmethod
    def default(cls, arg: str) -> Any:
        ret = cls._get_field(arg).default
        if isinstance(ret, enum.Enum):
            ret = ret.value
        return ret

    @classmethod
    def description(cls, arg: str, exclusive: bool = False) -> str:
        """
        Field description util for argparse.

        exclusive: add note that it is exclusive for this type of template.
        """
        ret = cls._get_field(arg).description
        assert ret is not None
        if exclusive:
            template_type = cls.default("type")
            ret += f" ({template_type} only)"
        return ret

    @classmethod
    def const(cls, arg: str) -> str:
        """
        Constant value.

        Default value = setting not mentioned
        Const value = setting mentioned without specifying value
        """
        return cls.default(arg)

    @classmethod
    def _get_field(cls, arg: str) -> FieldInfo:
        return cls.model_fields[arg.replace("-", "_")]

T_Settings = TypeVar("T_Settings", bound=BaseSettings)
