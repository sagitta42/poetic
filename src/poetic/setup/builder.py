from abc import abstractmethod
from pathlib import Path
from typing import Generic

from poetic.settings.base import T_Settings
from poetic.setup.base import BaseSetup


class BaseSetupBuilder(Generic[T_Settings]):
    """
    General builder for any kind of setup.
    """

    @abstractmethod
    def build(self, settings: T_Settings, path: Path, core: bool) -> BaseSetup:
        pass
