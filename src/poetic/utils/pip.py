from pathlib import Path


def get_package_info(pip_str: str, split_str: str) -> tuple[str, str]:
    """
    Get package information splitting dependency string by given split string.

    E.g. package==1.2.3, package @ path
    """
    package, info = [component.strip() for component in pip_str.split(split_str)]
    return package, info


def get_package_source(pip_str: str) -> tuple[str, str]:
    """
    Extract package name and source from "package @ source" pip string.

    Remove final "/" in filepath.
    """
    package, path = get_package_info(pip_str, "@")
    path = path.removesuffix("/")
    return package, path


def get_package_version(pip_str: str) -> tuple[str, str]:
    """
    Extract package version from "package==1.2.3" pip string.
    """
    ret = get_package_info(pip_str, "==")
    return ret
