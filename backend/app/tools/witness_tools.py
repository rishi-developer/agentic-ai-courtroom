import json

from langchain_core.tools import tool
from sqlalchemy import select

from app.database.connection import AsyncSessionLocal
from app.models.witness import Witness
from app.tools.tool_errors import tool_error_response
from app.tools.tool_errors import tool_success_response




@tool
async def get_case_witnesses(case_id: int) -> str:
    """Retrieve all witnesses associated with a particular courtroom case."""

    if case_id <= 0:
            return tool_error_response(
                "get_case_witnesses",
                "Invalid case ID",
                case_id
            )
    try: 
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Witness).where(Witness.case_id == case_id)
            )

            witnesses = result.scalars().all()

            witness_data = [
                {
                    "id": witness.id,
                    "case_id": witness.case_id,
                    "name": witness.name,
                    "role": witness.role,
                    "knowledge_profile": witness.knowledge_profile,
                    "original_statement": witness.original_statement
                }
                for witness in witnesses
            ]

            return tool_success_response({
                "case_id": case_id,
                "total_witnesses": len(witness_data),
                "witnesses": witness_data
            })

    except SQLAlchemyError:
            logger.exception("Database error retrieving witnesses")
            return tool_error_response(
                "get_case_witnesses",
                "Database operation failed",
                case_id
            )

    except Exception:
        logger.exception("Unexpected error retrieving witnesses")
        return tool_error_response(
            "get_case_witnesses",
            "Unexpected error occurred",
            case_id
        )


@tool
async def get_witness_details(witness_id: int) -> str:
    """Retrieve detailed information about a specific witness using their witness ID."""

    if witness_id <= 0:
        return tool_error_response(
            "get_witness_details",
            "Invalid witness ID",
            witness_id
        )
    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Witness).where(Witness.id == witness_id)
            )

            witness = result.scalar_one_or_none()

            if not witness:
                return json.dumps({
                    "error": "Witness not found",
                    "witness_id": witness_id
                })

            witness_data = {
                "id": witness.id,
                "case_id": witness.case_id,
                "name": witness.name,
                "role": witness.role,
                "knowledge_profile": witness.knowledge_profile,
                "original_statement": witness.original_statement
            }

            return json.dumps(witness_data)

    except SQLAlchemyError:
        logger.exception("Database error in get_witness_details")

        return tool_error_response(
            "get_witness_details",
            "Database operation failed",
            witness_id
        )

    except Exception:
        logger.exception("Unexpected error in get_witness_details")

    return tool_error_response(
        "get_witness_details",
        "Unexpected error occurred",
        witness_id
    )