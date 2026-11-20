
from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    Text,
    DateTime,
    UniqueConstraint,
    func
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Verdict(Base):
    __tablename__ = "verdicts"

    __table_args__ = (
        UniqueConstraint("trial_id", name="uq_verdict_trial"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    trial_id: Mapped[int] = mapped_column(
        ForeignKey("trials.id"),
        nullable=False,
        index=True
    )

    outcome: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    accused: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    prosecution_assessment: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    defense_assessment: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    evidence_considered: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="[]"
    )

    reasoning: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    unresolved_questions: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="[]"
    )

    limitations: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="[]"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
