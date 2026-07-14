import argparse
from poetic.builder import TemplateBuilder, TemplateType


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str)
    parser.add_argument(
        "--type",
        type=str,
        default=TemplateType.package,
        help="Template type",
        choices=TemplateType.values(),
    )
    parser.add_argument("--update", action="store_true", help="Update existing package")
    args = parser.parse_args()

    template_builder = TemplateBuilder()
    template = template_builder.build(args.name, args.type)

    template.update() if args.update else template.init()


main()
