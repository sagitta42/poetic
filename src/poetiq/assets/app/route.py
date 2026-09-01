from fastapi import APIRouter

from app.schemas.dummy import DummyRequest, DummyResponse

from app.services.dummy import dummy_service

router = APIRouter()


@router.post("/check_answer", response_model=DummyResponse)
def check_answer(payload: DummyRequest) -> DummyResponse:
    is_correct = dummy_service.check_answer(payload.foo)
    message = (
        "the answer is correct!"
        if is_correct
        else f"the answer is not correct; true answer is {dummy_service.get_true_answer()}"
    )
    ret = DummyResponse(message=message)
    return ret
