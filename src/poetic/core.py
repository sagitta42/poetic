from poetic.api import APISetup
from poetic.logger import logg
from poetic.package import PackageSetup
from poetic.tree import tree


def setup_package_template(name: str):
    package = PackageSetup(name)

    package.setup_gitignore()
    package.setup_dotenv_template()

    package.setup_source_files()

    package.setup_tests()
    package.setup_logger()

    package.setup_vscode()
    package.init_commit()

    logg.info(package.name)
    for line in tree(package.path):
        logg.info(line)


def setup_api_template(name: str):
    api = APISetup(name)
