import sys
import os

# TODO: in DEBUG env only
# make src modules accessible in all test_* files without having to install the package
path_current = os.path.dirname(__file__)
path_to_src = os.path.join(path_current, "..", "src")
path_to_src_absolute = os.path.abspath(path_to_src)

sys.path.insert(0, path_to_src_absolute)
