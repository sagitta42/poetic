import argparse
from poetic.api import APITemplate
from poetic.package import PackageTemplate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str)
    parser.add_argument(
        "--package", action="store_true", help="Initialize package template"
    )
    parser.add_argument(
        "--api", action="store_true", help="Initialize API service template"
    )
    args = parser.parse_args()

    if (not args.package and not args.api) or (args.package and args.api):
        parser.error(
            "Provide either --package or --api flag for the type of poetic init"
        )

    if args.package:
        template_class = PackageTemplate
    elif args.api:
        template_class = APITemplate
    else:
        raise NotImplementedError

    template = template_class(args.name)
    template.setup()


main()
