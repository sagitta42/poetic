from poetic.action.poetic import PoeticAction
from poetic.logger import logg
from poetic.settings.add import AddSettings


class AddAction(PoeticAction[AddSettings]):

    def launch(self) -> None:
        """
        Launch poetry add.

        Add to pyproject auto-detecting git+ or ssh://.
        If local, add to poetic.toml instead.
        """
        if self._settings.local == "":
            self._add_pyproject()
        else:
            self._add_poetic()

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

        self._poetry.add(prepend + package_source)

    def _add_poetic(self):
        dep_section = "dependency-groups"

        self._poetic_toml.add_section(dep_section)
        if not "local" in self._poetic_toml.get_section(dep_section):
            self._poetic_toml.add_section(dep_section, {"local": []})

        entry = f"{self._settings.package} @ {self._settings.local}"
        self._poetic_toml._toml_dict[dep_section]["local"].append(entry)
        logg.info(f"Added dependency to {self._toml_file}")
        logg.info(entry, poetic=True)
        self._poetic_toml.write()
