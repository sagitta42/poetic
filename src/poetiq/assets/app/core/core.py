class UniverseLogic:
    """
    Engine that handles the question of life, universe, and everything.
    """

    def __init__(self) -> None:
        self._true_answer: int = 42

    @property
    def true_answer(self) -> int:
        return self._true_answer

    def is_answer_correct(self, answer: int) -> bool:
        ret = answer == self._true_answer
        return ret
