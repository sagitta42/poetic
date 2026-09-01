from abc import abstractmethod
from pathlib import Path
from typing import Self

from poetiq.logger import logg
from poetiq.settings.item import DBSettings
from poetiq.setup.poetry import BasePoetrySetup


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

    @property
    @abstractmethod
    def main(self) -> Self:
        """
        Main DB of the setup.
        """
        pass

    def setup(self) -> None:
        super().setup()

        self.setup_db()

    @abstractmethod
    def setup_db(self):
        """
        Set up DB.
        """
        logg.info(f"...setting up {self.db_type.value} DB", header=True)
