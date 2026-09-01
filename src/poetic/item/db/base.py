from abc import abstractmethod
from pathlib import Path

from poetic.logger import logg
from poetic.settings.item import DBSettings
from poetic.setup.poetry import BasePoetrySetup
from poetic.utils.db import DBEnvVars


class BaseDBSetup(BasePoetrySetup[DBSettings]):
    """
    Base class for DB setup.

    Encompasses single and dual DB setups.
    """

    def __init__(self, path: Path, settings: DBSettings, core: bool) -> None:
        super().__init__(path, settings, core)

        self.db_type = self._settings.db_type

    @property
    def title(self) -> str:
        return f"{super().title}: {self.db_type.value}"

    def setup(self) -> None:
        super().setup()

        self.setup_db()

    @abstractmethod
    def setup_db(self):
        """
        Set up DB.
        """
        logg.info(f"...setting up {self.db_type.value} DB", header=True)
