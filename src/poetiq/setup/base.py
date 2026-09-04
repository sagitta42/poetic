from abc import abstractmethod
from pathlib import Path


from poetiq.action.base import BaseAction
from poetiq.settings.base import ActionType, T_SetupSettings
from poetiq.utils.git import Git

from poetiq.logger import logg
from poetiq.utils.template import TemplateManager


class BaseSetup(BaseAction[T_SetupSettings]):
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

    def __init__(
        self, path: Path | None, settings: T_SetupSettings, core: bool
    ) -> None:
        super().__init__(path, settings)

        self._core = core
        self._type: ActionType = settings.type

        self._templates = TemplateManager(self._type, self.path)
        self._git = Git(self.path)

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
