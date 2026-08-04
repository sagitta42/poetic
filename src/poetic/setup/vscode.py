import os
from pathlib import Path

from poetic.logger import logg
from poetic.settings import VSCodeSetupSettings
from poetic.setup.base import BaseFunctionalitySetup
from poetic.utils.tree import display


class VSCodeSetup(BaseFunctionalitySetup[VSCodeSetupSettings]):
    """
    VSCode settings and launch setup.
    """

    def __init__(self, settings: VSCodeSetupSettings, path: Path) -> None:
        super().__init__(settings, path)

        self._path_to_vscode = self.path / ".vscode"

    @property
    def name(self) -> str:
        return "VSCode"

    def setup(self, skip_super: bool = False) -> bool:
        """
        Set up VSCode.

        Return flag representing whether templates existed before.
        """
        os.makedirs(self._path_to_vscode, exist_ok=True)

        existed = []
        for template in ["settings", "launch"]:
            _, template_existed = self._copy_template(
                f"VSCode.{template}.json", self._path_to_vscode, f"{template}.json"
            )
            existed.append(template_existed)

        return any(existed)

    def display(self, suggest_commit: str | None = None):
        super().display(suggest_commit)
        display(self._path_to_vscode)
