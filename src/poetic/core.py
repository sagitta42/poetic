from poetic.api import APISetup
from poetic.package import PackageSetup


def setup_package_template(name: str):
    package = PackageSetup(name)

    package.setup_gitignore()
    package.setup_dotenv_template()

    package.setup_source_files()

    package.setup_tests()
    package.setup_logger()

    package.setup_vscode()
    package.init_commit()

    package.display()


def setup_api_template(name: str):
    api = APISetup(name)

    api.setup_gitignore()
    api.setup_dotenv_template()

    api.setup_subfolders()

    api.display()
