import json

import $PACKAGE.foo as foo
from $PACKAGE.logger import logg
from $PACKAGE.models import MyBaseModel

from tests.conftest import PATH_TO_CONFIGS

def test_foo():
    input = 21
    output = foo.answer(input)
    the_answer = 42
    assert output == the_answer, f"Test failed because answer not {the_answer}"


def test_mybasemodel():
    class TestModel(MyBaseModel):
        answer: int
        message: str

    path_to_model = PATH_TO_CONFIGS / "test_model.json"
    with open(path_to_model) as f:
        test_model = TestModel(**json.load(f))

    logg.info("Test model")
    test_model.display()