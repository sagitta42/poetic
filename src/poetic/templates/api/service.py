from core.dummy import UniverseLogic


class DummyService:
    """
    Dummy service.
    """

    def __init__(self) -> None:
        self._universe_logic = UniverseLogic()

    def get_true_answer(self) -> int:
        return self._universe_logic.true_answer

    def check_answer(self, answer: int) -> bool:
        """
        Check if the answer to the question of life, universe, and everything is correct.
        """
        ret = self._universe_logic.is_answer_correct(answer)
        return ret


dummy_service = DummyService()
