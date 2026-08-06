from abc import abstractmethod
import enum
from pathlib import Path
from typing import Generic

from poetic.item.db.base import BaseDBSetup
from poetic.item.db.sqlite import SQLiteSetup
from poetic.settings.item import DBSettings, DBType
from poetic.setup.base import BaseSetup
from poetic.item.gitignore import GitignoreSetup
from poetic.item.vscode import VSCodeSetup
from poetic.settings.base import SetupSettings, SetupType, T_Settings
from poetic.setup.dependency import BaseDependencySetup


class BaseSetupBuilder(Generic[T_Settings]):
    """
    General builder for any kind of setup.
    """

    @abstractmethod
    def buid(self, settings: T_Settings, path: Path, core: bool) -> BaseSetup:
        pass


class ItemSetupClass(enum.Enum):
    vscode = VSCodeSetup
    gitignore = GitignoreSetup

    @classmethod
    def from_setup_type(cls, setup_type: SetupType):
        return cls[setup_type.name]


class ItemSetupBuilder(BaseSetupBuilder):
    """
    Builder for item setup independent of template.

    Creates item setup in current directory.
    Marks it as core setup.
    """

    def build(self, settings: SetupSettings, path: Path, core: bool) -> BaseSetup:
        """
        Build item setup based on item type.
        """
        setup_class = ItemSetupClass.from_setup_type(settings.type).value
        kwargs = {"core": core} if issubclass(setup_class, BaseDependencySetup) else {}
        ret = setup_class(path, settings, **kwargs)
        return ret
