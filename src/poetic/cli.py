import argparse
import enum
from typing import Type

from poetic.settings.base import SetupSettings, SetupType
from poetic.settings.install import InstallSettings
from poetic.settings.item import DBSettings, LoggerSettings
from poetic.settings.template import (
    AppTemplateSettings,
    BaseTemplateSettings,
    PackageTemplateSettings,
)


class Subparser(str, enum.Enum):
    new = "new"
    add = "add"
    install = "install"
    update = "update"


# TODO: OOP encalsulate duplications
def add_bool(
    parser: argparse.ArgumentParser,
    name: str,
    help: Type[SetupSettings],
    exclusive: bool = False,
    informative: bool = True,
):
    """
    Add bool argument.

    exclusive: exclusive to these settings
    informative: True = flag not provided means False; False = flag not provided means no info (None)
    """

    parser.add_argument(
        f"--{name}",
        action="store_true",
        default=False if informative else None,
        help=help.description(name, exclusive=exclusive),
    )


def add_str(
    parser: argparse.ArgumentParser,
    name: str,
    help: Type[SetupSettings],
    optional: bool,
    flag: bool = True,
    exclusive: bool = False,
    informative: bool = True,
):
    """
    Add string argument.

    optional (bool): make argument optional = if not provided assume const value

    flag: add -- i.e. --name keyword argument

    exclusive (bool): this argument is exclusive to the given type of SetupSettings

    informative: True/False = flag not provided means use default/None (no info)
    """
    arg_name = name
    if flag:
        arg_name = f"--{arg_name}"

    parser.add_argument(
        arg_name,
        type=str,
        default=help.default(name) if informative else None,
        choices=help.options(name),
        nargs="?" if optional else None,
        const=help.const(name) if optional else None,
        help=help.description(name, exclusive=exclusive),
    )


def add_db_arguments(
    parser: argparse.ArgumentParser, help: Type[SetupSettings], informative: bool = True
):
    """
    Add arguments for DB setup to given parser.

    help: pydantic model to use for description; default, and const values.
        (can be DBSettings or AppTemplateSettings, for example)
    """
    add_str(
        parser, "db", help=help, optional=True, exclusive=True, informative=informative
    )


def add_template_arguments(parser: argparse.ArgumentParser, informative: bool):
    """
    Add arguments for template creation/update to given parser.
    """
    parser.add_argument(
        "--type",
        type=str,
        choices=[setup_type.value for setup_type in [SetupType.package, SetupType.app]],
        nargs="?",
        default=SetupType.package,
        help="Type of functionality",
    )

    add_db_arguments(parser, AppTemplateSettings, informative=informative)

    add_bool(
        parser,
        "settings",
        PackageTemplateSettings,
        exclusive=True,
        informative=informative,
    )
    add_bool(
        parser,
        "progressbar",
        PackageTemplateSettings,
        exclusive=True,
        informative=informative,
    )


def add_new_template_arguments(parser: argparse.ArgumentParser):
    """
    Add arguments for new template creation.
    """
    add_str(
        parser, "name", help=BaseTemplateSettings, optional=False, flag=False, informative=False
    )

    add_template_arguments(parser, informative=True)


def add_update_arguments(parser: argparse.ArgumentParser):
    """
    Add arguments for template update.

    During update, all unprovided flags assume None instead of default.
    """
    add_template_arguments(parser, informative=False)


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

    add_db_arguments(parser, DBSettings)
    add_str(parser, "subfolder", LoggerSettings, optional=True)

    add_bool(parser, "no-commit", SetupSettings)


def add_install_arguments(parser: argparse.ArgumentParser):
    """
    Add arguments for install functionalities.
    """
    add_bool(parser, "local", InstallSettings)
    add_str(parser, "package", help=InstallSettings, optional=True)
