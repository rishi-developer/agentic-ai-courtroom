from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.case import Case
from app.schemas.case import CaseCreate


async def create_case(db: AsyncSession, case_data: CaseCreate):

    new_case = Case(
        title=case_data.title,
        description=case_data.description,
        case_type=case_data.case_type
    )

    db.add(new_case)

    await db.commit()

    await db.refresh(new_case)

    return new_case


async def get_all_cases(db: AsyncSession):

    result = await db.execute(
        select(Case)
    )

    return result.scalars().all()


async def get_case_by_id(db: AsyncSession, case_id: int):

    result = await db.execute(
        select(Case).where(Case.id == case_id)
    )

    return result.scalar_one_or_none()