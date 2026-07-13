import argparse
from poetic.core import setup_api_template, setup_package_template


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
        setup_package_template(args.name)
    elif args.api:
        setup_api_template(args.name)
    else:
        raise NotImplementedError


main()
