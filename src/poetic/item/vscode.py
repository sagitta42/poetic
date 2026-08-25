import os
from pathlib import Path

from poetic.settings.item import VSCodeSetupSettings
from poetic.setup.functionality import BaseFunctionalitySetup
from poetic.utils.template import TemplateLocation
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
            self._templates.copy(
                f"{template}.json",
                package_path=self._path_to_vscode,
                package_filename=f"{template}.json",
                template_location=TemplateLocation.poetic_build,
            )

    def display(self, suggest_commit: str | None = None):
        super().display(suggest_commit)
        display(self._path_to_vscode)
