import enum
from pathlib import Path

from poetic.item.base import BaseDependencySetup, BaseItemSetup
from poetic.item.gitignore import GitignoreSetup
from poetic.item.vscode import VSCodeSetup
from poetic.settings.item import SetupSettings, SetupType


class ItemClass(enum.Enum):
    vscode = VSCodeSetup
    gitignore = GitignoreSetup

    @classmethod
    def from_setup_tupe(cls, setup_type: SetupType):
        return cls[setup_type.name]


class ItemBuilder:
    def build(self, settings: SetupSettings) -> BaseItemSetup:
        setup_class = ItemClass.from_setup_tupe(settings.type).value
        kwargs = {"core": True} if issubclass(setup_class, BaseDependencySetup) else {}
        ret = setup_class(settings, Path.cwd(), **kwargs)
        return ret
