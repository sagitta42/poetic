import enum
from pathlib import Path

from poetiq.item.logger import LoggerSetup
from poetiq.settings.setup import SetupSettings, SetupType
from poetiq.setup.base import BaseSetup
from poetiq.item.gitignore import GitignoreSetup
from poetiq.item.vscode import VSCodeSetup
from poetiq.setup.builder import BaseSetupBuilder


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
        ret = setup_class(path, settings, core=core)
        return ret
