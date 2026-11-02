import json
import logging

from langchain_core.tools import tool
from sqlalchemy import select
from app.tools.tool_errors import tool_success_response
from app.tools.tool_errors import tool_error_response

from app.database.connection import AsyncSessionLocal
from app.models.evidence import Evidence

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

@tool
async def get_evidence_details(case_id: int, evidence_id: int) -> str:
    """Retrieve specific evidence belonging to a particular courtroom case."""

    if case_id <= 0 or evidence_id <= 0:
        return tool_error_response(
            "get_evidence_details",
            "Invalid case ID or evidence ID",
            case_id
        )

    try:
        async with AsyncSessionLocal() as db:

            result = await db.execute(
                select(Evidence).where(
                    Evidence.id == evidence_id,
                    Evidence.case_id == case_id
                )
            )

            evidence = result.scalar_one_or_none()

            if not evidence:
                return json.dumps({
                    "success": False,
                    "error": "Evidence not found for this case"
                })

            return json.dumps({
                "success": True,
                "data": {
                    "id": evidence.id,
                    "evidence_code": evidence.evidence_code,
                    "case_id": evidence.case_id,
                    "title": evidence.title,
                    "description": evidence.description,
                    "evidence_type": evidence.evidence_type,
                    "content": evidence.content,
                    "origin": evidence.origin,
                    "verification_status": evidence.verification_status
                }
            })

    except SQLAlchemyError:
        logger.exception("Database error retrieving evidence")

        return json.dumps({
            "success": False,
            "error": "Database operation failed"
        })

    except Exception:
        logger.exception("Unexpected error retrieving evidence")

        return json.dumps({
            "success": False,
            "error": "Unexpected error occurred"
        })  


@tool
async def search_case_evidence(case_id: int, keyword: str) -> str:
    """Search evidence belonging to a case by keyword in its title, description, or content."""


    if not keyword or not keyword.strip():
        return tool_error_response(
            "search_case_evidence",
            "Search keyword cannot be empty",
            case_id
        )

    try:

        async with AsyncSessionLocal() as db:
            search_pattern = f"%{keyword}%"

            result = await db.execute(
                select(Evidence).where(
                    Evidence.case_id == case_id,
                    (
                        Evidence.title.ilike(search_pattern)
                        | Evidence.description.ilike(search_pattern)
                        | Evidence.content.ilike(search_pattern)
                    )
                )
            )

            evidence_records = result.scalars().all()

            evidence_data = [
                {
                    "id": item.id,
                    "evidence_code": item.evidence_code,
                    "title": item.title,
                    "description": item.description,
                    "evidence_type": item.evidence_type,
                    "content": item.content,
                    "verification_status": item.verification_status
                }
                for item in evidence_records
            ]

            return json.dumps({
                "case_id": case_id,
                "keyword": keyword,
                "total_matches": len(evidence_data),
                "evidence": evidence_data
            })

    except SQLAlchemyError:
            logger.exception("Database error retrieving evidence")
            return tool_error_response(
                "search_case_evidence",
                "Database operation failed",
                case_id
            )

    except Exception:
        logger.exception("Unexpected error retrieving evidence")
        return tool_error_response(
            "search_case_evidence",
            "Unexpected error occurred",
            case_id
        )

@tool
async def get_case_evidence(case_id: int) -> str:
    """Retrieve all evidence records associated with a specific courtroom case."""

    if case_id <= 0:
        return tool_error_response(
            "get_case_evidence",
            "Invalid case ID. It must be greater than zero.",
            case_id
        )

    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Evidence).where(Evidence.case_id == case_id)
            )

            evidence_records = result.scalars().all()

            evidence_data = [
                {
                    "id": item.id,
                    "case_id": item.case_id,
                    "evidence_code": item.evidence_code,
                    "title": item.title,
                    "description": item.description,
                    "evidence_type": item.evidence_type,
                    "content": item.content,
                    "origin": item.origin,
                    "verification_status": item.verification_status
                }
                for item in evidence_records
            ]

            return tool_success_response({
                "case_id": case_id,
                "total_evidence": len(evidence_data),
                "evidence": evidence_data
            })

    except SQLAlchemyError:
        logger.exception("Database error in get_case_evidence")
        return tool_error_response(
            "get_case_evidence",
            "Unable to retrieve case evidence.",
            case_id
        )