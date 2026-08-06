import enum
from pathlib import Path

from poetic.setup.base import BaseSetup
from poetic.item.gitignore import GitignoreSetup
from poetic.item.vscode import VSCodeSetup
from poetic.settings.base import SetupSettings, SetupType
from poetic.setup.dependency import BaseDependencySetup


class ItemSetupClass(enum.Enum):
    vscode = VSCodeSetup
    gitignore = GitignoreSetup

    @classmethod
    def from_setup_tupe(cls, setup_type: SetupType):
        return cls[setup_type.name]


class ItemSetupBuilder:
    """
    Builder for item setup independent of template.
    """

    def build(self, settings: SetupSettings) -> BaseSetup:
        setup_class = ItemSetupClass.from_setup_tupe(settings.type).value
        kwargs = {"core": True} if issubclass(setup_class, BaseDependencySetup) else {}
        ret = setup_class(settings, Path.cwd(), **kwargs)
        return ret
