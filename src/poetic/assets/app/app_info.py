from pathlib import Path
import tomllib

from pydantic import BaseModel, Field


class AppInfo(BaseModel):
    name: str = Field(description="App name")
    version: str = Field(description="App version")


class PyProjectInfoBuilder:
    """
    Build app info based on pyproject.toml
    """

    def __init__(self) -> None:
        self._pyproject_path: Path = self._find_pyproject()

    def build(self) -> AppInfo:
        with open(self._pyproject_path, "rb") as f:
            py_info = tomllib.load(f)
        project_info = py_info["project"] if "project" in py_info else py_info["tool"]["poetry"]
        ret = AppInfo(name=project_info["name"], version=project_info["version"])
        return ret

    def _find_pyproject(self) -> Path:
        """
        Find pyproject file in current path and its parents.
        """
        start_path = Path(__file__)

        for parent in [start_path, *start_path.parents]:
            pyproject_path = parent / "pyproject.toml"
            if pyproject_path.exists():
                return pyproject_path
        raise FileNotFoundError("pyproject.toml not found in any parent directory!")


app_info = PyProjectInfoBuilder().build()
