import enum
from pathlib import Path

from poetic.api import APITemplate
from poetic.base import BaseTemplate
from poetic.logger import logg
from poetic.package import PackageTemplate
from poetic.settings import BaseTemplateSettings, SetupSettings, SetupType
from poetic.setup.base import BaseSetup
from poetic.setup.gitignore import GitignoreSetup
from poetic.setup.vscode import VSCodeSetup


class SetupClass(enum.Enum):
    vscode = VSCodeSetup
    gitignore = GitignoreSetup

    @classmethod
    def from_setup_tupe(cls, setup_type: SetupType):
        return cls[setup_type.name]


# TODO: unify with template class/builder
class SetupBuilder:
    def build(self, settings: SetupSettings) -> BaseSetup:
        setup_class = SetupClass.from_setup_tupe(settings.type).value
        ret = setup_class(settings, Path.cwd())
        return ret


class TemplateClass(enum.Enum):
    package = PackageTemplate
    api = APITemplate

    @classmethod
    def from_template_type(cls, template_type: SetupType):
        return cls[template_type.name]


class TemplateBuilder:
    def build(self, settings: BaseTemplateSettings) -> BaseTemplate:
        """
        Build template setup.
        """
        template_class = TemplateClass.from_template_type(settings.type).value

        ret = template_class(settings)
        return ret


class PoeticFactory:
    def build(
        self, settings: BaseTemplateSettings | SetupSettings
    ) -> BaseTemplate | BaseSetup:
        """
        Build template or functionlaity setup.
        """
        if isinstance(settings, BaseTemplateSettings):
            builder_class = TemplateBuilder
        elif isinstance(settings, SetupSettings):
            builder_class = SetupBuilder
        else:
            raise ValueError(
                f"Settings class {settings.__class__.__name__} not supported in factory!"
            )

        builder = builder_class()
        ret = builder.build(settings)
        return ret
