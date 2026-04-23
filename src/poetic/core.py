import os
from pathlib import Path

from poetic.tree import tree


def setup_package_template(package_name: str):
    print(f"Setting up package: {package_name}")
    os.system(f"poetry new {package_name}")

    package_path: Path = Path(package_name)
    path_to_src: Path = package_path / "src" / package_name
    f = open(path_to_src / "core.py", "w")
    f.close()

    with open(path_to_src / "__init__.py", "a") as f:
        f.write("from core import *")

    for line in tree(package_path):
        print(line)
