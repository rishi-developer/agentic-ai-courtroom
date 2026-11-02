import json

from langchain_core.tools import tool
from sqlalchemy import select

from app.database.connection import AsyncSessionLocal
from app.models.trial_argument import TrialArgument
from app.models.witness_testimony import WitnessTestimony


@tool
async def get_trial_arguments(trial_id: int) -> str:
    """Retrieve all previous prosecutor and defense arguments from a trial."""

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(TrialArgument)
            .where(TrialArgument.trial_id == trial_id)
            .order_by(TrialArgument.created_at)
        )

        arguments = result.scalars().all()

        argument_data = [
            {
                "id": item.id,
                "agent": item.agent,
                "action": item.action,
                "argument": item.argument,
                "supporting_evidence": json.loads(
                    item.supporting_evidence
                ),
                "challenged_argument": item.challenged_argument,
                "reasoning": item.reasoning
            }
            for item in arguments
        ]

        return json.dumps({
            "trial_id": trial_id,
            "total_arguments": len(argument_data),
            "arguments": argument_data
        })


@tool
async def get_trial_testimonies(trial_id: int) -> str:
    """Retrieve all witness questions and responses from a trial."""

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(WitnessTestimony)
            .where(WitnessTestimony.trial_id == trial_id)
            .order_by(WitnessTestimony.created_at)
        )

        testimonies = result.scalars().all()

        testimony_data = [
            {
                "id": item.id,
                "witness_id": item.witness_id,
                "questioner": item.questioner,
                "question": item.question,
                "response": item.response,
                "knowledge_status": item.knowledge_status,
                "supporting_evidence": json.loads(
                    item.supporting_evidence
                ),
                "contradicts_previous_statement":
                    item.contradicts_previous_statement
            }
            for item in testimonies
        ]

        return json.dumps({
            "trial_id": trial_id,
            "total_testimonies": len(testimony_data),
            "testimonies": testimony_data
        })