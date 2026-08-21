import enum
from pathlib import Path

from poetic.item.logger import LoggerSetup
from poetic.setup.base import BaseSetup
from poetic.item.gitignore import GitignoreSetup
from poetic.item.vscode import VSCodeSetup
from poetic.settings.base import SetupSettings, SetupType
from poetic.setup.builder import BaseSetupBuilder
from poetic.setup.dependency import BaseDependencySetup


class ItemSetupClass(enum.Enum):
    vscode = VSCodeSetup
    gitignore = GitignoreSetup
    logger = LoggerSetup

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
