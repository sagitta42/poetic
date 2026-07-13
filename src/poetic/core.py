from poetic.logger import logg
from poetic.package import Package
from poetic.tree import tree


def setup_package_template(name: str):

    package = Package(name)

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
    raise NotImplementedError("API init with poetic not implemented yet")

