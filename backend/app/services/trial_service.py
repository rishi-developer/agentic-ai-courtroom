
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.case import Case
from app.models.trial import Trial


async def create_trial(db: AsyncSession, case_id: int):

    case = await db.get(Case, case_id)

    if not case:
        raise ValueError(f"Case {case_id} does not exist")

    trial = Trial(
        case_id=case_id,
        status="pending"
    )

    db.add(trial)
    await db.commit()
    await db.refresh(trial)

    return trial
