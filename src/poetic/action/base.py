from abc import abstractmethod
from pathlib import Path
from typing import Generic

from poetic.settings.base import T_Settings


class BaseAction(Generic[T_Settings]):
    def __init__(self, path: Path, settings: T_Settings) -> None:
        self._settings = settings
        self.path = path

    @abstractmethod
    def launch(self) -> None:
        """
        Launch action
        """
        pass
