from abc import abstractmethod
from pathlib import Path
from typing import Generic


from poetic.settings.base import SetupType, T_Settings
from poetic.utils.git import Git

from poetic.logger import logg
from poetic.utils.template import TemplateManager


class BaseSetup(Generic[T_Settings]):
    """
    General setup of any kind.

    path (Path): path to root directory of setup

    Main procedures:
        - setup: defines setup of folders, files etc.
        - launch: defines actions to be done if setup is launched

    Includes basic operations:
        - git control
        - copying templates
    """

    def __init__(self, path: Path, settings: T_Settings, core: bool) -> None:
        self._settings = settings
        self.path = path
        self._core = core

        self._type: SetupType = settings.type

        self._templates = TemplateManager(self._type, self.path)
        self.git = Git(self.path)

    @property
    def title(self) -> str:
        """
        Setup title
        """
        return self._settings.type.value

    @abstractmethod
    def setup(self) -> bool | None:
        """
        Main setup.

        Optionally return a flag representing whether this setup existed before.
        """
        line = "-" * 60
        if self._core:
            logg.info(line, header=True)
        logg.info(f"@ Setting up {self.title}", header=True)
        if self._core:
            logg.info(line, header=True)

    @abstractmethod
    def launch(self) -> None:
        """
        Launch action of this setup
        """
        pass