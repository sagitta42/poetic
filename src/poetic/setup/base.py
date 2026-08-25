from abc import abstractmethod
import enum
from pathlib import Path
import shutil
from typing import Generic


from poetic.settings.base import SetupType, T_Settings
from poetic.utils.git import Git

from poetic.logger import logg
from poetic.utils.template import TemplateLocation, TemplateManager


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

    def __init__(self, path: Path, settings: T_Settings) -> None:
        self._settings = settings
        self.path = path

        self._type: SetupType = settings.type

        self._templates = TemplateManager(self._type, self.path)
        self.git = Git(self.path)

    def global_setup(self):
        """
        Global multistage setup.

        Part 1 - Setup
        Part 2 - Post-setup
        """
        self.setup()
        self.post_setup()

    @abstractmethod
    def setup(self) -> bool | None:
        """
        Main setup.

        Optionally return a flag representing whether this setup existed before.
        """
        pass

    @abstractmethod
    def launch(self) -> None:
        """
        Launch action of this setup
        """
        pass

    def post_setup(self):
        """
        Post-setup actions (if any)
        """
        pass
