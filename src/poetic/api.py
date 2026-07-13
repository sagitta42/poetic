import os
from pathlib import Path
import subprocess

from poetic.general import GeneralSetup


class APISetup(GeneralSetup):
    _TYPE: str = "API"

    def __init__(self, name: str) -> None:
        super().__init__(name)

        os.mkdir(self.name)
        subprocess.run(
            [
                "poetry",
                "init",
                "--no-interaction",
                "--name",
                self.name,
                "--description",
                "",
            ],
            cwd=name,
        )
