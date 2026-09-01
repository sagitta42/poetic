# TODO: OOP encalsulate duplications -> pydantic-argparse
import argparse
from typing import Any, Type

from poetic.settings.base import BaseSettings


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
    choices: list[Any] | None = None,
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
        choices=choices or help.options(name),
        nargs="?" if optional else None,
        const=help.const(name) if flag and informative else None,
        help=help.description(name, exclusive=exclusive),
    )
