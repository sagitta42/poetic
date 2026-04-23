import $PACKAGE.foo as foo


def test_foo():
    input = 21
    output = foo.answer(input)
    the_answer = 42
    assert output == the_answer, f"Test failed because answer not {the_answer}"
