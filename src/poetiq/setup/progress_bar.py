from pathlib import Path

from poetiq.settings.setup import ProgressBarSettings
from poetiq.setup.base.poetry import BasePoetrySetup


class ProgressBarSetup(
    BasePoetrySetup[ProgressBarSettings],
):
    def __init__(
        self,
        path: Path,
        settings: ProgressBarSettings = ProgressBarSettings(),
        core: bool = True,
    ) -> None:
        super().__init__(path, settings, core)

    @property
    def name(self) -> str:
        return "ProgressBar"

    def setup(self) -> None:
        super().setup()

        self._templates.copy(
            "progress_bar.py", package_path=self.path / self._settings.subfolder
        )

    def setup_dependencies(self) -> None:
        super().setup_dependencies()

        self._poetry_add("tqdm")
