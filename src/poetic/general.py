from pathlib import Path

from poetic.logger import logg


class GeneralSetup:
    _TYPE: str

    def __init__(self, name: str) -> None:
        self.name = name
        self._inner_name = self.name.replace("-", "_")
        self.path = Path(self.name)

        logg.info(f"Setting up {self._TYPE}: {self.name}")
