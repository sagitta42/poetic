import os

from poetic.settings import VSCodeSetupSettings
from poetic.setup.base import BaseSetup


class VSCodeSetup(BaseSetup[VSCodeSetupSettings]):
    """
    VSCode settings and launch setup.
    """

    def setup(self, skip_super: bool = False) -> None:
        path_to_vscode = self.path / ".vscode"
        os.makedirs(path_to_vscode, exist_ok=True)
        self._copy_template("VSCode.settings.json", path_to_vscode, "settings.json")
        self._copy_template("VSCode.launch.json", path_to_vscode, "launch.json")

    def launch(self) -> None:
        self.setup()
