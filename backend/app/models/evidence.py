from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    Text,
    DateTime,
    func
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.case import Case

from sqlalchemy import UniqueConstraint




class Evidence(Base):
    __tablename__ = "evidence"

    __table_args__ = (
    UniqueConstraint(
        "case_id",
        "evidence_code",
        name="uq_case_evidence_code"
    ),
)   

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    case_id: Mapped[int] = mapped_column(
        ForeignKey(f"{Case.__tablename__}.id"),
        nullable=False,
        index=True
    )

    evidence_code: Mapped[str] = mapped_column(
        String(20), nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(200), nullable=False
    )

    description: Mapped[str] = mapped_column(Text, nullable=False)

    evidence_type: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)

    origin: Mapped[str] = mapped_column(
        String(50), default="original", nullable=False
    )

    verification_status: Mapped[str] = mapped_column(
        String(50), default="unverified", nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )