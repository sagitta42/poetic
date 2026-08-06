import os
from pathlib import Path

from poetic.settings.item import VSCodeSetupSettings
from poetic.setup.functionality import BaseFunctionalitySetup
from poetic.utils.tree import display


class VSCodeSetup(BaseFunctionalitySetup[VSCodeSetupSettings]):
    """
    VSCode settings and launch setup.
    """

    def __init__(
        self, path: Path, settings: VSCodeSetupSettings = VSCodeSetupSettings()
    ) -> None:
        super().__init__(path, settings)

        self._path_to_vscode = self.path / ".vscode"

    def setup(self) -> None:
        """
        Set up VSCode.
        """
        super().setup()

        os.makedirs(self._path_to_vscode, exist_ok=True)

        for template in ["settings", "launch"]:
            self._copy_template(
                f"VSCode.{template}.json", self._path_to_vscode, f"{template}.json"
            )

    def display(self, suggest_commit: str | None = None):
        super().display(suggest_commit)
        display(self._path_to_vscode)
