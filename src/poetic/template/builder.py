import enum
from pathlib import Path
from typing import Any

from poetic.exceptions import PoeticException
from poetic.settings.base import SetupType
from poetic.settings.options import TemplateOptions
from poetic.settings.template import BaseTemplateSettings
from poetic.template.api import APITemplate
from poetic.template.base import BaseTemplate
from poetic.template.package import PackageTemplate
from poetic.utils.toml import PyProjectHandler


class TemplateClass(enum.Enum):
    package = PackageTemplate
    api = APITemplate

    @classmethod
    def from_template_type(cls, template_type: SetupType):
        return cls[template_type.name]


class TemplateBuilder:
    def build(
        self,
        settings: BaseTemplateSettings,
        path: Path | None = None,
    ) -> BaseTemplate:
        """
        Build template setup.

        root_path (Path): path in which to do the setup. Used mainly for testing/debug.
            Default None -> setup path is same as package name. Otherwise prepend path
        """
        template_class = TemplateClass.from_template_type(settings.type).value

        ret = template_class(settings, path)
        return ret

    def find(self) -> BaseTemplate:
        """
        Find template setup in current path.

        Find setup information based on pyproject.toml.
        """
        pyproject_handler = PyProjectHandler(Path.cwd())
        pyproject_handler.read()

        poetic_config: dict[str, Any] = pyproject_handler.get_section("tool.poetic")
        if poetic_config == {}:
            raise PoeticException(
                f"No [tool.poetic] section found in pyproject.toml! Cannot auto-udpate.\nLaunch with command line arguments used to create tempalte with poetic new; or add them under tool.poetic manually"
            )
        poetic_config["name"] = pyproject_handler.get_section("project")["name"]
        settings = TemplateOptions(**{"settings": poetic_config}).settings
        ret = self.build(settings, path=Path.cwd())
        return ret
