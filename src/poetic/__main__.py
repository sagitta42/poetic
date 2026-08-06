import argparse
from poetic.cli import add_microfunctionality_arguments, add_template_arguments
from poetic.factory import PoeticFactory
from poetic.exceptions import PoeticException
from poetic.logger import logg
from poetic.settings.options import SettingsOptions


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    template_subparser = subparsers.add_parser(
        "template", help="create/update template"
    )
    add_template_arguments(template_subparser)

    micro_functionality_subparser = subparsers.add_parser(
        "add", help="add functionality to existing repo"
    )
    add_microfunctionality_arguments(micro_functionality_subparser)

    args = parser.parse_args()
    logg.debug(vars(args))

    settings_args = vars(args).copy()

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
