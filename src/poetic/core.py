import os
from pathlib import Path


def setup_package_template(package_name: str):
    print(f"Setting up package: {package_name}")
    os.system(f"poetry new {package_name}")

    path_to_src: Path = Path(package_name) / "src" / package_name
    f = open(path_to_src / "core.py", "w")
    f.close()

    with open(path_to_src / "__init__.py", "a") as f:
        f.write("from core import *")
