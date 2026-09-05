from abc import abstractmethod
from pathlib import Path
from typing import Generic

from poetiq.exceptions import PoetiqException
from poetiq.logger import logg
from poetiq.settings.base import (
    T_ActionSettings,
    T_PoetiqActionSettings,
    T_SplitActionSettings,
)
from poetiq.utils.poetry import Poetry
from poetiq.utils.toml import TomlHandler


class BaseAction(Generic[T_ActionSettings]):
    """
    Base clas for any kind of action.

    Action is performed in given path and may have specific settings.
    Steps of action are defined in the launch() method.
    """

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
        return [self._poetry]


class BaseSplitPoetiqAction(BasePoetiqAction[T_SplitActionSettings]):
    """
    True poetiq split action.

    This action can be performed on all split directories or specific given one
    (split setting is optional string, not bool)
    TODO: upgrade InstallAction to BaseSplitAction, rendering any PoetiqAction true split and unifying the classes
    """

    def _get_poetries_of_interest(self) -> list[Poetry]:
        """
        Get poetries of interest.

        All split poetries if --split was requested, specific poetries if specific directory given.
        Otherwise main poetry.
        """
        if self._settings.split is None:
            return super()._get_poetries_of_interest()

        if self._settings.split == "":
            return self._get_all_split_poetries()

        split_poetry = self._get_split_poetry(self._settings.split)
        return [split_poetry]

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
