from poetiq.action.base import BasePoetiqAction
from poetiq.logger import logg
from poetiq.settings.poetiq_action import AddSettings
from poetiq.utils.poetry import Poetry


class AddAction(BasePoetiqAction[AddSettings]):

    def launch(self) -> None:
        """
        Launch poetry add.

        Add to pyproject auto-detecting git+ or ssh://.
        If local, add to poetiq.toml instead.
        """
        if self._settings.local == "":
            self._add_pyproject()
        else:
            self._add_poetiq()

    def _add_pyproject(self):
        """
        Assumes https links start with https:// (e.g. GitHub) and only prepends git+
        Assumes if neither https nor ssh at start of link, that it is an ssh one missing the prepend.
        """
        package_source = self._settings.package

        prepend = ""
        if package_source.startswith("git") or package_source.endswith("git"):
            prepend = "git+"
            if not package_source.startswith("git@"):
                prepend += "file://"
            elif not any(
                package_source.startswith(start) for start in ["https", "ssh"]
            ):
                prepend += "ssh://"

        poetry = self._get_poetry_of_interest()
        logg.info(f"Adding to {poetry.path}...", poetiq=True)
        poetry.add(prepend + package_source)

    def _get_poetry_of_interest(self) -> Poetry:
        """
        Get poetries of interest.

        Specific subdirectory's poetry if split add was requested.
        Otherwise main poetry.
        """
        if self._settings.split_requested:
            return self._get_split_poetry(self._settings.split)
        return self._poetry

    def _add_poetiq(self):
        dep_section = "dependency-groups"

        self._poetiq_toml.add_section(dep_section)
        if not "local" in self._poetiq_toml.get_section(dep_section):
            self._poetiq_toml.add_section(dep_section, {"local": []})

        entry = f"{self._settings.package} @ {self._settings.local}"
        self._poetiq_toml._toml_dict[dep_section]["local"].append(entry)
        logg.info(f"Added dependency to {self._toml_name}")
        logg.info(entry, poetiq=True)
        self._poetiq_toml.write()
