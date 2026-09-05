from abc import abstractmethod
import enum
from typing import Any, TypeVar

from pydantic import BaseModel, ConfigDict, Field
from pydantic.fields import FieldInfo


class ActionType(enum.StrEnum):
    package = "package"
    app = "app"
    db = "db"
    envsettings = "envsettings"
    vscode = "vscode"
    gitignore = "gitignore"
    progressbar = "progressbar"
    logger = "logger"
    install = "install"
    add = "add"
    lock = "lock"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]


class BaseActionSettings(BaseModel):
    """
    Base class for settings for any action.

    Adaptor utils to argparse.
    """

    model_config = ConfigDict(extra="ignore")
    type: ActionType = Field(description="Action type; discriminator")

    @classmethod
    def options(cls, arg: str) -> list | None:
        field_type = cls._get_field(arg).annotation
        assert field_type is not None
        if issubclass(field_type, enum.Enum):
            ret = [item.value for item in field_type]
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


class BasePoetiqActionSettings(BaseActionSettings):
    @property
    @abstractmethod
    def split_requested(self) -> bool:
        pass


class BaseSplitActionSettings(BasePoetiqActionSettings):
    split: str = Field(default="", description="Split pyproject.toml directory")


class BaseSetupSettings(BaseActionSettings):
    """
    Base class for settings for any type of setup.
    """

    type: ActionType = Field(description="Setup type")
    no_commit: bool = Field(default=False, description="Do not commit changes")


T_ActionSettings = TypeVar("T_ActionSettings", bound=BaseActionSettings)
T_PoetiqActionSettings = TypeVar(
    "T_PoetiqActionSettings", bound=BasePoetiqActionSettings
)
T_SetupSettings = TypeVar("T_SetupSettings", bound=BaseSetupSettings)
