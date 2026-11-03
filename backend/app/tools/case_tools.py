import json
import logging

from langchain_core.tools import tool
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import AsyncSessionLocal
from app.models.case import Case
from app.tools.tool_errors import tool_error_response
from app.tools.tool_errors import tool_success_response
from app.models.suspect import Suspect


logger = logging.getLogger(__name__)


@tool
async def get_case_details(case_id: int) -> str:
    """Retrieve complete details of a courtroom case using its case ID."""

    if case_id <= 0:
        return tool_error_response(
            "get_case_details",
            "Invalid case ID",
            case_id
        )

    try:
        async with AsyncSessionLocal() as db:

            result = await db.execute(
                select(Case).where(Case.id == case_id)
            )

            case = result.scalar_one_or_none()

            if not case:
                return tool_error_response(
                    "get_case_details",
                    "Case not found",
                    case_id
                )

            case_data = {
                "id": case.id,
                "title": case.title,
                "description": case.description,
                "case_type": case.case_type,
                "status": case.status,
                "created_at": (
                    case.created_at.isoformat()
                    if case.created_at else None
                )
            }

            return json.dumps({
                "success": True,
                "data": case_data
            })

    except SQLAlchemyError:
        logger.exception("Database error in get_case_details")

        return tool_error_response(
            "get_case_details",
            "Database operation failed",
            case_id
        )

    except Exception:
        logger.exception("Unexpected error in get_case_details")

        return tool_error_response(
            "get_case_details",
            "Unexpected error occurred",
            case_id
        )



@tool
async def get_case_suspects(case_id: int) -> str:
    """
    Retrieve all suspects associated with a particular
    courtroom case using its case ID.
    """

    if case_id <= 0:
        return tool_error_response(
            "get_case_suspects",
            "Invalid case ID",
            case_id
        )

    try:
        async with AsyncSessionLocal() as db:



            result = await db.execute(
                select(Suspect).where(
                    Suspect.case_id == case_id
                )
            )

            suspects = result.scalars().all()

            suspect_data = [
                {
                    "id": suspect.id,
                    "case_id": suspect.case_id,
                    "name": suspect.name,
                    "role": suspect.role,
                    "description": suspect.description
                }
                for suspect in suspects
            ]

            return json.dumps({
                "case_id": case_id,
                "total_suspects": len(suspect_data),
                "suspects": suspect_data
            })

    except SQLAlchemyError:
        logger.exception("Database error retrieving suspects")
        return tool_error_response(
            "get_case_suspects",
            "Database operation failed",
            case_id
        )

    except Exception:
        logger.exception("Unexpected error retrieving suspects")
        return tool_error_response(
            "get_case_suspects",
            "Unexpected error occurred",
            case_id
        )