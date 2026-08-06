from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base


class Example(Base):
    __tablename__ = "examples"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
