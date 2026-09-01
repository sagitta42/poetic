
import argparse
from typing import Type

from poetiq.cli.args import add_bool, add_str
from poetiq.settings.item import DBSettings
from poetiq.settings.setup import SetupSettings


def add_db_arguments(
    parser: argparse.ArgumentParser,
    help: Type[SetupSettings],
    informative: bool,
    choices: list[str],
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
        choices=choices,
    )

    add_bool(parser, "dev-sqlite", help=help, exclusive=True)
    add_bool(parser, "pydantic-table", help=help, exclusive=True)
