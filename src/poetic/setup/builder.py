from abc import abstractmethod
from pathlib import Path
from typing import Generic

from poetic.settings.setup import T_SetupSettings
from poetic.setup.base import BaseSetup


class BaseSetupBuilder(Generic[T_SetupSettings]):
    """
    General builder for any kind of setup.
    """

    @abstractmethod
    def build(self, settings: T_SetupSettings, path: Path, core: bool) -> BaseSetup:
        pass
