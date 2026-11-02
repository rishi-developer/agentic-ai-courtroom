from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class TrialArgument(Base):
    __tablename__ = "trial_arguments"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    trial_id: Mapped[int] = mapped_column(
        ForeignKey("trials.id"),
        nullable=False,
        index=True
    )

    agent: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    action: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    argument: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    supporting_evidence: Mapped[str] = mapped_column(
        Text, nullable=False, default="[]"
    )

    challenged_argument: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    reasoning: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )