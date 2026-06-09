import sys
import os

from dotenv import dotenv_values

env_config = dotenv_values()
is_debug = env_config.get("DEBUG", "").lower() in ("true", "1")
test_eann = env_config.get("TEST_EANN", "").lower() in ("true", "1")

if is_debug:
    path_current = os.path.dirname(__file__)
    # make src modules accessible in all test_* files without having to install the package
    path_to_src = os.path.join(path_current, "..", "src")
    path_to_src_absolute = os.path.abspath(path_to_src)
    sys.path.insert(0, path_to_src_absolute)