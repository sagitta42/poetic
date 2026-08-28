from pathlib import Path

from poetic.action.base import BaseAction
from poetic.settings.add import AddSettings
from poetic.utils.poetry import Poetry


class AddAction(BaseAction[AddSettings]):
    def __init__(self, path: Path, settings: AddSettings) -> None:
        super().__init__(path, settings)

        self._poetry = Poetry(self.path)

    def launch(self) -> None:
        """
        Launch poetry add.

        Assumes https links start with https:// (e.g. GitHub) and only prepends git+
        Assumes if neither https nor ssh at start of link, that it is an ssh one missing the prepend.
        """
        package_source = self._settings.package

        prepend=""
        if package_source.startswith("git"):
            prepend = "git+"
            if not any(package_source.startswith(start) for start in ["https", "ssh"]):
                prepend += "ssh://"

        self._poetry.add(prepend+package_source)
