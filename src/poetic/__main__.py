import argparse
from pathlib import Path
from poetic.cli import (
    Subparser,
    add_install_arguments,
    add_microfunctionality_arguments,
    add_new_template_arguments,
)
from poetic.factory import PoeticFactory
from poetic.exceptions import PoeticException
from poetic.install import InstallSetup
from poetic.logger import logg
from poetic.settings.install import InstallSettings
from poetic.settings.options import SettingsOptions
from poetic.template.builder import TemplateBuilder


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    new_template_subparser = subparsers.add_parser(
        Subparser.new.value, help="create/update template"
    )
    add_new_template_arguments(new_template_subparser)

    subparsers.add_parser(
        Subparser.update.value, help="update current template with new poetic updates"
    )

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

    try:

        if command == Subparser.update:
            logg.info("Update subparser will be here")
            template_builder = TemplateBuilder()
            setupper = template_builder.find()
            setupper.update()
        elif command == Subparser.install:
            install_setup = InstallSetup(Path.cwd(), InstallSettings(**settings_args))
            install_setup.install()
        else:
            setup_settings = SettingsOptions(**{"settings": settings_args}).settings
            poetic_factory = PoeticFactory()
            setupper = poetic_factory.build(setup_settings)
            setupper.launch()

    except PoeticException as e:
        logg.error(str(e))
        return


if __name__ == "__main__":
    main()
