import enum
from typing import Any, TypeVar

from pydantic import BaseModel, ConfigDict, Field
from pydantic.fields import FieldInfo


class SetupType(str, enum.Enum):
    package = "package"
    app = "app"
    db = "db"
    dotenv = "dotenv"
    vscode = "vscode"
    gitignore = "gitignore"
    progressbar = "progressbar"
    logger = "logger"
    install = "install"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]


class SetupSettings(BaseModel):
    """
    Base class for settings for any type of setup.
    """

    model_config = ConfigDict(extra="ignore")

    type: SetupType = Field(description="Setup type")
    no_commit: bool = Field(default=False, description="Do not commit changes")

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


T_Settings = TypeVar("T_Settings", bound=SetupSettings)
