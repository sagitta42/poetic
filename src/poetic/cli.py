import argparse
import enum
from typing import Type

from poetic.settings.base import SetupSettings, SetupType
from poetic.settings.install import InstallSettings
from poetic.settings.item import DBSettings, LoggerSettings
from poetic.settings.template import (
    APITemplateSettings,
    BaseTemplateSettings,
    PackageTemplateSettings,
)


class Subparser(str, enum.Enum):
    new = "new"
    add = "add"
    install = "install"


def add_bool(
    parser: argparse.ArgumentParser,
    name: str,
    help: Type[SetupSettings],
    exclusive: bool = False,
):
    parser.add_argument(
        f"--{name}",
        action="store_true",
        help=help.description(name, exclusive=exclusive),
    )


def add_str(
    parser: argparse.ArgumentParser,
    name: str,
    help: Type[SetupSettings],
):
    parser.add_argument(
        f"--{name}",
        type=str,
        default=help.default(name),
        help=help.description(name),
        choices=help.options(name),
    )


def add_db_arguments(
    parser: argparse.ArgumentParser, description_source: Type[SetupSettings]
):
    """
    Add arguments for DB setup to given parser.

    description_source: pydantic model to use for description
        (can be DBSettings or APITemplateSettings, for example)
    """
    parser.add_argument(
        "--db",
        type=str,
        nargs="?",
        const=DBSettings.default("db"),
        default=None,
        choices=DBSettings.options("db"),
        help=description_source.description("db", exclusive=True),
    )


def add_logger_arguments(parser: argparse.ArgumentParser):
    """
    Add logger arguments
    """
    add_str(parser, "subfolder", LoggerSettings)


def add_template_arguments(parser: argparse.ArgumentParser):
    """
    Add arguments for template creation/update to given parser.
    """
    parser.add_argument("name", type=str, help=BaseTemplateSettings.description("name"))
    add_str(parser, "type", BaseTemplateSettings)

    add_db_arguments(parser, APITemplateSettings)

    # TODO: ? convert to single --items flag listing settings, progressbar and other types
    add_bool(parser, "settings", PackageTemplateSettings, exclusive=True)
    add_bool(parser, "progressbar", PackageTemplateSettings, exclusive=True)

    add_bool(parser, "update", BaseTemplateSettings)


def add_microfunctionality_arguments(parser: argparse.ArgumentParser):
    """
    Add arguments for adding functionality to given parser.
    """
    parser.add_argument(
        "type",
        type=str,
        choices=[
            setup_type.value
            for setup_type in [
                SetupType.vscode,
                SetupType.gitignore,
                SetupType.db,
                SetupType.logger,
            ]
        ],
        help="Type of functionality",
    )
    add_bool(parser, "no-commit", SetupSettings)
    add_db_arguments(parser, DBSettings)
    add_logger_arguments(parser)


def add_install_arguments(parser: argparse.ArgumentParser):
    """
    Add arguments for install functionalities.
    """
    add_bool(parser, "local", InstallSettings)
    parser.add_argument(
        "package",
        type=str,
        nargs="?",
        default=None,
        help=InstallSettings.description("package"),
    )
