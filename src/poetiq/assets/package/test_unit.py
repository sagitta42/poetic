from $PACKAGE.foo import is_answer
from $PACKAGE.logger import logg

from tests.conftest import PATH_TO_CONFIGS

def test_foo():
    input = 42
    output = is_answer(input)
    assert output, f"Test failed because {input} is not the answer"


def test_model(test_case_example):
    logg.info("Example model")
    test_case_example.display()