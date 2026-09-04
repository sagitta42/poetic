from abc import abstractmethod
from pathlib import Path
from typing import Generic

from poetiq.logger import logg
from poetiq.settings.base import T_ActionSettings


class BaseAction(Generic[T_ActionSettings]):
    def __init__(self, path: Path | None, settings: T_ActionSettings) -> None:
        self._settings = settings
        self.path: Path = path or Path.cwd()

    @abstractmethod
    def launch(self) -> None:
        """
        Launch action
        """
        pass
