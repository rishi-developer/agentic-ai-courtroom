from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.case import Case


class Witness(Base):
    __tablename__ = "witnesses"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    case_id: Mapped[int] = mapped_column(
        ForeignKey(f"{Case.__tablename__}.id"),
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(150), nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    knowledge_profile: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    original_statement: Mapped[str] = mapped_column(
        Text, nullable=False
    )