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

    def launch(self) -> None:
        """
        Launch VSCode setup.

        Perform setup.
        Commit setup if in git repository and files did not exist before.
        """
        existed_before = self.setup()

        if self.git.is_git_repo and not existed_before:
            message = f"VSCode setup with {self._poetic_link}"
            self.git.commit_all(message)

        logg.info("VSCode setup")
        display(self._path_to_vscode)
