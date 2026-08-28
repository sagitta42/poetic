import argparse
import enum
from typing import Type

from pydantic import Field

from poetic.settings.add import AddSettings
from poetic.settings.base import BaseSettings
from poetic.settings.install import InstallSettings
from poetic.settings.item import DBSettings, LoggerSettings
from poetic.settings.setup import SetupSettings, SetupType
from poetic.settings.template import (
    AppTemplateSettings,
    BaseTemplateSettings,
    PackageTemplateSettings,
)


class Subparser(str, enum.Enum):
    init = "init"
    add = "add"
    new = "new"
    setup = "setup"
    install = "install"
    update = "update"


# TODO: OOP encalsulate duplications -> pydantic-argparse
def add_bool(
    parser: argparse.ArgumentParser,
    name: str,
    help: Type[BaseSettings],
    exclusive: bool = False,
    optional: bool = True,
):
    """
    Add bool argument.

    exclusive: exclusive to these settings

    optional (bool): if not provided, defaults to False
    """

    parser.add_argument(
        f"--{name}",
        action="store_true",
        default=False if optional else None,
        help=help.description(name, exclusive=exclusive),
    )


def add_str(
    parser: argparse.ArgumentParser,
    name: str,
    help: Type[BaseSettings],
    optional: bool,
    flag: bool = True,
    exclusive: bool = False,
    informative: bool = True,
    none_is_option: bool = False,
):
    """
    Add string argument.

    optional (bool): if not provided, defaults to default
    flag: add -- i.e. --name keyword argument
    exclusive (bool): this argument is exclusive to the given type of settings
    informative ( bool): (applies to flag only) if just --flag is provided with no option, assume const value
    """
    arg_name = name
    if flag:
        arg_name = f"--{arg_name}"

    parser.add_argument(
        arg_name,
        type=str,
        default=help.default(name) if optional else None,
        choices=help.options(name, none_is_option),
        nargs="?" if optional else None,
        const=help.const(name) if flag and informative else None,
        help=help.description(name, exclusive=exclusive),
    )


def add_db_arguments(
    parser: argparse.ArgumentParser,
    help: Type[SetupSettings],
    informative: bool,
    none_is_option: bool,
):
    """
    Add arguments for DB setup to given parser.

    help: pydantic model to use for description; default, and const values.
        (can be DBSettings or AppTemplateSettings, for example)
    """
    add_str(
        parser,
        "db-type",
        help=help,
        optional=True,
        exclusive=True,
        informative=informative,
        none_is_option=none_is_option,
    )

    add_bool(parser, "dev-sqlite", help=DBSettings, exclusive=True)


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

    add_db_arguments(
        parser, AppTemplateSettings, informative=informative, none_is_option=True
    )

    add_bool(
        parser,
        "settings",
        PackageTemplateSettings,
        exclusive=True,
        optional=informative,
    )
    add_bool(
        parser,
        "progressbar",
        PackageTemplateSettings,
        exclusive=True,
        optional=informative,
    )


def add_new_template_arguments(parser: argparse.ArgumentParser):
    """
    Add arguments for new template creation.
    """
    add_str(
        parser,
        "name",
        help=BaseTemplateSettings,
        optional=False,
        flag=False,
        informative=False,
    )

    add_template_arguments(parser, informative=True)


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

    add_db_arguments(parser, DBSettings, informative=True, none_is_option=False)
    add_str(parser, "subfolder", LoggerSettings, optional=True, informative=False)

    add_bool(parser, "no-commit", SetupSettings)


def add_install_arguments(parser: argparse.ArgumentParser):
    """
    Add arguments for install functionalities.
    """
    add_bool(parser, "local", InstallSettings)
    add_str(parser, "package", help=InstallSettings, optional=True, flag=False)


def add_poetic_add_arguments(parser: argparse.ArgumentParser):
    add_str(parser, "package", help=AddSettings, optional=False, flag=False)
    add_str(parser, "local", help=AddSettings, optional=True, flag=True)
