from pathlib import Path

from poetic.settings.item import ProgressBarSettings
from poetic.setup.dependency import BaseDependencySetup


class ProgressBarSetup(
    BaseDependencySetup[ProgressBarSettings],
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

        self._copy_template("progress_bar.py")

    def setup_dependencies(self) -> None:
        super().setup_dependencies()

        self._poetry_add("tqdm")
