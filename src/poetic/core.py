from poetic.logger import logg
from poetic.package_setup import PackageSetup
from poetic.tree import tree


def setup_package_template(package_name: str):

    package_setup = PackageSetup(package_name)

    package_setup.setup_gitignore()
    package_setup.setup_source_files()
    package_setup.setup_tests()
    package_setup.setup_logger()

    for line in tree(package_setup.path):
        logg.info(line)
