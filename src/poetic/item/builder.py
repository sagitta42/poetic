import enum
from pathlib import Path

from poetic.item.base import BaseItemSetup
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
        ret = setup_class(settings, Path.cwd())
        return ret
