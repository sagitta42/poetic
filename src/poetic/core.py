from poetic.logger import logg
from poetic.package import Package
from poetic.tree import tree


def setup_package_template(package_name: str):

    package = Package(package_name)

    package.setup_gitignore()
    package.setup_source_files()
    package.setup_tests()
    package.setup_logger()
    package.init_commit()

    logg.info(package.name)
    for line in tree(package.path):
        logg.info(line)
