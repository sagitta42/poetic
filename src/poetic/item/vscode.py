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

    def setup(self) -> bool:
        """
        Set up VSCode.

        Return flag representing whether templates existed before.
        """
        existed = super().setup()

        os.makedirs(self._path_to_vscode, exist_ok=True)

        for template in ["settings", "launch"]:
            _, template_existed = self._copy_template(
                f"VSCode.{template}.json", self._path_to_vscode, f"{template}.json"
            )
            existed = existed or template_existed

        return existed

    def display(self, suggest_commit: str | None = None):
        super().display(suggest_commit)
        display(self._path_to_vscode)
