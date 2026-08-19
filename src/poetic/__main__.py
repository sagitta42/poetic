import argparse
from pathlib import Path
from poetic.cli import (
    Subparser,
    add_install_arguments,
    add_microfunctionality_arguments,
    add_template_arguments,
)
from poetic.factory import PoeticFactory
from poetic.exceptions import PoeticException
from poetic.install import InstallSetup
from poetic.logger import logg
from poetic.settings.install import InstallSettings
from poetic.settings.options import SettingsOptions


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    template_subparser = subparsers.add_parser(
        Subparser.init.value, help="create/update template"
    )
    add_template_arguments(template_subparser)

    micro_functionality_subparser = subparsers.add_parser(
        Subparser.add.value, help="add functionality to existing repo"
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

    if command == Subparser.install:
        install_setup = InstallSetup(Path.cwd(), InstallSettings(**settings_args))
        install_setup.install()
    else:
        setup_settings = SettingsOptions(**{"settings": settings_args}).settings
        poetic_factory = PoeticFactory()
        setupper = poetic_factory.build(setup_settings)

        try:
            setupper.launch()
        except PoeticException as e:
            logg.error(str(e))
            return


if __name__ == "__main__":
    main()
