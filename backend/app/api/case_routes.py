from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.schemas.case import CaseCreate, CaseResponse
from app.services.case_service import (
    create_case,
    get_all_cases,
    get_case_by_id
)

router = APIRouter(
    prefix="/api/cases",
    tags=["Cases"]
)


@router.post(
    "/",
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_new_case(
    case_data: CaseCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_case(db, case_data)


@router.get(
    "/",
    response_model=list[CaseResponse]
)
async def list_cases(
    db: AsyncSession = Depends(get_db)
):
    return await get_all_cases(db)


@router.get(
    "/{case_id}",
    response_model=CaseResponse
)
async def retrieve_case(
    case_id: int,
    db: AsyncSession = Depends(get_db)
):
    case = await get_case_by_id(db, case_id)

    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )

    return case