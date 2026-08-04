import os
from pathlib import Path

from poetic.logger import logg
from poetic.settings import VSCodeSetupSettings
from poetic.setup.base import BaseSetup
from poetic.utils.tree import display


class VSCodeSetup(BaseSetup[VSCodeSetupSettings]):
    """
    VSCode settings and launch setup.
    """

    def __init__(self, settings: VSCodeSetupSettings, path: Path) -> None:
        super().__init__(settings, path)

        self._path_to_vscode = self.path / ".vscode"

    def setup(self, skip_super: bool = False) -> None:
        os.makedirs(self._path_to_vscode, exist_ok=True)
        self._copy_template(
            "VSCode.settings.json", self._path_to_vscode, "settings.json"
        )
        self._copy_template("VSCode.launch.json", self._path_to_vscode, "launch.json")

    def launch(self) -> None:
        self.setup()

        logg.info("VSCode setup")
        display(self._path_to_vscode)
