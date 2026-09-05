from abc import abstractmethod
from pathlib import Path
from typing import Generic

from poetiq.exceptions import PoetiqException
from poetiq.logger import logg
from poetiq.settings.base import T_ActionSettings, T_PoetiqActionSettings
from poetiq.utils.poetry import Poetry
from poetiq.utils.toml import TomlHandler


class BaseAction(Generic[T_ActionSettings]):
    def __init__(self, path: Path | None, settings: T_ActionSettings) -> None:
        self._settings = settings
        self.path: Path = path or Path.cwd()

    @abstractmethod
    def launch(self) -> None:
        """
        Launch action
        """
        pass


class BasePoetiqAction(BaseAction[T_PoetiqActionSettings]):
    """
    Action that involves poetry and poetiq.toml
    """

    def __init__(self, path: Path, settings: T_PoetiqActionSettings) -> None:
        super().__init__(path, settings)

        self._toml_name = "poetiq.toml"
        self._poetiq_toml = TomlHandler(self.path / self._toml_name)
        self._poetiq_toml.read()

        self._poetry = Poetry(self.path)

    def _get_poetries_of_interest(self) -> list[Poetry]:
        """
        Get poetries of interest.

        Split poetries if split settings were requested, otherwise main poetry.
        """
        ret = (
            self._get_all_split_poetries()
            if self._settings.split_requested
            else [self._poetry]
        )
        return ret

    def _get_all_split_poetries(self) -> list[Poetry]:
        """
        Get list of poetry obejcts for each split pyproject.toml directory in poetiq.toml
        """
        poetiq_settings = self._poetiq_toml.get_section("dependency-groups")
        logg.debug(poetiq_settings)
        split_deps_dirs = poetiq_settings.get("split", [])
        logg.debug(split_deps_dirs)
        ret = [self._get_split_poetry(dir) for dir in split_deps_dirs]
        return ret

    def _get_split_poetry(self, dir: str) -> Poetry:
        """
        Get split poetry corresponding to given directory.
        """
        split_deps_dirs = self._get_split_deps_dirs()
        dirname = dir.removesuffix("/")
        if dirname not in split_deps_dirs:
            raise PoetiqException(
                f"Directory {dirname} not found under split dependency groups in {self._toml_name}!"
            )
        ret = Poetry(self.path / dir, venv_path=self.path)
        return ret

    def _get_split_deps_dirs(self) -> list[str]:
        """
        Get split dependency directories from poetiq.toml
        """
        poetiq_settings = self._poetiq_toml.get_section("dependency-groups")
        ret = poetiq_settings.get("split", [])
        return ret
