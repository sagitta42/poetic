import json
from pathlib import Path
from typing import Optional, Self
from pydantic import BaseModel, Field, model_validator
import pytest
import sys
import os

from dotenv import dotenv_values

from poetiq.logger import logg

env_config = dotenv_values()
is_debug = env_config.get("DEBUG", "").lower() in ("true", "1")
test_eann = env_config.get("TEST_EANN", "").lower() in ("true", "1")

if is_debug:
    path_current = os.path.dirname(__file__)
    # make src modules accessible in all test_* files without having to install the package
    path_to_src = os.path.join(path_current, "..", "src")
    path_to_src_absolute = os.path.abspath(path_to_src)
    sys.path.insert(0, path_to_src_absolute)

PATH_TO_ASSETS = Path(os.path.dirname(__file__))
PATH_TO_CONFIGS = PATH_TO_ASSETS / "configs"


def get_test_case_dict(filename: str) -> dict:
    """
    Get test case dict from given config filename (with extension).
    """
    filepath = PATH_TO_CONFIGS / filename
    with open(filepath) as f:
        ret = json.load(f)
    return ret


class SetupTestCase(BaseModel):
    settings: dict = Field(description="Setup settings")
    dir_name_: Optional[str] = Field(
        default=None,
        description="Directory of setup; optional for template setup",
        alias="dir_name",
    )
    overwrite: bool = Field(
        description="Overwrite template setup if directory already exists"
    )

    @property
    def dir_name(self) -> str:
        return self.dir_name_ or self.settings["name"]

    @model_validator(mode="after")
    def check_dir(self) -> Self:
        if self.dir_name_ is None and not self.is_template:
            raise ValueError(
                "Provide test setup directory name for non-template test cases!"
            )
        return self

    @property
    def is_template(self) -> bool:
        # FIXME: determines if test case is temlate or not based of "name"
        return "name" in self.settings


def create_setup_test_cases(
    filenames: list[str] | None = None,
    template_only: bool = False,
    overwrite: bool = False,
):
    """
    Create setup test cases based on given config filenames (with extension).

    If no names given, use all test configs.
    """
    config_filenames = filenames or os.listdir(PATH_TO_CONFIGS)

    ret = []
    for fname in config_filenames:
        test_case_dict = get_test_case_dict(fname)
        logg.debug(f"Test case file: {fname}")
        template_test_case = SetupTestCase(**test_case_dict, overwrite=overwrite)
        if template_only and not template_test_case.is_template:
            continue

        ret.append(
            pytest.param(
                template_test_case, id=f"{Path(fname).stem}_overwrite-{overwrite}"
            )
        )
    return ret


@pytest.fixture(params=create_setup_test_cases(template_only=False, overwrite=True))
def test_case_setup(request) -> SetupTestCase:
    return request.param


@pytest.fixture(params=create_setup_test_cases(template_only=True, overwrite=True))
def test_case_template(request) -> SetupTestCase:
    return request.param
