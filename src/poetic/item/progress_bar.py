from poetic.item.base import BaseDependencySetup
from poetic.settings.item import ProgressBarSettings


class ProgressBarSetup(
    BaseDependencySetup[ProgressBarSettings],
):
    @property
    def name(self) -> str:
        return "ProgressBar"

    def setup(self) -> None:
        super().setup()

        self._copy_template("progress_bar.py")

    def setup_dependencies(self) -> None:
        self._poetry_add("tqdm")
