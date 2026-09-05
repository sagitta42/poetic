import os
from pathlib import Path

from poetiq.settings.setup import VSCodeSetupSettings
from poetiq.setup.base.functionality import BaseFunctionalitySetup
from poetiq.utils.template import TemplateLocation
from poetiq.utils.tree import display


class VSCodeSetup(BaseFunctionalitySetup[VSCodeSetupSettings]):
    """
    VSCode settings and launch setup.
    """

    def __init__(
        self,
        path: Path,
        settings: VSCodeSetupSettings = VSCodeSetupSettings(),
        core: bool = False,
    ) -> None:
        super().__init__(path, settings, core)

        self._path_to_vscode = self.path / ".vscode"

    def setup(self) -> None:
        """
        Set up VSCode.
        """
        super().setup()

        os.makedirs(self._path_to_vscode, exist_ok=True)

        for template in ["settings", "launch"]:
            self._templates.copy(
                f"{template}.json",
                package_path=self._path_to_vscode,
                package_filename=f"{template}.json",
                template_location=TemplateLocation.poetiq_build,
            )

    def display(self, suggest_commit: str | None = None):
        super().display(suggest_commit)
        display(self._path_to_vscode)
