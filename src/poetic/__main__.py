import argparse
from poetic.builder import TemplateBuilder, BaseTemplateSettings
from poetic.exceptions import PoeticException
from poetic.logger import logg
from poetic.settings import (
    APITemplateSettings,
    DBSettings,
    DBType,
    PackageTemplateSettings,
    SettingsCrutch,
)


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


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    
    template_subparser = subparsers.add_parser(
        "template", help="create/update template"
    )
    add_template_arguments(template_subparser)

    args = parser.parse_args()
    logg.debug(vars(args))

    settings_args = vars(args).copy()
    settings_args.pop("update")

    template_settings = SettingsCrutch(**{"settings": settings_args}).settings
    template_builder = TemplateBuilder()
    template = template_builder.build(template_settings)

    try:
        template.update() if args.update else template.init()
    except PoeticException as e:
        logg.error(str(e))
        return


if __name__ == "__main__":
    main()
