import argparse
from pathlib import Path
from poetic.action.add import AddAction
from poetic.cli.cli import (
    Subparser,
    add_install_arguments,
    add_microfunctionality_arguments,
    add_new_template_arguments,
    add_poetic_add_arguments,
)
from poetic.core import install, launch, update
from poetic.exceptions import PoeticException
from poetic.logger import logg
from poetic.settings.add import AddSettings
from poetic.utils.poetry import Poetry


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    new_template_subparser = subparsers.add_parser(
        Subparser.new.value, help="create new template"
    )
    add_new_template_arguments(new_template_subparser)

    subparsers.add_parser(Subparser.init.value, help="basic no-interaction init")

    add_subparser = subparsers.add_parser(
        Subparser.add.value, help="poetry add with git+ auto-detect"
    )
    add_poetic_add_arguments(add_subparser)

    update_subparser = subparsers.add_parser(
        Subparser.update.value,
        help="update current template as is with new poetic updates",
    )
    # add_update_arguments(update_subparser)

    micro_functionality_subparser = subparsers.add_parser(
        Subparser.setup.value, help="setup functionality in existing repo/directory"
    )
    add_microfunctionality_arguments(micro_functionality_subparser)

    install_subparser = subparsers.add_parser(
        Subparser.install.value, help="poetry install with added options"
    )
    add_install_arguments(install_subparser)

    args = parser.parse_args()
    logg.debug(vars(args))

    settings_args = vars(args).copy()
    command = Subparser(settings_args.pop("command"))

    # TODO: attach exec() to parser, define elsewhere
    try:
        if command == Subparser.init:
            poetry = Poetry(Path.cwd())
            poetry.init_basic()
        elif command == Subparser.add:
            add_action = AddAction(Path.cwd(), AddSettings(**settings_args))
            add_action.launch()
        elif command == Subparser.update:
            update()
        elif command == Subparser.install:
            install(settings_args)
        else:
            launch(settings_args)

    except PoeticException as e:
        logg.error(str(e))
        return


if __name__ == "__main__":
    main()
