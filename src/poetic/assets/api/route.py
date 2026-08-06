from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas.dummy import DummyRequest, DummyResponse

from app.services.dummy import dummy_service
from core.db import get_db
from core.models.example import Example

router = APIRouter()


@router.post("/check_answer", response_model=DummyResponse)
def check_answer(payload: DummyRequest, db: Session = Depends(get_db)) -> DummyResponse:
    is_correct = dummy_service.check_answer(payload.foo)
    entry = db.scalar(select(Example).where(Example.id == payload.foo))
    message = (
        "the answer is correct!"
        if is_correct
        else f"the answer is not correct; true answer is {dummy_service.get_true_answer()}"
    )
    if entry is not None:
        message = f"{entry.name}: {message}"
    ret = DummyResponse(message=message)
    return ret
