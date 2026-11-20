
from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    DateTime,
    func
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Trial(Base):
    __tablename__ = "trials"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    case_id: Mapped[int] = mapped_column(
        ForeignKey("cases.id"),
        nullable=False,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending"
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
