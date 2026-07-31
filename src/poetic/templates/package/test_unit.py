import $PACKAGE.foo as foo
from $PACKAGE.logger import logg
from $PACKAGE.models import MyBaseModel


def test_foo():
    input = 21
    output = foo.answer(input)
    the_answer = 42
    assert output == the_answer, f"Test failed because answer not {the_answer}"


def test_mybasemodel():
    class TestModel(MyBaseModel):
        answer: int
        message: str

    test_model = TestModel(answer=42, message="The answer to the question of life, universe, and everything")
    logg.info("Test model")
    test_model.display()