import json
import logging
from sqlalchemy.exc import SQLAlchemyError

from langchain_core.tools import tool
from sqlalchemy import select, func

from app.database.connection import AsyncSessionLocal
from app.models.case import Case
from app.models.evidence import Evidence
from app.tools.tool_errors import tool_error_response



@tool
async def submit_new_evidence(
    case_id: int,
    title: str,
    description: str,
    evidence_type: str,
    content: str
) -> str:
    """Submit new user-provided evidence to an existing courtroom case."""


    if case_id <= 0:
        return tool_error_response(
            "submit_new_evidence",
            "Invalid case ID",
            case_id
        )

    if not title.strip() or not description.strip() or not content.strip():
        return tool_error_response(
            "submit_new_evidence",
            "Title, description and content cannot be empty",
            case_id
        )

    try:
        async with AsyncSessionLocal() as db:

        # Validate case
            case_result = await db.execute(
                select(Case).where(Case.id == case_id)
            )

            case = case_result.scalar_one_or_none()

            if not case:
                return json.dumps({
                    "error": "Case not found",
                    "case_id": case_id
                })

            # Generate next evidence code
            count_result = await db.execute(
                select(func.count(Evidence.id)).where(
                    Evidence.case_id == case_id
                )
            )

            evidence_count = count_result.scalar_one()

            evidence_code = f"E{evidence_count + 1:03d}"

            # Create evidence record
            evidence = Evidence(
                case_id=case_id,
                evidence_code=evidence_code,
                title=title,
                description=description,
                evidence_type=evidence_type,
                content=content,
                origin="user_submitted",
                verification_status="unverified"
            )

            db.add(evidence)
            await db.commit()
            await db.refresh(evidence)

            return json.dumps({
                "message": "Evidence submitted successfully",
                "evidence": {
                    "id": evidence.id,
                    "evidence_code": evidence.evidence_code,
                    "case_id": evidence.case_id,
                    "title": evidence.title,
                    "origin": evidence.origin,
                    "verification_status": evidence.verification_status
                }
            })
    except Exception:
        await db.rollback()
        logger.exception("Unexpected error submitting evidence")

        return tool_error_response(
            "submit_new_evidence",
            "Unexpected error occurred",
            case_id
    )