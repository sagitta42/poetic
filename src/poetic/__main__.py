import argparse
from poetic.builder import TemplateBuilder, TemplateSettings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, help=TemplateSettings.description("name"))
    parser.add_argument(
        "--type",
        type=str,
        default=TemplateSettings.default("type"),
        help=TemplateSettings.description("type"),
        choices=TemplateSettings.options("type"),
    )

    parser.add_argument("--update", action="store_true", help="Update existing package")
    args = parser.parse_args()

    template_settings = TemplateSettings(name=args.name, type=args.type)
    template_builder = TemplateBuilder()
    template = template_builder.build(template_settings)

    template.update() if args.update else template.init()


main()
