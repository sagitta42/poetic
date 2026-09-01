import argparse
import enum

from poetiq.cli.args import add_bool, add_str
from poetiq.cli.db import add_db_arguments
from poetiq.settings.add import AddSettings
from poetiq.settings.install import InstallSettings
from poetiq.settings.item import DBSettings, DBType, LoggerSettings
from poetiq.settings.setup import SetupSettings, SetupType
from poetiq.settings.template import (
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
        parser,
        AppTemplateSettings,
        informative=informative,
        choices=DBType.with_none(DBType.sql()),
    )

    add_bool(parser, "mongodb", AppTemplateSettings, exclusive=True)

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

    add_db_arguments(parser, DBSettings, informative=True, choices=DBType.sql())
    add_str(
        parser,
        "subfolder",
        LoggerSettings,
        optional=True,
        informative=False,
        exclusive=True,
    )

    add_bool(parser, "no-commit", SetupSettings)


def add_install_arguments(parser: argparse.ArgumentParser):
    """
    Add arguments for install functionalities.
    """
    add_bool(parser, "local", InstallSettings)
    add_str(parser, "package", help=InstallSettings, optional=True, flag=False)


def add_poetiq_add_arguments(parser: argparse.ArgumentParser):
    add_str(parser, "package", help=AddSettings, optional=False, flag=False)
    add_str(parser, "local", help=AddSettings, optional=True, flag=True)
