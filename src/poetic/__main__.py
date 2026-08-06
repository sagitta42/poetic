import argparse
from poetic.factory import PoeticFactory, BaseTemplateSettings
from poetic.exceptions import PoeticException
from poetic.logger import logg
from poetic.settings.options import SettingsCrutch
from poetic.settings.item import DBSettings, DBType, SetupType
from poetic.settings.template import APITemplateSettings, PackageTemplateSettings


def add_template_arguments(parser: argparse.ArgumentParser):
    """
    Add arguments for template creation/update to given parser.
    """
    parser.add_argument("name", type=str, help=BaseTemplateSettings.description("name"))
    parser.add_argument(
        "--type",
        type=str,
        default=BaseTemplateSettings.default("type"),
        help=BaseTemplateSettings.description("type"),
        choices=BaseTemplateSettings.options("type"),
    )
    parser.add_argument(
        "--db",
        type=str,
        nargs="?",
        const=DBType.sqlite.value,
        default=DBType.none.value,
        choices=DBSettings.options("db"),
        help=APITemplateSettings.description("db"),
    )
    parser.add_argument(
        "--settings",
        action="store_true",
        help=PackageTemplateSettings.description("settings"),
    )

    parser.add_argument("--update", action="store_true", help="Update existing package")


def add_microfunctionality_arguments(parser: argparse.ArgumentParser):
    """
    Add arguments for adding functionality to given parser
    """
    parser.add_argument(
        "type",
        type=str,
        choices=[SetupType.vscode.value, SetupType.gitignore.value],
        help="Type of functionality",
    )


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

    setup_settings = SettingsCrutch(**{"settings": settings_args}).settings

    poetic_factory = PoeticFactory()
    setupper = poetic_factory.build(setup_settings)

    try:
        setupper.launch()
    except PoeticException as e:
        logg.error(str(e))
        return


if __name__ == "__main__":
    main()
