import argparse
from typing import Type

from poetiq.cli.args import add_bool, add_str
from poetiq.settings.base import BaseSplitActionSettings
from poetiq.settings.poetiq_action import AddSettings, InstallSettings, LockSettings


def add_poetiq_split_arguments(
    parser: argparse.ArgumentParser,
    help: Type[BaseSplitActionSettings],
    informative: bool,
):
    add_str(
        parser,
        "split",
        help=help,
        optional=True,
        flag=True,
        informative=informative,
        metavar="DIR",
    )


def add_install_arguments(parser: argparse.ArgumentParser):
    """
    Add arguments for install functionalities.
    """
    add_poetiq_split_arguments(parser, InstallSettings, informative=True)
    add_bool(parser, "local", InstallSettings)
    add_str(parser, "package", help=InstallSettings, optional=True, flag=False)


def add_poetiq_add_arguments(parser: argparse.ArgumentParser):
    add_str(parser, "package", help=AddSettings, optional=False, flag=False)
    add_poetiq_split_arguments(parser, AddSettings, informative=False)
    add_str(parser, "local", help=AddSettings, optional=True, flag=True, metavar="PATH")


def add_poetiq_lock_arguments(parser: argparse.ArgumentParser):
    add_poetiq_split_arguments(parser, LockSettings, informative=True)
