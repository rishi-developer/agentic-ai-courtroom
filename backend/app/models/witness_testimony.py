from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, Text, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class WitnessTestimony(Base):
    __tablename__ = "witness_testimonies"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    trial_id: Mapped[int] = mapped_column(
        ForeignKey("trials.id"),
        nullable=False,
        index=True
    )

    witness_id: Mapped[int] = mapped_column(
        ForeignKey("witnesses.id"),
        nullable=False,
        index=True
    )

    questioner: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    question: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    response: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    knowledge_status: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    supporting_evidence: Mapped[str] = mapped_column(
        Text, nullable=False, default="[]"
    )

    contradicts_previous_statement: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )